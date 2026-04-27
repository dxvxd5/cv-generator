import os


def change_extension(path: str, new_extension: str) -> str:
    """
    Change the extension of the given path to the given new extension
    """
    return os.path.splitext(path)[0] + new_extension
