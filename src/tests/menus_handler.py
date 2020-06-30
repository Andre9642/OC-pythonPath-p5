"""Tests on module menu"""
import sys
sys.path.append("..")
from views.menus_handler import Menu, MenuItem

class TestMenu(Menu):
    """
    Description of TestMenu

    Attributes:
        attr1 (str): Description of 'attr1'

    Inheritance:
        Menu:
    """

    title = "Vive les tets !"
    description = "Choisissez votre activité"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.appendItems([
            MenuItem("Courir", "c", "course"),
            MenuItem("Coder", "dev", "code"),
            MenuItem("Danser", "d", "danse"),
            MenuItem("Dormir", "dodo", "dodo"),
            MenuItem("Lire", "l", "lecture"),
            MenuItem("Manger", "m", "miam")
        ])

    def lecture(self):
        """
        Description of lire
        """
        print("Vous souhaitez donc lire. Super !")
        self.show()

    @staticmethod
    def dodo():
        """
        description of dodo
        """
        print("Bonne nuit")

M = TestMenu()
M.show()
