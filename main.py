
import os
from os.path import isfile, isdir, join
import argparse
from template import prompt_create_template, write_template

def run():
  # take a directory as argument to get the working directory
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="The root directory")
    args = parser.parse_args()

    dir_arg = args.dir;
    if not dir_arg:
      dir_arg = "./"

    dir = os.path.abspath(join(os.getcwd(), dir_arg))

    if dir_arg:
      print(f"working directory: {dir}")
    else:
      print(f"no working directory provided, use default: {dir}")

    if not isdir(dir):
      try:
        os.makedirs(dir)
      except OSError as err:
        print(f"could not create the directory {dir}. error: {err}")
        return

    tpls_dir = join(dir, "tpls")

    if not isdir(tpls_dir):
        try:
          os.makedirs(tpls_dir)
        except OSError as err:
          print(f"could not create the directory {tpls_dir}. error: {err}")
          return

    def get_tplsdir():
      return tpls_dir

    def create_template():
        template = prompt_create_template()
        write_template(get_tplsdir(), template)
        print("create template...", template)

    def list_template():
        print("list template...")

    main_menu_list = {
        "ct": ( "Create template", create_template),
        "lt": ( "List templates", list_template)
    }

    def get_menu(chosen_menu):
        return main_menu_list.get(chosen_menu, ("None", lambda: None))

    def get_menuhandler(chosen_menu):
        return get_menu(chosen_menu)[1]

    # main menu
    for key in main_menu_list:
        item_name = main_menu_list[key][0]
        print(f"{key}: {item_name}")
    chosen_menu = input()

    get_menuhandler(chosen_menu)()

run()
