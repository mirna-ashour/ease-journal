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
PASSWORD = 'password'

FORMAT = "%Y-%m-%d"

USER_ID_LEN = 10
USER_BIG_NUM = 1000000000

MOCK_ID = '0' * USER_ID_LEN

MIN_USER_NAME_LEN = 2

MIN_USER_EMAIL_LEN = 8
MIN_USER_PSWD_LEN = 8

# users = {
#     1234567890: {
#         FIRST_NAME: "Emma",
#         LAST_NAME: "Watson",
#         DOB: "2002-11-20",
#         EMAIL: "emma.watson@gmail.com"
#         PASSWORD: Password1
#     },
# }


def _get_user_id():
    _id = random.randint(0, USER_BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(USER_ID_LEN, '0')
    return _id


def get_test_user():
    test_user = {}
    test_user[USER_ID] = _get_user_id()
    test_user[FIRST_NAME] = "Emma"
    test_user[LAST_NAME] = "Watson"
    test_user[DOB] = "2002-11-20"
    test_user[EMAIL] = "test@gmail.com"
    test_user[PASSWORD] = "Password1"
    return test_user


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USER_ID, USERS_COLLECT)


def add_user(user_id: str, first_name: str, last_name: str,
             dob: str, email: str, password: str):

    if exists(user_id):
        raise ValueError("Duplicate user.")

    if len(user_id) != USER_ID_LEN:
        raise ValueError(f'User id must be {USER_ID_LEN} characters.')

    if len(first_name) < MIN_USER_NAME_LEN:
        raise ValueError(f'First name must be at least '
                         f'{MIN_USER_NAME_LEN} characters.')

    if len(last_name) < MIN_USER_NAME_LEN:
        raise ValueError(f'Last name must be at least '
                         f'{MIN_USER_NAME_LEN} characters.')

    if email.find('@') == -1:
        raise ValueError('Invalid email address. '
                         'Missing domain (@) in email address.')

    if email.find('.') == -1:
        raise ValueError('Invalid email address. '
                         'Missing dot (.) in email address.')

    if email.find('@') > email.find('.'):
        raise ValueError('Invalid email address. '
                         'Incorrect order of domain and dot in email address.')

    if len(email) < MIN_USER_EMAIL_LEN:
        raise ValueError(f'Email must be at least '
                         f'{MIN_USER_EMAIL_LEN} characters.')

    if len(password) < MIN_USER_PSWD_LEN:
        raise ValueError('Password must be at least 8 characters long.')

    if not any(char.isdigit() for char in password):
        raise ValueError('Password must contain at least one digit.')

    dob = datetime.strptime(dob, FORMAT).strftime(FORMAT)
    user_entry = {}
    user_entry[USER_ID] = user_id
    user_entry[FIRST_NAME] = first_name
    user_entry[LAST_NAME] = last_name
    user_entry[DOB] = dob
    user_entry[EMAIL] = email
    user_entry[PASSWORD] = password
    dbc.connect_db()
    _id = dbc.insert_one(USERS_COLLECT, user_entry)
    return _id is not None


def get_user(user_id: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USER_ID: user_id})


def exists(user_id: str) -> bool:
    return get_user(user_id) is not None


def del_user(user_id: str):
    if exists(user_id):
        return dbc.del_one(USERS_COLLECT, {USER_ID: user_id})
    else:
        raise ValueError(f'Delete failure: {user_id} not in database.')


def get_first_name(user: dict):
    return user.get(FIRST_NAME)


def get_last_name(user: dict):
    return user.get(LAST_NAME)


def get_dob(user: dict):
    return user.get(DOB)


def get_email(user: dict):
    return user.get(EMAIL)


def get_password(user: dict):
    return user.get(PASSWORD)


def update_user(user_id: str, user_data: dict) -> bool:
    """
    Updates a user's information.

    Args:
    user_id (str): The ID of the user to update.
    user_data (dict): Dictionary containing user data to update.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    if not exists(user_id):
        raise ValueError(f"Update failure: {user_id} not in database.")

    if not user_data:
        raise ValueError("Update failure: No valid fields to update.")

    update_data = {}
    for key in [FIRST_NAME, LAST_NAME, DOB, EMAIL, PASSWORD]:
        if key in user_data:
            update_data[key] = user_data[key]

    dbc.connect_db()
    dbc.update_doc(USERS_COLLECT, {USER_ID: user_id}, update_data)
    return True
