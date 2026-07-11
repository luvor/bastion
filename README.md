# Bastion

`Bastion` is a risk-aware execution gateway for AI agents, automations, and operators.

It sits between intent and mutation. Instead of trusting prompts, it enforces policy before a command can touch production data, infrastructure, or budget.

## Why this exists

Most AI-driven failures are not model failures. They are control-plane failures:

- an agent gets direct access to a dangerous tool
- nobody verifies blast radius before execution
- backups exist in theory but not in recoverable form
- cost is noticed after the loop has already burned money
- postmortems start with guessing instead of evidence

Bastion is the missing last line of defense.

## Who this is for

- AI builders wiring agents into shell, infra, databases, or cloud APIs
- founders and operators who want automation without blind trust
- teams that need a control plane between agent intent and real-world mutation

## What Bastion does

- Classifies commands before execution
- Scores risk by environment, irreversibility, blast radius, and cost
- Enforces deterministic policy instead of prompt-only guardrails
- Auto-runs safety steps such as backup hooks before destructive work
- Requires approval for high-risk actions
- Supports `break-glass` for catastrophic actions
- Records incident capsules and an audit ledger for risky execution
- Tracks budget caps across a run, session, day, and month
- Supports `shadow` mode for policy rollout without blocking work

## Design goals

- Invisible for low-risk work
- Automatic for safety work
- Strict for irreversible work
- Explicit for expensive work
- Auditable after every serious decision

If a guardrail creates the same friction for `ls` and `terraform destroy`, it is the wrong guardrail.

## Implemented in `v0.1`

- Python package targeting Python `3.9+`
- One tiny compatibility dependency on Python `<3.11`: `tomli` for TOML parsing
- CLI gateway: `bastion run`, `bastion inspect`, `bastion backup record`, `bastion ledger tail`
- Built-in command classification for shell, Terraform, Kubernetes, DB, cloud, Docker, and model-spend patterns
- Policy engine with risk ladder `R0-R4`
- Asset registry with backup freshness and restore-test SLAs
- Auto-backup hooks for destructive actions
- Approval provider: console
- Approval provider: Telegram
- Budget guard with hard caps and warning thresholds
- Incident capsules in Markdown
- JSONL audit ledger
- Unit tests and GitHub Actions workflow

## For AI builders

The docs are written to be useful even if you never adopt this code directly:

- [PRD](docs/bastion-prd.md)
- [Threat Model](docs/threat-model.md)
- [Integration Playbook](docs/integration-playbook.md)
- [Agent Safety Patterns](docs/agent-safety-patterns.md)
- [Docs Index](docs/README.md)

## Quickstart

```bash
python3 -m pip install .
# Optional: only needed for Telegram approvals
cp .env.example .env
```

Inspect a command without executing it:

```bash
bastion inspect \
  --config examples/bastion.toml \
  --actor deploy-agent \
  --env prod \
  --asset prod-db \
  -- terraform destroy
```

Run a command through Bastion:

```bash
bastion run \
  --config examples/bastion.toml \
  --actor deploy-agent \
  --env staging \
  --asset staging-app \
  -- kubectl apply -f deploy.yaml
```

Record a fresh backup or restore test:

```bash
bastion backup record --config examples/bastion.toml --asset prod-db --restore-tested
```

Review recent audit decisions:

```bash
bastion ledger tail --config examples/bastion.toml --limit 10
```

## Example: production destructive action

```bash
bastion run \
  --config examples/bastion.toml \
  --actor ops-agent \
  --env prod \
  --asset prod-db \
  --break-glass-reason "manual disaster recovery on replica" \
  -- terraform destroy
```

What happens:

1. Bastion classifies the command as destructive.
2. The asset registry marks `prod-db` as `critical-data`.
3. Bastion upgrades the decision to `BREAK_GLASS_ONLY`.
4. If a fresh backup is missing and a backup hook exists, Bastion creates one first.
5. Bastion requests approval.
6. Bastion writes an incident capsule and an audit entry before the command can proceed.

## Configuration

Minimal config example:

```toml
[project]
state_dir = ".bastion"

[budgets]
per_run_usd = 50
per_day_usd = 250
per_month_usd = 1000

[approvals]
provider = "console"

[[assets]]
id = "prod-db"
env = "prod"
tags = ["critical-data", "database"]
backup_freshness_sla_hours = 24
restore_test_sla_days = 7
deletion_protection = true
backup_command = "python3 -c \"print('snap-{asset_id}-{request_id}')\""

[[rules]]
id = "prod-destructive-needs-approval"
decision = "REQUIRE_APPROVAL"
require_backup = true
match = { envs = ["prod"], destructive = true }
```

See [examples/bastion.toml](examples/bastion.toml) for a runnable sample and [docs/bastion-prd.md](docs/bastion-prd.md) for the full product spec.

## Architecture

```text
agent / human / automation
          |
          v
    Bastion Gateway
          |
          +--> classifier
          +--> policy engine
          +--> budget guard
          +--> backup hooks
          +--> approval provider
          +--> audit ledger
          +--> incident capsule
          |
          v
   real command execution
```

## What makes Bastion different

- It protects execution, not just prompting.
- It treats recoverability as a hard requirement, not a nice-to-have.
- It models accidental spend as a production risk.
- It is designed to stay quiet during safe work and become strict only when irreversibility, blast radius, or uncertainty rises.

## Telegram approvals

Bastion can send approval requests to Telegram and wait for a reply from the allowed chat:

```bash
export BASTION_TELEGRAM_BOT_TOKEN=...
export BASTION_TELEGRAM_CHAT_ID=...
export BASTION_TELEGRAM_ALLOWED_USERNAME=your_username
```

Then set:

```toml
[approvals]
provider = "telegram"
timeout_seconds = 300
```

Reply with one of:

```text
approve <request_id>
reject <request_id>
```

## Security notes

- Bastion is strongest when agents do not hold unrestricted production credentials.
- Provider-side controls still matter. Bastion should orchestrate them, not replace them.
- `break-glass` must stay rare, logged, and time-bounded.
- Backup existence is not enough; restore verification is the real control.

## Repository hygiene

This repository intentionally excludes:

- local secrets
- `.env` values
- runtime logs
- machine-specific launch configs
- local caches

## Roadmap

- richer policy DSL
- signed approvals and stronger break-glass identity
- provider adapters for cloud-native backup and deletion protection
- policy simulation and replay against historical ledgers
- web dashboard for approvals and incident review

## Contributing and security

- [Contributing](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## License

MIT. See [LICENSE](LICENSE).
