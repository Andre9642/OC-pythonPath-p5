import controller.products as controller
from .menus_handler import Menu, MenuItem
from .show_product import ShowProduct as ShowProductSubMenu


class SelectFood(Menu):

    title = "Sélectionnez l'aliment"

    def __init__(self, category, table_name_products, parent):
        self.category = category
        self.table_name_products = table_name_products
        self.title = f"Sélectionnez l'aliment (catégorie : {category.name})"
        super().__init__(parent)

    def post_init(self):
        self.products = controller.get_products_from_category(self.category.id)
        self.init_pager(
            self.products["count"],
            self.products["page_size"]
        )

    def retrieve_items(self):
        pager = self.pager
        self.clear_items()
        if self.products["page"] != self.pager:
            self.products = controller.get_products_from_category(self.category.id, self.pager.page)
        for i, product in enumerate(self.products["products"], pager.start):
            self.append_item(MenuItem(
                product.name, i, "show_product", [product, self.category]
            ))

    def show_product(self, product, category):
        show_product_menu = ShowProductSubMenu(
            product=product,
            category=category,
            parent=self)
        show_product_menu.show()
