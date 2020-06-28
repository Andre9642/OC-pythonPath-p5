import controller.administration as controller
from .menus_handler import Menu, MenuItem

class Administration(Menu):

    title = "Administration"

    def post_init(self):
        self.append_items([
            MenuItem("Créer la base de donnée", "cdb", "createDatabase"),
            MenuItem("Voir la structure de la base de donnée", "vsdb", "see_database_struct"),
            MenuItem("Mettre à jour les catégories depuis l'API Open Food Facts", "uc", "updateCategories"),
            MenuItem("Mettre à jour les produits depuis l'API Open Food Facts", "up", "update_products"),
            MenuItem("Supprimer la base de donnée", "ddb", "drop_database"),
        ])

    def see_database_struct(self):
        res = controller.get_database_struct()
        print("```")
        for k, v in res.items(): 
            print(v)
        print("```")
        input()
        self.show()
    def createDatabase(self):
        controller.createDatabase()
    
    def update_categories(self):
        addedEntriesNumber, updatedEntriesNumber = controller.update_categories()
        print(f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}")
        input()
        self.display()

    def update_products(self):
        user_input = "?"
        while not user_input.isnumeric() or int(user_input) < 1:
            user_input = input("Nombre de pages à télécharger : ")
        page = int(user_input)
        addedEntriesNumber, updatedEntriesNumber = controller.update_products(page)
        print(
            f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
        )
        input()
        self.display()
