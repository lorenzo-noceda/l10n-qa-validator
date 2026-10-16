from src.main import find_empty_text_issues


def test_empty_translation_returns_issue():
    translations = [
        {
            "id": "5",
            "source_text": "Your order is ready",
            "translated_text": "",
        }
    ]

    issues = find_empty_text_issues(translations)

    assert len(issues) == 1
    assert issues[0]["id"] == "5"
    assert issues[0]["issue_type"] == "empty_translated_text"
    assert (
        issues[0]["explanation"]
        == "The source text 'Your order is ready' has no translation provided."
    )


def test_empty_source_returns_issue():
    translations = [
        {"id": "8", "source_text": "", "translated_text": "Hola"}
    ]

    issues = find_empty_text_issues(translations)

    assert len(issues) == 1
    assert issues[0]["issue_type"] == "empty_source_text"
    assert issues[0]["explanation"] == (
        "The translated text 'Hola' has no source text provided."
    )


def test_both_empty_fields_return_one_issue():
    translations = [
        {"id": "9", "source_text": "", "translated_text": ""}
    ]

    issues = find_empty_text_issues(translations)

    assert len(issues) == 1
    assert issues[0]["issue_type"] == "empty_source_and_translated_text"


def test_whitespace_only_fields_are_empty():
    translations = [
        {"id": "10", "source_text": "   ", "translated_text": "\t"}
    ]

    issues = find_empty_text_issues(translations)

    assert len(issues) == 1
    assert issues[0]["issue_type"] == "empty_source_and_translated_text"


def test_nonempty_fields_return_no_issues():
    translations = [
        {"id": "1", "source_text": "Hello", "translated_text": "Hola"}
    ]

    assert find_empty_text_issues(translations) == []
