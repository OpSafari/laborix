from pathlib import Path

from laborix.ledger import Ledger, LedgerRecord


def record(step: str = "a", status: str = "success") -> LedgerRecord:
    return LedgerRecord(step, 1, "i", "v", "c", 7, "o", 0.2, status)


def test_empty_ledger_has_no_records(tmp_path: Path) -> None:
    assert list(Ledger(tmp_path / "run.jsonl").records()) == []
