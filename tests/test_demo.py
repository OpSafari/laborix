from laborix.demo import run_demo


def test_demo_executes_and_writes_honest_report(tmp_path) -> None:
    facts = run_demo(tmp_path)
    assert facts["synthetic"] is True
    assert facts["runs"] == 24
    assert "No model" in (tmp_path / "report.html").read_text()
