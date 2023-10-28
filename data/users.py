"""
This module interfaces to our user data.
"""

NAME = 'name'
MIN_USER_NAME_LEN = 2

users = {
    1234567890: {
        NAME: "Emma",
    },
    9876543210: {
        NAME: "Liam",
    },
}


def get_users() -> dict:
    return users
