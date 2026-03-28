from google.genai import types
from openai.types.chat import ChatCompletionToolParam

from .get_file_content import (
    get_file_content,
    schema_get_file_content,
    tool_get_file_content,
)
from .get_files_info import get_files_info, schema_get_files_info, tool_get_files_info
from .run_python_file import (
    run_python_file,
    schema_run_python_file,
    tool_run_python_file,
)
from .write_file import schema_write_file, tool_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

available_tools: list[ChatCompletionToolParam] = [tool_get_file_content, tool_get_files_info, tool_run_python_file, tool_write_file]

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(function_call_part, verbose=False):
    if verbose:
        print(
            f"Calling function : {function_call_part.name}({function_call_part.args})"
        )
    else:
        print(f"Calling function : {function_call_part.name}")

    if function_map[function_call_part.name]:
        results = function_map[function_call_part.name](
            working_dir=".", **function_call_part.args
        )
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name, response={"response": results}
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown functiona {function_call_part.name}"},
                )
            ],
        )
