"""
This module interfaces to our journal data.
"""

TITLE = 'title'
PROMPT = 'prompt'
CONTENT = 'content'
MODIFIED = 'modified'

DEFAULT_TITLE = 'Untitled'
TEST_PROMPT = 'Reflect on an act of kindness.'

journals = {
    "2023-10-27 08:30:00": {
        TITLE: "Morning Reflection",
        PROMPT: TEST_PROMPT,
        CONTENT: "My alarm is broken...",
        MODIFIED: "2023-11-28 08:31:00",
    },
    "2023-10-27 12:45:00": {
        TITLE: "Lunchtime Thoughts",
        PROMPT: "Write about an aspiration.",
        CONTENT: "I was hungry, so...",
        MODIFIED: "2023-10-28 11:23:00",
    },
    "2023-10-27 18:15:00": {
        TITLE: "Evening Musings",
        PROMPT: "Did you step out of your comfort zone today?",
        CONTENT: "The moon looks like cheese...",
        MODIFIED: "2023-10-30 20:00:00",
    },
}


def get_journals() -> dict:
    return journals


def add_journal(timestamp: str, title: str, prompt: str,
                content: str, modified: str):
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

    # Set default title if empty
    if not title:
        title = DEFAULT_TITLE

    # Check for duplicate prompts
    if any(journal.get(PROMPT) == prompt for journal in journals.values()):
        raise ValueError(f'Duplicate prompt: {prompt=}')

    # Create and add journal entry
    journal_entry = {
        TITLE: title,
        PROMPT: prompt,
        CONTENT: content,
        MODIFIED: modified,
    }
    journals[timestamp] = journal_entry
