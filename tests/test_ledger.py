from pathlib import Path

from laborix.ledger import Ledger, LedgerRecord


def record(step: str = "a", status: str = "success") -> LedgerRecord:
    return LedgerRecord(step, 1, "i", "v", "c", 7, "o", 0.2, status)


def test_empty_ledger_has_no_records(tmp_path: Path) -> None:
    assert list(Ledger(tmp_path / "run.jsonl").records()) == []


def test_append_links_records(tmp_path: Path) -> None:
    ledger = Ledger(tmp_path / "x")
    first = ledger.append(record("a"))
    second = ledger.append(record("b"))
    assert second["previous_hash"] == first["record_hash"]


def test_verify_detects_ledger_tampering(tmp_path: Path) -> None:
    path = tmp_path / "x"
    ledger = Ledger(path)
    ledger.append(record())
    path.write_text(path.read_text().replace('"status":"success"', '"status":"failed"'))
    assert ledger.verify() == (False, "record 1 content hash mismatch")
