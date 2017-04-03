# coding: utf-8

import os


def get_script_absdir(_file_):
    return os.path.dirname(os.path.abspath(_file_))


def path_join(*args):
    return os.path.normpath(os.path.join(*args))
