# from functions.get_files_info import get_files_info
# from functions.get_file_content import get_file_content
# from functions.write_file import write_file
from functions.run_python_file import run_python_file


def main():
    working_dir = "calculator"
    # print(get_files_info(working_dir))
    # print(get_files_info(working_dir, "pkg"))
    # print(get_files_info(working_dir, "/bin"))
    # print(get_files_info(working_dir, "../"))
    # print(get_file_content(working_dir, 'lorem.txt'))
    # print(write_file(working_dir, "lorem.txt", "************ WAIT, ADDITIONAL CONTENT"))
    # print(write_file(working_dir, "newlorem.txt", "************ WAIT, ADDITIONAL CONTENT"))
    # print(write_file(working_dir, "/pkg2/newlorem.txt", "************ WAIT, ADDITIONAL CONTENT"))
    print(run_python_file(working_dir, "main.py", "1+2"))
    print(run_python_file(working_dir, "tests.py"))

main()
