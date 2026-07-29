from pathlib import Path
import json
import argparse


def merge_chats(input_folder: Path, output_file: Path):
    """
    Une todos los JSON de una carpeta en una única lista 'chats'.
    """

    chats = []

    json_files = sorted(input_folder.glob("*.json"))

    if not json_files:
        print("No se encontraron archivos JSON.")
        return

    for json_file in json_files:

        print(f"Leyendo {json_file.name}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        chats.append(data)

    result = {
        "chats": chats
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            result,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(f"Se han combinado {len(chats)} chats.")
    print(f"Archivo generado: {output_file}")


def main():

    parser = argparse.ArgumentParser(
        description="Combina todos los JSON de una carpeta en una lista 'chats'."
    )

    parser.add_argument(
        "input_folder",
        type=Path,
        help="Carpeta que contiene los JSON."
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default="chats.json",
        help="Archivo JSON de salida."
    )

    args = parser.parse_args()

    merge_chats(
        args.input_folder,
        args.output
    )


if __name__ == "__main__":
    main()