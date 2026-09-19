from google.genai import types
from web.registry import get_tool_registry

def get_gemini_tools() -> list[types.Tool]:
    """
    Creates Gemini callable tools corresponding to the registered WebLens sources.
    """
    registry = get_tool_registry()
    function_declarations = []
    
    for source_id, data in registry.items():
        name = source_id.replace('-', '_')
        desc = f"Fetch information from {data['name']}. {data.get('description', '')}"
        
        function_declarations.append(
            types.FunctionDeclaration(
                name=name,
                description=desc,
            )
        )
        
    if not function_declarations:
        return []
        
    return [types.Tool(function_declarations=function_declarations)]
