from datetime import datetime
import random
import data.categories as cats
import pytest
from datetime import datetime


FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope='function')
def temp_category():
    category_id = cats._get_category_id()
    user_id = cats._get_user_id()
    title = cats._get_title_name()
    date_time = '2023-10-27 12:45:00'
    ret = cats.add_category(category_id, title, user_id, date_time)
    yield category_id
    if cats.exists(category_id):
        cats.del_category(category_id)


def test_get_category_id():
    _id = cats._get_category_id()
    assert isinstance(_id, str)
    assert len(_id) == cats.CATEGORY_ID_LEN


def test_get_user_id():
    _id = cats._get_user_id()
    assert isinstance(_id, str)
    assert len(_id) == cats.USER_ID_LEN


def test_get_test_category():
    assert isinstance(cats.get_test_category(), dict)


def test_get_title_name():
    name = cats._get_title_name()
    assert isinstance(name, str)


def test_get_categories(temp_category):
    categories = cats.get_categories()
    assert isinstance(categories, dict)
    assert len(categories) > 0
    for key in categories:
        assert isinstance(key, str)

        category = categories[key]
        assert isinstance(category, dict)
        assert cats.TITLE in category
        assert cats.USER in category
        assert cats.DATE_TIME in category

        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], str)
        date_time = str(category[cats.DATE_TIME])
        assert isinstance(datetime.strptime(date_time, FORMAT), datetime)
    
    assert cats.exists(temp_category)


def test_add_category():
    category_id = cats._get_category_id()
    title = cats._get_title_name()
    user_id = cats._get_user_id()
    date_time = '2023-10-27 12:45:00'
    ret = cats.add_category(category_id, title, user_id, date_time)
    assert cats.exists(category_id)
    assert isinstance(ret, bool)
    cats.del_category(category_id)


def test_add_category_without_title():
    category_id = cats._get_category_id()
    title = ""
    user_id = cats._get_user_id()
    date_time = (datetime.now()).strftime(FORMAT)
    ret = cats.add_category(category_id, title, user_id, date_time)
    assert cats.exists(category_id)
    assert isinstance(ret, bool)
    cats.del_category(category_id)


def test_add_duplicate_category(temp_category):
    cat_id = temp_category
    user = cats._get_user_id()
    title = cats._get_title_name()
    date_time = '2023-10-27 12:45:00'
        
    # attempting to add category again
    with pytest.raises(ValueError):
        cats.add_category(cat_id, title, user, date_time)


def test_del_category(temp_category):
    category_id = temp_category
    cats.del_category(category_id)
    assert not cats.exists(category_id)


def test_del_category_not_there():
    category_id = cats._get_category_id()
    with pytest.raises(ValueError):
        cats.del_category(category_id)      
        