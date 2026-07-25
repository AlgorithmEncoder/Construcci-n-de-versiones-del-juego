"""
test_room_backgrounds.py

Checks that every room background referenced in every memory
exists inside assets/rooms/.

Usage:
    python test_room_backgrounds.py
"""

from __future__ import annotations

import json
from pathlib import Path


# ==========================================================
# Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MEMORIES_PATH = PROJECT_ROOT / "data" / "memories"

ROOM_ASSETS_PATH = PROJECT_ROOT / "assets" / "rooms"


# ==========================================================
# Test
# ==========================================================

def main():

    print("=" * 60)
    print("ROOM BACKGROUND TEST")
    print("=" * 60)

    missing = []
    errors = []

    memories = sorted(MEMORIES_PATH.glob("memory_*"))

    if not memories:
        print("No memories found.")
        return

    for memory in memories:

        rooms_file = memory / "rooms.json"

        if not rooms_file.exists():

            errors.append(
                f"{memory.name}: rooms.json not found."
            )
            continue

        try:

            with open(rooms_file, "r", encoding="utf-8") as file:
                rooms = json.load(file)

        except Exception as exc:

            errors.append(
                f"{memory.name}: cannot read rooms.json ({exc})"
            )
            continue

        for room_id, room in rooms.items():

            background = room.get("background")

            if background is None:

                errors.append(
                    f"{memory.name}/{room_id}: missing 'background' field."
                )
                continue

            image = ROOM_ASSETS_PATH / f"{background}.png"

            if not image.exists():

                missing.append(
                    (
                        memory.name,
                        room_id,
                        background
                    )
                )

    # ======================================================
    # Report
    # ======================================================

    print()

    if errors:

        print("CONFIGURATION ERRORS")
        print("-" * 60)

        for error in errors:
            print(error)

        print()

    if missing:

        print("MISSING BACKGROUNDS")
        print("-" * 60)

        for memory, room, background in missing:

            print(
                f"[{memory}] "
                f"Room '{room}' -> "
                f"assets/rooms/{background}.png NOT FOUND"
            )

        print()

    if not errors and not missing:

        print("All room backgrounds are valid.")

    print("=" * 60)


# ==========================================================

if __name__ == "__main__":
    main()