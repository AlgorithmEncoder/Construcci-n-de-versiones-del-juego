"""
Achievement builder.

Builds the presentation data used by the achievements view.

Contains no achievement checking or persistence logic.
"""

from __future__ import annotations


ACHIEVEMENT_DATA = {
    # ==================================================
    # First achievements
    # ==================================================

    "first_incursion": {
        "title": "Primera incursión",
        "description": (
            "Realiza tu primera incursión en una memoria."
        ),
        "category": "general",
        "hidden": False,
    },

    "first_discovery": {
        "title": "Primer fragmento",
        "description": (
            "Realiza tu primer descubrimiento."
        ),
        "category": "discovery",
        "hidden": False,
    },

    "first_document": {
        "title": "Primer documento",
        "description": (
            "Abre un documento por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_computer": {
        "title": "Primer ordenador",
        "description": (
            "Consulta un ordenador por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_email": {
        "title": "Primer correo",
        "description": (
            "Lee un email por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_chat": {
        "title": "Primera conversación",
        "description": (
            "Lee un chat por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_file": {
        "title": "Primer archivo",
        "description": (
            "Abre un archivo por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_dialogue": {
        "title": "Primer contacto",
        "description": (
            "Habla con un personaje por primera vez."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "first_detection": {
        "title": "Te han visto",
        "description": (
            "Sé detectado por primera vez."
        ),
        "category": "detection",
        "hidden": False,
    },

    "first_memory_completed": {
        "title": "Una memoria menos",
        "description": (
            "Completa una memoria."
        ),
        "category": "progress",
        "hidden": False,
    },

    # ==================================================
    # Global memory achievements
    # ==================================================

    "memories_completed_1": {
        "title": "Primera memoria",
        "description": (
            "Completa 1 memoria."
        ),
        "category": "progress",
        "hidden": False,
    },

    "memories_completed_2": {
        "title": "Dos memorias",
        "description": (
            "Completa 2 memorias."
        ),
        "category": "progress",
        "hidden": True,
    },

    "memories_completed_5": {
        "title": "Coleccionista de memorias",
        "description": (
            "Completa 5 memorias."
        ),
        "category": "progress",
        "hidden": True,
    },

    "memories_completed_10": {
        "title": "Más allá de las memorias",
        "description": (
            "Completa 10 memorias."
        ),
        "category": "progress",
        "hidden": True,
    },

    "all_memories_completed": {
        "title": "La investigación continúa",
        "description": (
            "Completa todas las memorias disponibles."
        ),
        "category": "progress",
        "hidden": True,
    },

    # ==================================================
    # Exploration - rooms
    # ==================================================

    "explorer_10": {
        "title": "Explorador",
        "description": (
            "Visita 10 habitaciones."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "explorer_25": {
        "title": "Explorador incansable",
        "description": (
            "Visita 25 habitaciones."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "explorer_50": {
        "title": "Conocedor del terreno",
        "description": (
            "Visita 50 habitaciones."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "explorer_100": {
        "title": "Explorador experto",
        "description": (
            "Visita 100 habitaciones."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "explorer_250": {
        "title": "No queda ningún rincón",
        "description": (
            "Visita 250 habitaciones."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Documents
    # ==================================================

    "document_collector_10": {
        "title": "Archivista",
        "description": (
            "Abre 10 documentos."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "document_collector_25": {
        "title": "Archivista incansable",
        "description": (
            "Abre 25 documentos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "document_collector_50": {
        "title": "Investigador documental",
        "description": (
            "Abre 50 documentos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "document_collector_100": {
        "title": "Adicto a los archivos",
        "description": (
            "Abre 100 documentos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "document_collector_250": {
        "title": "Biblioteca humana",
        "description": (
            "Abre 250 documentos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Computers
    # ==================================================

    "computer_user_10": {
        "title": "Curioso",
        "description": (
            "Consulta 10 ordenadores."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "computer_user_25": {
        "title": "Usuario habitual",
        "description": (
            "Consulta 25 ordenadores."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "computer_user_50": {
        "title": "Intruso digital",
        "description": (
            "Consulta 50 ordenadores."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "computer_user_100": {
        "title": "Rastreador digital",
        "description": (
            "Consulta 100 ordenadores."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "computer_user_250": {
        "title": "No dejes ningún terminal",
        "description": (
            "Consulta 250 ordenadores."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Emails
    # ==================================================

    "email_reader_10": {
        "title": "Buzón lleno",
        "description": (
            "Lee 10 emails."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "email_reader_25": {
        "title": "Entre correos",
        "description": (
            "Lee 25 emails."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "email_reader_50": {
        "title": "Detective del correo",
        "description": (
            "Lee 50 emails."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "email_reader_100": {
        "title": "Buzón interminable",
        "description": (
            "Lee 100 emails."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "email_reader_250": {
        "title": "No tienes vida",
        "description": (
            "Lee 250 emails."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Chats
    # ==================================================

    "chat_reader_10": {
        "title": "Entre líneas",
        "description": (
            "Lee 10 chats."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "chat_reader_25": {
        "title": "Conversador silencioso",
        "description": (
            "Lee 25 chats."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "chat_reader_50": {
        "title": "Rumorólogo",
        "description": (
            "Lee 50 chats."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "chat_reader_100": {
        "title": "No se te escapa nada",
        "description": (
            "Lee 100 chats."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "chat_reader_250": {
        "title": "El gran cotilla",
        "description": (
            "Lee 250 chats."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Files
    # ==================================================

    "file_reader_10": {
        "title": "Archivero",
        "description": (
            "Abre 10 archivos."
        ),
        "category": "exploration",
        "hidden": False,
    },

    "file_reader_25": {
        "title": "Manoseando archivos",
        "description": (
            "Abre 25 archivos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "file_reader_50": {
        "title": "Buscador de pistas",
        "description": (
            "Abre 50 archivos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "file_reader_100": {
        "title": "Rastreador de documentos",
        "description": (
            "Abre 100 archivos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    "file_reader_250": {
        "title": "El archivo eres tú",
        "description": (
            "Abre 250 archivos."
        ),
        "category": "exploration",
        "hidden": True,
    },

    # ==================================================
    # Detection
    # ==================================================

    "detected_1": {
        "title": "Te han visto",
        "description": (
            "Sé detectado 1 vez."
        ),
        "category": "detection",
        "hidden": False,
    },

    "detected_5": {
        "title": "Ya deberías saberlo",
        "description": (
            "Sé detectado 5 veces."
        ),
        "category": "detection",
        "hidden": True,
    },

    "detected_10": {
        "title": "No aprendes",
        "description": (
            "Sé detectado 10 veces."
        ),
        "category": "detection",
        "hidden": True,
    },

    "detected_25": {
        "title": "Te tienen fichado",
        "description": (
            "Sé detectado 25 veces."
        ),
        "category": "detection",
        "hidden": True,
    },

    "detected_50": {
        "title": "Objetivo habitual",
        "description": (
            "Sé detectado 50 veces."
        ),
        "category": "detection",
        "hidden": True,
    },

    "detected_100": {
        "title": "¿Todavía sigues aquí?",
        "description": (
            "Sé detectado 100 veces."
        ),
        "category": "detection",
        "hidden": True,
    },

    # ==================================================
    # Iterations
    # ==================================================

    "iterations_10": {
        "title": "Otra vez",
        "description": (
            "Alcanza 10 iteraciones."
        ),
        "category": "progress",
        "hidden": False,
    },

    "iterations_25": {
        "title": "La rutina",
        "description": (
            "Alcanza 25 iteraciones."
        ),
        "category": "progress",
        "hidden": True,
    },

    "iterations_50": {
        "title": "Atrapar el bucle",
        "description": (
            "Alcanza 50 iteraciones."
        ),
        "category": "progress",
        "hidden": True,
    },

    "iterations_100": {
        "title": "¿Cuántas veces?",
        "description": (
            "Alcanza 100 iteraciones."
        ),
        "category": "progress",
        "hidden": True,
    },

    "iterations_250": {
        "title": "No puedes parar",
        "description": (
            "Alcanza 250 iteraciones."
        ),
        "category": "progress",
        "hidden": True,
    },

    "iterations_500": {
        "title": "El bucle te pertenece",
        "description": (
            "Alcanza 500 iteraciones."
        ),
        "category": "progress",
        "hidden": True,
    },

    # ==================================================
    # Incursions
    # ==================================================

    "incursions_5": {
        "title": "Una vez más",
        "description": (
            "Realiza 5 incursiones."
        ),
        "category": "general",
        "hidden": False,
    },

    "incursions_10": {
        "title": "Volviendo a entrar",
        "description": (
            "Realiza 10 incursiones."
        ),
        "category": "general",
        "hidden": True,
    },

    "incursions_25": {
        "title": "Visitante habitual",
        "description": (
            "Realiza 25 incursiones."
        ),
        "category": "general",
        "hidden": True,
    },

    "incursions_50": {
        "title": "No sabes cuándo parar",
        "description": (
            "Realiza 50 incursiones."
        ),
        "category": "general",
        "hidden": True,
    },

    "incursions_100": {
        "title": "Inmersión total",
        "description": (
            "Realiza 100 incursiones."
        ),
        "category": "general",
        "hidden": True,
    },

    # ==================================================
    # Social
    # ==================================================

    "social_10": {
        "title": "No estás solo",
        "description": (
            "Habla con 10 personajes."
        ),
        "category": "exploration",
        "hidden": False,
    },
}


class AchievementBuilder:
    """
    Builds presentation data for achievements.
    """

    @classmethod
    def build(
        cls,
        achievement_id: str,
        state: dict | None = None,
        visible: bool = True
    ) -> dict:

        data = ACHIEVEMENT_DATA.get(
            achievement_id
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

        # Unknown achievements should never silently
        # become fake locked achievements.
        if data is None:
            return {
                "id": achievement_id,
                "title": achievement_id,
                "description": "",
                "category": "general",
                "hidden": False,
                "unlocked": unlocked,
                "unlocked_at": state.get(
                    "unlocked_at"
                ),
            }

        hidden = bool(
            data.get(
                "hidden",
                False
            )
            and not visible
            and not unlocked
        )

        return {
            "id": achievement_id,
            "title": data["title"],
            "description": data["description"],
            "category": data["category"],
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
        visible_callback=None
    ) -> list[dict]:

        result = []

        if not isinstance(
            achievements,
            dict
        ):
            return result

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

            result.append(
                cls.build(
                    achievement_id,
                    state,
                    visible
                )
            )

        return result