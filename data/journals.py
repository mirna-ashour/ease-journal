"""
This module interfaces to our journal data.
"""
from datetime import datetime

TITLE = 'title'
PROMPT = 'prompt'
CONTENT = 'content'
DATE_TIME = 'created'

DEFAULT_TITLE = 'Untitled'
TEST_PROMPT = 'Reflect on an act of kindness.'

journals = {
    "2023-10-27 08:30:00": {
        TITLE: "Morning Reflection",
        PROMPT: TEST_PROMPT,
        CONTENT: "My alarm is broken...",
    },
    "2023-10-27 12:45:00": {
        TITLE: "Lunchtime Thoughts",
        PROMPT: "Write about an aspiration.",
        CONTENT: "I was hungry, so...",
    },
    "2023-10-27 18:15:00": {
        TITLE: "Evening Musings",
        PROMPT: "Did you step out of your comfort zone today?",
        CONTENT: "The moon looks like cheese...",
    },
}


# Two blank lines before the function definition
def get_journals() -> dict:
    return journals


# Two blank lines before the function definition
def add_journal(
        timestamp: str, 
        title: str, 
        prompt: str, 
        content: str, 
        date_time: str):
    # Cody's update 11/5 - Check if the input types are correct
    if not isinstance(title, str):
        raise TypeError("Title must be a string")
    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string")
    if not isinstance(content, str):
        raise TypeError("Content must be a string")

    # Cody's update 11/5 - Check prompt length
    if len(prompt) > 255:
        raise ValueError(
            "Woops! Prompt is too long!"
        )
    # fixing a damn long line by splitting it into multiple lines

    # Set default title if empty
    if not title:
        title = DEFAULT_TITLE

    # Check for duplicate prompts
    if any(journal.get(PROMPT) == prompt for journal in journals.values()):
        raise ValueError(f'Duplicate prompt: {prompt=}')

    date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    # Create and add journal entry
    journal_entry = {
        TITLE: title,
        PROMPT: prompt,
        CONTENT: content,
        DATE_TIME: date_time
    }
    journals[timestamp] = journal_entry
