"""categories module"""
from typing import List

import requests
import models.database as db


URL_CATEGORIES = "https://{lang}.openfoodfacts.org/categories.json"
URL_CATEGORIES_PAGE = "https://{lang}.openfoodfacts.org/categories/{page}.json"


def retrieve_from_api(
    lang: str = "fr", page: int = 0
) -> List:
    """Retrieves all Categories from the API.
    @param lang: the language for the API
    @param minProducts: the minimum number of products required in the category to keep it.
    @raise RuntimeError: if Open Food Facts  API doesn't return a success
    """
    if page:
        url = URL_CATEGORIES_PAGE.format(lang=lang, page=page)
    else:
        url = URL_CATEGORIES.format(lang=lang)
    req = requests.get(url)
    if req.status_code != 200:
        raise RuntimeError(f"Unable to retrieve page. Error {req.status_code}")
    return req.json()


def get_total_number():
    """Return the number of category"""
    return db.handler.execute_query("SELECT COUNT(*) as nb FROM categories")


def get_categories(start: int, nb_item: int, fields: str = '*', order_by: str = ''):
    """
    Retrieve the categories from database

    Args:
        start (int): the first item to retrieve
        nb_item (int): the number of items to retrieve (related to the previous argument)
        fields (str='*'): to specify fields to retrieve
        order_by (str=''): to specify th 'ORDER BY' Clause

    """
    query = f"SELECT {fields} FROM Categories\n"
    if order_by:
        query += f"ORDER BY {order_by}\n"
    query += "LIMIT %(start)s, %(nb_item)s"
    args = {"start": start-1, "nb_item": nb_item}
    success, res = db.handler.execute_query(query, args)
    if not success:
        raise RuntimeError(res)
    return res


def save_categories_db(categories: List):
    """
    Save several categories in database

    Args:
        categories (List): a list of categories to save
    """
    for category in categories:
        save_category_db(category, False)
    db.handler.commit()


def save_category_db(category, commit: bool = True):
    """
    Save a catagory in database

    Args:
        category (Category): the category to save in database
        commit=True (bool): commit or not the current transaction

    """
    query = ("INSERT INTO `categories`\n"
             "(id_api, name, url, products)\n"
             "VALUES (%(id)s, %(name)s, %(url)s, %(products)s)\n"
             "ON DUPLICATE KEY UPDATE\n"
             "name=%(name)s, url=%(url)s, products=%(products)s")
    args = {"id": category.id,
            "name": category.name,
            "url": category.url,
            "products": category.products}
    success, msg = db.handler.execute_query(query, args, False)
    if not success:
        raise RuntimeError(msg)
    if commit:
        db.handler.commit()
