import os


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
            return f"Error:Failed to create the parent dir for file {abs_file_path}, {e}"  # noqa: E501
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f"Success: content was written to file {abs_file_path}"
    except Exception as e:
        return f"Error: Failed to write contents to file {file_path}, exception : {e}"
