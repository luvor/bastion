from __future__ import annotations

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

from .models import (
    ApprovalConfig,
    ApprovalProviderType,
    Asset,
    BastionConfig,
    BudgetConfig,
    Decision,
    PolicyRule,
    ProjectConfig,
    RiskLevel,
    RuleMatch,
    TelegramConfig,
)


def _as_tuple(value: object | None) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(item) for item in value)


def load_config(path: str | Path | None) -> BastionConfig:
    if path is None:
        data: dict[str, object] = {}
    else:
        config_path = Path(path)
        with config_path.open("rb") as handle:
            data = tomllib.load(handle)

    project_data = data.get("project", {})
    budget_data = data.get("budgets", {})
    approval_data = data.get("approvals", {})
    telegram_data = data.get("telegram", {})

    config = BastionConfig(
        project=ProjectConfig(
            name=str(project_data.get("name", "Bastion")),
            default_env=str(project_data.get("default_env", "dev")),
            state_dir=str(project_data.get("state_dir", ".bastion")),
            default_mode=str(project_data.get("default_mode", "enforce")),
        ),
        budgets=BudgetConfig(
            per_run_usd=_maybe_float(budget_data.get("per_run_usd")),
            per_session_usd=_maybe_float(budget_data.get("per_session_usd")),
            per_day_usd=_maybe_float(budget_data.get("per_day_usd")),
            per_month_usd=_maybe_float(budget_data.get("per_month_usd")),
            warn_at_ratio=float(budget_data.get("warn_at_ratio", 0.8)),
        ),
        approvals=ApprovalConfig(
            provider=ApprovalProviderType(str(approval_data.get("provider", "console")).lower()),
            timeout_seconds=int(approval_data.get("timeout_seconds", 300)),
            poll_interval_seconds=int(approval_data.get("poll_interval_seconds", 5)),
        ),
        telegram=TelegramConfig(
            bot_token_env=str(telegram_data.get("bot_token_env", "BASTION_TELEGRAM_BOT_TOKEN")),
            chat_id_env=str(telegram_data.get("chat_id_env", "BASTION_TELEGRAM_CHAT_ID")),
            allowed_username_env=str(
                telegram_data.get("allowed_username_env", "BASTION_TELEGRAM_ALLOWED_USERNAME")
            ),
            state_filename=str(telegram_data.get("state_filename", "telegram_state.json")),
        ),
    )

    for raw_asset in data.get("assets", []):
        asset = Asset(
            id=str(raw_asset["id"]),
            env=str(raw_asset.get("env", config.project.default_env)),
            tags=_as_tuple(raw_asset.get("tags")),
            backup_freshness_sla_hours=_maybe_int(raw_asset.get("backup_freshness_sla_hours")),
            restore_test_sla_days=_maybe_int(raw_asset.get("restore_test_sla_days")),
            deletion_protection=bool(raw_asset.get("deletion_protection", False)),
            backup_command=_maybe_str(raw_asset.get("backup_command")),
            notes=str(raw_asset.get("notes", "")),
        )
        config.assets[asset.id] = asset

    for raw_rule in data.get("rules", []):
        match_data = raw_rule.get("match", {})
        config.rules.append(
            PolicyRule(
                id=str(raw_rule["id"]),
                decision=Decision(str(raw_rule["decision"]).upper()),
                match=RuleMatch(
                    envs=_as_tuple(match_data.get("envs")),
                    actions=_as_tuple(match_data.get("actions")),
                    tags=_as_tuple(match_data.get("tags")),
                    destructive=match_data.get("destructive"),
                    min_risk=(
                        RiskLevel.coerce(match_data.get("min_risk"))
                        if match_data.get("min_risk") is not None
                        else None
                    ),
                    unknown_cost=match_data.get("unknown_cost"),
                    actor_types=_as_tuple(match_data.get("actor_types")),
                ),
                require_backup=bool(raw_rule.get("require_backup", False)),
                require_restore_test=bool(raw_rule.get("require_restore_test", False)),
                require_approval=bool(raw_rule.get("require_approval", False)),
                auto_backup=bool(raw_rule.get("auto_backup", False)),
                notes=str(raw_rule.get("notes", "")),
            )
        )

    return config


def _maybe_float(value: object | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _maybe_int(value: object | None) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _maybe_str(value: object | None) -> str | None:
    if value in (None, ""):
        return None
    return str(value)
