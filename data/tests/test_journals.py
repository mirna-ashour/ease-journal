import pytest
import data.journals as jrnls

from datetime import datetime


FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope='function')
def temp_journal():
    timestamp = jrnls._get_test_timestamp()
    prompt = f"UniquePrompt_{timestamp}"
    ret = jrnls.add_journal(timestamp, "", prompt, "This is a fixture", timestamp)
    yield timestamp
    if jrnls.exists(timestamp):
        jrnls.del_journal(timestamp)


def test_get_test_journal():
    timestamp = jrnls._get_test_timestamp()
    assert isinstance(timestamp, str)
    assert isinstance(datetime.strptime(key, FORMAT), datetime)


def test_gen_id():
    _id = jrnls._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == jrnls.ID_LEN


def test_get_test_journal():
    assert isinstance(jrnls.get_test_journal(), dict)


"""
    Ensure:
        - get_journals() returns a dict with at least 1 journal
        - each journal key is a valid timestamp (str)
        - each journal is a dict with the following members:
            - TITLE (str)
            - PROMPT (str)
            - CONTENT (str)
            - MODIFIED (str/valid timestamp)
"""
def test_get_journals(temp_journal):
    journals = jrnls.get_journals()
    assert isinstance(journals, dict)
    assert len(journals) > 0

    for key in journals:
        assert isinstance(key, str)
        assert isinstance(journals[key], dict)
    assert jrnls.exists(temp_journal)


ADD_TIMESTAMP = '2000-01-01 09:57:00'
ADD_TITLE = 'SOME TITLE'
ADD_PROMPT0 = 'some prompt0'
ADD_PROMPT1 = 'some prompt1'
ADD_CONTENT = 'blah blah blah'
ADD_MODIFIED = ADD_TIMESTAMP

NON_STRING = 123


"""
    Ensure:
        - After adding a sample journal entry, it is 
          in the list of journals with valid input
"""
def test_add_journal():
    jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_PROMPT0, ADD_CONTENT, ADD_MODIFIED)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP][jrnls.TITLE] == ADD_TITLE
    assert journals[ADD_TIMESTAMP][jrnls.PROMPT] == ADD_PROMPT0
    assert journals[ADD_TIMESTAMP][jrnls.CONTENT] == ADD_CONTENT
    assert journals[ADD_TIMESTAMP][jrnls.MODIFIED] == ADD_MODIFIED


def test_add_journal_without_title_or_content():
    jrnls.add_journal(ADD_TIMESTAMP, "", ADD_PROMPT1, "", ADD_MODIFIED)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP][jrnls.TITLE] == jrnls.DEFAULT_TITLE
    assert journals[ADD_TIMESTAMP][jrnls.PROMPT] == ADD_PROMPT1
    assert journals[ADD_TIMESTAMP][jrnls.CONTENT] == ""
    assert journals[ADD_TIMESTAMP][jrnls.MODIFIED] == ADD_MODIFIED


def test_add_journal_dup_prompt(temp_journal):
    temp_journal_entry = jrnls.get_journal(temp_journal)
    temp_prompt = temp_journal_entry[jrnls.PROMPT]
    with pytest.raises(ValueError):
        jrnls.add_journal(ADD_TIMESTAMP, "", temp_prompt, "", ADD_MODIFIED)


def test_add_journal_invalid_timestamp():
    with pytest.raises(ValueError):
        jrnls.add_journal("invalid timestamp", ADD_TITLE, ADD_PROMPT1, ADD_CONTENT, ADD_MODIFIED)


def test_add_journal_prompt_too_long():
    long_prompt = "x" * 500  # Assuming there's a limit to prompt length
    with pytest.raises(ValueError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, long_prompt, ADD_CONTENT, ADD_MODIFIED)


def test_add_journal_non_string_title():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, NON_STRING, ADD_PROMPT1, ADD_CONTENT, ADD_MODIFIED)


def test_add_journal_non_string_prompt():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, NON_STRING, ADD_CONTENT, ADD_MODIFIED)


def test_add_journal_non_string_content():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_PROMPT1, NON_STRING, ADD_MODIFIED)


def test_del_journal(temp_journal):
    timestamp = temp_journal
    jrnls.del_journal(timestamp)
    assert not jrnls.exists(timestamp)


def test_del_journal_not_there():
    timestamp = jrnls._get_test_timestamp()
    with pytest.raises(ValueError):
        jrnls.del_journal(timestamp)