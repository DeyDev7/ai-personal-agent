import os


def get_files_info(working_directory: str, directory: str) -> str:
    try:
        absolute_path_of_curr_dir = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path_of_curr_dir, directory))

        valid_target_directory = ( # returns a boolean value 
            os.path.commonpath([absolute_path_of_curr_dir, target_directory])
            == absolute_path_of_curr_dir
        )

        if not valid_target_directory:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"