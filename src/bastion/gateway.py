from __future__ import annotations

from datetime import datetime, timezone
import shlex
import subprocess
from typing import Any
from uuid import uuid4

from .approvals import ApprovalProvider
from .models import ActionRequest, ApprovalRequest, Decision, ExecutionResult, serialize_model
from .policy import PolicyEngine
from .store import StateStore


class BastionGateway:
    def __init__(
        self,
        *,
        policy: PolicyEngine,
        store: StateStore,
        approvals: ApprovalProvider,
    ) -> None:
        self.policy = policy
        self.store = store
        self.approvals = approvals

    def inspect(self, request: ActionRequest) -> dict[str, Any]:
        assessment = self.policy.evaluate(request)
        payload = {
            "request": serialize_model(request),
            "assessment": serialize_model(assessment),
        }
        return payload

    def run(self, request: ActionRequest) -> ExecutionResult:
        request_id = uuid4().hex[:12]
        assessment = self.policy.evaluate(request)
        approval = None
        backup_snapshot_id = None
        incident_path = None

        if assessment.high_risk:
            incident_path = str(
                self.store.create_incident(
                    request_id,
                    title=f"Bastion incident capsule {request_id}",
                    body=self._render_incident(request_id, request, assessment, status="pending"),
                )
            )

        if request.mode != "shadow" and assessment.auto_hardening_steps:
            backup_snapshot_id = self._run_auto_hardening(request_id, request, assessment)

        blocked, details = self._should_block(request, assessment)
        if blocked:
            self._record_execution(
                request_id,
                request,
                assessment,
                allowed=request.mode == "shadow",
                exit_code=None,
                approval=approval,
                backup_snapshot_id=backup_snapshot_id,
                incident_path=incident_path,
                details=details,
            )
            if incident_path is not None:
                self.store.create_incident(
                    request_id,
                    title=f"Bastion incident capsule {request_id}",
                    body=self._render_incident(request_id, request, assessment, status="blocked", details=details),
                )
            return ExecutionResult(
                request_id=request_id,
                allowed=request.mode == "shadow",
                decision=assessment.decision,
                exit_code=0 if request.mode == "shadow" else None,
                approval=None,
                backup_snapshot_id=backup_snapshot_id,
                incident_path=incident_path,
                details=details,
            )

        if assessment.approval_required:
            approval_request = ApprovalRequest(
                request_id=request_id,
                summary=self._render_approval_summary(request, assessment),
                details=self._render_approval_details(request, assessment),
                timeout_seconds=self.policy.config.approvals.timeout_seconds,
                break_glass_reason=request.break_glass_reason,
            )
            approval = self.approvals.request(approval_request)
            if not approval.approved:
                details = "Approval rejected or timed out."
                self._record_execution(
                    request_id,
                    request,
                    assessment,
                    allowed=False,
                    exit_code=None,
                    approval=approval,
                    backup_snapshot_id=backup_snapshot_id,
                    incident_path=incident_path,
                    details=details,
                )
                if incident_path is not None:
                    self.store.create_incident(
                        request_id,
                        title=f"Bastion incident capsule {request_id}",
                        body=self._render_incident(
                            request_id,
                            request,
                            assessment,
                            status="rejected",
                            approval=approval,
                            details=details,
                        ),
                    )
                return ExecutionResult(
                    request_id=request_id,
                    allowed=False,
                    decision=assessment.decision,
                    exit_code=None,
                    approval=approval,
                    backup_snapshot_id=backup_snapshot_id,
                    incident_path=incident_path,
                    details=details,
                )

        if request.mode == "shadow":
            details = "Shadow mode: command not executed."
            self._record_execution(
                request_id,
                request,
                assessment,
                allowed=True,
                exit_code=0,
                approval=approval,
                backup_snapshot_id=backup_snapshot_id,
                incident_path=incident_path,
                details=details,
            )
            return ExecutionResult(
                request_id=request_id,
                allowed=True,
                decision=assessment.decision,
                exit_code=0,
                approval=approval,
                backup_snapshot_id=backup_snapshot_id,
                incident_path=incident_path,
                details=details,
            )

        completed = subprocess.run(request.command, cwd=request.cwd, check=False)
        details = f"Command exited with status {completed.returncode}."
        self._record_execution(
            request_id,
            request,
            assessment,
            allowed=True,
            exit_code=completed.returncode,
            approval=approval,
            backup_snapshot_id=backup_snapshot_id,
            incident_path=incident_path,
            details=details,
        )
        if incident_path is not None:
            self.store.create_incident(
                request_id,
                title=f"Bastion incident capsule {request_id}",
                body=self._render_incident(
                    request_id,
                    request,
                    assessment,
                    status="executed",
                    approval=approval,
                    backup_snapshot_id=backup_snapshot_id,
                    details=details,
                    exit_code=completed.returncode,
                ),
            )
        return ExecutionResult(
            request_id=request_id,
            allowed=True,
            decision=assessment.decision,
            exit_code=completed.returncode,
            approval=approval,
            backup_snapshot_id=backup_snapshot_id,
            incident_path=incident_path,
            details=details,
        )

    def _run_auto_hardening(self, request_id: str, request: ActionRequest, assessment) -> str | None:
        if "create_backup" not in assessment.auto_hardening_steps or assessment.asset is None:
            return None
        asset = assessment.asset
        if not asset.backup_command:
            return None

        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        backup_cmd = asset.backup_command.format(
            asset_id=asset.id,
            request_id=request_id,
            timestamp=timestamp,
        )
        completed = subprocess.run(shlex.split(backup_cmd), cwd=request.cwd, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RuntimeError(
                f"Auto-backup command failed for asset {asset.id}: {completed.stderr.strip() or completed.stdout.strip()}"
            )
        snapshot_id = (completed.stdout or "").strip() or f"snap-{request_id}"
        self.store.record_backup(asset.id, snapshot_id=snapshot_id)
        return snapshot_id

    def _should_block(self, request: ActionRequest, assessment) -> tuple[bool, str]:
        if request.mode == "shadow":
            return False, "Shadow mode active."
        if assessment.decision == Decision.DENY:
            return True, "Policy denied the action."
        if assessment.decision == Decision.DEFER_UNTIL_PRECONDITIONS:
            return True, "Required preconditions are not satisfied."
        if assessment.decision == Decision.BREAK_GLASS_ONLY and not request.break_glass_reason:
            return True, "Break-glass reason is required."
        return False, ""

    def _record_execution(
        self,
        request_id: str,
        request: ActionRequest,
        assessment,
        *,
        allowed: bool,
        exit_code: int | None,
        approval,
        backup_snapshot_id: str | None,
        incident_path: str | None,
        details: str,
    ) -> None:
        self.store.append_ledger(
            {
                "event_type": "execution",
                "request_id": request_id,
                "timestamp": datetime.now(timezone.utc),
                "allowed": allowed,
                "decision": assessment.decision,
                "risk": assessment.risk,
                "action": assessment.action,
                "command": request.command,
                "actor": request.actor,
                "actor_type": request.actor_type,
                "env": request.env,
                "asset_id": request.asset_id,
                "session_id": request.session_id,
                "break_glass_reason": request.break_glass_reason,
                "estimated_cost_usd": request.estimated_cost_usd,
                "approval": approval,
                "backup_snapshot_id": backup_snapshot_id,
                "incident_path": incident_path,
                "matched_rules": assessment.matched_rules,
                "reasons": assessment.reasons,
                "exit_code": exit_code,
                "details": details,
            }
        )

    def _render_approval_summary(self, request: ActionRequest, assessment) -> str:
        summary = [
            f"Decision: {assessment.decision}",
            f"Risk: {assessment.risk.name}",
            f"Action: {assessment.action}",
            f"Environment: {request.env}",
            f"Command: {request.command_text}",
        ]
        if request.asset_id:
            summary.append(f"Asset: {request.asset_id}")
        if request.estimated_cost_usd is not None:
            summary.append(f"Estimated cost: ${request.estimated_cost_usd:.2f}")
        if request.break_glass_reason:
            summary.append(f"Break-glass reason: {request.break_glass_reason}")
        return "\n".join(summary)

    def _render_approval_details(self, request: ActionRequest, assessment) -> str:
        details = ["Why Bastion stopped this:"]
        details.extend(f"- {reason}" for reason in assessment.reasons)
        if assessment.backup_status and assessment.backup_status.last_snapshot_id:
            details.append(f"- Latest snapshot: {assessment.backup_status.last_snapshot_id}")
        if assessment.auto_hardening_steps:
            details.append(f"- Auto-hardening: {', '.join(assessment.auto_hardening_steps)}")
        return "\n".join(details)

    def _render_incident(
        self,
        request_id: str,
        request: ActionRequest,
        assessment,
        *,
        status: str,
        approval=None,
        backup_snapshot_id: str | None = None,
        details: str = "",
        exit_code: int | None = None,
    ) -> str:
        lines = [
            f"# Bastion Incident Capsule {request_id}",
            "",
            f"- Status: {status}",
            f"- Timestamp: {datetime.now(timezone.utc).isoformat()}",
            f"- Actor: {request.actor} ({request.actor_type})",
            f"- Environment: {request.env}",
            f"- Action: {assessment.action}",
            f"- Risk: {assessment.risk.name}",
            f"- Decision: {assessment.decision}",
            f"- Command: `{request.command_text}`",
        ]
        if request.asset_id:
            lines.append(f"- Asset: {request.asset_id}")
        if request.break_glass_reason:
            lines.append(f"- Break-glass reason: {request.break_glass_reason}")
        if request.estimated_cost_usd is not None:
            lines.append(f"- Estimated cost: ${request.estimated_cost_usd:.2f}")
        if backup_snapshot_id:
            lines.append(f"- Backup snapshot: {backup_snapshot_id}")
        if approval is not None:
            lines.append(f"- Approval: {approval.channel} by {approval.approver} ({approval.reason})")
        if exit_code is not None:
            lines.append(f"- Exit code: {exit_code}")
        lines.append("")
        lines.append("## Reasons")
        lines.extend(f"- {reason}" for reason in assessment.reasons)
        if details:
            lines.append("")
            lines.append("## Notes")
            lines.append(details)
        return "\n".join(lines)
