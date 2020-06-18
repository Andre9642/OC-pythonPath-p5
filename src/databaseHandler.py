import sys
from typing import Optional, List, Set
import mysql.connector
from mysql.connector import errorcode

USER_NAME = "root"
PASSWORD = ""
HOST_NAME = "127.0.0.1"
DB_NAME = "purBeurre"

structDatabase = {
    "Create database": f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'",
    "Select database": f"USE {DB_NAME}",
    "Create table 'categories'": (
        "CREATE TABLE IF NOT EXISTS `categories` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`id_api` varchar(512) UNIQUE NOT NULL,"
        "`name` varchar(512) NOT NULL,"
        "`url` varchar(1024) NOT NULL,"
        "PRIMARY KEY (id)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ).strip(),
    "Create table 'products_categories'": (
        "CREATE TABLE IF NOT EXISTS `products_categories` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`id_category` int(11) NOT NULL,"
        "`id_product` int(11) NOT NULL,"
        "PRIMARY KEY (id),"
        "UNIQUE(id_category, id_product)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
    ),
    "Create table 'products'": (
        "CREATE TABLE IF NOT EXISTS `products` ("
        "`id` int(11) NOT NULL AUTO_INCREMENT,"
        "`id_api` varchar(100) UNIQUE NOT NULL,"
        "`name` varchar(100) NOT NULL,"
        "`brands` varchar(100) NOT NULL,"
        "`nutrition_grade` varchar(1),"
        "`fat` float NOT NULL,"
        "`saturated_fat` float NOT NULL,"
        "`sugars` float NOT NULL,"
        "`salt` float NOT NULL,"
        "`stores` varchar(150),"
        "`url` varchar(1024) NOT NULL,"
        "PRIMARY KEY (id)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8"
    ).strip(),
}
structDatabase["Create table 'substitute_products'"] = structDatabase[
    "Create table 'products'"
].replace("`products`", "`substitute_products`")


class DatabaseHandler:

    cnx = None
    database = None
    lastrowid = 0

    def __init__(
        self,
        user=USER_NAME,
        password=PASSWORD,
        host=HOST_NAME,
        database=DB_NAME,
        selectDatabase=True,
    ):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        if selectDatabase:
            try:
                self.cnx = mysql.connector.connect(
                    user=user, password=password, host=host, database=database
                )
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                    print("Wrong user name or password")
                    self.terminate()
                    sys.exit(1)
                elif err.errno == errorcode.ER_BAD_DB_ERROR:
                    print(f"Database '{database}' doesn't exist.")
                else:
                    print(err)
                    self.terminate()
                    sys.exit(1)
        else:
            self.connectWithoutSelectDatabase()

    def connectWithoutSelectDatabase(self):
        self.cnx = mysql.connector.connect(
            user=self.user, password=self.password, host=self.host
        )

    def createDatabase(self):
        cursor = self.cnx.cursor()
        for description, sql in structDatabase.items():
            print(f"- {description}", end="... ")
            try:
                cursor.execute(sql)
                print("OK")
            except mysql.connector.Error as err:
                print("KO")
                print(err)
                sys.exit(1)
        self.cnx.database = DB_NAME

    def executeQuery(self, query, args=None, fetchall=True):
        if not self.cnx:
            return False, "Database not set"
        cursor = self.cnx.cursor()
        try:
            cursor.execute(query, args)
            self.lastrowid = cursor.lastrowid
            if fetchall:
                records = cursor.fetchall()
                return True, (cursor.rowcount, records)
            else:
                return True, None
        except mysql.connector.Error as err:
            return False, (err.errno, err)

    def commit(self):
        return self.cnx.commit()

    def dropDatabase(self):
        DB_NAME = self.database
        query = f"DROP DATABASE {DB_NAME}"
        cursor = self.cnx.cursor()
        print("Drop database", end="... ")
        try:
            cursor.execute(query)
            print("OK")
        except mysql.connector.Error as err:
            print("KO")
            if err.errno == errorcode.ER_DB_DROP_EXISTS:
                print(f"! Database {DB_NAME} doesn't exist")
            else:
                print(f"! {err}")

    def getTableEntries(self, tableName, min, max):
        query = f"SELECT * FROM {tableName} LIMIT %(min)s, %(max)s"
        args = {"tableName": tableName, "min": min - 1, "max": max}
        res = self.executeQuery(query, args)
        return res

    def terminate(self):
        if self.cnx:
            self.cnx.close()


def getStructDatabase(self):
    for description, sql in structDatabase.items():
        print((sql if sql.endswith(";") else sql + ";").strip().replace("\t\t", "\t"))


#: The singleton DatabaseHandler instance.
handler: Optional[DatabaseHandler] = None


def initialize():
    global handler
    handler = DatabaseHandler()


def terminate():
    global handler
    if handler:
        handler.terminate()
        handler = None
