from laborix.schema import plan_schema


def test_plan_schema_has_stable_identity_and_required_fields() -> None:
    schema = plan_schema()
    assert schema["$id"].endswith("plan-2.0.json")
    assert schema["required"] == ["schema_version", "name", "steps"]


def test_plan_schema_returns_an_isolated_copy() -> None:
    schema = plan_schema()
    schema["required"].append("seed")
    assert "seed" not in plan_schema()["required"]
