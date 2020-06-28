import json
import os.path
import signal
import sys
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)
import models.database as db
import models.categories as categories
import models.products as products
import views.home as home
from getpass import getpass

configFile = "config.json"
default_host = "127.0.0.1"
default_user = "root"
default_port = "3306"
default_db_name = "pur_beurre"
def signal_handler(sig, frame):
    print("CTRL-C -- exit!\nBye")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_config():
    try:
        f = open(configFile, "r", encoding="UTF-8")
        return json.load(f)
    except FileNotFoundError:
        return set_config()
    return get_config()

def set_config():
    print("Initializing config")
    host = input(f"Host (default: {default_host}): ")
    port = input(f"Port (default: {default_port}): ")
    user = input(f"User (default: {default_user}): ")
    password = getpass()
    db_name = input(f"Database name (default: {default_db_name}): ")
    db_infos = {
        "host": host or default_host,
        "port": port or default_port,
        "user": user or default_user,
        "password": password,
        "db_name": db_name or default_db_name,
    }
    f = open(configFile, "w")
    json.dump(db_infos, f)
    f.close()
    return db_infos

db_infos = get_config()
# Initialize database
db.initialize(db_infos)


Home = home.Home()
Home.show()