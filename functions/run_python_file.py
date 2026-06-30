from functions.utils.paths import safe_path
import subprocess
import os


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None
) -> str:
    try:
        absolute_file_path = safe_path(working_directory, file_path)

        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")

            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_parts)

    except ValueError as e:
        return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
    except subprocess.TimeoutExpired:
        return "Error: Execution timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"