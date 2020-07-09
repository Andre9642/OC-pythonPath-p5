import controller.products as controller
from .menus_handler import Menu, MenuItem

class ShowProduct(Menu):

    def __init__(self, product, category, parent):
        self.product = product
        self.category = category
        self.title = product.name
        text = ""
        if product.brands:
            text += f"Marque : {product.brands}\n"
        if product.ingredients_text:
            text += f"Ingrédients : {product.ingredients_text}\n"
        if product.nutriscore_grade:
            text += f"Nutriscore : {product.nutriscore_grade.upper()}\n"
        if product.quantity:
            text += f"Quantité : {product.quantity}\n"
        if product.salt > 0:
            text += f"Sel : {product.salt}g\n"
        if product.sugars > 0:
            text += f"Sucre : {product.sugars}g\n"
        if product.stores:
            text += f"Magasin : {product.stores}\n"
        if product.code:
            text += f"Code barre : {product.code}\n"
        text += f"URL : {product.url}\n"
        self.description = text
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
        show_product_menu = ShowProduct(
            product=product,
            category=category,
            parent=self)
        show_product_menu.show()
