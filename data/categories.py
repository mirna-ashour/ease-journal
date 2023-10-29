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


# return categories with a specific user_id 
def get_user_categories(user_id: int) -> dict:
    pass


# category ids are currently a parameter but should later be uniquely generated 
def add_category(category_id: int, title: str, user_id: int, date_time: str):
    if not title:
        title = "Untitled"
    categories[category_id] = {TITLE: title, USER: user_id, DATE_TIME: datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")}
