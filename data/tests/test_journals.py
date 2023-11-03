from datetime import datetime
import data.journals as jrnls

FORMAT = "%Y-%m-%d %H:%M:%S"

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
        assert isinstance(datetime.strptime(key, FORMAT), datetime)
        journal = journals[key]
        assert isinstance(journal, dict)
        assert jrnls.TITLE in journal
        assert jrnls.CONTENT in journal
        j_title = journal[jrnls.TITLE]
        assert isinstance(j_title, str)
        j_content = journal[jrnls.CONTENT]
        assert isinstance(j_content, str)


ADD_TIMESTAMP = '2000-01-01 09:57:00'
ADD_TITLE = 'SOME TITLE'
ADD_CONTENT = 'blah blah blah'


"""
    Ensure:
        - After adding a sample journal entry, 
          it is in the list of journals
"""
def test_add_journal():
    jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_CONTENT)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {jrnls.TITLE: ADD_TITLE, jrnls.CONTENT: ADD_CONTENT}


def test_add_journal_without_title_or_content():
    jrnls.add_journal(ADD_TIMESTAMP, "", "")
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {jrnls.TITLE: jrnls.DEFAULT_TITLE, jrnls.CONTENT: ""}


def test_add_journal_without_content():
    jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, "")
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {jrnls.TITLE: ADD_TITLE, jrnls.CONTENT: ""}


def test_add_journal_without_title():
    jrnls.add_journal(ADD_TIMESTAMP, "", ADD_CONTENT)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {jrnls.TITLE: jrnls.DEFAULT_TITLE, jrnls.CONTENT: ADD_CONTENT}

