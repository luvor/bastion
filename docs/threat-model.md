# Bastion Threat Model

This document focuses on operational failures caused by AI-assisted execution, not on model benchmarking or generic security theory.

## The real problem

Most AI catastrophes are not caused by a model deciding to be evil. They happen because a system lets a model, agent, or automation mutate the world without a strong execution boundary.

Typical failure pattern:

1. The agent is given broad authority.
2. The task is under-specified or partially wrong.
3. The agent optimizes for completion, not reversibility.
4. Nobody checks blast radius before mutation.
5. Logging, approvals, recovery, or budgets are missing or weak.

## Threat categories

### 1. Destructive mutations

Examples:

- `terraform destroy` in the wrong workspace
- `kubectl delete` against the wrong cluster
- SQL migration with `DROP`, `TRUNCATE`, or unbounded `DELETE`
- deletion of storage buckets, snapshots, or retention policies

Controls:

- hard deny rules
- break-glass for catastrophic actions
- asset criticality tags
- backup freshness and restore-test requirements

### 2. High-blast-radius changes

Examples:

- replacing a core production service
- changing IAM or network boundaries
- mass permission updates
- changing shared infrastructure without impact awareness

Controls:

- risk scoring by environment and asset type
- explicit approvals for high-risk mutations
- incident capsules before execution
- canary and staged rollout hooks

### 3. Silent recovery failure

Examples:

- backups exist but are stale
- snapshots are in the same account and can be deleted with the primary asset
- restore path was never tested
- rollback notes exist only in a human’s head

Controls:

- asset registry
- freshness SLAs
- restore-test SLAs
- immutable or offsite backup strategy
- execution blocked when recovery posture is inadequate

### 4. Runaway cost

Examples:

- recursive agent loops
- unbounded API usage
- expensive model selection by default
- GPU or compute launches without budget checks
- parallel tasks multiplying spend unexpectedly

Controls:

- per-run caps
- per-session caps
- daily and monthly budgets
- cost-aware action classification
- approval when cost is unknown or near threshold

### 5. Bypass and policy erosion

Examples:

- agents receive direct credentials and stop going through Bastion
- exceptions accumulate until the control plane is mostly decorative
- operators bypass guardrails because prompts are noisy or too frequent
- Bastion policy can be weakened without strong review

Controls:

- no unrestricted prod credentials for agents
- mutation paths routed through Bastion
- audit of policy changes
- trust windows with expiry, not permanent carve-outs
- low-friction defaults for safe work

## System invariants

These are the conditions Bastion is designed to preserve:

- production mutation is never invisible
- catastrophic mutation is never one step away
- data protection is measured by recoverability, not backup existence
- expensive actions are bounded before execution
- risky actions leave enough evidence for immediate reconstruction

## What Bastion does not solve alone

- application correctness
- cloud account compromise
- insider abuse with already-authorized break-glass access
- business logic mistakes hidden inside a safe-looking command
- every possible class of prompt or planning failure

Bastion should be combined with:

- least-privilege IAM
- provider-native deletion protection
- CI/CD controls
- environment separation
- real monitoring and alerting

## Detection signals Bastion should care about

- destructive verbs
- production environment targets
- missing cost estimates
- missing rollback definition
- stale or missing backups
- stale restore tests
- commands affecting multiple assets or accounts
- permission or policy changes
- repetitive high-cost execution patterns

## Practical takeaway

If your AI system can mutate production without hitting an external policy gate, you do not have guardrails. You have hope.
