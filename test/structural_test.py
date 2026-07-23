from pathlib import Path
import sys

# ==========================================================
# ESTRUCTURA ESPERADA
# None = archivo
# dict = carpeta
# ==========================================================

EXPECTED_STRUCTURE = {
    "assets": {
        "rooms": {},
        "ui": {},
        "npcs": {},
    },
    "data": {
        "memories": {
            "<memory>": {
                "rooms.json": None,
                "computers.json": None,
                "npcs.json": None,
                "events.json": None,
                "story.json": None,
                "metadata.json": None,
                "diaglogues.json": None,
                "documents.json": None,
                "objects.json": None
            }
        }
    },
    "src": {
        "core": {
            "game.py": None,
            "clock.py": None,
            "memory_loader.py": None,
            "render_state.py": None,
        },
        "entities": {
            "npc.py": None
        },
        "managers": {
            "event_manager.py": None
        },
        "ui":{
            "ui.py": None,
            "computer.py": None,
            "document.py": None,
            "assets.py": None,
            "dialogue.py": None,
            "overlay.py": None,
            "renderer.py": None,
            "fonts.py": None
        },
        "world": {
            "objects": {
                "computer.py": None,
                "document.py": None,
                "door.py": None
            },
            "room.py": None,
            "object.py": None,
            "object_factory.py": None
        },
        "main.py": None,
        "constants.py": None,
    },
    "documents": {},
    "test": {},
    ".git": {}
}

# Carpetas cuyo contenido NO se revisa
IGNORED_CONTENT = {
    "documents",
    "test",
    ".git"
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def check_missing(base_path: Path, structure: dict, errors: list):
    """Comprueba que no falte ningún archivo o carpeta."""
    
    if "<memory>" in structure:

        template = structure["<memory>"]

        memories = [
            d for d in base_path.iterdir()
            if d.is_dir() and d.name.startswith("memory_")
        ]

        if not memories:
            errors.append(f"No existe ninguna carpeta memory_* en {base_path.relative_to(PROJECT_ROOT)}")

        for memory in memories:
            check_missing(memory, template, errors)

    # El resto de elementos normales
    for name, content in structure.items():
        if name == "<memory>":
            continue

        path = base_path / name

        if content is None:
            if not path.is_file():
                errors.append(f"Falta el archivo: {path.relative_to(PROJECT_ROOT)}")

        else:
            if not path.is_dir():
                errors.append(f"Falta la carpeta: {path.relative_to(PROJECT_ROOT)}")
            else:
                if name not in IGNORED_CONTENT:
                    check_missing(path, content, errors)


def check_extra(base_path: Path, structure: dict, warnings: list):
    """Busca archivos y carpetas que no estén definidos."""

    template = structure.get("<memory>")
    expected = {k for k in structure if k != "<memory>"}

    for item in base_path.iterdir():

        # Carpetas memory_*
        if (
            template is not None
            and item.is_dir()
            and item.name.startswith("memory_")
        ):
            check_extra(item, template, warnings)
            continue

        # Elemento inesperado
        if item.name not in expected:
            warnings.append(
                f"Elemento no definido: {item.relative_to(PROJECT_ROOT)}"
            )
            continue

        expected_content = structure[item.name]

        if expected_content is None:
            continue

        if item.name in IGNORED_CONTENT:
            continue

        check_extra(item, expected_content, warnings)


def main():

    errors = []
    warnings = []

    check_missing(PROJECT_ROOT, EXPECTED_STRUCTURE, errors)
    check_extra(PROJECT_ROOT, EXPECTED_STRUCTURE, warnings)

    print("=" * 60)

    if errors:
        print("❌ ERRORES")
        print("-" * 60)
        for error in errors:
            print(error)

    if warnings:
        print("⚠️  ADVERTENCIAS")
        print("-" * 60)
        for warning in warnings:
            print(warning)

    if not errors and not warnings:
        print("✅ La estructura del proyecto es correcta.")

    print("=" * 60)

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()