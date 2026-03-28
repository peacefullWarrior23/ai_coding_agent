import os
import subprocess

from google.genai import types
from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel, Field


def run_python_file(working_dir, python_file: str, args=[]):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, python_file))
    if not abs_file_path.startswith(abs_working_dir):
        return (
            f"Error : File {python_file} is not under working directory {working_dir}"
        )
    if not os.path.isfile(abs_file_path):
        return f"Error : File {python_file} is not actually a file"
    if not python_file.endswith(".py"):
        return f"Error : File {python_file} is not actually a Python file"

    try:
        final_args = [
            "python3",
            abs_file_path,
        ]
        final_args.extend(args)
        output = subprocess.run(
            final_args, cwd=abs_working_dir, timeout=30, capture_output=True
        )
        resonse_str = f"""
    [STDOUT]: {output.stdout}
    [STDERR]: {output.stderr}
"""
        if output.stderr == "" and output.stdout == "":
            return "WARNING: Python file outputted nothing"
        if output.returncode != 0:
            resonse_str += f"WARNING: python file run returned code {output.returncode}"
        return resonse_str
    except Exception as e:
        return f"Error: Failed to run python file {abs_file_path}, {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="""Runs the given python file witht the python3 interpreter and returns the response.
    The function also accepts additional CLI arguments as optional array and passes them on to the python file run process. 
    If accessing or running the file fails, it prints out 'Error : ' followed by the error details""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "python_file": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of strings to be used as arguments for the python file run",
                items=types.Schema(
                    type=types.Type.STRING,
                ),
            ),
        },
    ),
)


class RunPythonFile(BaseModel):
    python_file: str = Field(
        description="Path to the python file relative to the working directory."
    )
    args: list[str] = Field(
        description="An optional array of strings to be used as arguments for the python file run"
    )


tool_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the given python file witht the python3 interpreter and returns the response.The function also accepts additional CLI arguments as optional array and passes them on to the python file run process. If accessing or running the file fails, it prints out 'Error : ' followed by the error details",
        "parameters": RunPythonFile.model_json_schema(),
    },
}
