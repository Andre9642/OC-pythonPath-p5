import controller.select_category as controller
from .menus_handler import Menu, MenuItem
from .select_food import SelectFood


class SelectCategory(Menu):

    title = "Sélectionnez la catégorie"
    table_name_products: str
    order_by_display: list = ["name ASC", "name DESC"]

    def __init__(
        self,
        table_name_products,
        **kwargs
    ):
        self.table_name_products = table_name_products
        super().__init__(**kwargs)

    def post_init(self):
        self.orderBy = 0
        success, res = controller.get_total_number()
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[1][0][0]
            self.init_pager(resNumber)

    def set_order_by(self, orderBy):
        self.orderBy = orderBy

    def get_order_by(self, display=False):
        s = (
            self.order_by_display
            if display
            else [
                "name ASC, productsNumber ASC",
                "name DESC, productsNumber ASC",
                "productsNumber ASC, name ASC",
                "productsNumber DESC, name ASC",
            ]
        )
        return s[int(self.orderBy)]

    def set_contextual_items(self):
        super().set_contextual_items()
        self.contextualItems.append(MenuItem(
            f"Sort by (currently: {self.get_order_by(True)})", "o", "switchOrderBy"))

    def switchOrderBy(self):
        orderByList = self.order_by_display
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
        self.set_order_by(choice - 1)
        self.show()

    def retrieve_items(self):
        self.clear_items()
        pager = self._pager
        start = pager.start
        nb_items = pager.items_by_page
        categories = controller.get_categories(start, nb_items)
        for i, category in enumerate(categories, start):
            self.append_item(MenuItem(
                category.name, i, "show_category", [category.id]))

    def show_category(self, id_category):
        select_food_menu = SelectFood(
            id_category=id_category,
            table_name_products=self.table_name_products,
            parent=self)
        select_food_menu.show()
