from functions.utils.paths import safe_path
import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_file_path = safe_path(working_directory, file_path)

        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except Exception as e:
        return f'Error: {str(e)}'