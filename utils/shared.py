import os

def key_exists(d, *args):
    for arg in args:
        try:
            d[arg]
        except KeyError:
            return False
    return True


def strip_digits(s):
    result = ""
    for c in s:
        if c.isdigit():
            result += c
    return result


# returns: (path without filename, filename)
def strip_filename(full_path):
    pos = len(full_path) - 1
    while pos >= 0:
        if full_path[pos] == os.sep:
            return full_path[:pos], full_path[pos+1:]
        pos = pos - 1


# returns: (path without flag name, flag name, filename)
def strip_flag(full_path):
    stripped = strip_filename(full_path)
    res = stripped[0]
    pos = len(res) - 1

    while pos >= 0:
        if res[pos] == os.sep:
            return res[:pos], res[pos+1:], stripped[1]
        pos = pos - 1