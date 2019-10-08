from sys import stderr
from os.path import join
from os import walk
import json
from formatter import *
from textwrap import dedent
from re import match

from fs import *

def prompt_create_template():
    '''
    prompt every information for a new template
    '''
    field_number = 1
    print(dedent('''
      Create a new template.
      (n) save and new, (o) save and back, (c) cancel, (q) quit
    '''))
    lastchars = input("name: ")
    template = []
    while lastchars:
        template.append(lastchars)
        if lastchars in ["n", "o", "c", "q"]:
            return lastchars
        field_number += 1
        lastchars = input(f"field {field_number - 1}: ")

    return template

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
            name, *fields = content
            print(f"{name.ljust(60)}: {'|'.join(fields)}", end="\n")
        print()


    return lambda options: _list_template(options)


def get_createtemplate_fn(get_tpldir):
    '''
    get the create template function
    '''
    def _create_template(fields):
      '''
      create a template with fields or prompt the informations
      '''
      if fields:
        _create_template_file(get_tpldir(), fields)
        return

      while True:
        template = prompt_create_template()
        if template == "q":
          return

        if template == "n" or template == "o":
          _create_template_file(get_tpldir(), template)

        if template in ["o", "c"]:
          print()
          return;

    return lambda fields: _create_template(fields)


def _create_template_file(dir, template):
    template_filename = f"{join(dir, template[0])}.stp"
    content = format_list(template)

    return write_file(template_filename, content)

