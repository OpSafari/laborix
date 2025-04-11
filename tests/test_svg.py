import pytest

from laborix.svg import regret_svg


def test_regret_svg_is_deterministic_and_labeled() -> None:
    chart = regret_svg([0.0, 0.5, 0.75])
    assert chart == regret_svg([0.0, 0.5, 0.75])
    assert "synthetic data" in chart
    assert "polyline" in chart


def test_regret_svg_handles_empty_series_and_dimensions() -> None:
    assert "polyline" not in regret_svg([])
    with pytest.raises(ValueError, match="dimensions"):
        regret_svg([1], 10, 20)
