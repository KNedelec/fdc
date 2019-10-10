
def length_validator(length):
    return lambda options: len(options) == length

def ok_validator():
    return lambda: True

class Menu:
    def __init__(self, before, after):
        self.menu_items = []
        self.before = before
        self.after = after
        self.current = None

    def add_item(self, item):
        self.menu_items.append(item)

    def select_item(self, item):
        self.current = item

    def get_current(self):
        return self.current

    def prompt(self):
        self.before()
        while True:
            name = get_item_name(self.current)
            chosen_menu = input(f"{name}:")
            if chosen_menu is "q":
                break
        self.after()
        pass


def get_item_name(item):
    if not item:
        return ""
    return item(0)
