import json
import sys
from typing import List, Optional, Tuple

import requests
from . import database as db
from common import *


url_categories = "https://{lang}.openfoodfacts.org/categories.json"
url_categories_page = "https://{lang}.openfoodfacts.org/categories/{page}.json"


def retrieve_from_api(
    lang: str = "fr", page: int = 0
) -> List:
    """Retrieves all Categories from the API.
    @param lang: the language for the API
    @param minProducts: the minimum number of products required in the category to keep it.
    @raise RuntimeError: if no category is available
    """
    res = []
    if page:
        url = url_categories_page.format(lang=lang, page=page)
    else:
        url = url_categories.format(lang=lang)
    req = requests.get(url)
    if req.status_code != 200:
        raise RuntimeError("Unable to retrieve page")
    return req.json()

def write_in_db(categories: List):
    updated_entries_number = 0
    added_entries_number = 0
    for category in categories:
        query = (
            "INSERT INTO `categories`"
            "(id_api, name, url, products)"
            "VALUES (%(id)s, %(name)s, %(url)s, %(products)s)"
        )
        args = {
            "id": category.id,
            "name": category.name,
            "url": category.url,
            "products": category.products}
        ok, res = db.handler.execute_query(query, args, False)
        if not ok:
            if res[0] == db.errorcode.ER_DUP_ENTRY:
                query = (
                    "UPDATE `categories`"
                    "SET name = %(name)s, url = %(url)s, products = %(products)s\n"
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


def get_categories(start, nb_item, fields='*', order_by=''):
    query = f"SELECT {fields} FROM Categories\n" 
    if order_by: query += f"ORDER BY {order_by}\n"
    query += "LIMIT %(start)s, %(nb_item)s"
    args = {"start": start-1, "nb_item": nb_item}
    ok, res = db.handler.execute_query(query, args)
    if not ok:
        raise RuntimeError(res)
    return res
