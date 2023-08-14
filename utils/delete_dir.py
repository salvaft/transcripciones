"""
Module: delete_dir

This module provides functions to delete the contents of a directory. The main 
function is 'delete_directory', which deletes the contents of the specified 
directory, and the supporting function '_delete_contents' is used for the actual deletion process.

Functions:
- delete_directory(directory):
    Deletes the contents of the specified directory. If the directory does not 
    exist or is not a directory, a message is printed.

Internal Functions:
- _delete_contents(directory):
    Recursively deletes the contents of a directory, including subdirectories.

Usage:
1. Import the 'delete_directory' function from this module.
2. Call 'delete_directory' with the target directory you want to empty.

Note: This module assumes the 'directory' parameter is a pathlib.Path object
 representing the target directory.

Example:
```python
from pathlib import Path
from delete_dir import delete_directory

directory_to_clear = Path("path/to/empty")
delete_directory(directory_to_clear)
"""


# Function to delete the contents of a directory
def _delete_contents(directory):
    """
    Recursively delete the contents of a directory.

    Args:
    directory (pathlib.Path): The directory whose contents need to be deleted.

    Note:
    This function is intended for internal use by the 'delete_directory'
    function and should not be called directly.
    """
    for item in directory.iterdir():
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            _delete_contents(item)  # Recursively delete contents of subdirectories
            item.rmdir()  # Remove the empty subdirectory


def delete_directory(directory):
    """
    Delete the contents of the specified directory.

    This function deletes all the files and subdirectories within the specified
      directory. If the directory does not exist
    or is not a directory, a message indicating the status is printed.

    Args:
    directory (pathlib.Path): The directory whose contents need to be deleted.

    Note:
    If the provided directory does not exist or is not a directory, a message
    indicating the issue will be printed.

    Usage:
    1. Import the 'delete_directory' function from the 'delete_dir' module.
    2. Call 'delete_directory' with the target directory you want to empty.

    Example:
    ```python
    from pathlib import Path
    from delete_dir import delete_directory

    directory_to_clear = Path("path/to/empty")
    delete_directory(directory_to_clear)
    ```
    """
    # Check if the directory exists before deleting its contents
    if directory.exists() and directory.is_dir():
        # Delete the contents of the directory
        _delete_contents(directory)
        print(f"Contents of {directory} deleted.")
    else:
        print(f"{directory} does not exist or is not a directory.")
