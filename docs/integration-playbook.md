# Bastion Integration Playbook

This guide is for builders who want to adopt Bastion concepts in a real stack with minimal ceremony.

## Integration order

Do not start by protecting everything at once.

Recommended sequence:

1. Put Bastion in front of obviously destructive commands.
2. Turn on shadow mode and collect decisions.
3. Add hard-deny rules for catastrophic classes.
4. Add backup and recovery preconditions.
5. Add approval flows for `R3` actions.
6. Add budget controls and anomaly thresholds.

## Good first integration targets

- Terraform apply and destroy
- Kubernetes apply, delete, scale, and rollout commands
- database migration runners
- ad hoc SQL execution
- cloud CLI actions
- expensive model or compute invocation wrappers

## Deployment patterns

### Pattern A. Local CLI gateway

Best for:

- solo builders
- dev tools
- experimentation

Shape:

- developers and local agents call `bastion run -- ...`
- Bastion wraps command execution
- local state is stored in `.bastion/`

Tradeoff:

- fastest to adopt
- easiest to bypass unless credentials are also constrained

### Pattern B. CI/CD execution gate

Best for:

- infra changes
- deployment pipelines
- scheduled automations

Shape:

- pipeline jobs call Bastion before mutations
- approvals route to Telegram or another channel
- audit trail is captured in one place

Tradeoff:

- stronger control
- slower iteration for purely local work

### Pattern C. Agent tool proxy

Best for:

- autonomous or semi-autonomous agent systems
- long-running task executors

Shape:

- agent tools call Bastion adapters instead of raw shell or raw APIs
- agents never see unrestricted production credentials
- Bastion becomes the execution boundary, not an optional helper

Tradeoff:

- best protection model
- requires more deliberate integration

## Minimal production setup

If you want the smallest setup that is still serious, use this:

- separate prod credentials from dev credentials
- agents only get Bastion-mediated access
- critical assets are tagged in the config
- destructive prod actions require backup freshness checks
- `R3` actions require human approval
- `R4` actions require break-glass
- incident capsules and ledger are retained

## Practical policy design advice

- Keep hard rules small and obvious.
- Put heuristics behind `REQUIRE_APPROVAL`, not behind `DENY`, until you have baseline data.
- Treat unknown cost as a real risk.
- Prefer automatic safety steps before human interruption.
- Keep approvals short enough that a human can answer in under 10 seconds.

## Rollout mistakes to avoid

- Starting in hard-enforcement mode everywhere on day one
- Requiring approval for routine read-only work
- Treating backups as present-or-absent instead of fresh-or-recoverable
- Leaving agents with direct production credentials "just in case"
- Adding permanent exceptions instead of time-bounded trust windows

## Suggested first milestone

If you only have one weekend:

1. Protect `terraform destroy`, destructive SQL, and bucket deletion.
2. Add a small asset registry for your critical data systems.
3. Require a recent backup before risky data mutations.
4. Send approvals to a place you actually read.
5. Log every risky action with its reason and actor.

That alone is already better than most agent setups.
