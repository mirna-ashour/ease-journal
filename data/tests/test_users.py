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


def test_get_user(temp_user):
    user = usrs.get_user(temp_user)

    assert user is not None
    assert isinstance(user, dict)

    assert usrs.USER_ID in user
    assert usrs.FIRST_NAME in user
    assert usrs.LAST_NAME in user
    assert usrs.DOB in user
    assert usrs.EMAIL in user

    assert isinstance(datetime.strptime(user[usrs.DOB], FORMAT), datetime)


def test_get_first_name(temp_user):
    user = usrs.get_user(temp_user)
    assert usrs.get_first_name(user) == user[usrs.FIRST_NAME]


def test_get_last_name(temp_user):
    user = usrs.get_user(temp_user)
    assert usrs.get_last_name(user) == user[usrs.LAST_NAME]


def test_get_dob(temp_user):
    user = usrs.get_user(temp_user)
    assert usrs.get_dob(user) == user[usrs.DOB]


def test_get_email(temp_user):
    user = usrs.get_user(temp_user)
    assert usrs.get_email(user) == user[usrs.EMAIL]


def test_get_users(temp_user):
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0
    
    for key in users:
        assert isinstance(key, str)

        user = users[key]
        assert isinstance(user, dict)

        assert usrs.USER_ID in user
        assert usrs.FIRST_NAME in user
        assert usrs.LAST_NAME in user
        assert usrs.DOB in user
        assert usrs.EMAIL in user

        assert user[usrs.USER_ID] == key

        assert isinstance(usrs.get_first_name(user), str)
        assert isinstance(usrs.get_last_name(user), str)
        assert isinstance(usrs.get_email(user), str)
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


def test_add_user_invalid_id_length():
    with pytest.raises(ValueError):
        usrs.add_user("short_id", "John", "smith", "2002-11-20", "testemail@gmail.com")


def test_add_user_short_first_name():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "J", "Smith", "2002-11-20", "testemail@gmail.com")


def test_add_user_short_last_name():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "John", "S", "2002-11-20", "testemail@gmail.com")


def test_add_user_missing_at_in_email():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "John", "Smith", "2002-11-20", "testemailgmail.com")


def test_add_user_missing_dot_in_email():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "John", "Smith", "2002-11-20", "testemail@gmailcom")


def test_add_user_incorrect_order_of_domain_and_dot_in_email():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "John", "Smith", "2002-11-20", "testemail.gmail@com")


def test_add_user_short_email():
    with pytest.raises(ValueError):
        usrs.add_user(usrs._get_user_id(), "John", "Smith", "2002-11-20", "a@b.com")


def test_del_user(temp_user):
    user_id = temp_user
    usrs.del_user(user_id)
    assert not usrs.exists(user_id)


def test_del_user_not_there():
    user_id = usrs._get_user_id()
    with pytest.raises(ValueError):
        usrs.del_user(user_id)


UPDATED_FIRST_NAME = "James"
UPDATED_LAST_NAME = "Johnson"
UPDATED_DOB = "1980-02-16"
UPDATED_EMAIL = "johnsonJames@gmail.com"


def test_update_user(temp_user):
    user_id = temp_user
    update_data = {usrs.FIRST_NAME: UPDATED_FIRST_NAME, usrs.LAST_NAME: UPDATED_LAST_NAME, usrs.DOB: UPDATED_DOB, usrs.EMAIL: UPDATED_EMAIL}
    assert usrs.update_user(user_id, update_data)

    updated_user = usrs.get_user(user_id)
    assert usrs.get_first_name(updated_user) == UPDATED_FIRST_NAME
    assert usrs.get_last_name(updated_user) == UPDATED_LAST_NAME
    assert usrs.get_dob(updated_user) == UPDATED_DOB
    assert usrs.get_email(updated_user) == UPDATED_EMAIL


def test_update_user_partially(temp_user):
    user_id = temp_user
    prev_user = usrs.get_user(user_id)
    prev_last_name = usrs.get_last_name(prev_user)
    prev_dob = usrs.get_dob(prev_user)
    prev_email = usrs.get_email(prev_user)

    update_data = {usrs.FIRST_NAME: UPDATED_FIRST_NAME}
    assert usrs.update_user(user_id, update_data)

    updated_user = usrs.get_user(user_id)
    assert usrs.get_first_name(updated_user) == UPDATED_FIRST_NAME
    assert usrs.get_last_name(updated_user) == prev_last_name
    assert usrs.get_dob(updated_user) == prev_dob
    assert usrs.get_email(updated_user) == prev_email


def test_update_user_nonexistent_user():
    user_id = usrs._get_user_id()
    update_data = {usrs.FIRST_NAME: UPDATED_FIRST_NAME, usrs.LAST_NAME: UPDATED_LAST_NAME, usrs.DOB: UPDATED_DOB, usrs.EMAIL: UPDATED_EMAIL}
    with pytest.raises(ValueError):
        usrs.update_user(user_id, update_data)


def test_update_user_nothing_to_update(temp_user):
    user_id = temp_user
    update_data = {}
    with pytest.raises(ValueError):
        usrs.update_user(user_id, update_data)
