import pytest
import data.journals as jrnls

from datetime import datetime
from unittest.mock import patch, MagicMock


FORMAT = "%Y-%m-%d %H:%M:%S"

"""
    Ensure:
        - get_journals() returns a dict with at least 1 journal
        - each journal key is a valid timestamp (str)
        - each journal is a dict with the following members:
            - TITLE (str)
            - PROMPT (str)
            - CONTENT (str)
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
        assert jrnls.PROMPT in journal
        assert jrnls.CONTENT in journal
        
        j_title = journal[jrnls.TITLE]
        assert isinstance(j_title, str)

        j_prompt = journal[jrnls.PROMPT]
        assert isinstance(j_prompt, str)
        
        j_content = journal[jrnls.CONTENT]
        assert isinstance(j_content, str)


ADD_TIMESTAMP = '2000-01-01 09:57:00'
ADD_TITLE = 'SOME TITLE'
ADD_PROMPT0 = 'some prompt0'
ADD_PROMPT1 = 'some prompt1'
ADD_CONTENT = 'blah blah blah'
ADD_DATE = '2000-01-01 09:57:00'


"""
    Ensure:
        - After adding a sample journal entry, 
          it is in the list of journals
"""
def test_add_journal():
    jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_PROMPT0, ADD_CONTENT, ADD_DATE)
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {
         jrnls.TITLE: ADD_TITLE,
         jrnls.PROMPT: ADD_PROMPT0,
         jrnls.CONTENT: ADD_CONTENT
        }


def test_add_journal_without_title_or_content():
    jrnls.add_journal(ADD_TIMESTAMP, "", ADD_PROMPT1, "")
    journals = jrnls.get_journals()
    assert ADD_TIMESTAMP in journals
    assert journals[ADD_TIMESTAMP] == {
         jrnls.TITLE: jrnls.DEFAULT_TITLE,
         jrnls.PROMPT: ADD_PROMPT1,
         jrnls.CONTENT: ""
        }


def test_add_journal_dup_prompt():
    with pytest.raises(ValueError):
        jrnls.add_journal(ADD_TIMESTAMP, "", jrnls.TEST_PROMPT, "")



# Cody's update 11/4:
def test_add_journal_invalid_timestamp():
    with pytest.raises(ValueError):
        jrnls.add_journal("invalid timestamp", ADD_TITLE, ADD_PROMPT1, ADD_CONTENT)

def test_add_journal_prompt_too_long():
    long_prompt = "x" * 500  # Assuming there's a limit to prompt length
    with pytest.raises(ValueError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, long_prompt, ADD_CONTENT)

def test_add_journal_non_string_title():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, 123, ADD_PROMPT1, ADD_CONTENT)

def test_add_journal_non_string_prompt():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, 123, ADD_CONTENT)

def test_add_journal_non_string_content():
    with pytest.raises(TypeError):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_PROMPT1, 123)


# Cody's update 11/8
def test_add_journal_with_mocked_datetime():
    mock_now = datetime(2023, 11, 8)
    with patch('data.journals.datetime.now', return_value=mock_now):
        jrnls.add_journal(ADD_TIMESTAMP, ADD_TITLE, ADD_PROMPT0, ADD_CONTENT, ADD_DATE)
        journals = jrnls.get_journals()
        
        # Now assert if the journal with the ADD_TIMESTAMP exists
        assert ADD_TIMESTAMP in journals
        assert journals[ADD_TIMESTAMP] == {
             jrnls.TITLE: ADD_TITLE,
             jrnls.PROMPT: ADD_PROMPT0,
             jrnls.CONTENT: ADD_CONTENT
        }
