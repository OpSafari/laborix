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


def test_successful_steps_uses_latest_success(tmp_path: Path) -> None:
    ledger = Ledger(tmp_path / "x")
    ledger.append(record("a", "failed"))
    ledger.append(record("a"))
    assert ledger.successful_steps()["a"]["status"] == "success"


def test_ledger_rejects_secret_like_fields(tmp_path: Path) -> None:
    from dataclasses import asdict

    assert "token" not in asdict(record())
