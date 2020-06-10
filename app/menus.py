import sys
from typing import Union, Optional
from . import databaseHandler as db
from . import categories
from . import products
from . import paging


class Menu:

    title: str = None
    text: str = None
    items: list = []
    contextualItems: list = []
    previousMenu = None
    quitItem = ("q", "Quitter", "quit")
    previousMenuItem = lambda self: (
        "b",
        "Go back (%s)" % self.previousMenu.title,
        "goBack",
    )
    subMenus = {}
    maxLenShortcutItems = 0
    pager = None

    def __init__(self, previousMenu=None):
        if not self.title:
            self.title = "No title"
        self.previousMenu = previousMenu

    def setContextualItems(self):
        items = []
        pager = self.pager
        if pager:
            items.append(
                (
                    "c",
                    f"Change the number of items per page (currently : {self.pager.resultsByPage})",
                    "changeNumberResultsPerPage",
                )
            )
            if pager.curPage > 1:
                items.append(("f", "First page", "moveTo", paging.FIRSTPAGE))
                items.append(("j", "Previous page", "moveTo", paging.PREVIOUSPAGE))
            if pager.curPage != pager.nbPages:
                items.append(("k", "Next page", "moveTo", paging.NEXTPAGE))
                items.append(("l", "Last page", "moveTo", paging.LASTPAGE))
            if pager.nbPages > 1:
                items.append(("p", "Another page", "moveTo", paging.ANOTHERPAGE))
        if self.previousMenu:
            items.append(self.previousMenuItem())
        items.append(self.quitItem)
        self.contextualItems = items

    def preDisplayMenu(self):
        self.setContextualItems()
        items = self.items + self.contextualItems
        self.shortcutItems = [item[0] for item in items]
        self.nameItems = [item[1] for item in items]
        self.actionItems = [item[2] for item in items]
        self.argItems = [item[3:] for item in items]
        self.maxLenShortcutItems = max(
            [len(shortcutItem) for shortcutItem in self.shortcutItems]
        )

    def show(self, show_: bool=True):
        """Displays the menu and retrieves the user choice"""
        self.display()
        self.readInput()

    def display(self):
        """Displays the menu (all items with their shortcuts)
           A menu consists of:
            - A title
            - An optional text (an extra-info about the menu, an error messages, etc.)
            - Items of the form: '<shortcut> - <name>'
        """
        self.preDisplayMenu()
        print(f"=== {self.title} ===")
        if self.text:
            print(self.text)
        for shortcut, name in zip(self.shortcutItems, self.nameItems):
            print(f"%-{self.maxLenShortcutItems}s -- %s" % (shortcut, name))

    def readInput(self):
        """Retrieves the user choice
           User should type the shortcut corresponding to the desired menu item
           If input is invalid, we ask another input
        """
        choice = ""
        while not choice or choice not in self.shortcutItems:
            if choice:
                print("! Invalid input")
            choice = input("> ")
            if choice == "q":
                sys.exit(0)
        idx = self.shortcutItems.index(choice)
        action = self.actionItems[idx]
        args = self.argItems[idx] if len(self.argItems[idx]) > 0 else None
        self.executeAction(action, args)

    def executeAction(self, action, args=None):
        """Starts the script related to the menu item chosen"""
        if not self.isValidChoice(action):
            print("! Feature not implemented yet")
            self.display()
            self.readInput()
        else:
            if args:
                getattr(self, action)(*args)
            else:
                getattr(self, action)()

    def isValidChoice(self, choice):
        """Checks if the script attached to an item is valid"""
        return bool(choice) and hasattr(self, choice)

    def goBack(self):
        """Displays the previous menu"""
        if self.previousMenu:
            self.previousMenu.show()
            del self

    def moveTo(self, direction):
        if not self.pager:
            return
        res = self.pager.moveTo(direction)
        if res:
            self.display()
        self.readInput()

    def changeNumberResultsPerPage(self):
        resultsPerPage = 0
        while resultsPerPage < 2:
            resultsPerPage = input("Result number per page: ")
            if not resultsPerPage.isnumeric():
                resultsPerPage = 0
            else:
                resultsPerPage = int(resultsPerPage)
                self.pager.setResultPerPage(resultsPerPage)
                self.show()


class AdministrationSubMenu(Menu):

    title = "Administration"
    items = [
        ("cdb", "Créer la base de donnée", "createDatabase"),
        ("vsdb", "Voir la structure de la base de donnée ", "seeDatabaseStruct"),
        (
            "uc",
            "Mettre à jour les catégories depuis l'API Open Food Facts",
            "updateCategories",
        ),
        (
            "up",
            "Mettre à jour les produits depuis l'API Open Food Facts",
            "updateProducts",
        ),
        ("ddb", "Supprimer la base de donnée", "dropDatabase"),
    ]

    def createDatabase(self):
        db.terminate()
        db_ = db.DatabaseHandler(selectDatabase=False)
        db_.createDatabase()
        db_.terminate()
        db.initialize()
        self.show()

    def seeDatabaseStruct(self):
        print("```")
        db.getStructDatabase()
        print("```")
        self.show()

    def dropDatabase(self):
        db.terminate()
        db_ = db.DatabaseHandler(selectDatabase=False)
        db_.dropDatabase()
        db_.terminate()
        db.initialize()
        self.show()

    def updateCategories(self):
        res = categories.handler.retrieveFromAPI()
        if res:
            addedEntriesNumber, updatedEntriesNumber = categories.handler.writeInDB(res)
            print(
                f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
            )
        self.show()

    def updateProducts(self):
        pageNumber = input("Nombre de pages à télécharger : ")
        res = products.handler.retrieveFromAPI(page=int(pageNumber))
        if res:
            addedEntriesNumber, updatedEntriesNumber = products.handler.writeInDB(res)
            print(
                f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
            )
        self.show()


class SelectFoodCategorySubMenu(Menu):
    tableNameProducts: str
    items: list = []
    orderByDisplay: list = [
        "name ASC",
        "name DESC",
        "number of products ASC",
        "number of products DESC",
    ]

    def __init__(self, tableNameProducts, title="Sélectionnez la catégorie", **kwargs):
        self.categories = categories.Categories()
        self.title = title
        self.tableNameProducts = tableNameProducts
        self.orderBy = 0
        success, res = db.handler.executeQuery(
            "SELECT COUNT(*), c.id_api as id_api, count(p.category) as productsNumber"
            " FROM categories as c"
            f" LEFT JOIN {tableNameProducts} as p ON c.id_api = p.category"
            " GROUP BY p.category, c.id_api"
            " HAVING productsNumber > 0"
        )
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[0]
            self.pager = paging.Paging(self.display, resNumber)
        super().__init__(**kwargs)

    def setOrderBy(self, orderBy):
        self.orderBy = orderBy

    def getOrderBy(self, display=False):
        s = (
            self.orderByDisplay
            if display
            else [
                "name ASC, productsNumber ASC",
                "name DESC, productsNumber ASC",
                "productsNumber ASC, name ASC",
                "productsNumber DESC, name ASC",
            ]
        )
        return s[int(self.orderBy)]

    def setContextualItems(self):
        super().setContextualItems()
        self.contextualItems.append(
            ("o", f"Sort by (currently: {self.getOrderBy(True)})", "switchOrderBy")
        )

    def switchOrderBy(self):
        orderByList = self.orderByDisplay
        print("Please choose")
        for i, e in enumerate(orderByList, 1):
            print(f"{i} - {e}")
        choice = 0
        while choice < 1 or choice > len(orderByList):
            choice = input("> ")
            if not choice.isnumeric():
                choice = 0
            else:
                choice = int(choice)
        self.setOrderBy(choice - 1)
        self.show()

    def displayWithPagination(self, min, max):
        if self.pager.nbPages < 1:
            return print("! No item. Please update categories.")
        self.items = []
        categories = self.categories.display(
            tableNameProducts=self.tableNameProducts,
            min=min,
            max=max,
            orderBy=self.getOrderBy(),
        )
        i = min
        for category in categories:
            self.items.append(
                (
                    f"{i}",
                    f"{category.name} ({category.productsNumber})",
                    "selectFood",
                    category,
                    self.tableNameProducts,
                )
            )
            i += 1

    def display(self):
        pager = self.pager
        pagerPosition = pager.currentPosition()
        print(pagerPosition)
        self.displayWithPagination(self.pager.start, self.pager.resultsByPage)
        self.preDisplayMenu()
        super().display()
        print(pagerPosition)

    def selectFood(self, category, tableNameProducts):
        selectFoodMenu = SelectFood(
            category=category, tableNameProducts=tableNameProducts, previousMenu=self
        )
        selectFoodMenu.show()


class SelectFood(Menu):
    tableNameProducts: str = None
    title: str = "Sélectionnez l'aliment"
    items: list = []

    def __init__(self, category, tableNameProducts, previousMenu=None):
        if not isinstance(category, categories.Category):
            raise TypeError("category: Wrong type")
        self.title = f"Sélectionnez l'aliment (catégorie : {category.name})"
        self.tableNameProducts = tableNameProducts
        self.category = category
        super().__init__(previousMenu)
        self.products = products.handler
        success, res = db.handler.executeQuery(
            f"SELECT COUNT(*) FROM {tableNameProducts} WHERE category = %(category)s",
            {"category": category.id},
        )
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[-1][0][0]
            self.pager = paging.Paging(self.display, resNumber)

    def displayWithPagination(self, min, max):
        self.items = []
        if self.pager.nbPages < 1:
            return print("! No item. Please update products.")
        products_ = self.products.display(
            tableNameProducts=self.tableNameProducts,
            min=min,
            max=max,
            categoryID=self.category.id,
        )
        i = min
        for product in products_:
            self.items.append((f"{i}", product.name, "showProduct", product))
            i += 1

    def display(self):
        pager = self.pager
        pagerPosition = pager.currentPosition()
        print(pagerPosition)
        self.displayWithPagination(self.pager.start, self.pager.resultsByPage)
        self.preDisplayMenu()
        super().display()
        print(pagerPosition)

    def showProduct(self, product):
        showProductMenu = ShowProductMenu(product, self)
        showProductMenu.show()


class ShowProductMenu(Menu):
    title = "Détail d'un produit"
    items = []

    def __init__(self, product, previousMenu):
        self.product = product
        self.items = [("e", "Éditer ce produit", "editProduct")]
        super().__init__(previousMenu)

    def display(self, **kwargs):
        product = self.product
        self.text = (
            f"Nom : {product.name}\n"
            f"Marque : {product.brands}\n"
            f"Sel : {product.salt}\n"
            f"Sucre : {product.sugars}\n"
            f"Magasin : {product.stores}\n"
            f"URL : {product.url}\n"
        )
        super().display(*kwargs)

    def editProduct(self):
        product = self.product
        name = input(f"Nom ({product.name}) : ")
        if not name:
            name = product.name
        brands = input(f"Marque ({product.brands}) : ")
        if not brands:
            brands = product.brands
        nutrition_grade = input(f"Grade nutritionnel ({product.nutrition_grade}) : ")
        if not nutrition_grade:
            nutrition_grade = product.nutrition_grade
        fat = input(f"Gras ({product.fat}) : ")
        if not fat:
            fat = product.fat
        saturated_fat = input(f"Gras saturé ({product.saturated_fat}) : ")
        if not saturated_fat:
            saturated_fat = product.saturated_fat
        sugars = input(f"Sucres({product.sugars}) : ")
        if not sugars:
            sugars = product.sugars
        salt = input(f"Sel ({product.salt}) : ")
        if not salt:
            salt = product.salt
        newProduct = products.Product(
            product.id,
            name,
            brands,
            nutrition_grade,
            fat,
            saturated_fat,
            sugars,
            salt,
            product.url,
            product.category,
        )
        self.product = newProduct
        products.handler.writeInDB([newProduct], "substitute_products")
        self.show()


class replacedFoodSubMenu(Menu):

    title: str = "Aliments substitués"


class MainMenu(Menu):

    title: str = "Menu principal"
    items: list = [
        (
            "1",
            "Quel aliment souhaitez-vous remplacer ?",
            "selectFoodCategory",
            "products",
        ),
        (
            "2",
            "Retrouver mes aliments substitués.",
            "selectFoodCategory",
            "substitute_products",
        ),
        ("a", "Administration", "administration"),
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
