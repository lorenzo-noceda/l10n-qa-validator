from src.main import find_placeholder_issues


def test_matching_placeholders_return_no_issues():
    translations = [
        {
            "id": "1",
            "source_text": "Hello {user}, click {button}",
            "translated_text": "Hola {user}, pulsa {button}",
        }
    ]

    assert find_placeholder_issues(translations) == []


def test_multiple_missing_placeholders_are_reported_together():
    translations = [
        {
            "id": "2",
            "source_text": "Hello {user}, click {button}",
            "translated_text": "Hola",
        }
    ]

    issues = find_placeholder_issues(translations)

    assert len(issues) == 1
    assert issues[0]["issue_type"] == "missing_placeholder"
    assert "{button}, {user}" in issues[0]["explanation"]


def test_extra_placeholder_is_reported():
    translations = [
        {
            "id": "3",
            "source_text": "Hello",
            "translated_text": "Hola {user}",
        }
    ]

    issues = find_placeholder_issues(translations)

    assert len(issues) == 1
    assert issues[0]["issue_type"] == "extra_placeholder"
    assert "{user}" in issues[0]["explanation"]


def test_placeholder_case_mismatch_reports_missing_and_extra():
    translations = [
        {
            "id": "4",
            "source_text": "Hello {button} and {user}",
            "translated_text": "Hola {Button} y {user}",
        }
    ]

    issues = find_placeholder_issues(translations)

    assert [issue["issue_type"] for issue in issues] == [
        "missing_placeholder",
        "extra_placeholder",
    ]
    assert "{button}" in issues[0]["explanation"]
    assert "{Button}" in issues[1]["explanation"]


def test_repeated_source_placeholder_only_needs_to_appear_once():
    translations = [
        {
            "id": "5",
            "source_text": "{user}, welcome back, {user}",
            "translated_text": "Bienvenido, {user}",
        }
    ]

    assert find_placeholder_issues(translations) == []
