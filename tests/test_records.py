def test_statuses_records() -> None:
    from laborix.records import statuses

    assert statuses([{"status": "ok"}, {"status": "failed"}]) == ("ok", "failed")


def test_statuses_accepts_iterators() -> None:
    from laborix.records import statuses

    values = [{"status": "ok"}, {"status": "failed"}]
    assert statuses(iter(values)) == statuses(values)
