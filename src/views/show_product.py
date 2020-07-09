import os
import controller.products as controller
from .menus_handler import Menu, MenuItem
from .substitute_products import SubstituteProducts as SubstituteProductsSubMenu


class ShowProduct(Menu):

    def __init__(self, product, category, parent):
        self.product = product
        self.category = category
        super().__init__(parent)

    def post_init(self):
        product = self.product
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
        if product.saturated_fat:
            text += f"Matières grasses : {product.fat}g\n"
        if product.saturated_fat:
            text += f"Acides gras saturés : {product.saturated_fat}g\n"
        if product.stores:
            text += f"Magasin : {product.stores}\n"
        if product.code:
            text += f"Code barre : {product.code}\n"
        text += f"URL : {product.url}\n"
        self.description = text

    @property
    def contextual_items(self):
        items = [
            MenuItem("Ouvrir la fiche produit sur le site d'openfoodfacts",
                     'o', "open_in_browser"),
            MenuItem("Voir les produits de substitution",
                     'a', "substitute_product"),
            MenuItem("Enregistrer ce produit", 'e', "save_product")]
        return items + super().contextual_items

    def open_in_browser(self):
        print("Ouverture dans le navigateur...")
        os.startfile(self.product.url)
        self.show(True)

    def save_product(self):
        self.show(True)

    def substitute_product(self):
        substitute_product_menu = SubstituteProductsSubMenu(
            product=self.product,
            category=self.category,
            parent=self)
        substitute_product_menu.show()
