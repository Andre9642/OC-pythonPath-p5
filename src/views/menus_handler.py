"""Menus module"""
import sys
import config.config as config
from typing import Callable, List
from .paging import Paging

class MenuItem:
    """A Class to represent a menu item"""

    name: str = ''
    shortcut: str = ''
    func: str = None
    args: List = []
    level: int = 0

    def __init__(self,
                 name: str,
                 shortcut: str,
                 func: Callable,
                 args: List=[],
                 level: int=0):
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
        self.shortcut = str(shortcut)
        self.func = func
        self.args = args
        self.level = level
        if not self.check():
            raise ValueError("Invalid argument provided")

    def __repr__(self):
        return f"%{'  '* self.level}{self.shortcut} - {self.name}"

    def check(self):
        """
        Ensures that minimal attributes are valid
        """
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Invalid value/type for name")
        if not self.shortcut or not isinstance(self.shortcut, str):
            raise ValueError("Invalid value/type for shortcut")
        if not hasattr(self, "func"):
            raise ValueError("Invalid value/type for func")
        if not isinstance(self.level, int):
            raise ValueError("Invalid value/type for level")
        return True

class Menu:

    """A class that represents a menu"""

    title: str = None
    description: str = None
    parent = None
    _pager = None

    def __init__(self, parent=None):
        self.title = self.title or "No title"
        self.parent = parent
        self._sub_menus = {}
        self._items = []
        self._contextual_items = []
        self.post_init()

    def post_init(self):
        raise NotImplementedError
    
    def init_pager(self, nb_items, items_by_page=14):
        self._pager = Paging(nb_items, items_by_page)

    @property
    def pager(self):
        return self._pager

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
        pager = self._pager
        if pager:
            items += [MenuItem(*item) for item in pager.contextual_items]
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

    def clear_items(self):
        self._items.clear()

    @property
    def all_items(self):
        """returns menu items and contextual items"""
        return self.items + self.contextual_items

    def max_size_shortcut(self):
        max_size = 0
        for item in self.all_items:
            if not hasattr(item, "shortcut"):
                continue
            cur_size = 2* item.level + len(item.shortcut)
            if cur_size > max_size:
                max_size = cur_size
        return max_size

    def show(self, pause=False):
        """Displays the menu and retrieves the user choice"""
        if pause:
            input("Press enter to display the menu")
        self.display()
        self.read_input()

    def display(self):
        """Displays the menu"""
        pager = self._pager
        print(f"=== {self.title} ===")
        if self.description:
            print(self.description)
        self.retrieve_items()
        items = self.all_items
        pager_info = None
        if pager:
            if pager.total_items:
                pager_info = pager.current_position()
                print(pager_info)
            else:
                print("! no item")
        max_size_shortcut = self.max_size_shortcut()
        for item in items:
            if not isinstance(item, MenuItem):
                raise TypeError("Wrong type")
            print(f"%-{max_size_shortcut}s -- %s" % (("  " * item.level) + item.shortcut, item.name))
        if pager_info: print(pager_info)

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
        self._pager.move_to(direction)
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
                self._pager.items_by_page = results_per_page
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

    def quit(self):
        config.terminate()
        print("Good bye!")
        sys.exit(1)

    def retrieve_items(self):
        pass
