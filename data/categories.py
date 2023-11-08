from datetime import datetime

"""
This module interfaces to our journal data.
"""

TITLE = 'title'
USER = 'user'
DATE_TIME = 'created'

# dict of dicts or a list of dictionaries that include a key for category id
# like below?
categories = {
    75638475: {
        TITLE: "Work",
        USER: 1234567890,
        DATE_TIME: "2023-10-27 12:45:00"
    },
    384762549: {
        TITLE: "School",
        USER: 9876543210,
        DATE_TIME: "2023-10-27 18:15:00"
    }
}

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


# return all categories
def get_categories() -> dict:
    return categories


# return categories with a specific user_id - Cody updated in 10/29
def get_user_categories(user_id: int) -> dict:
    user_specific_categories = {}
    for category_id, category in categories.items():
        if category[USER] == user_id:
            user_specific_categories[category_id] = category
    return user_specific_categories


# category ids are currently a parameter but should later be uniquely generated
def add_category(category_id: int, title: str, user_id: int, date_time: str):
    if category_id in categories:
        raise ValueError("Duplicate category.")
    if not title:
        title = "Untitled"
    date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    categories[category_id] = {
        TITLE: title,
        USER: user_id,
        DATE_TIME: date_time
    }
