import os


def get_files_info(working_directory, directory = None):
    abs_working_dir_path = os.path.abspath(working_directory)
    if not directory:
        directory = working_directory
    else: 
        directory = os.path.join(working_directory,directory)
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