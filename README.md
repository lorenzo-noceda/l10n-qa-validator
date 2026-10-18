# Translation CSV Validator

A small Python command-line project for checking translation records in a CSV file. It is also a practice project for Python fundamentals, testing, and incremental AI-assisted development.

## Current features

- Reads `data/input/translations.csv` and expects the columns `id`, `source_text`, and `translated_text`.
- Reports missing or whitespace-only source and translated text.
- Reports placeholders such as `{button}` that are missing from one side or appear only on the other. Placeholder matching is case-sensitive.
- Prints validation issues to the terminal.
- Reports understandable errors for missing files, missing headers, invalid UTF-8, and rows with the wrong number of fields.

Repeated source phrases with different translations and exporting `report.csv` are planned, but are not implemented yet.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)

## Set up

From the project directory, sync the project environment and development dependencies:

```bash
uv sync
```

## Input format

Put the input file at `data/input/translations.csv`. It must include these headers:

```csv
id,source_text,translated_text
1,Hello {name},Hola {name}
2,Save changes,
```

## Run

```bash
uv run python src/main.py
```

The current version prints the records it reads and any validation issues to the terminal. It does not create `report.csv` yet.

## Run tests

```bash
uv run python -m pytest
```

The tests cover CSV reading and input errors, empty-text checks, placeholder checks, and the command-line `main()` function.

## Project layout

```text
data/input/    Sample translation CSV
data/output/   Reserved for generated output
src/main.py    CSV reader, validation functions, and entry point
test/          pytest tests
```
