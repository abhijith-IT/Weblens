import os
from google.genai import Client, types
from web.registry import get_tool_registry
from web.fetcher import fetch_tool
from llm.tools import get_gemini_tools
from llm.prompts import SYSTEM_INSTRUCTION
import config

def run_agent(query: str) -> dict:
    """
    Implements the complete agent loop:
    1. User query -> Gemini chooses tool
    2. fetch_tool()
    3. Fetched content returned to Gemini
    4. Gemini generates final answer
    """
    api_key = os.getenv("GEMINI_API_KEY") or getattr(config, "GEMINI_API_KEY", None)
    model = getattr(config, "GEMINI_MODEL", "gemini-3.6-flash")
    client = Client(api_key=api_key)
    
    registry = get_tool_registry()
    tools = get_gemini_tools()
    
    response = client.models.generate_content(
        model=model,
        contents=query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            tools=tools,
            temperature=0.0
        )
    )
    
    tool_name = None
    source_url = None
    answer = None
    
    if response.function_calls:
        function_call = response.function_calls[0]
        source_id = next(
            (sid for sid in registry if sid.replace('-', '_') == function_call.name), 
            None
        )
        
        if source_id:
            source_info = registry[source_id]
            source_url = source_info['url']
            tool_name = source_info['name']
            
            content = fetch_tool(source_url)
            
            tool_response = types.Part.from_function_response(
                name=function_call.name,
                response={"content": content}
            )
            
            final_response = client.models.generate_content(
                model=model,
                contents=[
                    types.Part.from_text(text=query),
                    response.candidates[0].content,
                    tool_response
                ],
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=0.0
                )
            )
            answer = final_response.text
        else:
            answer = "Error: Invalid tool requested by the model."
    else:
        answer = response.text
        
    return {
        "answer": answer,
        "tool_name": tool_name,
        "source_url": source_url
    }
