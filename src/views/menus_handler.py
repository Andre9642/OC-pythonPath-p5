"""Menus module"""
import sys

from typing import Callable, List


class MenuItem:
    """A Class to represent a menu item"""

    name: str = ''
    shortcut: str = ''
    func: str = None
    args: List = []

    def __init__(self,
                 name: str,
                 shortcut: str,
                 func: Callable,
                 args: List=[]):
        """
        Initialize instance of class and check if arguments provided are valid

        Args:
            self (undefined):
            name (str): the label for the menu item
            shortcut (str): a shortcut that lets to user to choose this item
            when the menu and the prompt appear
            func (str): the function to call when we select this item
            args (List): arguments to provide when we call `func()`
        """
        self.name = name
        self.shortcut = shortcut
        self.func = func
        self.args = args
        if not self.check():
            raise ValueError("Invalid argument provided")

    def __repr__(self):
        return f"{self.shortcut} - {self.name}"

    def check(self):
        """
        Ensures that minimal attributes are valid
        """
        if not self.name or not isinstance(self.name, str):
            return False
        if not self.shortcut or not isinstance(self.shortcut, str):
            return False
        if not hasattr(self, "func"):
            return False
        return True

    def exit():
        print("Good bye!")
        sys.exit(1)
class Menu:

    """A class that represents a menu"""

    title: str = None
    description: str = None
    parent = None

    def __init__(self, parent=None):
        self.title = self.title or "No title"
        self.parent = parent
        self._sub_menus = {}
        self._items = []
        self._contextual_items = []
        self._pager = None
        self.post_init()

    def post_init(self):
        raise NotImplementedError

    @property
    def previous_menu_item(self):
        """Returns the previous menu item"""
        previous_menu_title = self.parent.title
        return MenuItem(f"Go back ({previous_menu_title})", "b", "go_back")

    @previous_menu_item.setter
    def previous_menu_item(self, previous_menu):
        self.parent = previous_menu

    @property
    def contextual_items(self):
        """returns contextual/dynamic items such as next/previous page"""
        items = []
        _pager = self._pager
        if _pager:
            items += self._pager.contextual_items
        if self.parent:
            items.append(self.previous_menu_item)
        items.append(MenuItem("Quitter", 'q', "quit"))
        return items

    @property
    def items(self):
        """
        returns items of the menu excluding contextual items
        """
        return self._items

    @property
    def all_items(self):
        """returns menu items and contextual items"""
        return self.items + self.contextual_items

    def max_size_shortcut(self):
        max_size = 0
        for item in self.all_items:
            if not hasattr(item, "shortcut"):
                continue
            cur_size = len(item.shortcut)
            if cur_size > max_size:
                max_size = cur_size
        return max_size

    def show(self):
        """Displays the menu and retrieves the user choice"""
        self.display()
        self.read_input()

    def display(self):
        """Displays the menu
           A menu consists of:
            - A title
            - An optional text, i.e. an extra-info about the menu, an error messages, etc.
            - Items of the form: '<shortcut> - <name>'
        """
        print(f"=== {self.title} ===")
        if self.description:
            print(self.description)
        items = self.all_items
        if not items:
            print("No entry")
        else:
            max_size_shortcut = self.max_size_shortcut()
            for item in items:
                print(f"%-{max_size_shortcut}s -- {item.name}" % item.shortcut)

    def read_input(self):
        """Retrieves the user choice
           User should type the shortcut corresponding to the desired menu item
           While the user input is invalid, we ask another input
        """
        choice = ""
        item = None
        while not choice or not item:
            if choice:
                print("! Invalid input")
            choice = input("> ")
            if choice == "q":
                sys.exit(0)
            item = self.get_item_from_shortcut(choice)
        self.execute_action(item.func, item.args)

    def execute_action(self, action, args=None):
        """Runs the script related to the menu item chosen"""
        if not self.valid_choice(action):
            print("! Feature not implemented yet")
            self.display()
            self.read_input()
        else:
            if args:
                getattr(self, action)(*args)
            else:
                getattr(self, action)()

    def valid_choice(self, choice):
        """Checks if the attached script to an item is valid"""
        return bool(choice) and hasattr(self, choice)

    def go_back(self):
        """Displays the previous menu if available"""
        if self.parent:
            self.parent.show()

    def get_item_from_shortcut(self, shortcut: str) -> MenuItem:
        """
        returns an item from its shortcut

        Args:
            self (undefined):
            shortcut (str): the shortcut to check
        Returns:
            MenuItem
        """
        for item in self.all_items:
            if item.shortcut == shortcut:
                return item
        return None

    def move_to(self, direction: int):
        """
        Description of move_to

        Args:
            self (undefined):
            direction (int):
        """
        res = self._pager.move_to(direction)
        if res:
            self.display()
        self.read_input()

    def change_number_results_per_page(self):
        """Asks to the user a number then sets this number as items Number per page"""
        results_per_page = 0
        while results_per_page < 2:
            results_per_page = input("Result number per page: ")
            if not results_per_page.isnumeric():
                results_per_page = 0
            else:
                results_per_page = int(results_per_page)
                self._pager.set_results_per_page(results_per_page)
                self.show()

    def shortcut_exists(self, shortcut: str) -> bool:
        """Checks if a given shortcut is valid"""
        for item in self.all_items:
            if hasattr(item, "shortcut") and item.shortcut == shortcut: return True
        return False

    def append_items(self, items, contextual=False):
        for item in items:
            self.append_item(item, contextual)

    def append_item(self, item, contextual=False):
        items = self._contextual_items if contextual else self._items
        item_ = self.get_item_from_shortcut(item.shortcut)
        if hasattr(item, "shortcut") and item_:
            raise RuntimeError(f"Duplicate shortcut for following item: `{repr(item)}`. Already used for `{repr(item_)}`")
        items.append(item)
