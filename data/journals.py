"""
This module interfaces to our journal data.
"""

TITLE = 'title'
PROMPT = 'prompt'
CONTENT = 'content'

DEFAULT_TITLE = 'Untitled'
TEST_PROMPT = 'Reflect on a act of kindness.'

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


def get_journals() -> dict:
    return journals


def add_journal(timestamp: str, title: str, prompt: str, content: str):
    # if title is empty, set title to default title
    if not title:
        title = DEFAULT_TITLE

    # if prompt is duplicated, raise Value Error
    prompt_dup = any(journal.get(PROMPT) ==
                     prompt for journal in journals.values())
    if prompt_dup:
        raise ValueError(f'Duplicate journal entry prompt: {prompt=}')

    journal_entry = {TITLE: title, PROMPT: prompt, CONTENT: content}
    journals[timestamp] = journal_entry
