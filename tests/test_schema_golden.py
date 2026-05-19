from laborix.schema import plan_schema


def test_schema_identity_is_golden() -> None:
    assert plan_schema()["$id"] == "https://laborix.dev/schema/plan-2.0.json"
