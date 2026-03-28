import os

from google.genai import types
from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel, Field

MAX_CHARS = 10000


def get_file_content(working_dir, file_path):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error : File {file_path} is not under working directory {working_dir}"
    if not os.path.isfile(abs_file_path):
        return f"Error : File {file_path} is not actually a file"
    try:
        file_content = ""
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) <= MAX_CHARS:
                file_content += f"..., File truncated at {MAX_CHARS} chars."
        return file_content
    except Exception as e:
        return f"Error : Failed to read contents of file {file_path}, exception : {e}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Provides the file content as a string upto 10000 characters. If reading or accessing the file fails, it prints out 'Error : ' followed by the error details",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory.",
            ),
        },
    ),
)

class GetFileContent(BaseModel):
    file_path: str = Field(description="Path to the file relative to the working directory")

tool_get_file_content: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description" : "Provides the file content as a string upto 10000 characters. If reading or accessing the file fails, it prints out 'Error : ' followed by the error details",
        "parameters" : GetFileContent.model_json_schema(),
    }
}
