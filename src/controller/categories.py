"""categories module"""
from collections import namedtuple
from typing import List
import models.categories as model


Category = namedtuple("category", ("id", "name", "url", "products"))


def get_total_number():
    """Returns the number of category"""
    return model.get_total_number()


def get_categories(start, nb_items, order_by=''):
    """
    Retrieve categories

    Args:
        start (undefined): the first item to retrieve
        nb_items (undefined): the number of items to retrieve
        order_by='' (undefined): to specify an ORDER BY clause
    """
    if nb_items < 1 or start < 1:
        return []
    res = model.get_categories(start,
                               nb_items,
                               "id_api, name, url, products",
                               order_by)
    categories = []
    for category in res[1]:
        category = Category(category[0], category[1], category[2], category[3])
        categories.append(category)
    return categories


def retrieve_from_api():
    """Retrieve all categories from Open Food Facts API"""
    return model.retrieve_from_api()


def process_json(json_: dict) -> List:
    """
    Convert the JSON from API to a list of Category object

    Args:
        json_ (dict): the JSON from the Open Food Fact API

    Returns:
        List

    """
    out = []
    for tag in json_["tags"]:
        out.append(Category(tag["id"], tag["name"],
                            tag["url"], tag["products"]))
    return out


def save_categories(categories: List):
    """
    Save several categories

    Args:
        categories (List): the category list
    """
    return model.save_categories_db(categories)


def save_category(category: Category):
    """
    Save a category

    Args:
        category (Category): the category to save
    """
    return model.save_category_db(category)
