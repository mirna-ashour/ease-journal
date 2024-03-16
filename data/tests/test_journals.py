import pytest
import data.journals as jrnls

from datetime import datetime


FORMAT = "%Y-%m-%d %H:%M:%S"


@pytest.fixture(scope='function')
def temp_journal():
    journal_id = jrnls._get_journal_id()
    timestamp = jrnls._get_test_timestamp()
    prompt = f"UniquePrompt_{timestamp}"
    ret  = jrnls.add_journal(journal_id, "", prompt, "This is a journal fixture")
    yield journal_id
    if jrnls.exists(journal_id):
        jrnls.del_journal(journal_id)


def test_get_test_timestamp():
    timestamp = jrnls._get_test_timestamp()
    assert isinstance(timestamp, str)
    assert isinstance(datetime.strptime(timestamp, FORMAT), datetime)


def test_get_journal_id():
    _id = jrnls._get_journal_id()
    assert isinstance(_id, str)
    assert len(_id) == jrnls.ID_LEN


def test_get_test_journal():
    assert isinstance(jrnls.get_test_journal(), dict)


def test_get_journal(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    
    assert journal is not None
    assert isinstance(journal, dict)

    assert jrnls.JOURNAL_ID in journal
    assert jrnls.TIMESTAMP in journal
    assert jrnls.TITLE in journal
    assert jrnls.PROMPT in journal
    assert jrnls.CONTENT in journal
    assert jrnls.MODIFIED in journal


def test_get_title(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_title(journal) == journal[jrnls.TITLE]


def test_get_prompt(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_prompt(journal) == journal[jrnls.PROMPT]


def test_get_content(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_content(journal) == journal[jrnls.CONTENT]


def test_get_modified(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_modified(journal) == journal[jrnls.MODIFIED]


"""
    Ensure:
        - get_journals() returns a dict with at least 1 journal
        - each journal key is a valid journal_id (str)
        - each journal is a dict with the following members:
            - TIMESTAMP (str/valid timestamp)
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

        journal = journals[key]
        assert isinstance(journal, dict)

        assert jrnls.JOURNAL_ID in journal
        assert jrnls.TIMESTAMP in journal
        assert jrnls.TITLE in journal
        assert jrnls.PROMPT in journal
        assert jrnls.CONTENT in journal
        assert jrnls.MODIFIED in journal

        assert journal[jrnls.JOURNAL_ID] == key

        assert isinstance(jrnls.get_timestamp(journal), str)
        assert isinstance(jrnls.get_title(journal), str)
        assert isinstance(jrnls.get_prompt(journal), str)
        assert isinstance(jrnls.get_content(journal), str)
        assert isinstance(jrnls.get_modified(journal), str)

        assert isinstance(datetime.strptime(journal[jrnls.TIMESTAMP], FORMAT), datetime)
        assert isinstance(datetime.strptime(journal[jrnls.MODIFIED], FORMAT), datetime)
        assert datetime.strptime(journal[jrnls.TIMESTAMP], FORMAT) <= datetime.strptime(journal[jrnls.MODIFIED], FORMAT)
        
    assert jrnls.exists(temp_journal)


ADD_TITLE = 'Added title'
ADD_PROMPT0 = 'Added prompt0'
ADD_PROMPT1 = 'Added prompt1'
ADD_CONTENT = 'Added content'

INVALID_TIMESTAMP = "invalid timestamp"
NON_STRING = 123


"""
    Ensure:
        - After adding a sample journal entry, it is 
          in the list of journals with valid input
"""
def test_add_journal():
    journal_id = jrnls._get_journal_id()
    ret = jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT0, ADD_CONTENT)
    assert jrnls.exists(journal_id)
    assert isinstance(ret, bool)

    added_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(added_journal) == jrnls.get_modified(added_journal)
    assert jrnls.get_title(added_journal) == ADD_TITLE
    assert jrnls.get_prompt(added_journal) == ADD_PROMPT0
    assert jrnls.get_content(added_journal) == ADD_CONTENT
    jrnls.del_journal(journal_id)


def test_add_dup_journal_id(temp_journal):
    journal_id = temp_journal
        
    # attempting to add journal again
    with pytest.raises(ValueError):
        jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT1, ADD_CONTENT)


def test_add_journal_without_title_or_content():
    journal_id = jrnls._get_journal_id()
    ret = jrnls.add_journal(journal_id, "", ADD_PROMPT1, "")
    assert jrnls.exists(journal_id)
    assert isinstance(ret, bool)

    added_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(added_journal) == jrnls.get_modified(added_journal)
    assert jrnls.get_title(added_journal) == jrnls.DEFAULT_TITLE
    assert jrnls.get_prompt(added_journal) == ADD_PROMPT1
    assert jrnls.get_content(added_journal) == ""
    jrnls.del_journal(journal_id)


def test_add_journal_dup_prompt(temp_journal):
    temp_journal_entry = jrnls.get_journal(temp_journal)
    new_journal_id = jrnls._get_journal_id()
    temp_prompt = jrnls.get_prompt(temp_journal_entry)
    with pytest.raises(ValueError):
        jrnls.add_journal(new_journal_id, "", temp_prompt, "")


def test_add_journal_prompt_too_long():
    journal_id = jrnls._get_journal_id()
    long_prompt = "x" * 500  # Assuming there's a limit to prompt length
    with pytest.raises(ValueError):
        jrnls.add_journal(journal_id, ADD_TITLE, long_prompt, ADD_CONTENT)


def test_add_journal_non_string_title():
    journal_id = jrnls._get_journal_id()
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, NON_STRING, ADD_PROMPT1, ADD_CONTENT)


def test_add_journal_non_string_prompt():
    journal_id = jrnls._get_journal_id()
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, ADD_TITLE, NON_STRING, ADD_CONTENT)


def test_add_journal_non_string_content():
    journal_id = jrnls._get_journal_id()
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT1, NON_STRING)


def test_del_journal(temp_journal):
    journal_id = temp_journal
    jrnls.del_journal(journal_id)
    assert not jrnls.exists(journal_id)


def test_del_journal_not_there():
    journal_id = jrnls._get_journal_id()
    with pytest.raises(ValueError):
        jrnls.del_journal(journal_id)


UPDATED_TITLE = "Updated Title"
UPDATED_PROMPT = "Updated Prompt"
UPDATED_CONTENT = "Updated Content"


def test_update_journal(temp_journal):
    journal_id = temp_journal
    prev_journal = jrnls.get_journal(journal_id)
    prev_timestamp = jrnls.get_timestamp(prev_journal)
    prev_modified = jrnls.get_modified(prev_journal)

    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    assert jrnls.update_journal(journal_id, update_data)

    updated_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(updated_journal) == prev_timestamp
    assert jrnls.get_title(updated_journal) == UPDATED_TITLE
    assert jrnls.get_prompt(updated_journal) == UPDATED_PROMPT
    assert jrnls.get_content(updated_journal) == UPDATED_CONTENT
    assert jrnls.get_modified(updated_journal) >= prev_modified


def test_update_journal_partially(temp_journal):
    journal_id = temp_journal
    prev_journal = jrnls.get_journal(journal_id)
    prev_timestamp = jrnls.get_timestamp(prev_journal)
    prev_prompt = jrnls.get_prompt(prev_journal)
    prev_content = jrnls.get_content(prev_journal)
    prev_modified = jrnls.get_modified(prev_journal)

    update_data = {jrnls.TITLE: UPDATED_TITLE}
    assert jrnls.update_journal(journal_id, update_data)

    updated_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(updated_journal) == prev_timestamp
    assert jrnls.get_title(updated_journal) == UPDATED_TITLE
    assert jrnls.get_prompt(updated_journal) == prev_prompt
    assert jrnls.get_content(updated_journal) == prev_content
    assert jrnls.get_modified(updated_journal) >= prev_modified


def test_update_journal_nonexistent_journal():
    journal_id = jrnls._get_journal_id()
    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    with pytest.raises(ValueError):
        jrnls.update_journal(journal_id, update_data)


def test_update_journal_nothing_to_update(temp_journal):
    journal_id = temp_journal
    update_data = {}
    with pytest.raises(ValueError):
        jrnls.update_journal(journal_id, update_data)
