"""
===========================================================
Dream Office - Document Analyzer
Version 1.0

Checks:

- files.json integrity
- computer_files.json integrity
- generated files
- missing files
- extra files
- manifest consistency
- binary sources

This script DOES NOT create or modify files.

===========================================================
"""

from pathlib import Path
import json
import hashlib
import os
import argparse


# ==========================================================
# CONFIGURATION
# ==========================================================

ROOT = Path(__file__).parent.parent.parent


# -----------------------------
# CHANGE THESE PATHS
# -----------------------------

MEMORY_FOLDER = ROOT / "data" / "memories" / "memory_01"

FILES_JSON = MEMORY_FOLDER / "files.json"

COMPUTER_FILES_JSON = MEMORY_FOLDER / "computer_files.json"

OUTPUT_FOLDER = MEMORY_FOLDER / "assets" / "documents"

MANIFEST_FILE = Path(__file__).parent / ".manifest.json"


# -----------------------------

SUPPORTED_EXTENSIONS = {

    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".zip"

}


VERBOSE = True


# ==========================================================
# ANALYZER
# ==========================================================

class DocumentAnalyzer:


    def __init__(self):

        self.files = {}

        self.computer_files = {}

        self.manifest = {}

        self.errors = []

        self.warnings = []

        self.stats = {

            "total_documents": 0,

            "missing_files": 0,

            "extra_files": 0,

            "changed_files": 0,

            "invalid_entries": 0

        }


    # ======================================================

    def load_json(self, path):

        with open(
            path,
            "r",
            encoding="utf8"
        ) as file:

            return json.load(file)


    # ======================================================

    def load(self):

        self.files = self.load_json(
            FILES_JSON
        )


        self.computer_files = self.load_json(
            COMPUTER_FILES_JSON
        )


        if MANIFEST_FILE.exists():

            self.manifest = self.load_json(
                MANIFEST_FILE
            )

        else:

            self.warnings.append(
                "Manifest file does not exist."
            )


    # ======================================================

    def calculate_hash(self, data):

        raw = json.dumps(
            data,
            sort_keys=True,
            ensure_ascii=False
        )

        return hashlib.sha256(
            raw.encode("utf8")
        ).hexdigest()


    # ======================================================

    def expected_path(self, document_id):

        return OUTPUT_FOLDER / self.computer_files[document_id]["file"]


    # ======================================================

    def extension(self, document_id):

        return self.expected_path(
            document_id
        ).suffix.lower()
    
    # ======================================================
    # JSON VALIDATION
    # ======================================================

    def check_matching_ids(self):

        file_ids = set(
            self.files.keys()
        )

        computer_ids = set(
            self.computer_files.keys()
        )


        missing_locations = (

            file_ids - computer_ids

        )


        missing_documents = (

            computer_ids - file_ids

        )


        for document_id in sorted(
            missing_locations
        ):

            self.errors.append(

                f"Missing in computer_files.json: {document_id}"

            )

            self.stats["invalid_entries"] += 1



        for document_id in sorted(
            missing_documents
        ):

            self.errors.append(

                f"Missing in files.json: {document_id}"

            )

            self.stats["invalid_entries"] += 1


    # ======================================================

    def check_extensions(self):

        for document_id in self.computer_files:

            ext = self.extension(
                document_id
            )


            if ext not in SUPPORTED_EXTENSIONS:

                self.errors.append(

                    f"Unsupported extension "
                    f"{ext}: {document_id}"

                )

                self.stats["invalid_entries"] += 1


    # ======================================================

    def check_duplicate_paths(self):

        paths = {}

        for document_id, data in self.computer_files.items():

            path = data.get(
                "file"
            )


            if path in paths:

                self.errors.append(

                    "Duplicate path: "

                    f"{path} "

                    f"used by "

                    f"{paths[path]} and {document_id}"

                )

                self.stats["invalid_entries"] += 1


            else:

                paths[path] = document_id


    # ======================================================
    # RUN BASIC CHECKS
    # ======================================================

    def validate_json(self):

        print()

        print("Checking JSON files...")

        print()


        self.check_matching_ids()

        self.check_extensions()

        self.check_duplicate_paths()


        if not self.errors:

            print(
                "JSON validation successful."
            )

        else:

            print(
                f"Found {len(self.errors)} JSON problems."
            )

        print()
    
        # ======================================================
    # OUTPUT ANALYSIS
    # ======================================================

    def collect_output_files(self):

        files = []

        if not OUTPUT_FOLDER.exists():

            return files


        for path in OUTPUT_FOLDER.rglob("*"):

            relative = path.relative_to(
                OUTPUT_FOLDER
            )

            files.append(
                str(relative)
            )


        return files


    # ======================================================

    def expected_files(self):

        expected = []

        for document_id in self.computer_files:

            expected.append(

                self.computer_files[document_id]["file"]

            )


        return expected


    # ======================================================

    def check_missing_output_files(self):

        existing = set(
            self.collect_output_files()
        )

        expected = set(
            self.expected_files()
        )


        missing = expected - existing


        for file in sorted(missing):

            self.warnings.append(

                f"Missing generated file: {file}"

            )

            self.stats["missing_files"] += 1


    # ======================================================

    def check_extra_output_files(self):

        existing = set(
            self.collect_output_files()
        )

        expected = set(
            self.expected_files()
        )


        extra = existing - expected


        for file in sorted(extra):

            self.warnings.append(

                f"Unknown file in output: {file}"

            )

            self.stats["extra_files"] += 1


    # ======================================================

    def analyze_output(self):

        print()

        print("Checking output folder...")

        print()


        self.check_missing_output_files()

        self.check_extra_output_files()


        if (

            self.stats["missing_files"] == 0

            and

            self.stats["extra_files"] == 0

        ):

            print(
                "Output folder is consistent."
            )

        else:

            print(

                "Output folder has differences."

            )

        print()
    
        # ======================================================
    # MANIFEST ANALYSIS
    # ======================================================

    def current_document_hash(self, document_id):

        document = self.files.get(
            document_id
        )

        if document is None:

            return None


        return self.calculate_hash(
            document
        )


    # ======================================================

    def check_manifest_missing_entries(self):

        for document_id in self.files:

            if document_id not in self.manifest:

                self.warnings.append(

                    f"No manifest entry: {document_id}"

                )


    # ======================================================

    def check_manifest_orphans(self):

        for document_id in self.manifest:

            if document_id not in self.files:

                self.warnings.append(

                    f"Manifest entry without document: {document_id}"

                )


    # ======================================================

    def check_changed_documents(self):

        for document_id in self.files:

            if document_id not in self.manifest:

                continue


            stored_hash = self.manifest[document_id].get(
                "hash"
            )


            current_hash = self.current_document_hash(
                document_id
            )


            if stored_hash != current_hash:

                self.warnings.append(

                    f"Document changed since generation: {document_id}"

                )

                self.stats["changed_files"] += 1


    # ======================================================

    def check_manifest_paths(self):

        for document_id, data in self.manifest.items():

            if document_id not in self.computer_files:

                continue


            expected = self.computer_files[document_id]["file"]

            stored = data.get(
                "file"
            )


            if stored != expected:

                self.warnings.append(

                    f"Manifest path mismatch: {document_id}"

                )


    # ======================================================

    def analyze_manifest(self):

        print()

        print("Checking manifest...")

        print()


        if not self.manifest:

            print(
                "No manifest available."
            )

            print()

            return


        self.check_manifest_missing_entries()

        self.check_manifest_orphans()

        self.check_changed_documents()

        self.check_manifest_paths()


        print(
            "Manifest analysis complete."
        )

        print()
    
        # ======================================================
    # CONTENT VALIDATION
    # ======================================================

    def check_document_structure(self):

        for document_id, document in self.files.items():

            if not isinstance(document, dict):

                self.errors.append(

                    f"Invalid document structure: {document_id}"

                )

                self.stats["invalid_entries"] += 1

                continue


            if "content" not in document:

                self.warnings.append(

                    f"No content field: {document_id}"

                )


    # ======================================================

    def check_content_blocks(self):

        valid_types = {

            "heading",

            "paragraph",

            "bullet_list",

            "table",

            "page_break"

        }


        for document_id, document in self.files.items():

            content = document.get(
                "content",
                []
            )


            if not isinstance(content, list):

                self.errors.append(

                    f"Content is not a list: {document_id}"

                )

                self.stats["invalid_entries"] += 1

                continue


            for index, block in enumerate(content):

                if not isinstance(block, dict):

                    self.errors.append(

                        f"Invalid block {index} in {document_id}"

                    )

                    continue


                block_type = block.get(
                    "type"
                )


                if block_type not in valid_types:

                    self.errors.append(

                        f"Unknown block type '{block_type}' "
                        f"in {document_id}"

                    )

                    self.stats["invalid_entries"] += 1


    # ======================================================

    def check_tables(self):

        for document_id, document in self.files.items():

            for block in document.get("content", []):

                if block.get("type") != "table":

                    continue


                headers = block.get(
                    "headers"
                )

                rows = block.get(
                    "rows"
                )


                if not headers:

                    self.errors.append(

                        f"Table without headers: {document_id}"

                    )

                    self.stats["invalid_entries"] += 1


                if not isinstance(rows, list):

                    self.errors.append(

                        f"Invalid table rows: {document_id}"

                    )

                    self.stats["invalid_entries"] += 1

                    continue


                for row in rows:

                    if len(row) != len(headers):

                        self.errors.append(

                            f"Table column mismatch: {document_id}"

                        )

                        self.stats["invalid_entries"] += 1



    # ======================================================

    def check_lists(self):

        for document_id, document in self.files.items():

            for block in document.get("content", []):

                if block.get("type") != "bullet_list":

                    continue


                items = block.get(
                    "items"
                )


                if not items:

                    self.warnings.append(

                        f"Empty list: {document_id}"

                    )


    # ======================================================

    def check_sources(self):

        for document_id, document in self.files.items():

            source = document.get(
                "source"
            )


            if source:

                path = OUTPUT_FOLDER / source


                if not path.exists():

                    self.errors.append(

                        f"Missing source file "
                        f"{source}: {document_id}"

                    )

                    self.stats["invalid_entries"] += 1


    # ======================================================

    def analyze_content(self):

        print()

        print("Checking document content...")

        print()


        self.check_document_structure()

        self.check_content_blocks()

        self.check_tables()

        self.check_lists()

        self.check_sources()


        print(
            "Content analysis complete."
        )

        print()
    
        # ======================================================
    # STATISTICS
    # ======================================================

    def calculate_statistics(self):

        self.stats["total_documents"] = len(
            self.files
        )


        extensions = {}

        folders = {}

        total_blocks = 0

        empty_documents = 0


        for document_id, document in self.files.items():


            # -----------------------------
            # Extensions
            # -----------------------------

            ext = self.extension(
                document_id
            )

            extensions[ext] = (

                extensions.get(ext, 0)

                + 1

            )


            # -----------------------------
            # Folders
            # -----------------------------

            path = self.computer_files[document_id]["file"]

            folder = str(
                Path(path).parent
            )


            folders[folder] = (

                folders.get(folder, 0)

                + 1

            )


            # -----------------------------
            # Content
            # -----------------------------

            blocks = document.get(
                "content",
                []
            )


            total_blocks += len(
                blocks
            )


            if len(blocks) == 0:

                empty_documents += 1



        self.stats["extensions"] = extensions

        self.stats["folders"] = folders

        self.stats["total_blocks"] = total_blocks

        self.stats["average_blocks"] = (

            round(
                total_blocks / len(self.files),
                2
            )

            if self.files

            else 0

        )

        self.stats["empty_documents"] = empty_documents



    # ======================================================

    def calculate_file_sizes(self):

        sizes = []


        for document_id in self.computer_files:

            path = self.expected_path(
                document_id
            )


            if path.exists():

                sizes.append(

                    (
                        document_id,

                        path.stat().st_size

                    )

                )


        sizes.sort(

            key=lambda x: x[1],

            reverse=True

        )


        self.stats["largest_files"] = sizes[:10]


    # ======================================================

    def generate_statistics(self):

        print()

        print("Generating statistics...")

        print()


        self.calculate_statistics()

        self.calculate_file_sizes()


        print(
            "Statistics generated."
        )

        print()


    # ======================================================

    def print_statistics(self):

        print()

        print("=" * 60)

        print("PROJECT STATISTICS")

        print("=" * 60)

        print()


        print(
            f"Documents: "
            f"{self.stats['total_documents']}"
        )


        print(
            f"Total blocks: "
            f"{self.stats['total_blocks']}"
        )


        print(
            f"Average blocks/document: "
            f"{self.stats['average_blocks']}"
        )


        print(
            f"Empty documents: "
            f"{self.stats['empty_documents']}"
        )


        print()

        print("By extension:")


        for ext, amount in sorted(

            self.stats["extensions"].items()

        ):

            print(
                f"  {ext}: {amount}"
            )


        print()

        print("By folder:")


        for folder, amount in sorted(

            self.stats["folders"].items()

        ):

            print(
                f"  {folder}: {amount}"
            )


        print()

        print("Largest generated files:")


        for name, size in self.stats["largest_files"]:

            kb = round(
                size / 1024,
                2
            )

            print(
                f"  {name}: {kb} KB"
            )


        print()

        print("=" * 60)

        print()
    
        # ======================================================
    # REPORT OUTPUT
    # ======================================================

    def print_report(self):

        print()

        print("=" * 60)
        print("ANALYSIS REPORT")
        print("=" * 60)
        print()


        if not self.errors:

            print("✓ No errors found.")

        else:

            print(
                f"✗ Errors found: {len(self.errors)}"
            )

            print()

            for error in self.errors:

                print(
                    "  ERROR:",
                    error
                )


        print()


        if not self.warnings:

            print("✓ No warnings.")

        else:

            print(
                f"! Warnings found: {len(self.warnings)}"
            )

            print()

            for warning in self.warnings:

                print(
                    "  WARNING:",
                    warning
                )


        print()

        print("=" * 60)

        print()
    
        # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report(
        self,
        filename="analysis_report.json"
    ):

        report = self.build_report()

        output = ROOT / filename

        with open(
            output,
            "w",
            encoding="utf8"
        ) as file:

            json.dump(
                report,
                file,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"Report saved: {output}"
        )
    
    def build_report(self):

        return {

            "summary": {

                "errors": len(self.errors),

                "warnings": len(self.warnings),

                "documents": self.stats.get(
                    "total_documents",
                    0
                ),

                "changed_files": self.stats.get(
                    "changed_files",
                    0
                ),

                "missing_files": self.stats.get(
                    "missing_files",
                    0
                ),

                "extra_files": self.stats.get(
                    "extra_files",
                    0
                )

            },

            "errors": self.errors,

            "warnings": self.warnings,

            "statistics": self.stats

        }
    
    def exit_code(self):

        if self.errors:

            return 1

        return 0
    
# ==========================================================
# MAIN
# ==========================================================

# ==========================================================
# COMMAND LINE
# ==========================================================

def parse_arguments():

    parser = argparse.ArgumentParser(

        description=
        "Dream Office document analyzer"

    )


    parser.add_argument(

        "--quiet",

        action="store_true",

        help="Reduce console output"

    )


    parser.add_argument(

        "--no-report",

        action="store_true",

        help="Do not create JSON report"

    )


    parser.add_argument(

        "--stats",

        action="store_true",

        help="Show statistics"

    )


    parser.add_argument(

        "--output",

        default="analysis_report.json",

        help="Report filename"

    )


    return parser.parse_args()



# ==========================================================
# FINAL RUNNER
# ==========================================================

def run_analysis():

    args = parse_arguments()


    analyzer = DocumentAnalyzer()


    if not FILES_JSON.exists():

        print(

            f"Missing configuration: {FILES_JSON}"

        )

        return 2



    if not COMPUTER_FILES_JSON.exists():

        print(

            f"Missing configuration: {COMPUTER_FILES_JSON}"

        )

        return 2



    analyzer.load()



    analyzer.validate_json()

    analyzer.analyze_output()

    analyzer.analyze_manifest()

    analyzer.analyze_content()

    analyzer.generate_statistics()



    if args.stats:

        analyzer.print_statistics()



    if not args.quiet:

        analyzer.print_report()



    if not args.no_report:

        analyzer.save_report(
            args.output
        )


    return analyzer.exit_code()



# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    exit_code = run_analysis()

    raise SystemExit(exit_code)