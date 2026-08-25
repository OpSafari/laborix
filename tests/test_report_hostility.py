from laborix.ablation import ResultTable
from laborix.report import Report, html_report


def test_report_escapes_hostile_metadata_and_title() -> None:
    value = Report(
        "<script>x</script>", {"note": "a&b"}, ResultTable(("x",), ((1,),)), ("<unsafe>",)
    )
    text = html_report(value)
    assert "<script>" not in text
    assert "&lt;script&gt;" in text
    assert "&amp;" in text
    assert "&lt;unsafe&gt;" in text
