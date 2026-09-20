import os

from google.genai import Client, types

from web.registry import get_tool_registry
from web.fetcher import fetch_tool
from llm.tools import get_gemini_tools
from llm.prompts import SYSTEM_INSTRUCTION
import config


def run_agent(query: str) -> dict:
    """Run the WebLens Gemini function-calling agent."""

    api_key = os.getenv("GEMINI_API_KEY") or getattr(
        config, "GEMINI_API_KEY", None
    )

    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured.")

    model = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
    client = Client(api_key=api_key)

    registry = get_tool_registry()
    tools = get_gemini_tools()

    # ---------------------------------------------------------
    # STEP 1: Ask Gemini which registered source(s) to use.
    # ---------------------------------------------------------
    config_for_tool_call = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=tools,
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        temperature=0.0,
    )

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=query)],
    )

    response = client.models.generate_content(
        model=model,
        contents=user_content,
        config=config_for_tool_call,
    )

    # ---------------------------------------------------------
    # If Gemini doesn't select a tool.
    # ---------------------------------------------------------
    if not response.function_calls:
        answer = response.text

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

    # ---------------------------------------------------------
    # STEP 2: Process ALL function calls selected by Gemini.
    # ---------------------------------------------------------
    function_response_parts = []
    tool_names = []
    source_urls = []

    for function_call in response.function_calls:

        # Find matching registry entry.
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

        tool_name = source_info["name"]
        source_url = source_info["url"]

        tool_names.append(tool_name)
        source_urls.append(source_url)

        # -----------------------------------------------------
        # STEP 3: Fetch live content from the selected source.
        # -----------------------------------------------------
        content = fetch_tool(source_url)

        # -----------------------------------------------------
        # STEP 4: Create function response for Gemini.
        # -----------------------------------------------------
        function_response_parts.append(
            types.Part.from_function_response(
                name=function_call.name,
                response={
                    "result": content,
                },
            )
        )

    # If none of the selected tools matched our registry.
    if not function_response_parts:
        return {
            "answer": "The requested source could not be identified.",
            "tool_name": None,
            "source_url": None,
        }

    # ---------------------------------------------------------
    # STEP 5: Preserve Gemini's original function-call turn.
    # ---------------------------------------------------------
    function_call_content = response.candidates[0].content

    # Gemini's API expects the function responses in a user turn.
    function_response_content = types.Content(
        role="user",
        parts=function_response_parts,
    )

    # ---------------------------------------------------------
    # STEP 6: Ask Gemini to produce the grounded answer.
    # ---------------------------------------------------------
    final_response = client.models.generate_content(
        model=model,
        contents=[
            user_content,
            function_call_content,
            function_response_content,
        ],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.0,
        ),
    )

    answer = final_response.text

    if not answer:
        answer = (
            "The requested information could not be found "
            "in the provided website content."
        )

    # ---------------------------------------------------------
    # STEP 7: Return answer + source information.
    # ---------------------------------------------------------
    return {
        "answer": answer,
        "tool_name": ", ".join(tool_names),
        "source_url": ", ".join(source_urls),
    }