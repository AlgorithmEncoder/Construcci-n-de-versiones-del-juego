"""
Achievement checks.

Contains only the conditions used to determine whether
an achievement has been unlocked.

This module contains no persistence or presentation logic.
"""

from __future__ import annotations


# ==================================================
# Helpers
# ==================================================

def _value(
    stats,
    section,
    key,
    default=0
):
    """
    Safely obtain a numeric statistic from a memory
    statistics dictionary.
    """

    try:

        return int(
            stats.get(
                section,
                {}
            ).get(
                key,
                default
            )
        )

    except (
        TypeError,
        ValueError
    ):

        return default


# ==================================================
# First achievements
# ==================================================

def first_incursion(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 1


def first_discovery(stats):

    return bool(
        stats.get(
            "discoveries",
            {}
        )
    )


def first_document(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 1


def first_computer(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 1


def first_email(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 1


def first_chat(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 1


def first_file(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 1


def first_dialogue(stats):

    return _value(
        stats,
        "exploration",
        "npcs_talked_to"
    ) >= 1


def first_detection(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 1


def first_memory_completed(stats):

    return bool(
        stats.get(
            "state",
            {}
        ).get(
            "completed",
            False
        )
    )


# ==================================================
# Global memory achievements
# ==================================================

def all_memories_completed(
    stats_manager
):
    """
    Returns True when every known memory is completed.
    """

    memories = getattr(
        stats_manager,
        "memories",
        {}
    )

    if not memories:

        return False

    return all(
        bool(
            stats.get(
                "state",
                {}
            ).get(
                "completed",
                False
            )
        )
        for stats in memories.values()
    )


def memories_completed_1(
    stats_manager
):

    return _completed_memories_count(
        stats_manager
    ) >= 1


def memories_completed_2(
    stats_manager
):

    return _completed_memories_count(
        stats_manager
    ) >= 2


def memories_completed_5(
    stats_manager
):

    return _completed_memories_count(
        stats_manager
    ) >= 5


def memories_completed_10(
    stats_manager
):

    return _completed_memories_count(
        stats_manager
    ) >= 10


def _completed_memories_count(
    stats_manager
):

    memories = getattr(
        stats_manager,
        "memories",
        {}
    )

    return sum(
        1
        for stats in memories.values()
        if bool(
            stats.get(
                "state",
                {}
            ).get(
                "completed",
                False
            )
        )
    )


# ==================================================
# Exploration
# ==================================================

def explorer_10(stats):

    return _value(
        stats,
        "exploration",
        "rooms_visited"
    ) >= 10


def explorer_25(stats):

    return _value(
        stats,
        "exploration",
        "rooms_visited"
    ) >= 25


def explorer_50(stats):

    return _value(
        stats,
        "exploration",
        "rooms_visited"
    ) >= 50


def explorer_100(stats):

    return _value(
        stats,
        "exploration",
        "rooms_visited"
    ) >= 100


def explorer_250(stats):

    return _value(
        stats,
        "exploration",
        "rooms_visited"
    ) >= 250


# ==================================================
# Documents
# ==================================================

def document_collector_10(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 10


def document_collector_25(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 25


def document_collector_50(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 50


def document_collector_100(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 100


def document_collector_250(stats):

    return _value(
        stats,
        "exploration",
        "documents_opened"
    ) >= 250


# ==================================================
# Computers
# ==================================================

def computer_user_10(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 10


def computer_user_25(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 25


def computer_user_50(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 50


def computer_user_100(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 100


def computer_user_250(stats):

    return _value(
        stats,
        "exploration",
        "computers_opened"
    ) >= 250


# ==================================================
# Emails
# ==================================================

def email_reader_10(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 10


def email_reader_25(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 25


def email_reader_50(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 50


def email_reader_100(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 100


def email_reader_250(stats):

    return _value(
        stats,
        "exploration",
        "emails_read"
    ) >= 250


# ==================================================
# Chats
# ==================================================

def chat_reader_10(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 10


def chat_reader_25(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 25


def chat_reader_50(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 50


def chat_reader_100(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 100


def chat_reader_250(stats):

    return _value(
        stats,
        "exploration",
        "chats_read"
    ) >= 250


# ==================================================
# Files
# ==================================================

def file_reader_10(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 10


def file_reader_25(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 25


def file_reader_50(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 50


def file_reader_100(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 100


def file_reader_250(stats):

    return _value(
        stats,
        "exploration",
        "files_opened"
    ) >= 250


# ==================================================
# Detection
# ==================================================

def detected_1(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 1


def detected_5(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 5


def detected_10(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 10


def detected_25(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 25


def detected_50(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 50


def detected_100(stats):

    return _value(
        stats,
        "detection",
        "total"
    ) >= 100


# ==================================================
# Iterations
# ==================================================

def iterations_10(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 10


def iterations_25(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 25


def iterations_50(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 50


def iterations_100(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 100


def iterations_250(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 250


def iterations_500(stats):

    return _value(
        stats,
        "played",
        "iterations"
    ) >= 500


# ==================================================
# Incursions
# ==================================================

def incursions_5(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 5


def incursions_10(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 10


def incursions_25(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 25


def incursions_50(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 50


def incursions_100(stats):

    return _value(
        stats,
        "played",
        "times_incursion"
    ) >= 100


# ==================================================
# Social
# ==================================================

def social_10(stats):

    return _value(
        stats,
        "exploration",
        "npcs_talked_to"
    ) >= 10