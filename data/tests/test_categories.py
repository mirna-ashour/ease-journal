from datetime import datetime
import random
import data.categories as cats
import data.journals as jrnls
import data.users as usrs
import pytest
from datetime import datetime


FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope='module')
def temp_user():
    """
    Fixture to create a temporary user for testing purposes.
    Adds a user to the database and deletes it after the test module completes.
    """
    user_id = usrs._get_user_id()
    ret = usrs.add_user(user_id, "John", "Smith", "2002-11-20", "testemail@gmail.com", "Password1")
    yield user_id
    if usrs.exists(user_id):
        usrs.del_user(user_id)


@pytest.fixture(scope='function')
def temp_category(temp_user):
    """
    Fixture to create a temporary category for testing purposes.
    Adds a category to the database associated with a temporary user,
    and deletes it after each test function that uses this fixture completes.
    """
    category_id = cats._get_category_id()
    user_id = temp_user
    category_name = cats._get_category_name()
    ret = cats.add_category(category_id, category_name, user_id)
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
    assert cats.CATEGORY_NAME in category
    assert cats.USER in category
    assert cats.DATE_TIME in category
    assert cats.JOURNALS in category


def test_get_test_category():
    assert isinstance(cats.get_test_category(), dict)


def test_get_user_categories(temp_user):
    user_id = temp_user

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


def test_get_category_name():
    name = cats._get_category_name()
    assert isinstance(name, str)


def test_get_category_name(temp_category):
    category = cats.get_category(temp_category)
    assert cats.get_category_name(category) == category[cats.CATEGORY_NAME]


def test_get_journals(temp_category):
    category = cats.get_category(temp_category)
    assert cats.get_journals(category) == category[cats.JOURNALS]


def test_get_categories(temp_category):
    categories = cats.get_categories()
    assert isinstance(categories, dict)
    assert len(categories) > 0
    for key in categories:
        assert isinstance(key, str)

        category = categories[key]
        assert isinstance(category, dict)
        assert cats.CATEGORY_NAME in category
        assert cats.USER in category
        assert cats.DATE_TIME in category
        assert cats.JOURNALS in category

        assert isinstance(category[cats.CATEGORY_NAME], str)
        assert isinstance(category[cats.USER], str)
        date_time = str(category[cats.DATE_TIME])
        assert isinstance(datetime.strptime(date_time, FORMAT), datetime)
        assert isinstance(category[cats.JOURNALS], dict)

    assert cats.exists(temp_category)


def test_add_category(temp_user):
    category_id = cats._get_category_id()
    category_name = cats._get_category_name()
    user_id = temp_user
    ret = cats.add_category(category_id, category_name, user_id)
    assert cats.exists(category_id)
    assert isinstance(ret, bool)
    cats.del_category(category_id)


def test_add_category_without_category_name(temp_user):
    category_id = cats._get_category_id()
    category_name = ""
    user_id = temp_user

    # attempting to add category without a category_name 
    with pytest.raises(ValueError):
        cats.add_category(category_id, category_name, user_id)


def test_add_dup_category_id(temp_category):
    cat_id = temp_category
    user = cats.get_user(cats.get_category(cat_id))
    category_name = cats._get_category_name()
        
    # attempting to add category again
    with pytest.raises(ValueError):
        cats.add_category(cat_id, category_name, user)


def test_add_dup_category_name(temp_category):
    existing_category = cats.get_category(temp_category)
    existing_category_name = cats.get_category_name(existing_category)
    user = cats.get_user(existing_category)

    # Ensure that the category category_name is not empty
    assert existing_category_name is not None

    # Attempt to add a new category with the same category_name
    with pytest.raises(ValueError):
        cats.add_category(cats._get_category_id(), existing_category_name, user)
       
       
def test_del_category(temp_category):
    category_id = temp_category
    cats.del_category(category_id)
    assert not cats.exists(category_id)


def test_del_category_not_there():
    category_id = cats._get_category_id()
    with pytest.raises(ValueError):
        cats.del_category(category_id)      


UPDATED_CATEGORY_NAME = "Updated category_name"


def test_update_category(temp_category):
    category_id = temp_category
    update_data = {cats.CATEGORY_NAME: UPDATED_CATEGORY_NAME}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_category_name(updated_category) == UPDATED_CATEGORY_NAME


def test_update_category_name(temp_category):
    category_id = temp_category
    prev_category = cats.get_category(category_id)
    prev_journals = cats.get_journals(prev_category)
    
    update_data = {cats.CATEGORY_NAME: UPDATED_CATEGORY_NAME}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_category_name(updated_category) == UPDATED_CATEGORY_NAME
    assert cats.get_journals(updated_category) == prev_journals


def test_update_category_name_zero_length(temp_category):
    category_id = temp_category
    prev_category = cats.get_category(category_id)
    prev_category_name = cats.get_category_name(prev_category)
    prev_journals = cats.get_journals(prev_category)

    update_data = {cats.CATEGORY_NAME: ""}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_category_name(updated_category) == prev_category_name
    assert cats.get_journals(updated_category) == prev_journals


def test_update_category_journals(temp_category):
    category_id = temp_category
    prev_category = cats.get_category(category_id)
    prev_category_name = cats.get_category_name(prev_category)
    prev_journals = cats.get_journals(prev_category)

    journal_id = jrnls._get_journal_id()
    new_journal = jrnls.add_journal(journal_id, "", "", "", 
        cats.get_user(prev_category), category_id)
    journal_update_data = {jrnls.TITLE: UPDATED_CATEGORY_NAME}
    assert jrnls.update_journal(journal_id, journal_update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_category_name(updated_category) == prev_category_name
    assert cats.get_journals(updated_category) != prev_journals
    assert cats.get_journals(updated_category) == {journal_id: UPDATED_CATEGORY_NAME}


def test_update_category_invalid_key(temp_category):
    category_id = temp_category
    prev_category = cats.get_category(category_id)
    prev_category_name = cats.get_category_name(prev_category)
    prev_journals = cats.get_journals(prev_category)
    
    update_data = {"INVALID": "KEY"}
    assert cats.update_category(category_id, update_data)

    updated_category = cats.get_category(category_id)
    assert cats.get_category_name(updated_category) == prev_category_name
    assert cats.get_journals(updated_category) == prev_journals


def test_update_category_nonexistent_category():
    category_id = cats._get_category_id()
    update_data = {cats.CATEGORY_NAME: UPDATED_CATEGORY_NAME}
    with pytest.raises(ValueError):
        cats.update_category(category_id, update_data)


def test_update_category_nothing_to_update(temp_category):
    category_id = temp_category
    update_data = {}
    with pytest.raises(ValueError):
        cats.update_category(category_id, update_data)
