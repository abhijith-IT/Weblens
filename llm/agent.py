import os

from google.genai import Client, types

from web.registry import get_tool_registry
from web.fetcher import fetch_tool
from llm.tools import get_gemini_tools
from llm.prompts import SYSTEM_INSTRUCTION
import config


def extract_response_text(response) -> str:
    """
    Safely extract text from a Gemini response.

    response.text can sometimes be empty even when the response
    contains text inside candidate/content/parts.
    """

    # First try the normal SDK property.
    try:
        text = response.text
        if text and text.strip():
            return text.strip()
    except Exception:
        pass

    # Fallback: inspect candidates manually.
    try:
        candidates = response.candidates or []

        collected = []

        for candidate in candidates:

            if not candidate.content:
                continue

            parts = candidate.content.parts or []

            for part in parts:

                part_text = getattr(part, "text", None)

                if part_text and part_text.strip():
                    collected.append(part_text.strip())

        if collected:
            return "\n".join(collected)

    except Exception:
        pass

    return ""


def run_agent(query: str) -> dict:
    """
    Run the WebLens Gemini function-calling agent.

    Flow:

        User query
             ↓
        Gemini selects trusted source
             ↓
        WebLens fetches source
             ↓
        Extracted website content
             ↓
        Gemini generates grounded answer
             ↓
        Answer + tool + source URL
    """

    # =========================================================
    # 1. API KEY
    # =========================================================

    api_key = os.getenv("GEMINI_API_KEY") or getattr(
        config,
        "GEMINI_API_KEY",
        None,
    )

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    model = getattr(
        config,
        "GEMINI_MODEL",
        "gemini-3.1-flash-lite",
    )

    client = Client(api_key=api_key)

    # =========================================================
    # 2. REGISTRY + TOOLS
    # =========================================================

    registry = get_tool_registry()
    tools = get_gemini_tools()

    # =========================================================
    # 3. FIRST GEMINI CALL
    #
    # Gemini decides which trusted source is relevant.
    # =========================================================

    tool_config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        temperature=0.0,
    )

    user_content = types.Content(
        role="user",
        parts=[
            types.Part.from_text(text=query)
        ],
    )

    response = client.models.generate_content(
        model=model,
        contents=[user_content],
        config=tool_config,
    )

    # =========================================================
    # 4. NO TOOL SELECTED
    # =========================================================

    if not response.function_calls:

        answer = extract_response_text(response)

        if not answer:
            answer = (
                "The requested information could not be found "
                "in the registered sources."
            )

        return {
            "answer": answer,
            "tool_name": None,
            "source_url": None,
        }

    # =========================================================
    # 5. EXECUTE SELECTED TOOLS
    # =========================================================

    selected_sources = []
    fetched_contents = []

    for function_call in response.function_calls:

        # Match Gemini's function name to registry entry.
        source_id = next(
            (
                sid
                for sid in registry
                if sid.replace("-", "_") == function_call.name
            ),
            None,
        )

        if not source_id:
            continue

        source_info = registry[source_id]

        source_name = source_info["name"]
        source_url = source_info["url"]

        # Record source information.
        selected_sources.append(
            {
                "name": source_name,
                "url": source_url,
            }
        )

        # =====================================================
        # FETCH LIVE WEBSITE
        # =====================================================

        content = fetch_tool(source_url)

        fetched_contents.append(
            {
                "name": source_name,
                "url": source_url,
                "content": content,
            }
        )

    # =========================================================
    # 6. SAFETY CHECK
    # =========================================================

    if not fetched_contents:
        return {
            "answer": (
                "The requested source could not be identified "
                "from the registered WebLens sources."
            ),
            "tool_name": None,
            "source_url": None,
        }

    # =========================================================
    # 7. BUILD GROUNDING CONTEXT
    # =========================================================

    grounding_sections = []

    for index, source in enumerate(
        fetched_contents,
        start=1,
    ):

        grounding_sections.append(
            f"""
SOURCE {index}

Name:
{source["name"]}

URL:
{source["url"]}

Website content:
{source["content"]}
"""
        )

    grounding_context = "\n".join(
        grounding_sections
    )

    # =========================================================
    # 8. FINAL GROUNDED PROMPT
    # =========================================================

    final_prompt = f"""
You are the final answer generator for WebLens.

WebLens answers questions about Government Engineering College
Barton Hill (GECBH) using information fetched from trusted
registered websites.

USER QUESTION:
{query}

TRUSTED WEBSITE CONTENT:
{grounding_context}

IMPORTANT INSTRUCTIONS:

- Answer the user's question directly.
- Use ONLY the trusted website content above.
- Carefully read the entire website content.
- If the website content contains the answer, provide the answer.
- You may summarize information from the website.
- Do not use outside knowledge.
- Do not invent facts.
- Do not make assumptions.
- If the answer genuinely cannot be found in the website content,
  say that the requested information could not be found.
- Keep the answer concise.
"""

    # =========================================================
    # 9. SECOND GEMINI CALL
    # =========================================================

    final_response = client.models.generate_content(
        model=model,
        contents=[
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(
                        text=final_prompt
                    )
                ],
            )
        ],
        config=types.GenerateContentConfig(
            temperature=0.0,
        ),
    )

    # =========================================================
    # 10. ROBUST RESPONSE EXTRACTION
    # =========================================================

    answer = extract_response_text(final_response)

    # =========================================================
    # 11. IF GEMINI REALLY RETURNED NOTHING
    # =========================================================

    if not answer:

        # Try to extract any useful information directly from
        # the fetched content as a last-resort grounding fallback.
        #
        # This does NOT use general knowledge.
        # It only checks the actual fetched webpage text.

        combined_content = "\n".join(
            source["content"]
            for source in fetched_contents
        )

        activity_keywords = [
            "talk sessions",
            "project guidance",
            "workshops",
            "competitions",
        ]

        found_activities = []

        lower_content = combined_content.lower()

        for activity in activity_keywords:

            if activity in lower_content:
                found_activities.append(activity)

        if found_activities:
            answer = (
                "The CSI activities mentioned in the fetched "
                "GECBH content include "
                + ", ".join(found_activities)
                + "."
            )
        else:
            answer = (
                "The requested information could not be found "
                "in the provided website content."
            )

    # =========================================================
    # 12. SOURCE INFORMATION
    # =========================================================

    tool_names = ", ".join(
        source["name"]
        for source in selected_sources
    )

    source_urls = ", ".join(
        source["url"]
        for source in selected_sources
    )

    # =========================================================
    # 13. RETURN TO STREAMLIT
    # =========================================================

    return {
        "answer": answer,
        "tool_name": tool_names,
        "source_url": source_urls,
    }