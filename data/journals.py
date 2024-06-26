"""
This module interfaces to our journal data.
"""

import random
# import time
import data.db_connect as dbc
import data.users as usrs
import data.categories as ctgs

from datetime import datetime, timedelta


JOURNALS_COLLECT = 'journals'

ID_LEN = 9
BIG_NUM = 1_000_000_000

MOCK_ID = "0" * ID_LEN

JOURNAL_ID = 'journal_id'
TIMESTAMP = 'timestamp'
TITLE = 'title'
PROMPT = 'prompt'
CONTENT = 'content'
MODIFIED = 'modified'
USER = 'user'
CATEGORY = 'category'

DEFAULT_TITLE = 'Untitled'
TEST_PROMPT = 'Reflect on an act of kindness.'

FORMAT = "%Y-%m-%d %H:%M:%S"

journals = {}


def _get_test_timestamp():
    start_date = datetime(2020, 1, 1)
    rand_days = random.randint(0, 365)
    rand_secs = random.randint(0, 24*60*60)
    rand_timedelta = timedelta(days=rand_days, seconds=rand_secs)
    rand_timestamp = start_date + rand_timedelta
    rand_timestamp_str = rand_timestamp.strftime(FORMAT)
    return rand_timestamp_str


def _get_journal_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_test_journal():
    test_journal = {}
    test_journal[JOURNAL_ID] = _get_journal_id()
    test_journal[TIMESTAMP] = _get_test_timestamp()
    test_journal[TITLE] = DEFAULT_TITLE
    test_journal[PROMPT] = TEST_PROMPT
    test_journal[CONTENT] = 'some content'
    test_journal[MODIFIED] = test_journal[TIMESTAMP]
    test_journal[USER] = usrs._get_user_id()
    test_journal[CATEGORY] = ctgs._get_category_id()
    return test_journal


def get_journals() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(JOURNAL_ID, JOURNALS_COLLECT)


def get_user_journals(user_id: str) -> dict:
    dbc.connect_db()
    all_journals = dbc.fetch_all_as_dict(JOURNAL_ID, JOURNALS_COLLECT)
    user_specific_journals = {}
    for journal_id, journal in all_journals.items():
        if journal[USER] == user_id:
            user_specific_journals[journal_id] = journal
    return user_specific_journals


def get_category_journals(category_id: str) -> dict:
    dbc.connect_db()
    all_journals = dbc.fetch_all_as_dict(JOURNAL_ID, JOURNALS_COLLECT)
    category_specific_journals = {}
    for journal_id, journal in all_journals.items():
        if journal[CATEGORY] == category_id:
            category_specific_journals[journal_id] = journal
    return category_specific_journals


def add_journal(journal_id: str, title: str, prompt: str, content: str,
                user_id: str, category_id: str):
    if exists(journal_id):
        raise ValueError("Duplicate journal")

    # The commented checks below are done in the Journal POST endpoint
    # if not usrs.exists(user_id):
    #     raise wz.NotAcceptable("Please input a user ID that exists.")
    # if not categories.exists(user_id):
    #     raise wz.NotAcceptable("Please input a category ID that exists.")

    # Check if the input types are correct
    if not isinstance(title, str):
        raise TypeError("Title must be a string")
    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string")
    if not isinstance(content, str):
        raise TypeError("Content must be a string")

    # Check prompt length
    if len(prompt) > 255:
        raise ValueError("Prompt exceeds 255 character limit")

    # Check for duplicate prompts (case-insensitive and user-specific)
    # if any(journal.get(PROMPT, '').lower() ==
    #         prompt.lower() for journal in
    # get_user_journals(user_id).values()):
    #     raise ValueError(f'Duplicate prompt: {prompt}')

    # Set the created and modified timestamps
    timestamp = datetime.now().strftime(FORMAT)
    modified = timestamp

    # Set default title if empty
    if not title:
        title = DEFAULT_TITLE

    # Create and add journal entry
    journal_entry = {}
    journal_entry[JOURNAL_ID] = journal_id
    journal_entry[TIMESTAMP] = timestamp
    journal_entry[TITLE] = title
    journal_entry[PROMPT] = prompt
    journal_entry[CONTENT] = content
    journal_entry[MODIFIED] = modified
    journal_entry[USER] = user_id
    journal_entry[CATEGORY] = category_id
    dbc.connect_db()
    _id = dbc.insert_one(JOURNALS_COLLECT, journal_entry)

    # Add (journal_id: title) key-value pair to the
    # corresponding category's Journals field
    category = ctgs.get_category(category_id)
    category_journals = ctgs.get_journals(category)
    category_journals[journal_id] = title
    category_data = {ctgs.JOURNALS: category_journals}
    ctgs.update_category(category_id, category_data)

    return _id is not None


def del_journal(journal_id: str):
    dbc.connect_db()
    if not exists(journal_id):
        raise ValueError(f"Delete failure: {journal_id} not in database.")

    # Removing the journal entry from
    # the category it belongs to before deleting
    journal_entry = get_journal(journal_id)
    category_id = get_category(journal_entry)
    category_entry = ctgs.get_category(category_id)
    category_entry_journals = ctgs.get_journals(category_entry)
    del category_entry_journals[journal_id]
    category_data = {ctgs.JOURNALS: category_entry_journals}
    ctgs.update_category(category_id, category_data)

    dbc.del_one(JOURNALS_COLLECT, {JOURNAL_ID: journal_id})
    return True


def get_journal(journal_id: str) -> dict:
    dbc.connect_db()
    return dbc.fetch_one(JOURNALS_COLLECT, {JOURNAL_ID: journal_id})


def exists(journal_id: str) -> bool:
    return get_journal(journal_id) is not None


def get_timestamp(journal: dict):
    return journal.get(TIMESTAMP)


def get_title(journal: dict):
    return journal.get(TITLE)


def get_prompt(journal: dict):
    return journal.get(PROMPT)


def get_content(journal: dict):
    return journal.get(CONTENT)


def get_modified(journal: dict):
    return journal.get(MODIFIED)


def get_user(journal: dict):
    return journal.get(USER)


def get_category(journal: dict):
    return journal.get(CATEGORY)


def update_journal(journal_id: str, journal_data: dict) -> bool:
    """
    Updates a journal's information.

    Args:
    journal_id (str): The journal_id of the journal to update.
    journal_data (dict): Dictionary containing journal data to update.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    if not exists(journal_id):
        raise ValueError(f"Update failure: {journal_id} not in database.")

    if not journal_data:
        raise ValueError("Update failure: No valid fields to update.")

    update_data = {}
    for key in [TITLE, PROMPT, CONTENT, CATEGORY]:
        if key in journal_data and (len(journal_data[key]) != 0):

            if key == CATEGORY and (len(journal_data[key]) != 0):
                if not ctgs.exists(journal_data[CATEGORY]):
                    raise ValueError("Please input a category ID that exists.")

                # remove journal from previous category
                journal_entry = get_journal(journal_id)
                prev_cat_id = get_category(journal_entry)
                prev_category = ctgs.get_category(prev_cat_id)
                prev_category_journals = ctgs.get_journals(prev_category)
                del prev_category_journals[journal_id]
                prev_category_data = {ctgs.JOURNALS: prev_category_journals}
                ctgs.update_category(prev_cat_id, prev_category_data)

                # add journal to new category
                new_cat_id = journal_data[CATEGORY]
                new_category = ctgs.get_category(new_cat_id)
                new_category_journals = ctgs.get_journals(new_category)
                new_category_journals[journal_id] = get_title(journal_entry)
                new_category_data = {ctgs.JOURNALS: new_category_journals}
                ctgs.update_category(new_cat_id, new_category_data)

            if key == TITLE and (len(journal_data[key]) != 0):
                journal_entry = get_journal(journal_id)
                cat_id = get_category(journal_entry)
                category = ctgs.get_category(cat_id)
                category_journals = ctgs.get_journals(category)
                category_journals[journal_id] = journal_data[TITLE]
                category_data = {ctgs.JOURNALS: category_journals}
                ctgs.update_category(cat_id, category_data)

            update_data[key] = journal_data[key]

    # To see a measureable difference between TIMESTAMP and MODIFIED
    # time.sleep(1)
    update_data[MODIFIED] = datetime.now().strftime(FORMAT)

    dbc.connect_db()
    dbc.update_doc(JOURNALS_COLLECT, {JOURNAL_ID: journal_id}, update_data)
    return True
