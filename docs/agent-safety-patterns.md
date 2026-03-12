# Agent Safety Patterns

These patterns are useful even if you never deploy Bastion itself. They are the core habits behind safer AI-assisted systems.

## 1. Execution gateway, not prompt-only guardrails

Prompt rules are soft. Execution rules are real.

Bad pattern:

- "Never touch production unless I say so."

Better pattern:

- the agent cannot mutate production except through a gateway that checks policy

## 2. Risk-based friction

Do not make the same control path for `cat README.md` and `drop database`.

Good pattern:

- low-risk actions pass automatically
- medium-risk actions get auto-hardened
- high-risk actions require approval
- catastrophic actions require break-glass

## 3. Recoverability as a first-class control

A backup is not protection if nobody can restore it.

Good pattern:

- tag critical assets
- define backup freshness SLAs
- define restore-test SLAs
- block risky mutations when recovery posture is weak

## 4. Budget before execution, not after

Cost alerts that fire after the run are accounting, not guardrails.

Good pattern:

- estimate cost before execution when possible
- cap per run, per session, per day, per month
- escalate when cost is unknown

## 5. Incident capsules by default

When something goes wrong, you want a reconstruction packet, not a scavenger hunt.

Good pattern:

- actor
- target
- command
- risk
- policy decision
- approvals
- backups
- result

## 6. Shadow mode before enforcement

Most guardrail systems fail because they are too noisy on day one.

Good pattern:

- observe first
- study false positives
- then enforce the clearly catastrophic classes

## 7. Trust windows instead of permanent exceptions

Operators need speed sometimes. That does not justify permanent holes in policy.

Good pattern:

- scoped approvals
- short expiry
- audit trail

## 8. Protect the protector

If the guardrail system can be weakened casually, it will be.

Good pattern:

- log policy edits
- require stronger approval for weakening controls
- test policies before activation

## Checklist for AI builders

- Can the agent mutate production without an external gate?
- Do you know which assets are critical?
- Can a human approve risky actions in one short step?
- Are backups fresh enough to meet your real RPO?
- Have restores been tested recently?
- Can one loop blow your monthly budget?
- Can you reconstruct a risky action from logs alone?

If too many answers are "no", you do not need a smarter model first. You need a stronger control plane.
