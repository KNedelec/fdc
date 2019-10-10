from sys import stderr
from os.path import *
from os import makedirs

from utils import *

def ensure_dir(dir):
    '''
    create dir if not exists
    @return 0 if dir exists or has been created, otherwise 1
    '''
    if not isdir(dir):
        try:
            makedirs(dir)
        except OSError as err:
            print(f"could not create the directory {dir}. error: {err}",
                    file=stderr)
            return get_fserror_code(dir=dir, err=err)

    return get_ok_code()


def write_file(file_path, content):
    ''' Write the file on disk '''
    try:
        with open(file_path, mode="w") as wfile:
            print(content, file=wfile)
            return get_ok_code()

    except OSError as err:
        print(f"could not create the file {file_path}. error: {err}",
            file=stderr)
        return get_fserror_code(file = file_path)

def read_file(file_path):
    ''' Get the file content '''
    try:
        with open(file_path, mode="r") as rfile:
            return rfile.read()

    except OSError as err:
        print(f"could not read the file {file_path}. error: {err}",
            file=stderr)
        return get_fserror_code(file = file_path)


def get_basepath_fn(app_rgs):
    '''
    return a getter for the base path
    app_args -- a dict containing the app config containing the "dir" value
    '''
    return lambda: app_rgs["dir"]


def get_tplpath_fn(app_args):
    '''
    return a function that returns the base path of the templates
    app_args -- a dict containing the app config containing the "dir" value
    '''
    return lambda: join(get_basepath_fn(app_args)(), "template")


def get_datapath_fn(app_args):
    '''
    return a function that returns the base path of the data files
    app_args -- a dict containing the app config containing the "dir" value
    '''
    return lambda: join(get_basepath_fn(app_args)(), "data")


def get_fserror_code(**args):
    ''' return the error tuple '''
    return get_baseerror_code("fs_error", args)
