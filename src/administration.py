import os.path
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)
import config.config as config
import controller.categories as categories
import controller.products as products
import models.database as db

config.initialize()

def create_database():
    db_infos = db.getConfig()
    db_ = db.DatabaseHandler(db_infos, select_database=False)
    db_.create_database()
    db_.terminate()
    db.initialize(db_infos)

def get_database_struct():
    db_name = db.handler._db_infos["database"]
    o = {k: v.format(db_name=db_name) for k, v in db.struct_database.items()}
    for k, v in o.items():
        print(f"--- {k}\n{v}")

def drop_database():
    db.terminate()
    db_ = db.DatabaseHandler(select_database=False)
    db_.drop_database()
    db_.terminate()
    db.initialize()

def update_categories():
    res = categories.retrieve_from_api()
    if res:
        res = categories.process_json(res)
        res = [category for category in res if category.name and category.products > 0]
        addedEntriesNumber, updatedEntriesNumber = categories.write_in_db(res)
        print(f"Nouvelles entrées : {addedEntriesNumber}, mise à jour : {updatedEntriesNumber}")
    else:
        print("error")

def update_products():
    res = products.handler.retrieve_from_api(page=int(nb_pages))
    if res:
        addedEntriesNumber, updatedEntriesNumber = products.handler.write_in_db(res)
        return addedEntriesNumber, updatedEntriesNumber

def drop_database():
    db.handler.drop_database()


actions = {
    "Créer la BDD": create_database,
    "Mettre à jour les catégories": update_categories,
    "Mettre à jour les produits": update_products,
    "Supprimer la BDD": drop_database,
    "Montrer la structure de la BDD": get_database_struct,
    "Quitter": sys.exit,
}


while True:
    print("Choisissez une actions :")
    for i, action in enumerate(actions, 1):
        print(f"{i} - {action}")
    choice = input("> ")
    if choice.isnumeric():
        choice = int(choice)-1
        if choice < len(actions):
            k = list(actions.keys())[choice]
            print (f"OK. {k}")
            actions[k]()
