import json
import sys
from collections import namedtuple
from typing import List, Optional, Tuple

import requests
from . import database as db
from common import *

category = namedtuple("category", ("id", "name", "url"))
url_categories = "https://{lang}.openfoodfacts.org/Categories.json"


class Categories:

    tableName: str = "Categories"
    idapi2_id: dict = {}

    def display(
        self, table_name_products: str, min: int, max: int, orderBy: str = "name"
    ) -> List:
        out = []
        query = (
            "SELECT id_api, name, url FROM Categories"
            # f" ORDER BY {orderBy}"
            f" LIMIT %(min)s, %(max)s"
        )
        args = {"min": min - 1, "max": max}
        ok, res = db.handler.executeQuery(query, args)
        if ok:
            for i, row in enumerate(res[1], min + 1):
                out.append(category(row[0], row[1], row[2]))
            return out
        else:
            raise RuntimeError(res[-1])

    def get_all_categories(self, args: dict = {}, fields: str = "id, id_API"):
        query = f"SELECT {fields} FROM Categories"
        ok, res = db.handler.executeQuery(query, args)
        if not ok:
            raise RuntimeError(res)
        return res

    def _initialize_categories_ids(self):
        """
        Creates a dictionary that contains all Categories. `id_api: id`.
        """
        res = self.get_all_categories()
        self.idapi2_id = {e[1]: e[0] for e in res[1]}

    def get_category_id(self, id_api: str) -> Tuple[bool, int]:
        """Returns the value of the id field associated to the category.
        @param id_api: the ID provided by the API
        @return: a tuple of:
            a bool that indicates if an ID is available
            an integer that represents the ID or an error message
        """
        if not self.idapi2_id:
            self._initialize_categories_ids()
        if id_api in self.idapi2_id.keys():
            return True, self.idapi2_id[id_api]
        else:
            return False, ERR_UNKNOWN_ID_API

    def retrieve_from_api(
        self, lang: str = "fr", minProducts: int = 10, page: int = 0, limit: int = 0
    ) -> List:
        """Retrieves all Categories from the API.
        @param lang: the language for the API
        @param minProducts: the minimum number of products required in the category to keep it in local.
        @raise RuntimeError: if no category is available
        """
        res = []
        req = requests.get(url_categories.format(lang=lang))
        json_ = req.json()
        if not "tags" in json_:
            raise RuntimeError("No tag available")
        res += self.processJSON(req.json())
        return res

    def process_json(self, json_: dict) -> List:
        out = []
        for tag in json_["tags"]:
            out.append(category(tag["id"], tag["name"], tag["url"]))
        return out

    def write_in_db(self, categories: List[category]):
        updated_entries_number = 0
        added_entries_number = 0
        for category in categories:
            query = (
                "INSERT INTO `categories`"
                "(id_api, name, url)"
                "VALUES (%(id)s, %(name)s, %(url)s)"
            )
            args = {"id": category.id,
                    "name": category.name, "url": category.url}
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
                    updated_entries_number += 1
                else:
                    raise RuntimeError((res, args))
            else:
                added_entries_number += 1
        db.handler.commit()
        return added_entries_number, updated_entries_number

    def terminate(self):
        """Frees ressources"""
        if self.idapi2_id:
            self.idapi2_id = dict()


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
    Categories = Categories()
    res = Categories.retrieve_from_api()
    write_in_file(res, "out_categories.txt")
    print("Done")
