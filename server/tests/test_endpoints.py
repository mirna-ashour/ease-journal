import server.endpoints as ep
import pytest
import data.categories as categories
import data.users as usrs
import data.journals as jrnls
from unittest.mock import patch
from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_EP)
    print(f'{resp=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.HELLO_RESP in resp_json


def test_list_users():
    resp = TEST_CLIENT.get(ep.USERS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


@patch('data.users.add_user', return_value=usrs.MOCK_ID, autospec=True)
def test_users_add(mock_add):
    """
    Testing we do the right thing with a good return from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user())
    assert resp.status_code == OK


@patch('data.users.add_user', side_effect=ValueError(), autospec=True)
def test_users_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.users.add_user', return_value=None)
def test_users_add_db_failure(mock_add):
    """
    Testing we do the right thing with a null ID return from add_user.
    """
    resp = TEST_CLIENT.post(ep.USERS_EP, json=usrs.get_test_user()) 
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.users.update_user', return_value=True, autospec=True)
def test_update_user_success(mock_update):
    """
    Testing successful update of a user's information.
    """
    user_id = "test_user_id"
    resp = TEST_CLIENT.put(f'{ep.USERS_EP}/{user_id}', json=usrs.get_test_user())
    assert resp.status_code == OK


@patch('data.users.update_user', return_value=False, autospec=True)
def test_update_user_not_found(mock_update):
    """
    Testing update of a user's information when user is not found.
    """
    user_id = "nonexistent_user_id"
    resp = TEST_CLIENT.put(f'{ep.USERS_EP}/{user_id}', json=usrs.get_test_user())
    assert resp.status_code == NOT_FOUND


@patch('data.users.del_user', autospec=True)
def test_users_del(mock_del):
    """
    Testing we do the right thing with a call to del_user that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/user_id')
    assert resp.status_code == OK


@patch('data.users.del_user', side_effect=ValueError(), autospec=True)
def test_users_bad_del(mock_del):
    """
    Testing we do the right thing with a value error from del_user.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_USER_EP}/user_id')
    assert resp.status_code == NOT_FOUND


@patch('data.users.get_user', return_value=usrs.get_test_user(), autospec=True)
def test_get_user_by_id_success(mock_get_user):
    """
    Testing successful retrieval of a user by ID.
    """
    USER_ID = mock_get_user.return_value[usrs.USER_ID]
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{USER_ID}')
    assert resp.status_code == OK


@patch('data.users.get_user', return_value=usrs.get_test_user(), autospec=True)
def test_get_user_by_email_success(mock_get_user):
    """
    Testing successful retrieval of a user by email.
    """
    EMAIL = mock_get_user.return_value[usrs.EMAIL]
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{EMAIL}')
    assert resp.status_code == OK


@patch('data.users.get_user', return_value=None, autospec=True)
def test_get_user_not_found(mock_get_user):
    """
    Testing retrieval of a user that does not exist.
    """
    nonexistent_user_id = usrs._get_user_id()
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/{nonexistent_user_id}')
    assert resp.status_code == NOT_FOUND


@patch('data.users.get_user', side_effect=ValueError(), autospec=True)
def test_get_user_invalid_identifier(mock_get_user):
    """
    Testing retrieval of a user with an invalid identifier.
    """
    resp = TEST_CLIENT.get(f'{ep.USERS_EP}/invalid_identifier')
    assert resp.status_code == BAD_REQUEST


def test_main_menu():
    resp = TEST_CLIENT.get(ep.MAIN_MENU)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert 'Default' in resp_json
    assert 'Choices' in resp_json
    assert '1' in resp_json['Choices']
    assert '2' in resp_json['Choices']
    assert '3' in resp_json['Choices']
    assert '4' in resp_json['Choices']
    assert 'X' in resp_json['Choices']


@patch('data.categories.get_user_categories', return_value='categories_list', autospec=True)
def test_get_user_categories_success(mock_get_user_categories):
    USER_ID = "1234567890"
    resp = TEST_CLIENT.get(f'/categories/{USER_ID}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


@patch('data.categories.get_user_categories', return_value=None, autospec=True)
def test_get_user_categories_not_found(mock_get_user_categories):
    USER_ID = "1234567890"
    resp = TEST_CLIENT.get(f'/categories/{USER_ID}')
    # assert resp.status_code == NOT_ACCEPTABLE
    assert resp.status_code == OK


def test_list_categories():
    resp = TEST_CLIENT.get(ep.CATEGORIES_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


@patch('data.categories.add_category', return_value=categories.MOCK_ID, autospec=True)
@patch('data.users.exists', return_value=True)  # Mocking usrs.exists to always return True
def test_categories_add(mock_add, mock_exists):
    """
    Testing we do the right thing with a good return from add_category.
    """
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categories.get_test_category())
    assert resp.status_code == OK


@patch('data.categories.add_category', side_effect=ValueError(), autospec=True)
def test_categories_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_category.
    """
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categories.get_test_category())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.categories.add_category', return_value=None)
@patch('data.users.exists', return_value=True)  # Mocking usrs.exists to always return True
def test_categories_add_db_failure(mock_add, mock_exists):
    """
    Testing we do the right thing with a null ID return from add_category.
    """
    resp = TEST_CLIENT.post(ep.CATEGORIES_EP, json=categories.get_test_category()) 
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.categories.update_category', return_value=True, autospec=True)
def test_update_category_success(mock_update):
    """
    Testing successful update of a category's details.
    """
    category_id = "test_category_id"
    resp = TEST_CLIENT.put(f'{ep.CATEGORIES_EP}/{category_id}', json=categories.get_test_category())
    assert resp.status_code == OK


@patch('data.categories.update_category', return_value=False, autospec=True)
def test_update_category_not_found(mock_update):
    """
    Testing update of a category's details when category is not found.
    """
    category_id = "nonexistent_category_id"
    resp = TEST_CLIENT.put(f'{ep.CATEGORIES_EP}/{category_id}', json=categories.get_test_category())
    assert resp.status_code == NOT_FOUND


@patch('data.categories.del_category', autospec=True)
def test_categories_del(mock_del):
    """
    Testing we do the right thing with a call to del_category that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_CATEGORY_EP}/category_id')
    assert resp.status_code == OK


@patch('data.categories.del_category', side_effect=ValueError(), autospec=True)
def test_categories_bad_del(mock_del):
    """
    Testing we do the right thing with a value error from del_category.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_CATEGORY_EP}/category_id')
    assert resp.status_code == NOT_FOUND


@pytest.mark.skip('This test is failing, but it is just an example of using '
                   + 'skip')
def test_that_doesnt_work():
    assert False


def test_list_journals():
    resp = TEST_CLIENT.get(ep.JOURNALS_EP)
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json

@patch('data.journals.get_category_journals', return_value='journals_list', autospec=True)
def test_get_category_journals_success(mock_get_category_journals):
    CATEGORY_ID= "12345678"
    resp = TEST_CLIENT.get(f'{ep.JOURNALS_EP}/{CATEGORY_ID}')
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert isinstance(resp_json, dict)
    assert ep.TITLE in resp_json
    assert ep.TYPE in resp_json
    assert ep.DATA in resp_json


@patch('data.journals.get_category_journals', return_value=None, autospec=True)
def test_get_category_journals_not_found(mock_get_category_journals):
    CATEGORY_ID= "12345678"
    resp = TEST_CLIENT.get(f'{ep.JOURNALS_EP}/{CATEGORY_ID}')
    # assert resp.status_code == NOT_ACCEPTABLE
    assert resp.status_code == OK


@patch('data.journals.add_journal', return_value=jrnls.MOCK_ID, autospec=True)
@patch('data.users.exists', return_value=True)  # Mocking usrs.exists to always return True
@patch('data.categories.exists', return_value=True)  # Mocking categories.exists to always return True
def test_journals_add(mock_add, mock_user_exists, mock_category_exists):
    """
    Testing we do the right thing with a good return from add_journal.
    """
    resp = TEST_CLIENT.post(ep.JOURNALS_EP, json=jrnls.get_test_journal())
    assert resp.status_code == OK


@patch('data.journals.add_journal', side_effect=ValueError(), autospec=True)
def test_journals_bad_add(mock_add):
    """
    Testing we do the right thing with a value error from add_journal.
    """
    resp = TEST_CLIENT.post(ep.JOURNALS_EP, json=jrnls.get_test_journal())
    assert resp.status_code == NOT_ACCEPTABLE


@patch('data.journals.add_journal', return_value=None)
@patch('data.users.exists', return_value=True)  # Mocking usrs.exists to always return True
@patch('data.categories.exists', return_value=True)  # Mocking categories.exists to always return True
def test_journals_add_db_failure(mock_add, mock_user_exists, mock_category_exists):
    """
    Testing we do the right thing with a null ID return from add_journal.
    """
    resp = TEST_CLIENT.post(ep.JOURNALS_EP, json=jrnls.get_test_journal())
    assert resp.status_code == SERVICE_UNAVAILABLE


@patch('data.journals.del_journal', autospec=True)
def test_journals_del(mock_del):
    """
    Testing we do the right thing with a call to del_journal that succeeds.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_JOURNAL_EP}/journal_id')
    assert resp.status_code == OK


@patch('data.journals.del_journal', side_effect=ValueError(), autospec=True)
def test_journals_bad_del(mock_del):
    """
    Testing we do the right thing with a value error from del_journal.
    """
    resp = TEST_CLIENT.delete(f'{ep.DEL_JOURNAL_EP}/journal_id')
    assert resp.status_code == NOT_FOUND


@patch('data.journals.update_journal', return_value=True, autospec=True)
def test_update_journal_success(mock_update):
    """
    Testing successful update of a Journal's details.
    """
    journal_id = "test_journal_id"
    resp = TEST_CLIENT.put(f'{ep.JOURNALS_EP}/{journal_id}', json=jrnls.get_test_journal())
    assert resp.status_code == OK


@patch('data.journals.update_journal', return_value=False, autospec=True)
def test_update_journal_not_found(mock_update):
    """
    Testing update of a journal's details when journal is not found.
    """
    journal_id = "nonexistent_journal_id"
    resp = TEST_CLIENT.put(f'{ep.JOURNALS_EP}/{journal_id}', json=jrnls.get_test_journal())
    assert resp.status_code == NOT_FOUND


def test_get_signup_form():
    signup_url = '/signup/form'
    resp = TEST_CLIENT.get(signup_url)
    resp_json = resp.get_json()
    assert ep.SIGNUP_FORM in resp_json
    assert isinstance(resp_json, dict)