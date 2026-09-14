from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import plistlib
import stat
import subprocess
from typing import Any
from uuid import uuid4


SYSTEM_PERSISTENCE_DIRS = (Path("/Library/LaunchAgents"), Path("/Library/LaunchDaemons"))
USER_PERSISTENCE_DIR = Path("Library/LaunchAgents")
SENSITIVE_NAMES = (".env", "secret", "credential", "token", "password", "id_rsa", "private")


@dataclass
class ScanResult:
    state: str
    message: str
    findings: list[dict[str, Any]]
    checks: dict[str, str]
    inventory: list[dict[str, Any]]
    baseline: bool
    updated_at: str


def run_scan(state_dir: str | Path, *, home: str | Path | None = None) -> ScanResult:
    root = Path(state_dir).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    home_path = Path(home).expanduser() if home is not None else Path.home()
    inventory = _collect_persistence(home_path)
    inventory.extend(_collect_processes())
    inventory.extend(_collect_network())
    previous = _read_json(root / "inventory.json")
    baseline = not (root / "baseline-created").exists()
    findings = []

    if baseline:
        message = "Baseline created; review existing persistence before trusting this Mac."
        findings.append({"kind": "baseline", "severity": "medium", "message": message})
    else:
        old_by_key = {str(item.get("key")): item for item in previous}
        for item in inventory:
            old_item = old_by_key.get(item["key"])
            if old_item is None:
                findings.append(
                    {
                        "kind": "new_inventory_item",
                        "severity": "high",
                        "path": item.get("path", item["key"]),
                        "message": "New monitored item since the previous scan.",
                    }
                )
            elif item.get("sha256") != old_item.get("sha256"):
                findings.append(
                    {
                        "kind": "changed_inventory_item",
                        "severity": "high",
                        "path": item.get("path", item["key"]),
                        "message": "Monitored item changed since the previous scan.",
                    }
                )

    checks = _security_checks()
    for name, value in checks.items():
        if value != "enabled":
            findings.append(
                {
                    "kind": "security_posture",
                    "severity": "high" if value == "disabled" else "medium",
                    "check": name,
                    "message": f"{name} is {value}.",
                }
            )

    if any(value == "error" for value in checks.values()):
        state = "degraded"
        message = "Scan completed with unavailable security checks."
    elif findings:
        state = "attention"
        message = f"Scan completed with {len(findings)} finding(s)."
    else:
        state = "protected"
        message = "Scan completed; monitored checks passed."

    updated_at = datetime.now(timezone.utc).isoformat()
    result = ScanResult(state, message, findings, checks, inventory, baseline, updated_at)
    _write_json(root / "inventory.json", inventory)
    (root / "baseline-created").touch()
    _write_json(root / "findings.json", {"updatedAt": updated_at, "findings": findings})
    _write_json(
        root / "status.json",
        {
            "state": state,
            "message": message,
            "updatedAt": updated_at,
            "scanId": uuid4().hex,
            "findingsCount": len(findings),
            "baseline": baseline,
            "checks": checks,
        },
    )
    return result


def _collect_persistence(home: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    directories = [home / USER_PERSISTENCE_DIR, *SYSTEM_PERSISTENCE_DIRS]
    for directory in directories:
        if not directory.exists():
            continue
        try:
            children = sorted(path for path in directory.iterdir() if path.is_file())
        except OSError:
            continue
        for path in children:
            item: dict[str, Any] = {
                "key": f"launchd:{path}",
                "path": str(path),
                "kind": "launchd",
                "mode": stat.filemode(path.stat().st_mode),
            }
            if _is_sensitive_name(path.name):
                item["sha256"] = "redacted"
            else:
                item["sha256"] = _sha256(path)
            if path.suffix == ".plist" and not _is_sensitive_name(path.name):
                item.update(_plist_metadata(path))
            entries.append(item)
    return entries


def _plist_metadata(path: Path) -> dict[str, Any]:
    try:
        with path.open("rb") as handle:
            payload = plistlib.load(handle)
    except (OSError, plistlib.InvalidFileException, ValueError):
        return {"plist": "invalid"}
    arguments = payload.get("ProgramArguments")
    if isinstance(arguments, list):
        program = str(arguments[0]) if arguments else ""
    else:
        program = str(payload.get("Program", ""))
    return {
        "program": program,
        "run_at_load": bool(payload.get("RunAtLoad", False)),
        "keep_alive": bool(payload.get("KeepAlive", False)),
    }


def _collect_processes() -> list[dict[str, Any]]:
    try:
        completed = subprocess.run(
            ("/bin/ps", "-axo", "pid=,ppid=,user=,comm="),
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return [{"key": "processes", "kind": "processes", "state": "error"}]
    if completed.returncode != 0:
        return [{"key": "processes", "kind": "processes", "state": "error"}]
    processes = []
    for line in completed.stdout.splitlines():
        fields = line.split(None, 3)
        if len(fields) != 4:
            continue
        pid, ppid, user, command = fields
        processes.append({"pid": pid, "ppid": ppid, "user": user, "command": command})
    return [{"key": "processes", "kind": "processes", "count": len(processes), "items": processes}]


def _collect_network() -> list[dict[str, Any]]:
    try:
        completed = subprocess.run(
            ("/usr/sbin/lsof", "-nP", "-i", "-sTCP:ESTABLISHED"),
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return [{"key": "network", "kind": "network", "state": "unavailable"}]
    if completed.returncode not in (0, 1):
        return [{"key": "network", "kind": "network", "state": "unavailable"}]
    lines = [line.strip() for line in completed.stdout.splitlines()[1:] if line.strip()]
    endpoints = []
    for line in lines[:500]:
        fields = line.split()
        if len(fields) >= 9:
            endpoints.append({"process": fields[0], "pid": fields[1], "name": fields[-1]})
    return [{"key": "network", "kind": "network", "count": len(endpoints), "items": endpoints}]


def _security_checks() -> dict[str, str]:
    return {
        "filevault": _command_state(("/usr/bin/fdesetup", "status"), "FileVault is On"),
        "gatekeeper": _command_state(("/usr/sbin/spctl", "--status"), "assessments enabled"),
        "sip": _command_state(("/usr/bin/csrutil", "status"), "enabled"),
    }


def _command_state(command: tuple[str, ...], expected: str) -> str:
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "error"
    output = f"{completed.stdout}\n{completed.stderr}".lower()
    if completed.returncode == 0 and expected.lower() in output:
        return "enabled"
    if completed.returncode == 0:
        return "disabled"
    return "error"


def _is_sensitive_name(name: str) -> bool:
    normalized = name.lower()
    return any(part in normalized for part in SENSITIVE_NAMES)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return "unreadable"
    return digest.hexdigest()


def _read_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    return payload if isinstance(payload, list) else []


def _write_json(path: Path, payload: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)
