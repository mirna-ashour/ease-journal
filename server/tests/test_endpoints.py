import server.endpoints as ep
import pytest
import data.categories as categories
import data.users as usrs
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


#@pytest.mark.skip(reason="Getting status code 500 error")
@patch('data.categories.add_category', return_value='000000000',autospec=True)
def test_add_category_success(mock_add_category):
    mock_add_category.return_value = 123456
    test_data = {
        "user_id": 1234567890,
        "title": "Test Category",
        "date_time": "2023-11-05 15:30:00"
    }
    resp = TEST_CLIENT.post('/add_category', json=test_data)
    assert resp.status_code == OK

#@pytest.mark.skip(reason="Getting status code 500 error")
@patch('data.categories.add_category', side_effect=ValueError("Duplicate category"), autospec=True)
def test_add_category_failure(mock_add_category):
    test_data = {
        'user_id': 1234567890, 
        'title': 'Test Category',
        'date_time': '2023-11-08 12:00:00'
    }
    resp = TEST_CLIENT.post('/add_category', json=test_data)
    assert resp.status_code == NOT_ACCEPTABLE

@pytest.mark.skip('This test is failing, but it is just an example of using '
                   + 'skip')
def test_that_doesnt_work():
    assert False


def test_add_journal():
    test_data = {
        "timestamp": "2023-11-10 10:00:00",
        "title": "Test Journal",
        "prompt": "Test Prompt",
        "content": "Test Content",
        "modified": "2023-11-10 10:00:00"
    }
    resp = TEST_CLIENT.post('/journal', json=test_data)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert "message" in resp_json
    assert resp_json["message"] == "Journal added successfully"


def test_delete_journal():
    # Ensure this timestamp exists in your test database
    test_data = {"timestamp": "2023-11-10 10:00:00"}
    resp = TEST_CLIENT.delete('/delete_journal', json=test_data)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    assert "message" in resp_json
    assert resp_json["message"] == "Journal deleted successfully"
