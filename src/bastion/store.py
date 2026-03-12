from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from .models import Asset, BackupStatus, serialize_model


class StateStore:
    def __init__(self, state_dir: str | Path) -> None:
        self.root = Path(state_dir)
        self.root.mkdir(parents=True, exist_ok=True)
        self.incidents_dir = self.root / "incidents"
        self.incidents_dir.mkdir(exist_ok=True)
        self.ledger_path = self.root / "ledger.jsonl"
        self.backups_path = self.root / "backups.json"

    def append_ledger(self, record: dict[str, Any]) -> None:
        line = json.dumps(serialize_model(record), ensure_ascii=False, sort_keys=True)
        with self.ledger_path.open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")

    def read_ledger(self, limit: int | None = None) -> list[dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        lines = self.ledger_path.read_text(encoding="utf-8").splitlines()
        if limit is not None:
            lines = lines[-limit:]
        return [json.loads(line) for line in lines if line.strip()]

    def record_backup(
        self,
        asset_id: str,
        *,
        snapshot_id: str | None = None,
        created_at: datetime | None = None,
        restore_test_at: datetime | None = None,
    ) -> str:
        created_at = created_at or datetime.now(timezone.utc)
        snapshot_id = snapshot_id or f"snap-{uuid4().hex[:12]}"
        payload = self._read_backups()
        asset_payload = payload.setdefault(asset_id, {})
        asset_payload["last_backup_at"] = created_at.isoformat()
        asset_payload["last_snapshot_id"] = snapshot_id
        if restore_test_at is not None:
            asset_payload["last_restore_test_at"] = restore_test_at.isoformat()
        self._write_json(self.backups_path, payload)
        return snapshot_id

    def get_backup_status(self, asset: Asset | None) -> BackupStatus:
        if asset is None:
            return BackupStatus()

        payload = self._read_backups().get(asset.id, {})
        status = BackupStatus()
        now = datetime.now(timezone.utc)

        last_backup_raw = payload.get("last_backup_at")
        if last_backup_raw:
            status.last_backup_at = datetime.fromisoformat(last_backup_raw)
            status.last_snapshot_id = payload.get("last_snapshot_id")

        last_restore_raw = payload.get("last_restore_test_at")
        if last_restore_raw:
            status.last_restore_test_at = datetime.fromisoformat(last_restore_raw)

        if asset.backup_freshness_sla_hours is not None:
            if status.last_backup_at is None:
                status.fresh = False
                status.reasons.append("No recorded backup for asset.")
            else:
                age_hours = (now - status.last_backup_at).total_seconds() / 3600
                if age_hours > asset.backup_freshness_sla_hours:
                    status.fresh = False
                    status.reasons.append(
                        f"Latest backup is {age_hours:.1f}h old, beyond SLA of {asset.backup_freshness_sla_hours}h."
                    )

        if asset.restore_test_sla_days is not None:
            if status.last_restore_test_at is None:
                status.restore_test_ok = False
                status.reasons.append("No successful restore test is recorded.")
            else:
                age_days = (now - status.last_restore_test_at).days
                if age_days > asset.restore_test_sla_days:
                    status.restore_test_ok = False
                    status.reasons.append(
                        f"Latest restore test is {age_days}d old, beyond SLA of {asset.restore_test_sla_days}d."
                    )

        return status

    def spend_totals(self, session_id: str) -> dict[str, float]:
        day_key = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        month_key = datetime.now(timezone.utc).strftime("%Y-%m")
        totals = defaultdict(float)
        for record in self.read_ledger():
            if record.get("event_type") != "execution":
                continue
            if not record.get("allowed"):
                continue
            cost = record.get("estimated_cost_usd")
            if cost in (None, ""):
                continue
            amount = float(cost)
            totals["month"] += amount
            if str(record.get("timestamp", "")).startswith(day_key):
                totals["day"] += amount
            if record.get("session_id") == session_id:
                totals["session"] += amount
        return totals

    def create_incident(
        self,
        request_id: str,
        title: str,
        body: str,
    ) -> Path:
        filename = f"{request_id}.md"
        path = self.incidents_dir / filename
        path.write_text(body, encoding="utf-8")
        return path

    def _read_backups(self) -> dict[str, Any]:
        return self._read_json(self.backups_path)

    def _read_json(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_json(self, path: Path, payload: dict[str, Any]) -> None:
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
