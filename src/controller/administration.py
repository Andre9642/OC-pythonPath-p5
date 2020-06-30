import models.database as db
import models.categories as categories

def create_database():
    db_infos = db.getConfig()
    db.terminate()
    db_ = db.DatabaseHandler(db_infos, select_database=False)
    db_.create_database()
    db_.terminate()
    db.initialize(db_infos)

def get_database_struct():
    return db.get_struct_database()

def drop_database():
    db.terminate()
    db_ = db.DatabaseHandler(select_database=False)
    db_.drop_database()
    db_.terminate()
    db.initialize()

def update_categories():
    res = categories.handler.retrieve_from_api()
    if res:
        addedEntriesNumber, updatedEntriesNumber = categories.handler.writeInDB(res)
        return addedEntriesNumber, updatedEntriesNumber

def update_products(nb_pages):
    res = products.handler.retrieve_from_api(page=int(nb_pages))
    if res:
        addedEntriesNumber, updatedEntriesNumber = products.handler.writeInDB(res)
        return addedEntriesNumber, updatedEntriesNumber
