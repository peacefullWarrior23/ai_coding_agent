import os

from google.genai import types
from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel, Field


def write_file(working_dir, file_path, content):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error : File {file_path} is not under working directory {working_dir}"
    if not os.path.isdir(os.path.dirname(abs_file_path)):
        parent_dir = os.path.dirname(abs_file_path)
        try:
            os.makedirs(parent_dir)
        except Exception as e:
            return (
                f"Error : Failed to create the parent dir for file {abs_file_path}, {e}"  # noqa: E501
            )
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f"Success: content was written to file {abs_file_path}"
    except Exception as e:
        return f"Error : Failed to write contents to file {file_path}, exception : {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="""Writes the provided string content to the given file. 
    Any existing text in the file will be replaced with the provided content.
    If the file does not exist it will be created along with parent directory, before it is written to.
    If accessing or running the file fails, it prints out 'Error : ' followed by the error details""",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file which is to be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string content which will be written to the file.",
            ),
        },
    ),
)


class WriteFile(BaseModel):
    file_path: str = Field(
        description="Path to the file which is to be written to, relative to the working directory."
    )
    content: str = Field(
        description="The string content which will be written to the file."
    )


tool_write_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes the provided string content to the given file. Any existing text in the file will be replaced with the provided content.If the file does not exist it will be created along with parent directory, before it is written to. If accessing or running the file fails, it prints out 'Error : ' followed by the error details",
        "parameters": WriteFile.model_json_schema(),
    },
}
