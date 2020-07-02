import controller.select_food as controller
from .menus_handler import Menu, MenuItem


class SelectFood(Menu):

    title = "Sélectionnez l'aliment"

    def __init__(self, id_category, table_name_products, parent):
        self.id_category = id_category
        self.table_name_products = table_name_products
        super().__init__(parent)

    def post_init(self):
        self.products = controller.get_products_from_category(self.id_category)
        self.init_pager(len(self.products))

    def retrieve_items(self):
        self.clear_items()
        pager = self.pager
        if not pager:
            return
        for i, product in enumerate(self.products[pager.start-1:pager.end], pager.start):
            self.append_item(MenuItem(
                product.name, i, "show_product", [product]
            ))
    def show_product(self, product):
        text = (
            f"Nom : {product.name}\n"
            f"Marque : {product.brands}\n"
            f"Sel : {product.salt}\n"
            f"Sucre : {product.sugars}\n"
            f"Magasin : {product.stores}\n"
            f"URL : {product.url}\n"
        )
        print(text)
        input("Souhaitez-vous enregistrer ce produit ? ")
        