import os


def change_extension(path, new_extension):
    """
    Change the extension of the given path to the given new extension
    """
    return os.path.splitext(path)[0] + new_extension
