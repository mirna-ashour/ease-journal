import data.users as usrs
import pytest


"""
    Ensure:
        - get_users() returns a dict with at least 1 user
        - each user key, or ID, is an int
        - each user is a dict with a name member
        - each user name is an alphabetical str with at least two letters
"""


def test_get_users():
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for key in users:
        assert isinstance(key, int)
        user = users[key]
        assert isinstance(user, dict)
        # first name
        assert usrs.FIRST_NAME in user
        user_first_name = user[usrs.FIRST_NAME]
        assert isinstance(user_first_name, str)
        assert user_first_name.isalpha()
        assert len(user_first_name) >= usrs.MIN_USER_NAME_LEN
        # last name
        assert usrs.LAST_NAME in user
        user_last_name = user[usrs.LAST_NAME]
        assert isinstance(user_last_name, str)
        assert user_last_name.isalpha()
        assert len(user_last_name) >= usrs.MIN_USER_NAME_LEN
        # dob
        user_dob = user[usrs.DOB]
        assert isinstance(user_dob, str)
        # email
        user_email = user[usrs.EMAIL]
        assert isinstance(user_email, str)


def test_add_user():
    user_id = 1902837465
    first_name = "Emma"
    last_name = "Watson"
    dob = "2002-11-20"
    email = "emma.watson@gmail.com"
    usrs.add_user(user_id, first_name, last_name, dob, email)
    # check
    users = usrs.get_users()
    assert user_id in users
    assert users[user_id][usrs.FIRST_NAME] == first_name
    assert users[user_id][usrs.LAST_NAME] == last_name
    assert users[user_id][usrs.DOB] == dob
    assert users[user_id][usrs.EMAIL] == email
