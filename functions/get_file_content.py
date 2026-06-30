from config import MAX_CHARS
from functions.utils.paths import safe_path
import os


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_path = safe_path(working_directory, file_path)

        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)

            extra = f.read(1)
            if extra:
                content += f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except ValueError as e:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    except Exception as e:
        return f"Error: {str(e)}"