class SelectFoodCategorySubMenu(Menu):
    tableNameProducts: str
    items: list = []
    orderByDisplay: list = ["name ASC", "name DESC"]

    def __init__(
            self,
            tableNameProducts,
            title="Sélectionnez la catégorie",
            **kwargs):
        self.categories = categories.Categories()
        self.title = title
        self.tableNameProducts = tableNameProducts
        self.orderBy = 0
        success, res = db.handler.executeQuery(
            "SELECT COUNT(*) as nb FROM categories")
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[1][0][0]
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
            ("o", f"Sort by (currently: {self.getOrderBy(True)})", "switchOrderBy"))

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
                (str(i),
                 category.name,
                 "selectFood",
                 category,
                 self.tableNameProducts,
                 ))
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
            category=category,
            tableNameProducts=tableNameProducts,
            previousMenu=self)
        selectFoodMenu.show()


