'''
utility routines for PvMail 

Copyright (c) 2014-2017, UChicago Argonne, LLC.  See LICENSE file.
'''


import os

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def get_pkg_file_path(fname):
    '''return the absolute path to the named file in the package directory'''
    vpath = os.path.abspath(os.path.dirname(__file__))
    vfile = os.path.join(vpath, fname)
    if not os.path.exists(vfile):
        raise FileNotFoundError('file does not exist: ' + vfile)
    return vfile


def read_resource_file(fname):
    '''return contents of the named file in the package directory'''
    return open(get_pkg_file_path(fname)).read()

