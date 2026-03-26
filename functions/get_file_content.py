import os

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
        return f"Error: Failed to read contents of file {file_path}, exception : {e}"
