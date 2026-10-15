import os
import subprocess
import sys


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        absolute_path_of_curr_dir = os.path.realpath(working_directory)
        target_directory = os.path.realpath(
            os.path.join(absolute_path_of_curr_dir, file_path)
        )

        valid_target_directory = (
            os.path.commonpath([absolute_path_of_curr_dir, target_directory])
            == absolute_path_of_curr_dir
        )

        command: list[str] = [sys.executable, target_directory]

        if not valid_target_directory:
            return (
                f'Error: Cannot execute "{file_path}" '
                "as it is outside the permitted working directory"
            )

        if not os.path.isfile(target_directory):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_directory.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        if args is not None:
            command.extend(args)

        children_process = subprocess.run(
            command,
            cwd=absolute_path_of_curr_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []

        if children_process.returncode != 0:
            output.append(
                f"Process exited with code {children_process.returncode}"
            )

        stdout = children_process.stdout or ""
        stderr = children_process.stderr or ""

        if not stderr and not stdout:
            output.append("No output produced")
        else:
            if stdout:
                output.append(f"STDOUT: {stdout}")
            if stderr:
                output.append(f"STDERR: {stderr}")

        return "\n".join(output)

    except Exception as err:
        return f"Error: executing Python file: {err}"
