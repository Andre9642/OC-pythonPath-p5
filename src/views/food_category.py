from .menus_handler import Menu, MenuItem
import controller.food_category as controller
from .paging import Paging

class FoodCategory(Menu):

    title="Sélectionnez la catégorie",
    tableNameProducts: str
    orderByDisplay: list = ["name ASC", "name DESC"]
    
    def __init__(
        self,
        tableNameProducts,
        **kwargs
    ):
        self.tableNameProducts = tableNameProducts
        super().__init__(**kwargs)

    def post_init(self):
        self.orderBy = 0
        success, res = controller.get_total_number()
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[1][0][0]
            self.pager = Paging(resNumber)

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

    def display_with_pagination(self, min, max):
        if self.pager._nb_pages < 1:
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
        pagerPosition = pager.current_position()
        print(pagerPosition)
        self.display_with_pagination(self.pager.start, self.pager.items_by_page)
        super().display()
        print(pagerPosition)

    def selectFood(self, category, tableNameProducts):
        selectFoodMenu = SelectFood(
            category=category,
            tableNameProducts=tableNameProducts,
            previousMenu=self)
        selectFoodMenu.show()


