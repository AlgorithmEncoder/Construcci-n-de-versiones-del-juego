"""
time_utils.py

Utility functions for converting game time.
"""

from __future__ import annotations


def time_to_seconds(time_string: str) -> int:
    """
    Converts 'HH:MM' into seconds from 00:00.
    """

    hours, minutes = map(int, time_string.split(":"))

    return hours * 3600 + minutes * 60


def seconds_to_time(total_seconds: int) -> tuple[int, int, int]:
    """
    Converts seconds from 00:00 into
    (hours, minutes, seconds).
    """

    hours = total_seconds // 3600

    total_seconds %= 3600

    minutes = total_seconds // 60

    seconds = total_seconds % 60

    return hours, minutes, seconds