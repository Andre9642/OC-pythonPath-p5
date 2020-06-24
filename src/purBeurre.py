import json
import os.path
import signal
import sys
import models.database as db
import models.categories as categories
import models.products as products
from getpass import getpass

default_db_name = "pur_beurre"

def signal_handler(sig, frame):
    print("CTRL-C -- exit!\nBye")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_config():
    fp = "config.json"
    try:
        f = open(fp, "r", encoding="UTF-8")
        return json.load(f)
    except FileNotFoundError:
        return set_config()
    return get_config()

def set_config():
    print("Initializing config")
    host = input("Host: ")
    port = input("Port: ")
    user = input("User: ")
    password = getpass()
    db_name = input(f"Database name (default: {default_db_name}): ")
    db_infos = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "db_name": db_name,
    }
    f = open(fp, "w")
    json.dump(db_infos, f)
    f.close()
    return db_infos

db_infos = get_config()
print(db_infos)
# Initialize database
db.initialize(db_infos)

# Initialize categories
categories.initialize()

# Initialize products
products.initialize()

# Initialize main menu
#mainMenu = menus.MainMenu()
#mainMenu.show()
