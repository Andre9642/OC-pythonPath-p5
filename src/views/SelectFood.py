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
            f"SELECT COUNT(*) FROM {tableNameProducts} as p"
            " RIGHT JOIN products_categories as pc ON p.id = pc.id_product"
            " WHERE id_category = %(category)s",
            {"category": category.id},
        )
        if not success:
            raise RuntimeError(res)
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


