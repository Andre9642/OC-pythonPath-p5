import Menus

class MainMenu(Menu):

    title: str = "Menu principal"
    items: list = [
        (
            "1",
            "Quel aliment souhaitez-vous remplacer ?",
            "selectFoodCategory",
            "products",
        ),
        ("2",
         "Retrouver mes aliments substitués.",
         "selectFoodCategory",
         "substitute_products",),
        ("a",
         "Administration",
         "administration"),
    ]

    def administration(self):
        name = "administration"
        if name not in self.subMenus.keys():
            self.subMenus[name] = AdministrationSubMenu(previousMenu=self)
        self.subMenus[name].show()

    def selectFoodCategory(self, tableNameProducts):
        name = "selectFoodCategory%s" % tableNameProducts
        if name not in self.subMenus.keys():
            self.subMenus[name] = SelectFoodCategorySubMenu(
                tableNameProducts=tableNameProducts, previousMenu=self
            )
        self.subMenus[name].show()

    def replacedFood(self):
        name = "replacedFood"
        if name not in self.subMenus.keys():
            self.subMenus[name] = replacedFoodSubMenu(previousMenu=self)
        self.subMenus[name].show()
