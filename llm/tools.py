from google.genai import types

from web.registry import get_tool_registry


def get_gemini_tools() -> list[types.Tool]:
    """
    Create Gemini function declarations for all registered WebLens sources.

    Gemini uses these descriptions to decide which trusted college
    source is relevant to the user's question.
    """

    registry = get_tool_registry()
    function_declarations = []

    for source_id, data in registry.items():
        name = source_id.replace("-", "_")

        description = (
            f"Fetch information from {data['name']}. "
            f"{data.get('description', '')}"
        )

        function_declarations.append(
            types.FunctionDeclaration(
                name=name,
                description=description,
            )
        )

    if not function_declarations:
        return []

    return [
        types.Tool(
            function_declarations=function_declarations
        )
    ]