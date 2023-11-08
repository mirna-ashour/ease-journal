from datetime import datetime
import random
import data.categories as cats
import pytest
from datetime import datetime

FORMAT = "%Y-%m-%d %H:%M:%S"

"""
	Ensure:
		- get_categories() returns a dict with at least 1 journal
		- each category key is a valid int 
		- each category is a dict with keys-values: title, user_id, and timestamp
		- each category title is a str
		- each category user_id is an int
        - each category date_time is a timestamp
"""
def test_get_categories():
    categories = cats.get_categories()
    assert isinstance(categories, dict)
    assert len(categories) > 0
    for key in categories:
        assert isinstance(key, int)

        category = categories[key]
        assert isinstance(category, dict)
        assert cats.TITLE in category
        assert cats.USER in category
        assert cats.DATE_TIME in category

        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], int)
        date_time = category[cats.DATE_TIME]
        assert isinstance(datetime.strptime(date_time, FORMAT), datetime)

@pytest.fixture(scope='function')
def make_category():
    cat_id = random.randint(10**9, (10**10 - 1))
    user = random.randint(10**8, (10**9 - 1))
    current_time = datetime.now().strftime(FORMAT)

    return {
        'cat_id' : cat_id,
        'title' : "Health",
        'user' : user,
        'date_time' : current_time, 
    }


"""
    Ensure:
    	- After adding a category, 
    	  it is in the list of categories
"""
def test_add_category(make_category):
    cat_id, title, user, date_time = make_category.values() 
    cats.add_category(cat_id, title, user, date_time)
    new_cat = cats.get_categories()[cat_id]
    assert cat_id in cats.get_categories()
    assert cats.TITLE in new_cat
    assert cats.USER in new_cat
    assert cats.DATE_TIME in new_cat
    assert isinstance(cat_id, int)
    assert isinstance(title, str)
    assert isinstance(user, int)
    assert isinstance(date_time, str)


def test_add_duplicate_category(make_category):
    cat_id, title, user, date_time = make_category.values()
    
    # adding category for the first time
    cats.add_category(cat_id, title, user, date_time)
    
    # attempting to add category again
    with pytest.raises(ValueError):
        cats.add_category(cat_id, title, user, date_time)


"""
	Cody Updated in 10/29
	Ensure:
		- get_user_categories(user_id) returns a dict of categories associated with a user
		- each category key is a valid int 
		- each category is a dict with keys-values: title, user_id, and timestamp
		- each category title is a str
		- each category user_id is an int and matches the provided user_id
        	- each category date_time is a timestamp
"""
def test_get_user_categories():
    emma_id = 1234567890
    liam_id = 9876543210
    
    # Testing categories for Emma
    emma_categories = cats.get_user_categories(emma_id)
    assert isinstance(emma_categories, dict)

    for key in emma_categories:
        assert isinstance(key, int)

        category = emma_categories[key]
        assert isinstance(category, dict)
        assert cats.TITLE in category
        assert cats.USER in category
        assert cats.DATE_TIME in category

        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], int)
        assert category[cats.USER] == emma_id
        date_time_1 = category[cats.DATE_TIME]
        assert isinstance(datetime.strptime(date_time_1, FORMAT), datetime)

    # Testing categories for Liam
    liam_categories = cats.get_user_categories(liam_id)
    assert isinstance(liam_categories, dict)

    for key in liam_categories:
        assert isinstance(key, int)

        category = liam_categories[key]
        assert isinstance(category, dict)
        assert cats.TITLE in category
        assert cats.USER in category
        assert cats.DATE_TIME in category

        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], int)
        assert category[cats.USER] == liam_id
        date_time_2 = category[cats.DATE_TIME]
        assert isinstance(datetime.strptime(date_time_2, FORMAT), datetime)

    print("All tests for get_user_categories passed!")
