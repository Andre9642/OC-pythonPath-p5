from .menus_handler import Menu, MenuItem
from .administration import Administration as AdministrationSubMenu

class Home(Menu):

    title = "Menu principal"
    description = "Bienvenue dans purBeurre !"

    def post_init(self):
        self.append_items([
            MenuItem("Quel aliment souhaitez-vous remplacer ?", '1', "select_food_category", ["products"]),
            MenuItem("Retrouver mes aliments substitués.", '2', "select_food_category", ["substitute_products"]),
            MenuItem("Administration", 'a', "administration"),
        ])

    def administration(self):
        name = "administration"
        if name not in self._sub_menus.keys():
            self._sub_menus[name] = AdministrationSubMenu(parent=self)
        self._sub_menus[name].show()

    def select_food_category(self, tableNameProducts):
        name = "select_food_category%s" % tableNameProducts
        if name not in self._sub_menus.keys():
            self._sub_menus[name] = select_food_categorySubMenu(
                tableNameProducts=tableNameProducts, parent=self
            )
        self._sub_menus[name].show()

    def replaced_food(self):
        name = "replaced_food"
        if name not in self._sub_menus.keys():
            self._sub_menus[name] = replaced_foodSubMenu(parent=self)
        self._sub_menus[name].show()
