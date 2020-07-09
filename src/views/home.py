from .menus_handler import Menu, MenuItem
from .select_category import SelectCategory as FoodCategorySubMenu


class Home(Menu):

    title = "Menu principal"
    description = "Bienvenue dans purBeurre !"

    def post_init(self):
        self.append_items([
            MenuItem("Quel aliment souhaitez-vous remplacer ?",
                     '1', "food_category"),
            MenuItem("Retrouver mes aliments substitués.", '2',
                     "replaced_food"),
        ])

    def food_category(self):
        name = "select_food_category"
        if name not in self._sub_menus.keys():
            self._sub_menus[name] = FoodCategorySubMenu(self)
        self._sub_menus[name].show()

    def replaced_food(self):
        name = "replaced_food"
        if name not in self._sub_menus.keys():
            self._sub_menus[name] = Replaced_foodSubMenu(self)
        self._sub_menus[name].show()
