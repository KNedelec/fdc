from os import walk, getcwd, makedirs
from os.path import isfile, isdir, join

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

    create_template = get_createtemplate_fn(get_tpldir)
    list_template = get_listtemplate_fn(get_tpldir)

    mainmenu_list = {
        "ct": ( "[name, [field1, [field2, [...]]] Create template",
          create_template),
        "lt": ( "List templates", list_template),
        "dt": ( "delete templates", list_template),
    }

    def get_menu(chosen_menu):
        return mainmenu_list.get(chosen_menu, ("None",
          lambda: print("unknown argument")))

    def get_menuhandler(chosen_menu):
        return get_menu(chosen_menu)[1]

    def parse_mainmenu_choice(choice):
      return choice.split(" ")


    while True:
      # main menu
      for key in mainmenu_list:
          item_name = mainmenu_list[key][0]
          print(f"{key}: {item_name}")
      chosen_menu = input("Please chose an action: ")
      if chosen_menu is "q":
        return

      chosen_menu, *options = parse_mainmenu_choice(chosen_menu)
      print(f"chosen: {chosen_menu}, options: {options}")

      returnkey = get_menuhandler(chosen_menu)(options)
      if returnkey == "q":
        return


run()
