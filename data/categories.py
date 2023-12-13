from datetime import datetime

"""
This module interfaces to our categories data.
"""

import data.db_connect as dbc
import random

FORMAT = "%Y-%m-%d %H:%M:%S"
CATEGORIES_COLLECT = 'categories'
CATEGORY_ID = 'category_id'
TITLE = 'title'
USER = 'user'
DATE_TIME = 'created'

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
def add_category(category_id: str, title: str, user_id: str, date_time: str):
    if exists(category_id):
        raise ValueError("Duplicate category.")
    if not title:
        title = "Untitled"
    date_time = str(datetime.strptime(date_time, FORMAT))
    category_entry = {}
    category_entry[CATEGORY_ID] = category_id
    category_entry[TITLE] = title
    category_entry[USER] = user_id
    category_entry[DATE_TIME] = date_time
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
