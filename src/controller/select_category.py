import models.categories as model
from collections import namedtuple

Category = namedtuple("category", ("id", "name", "url"))


def get_total_number():
    return model.get_total_number()


def get_categories(start, nb_items):
    if nb_items < 1 or start < 0:
        return []
    res = model.get_categories(start, nb_items, "id, name, id_api")
    categories = []
    for category in res[1]:
        categories.append(Category(
            id=category[0], name=category[1], url=category[2]
        ))
    return categories
