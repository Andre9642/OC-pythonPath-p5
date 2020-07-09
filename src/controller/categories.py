import models.categories as model
from collections import namedtuple
from typing import List

Category = namedtuple("category", ("id", "name", "url", "products"))


def get_total_number():
    return model.get_total_number()


def get_categories(start, nb_items, order_by=''):
    if nb_items < 1 or start < 1:
        return []
    res = model.get_categories(
        start, nb_items, "id_api, name, url, products", order_by)
    categories = []
    for category in res[1]:
        categories.append(Category(
            id=category[0],
            name=category[1],
            url=category[2],
            products=category[3]
        ))
    return categories


def retrieve_from_api():
    return model.retrieve_from_api()


def process_json(json_: dict) -> List:
    out = []
    for tag in json_["tags"]:
        out.append(Category(tag["id"], tag["name"],
                            tag["url"], tag["products"]))
    return out


def write_in_db(*args, **kwargs):
    return model.write_in_db(*args, **kwargs)
