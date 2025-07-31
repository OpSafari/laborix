from laborix.ablation import ResultTable
from laborix.report import Report, html_report, markdown


def sample():
    return Report(
        "Synthetic <run>",
        {"seed": 7},
        ResultTable(("score",), ((0.5,),)),
        ("offline synthetic data",),
    )


def test_markdown_contains_reproducibility_facts() -> None:
    text = markdown(sample())
    assert "seed: 7" in text
    assert "Limitations" in text


def test_html_report_escapes_hostile_text() -> None:
    text = html_report(sample())
    assert "<run>" not in text
    assert "&lt;run&gt;" in text
