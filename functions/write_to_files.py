import os
import stat

from config import MAX_CHARS

def write_to_file(working_directory: str, file_path: str, content: str) -> str:
    directory_fd = None
    file_fd = None
    try:
        relative_path = os.path.normpath(file_path)
        if (
            os.path.isabs(relative_path)
            or relative_path == os.pardir
            or relative_path.startswith(os.pardir + os.sep)
        ):
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )

        path_parts = relative_path.split(os.sep)
        if relative_path in ("", "."):
            return(
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )

        directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        directory_fd = os.open(os.path.realpath(working_directory), directory_flags)
        for part in path_parts[:-1]:
            try:
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)
            except FileNotFoundError:
                try:
                    os.mkdir(part, dir_fd=directory_fd)
                except FileExistsError:
                    pass
                next_fd = os.open(part, directory_flags, dir_fd=directory_fd)

            os.close(directory_fd)
            directory_fd = next_fd

        try:
            file_fd = os.open(
                path_parts[-1],
                os.O_WRONLY | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                0o666,
                dir_fd=directory_fd,
            )
        except IsADirectoryError:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        if not stat.S_ISREG(os.fstat(file_fd).st_mode):
            return f'Error: Cannot write to "{file_path}" as it is not a regular file'

        os.ftruncate(file_fd, 0)
        with os.fdopen(file_fd, 'w', encoding="utf-8") as file:
            file_fd = None
            file.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as err:
        return f"Error: {err}"
    finally:
        if file_fd is not None:
            os.close(file_fd)
        if directory_fd is not None:
            os.close(directory_fd)