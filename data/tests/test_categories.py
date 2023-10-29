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

        assert isinstance(category[cats.TITLE], str)
        assert isinstance(category[cats.USER], int)
        format = "%Y-%m-%d %H:%M:%S"
        date_time = category[cats.DATE_TIME]
        assert isinstance(datetime.strptime(date_time, format), datetime)


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