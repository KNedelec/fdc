from sys import stderr
from os.path import join
from os import walk
import subprocess
import json
from formatter import format, format_list, parse_list
from textwrap import dedent
from re import match

from fs import *

def get_listtemplate_fn(get_tpldir):
    '''
    get the list template function
    get_tpldir -- get the template path function
    '''
    def _list_template(options = []):
      if len(options) > 0:
          pattern = options[0]
      else:
          pattern = ""

      for root, dirs, files in walk(get_tpldir()):
        for name in files:
          if not match(pattern, name):
            continue;

          with open(join(get_tpldir(), name), mode="r") as rfile:
            content = json.loads(rfile.read())
            yield content

    return lambda options = []: _list_template(options)


def get_print_listtemplates_fn(get_tpldir):
    def _print_listtemplates(options = []):
        templates = get_listtemplate_fn(get_tpldir)(options)
        for template in templates:
            name, *fields = template
            print(f"{name.ljust(60)}: {'|'.join(fields)}", end="\n")
        print()

    return lambda options = []: _print_listtemplates(options)


def get_createtemplate_fn(get_tpldir, get_datadir):
    '''
    get the create template function
    '''
    def _create_template(fields):
      '''
      create a template with fields or prompt the informations
      '''
      if fields:
        _create_template_file(get_tpldir(), fields)
        _create_data_file(get_datadir(), fields)
        return

      while True:
        template = prompt_create_template()
        if template == "q":
          return

        if template == "n" or template == "o":
          _create_template_file(get_tpldir(), template)
          _create_data_file(get_datadir(), template)

        if template in ["o", "c"]:
          print()
          return;

    return lambda fields: _create_template(fields)


def get_adddata_fn(get_tpldir, get_datadir):
    ''' get the add data function '''
    def _add_data(fields):
        ''' add data from a template '''
        template_list = get_listtemplate_fn(get_tpldir)()
        template_names = list(map(lambda t: t[0], template_list))
        try:
            if not len(fields) == 1:
                print("Choose a template in ", end="")
                print(", ".join(template_names))
                while True:
                    template_name = input(":")
                    if template_name not in template_names:
                        print("unknown template")
                    else:
                        break
            else:
                template_name = fields[0]
            template = get_template(get_tpldir, template_name)
            while True:
                new_data = prompt_create_data(template)
                update_data_file(get_datadir, template_name, new_data)
                subprocess.run(["git", "add", get_data_path(get_datadir, template_name)], cwd=get_datadir())
                subprocess.run(["git",  "commit", f"-m data ${new_data} added to ${template_name}"], cwd=get_datadir())
        except KeyboardInterrupt as err:
            return

    return lambda fields: _add_data(fields)


def prompt_create_data(template):
    ''' prompt every informations for a new data '''
    name, *fields = template
    values = [input(f"[{name}]/{field}: ") for field in fields]

    return dict(zip(fields, values))

def prompt_create_template():
    ''' prompt every information for a new template '''
    field_number = 1
    print(dedent('''
      Create a new template.
      (n) save and new, (o) save and back, (c) cancel, (q) quit
    '''))
    lastchars = input("name: ")
    template = []
    while True:
        if lastchars in ["n", "o", "c", "q"]:
            return lastchars
        template.append(lastchars)
        field_number += 1
        lastchars = input(f"field {field_number - 1}: ")

    return template


def get_data(get_datadir, template_name):
    data_path = get_data_path(get_datadir, template_name)
    return parse_list(read_file(data_path))


def update_data_file(get_datadir, template_name, data_item):
    data = get_data(get_datadir, template_name)
    data.append(data_item)
    data_json = format(data)
    return_code = write_file(get_data_path(get_datadir, template_name), data_json)
    if return_code[0] == 0:
        print("...ok")

    return return_code


def get_data_path(get_datadir, template_name):
    return join(get_datadir(), f"{template_name}.sdt")


def get_template_path(get_tpldir, template_name):
    return join(get_tpldir(), f"{template_name}.stp")


def get_template(get_tpldir, template_name):
    template_path = get_template_path(get_tpldir, template_name)
    return parse_list(read_file(template_path))


def _create_data_file(dir, template):
    data_filename = f"{join(dir, template[0])}.sdt"
    content = "[]"
    return_code = write_file(data_filename, content)
    if return_code[0] == 0:
        print("...ok")

    return return_code


def _create_template_file(dir, template):
    template_filename = f"{join(dir, template[0])}.stp"
    content = format_list(template)
    return write_file(template_filename, content)

