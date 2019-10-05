
import os
from os.path import isfile, isdir
import argparse

def run():
    # take a directory as argument to get the working directory
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="The root directory")
    args = parser.parse_args()

    dirArg = args.dir;
    if not dirArg:
        dirArg = "./"

    dir = os.path.abspath(os.path.join(os.getcwd(), dirArg))

    if dirArg:
        print(f"working directory: {dir}")
    else:
        print(f"no working directory provided, use default: {dir}")

    if not isdir(dir):
        try:
            os.makedirs(dir)
        except OSError as err:
            print(f"could not create the directory {dir}. error: {err}")
            pass
        return

    dirs = os.listdir()
    print(dirs)

run()
