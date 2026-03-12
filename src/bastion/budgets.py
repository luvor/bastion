from __future__ import annotations

from .models import ActionRequest, BudgetConfig, BudgetStatus, Decision
from .store import StateStore


def evaluate_budget(
    config: BudgetConfig,
    store: StateStore,
    request: ActionRequest,
    *,
    unknown_cost: bool,
) -> BudgetStatus:
    totals = store.spend_totals(request.session_id)
    estimated = request.estimated_cost_usd
    status = BudgetStatus(estimated_cost_usd=estimated)

    if estimated is None:
        if unknown_cost:
            status.allowed = False
            status.decision = Decision.REQUIRE_APPROVAL
            status.reasons.append("Command can spend money, but estimated cost is unknown.")
        return status

    status.session_total_after_usd = totals["session"] + estimated
    status.day_total_after_usd = totals["day"] + estimated
    status.month_total_after_usd = totals["month"] + estimated

    if config.per_run_usd is not None and estimated > config.per_run_usd:
        status.allowed = False
        status.decision = Decision.DENY
        status.reasons.append(
            f"Estimated cost ${estimated:.2f} exceeds per-run cap ${config.per_run_usd:.2f}."
        )
        return status

    if config.per_session_usd is not None and status.session_total_after_usd > config.per_session_usd:
        status.allowed = False
        status.decision = Decision.DENY
        status.reasons.append(
            f"Session spend would reach ${status.session_total_after_usd:.2f}, above cap ${config.per_session_usd:.2f}."
        )
        return status

    if config.per_day_usd is not None and status.day_total_after_usd > config.per_day_usd:
        status.allowed = False
        status.decision = Decision.DENY
        status.reasons.append(
            f"Daily spend would reach ${status.day_total_after_usd:.2f}, above cap ${config.per_day_usd:.2f}."
        )
        return status

    if config.per_month_usd is not None and status.month_total_after_usd > config.per_month_usd:
        status.allowed = False
        status.decision = Decision.DENY
        status.reasons.append(
            f"Monthly spend would reach ${status.month_total_after_usd:.2f}, above cap ${config.per_month_usd:.2f}."
        )
        return status

    warn_reasons: list[str] = []
    if config.per_day_usd is not None and status.day_total_after_usd is not None:
        if status.day_total_after_usd >= config.per_day_usd * config.warn_at_ratio:
            warn_reasons.append(
                f"Daily spend would reach ${status.day_total_after_usd:.2f} of ${config.per_day_usd:.2f}."
            )
    if config.per_month_usd is not None and status.month_total_after_usd is not None:
        if status.month_total_after_usd >= config.per_month_usd * config.warn_at_ratio:
            warn_reasons.append(
                f"Monthly spend would reach ${status.month_total_after_usd:.2f} of ${config.per_month_usd:.2f}."
            )
    if warn_reasons:
        status.allowed = False
        status.decision = Decision.REQUIRE_APPROVAL
        status.reasons.extend(warn_reasons)

    return status
