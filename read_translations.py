import csv
import re
from pathlib import Path

REQUIRED_COLUMNS = {"id", "source_text", "translated_text"}
CSV_PATH = Path(__file__).parent / "data" / "input" / "translations.csv"


def read_translations(path):
    """Read translation records from a CSV file and return them as dictionaries."""
    try:
        with path.open(mode="r", encoding="utf-8-sig", newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames

            if headers is None:
                raise ValueError("The CSV file is empty or has no header row.")

            missing_columns = REQUIRED_COLUMNS - set(headers)
            if missing_columns:
                missing = ", ".join(sorted(missing_columns))
                raise ValueError(
                    f"The CSV file is missing required column(s): {missing}."
                )

            translations = []
            for row in reader:
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(
                        f"Malformed CSV data near line {reader.line_num}: "
                        "a row has more or fewer fields than the header."
                    )
                translations.append(row)

            return translations
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Could not find the input CSV file: {path}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"The CSV file is not valid UTF-8: {path}") from error
    except csv.Error as error:
        raise ValueError(f"Could not parse the CSV file: {error}") from error


def find_empty_text_issues(translations):
    """Return issues for records with empty source or translated text."""
    issues = []
    validation_rules = [
        {
            "issue_type": "empty_translated_text",
            "target_field": "translated_text",
            "ref_field": "source_text",
            "template": "The source text {ref_value!r} has no translation provided.",
        },
        {
            "issue_type": "empty_source_text",
            "target_field": "source_text",
            "ref_field": "translated_text",
            "template": "The translated text {ref_value!r} has no source text provided.",
        },
    ]

    for row in translations:
        source_is_empty = not row["source_text"].strip()
        translation_is_empty = not row["translated_text"].strip()

        if source_is_empty and translation_is_empty:
            issues.append(
                {
                    "id": row["id"],
                    "issue_type": "empty_source_and_translated_text",
                    "explanation": "Both source and translated text are empty.",
                }
            )
            continue

        for rule in validation_rules:
            target_value = row[rule["target_field"]]
            if not target_value.strip():
                ref_value = row[rule["ref_field"]]
                issues.append(
                    {
                        "id": row["id"],
                        "issue_type": rule["issue_type"],
                        "explanation": rule["template"].format(ref_value=ref_value),
                    }
                )

    return issues


def find_missing_placeholder_issues(translations):
    """Return issues for placeholders found in source but absent from translation."""
    issues = []
    for row in translations:
        source_placeholders = set(re.findall(r"\{[^{}]+\}", row["source_text"]))
        translated_placeholders = set(re.findall(r"\{[^{}]+\}", row["translated_text"]))
        missing_placeholders = sorted(source_placeholders - translated_placeholders)
        extra_placeholders = sorted(translated_placeholders - source_placeholders)

        if missing_placeholders:
            placeholder_list = ", ".join(missing_placeholders)
            issues.append(
                {
                    "id": row["id"],
                    "issue_type": "missing_placeholder",
                    "explanation": (
                        f"The translation for {row['source_text']!r} is missing placeholder(s): {placeholder_list}."
                    ),
                }
            )
        if extra_placeholders:
            placeholder_list = ", ".join(extra_placeholders)
            issues.append(
                {
                    "id": row["id"],
                    "issue_type": "extra_placeholder",
                    "explanation": (
                        f"The translation for {row['source_text']!r} contains "
                        f"placeholder(s) not in the source: {placeholder_list}. "
                        "Please review."
                    ),
                }
            )
    return issues


if __name__ == "__main__":
    try:
        rows = read_translations(CSV_PATH)
        print(f"Read {len(rows)} translation record(s):")
        for row in rows:
            print(row)

        issues = find_empty_text_issues(rows)
        issues.extend(find_missing_placeholder_issues(rows))
        print(f"Found {len(issues)} issue(s):")
        for issue in issues:
            print(issue)

    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
