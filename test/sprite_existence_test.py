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

NPC_ASSETS_PATH = PROJECT_ROOT / "assets" / "npcs"


# ==========================================================
# Test
# ==========================================================

def main():

    print("=" * 60)
    print("NPC SPRITE TEST")
    print("=" * 60)

    missing = []
    errors = []

    memories = sorted(MEMORIES_PATH.glob("memory_*"))

    if not memories:
        print("No memories found.")
        return

    for memory in memories:

        npcs_file = memory / "npcs.json"

        if not npcs_file.exists():

            errors.append(
                f"{memory.name}: npcs.json not found."
            )
            continue

        try:

            with open(npcs_file, "r", encoding="utf-8") as file:
                npcs = json.load(file)

        except Exception as exc:

            errors.append(
                f"{memory.name}: cannot read npcs.json ({exc})"
            )
            continue

        for npc_id, npc in npcs.items():

            sprite = npc.get("sprite")

            if sprite is None:

                errors.append(
                    f"{memory.name}/{npc_id}: missing 'sprite' field."
                )
                continue

            sprite = npc.get("sprite")

            if sprite is None:

                errors.append(
                    f"{memory.name}/{npc_id}: missing 'sprite' field."
                )
                continue

            image = NPC_ASSETS_PATH / f"{sprite}.png"

            if not image.exists():

                missing.append(
                    (
                        memory.name,
                        npc_id,
                        sprite
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

        print("MISSING SPRITES")
        print("-" * 60)

        for memory, npc, sprite in missing:

            print(
                f"[{memory}] "
                f"NPC '{npc}' -> "
                f"assets/npcs/{sprite}.png NOT FOUND"
            )

        print()

    if not errors and not missing:

        print("All NPC sprites are valid.")

    print("=" * 60)


# ==========================================================

if __name__ == "__main__":
    main()