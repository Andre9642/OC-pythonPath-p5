import sys
from typing import Optional, List, Set
import mysql.connector
from mysql.connector import errorcode

struct_database = {
    "Create database": "CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8'",
    "Select database": "USE {db_name}",
    "Create table 'categories'": (
        "CREATE TABLE IF NOT EXISTS `categories` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,\n"
        "`id_api` varchar(512) UNIQUE NOT NULL,\n"
        "`name` varchar(512) NOT NULL,\n"
        "`url` varchar(1024) NOT NULL,\n"
        "`products` int(11) NOT NULL,\n"
        "PRIMARY KEY (id)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ),
    "Create table 'products_categories'": (
        "CREATE TABLE IF NOT EXISTS `products_categories` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,\n"
        "`id_category` int(11) NOT NULL,\n"
        "`id_product` int(11) NOT NULL,\n"
        "PRIMARY KEY (id),\n"
        "UNIQUE(id_category, id_product)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
    ),
    "Create table 'products'": (
        "CREATE TABLE IF NOT EXISTS `products` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,\n"
        "`id_api` varchar(100) UNIQUE NOT NULL,\n"
        "`name` varchar(100) NOT NULL,\n"
        "`brands` varchar(100) NOT NULL,\n"
        "`nutriscore_grade` varchar(1),\n"
        "`fat` varchar(20),\n"
        "`saturated_fat` varchar(20),\n"
        "`sugars` varchar(20),\n"
        "`salt` varchar(20),\n"
        "`stores` varchar(150),\n"
        "`url` varchar(1024) NOT NULL,\n"
        "`ingredients_text` text,\n"
        "`quantity` varchar(20),\n"
        "`code` varchar(20),\n"
        "PRIMARY KEY (id)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
    )
}

class DatabaseHandler:

    _db_infos = None
    cnx = None
    last_row_id = 0

    def __init__(
        self,
        db_infos,
        select_database=True,
    ):
        user = db_infos.get("user")
        password = db_infos.get("password")
        host = db_infos.get("host")
        port = db_infos.get("port")
        if isinstance(port, str) and port and port.isnumeric:
            port = int(port)
        database = db_infos.get("db_name") or db_infos.get("database")
        if not database:
            raise ValueError("Database name is missing")
        if not user:
            raise ValueError("user name is missing")
        if not port or not isinstance(port, int):
            port = 3306
        self._db_infos = {
            "user": user,
            "password": password,
            "port": port,
            "database": database,
        }
        if select_database:
            try:
                self.cnx = mysql.connector.connect(**self._db_infos)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    raise RuntimeError("Wrong user name or password")
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    self.connect_without_select_database()
                    self.create_database()
                    self.cnx = mysql.connector.connect(**self._db_infos)
                else:
                    raise RuntimeError(err)
        else:
            self.connect_without_select_database()

    def connect_without_select_database(self):
        self.cnx = mysql.connector.connect(
            **{k: v for k, v in self._db_infos.items() if k != "database"}
        )

    def create_database(self):
        db_name = self._db_infos.get("database")
        if not db_name:
            raise ValueError("No database name")
        cursor = self.cnx.cursor()
        for description, sql in struct_database.items():
            print(f"- {description}", end="...")
            try:
                cursor.execute(sql.format(db_name=db_name))
                print("OK")
            except mysql.connector.Error as err:
                print("KO")
                print(err)
                sys.exit(1)
        self.cnx.database = self._db_infos.get("database")

    def execute_query(self, query, args=None, fetchall=True):
        if not self.cnx:
            return False, "Database not set"
        cursor = self.cnx.cursor()
        try:
            cursor.execute(query, args)
            self.last_row_id = cursor.lastrowid
            if fetchall:
                records = cursor.fetchall()
                return True, (cursor.rowcount, records)
            else:
                return True, None
        except mysql.connector.Error as err:
            return False, (err.errno, err)

    def commit(self):
        return self.cnx.commit()

    def drop_database(self):
        db_name = self._db_infos["database"]
        query = f"DROP DATABASE {db_name}"
        cursor = self.cnx.cursor()
        print("Drop database", end="... ")
        try:
            cursor.execute(query)
            print("OK")
        except mysql.connector.Error as err:
            print("KO")
            if err.errno == errorcode.ER_DB_DROP_EXISTS:
                print(f"! Database {db_name} doesn't exist")
            else:
                print(f"! {err}")

    def get_table_entries(self, table_name, min, max):
        query = f"SELECT * FROM {table_name} LIMIT %(min)s, %(max)s"
        args = {"table_name": table_name, "min": min - 1, "max": max}
        res = self.execute_query(query, args)
        return res

    def terminate(self):
        if self.cnx:
            self.cnx.close()


def getConfig():
    if not handler:
        return None
    return handler._db_infos


def initialize(db_infos):
    global handler
    handler = DatabaseHandler(db_infos)


def terminate():
    global handler
    if handler:
        handler.terminate()
        handler = None


#: The singleton DatabaseHandler instance.
handler: Optional[DatabaseHandler] = None
