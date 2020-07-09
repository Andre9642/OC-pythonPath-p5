import controller.products as controller
from .menus_handler import Menu, MenuItem


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
                product.name, i, "show_product", [product]
            ))

    def show_product(self, product):
        text = (
            f"Nom : {product.name}\n"
            f"Marque : {product.brands}\n")
        if product.nutriscore_grade:
            text += f"Nutriscore : {product.nutriscore_grade}\n"
        text += (
            f"Sel : {product.salt}\n"
            f"Sucre : {product.sugars}\n"
            f"Magasin : {product.stores}\n"
            f"URL : {product.url}\n"
        )
        print(text)
        input("Souhaitez-vous enregistrer ce produit ? ")
        self.go_back()
