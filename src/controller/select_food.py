import models.products as model
from collections import namedtuple


product = namedtuple(
    "product",
    (
        "id",
        "name",
        "brands",
        "nutrition_grade",
        "fat",
        "saturated_fat",
        "sugars",
        "salt",
        "stores",
        "url",
        "categories_tags",
    ),
)

def get_products_from_category(id_category):
    return []
