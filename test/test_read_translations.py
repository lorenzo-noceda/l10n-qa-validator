import pytest

from src.main import read_translations


def test_converts_valid_csv_to_dictionaries(tmp_path):
    csv_path = tmp_path / "translations.csv"
    csv_path.write_text(
        "id,source_text,translated_text\n1,Hello,Hola\n",
        encoding="utf-8",
    )

    translations = read_translations(csv_path)

    assert translations == [
        {"id": "1", "source_text": "Hello", "translated_text": "Hola"}
    ]


def test_missing_required_header_raises_clear_error(tmp_path):
    csv_path = tmp_path / "translations.csv"
    csv_path.write_text("id,source_text\n1,Hello\n", encoding="utf-8")

    with pytest.raises(ValueError, match="missing required column.*translated_text"):
        read_translations(csv_path)


@pytest.mark.parametrize(
    "data",
    [
        "id,source_text,translated_text\n1,Hello\n",
        "id,source_text,translated_text\n1,Hello,Hola,unexpected\n",
    ],
)
def test_wrong_number_of_fields_raises_clear_error(tmp_path, data):
    csv_path = tmp_path / "translations.csv"
    csv_path.write_text(data, encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed CSV data near line 2"):
        read_translations(csv_path)


def test_missing_file_raises_clear_error(tmp_path):
    csv_path = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError, match="Could not find the input CSV file"):
        read_translations(csv_path)


def test_empty_file_raises_clear_error(tmp_path):
    csv_path = tmp_path / "translations.csv"
    csv_path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty or has no header row"):
        read_translations(csv_path)
