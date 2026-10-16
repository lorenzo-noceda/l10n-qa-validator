from src import main as main_module


def test_main_prints_read_count_and_validation_issues(tmp_path, monkeypatch, capsys):
    csv_path = tmp_path / "translations.csv"
    csv_path.write_text(
        "id,source_text,translated_text\n"
        "1,Hello {user},Hola\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(main_module, "INPUT_PATH", csv_path)

    main_module.main()

    output = capsys.readouterr().out
    assert "Read 1 translation record(s)" in output
    assert "missing_placeholder" in output
    assert "{user}" in output
