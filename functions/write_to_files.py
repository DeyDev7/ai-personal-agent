import os


from config import MAX_CHARS

def write_to_file(working_directory: str, file_path: str, content: str) -> str:
    try: 
        absolute_path_of_curr_dir = os.path.realpath(working_directory)
        target_file = os.path.realpath(
            os.path.join(
                absolute_path_of_curr_dir,
                file_path
            )
        )
    
        validate_target_file = (
            os.path.commonpath([absolute_path_of_curr_dir, target_file]) 
            == absolute_path_of_curr_dir
        )
    
        if not validate_target_file:
            return (
                f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            )
    
        if os.path.isdir(target_file):
            return(
                f'Error: Cannot write to "{file_path}" as it is a directory'
            )
    
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
        with open(target_file, 'w', encoding="utf-8") as file:
            file.write(content)
    
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as err:
        return f"Error: {err}"