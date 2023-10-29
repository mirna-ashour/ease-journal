from datetime import datetime
import data.categories as cats

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


"""
    Ensure:
    	- After adding a sample journal entry, 
    	  it is in the list of journals
"""
def test_add_category():
    cat_id = 2753837783
    title = "Health"
    user = 826393752
    date_time = "2023-04-12 01:16:00"
    cats.add_category(cat_id, title, user, date_time)
    assert cat_id in cats.get_categories()


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
        assert isinstance(category[cats.DATE_TIME], datetime)

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
        assert isinstance(category[cats.DATE_TIME], datetime)

    print("All tests for get_user_categories passed!")
