import controller.products as controller
from .menus_handler import Menu, MenuItem

class SubstituteProducts(Menu):
    
    def __init__(self, product, category, parent):
        self.product = product
        self.category = category
        self.title = f"Substituts pour {product.name}"
        super().__init__(parent)

    def post_init(self):
        product = self.product
        self.products = controller.get_product_substitutes(product.name, self.category.id, self.product.id)
        self.init_pager(
            self.products["count"],
            self.products["page_size"]
        )

    def retrieve_items(self):
        pager = self.pager
        self.clear_items()
        if self.products["page"] != self.pager:
            product = self.product
            self.products = controller.get_product_substitutes(product.name, self.category.id, self.product.id)
        for i, product in enumerate(self.products["products"], pager.start):
            self.append_item(MenuItem(
                product.name, i, "show_product", [product, self.category]
            ))

    def show_product(self, product, category):
        self.parent.product = product
        self.parent.category=category
        self.go_back()
