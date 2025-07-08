def test_statuses_records() -> None:
    from laborix.records import statuses

    assert statuses([{"status": "ok"}, {"status": "failed"}]) == ("ok", "failed")


def test_statuses_accepts_iterators() -> None:
    from laborix.records import statuses

    values = [{"status": "ok"}, {"status": "failed"}]
    assert statuses(iter(values)) == statuses(values)


def test_successful_records() -> None:
    from laborix.records import successful

    assert successful([{"status": "success"}, {"status": "failed"}]) == ({"status": "success"},)


def test_failed_records() -> None:
    from laborix.records import failed

    assert failed([{"status": "success"}, {"status": "failed"}]) == ({"status": "failed"},)


def test_failed_accepts_iterators() -> None:
    from laborix.records import failed

    values = [{"status": "success"}, {"status": "failed"}]
    assert failed(iter(values)) == failed(values)


def test_step_names_records() -> None:
    from laborix.records import step_names

    assert step_names([{"step_id": "a"}, {"step_id": "a"}, {"step_id": "b"}]) == ("a", "b")


def test_attempt_total_records() -> None:
    from laborix.records import attempt_total

    assert attempt_total([{"attempt": 1}, {"attempt": 2}]) == 3


def test_attempt_total_accepts_iterators() -> None:
    from laborix.records import attempt_total

    values = [{"attempt": 1}, {"attempt": 2}]
    assert attempt_total(iter(values)) == attempt_total(values)
