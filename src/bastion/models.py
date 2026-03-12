from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, IntEnum
from typing import Any


class RiskLevel(IntEnum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4

    @classmethod
    def coerce(cls, value: str | int | None, default: "RiskLevel" = None) -> "RiskLevel":
        if default is None:
            default = cls.R1
        if value is None:
            return default
        if isinstance(value, int):
            return cls(max(0, min(4, value)))
        normalized = str(value).strip().upper()
        if normalized.startswith("R") and normalized[1:].isdigit():
            return cls(int(normalized[1:]))
        if normalized.isdigit():
            return cls(int(normalized))
        raise ValueError(f"Unsupported risk level: {value}")


class Decision(str, Enum):
    ALLOW = "ALLOW"
    ALLOW_WITH_LOG = "ALLOW_WITH_LOG"
    AUTO_HARDEN_AND_ALLOW = "AUTO_HARDEN_AND_ALLOW"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    DEFER_UNTIL_PRECONDITIONS = "DEFER_UNTIL_PRECONDITIONS"
    DENY = "DENY"
    BREAK_GLASS_ONLY = "BREAK_GLASS_ONLY"


class ApprovalProviderType(str, Enum):
    NONE = "none"
    CONSOLE = "console"
    TELEGRAM = "telegram"


DECISION_SEVERITY: dict[Decision, int] = {
    Decision.ALLOW: 0,
    Decision.ALLOW_WITH_LOG: 1,
    Decision.AUTO_HARDEN_AND_ALLOW: 2,
    Decision.REQUIRE_APPROVAL: 3,
    Decision.DEFER_UNTIL_PRECONDITIONS: 4,
    Decision.DENY: 5,
    Decision.BREAK_GLASS_ONLY: 6,
}


@dataclass
class Asset:
    id: str
    env: str = "dev"
    tags: tuple[str, ...] = ()
    backup_freshness_sla_hours: int | None = None
    restore_test_sla_days: int | None = None
    deletion_protection: bool = False
    backup_command: str | None = None
    notes: str = ""


@dataclass
class RuleMatch:
    envs: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    destructive: bool | None = None
    min_risk: RiskLevel | None = None
    unknown_cost: bool | None = None
    actor_types: tuple[str, ...] = ()


@dataclass
class PolicyRule:
    id: str
    decision: Decision
    match: RuleMatch = field(default_factory=RuleMatch)
    require_backup: bool = False
    require_restore_test: bool = False
    require_approval: bool = False
    auto_backup: bool = False
    notes: str = ""


@dataclass
class ProjectConfig:
    name: str = "Bastion"
    default_env: str = "dev"
    state_dir: str = ".bastion"
    default_mode: str = "enforce"


@dataclass
class BudgetConfig:
    per_run_usd: float | None = None
    per_session_usd: float | None = None
    per_day_usd: float | None = None
    per_month_usd: float | None = None
    warn_at_ratio: float = 0.8


@dataclass
class ApprovalConfig:
    provider: ApprovalProviderType = ApprovalProviderType.CONSOLE
    timeout_seconds: int = 300
    poll_interval_seconds: int = 5


@dataclass
class TelegramConfig:
    bot_token_env: str = "BASTION_TELEGRAM_BOT_TOKEN"
    chat_id_env: str = "BASTION_TELEGRAM_CHAT_ID"
    allowed_username_env: str = "BASTION_TELEGRAM_ALLOWED_USERNAME"
    state_filename: str = "telegram_state.json"


@dataclass
class BastionConfig:
    project: ProjectConfig = field(default_factory=ProjectConfig)
    budgets: BudgetConfig = field(default_factory=BudgetConfig)
    approvals: ApprovalConfig = field(default_factory=ApprovalConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    assets: dict[str, Asset] = field(default_factory=dict)
    rules: list[PolicyRule] = field(default_factory=list)


@dataclass
class ActionRequest:
    command: list[str]
    actor: str
    actor_type: str = "agent"
    env: str = "dev"
    asset_id: str | None = None
    description: str = ""
    estimated_cost_usd: float | None = None
    mode: str = "enforce"
    session_id: str = "default"
    cwd: str | None = None
    break_glass_reason: str | None = None
    extra_tags: tuple[str, ...] = ()

    @property
    def command_text(self) -> str:
        return " ".join(self.command)


@dataclass
class BackupStatus:
    fresh: bool = True
    restore_test_ok: bool = True
    last_backup_at: datetime | None = None
    last_restore_test_at: datetime | None = None
    last_snapshot_id: str | None = None
    reasons: list[str] = field(default_factory=list)


@dataclass
class BudgetStatus:
    allowed: bool = True
    decision: Decision | None = None
    reasons: list[str] = field(default_factory=list)
    estimated_cost_usd: float | None = None
    session_total_after_usd: float | None = None
    day_total_after_usd: float | None = None
    month_total_after_usd: float | None = None


@dataclass
class Assessment:
    action: str
    risk: RiskLevel
    decision: Decision
    reasons: list[str]
    destructive: bool = False
    unknown_cost: bool = False
    asset: Asset | None = None
    backup_status: BackupStatus | None = None
    budget_status: BudgetStatus | None = None
    matched_rules: list[str] = field(default_factory=list)
    auto_hardening_steps: list[str] = field(default_factory=list)
    require_backup: bool = False
    require_restore_test: bool = False
    break_glass_required: bool = False
    approval_required: bool = False

    @property
    def high_risk(self) -> bool:
        return self.risk >= RiskLevel.R3 or self.break_glass_required


@dataclass
class ApprovalRequest:
    request_id: str
    summary: str
    details: str
    timeout_seconds: int
    break_glass_reason: str | None = None


@dataclass
class ApprovalResult:
    approved: bool
    approver: str
    channel: str
    decided_at: datetime
    reason: str = ""


@dataclass
class ExecutionResult:
    request_id: str
    allowed: bool
    decision: Decision
    exit_code: int | None
    approval: ApprovalResult | None = None
    backup_snapshot_id: str | None = None
    incident_path: str | None = None
    details: str = ""


def stronger_decision(current: Decision, candidate: Decision) -> Decision:
    if DECISION_SEVERITY[candidate] > DECISION_SEVERITY[current]:
        return candidate
    return current


def isoformat(dt: datetime | None) -> str | None:
    if dt is None:
        return None
    return dt.isoformat()


def serialize_model(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, RiskLevel):
        return value.name
    if isinstance(value, IntEnum):
        return int(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, list):
        return [serialize_model(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_model(item) for key, item in value.items()}
    if hasattr(value, "__dataclass_fields__"):
        return {
            name: serialize_model(getattr(value, name))
            for name in value.__dataclass_fields__
        }
    return value
