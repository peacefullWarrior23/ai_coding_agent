import os
import subprocess


def run_python_file(working_dir, python_file: str, args=[]):
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, python_file))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error : File {python_file} is not under working directory {working_dir}"
    if not os.path.isfile(abs_file_path):
        return f"Error : File {python_file} is not actually a file"
    if not python_file.endswith(".py"):
        return f"Error : File {python_file} is not actually a Python file"
    
    try:
        final_args = ["python3",abs_file_path,]
        final_args.extend(args)
        output = subprocess.run(
            final_args,
            cwd=abs_working_dir,
            timeout= 30,
            capture_output=True
            )
        resonse_str = f"""
    [STDOUT]: {output.stdout}
    [STDERR]: {output.stderr}
"""
        if output.stderr == "" and output.stdout=="":
            return "WARNING: Python file outputted nothing"
        if output.returncode != 0:
            resonse_str += f"WARNING: python file run returned code {output.returncode}"
        return resonse_str
    except Exception as e:
        return f"Error: Failed to run python file {abs_file_path}, {e}"