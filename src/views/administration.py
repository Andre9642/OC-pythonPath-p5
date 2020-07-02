import controller.administration as controller
from .menus_handler import Menu, MenuItem

class Administration(Menu):

    title = "Administration"

    def post_init(self):
        self.append_items([
            MenuItem("Installation de la base", "i", "install"),
            MenuItem("Créer/compléter la structure de la base de donnée", "cdb", "create_database", level=1),
            MenuItem("Mettre à jour les catégories depuis l'API Open Food Facts", "uc", "update_categories", level=1),
            MenuItem("Mettre à jour les produits depuis l'API Open Food Facts", "up", "update_products", level=1),
            MenuItem("Voir la structure de la base de donnée", "vsdb", "see_database_struct", level=0),
            MenuItem("Supprimer la base de donnée", "ddb", "drop_database", level=0),
        ])

    def see_database_struct(self):
        res = controller.get_database_struct()
        print("```")
        for k, v in res.items(): 
            print(v)
        print("```")
        input()
        self.show()

    def create_database(self):
        controller.create_database()
        self.show(True)

    def update_categories(self):
        addedEntriesNumber, updatedEntriesNumber = controller.update_categories()
        print(f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}")
        self.show(True)

    def update_products(self):
        user_input = "?"
        while not user_input.isnumeric() or int(user_input) < 1:
            user_input = input("Nombre de pages à télécharger : ")
        page = int(user_input)
        addedEntriesNumber, updatedEntriesNumber = controller.update_products(page)
        print(
            f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
        )
        self.show(True)
