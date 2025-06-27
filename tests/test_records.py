def test_statuses_records() -> None:
    from laborix.records import statuses

    assert statuses([{"status": "ok"}, {"status": "failed"}]) == ("ok", "failed")
