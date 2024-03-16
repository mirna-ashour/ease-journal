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
    ret = cats.add_category(category_id, title, user_id)
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


def test_get_category(temp_category):
    category = cats.get_category(temp_category)

    assert category is not None
    assert isinstance(category, dict)
    
    assert cats.CATEGORY_ID in category
    assert cats.TITLE in category
    assert cats.USER in category
    assert cats.DATE_TIME in category
    assert cats.JOURNALS in category


def test_get_test_category():
    assert isinstance(cats.get_test_category(), dict)


def test_get_user_categories(temp_category):
    user_id = cats._get_user_id()

    cat1_id = cats._get_category_id()
    cat2_id = cats._get_category_id()

    cats.add_category(cat1_id, "Category 1", user_id)
    cats.add_category(cat2_id, "Category 2", user_id)

    user_cats = cats.get_user_categories(user_id)

    assert len(user_cats) == 2
    assert cat1_id in user_cats
    assert cat2_id in user_cats

    cats.del_category(cat1_id)
    cats.del_category(cat2_id)


def test_get_title_name():
    name = cats._get_title_name()
    assert isinstance(name, str)


def test_get_title(temp_category):
    category = cats.get_category(temp_category)
    assert cats.get_title(category) == category[cats.TITLE]


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
        assert cats.JOURNALS in category


        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], str)
        date_time = str(category[cats.DATE_TIME])
        assert isinstance(datetime.strptime(date_time, FORMAT), datetime)
        assert isinstance(category[cats.JOURNALS], list)

    
    assert cats.exists(temp_category)


def test_add_category():
    category_id = cats._get_category_id()
    title = cats._get_title_name()
    user_id = cats._get_user_id()
    ret = cats.add_category(category_id, title, user_id)
    assert cats.exists(category_id)
    assert isinstance(ret, bool)
    cats.del_category(category_id)


def test_add_category_without_title():
    category_id = cats._get_category_id()
    title = ""
    user_id = cats._get_user_id()

    # attempting to add category without a title 
    with pytest.raises(ValueError):
        cats.add_category(category_id, title, user_id)


def test_add_dup_category_id(temp_category):
    cat_id = temp_category
    user = cats._get_user_id()
    title = cats._get_title_name()
        
    # attempting to add category again
    with pytest.raises(ValueError):
        cats.add_category(cat_id, title, user)


def test_add_dup_category_title(temp_category):
    category = cats.get_category(temp_category)

    cat_id = cats._get_category_id()
    title = cats.get_title(category)
    user = cats._get_user_id()
    
    with pytest.raises(ValueError):
        cats.add_category(cat_id, title, user)
       
       
def test_del_category(temp_category):
    category_id = temp_category
    cats.del_category(category_id)
    assert not cats.exists(category_id)


def test_del_category_not_there():
    category_id = cats._get_category_id()
    with pytest.raises(ValueError):
        cats.del_category(category_id)      


UPDATED_TITLE = "Updated Title"


def test_update_category(temp_category):
    category_id = temp_category
    update_data = {cats.TITLE: UPDATED_TITLE}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_title(updated_category) == UPDATED_TITLE


# This test must be updated if more category attributes are added
def test_update_category_partially(temp_category):
    category_id = temp_category
    prev_category = cats.get_category(category_id)
    prev_title = cats.get_title(prev_category)

    update_data = {cats.DATE_TIME: "03-01-2024 10:57:00"}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_title(updated_category) == prev_title


def test_update_category_nonexistent_category():
    category_id = cats._get_category_id()
    update_data = {cats.TITLE: UPDATED_TITLE}
    with pytest.raises(ValueError):
        cats.update_category(category_id, update_data)


def test_update_category_nothing_to_update(temp_category):
    category_id = temp_category
    update_data = {}
    with pytest.raises(ValueError):
        cats.update_category(category_id, update_data)
