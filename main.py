from os import walk, getcwd, makedirs
from os.path import isfile, isdir, join
from re import match

from template import *
from fs import *
from app_args import *

def run():
    '''
    Main entry
    '''
    # get app config overriden by arguments
    app_args = get_appargs()

    # function to get the base directory path
    get_basedir = get_basepath_fn(app_args)
    if ensure_dir(get_basedir())[0] == 1: return

    # function to get the template directory path
    get_tpldir = get_tplpath_fn(app_args)
    if ensure_dir(get_tpldir())[0] == 1: return

    # function to get the data directory path
    get_datadir = get_datapath_fn(app_args)
    if ensure_dir(get_datadir())[0] == 1: return

    create_template = get_createtemplate_fn(get_tpldir, get_datadir)
    print_list_template = get_print_listtemplates_fn(get_tpldir)
    add_data = get_adddata_fn(get_tpldir, get_datadir)

    mainmenu_list = {
        "help": ( "[command] show help",
          lambda option: show_help(mainmenu_list, option)),
        "ct": ( "[name, [field1, [field2, [...]]] Create template",
          create_template ),
        "lt": ( "List templates", print_list_template ),
        "ad": ( "[template_name] Add items from a template", add_data ),
    }

    def get_menu(chosen_menu):
        return mainmenu_list.get(chosen_menu, ("None",
          lambda: print("unknown argument")))

    def get_menuhandler(chosen_menu):
        return get_menu(chosen_menu)[1]

    def parse_mainmenu_choice(choice):
      return choice.split(" ")


    while True:
      chosen_menu = input(":")
      if chosen_menu is "q":
        return

      chosen_menu, *options = parse_mainmenu_choice(chosen_menu)

      returnkey = get_menuhandler(chosen_menu)(options)
      if returnkey == "q":
        return

def show_help(mainmenu_list, options):
    '''
    Show the list of commands
    '''
    if not len(options) == 1:
      option = ""
    else:
        option = options[0]
    for key in mainmenu_list:
        item_name = mainmenu_list[key][0]
        if match(option, item_name) or match(option, key):
          print(f"{key}: {item_name}")

    print("\n")

run()
