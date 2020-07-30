"""products module"""
from collections import namedtuple
from typing import List
import models.products as model


Product = namedtuple("product", ("id",
                                 "name",
                                 "brands",
                                 "nutriscore_grade",
                                 "fat",
                                 "saturated_fat",
                                 "sugars",
                                 "salt",
                                 "stores",
                                 "url",
                                 "ingredients_text",
                                 "quantity",
                                 "code",
                                 "categories_tags"))


def get_product_substitutes(terms: str, id_category: str):
    """
    Retrieve substitutes of a product

    Args:
        terms (str):
        id_category (str): the category in
        id_product (str):
    """
    res = model.get_product_substitutes(terms, id_category)
    products = process_json(res)
    return {"count": int(res["count"]),
            "page_size": int(res["page_size"]),
            "page": res["page"],
            "products": products}


def get_products_from_category(id_category: str, page: int = 1):
    """
    Return products from a category

    Args:
        id_category (str): the ID category
        page=1 (int): the page to retrieve
    """
    if page < 1:
        page = 1
    res = model.get_products_from_category(id_category)
    products = process_json(res)
    return {"count": int(res["count"]),
            "page_size": int(res["page_size"]),
            "page": res["page"],
            "products": products}


def process_json(json_: dict) -> List:
    """
    Convert products JSON to Products objects

    Args:
        json_ (dict): the JSON to convert

    Returns:
        List

    """
    out = []
    for product in json_["products"]:
        if ("categories_tags" not in product.keys()
            or "id" not in product.keys()
            or not all([product["id"], product["product_name"], product["url"]])):
            continue
        product = Product(product["id"],
                          product["product_name"],
                          product.get("brands", ""),
                          product.get("nutriscore_grade"),
                          product["nutriments"].get("fat"),
                          product["nutriments"].get("saturated-fat"),
                          product["nutriments"].get("sugars"),
                          product["nutriments"].get("salt"),
                          product.get("stores"),
                          product.get("url"),
                          product.get("ingredients_text"),
                          product.get("quantity"),
                          product.get("code"),
                          product.get("categories_tags"))
        out.append(product)
    return out


def save_products(products: Product):
    """
    Save several product

    Args:
        products (Product): the product list
    """
    return model.save_products_db(products)


def save_product(product: Product):
    """
    Save a product

    Args:
        product (Product): the product to save
    """
    return model.save_product_db(product)
