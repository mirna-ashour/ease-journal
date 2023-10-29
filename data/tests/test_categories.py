from datetime import datetime
import data.categories as cats

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

        assert isinstance(cats.TITLE, str)
        assert isinstance(cats.USER, int)
        assert isinstance(cats.DATE_TIME, datetime)