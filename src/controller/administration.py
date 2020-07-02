import models.administration as model


def create_database():
    return model.create_database()


def get_database_struct():
    return model.get_struct_database()


def drop_database():
    model.drop_database()


def update_categories():
    return model.update_categories()


def update_products(nb_pages):
    model.update_products()
