import json
import sys
from typing import List, Optional, Tuple

import requests
from . import database as db
from common import *


url_categories = "https://{lang}.openfoodfacts.org/categories.json"


def retrieve_from_api(
    lang: str = "fr", minProducts: int = 10, page: int = 0, limit: int = 0
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
    res += process_json(req.json())
    return res


def process_json(json_: dict) -> List:
    out = []
    for tag in json_["tags"]:
        out.append(category(tag["id"], tag["name"], tag["url"]))
    return out


def write_in_db(categories: List):
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
        ok, res = db.handler.execute_query(query, args, False)
        if not ok:
            if res[0] == db.errorcode.ER_DUP_ENTRY:
                query = (
                    "UPDATE `categories`"
                    "SET name = %(name)s, url = %(url)s"
                    "WHERE id_api = %(id)s"
                )
                ok, res = db.handler.execute_query(query, args, False)
                if not ok:
                    raise RuntimeError(res)
                updated_entries_number += 1
            else:
                raise RuntimeError((res, args))
        else:
            added_entries_number += 1
    db.handler.commit()
    return added_entries_number, updated_entries_number


def get_total_number():
    return db.handler.execute_query("SELECT COUNT(*) as nb FROM categories")


def get_categories(start, nb_item, fields='*'):
    query = (f"SELECT {fields} FROM Categories\n"
             "LIMIT %(start)s, %(nb_item)s")
    args = {"start": start-1, "nb_item": nb_item}
    ok, res = db.handler.execute_query(query, args)
    if not ok:
        raise RuntimeError(res)
    return res
