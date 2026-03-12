from __future__ import annotations

from .budgets import evaluate_budget
from .classifier import classify_action
from .models import (
    ActionRequest,
    Assessment,
    Asset,
    BastionConfig,
    Decision,
    PolicyRule,
    RiskLevel,
    stronger_decision,
)
from .store import StateStore


class PolicyEngine:
    def __init__(self, config: BastionConfig, store: StateStore) -> None:
        self.config = config
        self.store = store

    def evaluate(self, request: ActionRequest) -> Assessment:
        asset = self.config.assets.get(request.asset_id) if request.asset_id else None
        action, risk, destructive, unknown_cost, reasons = classify_action(request, asset)
        backup_status = self.store.get_backup_status(asset)
        budget_status = evaluate_budget(self.config.budgets, self.store, request, unknown_cost=unknown_cost)

        decision = self._baseline_decision(risk)
        require_backup = destructive and asset is not None and asset.backup_freshness_sla_hours is not None
        require_restore_test = risk >= RiskLevel.R3 and asset is not None and asset.restore_test_sla_days is not None
        matched_rules: list[str] = []
        auto_hardening_steps: list[str] = []

        if request.env == "prod" and destructive:
            reasons.append("Production destructive mutation detected.")
            decision = stronger_decision(decision, Decision.REQUIRE_APPROVAL)

        if asset is not None and "critical-data" in asset.tags and destructive:
            reasons.append("Critical data asset requires break-glass.")
            decision = Decision.BREAK_GLASS_ONLY

        if action == "iam.change" and request.env == "prod":
            reasons.append("Production IAM change detected.")
            decision = stronger_decision(decision, Decision.REQUIRE_APPROVAL)

        if require_backup and not backup_status.fresh:
            reasons.extend(backup_status.reasons)
            if asset and asset.backup_command:
                auto_hardening_steps.append("create_backup")
                reasons.append("Bastion can create a fresh backup before execution.")
                decision = stronger_decision(decision, Decision.AUTO_HARDEN_AND_ALLOW)
            else:
                decision = stronger_decision(decision, Decision.DEFER_UNTIL_PRECONDITIONS)

        if require_restore_test and not backup_status.restore_test_ok:
            reasons.extend(backup_status.reasons)
            decision = stronger_decision(decision, Decision.DEFER_UNTIL_PRECONDITIONS)

        if budget_status.decision is not None:
            reasons.extend(budget_status.reasons)
            decision = stronger_decision(decision, budget_status.decision)

        for rule in self.config.rules:
            if self._matches_rule(rule, request, action, risk, destructive, unknown_cost, asset):
                matched_rules.append(rule.id)
                reasons.append(f"Matched policy rule `{rule.id}`.")
                decision = stronger_decision(decision, rule.decision)
                require_backup = require_backup or rule.require_backup
                require_restore_test = require_restore_test or rule.require_restore_test
                if rule.require_approval:
                    decision = stronger_decision(decision, Decision.REQUIRE_APPROVAL)
                if rule.auto_backup and "create_backup" not in auto_hardening_steps:
                    auto_hardening_steps.append("create_backup")

        approval_required = decision in {Decision.REQUIRE_APPROVAL, Decision.BREAK_GLASS_ONLY}
        break_glass_required = decision == Decision.BREAK_GLASS_ONLY

        if request.mode == "shadow" and decision not in {Decision.ALLOW, Decision.ALLOW_WITH_LOG}:
            reasons.append("Shadow mode active: Bastion will log but not block.")

        reasons = list(dict.fromkeys(reasons))
        auto_hardening_steps = list(dict.fromkeys(auto_hardening_steps))

        return Assessment(
            action=action,
            risk=risk,
            decision=decision,
            reasons=reasons,
            destructive=destructive,
            unknown_cost=unknown_cost,
            asset=asset,
            backup_status=backup_status,
            budget_status=budget_status,
            matched_rules=matched_rules,
            auto_hardening_steps=auto_hardening_steps,
            require_backup=require_backup,
            require_restore_test=require_restore_test,
            break_glass_required=break_glass_required,
            approval_required=approval_required,
        )

    def _baseline_decision(self, risk: RiskLevel) -> Decision:
        if risk <= RiskLevel.R0:
            return Decision.ALLOW
        if risk == RiskLevel.R1:
            return Decision.ALLOW_WITH_LOG
        if risk == RiskLevel.R2:
            return Decision.AUTO_HARDEN_AND_ALLOW
        if risk == RiskLevel.R3:
            return Decision.REQUIRE_APPROVAL
        return Decision.BREAK_GLASS_ONLY

    def _matches_rule(
        self,
        rule: PolicyRule,
        request: ActionRequest,
        action: str,
        risk: RiskLevel,
        destructive: bool,
        unknown_cost: bool,
        asset: Asset | None,
    ) -> bool:
        match = rule.match
        if match.envs and request.env not in match.envs:
            return False
        if match.actions and action not in match.actions:
            return False
        if match.destructive is not None and destructive is not match.destructive:
            return False
        if match.min_risk is not None and risk < match.min_risk:
            return False
        if match.unknown_cost is not None and unknown_cost is not match.unknown_cost:
            return False
        if match.actor_types and request.actor_type not in match.actor_types:
            return False
        if match.tags:
            asset_tags = set(asset.tags if asset else ())
            if not asset_tags.issuperset(match.tags):
                return False
        return True
