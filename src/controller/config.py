import json
from getpass import getpass
import models.database as db
import models.categories as categories
import models.products as products

configFile = "config_pur_beurre.json"
default_host = "127.0.0.1"
default_user = "root"
default_port = "3306"
default_db_name = "pur_beurre"


def get_config():
    conf = {}
    try:
        f = open(configFile, "r", encoding="UTF-8")
        conf = json.load(f)
        f.close()
    except FileNotFoundError:
        pass
    return conf

def declare_db_config():
    print("Initializing database config")
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
    conf["db"] = db_infos
    return db_infos

def initialize():
    global conf
    conf = get_config()
    if not "db" in conf or not conf["db"]:
        declare_db_config()
    db.initialize(conf["db"])

def terminate():
    global conf
    if not conf: return
    save_conf()
    del conf
    db.terminate()

def save_conf():
    global conf
    if not conf: return
    f = open(configFile, "w")
    json.dump(conf, f)
    f.close()

conf = None