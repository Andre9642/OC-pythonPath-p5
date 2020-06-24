class AdministrationSubMenu(Menu):

    title = "Administration"
    items = [
        ("cdb",
         "Créer la base de donnée",
         "createDatabase"),
        ("vsdb",
         "Voir la structure de la base de donnée ",
         "seeDatabaseStruct"),
        ("uc",
         "Mettre à jour les catégories depuis l'API Open Food Facts",
         "updateCategories",),
        ("up",
         "Mettre à jour les produits depuis l'API Open Food Facts",
         "updateProducts",),
        ("ddb",
         "Supprimer la base de donnée",
         "dropDatabase"),
    ]

    def createDatabase(self):
        db.terminate()
        db_ = db.DatabaseHandler(selectDatabase=False)
        db_.createDatabase()
        db_.terminate()
        db.initialize()
        self.show()

    def seeDatabaseStruct(self):
        print("```")
        db.getStructDatabase()
        print("```")
        self.show()

    def dropDatabase(self):
        db.terminate()
        db_ = db.DatabaseHandler(selectDatabase=False)
        db_.dropDatabase()
        db_.terminate()
        db.initialize()
        self.show()

    def updateCategories(self):
        res = categories.handler.retrieveFromAPI()
        if res:
            addedEntriesNumber, updatedEntriesNumber = categories.handler.writeInDB(
                res)
            print(
                f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
            )
        self.show()

    def updateProducts(self):
        userInput = "?"
        while not userInput.isnumeric() or int(userInput) < 1:
            userInput = input("Nombre de pages à télécharger : ")
        res = products.handler.retrieveFromAPI(page=int(userInput))
        if res:
            addedEntriesNumber, updatedEntriesNumber = products.handler.writeInDB(
                res)
            print(
                f"Done. New entries: {addedEntriesNumber}, updated: {updatedEntriesNumber}"
            )
        self.show()


