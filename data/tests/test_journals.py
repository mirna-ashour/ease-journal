import pytest
import data.journals as jrnls
import data.users as usrs
import data.categories as ctgs

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


@pytest.fixture(scope='module')
def temp_category(temp_user):
    """
    Fixture to create a temporary category for testing purposes.
    Adds a category to the database associated with a temporary user,
    and deletes it after the test module completes.
    """
    category_id = ctgs._get_category_id()
    user_id = temp_user
    category_name = ctgs._get_category_name()
    ret = ctgs.add_category(category_id, category_name, user_id)
    yield category_id
    if ctgs.exists(category_id):
        ctgs.del_category(category_id)


@pytest.fixture(scope='function')
def temp_journal(temp_category):
    """
    Fixture to create a temporary journal entry for testing purposes.
    Adds a journal entry to the database associated with a temporary user and category,
    and deletes it after each test function that uses this fixture completes.
    """
    journal_id = jrnls._get_journal_id()
    timestamp = jrnls._get_test_timestamp()
    prompt = f"UniquePrompt_{timestamp}"
    user_id = ctgs.get_user(ctgs.get_category(temp_category))
    category_id = temp_category
    ret  = jrnls.add_journal(journal_id, "", prompt, "This is a journal fixture", user_id, category_id)
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


def test_get_user(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_user(journal) == journal[jrnls.USER]


def test_get_modified(temp_journal):
    journal = jrnls.get_journal(temp_journal)
    assert jrnls.get_category(journal) == journal[jrnls.CATEGORY]


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
def test_add_journal(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    ret = jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT0, ADD_CONTENT, user_id, category_id)
    assert jrnls.exists(journal_id)
    assert isinstance(ret, bool)

    added_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(added_journal) == jrnls.get_modified(added_journal)
    assert jrnls.get_title(added_journal) == ADD_TITLE
    assert jrnls.get_prompt(added_journal) == ADD_PROMPT0
    assert jrnls.get_content(added_journal) == ADD_CONTENT
    assert jrnls.get_user(added_journal) == user_id
    assert jrnls.get_category(added_journal) == category_id
    jrnls.del_journal(journal_id)


def test_add_dup_journal_id(temp_journal):
    journal_id = temp_journal
    user_id = jrnls.get_user(jrnls.get_journal(journal_id))
    category_id = jrnls.get_category(jrnls.get_journal(journal_id))
        
    # attempting to add journal again
    with pytest.raises(ValueError):
        jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT1, ADD_CONTENT, user_id, category_id)


def test_add_journal_without_title_or_content(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    ret = jrnls.add_journal(journal_id, "", ADD_PROMPT1, "", user_id, category_id)
    assert jrnls.exists(journal_id)
    assert isinstance(ret, bool)

    added_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(added_journal) == jrnls.get_modified(added_journal)
    assert jrnls.get_title(added_journal) == jrnls.DEFAULT_TITLE
    assert jrnls.get_prompt(added_journal) == ADD_PROMPT1
    assert jrnls.get_content(added_journal) == ""
    assert jrnls.get_user(added_journal) == user_id
    assert jrnls.get_category(added_journal) == category_id
    jrnls.del_journal(journal_id)


def test_add_journal_dup_prompt(temp_journal):
    journal_id = temp_journal
    existing_journal = jrnls.get_journal(journal_id)
    existing_prompt = jrnls.get_prompt(existing_journal)
    new_journal_id = jrnls._get_journal_id()
    user_id = jrnls.get_user(jrnls.get_journal(journal_id))
    category_id = jrnls.get_category(jrnls.get_journal(journal_id))
    with pytest.raises(ValueError):
        jrnls.add_journal(new_journal_id, "", existing_prompt, "", user_id, category_id)


def test_add_journal_prompt_too_long(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    long_prompt = "x" * 500  # Assuming there's a limit to prompt length
    with pytest.raises(ValueError):
        jrnls.add_journal(journal_id, ADD_TITLE, long_prompt, ADD_CONTENT, user_id, category_id)


def test_add_journal_non_string_title(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, NON_STRING, ADD_PROMPT1, ADD_CONTENT, user_id, category_id)


def test_add_journal_non_string_prompt(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, ADD_TITLE, NON_STRING, ADD_CONTENT, user_id, category_id)


def test_add_journal_non_string_content(temp_user, temp_category):
    journal_id = jrnls._get_journal_id()
    user_id = temp_user
    category_id = temp_category
    with pytest.raises(TypeError):
        jrnls.add_journal(journal_id, ADD_TITLE, ADD_PROMPT1, NON_STRING, user_id, category_id)


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
    prev_user = jrnls.get_user(prev_journal)

    updated_category = jrnls.get_category(jrnls.get_journal(journal_id))
    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, 
                   jrnls.CONTENT: UPDATED_CONTENT, jrnls.CATEGORY: updated_category}
    assert jrnls.update_journal(journal_id, update_data)

    updated_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(updated_journal) == prev_timestamp
    assert jrnls.get_title(updated_journal) == UPDATED_TITLE
    assert jrnls.get_prompt(updated_journal) == UPDATED_PROMPT
    assert jrnls.get_content(updated_journal) == UPDATED_CONTENT
    assert jrnls.get_modified(updated_journal) >= prev_modified
    assert jrnls.get_user(updated_journal) == prev_user
    assert jrnls.get_category(updated_journal) == updated_category


def test_update_journal_partially(temp_journal):
    journal_id = temp_journal
    prev_journal = jrnls.get_journal(journal_id)
    prev_timestamp = jrnls.get_timestamp(prev_journal)
    prev_prompt = jrnls.get_prompt(prev_journal)
    prev_content = jrnls.get_content(prev_journal)
    prev_modified = jrnls.get_modified(prev_journal)
    prev_user = jrnls.get_user(prev_journal)
    prev_category = jrnls.get_category(prev_journal)

    update_data = {jrnls.TITLE: UPDATED_TITLE}
    assert jrnls.update_journal(journal_id, update_data)

    updated_journal = jrnls.get_journal(journal_id)
    assert jrnls.get_timestamp(updated_journal) == prev_timestamp
    assert jrnls.get_title(updated_journal) == UPDATED_TITLE
    assert jrnls.get_prompt(updated_journal) == prev_prompt
    assert jrnls.get_content(updated_journal) == prev_content
    assert jrnls.get_modified(updated_journal) >= prev_modified
    assert jrnls.get_user(updated_journal) == prev_user
    assert jrnls.get_category(updated_journal) == prev_category


def test_update_journal_nonexistent_journal():
    journal_id = jrnls._get_journal_id()
    update_data = {jrnls.TITLE: UPDATED_TITLE, jrnls.PROMPT: UPDATED_PROMPT, jrnls.CONTENT: UPDATED_CONTENT}
    with pytest.raises(ValueError):
        jrnls.update_journal(journal_id, update_data)


def test_update_journal_nonexistent_new_category(temp_journal):
    journal_id = temp_journal
    new_category_id = ctgs._get_category_id()
    update_data = {jrnls.CATEGORY: new_category_id}
    with pytest.raises(ValueError):
        jrnls.update_journal(journal_id, update_data)


def test_update_journal_nothing_to_update(temp_journal):
    journal_id = temp_journal
    update_data = {}
    with pytest.raises(ValueError):
        jrnls.update_journal(journal_id, update_data)
