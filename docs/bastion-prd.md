# Bastion PRD

Status: Draft v1  
Date: 2026-03-12  
Owner: Bastion project  
Related components: Telegram approvals, agent runtime, cloud/tool adapters

## 1. Product Summary

`Bastion` is a risk-aware execution gateway for AI agents, automations, and humans. Its job is to prevent catastrophic outcomes caused by oversight, over-trust, hidden risk, runaway automation, or missing recovery paths, without becoming a general-purpose blocker to everyday work.

`Bastion` is not a smarter advisor. It is an enforceable control plane.

Core idea:

- Low-risk work should pass with near-zero friction.
- Medium-risk work should be auto-hardened by default.
- High-risk work should require clear, short human approval.
- Catastrophic work should be denied unless explicitly escalated through break-glass.

The target outcome is not "perfect safety". The target outcome is:

- catastrophic actions become rare
- damage radius becomes bounded
- recovery becomes reliable
- cost overruns become hard to trigger by accident
- post-incident forensics become obvious instead of speculative

## 2. Problem Statement

AI agents can move too fast, act on incomplete context, overfit to a prompt, misunderstand blast radius, or execute a technically valid action that is operationally dangerous.

The main failure modes Bastion must prevent:

- Data loss from destructive operations
- Irreversible infrastructure changes in production
- Silent deletion of backups, snapshots, or rollback paths
- Dangerous permission escalation
- Expensive runaway loops, model misuse, or resource over-provisioning
- Agent actions that bypass logging, oversight, or change review
- Overconfident execution under uncertainty
- Slow or confused incident reconstruction after something goes wrong

The current gap in most agent systems is not intelligence. It is the lack of an independent last line of defense between "agent intent" and "real world mutation".

## 3. Product Vision

Bastion should feel like a seatbelt and airbag, not a parking brake.

The ideal user experience:

- The user barely notices Bastion during safe work.
- Bastion steps in automatically when it can reduce risk without user attention.
- Bastion asks for approval only when the action is genuinely dangerous, expensive, irreversible, or uncertain.
- When an incident happens, Bastion leaves a complete evidence trail and recovery context automatically.

## 4. Users And Jobs To Be Done

### Primary users

- Solo founder / operator running agents close to production
- Developer using AI agents for code, infra, migrations, or ops
- AI automation owner running scheduled or event-driven tasks

### Secondary users

- Auditor / future teammate reviewing incidents or policy changes
- On-call operator responding to alerts or approving risky actions

### Jobs to be done

- "Let agents move quickly without letting them silently destroy something important."
- "Catch the dangerous action before it lands, not after."
- "Make sure I can recover what matters."
- "Make sure one dumb loop cannot burn my budget."
- "If something bad happens, tell me exactly what happened and why."

## 5. Product Principles

1. Bastion is external to the agent's reasoning loop.
2. Policies are deterministic and enforceable, not prompt-level suggestions.
3. Risk controls should be proportional to irreversibility and blast radius.
4. Bastion should prefer automatic safety actions over asking the user.
5. Production mutations must never bypass Bastion.
6. Bastion must not be able to silently weaken its own protections.
7. Recovery quality matters as much as prevention quality.
8. Read-only and low-risk work should remain fast.
9. Humans should spend attention only on decisions that justify it.
10. Unknown cost or unknown blast radius should be treated as risk, not ignored.

## 6. Goals

### Primary goals

- Prevent catastrophic data loss
- Prevent irreversible production mistakes
- Prevent accidental high-cost runs
- Preserve operator velocity for low-risk work
- Guarantee tamper-evident audit trails for risky actions
- Guarantee precondition checks for risky mutations

### Success criteria

- High-severity incidents caused by agent execution trend toward zero
- Time-to-detect risky execution is near-real-time
- Recovery paths exist and are validated for critical assets
- False-positive approval prompts remain low enough that users do not route around Bastion
- Direct-to-prod mutations outside Bastion trend toward zero
- At least 90% of `R0/R1` actions pass without human interruption after baseline tuning
- 100% of `R3+` actions create an audit record and incident capsule
- 100% of `R4` production mutations are blocked or forced through break-glass
- Critical-asset backup freshness compliance stays above 95%
- Median approval delivery time stays under 10 seconds on the primary channel

## 7. Non-Goals

- Replacing code review, CI, or cloud-native security tooling
- Solving all security problems
- Fully understanding arbitrary business impact without operator-defined context
- Acting as a general chat assistant
- Blocking every risky action absolutely; break-glass will remain possible

## 8. Core Conceptual Model

Every requested action is evaluated as:

`intent + context + blast radius + reversibility + uncertainty + cost = policy decision`

Possible decisions:

- `ALLOW`
- `ALLOW_WITH_LOG`
- `AUTO_HARDEN_AND_ALLOW`
- `REQUIRE_APPROVAL`
- `DEFER_UNTIL_PRECONDITIONS`
- `DENY`
- `BREAK_GLASS_ONLY`

## 9. Risk Model

### Risk dimensions

- Environment sensitivity: `local`, `dev`, `staging`, `prod`
- Mutation class: `read`, `write`, `delete`, `replace`, `permission`, `spend`
- Asset criticality: data-bearing, customer-facing, security boundary, cost-heavy
- Reversibility: instant rollback, partial rollback, unclear rollback, no rollback
- Blast radius: single object, service, namespace, account, region
- Confidence: exact plan known vs inferred from intent
- Timing: business hours vs unattended window
- Novelty: common pattern vs first-time pattern
- Budget impact: bounded vs unknown vs high

### Risk ladder

- `R0`: safe, low blast radius, reversible, bounded cost
- `R1`: low risk, observable, reversible, standard pattern
- `R2`: moderate risk, requires auto-hardening before execution
- `R3`: high risk, human approval required
- `R4`: catastrophic or policy-prohibited, denied unless break-glass

### Example mappings

- Read-only log query in prod: `R0`
- Staging deploy with health checks: `R1`
- Prod deploy with canary and rollback: `R2`
- SQL migration that drops columns in prod: `R3`
- Destroying a production database or backup vault: `R4`
- Launching unknown-cost GPU fleet from an agent loop: `R3` or `R4`

## 10. Anti-Friction Strategy

Bastion must not become "approval theater".

### Rules

- Do not ask for approval if automation can remove the risk first.
- Do not interrupt for read-only work.
- Do not interrupt for low-cost, low-blast-radius actions in safe environments.
- Ask only when the operator is the correct bottleneck.
- Show one decision, not a wall of text.
- Allow time-boxed trust windows for repeated safe operations within the same task.
- Learn normal baselines before tightening prompts and thresholds.

### Preferred order of intervention

1. Log only
2. Warn only
3. Auto-run dry run / plan
4. Auto-create backup / snapshot / checkpoint
5. Auto-enable canary / rate limit / spend cap
6. Ask for approval
7. Deny

## 11. Functional Requirements

### FR1. Mandatory execution gateway

Bastion must sit between actor and mutating tools.

- Agents do not receive unrestricted production credentials.
- Mutating actions are routed through Bastion adapters.
- Supported initial surfaces:
  - shell wrappers
  - infrastructure tools
  - database migration runners
  - cloud APIs
  - deployment APIs
  - model/provider usage APIs for cost enforcement

### FR2. Action classification

Bastion must classify requested actions before execution.

- Parse structured plans when available
- Detect destructive verbs and replace operations
- Identify target assets and environment
- Detect permission changes and policy changes
- Estimate blast radius and irreversibility

### FR3. Risk scoring and policy evaluation

Bastion must score and evaluate every mutating action.

- Deterministic policy engine
- Support static deny-lists and dynamic thresholds
- Separate hard policies from tunable heuristics
- Unknown or partial context must increase risk

### FR4. Automatic safety actions

Before high-risk mutations, Bastion should automatically perform relevant safety steps where possible.

- Create backup, snapshot, or export
- Require dry-run or plan
- Enable canary
- Set temporary rate/concurrency caps
- Capture dependency and impact summary
- Verify rollback path

### FR5. Approval system

For `R3` actions, Bastion must request a clear approval with concise context.

Approval payload must include:

- what will change
- where it will change
- why the action is risky
- what backup was created
- what rollback path exists
- expected cost impact
- expiration time for approval

Approval channels for initial version:

- Telegram

Future channels:

- Slack
- email
- web dashboard

### FR6. Break-glass workflow

For `R4` actions, Bastion must default to deny and require explicit emergency override.

Break-glass requirements:

- explicit operator intent
- short-lived override token
- stronger authentication than ordinary approval
- mandatory reason capture
- mandatory incident capsule and post-action review

### FR7. Backup and recovery assurance

Bastion must reason about recoverability, not just existence of backups.

For critical assets, Bastion must track:

- backup freshness
- backup scope
- backup location
- immutability status
- last successful restore test
- recovery objective tags

For risky data mutations, Bastion should deny or defer if recovery posture is inadequate.

### FR8. Spend guard

Bastion must prevent accidental overspend at multiple levels.

- per action budget
- per session budget
- per agent daily budget
- per project monthly budget
- concurrency caps
- runtime caps
- token caps
- model allowlists / deny-lists
- provider/resource-type allowlists

If estimated cost is unavailable, Bastion should treat that as elevated risk.

### FR9. Incident capsule

For every `R3+` action, Bastion must automatically create an incident capsule before execution.

Contents:

- action intent
- actor and origin
- timestamp
- target assets
- policy decision
- backup/checkpoint identifiers
- rollback path
- approval record
- execution result

If the action fails or causes alerts, Bastion should post a concise incident note automatically.

### FR10. Audit ledger

Bastion must maintain tamper-evident logs for risky actions and policy changes.

Track:

- action requests
- plan summaries
- decisions
- approvals
- break-glass events
- policy edits
- bypass attempts

### FR11. Self-protection

Bastion must guard against its own weakening.

- Bastion cannot disable its hard deny rules without stronger approval
- Bastion cannot silently exempt itself from audit
- Changes to Bastion policy, credentials, or allowlists are `R3` or `R4`
- Bastion must test policy changes before activation

### FR12. Shadow mode and simulation

Bastion must support non-blocking rollout.

- Observe actions without blocking
- Produce "would have blocked" reports
- Replay historical actions against new policies
- Compare false-positive and false-negative rates

## 12. Non-Functional Requirements

### Reliability

- Bastion must not become a hidden single point of failure for low-risk work
- Safe degraded modes must be defined
- Production mutation paths should fail closed when Bastion is unavailable
- Read-only paths may fail open

### Performance

- Low-risk decision latency target: under 1 second
- High-risk pre-execution decision target: under 5 seconds before async safety actions
- Approval requests should arrive in under 10 seconds

### Security

- Least-privilege credentials
- Short-lived scoped tokens where possible
- Separate trust boundary from agent runtime
- Encrypted storage for secrets and audit data

### Observability

- structured logs
- metrics
- traces for execution pipeline
- policy-decision inspection tooling

### Usability

- concise human prompts
- predictable decision categories
- explainable decisions
- minimal repetitive confirmation

## 13. Core User Flows

### Flow A. Safe work

1. Agent requests low-risk action
2. Bastion classifies as `R0/R1`
3. Bastion logs and allows
4. User sees no interruption

### Flow B. Guarded work

1. Agent requests moderate-risk action
2. Bastion classifies as `R2`
3. Bastion runs auto-hardening: plan, backup, rate cap, canary, or similar
4. Bastion allows after safeguards pass
5. User sees optional summary, no required approval

### Flow C. Approval-required work

1. Agent requests high-risk action
2. Bastion classifies as `R3`
3. Bastion prepares evidence, backup, and rollback context
4. Bastion sends approval request
5. User approves, rejects, or times out
6. Bastion executes or aborts

### Flow D. Break-glass work

1. Operator requests prohibited or catastrophic action
2. Bastion classifies as `R4`
3. Bastion denies by default
4. Operator enters break-glass with stronger intent and expiry
5. Bastion records reason and raises incident visibility
6. Action proceeds only inside limited emergency window

## 14. Policy Model

Policies should be stored as code and support:

- actor scopes
- environment scopes
- action scopes
- target asset tags
- risk thresholds
- required preconditions
- automated safety actions
- approval requirements
- hard denies
- trust-window exceptions with expiry

### Example policy shape

```yaml
rules:
  - id: deny-prod-db-destroy
    when:
      env: prod
      action: [db.drop, db.destroy, terraform.destroy]
      target_tags: [critical-data]
    decision: BREAK_GLASS_ONLY

  - id: require-backup-before-prod-migration
    when:
      env: prod
      action: [db.migrate]
      effects: [drop_column, delete_rows, replace_table]
    require:
      - backup_freshness_hours <= 24
      - restore_test_age_days <= 7
      - rollback_defined == true
      - human_approval == true

  - id: cap-agent-spend
    when:
      actor_type: agent
      estimated_cost_usd: ">=100"
    decision: REQUIRE_APPROVAL
```

## 15. What Bastion Must Block By Default

- Destruction of production data stores
- Destruction or disabling of backups, snapshots, retention, audit, or monitoring
- Permission escalation to broad admin scopes without approval
- Untracked mutations outside the gateway
- Deletion with unknown blast radius
- Unknown-cost execution above configured thresholds
- Policy changes that weaken Bastion controls without stronger review

## 16. Data Protection Strategy

For critical assets, Bastion should maintain an asset registry with:

- data classification
- owner
- environment
- RPO
- RTO
- backup method
- restore method
- last restore verification
- deletion protection state

Backup policy should distinguish:

- operational backups for fast restore
- offsite backups for disaster recovery
- immutable backups for sabotage resistance

The system is not "safe" unless restore is regularly validated.

## 17. Cost Protection Strategy

Bastion should treat cost as a first-class risk category, not a reporting afterthought.

### Cost controls

- Budget envelopes at run, day, month, and project levels
- Hard provider caps where supported
- Soft warnings before hard thresholds
- Concurrency limits
- Runtime limits
- Tool invocation limits
- Model usage limits
- Resource-type restrictions for autonomous agents
- Anomaly detection against recent baseline

### Cost policies by actor

- Research agent: low budget, read-mostly, no infra mutations
- Coding agent: medium budget, test/staging writes allowed
- Deploy/ops agent: low frequency, higher scrutiny, higher approval burden
- Batch automation: strict schedule and bounded concurrency

## 18. Current Repo Fit

The current repository already has:

- Telegram messaging
- a supervisor persona layer
- Python runtime suitable for a lightweight first version

That makes the following MVP path realistic:

- Python-based Bastion service or library
- Telegram approval and alert channel
- local JSON or SQLite state initially
- shell/tool wrappers for first integrations
- policy files in the repo

## 19. MVP Scope

### In scope

- Policy engine with static and dynamic rules
- Action classifier for shell, infra, DB, and cost-related actions
- Telegram approval workflow
- Incident capsule generation
- Audit logging
- Backup-precondition checks
- Basic spend caps and run/session budgets
- Shadow mode

### Out of scope for MVP

- Full cloud-agnostic abstraction across every provider
- Rich web UI
- Deep semantic understanding of arbitrary business context
- Autonomous incident remediation beyond simple playbooks

### MVP acceptance criteria

- Bastion can intercept and classify a defined first set of mutating actions
- Bastion can block at least one critical destructive class end-to-end
- Bastion can request and record Telegram approvals for `R3` actions
- Bastion can create and persist an incident capsule for every `R3+` action
- Bastion can enforce at least one backup precondition before a risky mutation
- Bastion can enforce at least one hard budget threshold and stop execution
- Bastion supports shadow mode and reports "would have blocked" outcomes
- Bastion policy changes are versioned and auditable

## 20. Rollout Plan

### Phase 0. Observe

- Shadow mode only
- No blocking
- Collect action patterns, risk labels, and false-positive candidates

### Phase 1. Hard-deny catastrophic classes

- Block obvious `R4` actions
- Require Bastion for production mutations
- Start incident capsules

### Phase 2. Auto-hardening

- Add backup checks
- Add dry-run enforcement
- Add canary and rate-cap helpers

### Phase 3. Approval workflows

- Introduce `R3` approvals via Telegram
- Add trust windows and expiry-based exceptions

### Phase 4. Cost guard and baselines

- Session budgets
- Daily and monthly budgets
- anomaly detection

### Phase 5. Recovery assurance

- Restore drill tracking
- asset registry completeness
- periodic policy simulation

## 21. Metrics

### Safety metrics

- count of blocked `R4` actions
- count of approved `R3` actions
- number of risky actions executed without required preconditions
- time from risky request to approval or denial
- backup freshness compliance rate
- restore test freshness compliance rate

### Velocity metrics

- percent of actions that pass without interruption
- median latency added by Bastion for `R0/R1`
- approval prompt rate per day
- approval fatigue signals: reject rate, timeout rate, bypass attempts

### Cost metrics

- avoided spend from blocked or capped runs
- number of budget threshold crossings
- anomaly detection lead time

## 22. Failure Modes And Degraded Behavior

### Bastion unavailable

- Read-only actions: may fail open or fall back depending on policy
- Dev/staging mutations: configurable, default fail open with audit warning
- Production mutations: fail closed

### Approval channel unavailable

- `R0-R2`: continue
- `R3`: queue or deny depending on expiry and policy
- `R4`: deny

### Backup system unavailable

- Safe actions continue
- Risky data mutations defer or deny

### Cost estimation unavailable

- Treat unknown cost as elevated risk
- escalate to approval above defined thresholds

## 23. Abuse And Bypass Resistance

Bastion must assume agents and operators will sometimes try to route around friction.

Controls:

- no standing unrestricted prod credentials for agents
- mutation APIs routed only through Bastion
- explicit detection of out-of-band changes where possible
- alerts on bypass attempts
- policy tests for loopholes

## 24. Open Questions

- Which production surfaces matter first: cloud infra, DB, deployments, or AI spend?
- Which provider-native controls already exist and should Bastion orchestrate rather than replace?
- What is the preferred persistent store for audit and policy state in v1?
- Which actions require two-person approval instead of one-person approval?
- What exact break-glass identity proof is acceptable?

## 25. Final Product Requirement Statement

Bastion must make catastrophic AI-assisted mistakes materially harder to execute than safe work.

It should do this by being:

- invisible for low-risk work
- automatic for safety work
- strict for irreversible work
- explicit for expensive work
- unforgiving about missing recovery paths
- auditable after every serious decision

If Bastion creates the same amount of friction for harmless actions and catastrophic actions, it has failed.

If Bastion can be bypassed silently, it has failed.

If Bastion prevents damage but leaves no recovery context, it has failed.

If Bastion keeps velocity high while making catastrophic mistakes rare, bounded, recoverable, and obvious, it has done its job.
