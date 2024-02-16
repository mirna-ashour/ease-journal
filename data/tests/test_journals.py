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


def test_get_test_timestamp():
    timestamp = jrnls._get_test_timestamp()
    assert isinstance(timestamp, str)
    assert isinstance(datetime.strptime(timestamp, FORMAT), datetime)


def test_gen_id():
    _id = jrnls._gen_id()
    assert isinstance(_id, str)
    assert len(_id) == jrnls.ID_LEN


def test_get_test_journal():
    assert isinstance(jrnls.get_test_journal(), dict)


def test_get_journal(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    
    assert journal is not None
    assert isinstance(journal, dict)

    assert jrnls.TIMESTAMP in journal
    assert jrnls.TITLE in journal
    assert jrnls.PROMPT in journal
    assert jrnls.CONTENT in journal
    assert jrnls.MODIFIED in journal


def test_get_title(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_title(journal) == journal[jrnls.TITLE]


def test_get_content(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_content(journal) == journal[jrnls.CONTENT]


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
        assert isinstance(datetime.strptime(key, FORMAT), datetime)

        journal = journals[key]
        assert isinstance(journal, dict)

        assert jrnls.TIMESTAMP in journal
        assert jrnls.TITLE in journal
        assert jrnls.PROMPT in journal
        assert jrnls.CONTENT in journal
        assert jrnls.MODIFIED in journal

        assert journal[jrnls.TIMESTAMP] == key

        assert isinstance(journal[jrnls.TITLE], str)
        assert isinstance(journal[jrnls.PROMPT] ,str)
        assert isinstance(journal[jrnls.CONTENT] ,str)
        assert isinstance(journal[jrnls.MODIFIED] ,str)

        assert datetime.strptime(key, FORMAT) <= datetime.strptime(journal[jrnls.MODIFIED], FORMAT)
        
    assert jrnls.exists(temp_journal)


ADD_TIMESTAMP = '2000-01-01 09:57:00'
ADD_TITLE = 'Added title'
ADD_PROMPT0 = 'Added prompt0'
ADD_PROMPT1 = 'Added prompt1'
ADD_CONTENT = 'Added content'
ADD_MODIFIED = ADD_TIMESTAMP

INVALID_TIMESTAMP = "invalid timestamp"
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
    jrnls.del_journal(ADD_TIMESTAMP)


def test_add_journal_without_title_or_content():
    jrnls.add_journal(ADD_TIMESTAMP, "", ADD_PROMPT1, "", ADD_MODIFIED)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP][jrnls.TITLE] == jrnls.DEFAULT_TITLE
    assert journals[ADD_TIMESTAMP][jrnls.PROMPT] == ADD_PROMPT1
    assert journals[ADD_TIMESTAMP][jrnls.CONTENT] == ""
    assert journals[ADD_TIMESTAMP][jrnls.MODIFIED] == ADD_MODIFIED
    jrnls.del_journal(ADD_TIMESTAMP)


def test_add_journal_dup_prompt(temp_journal):
    temp_journal_entry = jrnls.get_journal(temp_journal)
    temp_prompt = temp_journal_entry[jrnls.PROMPT]
    with pytest.raises(ValueError):
        jrnls.add_journal(ADD_TIMESTAMP, "", temp_prompt, "", ADD_MODIFIED)


def test_add_journal_invalid_timestamp():
    with pytest.raises(ValueError):
        jrnls.add_journal(INVALID_TIMESTAMP, ADD_TITLE, ADD_PROMPT1, ADD_CONTENT, ADD_MODIFIED)


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


UPDATED_TITLE = "Updated Title"
UPDATED_PROMPT = "Updated Prompt"
UPDATED_CONTENT = "Updated Content"


def test_update_journal(temp_journal):
    timestamp = temp_journal
    prev_modified = jrnls.get_journal(timestamp)[jrnls.MODIFIED]

    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    assert jrnls.update_journal(timestamp, update_data)

    updated_journal = jrnls.get_journal(timestamp)
    assert updated_journal[jrnls.TITLE] == UPDATED_TITLE
    assert updated_journal[jrnls.PROMPT] == UPDATED_PROMPT
    assert updated_journal[jrnls.CONTENT] == UPDATED_CONTENT
    assert updated_journal[jrnls.MODIFIED] > prev_modified


def test_update_journal_partially(temp_journal):
    timestamp = temp_journal
    prev_prompt = jrnls.get_journal(timestamp)[jrnls.PROMPT]
    prev_content = jrnls.get_journal(timestamp)[jrnls.CONTENT]
    prev_modified = jrnls.get_journal(timestamp)[jrnls.MODIFIED]

    update_data = {jrnls.TITLE: UPDATED_TITLE}
    assert jrnls.update_journal(timestamp, update_data)

    updated_journal = jrnls.get_journal(timestamp)
    assert updated_journal[jrnls.TITLE] == UPDATED_TITLE
    assert updated_journal[jrnls.PROMPT] == prev_prompt
    assert updated_journal[jrnls.CONTENT] == prev_content
    assert updated_journal[jrnls.MODIFIED] > prev_modified


def test_update_journal_invalid_timestamp():
    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    with pytest.raises(TypeError):
        jrnls.update_journal(INVALID_TIMESTAMP, update_data)


def test_update_journal_nonexistent_timestamp():
    timestamp = jrnls._get_test_timestamp()
    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    with pytest.raises(ValueError):
        jrnls.update_journal(timestamp, update_data)


def test_update_journal_nothing_to_update(temp_journal):
    timestamp = temp_journal
    update_data = {}
    with pytest.raises(ValueError):
        jrnls.update_journal(timestamp, update_data)
