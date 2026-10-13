import os


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        absolute_path_of_curr_dir = os.path.realpath(working_directory)
        target_file = os.path.realpath(
            os.path.join(absolute_path_of_curr_dir, file_path)
        )

        valid_target_file = (
            os.path.commonpath([absolute_path_of_curr_dir, target_file])
            == absolute_path_of_curr_dir
        )

        if not valid_target_file:
            return (
                f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" is not a file'

        with open(target_file, encoding="utf-8") as file:
            return file.read()
    except Exception as err:
        return f"Error: {err}"