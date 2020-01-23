from os.path import abspath, join
from os import getcwd
import argparse

def get_appargs():
    '''
    Parse cli arguments
    Return a dictionary with app defaults or cli overrides
    '''
    # take a directory as argument to get the working directory
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="The root directory")
    args = parser.parse_args()

    # set working directory
    dir_arg = args.dir;
    if not dir_arg:
      dir_arg = "./"

    dir = abspath(join(getcwd(), dir_arg, 'fdc'))

    return { "dir": dir }

