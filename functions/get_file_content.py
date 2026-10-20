import os


from config import MAX_CHARS


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
            content = file.read(MAX_CHARS + 1)

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as err:
        return f"Error: {err}"


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns file content, truncating it when it exceeds the maximum character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}