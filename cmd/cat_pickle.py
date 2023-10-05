"""
This module reads and prints data from a pickled file located in the parent 
directory of the current working directory. It performs the following steps:

1. Specifies the current working directory (CWD) and the parent directory 
(PROJECT) based on the CWD.
2. Reads data from a pickled file named "pickle.pkl" located in the parent directory.
3. Prints the loaded data to the console.

Module Components:
- CWD: The current working directory, where the script is executed.
- PROJECT: The parent directory of the current working directory.
- "pickle.pkl": The pickled file from which data is read.

Usage:
1. Ensure that the "pickle.pkl" file is present in the parent directory.
2. Run the script to read and print the data from the pickled file.

Note: This module assumes that the specified pickled file contains data that 
can be deserialized using the pickle module.

Please make sure the "pickle.pkl" file exists in the correct location before running this script.
"""

from pathlib import Path
import pickle
import pprint

CWD = Path(".")

PROJECT = CWD.parent

with open(PROJECT / "pickle.pkl", "rb+") as pkl:
    data = pickle.load(pkl)
    pkl.seek(0)
    data["temas"] = [item for item in data["temas"] if item["files"]]
    # pickle.dump(data, pkl)
    pprint.pprint(data)
