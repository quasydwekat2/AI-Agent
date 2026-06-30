from config import MAX_CHARS
from google.genai import types
from functions.utils.paths import safe_path
import os

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

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