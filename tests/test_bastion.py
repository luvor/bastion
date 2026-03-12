from __future__ import annotations

from datetime import datetime, timezone
import tempfile
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from bastion.approvals import NullApprovalProvider
from bastion.gateway import BastionGateway
from bastion.models import (  # noqa: E402
    ActionRequest,
    ApprovalConfig,
    ApprovalProviderType,
    Asset,
    BastionConfig,
    BudgetConfig,
    Decision,
    ProjectConfig,
    TelegramConfig,
)
from bastion.policy import PolicyEngine  # noqa: E402
from bastion.store import StateStore  # noqa: E402


class BastionTests(unittest.TestCase):
    def test_prod_critical_destroy_requires_break_glass(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = make_config(
                tmpdir,
                assets={
                    "prod-db": Asset(
                        id="prod-db",
                        env="prod",
                        tags=("critical-data", "database"),
                        backup_freshness_sla_hours=24,
                    )
                },
            )
            store = StateStore(config.project.state_dir)
            engine = PolicyEngine(config, store)
            assessment = engine.evaluate(
                ActionRequest(
                    command=["terraform", "destroy"],
                    actor="agent",
                    env="prod",
                    asset_id="prod-db",
                )
            )
            self.assertEqual(assessment.decision, Decision.BREAK_GLASS_ONLY)

    def test_budget_denies_over_per_run_cap(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = make_config(tmpdir, budgets=BudgetConfig(per_run_usd=5))
            store = StateStore(config.project.state_dir)
            engine = PolicyEngine(config, store)
            assessment = engine.evaluate(
                ActionRequest(
                    command=["docker", "run", "--gpus", "all", "trainer"],
                    actor="agent",
                    env="dev",
                    estimated_cost_usd=25,
                )
            )
            self.assertEqual(assessment.decision, Decision.DENY)

    def test_shadow_mode_does_not_execute_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            workspace = Path(tmpdir) / "workspace"
            workspace.mkdir()
            marker = workspace / "marker.txt"

            config = make_config(tmpdir)
            store = StateStore(config.project.state_dir)
            gateway = BastionGateway(
                policy=PolicyEngine(config, store),
                store=store,
                approvals=NullApprovalProvider(),
            )
            result = gateway.run(
                ActionRequest(
                    command=[sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).write_text('x')"],
                    actor="agent",
                    env="dev",
                    mode="shadow",
                    cwd=str(workspace),
                )
            )

            self.assertTrue(result.allowed)
            self.assertEqual(result.exit_code, 0)
            self.assertFalse(marker.exists())
            self.assertTrue(store.ledger_path.exists())

    def test_auto_backup_runs_before_destructive_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            asset = Asset(
                id="stage-storage",
                env="staging",
                tags=("storage",),
                backup_freshness_sla_hours=1,
                backup_command=f"{sys.executable} -c \"print('snap-stage-storage')\"",
            )
            config = make_config(tmpdir, assets={asset.id: asset})
            store = StateStore(config.project.state_dir)
            gateway = BastionGateway(
                policy=PolicyEngine(config, store),
                store=store,
                approvals=NullApprovalProvider(),
            )
            result = gateway.run(
                ActionRequest(
                    command=["rm", "-f", "missing-file.txt"],
                    actor="human",
                    actor_type="human",
                    env="staging",
                    asset_id=asset.id,
                )
            )

            self.assertEqual(result.exit_code, 0)
            self.assertEqual(result.backup_snapshot_id, "snap-stage-storage")
            backup_state = store.get_backup_status(asset)
            self.assertTrue(backup_state.fresh)

    def test_incident_capsule_created_for_high_risk_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config = make_config(
                tmpdir,
                assets={
                    "prod-db": Asset(
                        id="prod-db",
                        env="prod",
                        tags=("critical-data",),
                        backup_freshness_sla_hours=24,
                    )
                },
            )
            store = StateStore(config.project.state_dir)
            gateway = BastionGateway(
                policy=PolicyEngine(config, store),
                store=store,
                approvals=NullApprovalProvider(),
            )
            result = gateway.run(
                ActionRequest(
                    command=["terraform", "destroy"],
                    actor="agent",
                    env="prod",
                    asset_id="prod-db",
                    break_glass_reason="manual disaster recovery",
                    mode="shadow",
                )
            )

            self.assertTrue(result.incident_path)
            self.assertTrue(Path(result.incident_path).exists())


def make_config(
    root: str,
    *,
    assets: dict[str, Asset] | None = None,
    budgets: BudgetConfig | None = None,
) -> BastionConfig:
    state_dir = str(Path(root) / ".bastion")
    return BastionConfig(
        project=ProjectConfig(state_dir=state_dir),
        budgets=budgets or BudgetConfig(),
        approvals=ApprovalConfig(provider=ApprovalProviderType.NONE),
        telegram=TelegramConfig(),
        assets=assets or {},
        rules=[],
    )


if __name__ == "__main__":
    unittest.main()
