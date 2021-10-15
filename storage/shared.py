# Make Python aware of upper-level modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import os
import pathlib
import platform
import subprocess
from os import listdir
from os.path import isfile, join
from enum import Enum


class PathPos(Enum):
    FILE = 1,
    FLAG = 2,
    BENCHMARK = 3,
    COMMIT = 4,
    MACHINE = 5


def get_result_files(path="."):
    return [os.path.join(path, f) for f in listdir(path) if isfile(join(path, f))]

def get_all_files():
    res = list()
    for root, dirs, files in os.walk(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "processed_results"))):
        for file in files:
            if file.endswith(".txt"):
                res.append(os.path.join(root, file))
    return res


def get_path(sep_path, pos):
    if pos == PathPos.FILE:
        return os.path.join(*sep_path)
    elif pos == PathPos.FLAG:
        return os.path.basename(os.path.join(*sep_path[:-1]))
    elif pos == PathPos.BENCHMARK:
        return os.path.basename(os.path.join(*sep_path[:-2]))
    elif pos == PathPos.COMMIT:
        return os.path.basename(os.path.join(*sep_path[:-3]))
    elif pos == PathPos.MACHINE:
        return os.path.basename(os.path.join(*sep_path[:-4]))
