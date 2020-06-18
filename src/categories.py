import json
import sys
from collections import namedtuple
from typing import List, Optional, Tuple

import requests
import databaseHandler as db
from common import *

Category = namedtuple("Category", ("id", "name", "url"))
urlCategories = "https://{lang}.openfoodfacts.org/categories.json"


class Categories:

    tableName: str = "categories"
    IDAPI2ID: dict = {}

    def display(
        self, tableNameProducts: str, min: int, max: int, orderBy: str = "name"
    ) -> List:
        out = []
        query = (
            "SELECT id_api, name, url FROM categories"
            # f" ORDER BY {orderBy}"
            f" LIMIT %(min)s, %(max)s"
        )
        args = {"min": min - 1, "max": max}
        ok, res = db.handler.executeQuery(query, args)
        if ok:
            for i, row in enumerate(res[1], min + 1):
                out.append(Category(row[0], row[1], row[2]))
            return out
        else:
            raise RuntimeError(res[-1])

    def getAllCategories(self, args: dict = {}, fields: str = "id, id_API"):
        query = f"SELECT {fields} FROM categories"
        ok, res = db.handler.executeQuery(query, args)
        if not ok:
            raise RuntimeError(res)
        return res

    def _initializeCategoriesIDS(self):
        """
        Creates a dictionary that contains all categories. `id_api: id`.
        """
        res = self.getAllCategories()
        self.IDAPI2ID = {e[1]: e[0] for e in res[1]}

    def getCategoryID(self, id_API: str) -> Tuple[bool, int]:
        """Returns the value of the id field associated to the category.
        @param id_API: the ID provided by the API
        @return: a tuple of:
            a bool that indicates if an ID is available
            an integer that represents the ID or an error message
        """
        if not self.IDAPI2ID:
            self._initializeCategoriesIDS()
        if id_API in self.IDAPI2ID.keys():
            return True, self.IDAPI2ID[id_API]
        else:
            return False, ERR_UNKNOWN_ID_API

    def retrieveFromAPI(
        self, lang: str = "fr", minProducts: int = 10, page: int = 0, limit: int = 0
    ) -> List:
        """Retrieves all categories from the API.
        @param lang: the language for the API
        @param minProducts: the minimum number of products required in the category to keep it in local.
        @raise RuntimeError: if no category is available
        """
        res = []
        req = requests.get(urlCategories.format(lang=lang))
        json_ = req.json()
        if not "tags" in json_:
            raise RuntimeError("No tag available")
        res += self.processJSON(req.json())
        return res

    def processJSON(self, json_: dict) -> List:
        out = []
        for tag in json_["tags"]:
            out.append(Category(tag["id"], tag["name"], tag["url"]))
        return out

    def writeInDB(self, categories: List[Category]):
        updatedEntriesNumber = 0
        addedEntriesNumber = 0
        for category in categories:
            query = (
                "INSERT INTO `categories`"
                "(id_api, name, url)"
                "VALUES (%(id)s, %(name)s, %(url)s)"
            )
            args = {"id": category.id, "name": category.name, "url": category.url}
            ok, res = db.handler.executeQuery(query, args, False)
            if not ok:
                if res[0] == db.errorcode.ER_DUP_ENTRY:
                    query = (
                        "UPDATE `categories`"
                        "SET name = %(name)s, url = %(url)s"
                        "WHERE id_api = %(id)s"
                    )
                    ok, res = db.handler.executeQuery(query, args, False)
                    if not ok:
                        raise RuntimeError(res)
                    updatedEntriesNumber += 1
                else:
                    raise RuntimeError((res, args))
            else:
                addedEntriesNumber += 1
        db.handler.commit()
        return addedEntriesNumber, updatedEntriesNumber

    def terminate(self):
        """Frees ressources"""
        if self.IDAPI2ID:
            self.IDAPI2ID = dict()


#: The singleton Categories handler instance.
handler: Optional[Categories] = None


def initialize():
    global handler
    handler = Categories()


def terminate():
    global handler
    if handler:
        handler.terminate()
        handler = None


if __name__ == "__main__":
    categories = Categories()
    res = categories.retrieveFromAPI()
    writeInFile(res, "out_categories.txt")
    print("Done")
