from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_to_files import schema_write_to_file

available_schemas = [
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_to_file,
]