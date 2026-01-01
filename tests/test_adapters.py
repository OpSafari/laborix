import pytest

from laborix.adapters import ScriptedAdapter


def test_scripted_adapter_consumes_in_order() -> None:
    a = ScriptedAdapter({"propose_ideas": ["first", "second"]})
    assert a.propose_ideas("x") == "first"
    assert a.propose_ideas("x") == "second"


def test_scripted_adapter_reports_exhaustion() -> None:
    with pytest.raises(LookupError, match="propose_ideas"):
        ScriptedAdapter({}).propose_ideas("x")


def test_replay_adapter_loads_jsonl(tmp_path) -> None:
    from laborix.adapters import ReplayAdapter

    p = tmp_path / "r.jsonl"
    p.write_text('{"kind":"summarize_paper","prompt":"p","response":"s"}' + chr(10))
    assert ReplayAdapter.from_jsonl(p).summarize_paper("p") == "s"
