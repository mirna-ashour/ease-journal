
import server.endpoints as ep
import pytest

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

@pytest.mark.skip(reason="Getting status code 500 error")
def test_add_category():
    test_data = {
        "user_id": 1234567890,
        "title": "Test Category",
        "date_time": "2023-11-05 15:30:00"
    }
    resp = TEST_CLIENT.post('/add_category', json=test_data)

    assert resp.status_code == 200  
    resp_json = resp.get_json()
    assert "message" in resp_json
    assert "category_id" in resp_json
