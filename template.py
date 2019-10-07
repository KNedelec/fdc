from formatter import *
from os.path import join

def prompt_create_template():
    field_number = 1
    lastchars = input("name: ")
    template = []
    while lastchars:
        template.append(lastchars)
        if lastchars == "_q":
            return []
        field_number += 1
        lastchars = input(f"field {field_number - 1}: ")

    return template

def write_template(dir, template):
    wfile_name = f"{join(dir, template[0])}.sik"
    try:
        with open(wfile_name, mode="w") as wfile:
            print(format_list(template), file=wfile)
    except OSError as err:
        print(f"could not create the file {template[0]}. error: {err}")

