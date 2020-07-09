import controller.categories as controller
from .menus_handler import Menu, MenuItem
from .select_food import SelectFood


class SelectCategory(Menu):

    title = "Sélectionnez la catégorie"
    table_name_products: str
    _order_by_display: list = [
        "products DESC",
        "name ASC",
        "name DESC",
        "products ASC",
        ]

    def __init__(
        self,
        table_name_products,
        **kwargs
    ):
        self.table_name_products = table_name_products
        super().__init__(**kwargs)

    def post_init(self):
        self._order_by = 0
        success, res = controller.get_total_number()
        if not success:
            print(f"! {res}")
            self.goBack()
        else:
            resNumber = res[1][0][0]
            self.init_pager(resNumber)

    @property
    def order_by(self):
        return self._order_by_display[int(self._order_by)]

    @order_by.setter
    def order_by(self, order_by: int):
        if not isinstance(order_by, int):
            raise TypeError("wrong type")
        if order_by < len(self._order_by_display):
            self._order_by = order_by

    @property
    def contextual_items(self):
        items = super().contextual_items
        items.append(MenuItem(f"Trier par (actuellement : {self.order_by})", "o", "toggle_order_by"))
        return items

    def toggle_order_by(self):
        order_byList = self._order_by_display
        print("Veuillez choisir")
        for i, e in enumerate(order_byList, 1):
            print(f"{i} - {e}")
        choice = 0
        while choice < 1 or choice > len(order_byList):
            choice = input("> ")
            if not choice.isnumeric():
                choice = 0
            else:
                choice = int(choice)
        self.order_by = choice - 1
        self.show()

    def retrieve_items(self):
        self.clear_items()
        pager = self._pager
        start = pager.start
        nb_items = pager.items_by_page
        categories = controller.get_categories(start, nb_items, order_by=self.order_by)
        for i, category in enumerate(categories, start):
            self.append_item(MenuItem(
                ((category.name or "sans nom") + f" (~{category.products})"),
                i,
                "show_category",
                [category]))

    def show_category(self, category):
        select_food_menu = SelectFood(
            category=category,
            table_name_products=self.table_name_products,
            parent=self)
        select_food_menu.show()
