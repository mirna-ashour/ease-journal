from datetime import datetime
import data.journals as jrnls


"""
	Ensure:
		- get_journals() returns a dict with at least 1 journal
		- each journal key is a valid timestamp str
		- each journal is a dict with title & content members
		- each journal title is a str
		- each journal entry content is a str
"""
def test_get_journals():
    journals = jrnls.get_journals()
    assert isinstance(journals, dict)
    assert len(journals) > 0
    for key in journals:
        assert isinstance(key, str)
        format = "%Y-%m-%d %H:%M:%S"
        assert isinstance(datetime.strptime(key, format), datetime)
        journal = journals[key]
        assert isinstance(journal, dict)
        assert jrnls.TITLE in journal
        assert jrnls.CONTENT in journal
        j_title = journal[jrnls.TITLE]
        assert isinstance(j_title, str)
        j_content = journal[jrnls.CONTENT]
        assert isinstance(j_content, str)


ADD_TIMESTAMP = '2000-01-01 09:57:00'


"""
    Ensure:
    	- After adding a sample journal entry, 
    	  it is in the list of journals
"""
def test_add_journal():
	jrnls.add_journal(ADD_TIMESTAMP, "", "")
	assert ADD_TIMESTAMP in jrnls.get_journals()