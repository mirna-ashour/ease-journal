"""
This module interfaces to our user data.
"""

import data.db_connect as dbc
import random
from datetime import datetime


USERS_COLLECT = 'users'
USER_ID = 'user_id'
FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
DOB = 'dob'
EMAIL = 'email'

FORMAT = "%Y-%m-%d"

USER_ID_LEN = 10
USER_BIG_NUM = 1000000000


MIN_USER_NAME_LEN = 2

# users = {
#     1234567890: {
#         FIRST_NAME: "Emma",
#         LAST_NAME: "Watson",
#         DOB: "2002-11-20",
#         EMAIL: "emma.watson@gmail.com"
#     },
# }


def _get_user_id():
    _id = random.randint(0, USER_BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(USER_ID_LEN, '0')
    return _id


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USER_ID, USERS_COLLECT)


def add_user(user_id: str, first_name: str, last_name: str,
             dob: str, email: str):
    if exists(user_id):
        raise ValueError("Duplicate user.")
    dob = datetime.strptime(dob, FORMAT).strftime(FORMAT)
    user_entry = {}
    user_entry[USER_ID] = user_id
    user_entry[FIRST_NAME] = first_name
    user_entry[LAST_NAME] = last_name
    user_entry[DOB] = dob
    user_entry[EMAIL] = email
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user_entry)
    return _id is not None


def exists(user_id: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USER_ID: user_id})


def del_user(user_id: str):
    if exists(user_id):
        return dbc.del_one(USERS_COLLECT, {USER_ID: user_id})
    else:
        raise ValueError(f'Delete failure: {user_id} not in database.')


def get_user(user_id: str):
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USER_ID: user_id})
