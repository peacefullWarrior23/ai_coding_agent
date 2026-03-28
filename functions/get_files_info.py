import os

from google.genai import types


def get_files_info(working_dir, directory = None):
    abs_working_dir_path = os.path.abspath(working_dir)
    if not directory:
        directory = working_dir
    else: 
        directory = os.path.join(working_dir,directory)
    abs_dir_path = os.path.abspath(directory)
    if not abs_dir_path.startswith(abs_working_dir_path):
        return f"Error {directory} is outside of the working directory"
    
    # try:
    contents = os.listdir(abs_dir_path)
    final_response = ""
    for content in contents:
        content_path = os.path.join(abs_dir_path, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f"- {content} : file_size ={size} bytes, is_dir={is_dir} \n"
    return final_response

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)