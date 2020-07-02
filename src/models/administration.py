from . import database as db
from . import categories as categories
from . import products as products
from common import *

def create_database():
    db_infos = db.getConfig()
    db.terminate()
    db_ = db.DatabaseHandler(db_infos, select_database=False)
    db_.create_database()
    db_.terminate()
    db.initialize(db_infos)

def get_database_struct():
    db_name = db.handler._db_infos["database"]
    return {k: v.format(db_name=db_name) for k, v in struct_database.items()}

def drop_database():
    db.terminate()
    db_ = db.DatabaseHandler(select_database=False)
    db_.drop_database()
    db_.terminate()
    db.initialize()

def update_categories():
    res = categories.retrieve_from_api()
    if res:
        addedEntriesNumber, updatedEntriesNumber = categories.write_in_db(res)
        return addedEntriesNumber, updatedEntriesNumber

def update_products():
    res = products.handler.retrieve_from_api(page=int(nb_pages))
    if res:
        addedEntriesNumber, updatedEntriesNumber = products.handler.write_in_db(res)
        return addedEntriesNumber, updatedEntriesNumber
