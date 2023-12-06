import data.users as usrs
import pytest
import random
from datetime import datetime

FORMAT = "%Y-%m-%d"

"""
    Ensure:
        - get_users() returns a dict with at least 1 user
        - each user key, or ID, is an int
        - each user is a dict with a name member
        - each user name is an alphabetical str with at least two letters
"""


@pytest.fixture(scope='function')
def temp_user():
    user_id = usrs._get_user_id()
    ret = usrs.add_user(user_id, "John", "smith", "2002-11-20", "testemail@gmail.com")
    yield user_id
    if usrs.exists(user_id):
        usrs.del_user(user_id)


def test_get_user_id():
    _id = usrs._get_user_id()
    assert isinstance(_id, str)
    assert len(_id) == usrs.USER_ID_LEN


def test_get_test_user():
    assert isinstance(usrs.get_test_user(), dict)


def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    for key in users:
        assert isinstance(key, str)

        user = users[key]
        assert isinstance(user, dict)
        assert usrs.FIRST_NAME in user
        assert usrs.LAST_NAME in user
        assert usrs.DOB in user
        assert usrs.EMAIL in user

        assert isinstance(user[usrs.FIRST_NAME], str)
        assert isinstance(user[usrs.LAST_NAME], str)
        assert isinstance(user[usrs.EMAIL], str)
        assert isinstance(datetime.strptime(user[usrs.DOB], FORMAT), datetime)
        
    assert usrs.exists(temp_user)


def test_add_user():
    user_id = usrs._get_user_id()
    ret = usrs.add_user(user_id, "John", "smith", "2002-11-20", "testemail@gmail.com")
    assert usrs.exists(user_id)
    assert isinstance(ret, bool)
    usrs.del_user(user_id)


def test_add_duplicate_user(temp_user):
    user_id = temp_user
        
    # attempting to add user again
    with pytest.raises(ValueError):
        usrs.add_user(user_id, "John", "smith", "2002-11-20", "testemail@gmail.com")


def test_del_user(temp_user):
    user_id = temp_user
    usrs.del_user(user_id)
    assert not usrs.exists(user_id)


def test_del_user_not_there():
    user_id = usrs._get_user_id()
    with pytest.raises(ValueError):
        usrs.del_user(user_id)