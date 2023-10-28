"""
This module interfaces to our journal data.
"""

TITLE = 'title'
CONTENT = 'content'

journals = {
    "2023-10-27 08:30:00": {
        TITLE: "Morning Reflection",
        CONTENT: "My alarm is broken...",
    },
    "2023-10-27 12:45:00": {
        TITLE: "Lunchtime Thoughts",
        CONTENT: "I was hungry, so...",
    },
    "2023-10-27 18:15:00": {
        TITLE: "Evening Musings",
        CONTENT: "The moon looks like cheese...",
    },
}


def get_journals() -> dict:
    return journals
