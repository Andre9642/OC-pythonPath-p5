"""Menus module"""
import sys
from typing import Callable, List


class MenuItem:
    """A Class that represents a menu item"""

    name: str = ''
    shortcut: str = ''
    func: Callable = None
    args: List = []

    def __init__(self,
                 name: str,
                 shortcut: str,
                 func: Callable,
                 args: list):
        """
        Initialize instance of class and check if arguments provided are valid

        Args:
            self (undefined):
            name (str): the label for the menu item
            shortcut (str): a shortcut that lets to user to choose this item
            when the menu and the prompt appear
            func (Callable): the function to call when we select this item
            args (list): arguments to provide when we call `func()`

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
        if not callable(self.func):
            return False
        return True


class Menu:

    """A class that represents a menu"""

    _items: List[MenuItem] = []
    _contextual_items: List[MenuItem] = []
    _previous_menu = None
    subMenus = {}
    pager = None
    title: str = None
    text: str = None

    def __init__(self, _previous_menu=None):
        self.title = self.title or "No title"
        self._previous_menu = _previous_menu

    @property
    def previous_menu_item(self):
        """Returns the previous menu item"""
        previous_menu_title = self._previous_menu.title
        return ("b",
                f"Go back ({previous_menu_title})"
                "go_back")

    @previous_menu_item.setter
    def previous_menu_item(self, previous_menu):
        self._previous_menu = previous_menu

    @property
    def contextual_items(self):
        """returns contextual/dynamic items such as next/previous page"""
        items = []
        pager = self.pager
        if pager:
            items += self.pager.contextual_items
        if self._previous_menu:
            items.append(self.previous_menu_item)
        items.append(("q", "Quitter", "quit"))
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
        if self.text:
            print(self.text)
        for item in self.all_items:
            #print(f"%-{self._shortcut_len_max}s -- {name}" % shortcut)
            print(item)

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
        if self._previous_menu:
            self._previous_menu.show()
            del self

    def get_item_from_shortcut(self, shortcut):
        """returns an item from its shortcut"""
        for item in self.all_items:
            if item.shortcut == shortcut:
                return item
        return None
