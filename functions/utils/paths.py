import os


def safe_path(working_directory: str, user_path: str) -> str:
    """
    Resolves a user-provided path safely inside working_directory.
    Raises ValueError if path escapes working directory.
    """
    working_dir_abs = os.path.abspath(working_directory)

    target_path = os.path.normpath(
        os.path.join(working_dir_abs, user_path)
    )

    if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
        raise ValueError("Path escapes working directory")

    return target_path