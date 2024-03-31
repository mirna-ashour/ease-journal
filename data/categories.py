"""
This module interfaces to our categories data.
"""

# import data.users as usrs
import data.db_connect as dbc
import random

from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"
CATEGORIES_COLLECT = 'categories'
CATEGORY_ID = 'category_id'
TITLE = 'title'
USER = 'user'
DATE_TIME = 'created'
JOURNALS = 'Journals'

categories = {}

CATEGORY_ID_LEN = 8
USER_ID_LEN = 10
CATEGORY_BIG_NUM = 10000000
USER_BIG_NUM = 1000000000
BIG_NUM = 100_000_000_000_000_000_000

MOCK_ID = '0' * CATEGORY_ID_LEN

# categories = [
#     {
#         CATEGORY_ID:  75638475,
#         TITLE: "Work",
#         USER: 1234567890,
#         DATE_TIME: "2023-10-27 12:45:00"
#     },
#     {
#         CATEGORY_ID: 384762549,
#         TITLE: "School",
#         USER: 9876543210,
#         DATE_TIME: "2023-10-27 18:15:00"
#     }
# ]


def _get_category_id():
    _id = random.randint(0, CATEGORY_BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(CATEGORY_ID_LEN, '0')
    return _id


def get_test_category():
    test_category = {}
    test_category[CATEGORY_ID] = _get_category_id()
    test_category[TITLE] = "untitled"
    test_category[USER] = "1234567890"
    test_category[DATE_TIME] = "2002-11-20 12:00:00"
    test_category[JOURNALS] = {}
    return test_category


def _get_user_id():
    _id = random.randint(0, USER_BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(USER_ID_LEN, '0')
    return _id


def _get_title_name():
    name = 'test'
    rand_part = random.randint(0, BIG_NUM)
    return name + str(rand_part)


# return all categories
def get_categories() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(CATEGORY_ID, CATEGORIES_COLLECT)


# return categories with a specific user_id - Cody updated in 10/29
def get_user_categories(user_id: str) -> dict:
    dbc.connect_db()
    all_categories = dbc.fetch_all_as_dict(CATEGORY_ID, CATEGORIES_COLLECT)
    user_specific_categories = {}
    for category_id, category in all_categories.items():
        if category[USER] == user_id:
            user_specific_categories[category_id] = category
    return user_specific_categories


# category ids are currently a parameter but should later be uniquely generated
def add_category(category_id: str, title: str, user_id: str):
    if exists(category_id):
        raise ValueError("Duplicate category.")
    if not title:
        raise ValueError("Please input a title.")

    lowercase_title = title.lower()

    # Check for duplicate title
    existing_category = dbc.fetch_one(CATEGORIES_COLLECT,
                                      {TITLE:
                                       {'$regex': f'^{lowercase_title}$',
                                        '$options': 'i'}})
    if existing_category:
        raise ValueError("Duplicate title.")

    # The commented check below is done in the POST endpoint for Category class
    # if not usrs.exists(user_id):
    #     raise wz.NotAcceptable("Please input a user ID that exists.")

    date_time = datetime.now().strftime(FORMAT)
    category_entry = {}
    category_entry[CATEGORY_ID] = category_id
    category_entry[TITLE] = title
    category_entry[USER] = user_id
    category_entry[DATE_TIME] = date_time
    category_entry[JOURNALS] = {}
    dbc.connect_db()
    _id = dbc.insert_one(CATEGORIES_COLLECT, category_entry)
    return _id is not None


def exists(category_id: str) -> bool:
    return get_category(category_id) is not None


def del_category(category_id: str):
    if exists(category_id):
        return dbc.del_one(CATEGORIES_COLLECT, {CATEGORY_ID: category_id})
    else:
        raise ValueError(f'Delete failure: {category_id} not in database.')


def get_category(category_id: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(CATEGORIES_COLLECT, {CATEGORY_ID: category_id})


def get_title(category: dict):
    return category.get(TITLE)


def get_user(category: dict):
    return category.get(USER)


def get_journals(category: dict):
    return category.get(JOURNALS)


def update_category(category_id: str, category_data: dict) -> bool:
    """
    Updates a category's information.

    Args:
    category_id (str): The ID of the category to update.
    category_data (dict): Dictionary containing category data to update.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    if not exists(category_id):
        raise ValueError(f"Update failure: {category_id} not in database.")

    if not category_data:
        raise ValueError("Update failure: No valid fields to update.")

    update_data = {}
    for key in [TITLE, JOURNALS]:
        if key in category_data:
            if key == TITLE and (len(category_data[key]) != 0):
                update_data[key] = category_data[key]
            elif key == JOURNALS:  # Journals dictionary can be empty
                update_data[key] = category_data[key]

    dbc.connect_db()
    dbc.update_doc(CATEGORIES_COLLECT, {CATEGORY_ID: category_id}, update_data)
    return True
