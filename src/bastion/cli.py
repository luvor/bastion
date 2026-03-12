from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys

from .approvals import ConsoleApprovalProvider, NullApprovalProvider, TelegramApprovalProvider
from .config import load_config
from .gateway import BastionGateway
from .models import ActionRequest, ApprovalProviderType, serialize_model
from .policy import PolicyEngine
from .store import StateStore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bastion",
        description="Risk-aware execution gateway for AI agents and operators.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Execute a command through Bastion.")
    _add_request_arguments(run_parser)
    run_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run, prefixed by --")
    run_parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")

    inspect_parser = subparsers.add_parser("inspect", help="Inspect a command without executing it.")
    _add_request_arguments(inspect_parser)
    inspect_parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to inspect, prefixed by --")
    inspect_parser.add_argument("--json", action="store_true", help="Emit machine-readable output.")

    backup_parser = subparsers.add_parser("backup", help="Manage backup state.")
    backup_subparsers = backup_parser.add_subparsers(dest="backup_command", required=True)
    backup_record = backup_subparsers.add_parser("record", help="Record a backup or restore test.")
    backup_record.add_argument("--config", default=None, help="Path to bastion TOML config.")
    backup_record.add_argument("--asset", required=True, help="Asset id.")
    backup_record.add_argument("--snapshot-id", default=None, help="Snapshot id to record.")
    backup_record.add_argument(
        "--restore-tested",
        action="store_true",
        help="Also mark the latest restore test as successful now.",
    )

    ledger_parser = subparsers.add_parser("ledger", help="Read Bastion audit entries.")
    ledger_subparsers = ledger_parser.add_subparsers(dest="ledger_command", required=True)
    ledger_tail = ledger_subparsers.add_parser("tail", help="Show recent audit entries.")
    ledger_tail.add_argument("--config", default=None, help="Path to bastion TOML config.")
    ledger_tail.add_argument("--limit", type=int, default=20, help="Number of entries to print.")
    ledger_tail.add_argument("--json", action="store_true", help="Emit JSON lines.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "backup":
        return handle_backup_record(args)
    if args.command == "ledger":
        return handle_ledger_tail(args)

    request = _request_from_args(args)
    config = load_config(args.config)
    store = StateStore(config.project.state_dir)
    gateway = BastionGateway(
        policy=PolicyEngine(config, store),
        store=store,
        approvals=_build_approvals(config, store),
    )

    try:
        if args.command == "inspect":
            payload = gateway.inspect(request)
            return _emit_inspect(payload, as_json=args.json)

        result = gateway.run(request)
    except RuntimeError as exc:
        print(f"Bastion error: {exc}", file=sys.stderr)
        return 2

    return _emit_run_result(result, as_json=args.json)


def handle_backup_record(args) -> int:
    config = load_config(args.config)
    store = StateStore(config.project.state_dir)
    restore_test_at = datetime.now(timezone.utc) if args.restore_tested else None
    snapshot_id = store.record_backup(
        args.asset,
        snapshot_id=args.snapshot_id,
        restore_test_at=restore_test_at,
    )
    print(f"Recorded backup for {args.asset}: {snapshot_id}")
    return 0


def handle_ledger_tail(args) -> int:
    config = load_config(args.config)
    store = StateStore(config.project.state_dir)
    entries = store.read_ledger(limit=args.limit)
    if args.json:
        for entry in entries:
            print(json.dumps(entry, ensure_ascii=False))
        return 0

    if not entries:
        print("Ledger is empty.")
        return 0

    for entry in entries:
        timestamp = entry.get("timestamp", "n/a")
        print(
            f"{timestamp} | {entry.get('decision')} | {entry.get('env')} | "
            f"{entry.get('action')} | allowed={entry.get('allowed')} | {entry.get('details')}"
        )
    return 0


def _build_approvals(config, store):
    if config.approvals.provider == ApprovalProviderType.NONE:
        return NullApprovalProvider()
    if config.approvals.provider == ApprovalProviderType.TELEGRAM:
        state_path = Path(config.project.state_dir) / config.telegram.state_filename
        return TelegramApprovalProvider.from_config(
            config.telegram,
            state_path,
            timeout_seconds=config.approvals.timeout_seconds,
            poll_interval_seconds=config.approvals.poll_interval_seconds,
        )
    return ConsoleApprovalProvider()


def _request_from_args(args) -> ActionRequest:
    command = list(args.cmd)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise SystemExit("Command is required. Example: bastion run --config examples/bastion.toml -- echo hello")

    return ActionRequest(
        command=command,
        actor=args.actor,
        actor_type=args.actor_type,
        env=args.env,
        asset_id=args.asset,
        description=args.description,
        estimated_cost_usd=args.estimated_cost,
        mode=args.mode,
        session_id=args.session,
        cwd=args.cwd,
        break_glass_reason=args.break_glass_reason,
        extra_tags=tuple(args.tag or ()),
    )


def _emit_inspect(payload: dict[str, object], *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    assessment = payload["assessment"]
    request = payload["request"]
    print(f"Decision: {assessment['decision']}")
    print(f"Risk: {assessment['risk']}")
    print(f"Action: {assessment['action']}")
    print(f"Command: {' '.join(request['command'])}")
    if request.get("asset_id"):
        print(f"Asset: {request['asset_id']}")
    for reason in assessment["reasons"]:
        print(f"- {reason}")
    return 0


def _emit_run_result(result, *, as_json: bool) -> int:
    if as_json:
        print(json.dumps(serialize_model(result), ensure_ascii=False, indent=2))
    else:
        print(f"Request: {result.request_id}")
        print(f"Decision: {result.decision}")
        print(f"Allowed: {result.allowed}")
        if result.details:
            print(result.details)
        if result.backup_snapshot_id:
            print(f"Backup snapshot: {result.backup_snapshot_id}")
        if result.incident_path:
            print(f"Incident capsule: {result.incident_path}")
        if result.approval is not None:
            print(f"Approval: {result.approval.channel} by {result.approval.approver}")
    if result.exit_code is None:
        return 1
    return int(result.exit_code)


def _add_request_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default=None, help="Path to bastion TOML config.")
    parser.add_argument("--actor", default="unknown", help="Actor name recorded in the audit log.")
    parser.add_argument(
        "--actor-type",
        default="agent",
        choices=["agent", "human", "automation"],
        help="Actor category used in policy rules.",
    )
    parser.add_argument("--env", default="dev", help="Target environment.")
    parser.add_argument("--asset", default=None, help="Asset id from the config file.")
    parser.add_argument("--description", default="", help="Human description of the requested action.")
    parser.add_argument("--estimated-cost", type=float, default=None, help="Estimated cost in USD.")
    parser.add_argument(
        "--mode",
        default="enforce",
        choices=["enforce", "shadow"],
        help="Shadow logs decisions without executing the command.",
    )
    parser.add_argument("--session", default="default", help="Session id for spend tracking.")
    parser.add_argument("--cwd", default=None, help="Working directory for command execution.")
    parser.add_argument(
        "--break-glass-reason",
        default=None,
        help="Emergency override reason for break-glass-only actions.",
    )
    parser.add_argument("--tag", action="append", default=None, help="Additional free-form tags.")


if __name__ == "__main__":
    raise SystemExit(main())
