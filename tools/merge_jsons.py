from pathlib import Path
import json
import argparse


LIST_FIELDS = ("emails", "chats", "files")


def merge_json_files(input_folder: Path, output_file: Path):

    merged = {}

    json_files = sorted(input_folder.glob("*.json"))

    if not json_files:
        print("No se encontraron archivos JSON.")
        return

    for json_file in json_files:

        print(f"Leyendo {json_file.name}")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for name, content in data.items():

            if name not in merged:
                merged[name] = {
                    "emails": [],
                    "chats": [],
                    "files": []
                }

            for field in LIST_FIELDS:

                merged[name][field].extend(
                    content.get(field, [])
                )

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            merged,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()
    print(f"JSON generado correctamente:")
    print(output_file)


def main():

    parser = argparse.ArgumentParser(
        description="Une varios JSON de ordenadores."
    )

    parser.add_argument(
        "input_folder",
        type=Path,
        help="Carpeta con los JSON"
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default="merged.json",
        help="Archivo de salida"
    )

    args = parser.parse_args()

    merge_json_files(
        args.input_folder,
        args.output
    )


if __name__ == "__main__":
    main()