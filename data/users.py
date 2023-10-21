"""
This module interfaces to our user data.
"""

NAME = 'name'
MIN_USER_NAME_LEN = 2


def get_users():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of users keyed on user ID (an int).
        - Each user ID must be the key for a dictionary.
        - That dictionary must at least include:
            - a NAME member (a str)
    """
    users = {
        1234567890: {
            NAME: "Emma",
        },
        9876543210: {
            NAME: "Liam",
        },
    }
    return users
