import os
import stat


def get_files_info(working_directory: str, directory: str) -> str:
    try:
        absolute_path_of_curr_dir = os.path.realpath(working_directory)
        target_directory = os.path.realpath(
            os.path.join(absolute_path_of_curr_dir, directory)
        )

        valid_target_directory = (
            os.path.commonpath([absolute_path_of_curr_dir, target_directory])
            == absolute_path_of_curr_dir
        )

        if not valid_target_directory:
            return (
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            )

        if not os.path.isdir(target_directory):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for name in sorted(os.listdir(target_directory)):
            full_path = os.path.join(target_directory, name)
            metadata = os.lstat(full_path)
            is_dir = stat.S_ISDIR(metadata.st_mode)
            entries.append(
                f"  - {name}: file_size={metadata.st_size} bytes, is_dir={is_dir}"
            )

        return "Result for current directory:\n" + "\n".join(entries)

    except Exception as err:
        return f"Error: {err}"
