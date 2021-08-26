# Make Python aware of upper-level modules
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import os
from storage.shared import get_all_files, PathPos, get_path


class UniqueRuns:
    def __init__(self, files=None):
        self.db = dict()

        if files is None:
            files = get_all_files()

        for file in files:
            self.add(file)

    def add(self, path):
        sep_path = path.split(os.sep)
        self.__add_or_init_dict__(
            get_path(sep_path, PathPos.MACHINE),
            get_path(sep_path, PathPos.COMMIT),
            get_path(sep_path, PathPos.BENCHMARK),
            get_path(sep_path, PathPos.FLAG),
            path,
                )

    def __add_or_init_dict__(self,
                             machine_key, commit_key, benchmark_key, flag_key, file   ):

        try:
            self.db[machine_key]
        except KeyError:
            self.db[machine_key] = dict()

        try:
            self.db[machine_key][commit_key]
        except KeyError:
            self.db[machine_key][commit_key] = dict()

        try:
            self.db[machine_key][commit_key][benchmark_key]
        except KeyError:
            self.db[machine_key][commit_key][benchmark_key] = dict()

        try:
            self.db[machine_key][commit_key][benchmark_key][flag_key]
        except KeyError:
            self.db[machine_key][commit_key][benchmark_key][flag_key] = list()

        self.db[machine_key][commit_key][benchmark_key][flag_key].append(file)

    def values(self):
        return self.db.values()

    def items(self):
        return self.db.items()

    def __getitem__(self, item):
        return self.db[item]

    def __iter__(self):
        return self.db.__iter__()

    def __str__(self):
        return self.db.__str__()
