"""
Achievement builder.

Builds the presentation data used by the achievements view.

Contains no achievement checking, persistence logic,
or translated achievement data.
"""

from __future__ import annotations


class AchievementBuilder:

    """
    Builds presentation data for achievements.

    Achievement definitions are supplied externally,
    normally from the language-specific achievement
    JSON loaded by the achievement data manager.
    """

    @classmethod
    def build(
        cls,
        achievement_id: str,
        data: dict | None = None,
        state: dict | None = None,
        visible: bool = True
    ) -> dict:

        data = (
            data
            if isinstance(data, dict)
            else {}
        )

        state = (
            state
            if isinstance(state, dict)
            else {}
        )

        unlocked = bool(
            state.get(
                "unlocked",
                False
            )
        )

        # --------------------------------------------------
        # Hidden achievement
        # --------------------------------------------------

        hidden = bool(
            data.get(
                "hidden",
                False
            )
            and not visible
            and not unlocked
        )

        # --------------------------------------------------
        # Result
        # --------------------------------------------------

        return {
            "id": achievement_id,

            "title": data.get(
                "title",
                achievement_id
            ),

            "description": data.get(
                "description",
                ""
            ),

            "category": data.get(
                "category",
                "general"
            ),

            "hidden": hidden,

            "unlocked": unlocked,

            "unlocked_at": state.get(
                "unlocked_at"
            ),
        }

    # --------------------------------------------------

    @classmethod
    def build_all(
        cls,
        achievements: dict,
        achievement_data: dict,
        visible_callback=None
    ) -> list[dict]:

        result = []

        if not isinstance(
            achievements,
            dict
        ):

            return result

        if not isinstance(
            achievement_data,
            dict
        ):

            achievement_data = {}

        for achievement_id, state in (
            achievements.items()
        ):

            visible = True

            if visible_callback is not None:

                visible = bool(
                    visible_callback(
                        achievement_id
                    )
                )

            data = achievement_data.get(
                achievement_id,
                {}
            )

            result.append(
                cls.build(
                    achievement_id,
                    data,
                    state,
                    visible
                )
            )

        return result