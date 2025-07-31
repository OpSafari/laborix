import pytest

from laborix.adapters import ScriptedAdapter


def test_scripted_adapter_consumes_in_order() -> None:
    a = ScriptedAdapter({"propose_ideas": ["first", "second"]})
    assert a.propose_ideas("x") == "first"
    assert a.propose_ideas("x") == "second"


def test_scripted_adapter_reports_exhaustion() -> None:
    with pytest.raises(LookupError, match="propose_ideas"):
        ScriptedAdapter({}).propose_ideas("x")
