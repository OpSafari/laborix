import pytest

from laborix.cli import main, parser


def test_cli_lists_complete_command_surface() -> None:
    help_text = parser().format_help()
    assert "validate" in help_text
    assert "demo" in help_text


def test_validate_cli_accepts_plan(tmp_path, capsys) -> None:
    p = tmp_path / "p.json"
    p.write_text('{"schema_version":"2.0","name":"x","seed":0,"steps":[]}')
    assert main(["validate", str(p)]) == 0
    assert capsys.readouterr().out == "valid" + chr(10)


def test_cli_requires_subcommand() -> None:
    with pytest.raises(SystemExit):
        main([])
