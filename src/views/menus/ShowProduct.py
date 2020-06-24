class ShowProductMenu(Menu):
    title = "Détail d'un produit"
    items = []

    def __init__(self, product, previousMenu):
        self.product = product
        self.items = [("e", "Éditer ce produit", "editProduct")]
        super().__init__(previousMenu)

    def display(self, **kwargs):
        product = self.product
        self.text = (
            f"Nom : {product.name}\n"
            f"Marque : {product.brands}\n"
            f"Sel : {product.salt}\n"
            f"Sucre : {product.sugars}\n"
            f"Magasin : {product.stores}\n"
            f"URL : {product.url}\n"
        )
        super().display(*kwargs)

    def editProduct(self):
        product = self.product
        name = input(f"Nom ({product.name}) : ")
        if not name:
            name = product.name
        brands = input(f"Marque ({product.brands}) : ")
        if not brands:
            brands = product.brands
        nutrition_grade = input(
            f"Grade nutritionnel ({product.nutrition_grade}) : ")
        if not nutrition_grade:
            nutrition_grade = product.nutrition_grade
        fat = input(f"Gras ({product.fat}) : ")
        if not fat:
            fat = product.fat
        saturated_fat = input(f"Gras saturé ({product.saturated_fat}) : ")
        if not saturated_fat:
            saturated_fat = product.saturated_fat
        sugars = input(f"Sucres({product.sugars}) : ")
        if not sugars:
            sugars = product.sugars
        salt = input(f"Sel ({product.salt}) : ")
        if not salt:
            salt = product.salt
        newProduct = products.Product(
            product.id,
            name,
            brands,
            nutrition_grade,
            fat,
            saturated_fat,
            sugars,
            salt,
            product.url,
            product.category,
        )
        self.product = newProduct
        products.handler.writeInDB([newProduct], "substitute_products")
        self.show()


