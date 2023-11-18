"""
This module interfaces to our journal data.
"""
import random
import data.db_connect as dbc

from datetime import datetime, timedelta


JOURNALS_COLLECT = 'journals'

ID_LEN = 9
BIG_NUM = 1_000_000_000

MOCK_ID = "0" * ID_LEN

TIMESTAMP = 'timestamp'
TITLE = 'title'
PROMPT = 'prompt'
CONTENT = 'content'
MODIFIED = 'modified'

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


def get_test_journal():
    test_journal = {}
    test_journal[TIMESTAMP] = _get_test_timestamp()
    test_journal[TITLE] = DEFAULT_TITLE
    test_journal[PROMPT] = TEST_PROMPT
    test_journal[CONTENT] = 'some content'
    test_journal[MODIFIED] = test_journal[TIMESTAMP]
    return test_journal


def _gen_id() -> str:
    _id = random.randint(0, BIG_NUM)
    _id = str(_id)
    _id = _id.rjust(ID_LEN, '0')
    return _id


def get_journals() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(TIMESTAMP, JOURNALS_COLLECT)


def exists(timestamp: str) -> bool:
    dbc.connect_db()
    return dbc.fetch_one(JOURNALS_COLLECT, {TIMESTAMP: timestamp})


def add_journal(timestamp: str, title: str, prompt: str,
                content: str, modified: str) -> bool:
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

    # Validate timestamp format
    try:
        datetime.strptime(timestamp, FORMAT)
    except ValueError:
        raise ValueError("Invalid timestamp format")

    # Set default title if empty
    if not title:
        title = DEFAULT_TITLE

    # Check for duplicate prompts (case-insensitive)
    if any(journal.get(PROMPT, '').lower() ==
            prompt.lower() for journal in get_journals().values()):
        raise ValueError(f'Duplicate prompt: {prompt}')

    # Create and add journal entry
    journal_entry = {}
    journal_entry[TIMESTAMP] = timestamp
    journal_entry[TITLE] = title
    journal_entry[PROMPT] = prompt
    journal_entry[CONTENT] = content
    journal_entry[MODIFIED] = modified
    dbc.connect_db()
    _id = dbc.insert_one(JOURNALS_COLLECT, journal_entry)
    return _id is not None


def del_journal(timestamp: str):
    if exists(timestamp):
        return dbc.del_one(JOURNALS_COLLECT, {TIMESTAMP: timestamp})
    else:
        raise ValueError(f'Delete failure: {timestamp} not in database.')


def get_journal(timestamp: str):
    dbc.connect_db()
    return dbc.fetch_one(JOURNALS_COLLECT, {TIMESTAMP: timestamp})
