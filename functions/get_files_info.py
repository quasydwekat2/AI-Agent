from utils.paths import safe_path
import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        target_dir = safe_path(working_directory, directory)

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        result_lines = []

        def scan(dir_path):
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)

                is_dir = os.path.isdir(item_path)
                size = os.path.getsize(item_path)

                result_lines.append(
                    f"- {item}: file_size={size} bytes, is_dir={is_dir}"
                )

                if is_dir:
                    scan(item_path)

        scan(target_dir)

        return "\n".join(result_lines)

    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except Exception as e:
        return f"Error: {str(e)}"