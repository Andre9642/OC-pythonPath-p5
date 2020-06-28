import models.database as db

def createDatabase():
    db.terminate()
    db_ = db.DatabaseHandler(selectDatabase=False)
    db_.createDatabase()
    db_.terminate()
    db.initialize()

def get_database_struct():
    return db.get_struct_database()

def drop_database():
    db.terminate()
    db_ = db.DatabaseHandler(selectDatabase=False)
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
