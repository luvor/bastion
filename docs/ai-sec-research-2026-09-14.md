# Bastion AI SEC: research synthesis

Date: 2026-09-14

## Boundary

Absolute security is impossible. The target is a **fail-closed personal AI
security control plane**: no agent receives broad standing authority; every
mutation is scoped, observable, reversible where possible, and blocked or
escalated when confidence is low. The LLM is an analyst and explainer, never
the final policy authority.

The research is organized as 30 research tracks, 30 design debates, and 30
thought experiments. They are deliberately compact: each item ends in a
decision useful for Bastion rather than becoming a literature dump.

## 30 research tracks

| # | Track | Finding / Bastion consequence |
|---:|---|---|
| 1 | AI risk governance | NIST AI RMF uses Govern, Map, Measure, Manage; make these four lifecycle states explicit. |
| 2 | Agent threats | OWASP's agentic taxonomy covers goal hijack, tool misuse, identity abuse, supply chain, code execution, memory poisoning, inter-agent spoofing, cascades, trust exploitation, and rogue agents; map each to a control. |
| 3 | Prompt injection | Treat external text as hostile data; source-sink analysis matters more than a keyword filter. |
| 4 | Tool authority | Use capability-based, per-call grants; never expose a general shell when a narrow operation exists. |
| 5 | Identity | Bind actor, agent, session, tool, asset, and human approver; username-only approval is insufficient for high risk. |
| 6 | Secrets | Keep secrets outside model context and child process environments where possible; use short-lived brokered credentials. |
| 7 | Sandboxing | Run untrusted agent work rootless with no host mounts, minimal capabilities, seccomp/AppArmor, CPU/memory/time limits. |
| 8 | Egress | Default-deny network egress; approve destination, method, data class, and volume together. |
| 9 | Data loss | Add DLP/redaction at tool boundaries and before outbound transmission; block suspicious source-to-sink paths. |
| 10 | Memory | Treat long-term memory as mutable untrusted state; provenance, expiry, quarantine, and human confirmation are required. |
| 11 | MCP/A2A | Registry entries need signed identity, pinned versions, declared capabilities, permission diffs, and revocation. |
| 12 | Supply chain | Require dependency lockfiles, SBOM, vulnerability scan, signature/provenance verification, and review of new tools. |
| 13 | Runtime | Static scans miss behavior; collect process, file, network, privilege, and tool-call events continuously. |
| 14 | Policy engine | OPA/Rego is a mature policy-as-code option; Bastion can keep its Python API and optionally delegate decisions. |
| 15 | Observability | OpenTelemetry gives vendor-neutral traces, metrics, and logs; correlate every model/tool/mutation event by request ID. |
| 16 | Audit integrity | Append-only JSONL is useful locally but not tamper-proof; add hash chaining and periodic external checkpoints. |
| 17 | Recovery | A backup without a recent restore test is not a recovery control; block critical destructive actions on stale recovery posture. |
| 18 | Break-glass | Break-glass must be time-bound, narrowly scoped, separately alerted, and reviewed after use. |
| 19 | Cost | Enforce budgets before execution; cap calls, tokens, wall time, concurrency, and spend, not only dollars. |
| 20 | Availability | Kill switches and lease expiry must work if the model, network, or Bastion UI is down. |
| 21 | Change management | Policy weakening is a high-risk mutation and needs stronger approval than ordinary policy edits. |
| 22 | Detection | Prefer deterministic high-signal rules first; use an LLM for triage, clustering, and explanation. |
| 23 | Vulnerability intel | Poll vendor advisories, CVE/NVD, CISA KEV, package feeds, model/tool release notes; deduplicate into a local knowledge base. |
| 24 | Research safety | Fetch research in a quarantine worker; never let a web page's instructions alter policy or execute. |
| 25 | Red teaming | Maintain a small regression corpus for prompt injection, exfiltration, privilege escalation, destructive intent, and approval spoofing. |
| 26 | Human factors | Alert fatigue defeats security; aggregate unchanged findings and notify only on new, worsening, exploitable, or action-required state. |
| 27 | Privacy | Minimize telemetry, redact secrets/PII, encrypt state, define retention, and make local-only mode possible. |
| 28 | Platform scope | macOS personal protection and Linux/cloud runtime protection are different products; begin with declared assets and integrations. |
| 29 | Metrics | Measure blocked dangerous actions, detection latency, false positives, restore success, policy bypass attempts, and coverage. |
| 30 | Limits | Bastion cannot fix a compromised host, stolen owner account, malicious approved action, kernel exploit, or unavailable recovery. |

## 30 design debates

| # | Debate | Verdict |
|---:|---|---|
| 1 | One super-agent vs many specialists | One narrow security analyst plus deterministic workers; fewer tokens and fewer trust edges. |
| 2 | LLM firewall vs policy engine | Policy engine decides; LLM classifies/explains uncertain evidence. |
| 3 | Scan everything vs risk-based cadence | Inventory continuously; deep scan only changed or high-risk assets. |
| 4 | Cloud model vs local model | Local for sensitive triage when available; cloud only with explicit data policy and redaction. |
| 5 | Allowlist vs denylist | Allowlist capabilities at trust boundaries; denylist only as defense-in-depth. |
| 6 | Shell gateway vs structured tools | Structured tools first; shell is quarantined and heavily constrained. |
| 7 | Human approval for all vs risky only | Automatic low risk, approval for high risk, break-glass for catastrophic. |
| 8 | Live web research vs curated feeds | Curated signed feeds first; web research is quarantined evidence, never authority. |
| 9 | SQLite vs external SIEM | SQLite remains the local kernel; optional export later. |
| 10 | JSONL vs database ledger | Keep JSONL compatibility, add hash chain and SQLite index only when needed. |
| 11 | Docker vs VM | Rootless container is cheapest baseline; VM boundary for hostile code or sensitive assets. |
| 12 | Egress proxy vs no network | No network by default; narrow proxy for explicitly required destinations. |
| 13 | Automatic remediation vs recommendations | Auto-remediate only reversible, pre-approved fixes; otherwise create a plan and alert. |
| 14 | Continuous autonomous patching vs approval | Never auto-patch production by default; stage, test, approve, then deploy. |
| 15 | Full packet capture vs metadata | Metadata by default; capture content only during a bounded incident and with consent. |
| 16 | Memory convenience vs memory integrity | Integrity wins: provenance and expiry before recall. |
| 17 | Secret scanning only vs secret prevention | Prevent context/egress exposure first; scan as a backstop. |
| 18 | One global risk score vs domain scores | Keep explainable dimensions: privilege, blast radius, reversibility, confidence, cost. |
| 19 | Silent monitoring vs visible status | Quiet unchanged state, visible coverage gaps and degraded protection. |
| 20 | Alert every CVE vs exploitability | Prioritize reachable, affected, exploitable assets; still retain full inventory. |
| 21 | Signed policy vs editable config | Versioned signed policy bundle; edits create a reviewable event. |
| 22 | Central coordinator vs edge agents | Local enforcement must survive coordinator outage; central service aggregates. |
| 23 | Trust score for tools vs explicit grants | Explicit grants; scores can prioritize review but cannot authorize. |
| 24 | Token minimization vs evidence quality | Send hashes, summaries, and diffs first; fetch raw evidence only on escalation. |
| 25 | Red-team model vs production model | Separate attacker simulation from production authority and credentials. |
| 26 | Universal product vs personal profile | Build a personal profile first; generic multi-tenant policy is later work. |
| 27 | Telegram approval vs hardware-backed approval | Telegram is acceptable for medium risk; high risk needs local/hardware-bound confirmation. |
| 28 | Detect everything vs bounded coverage | Declare coverage and blind spots; measured partial defense beats false confidence. |
| 29 | Build daemon now vs CLI/cron first | Start with CLI plus launchd/cron-style scheduler; daemon adds attack surface. |
| 30 | Add more AI vs stronger boundaries | Spend the first token on deterministic controls, not a smarter watcher. |

## 30 thought experiments

| # | Scenario | Required invariant |
|---:|---|---|
| 1 | Web page tells agent to upload `.ssh` | Untrusted page cannot create an outbound capability. |
| 2 | Tool result contains fake approval | Only cryptographically bound approver identity counts. |
| 3 | Agent asks for root to install a scanner | Privilege escalation is denied or separately approved. |
| 4 | Model hallucinates a CVE | Evidence must link to an advisory and affected version. |
| 5 | Scanner itself is compromised | Scanner runs isolated and cannot weaken enforcement. |
| 6 | Policy file is edited at 03:00 | Signature/version/approval failure leaves old policy active. |
| 7 | Telegram bot token leaks | Token is scoped/rotated; high-risk approval does not depend on it alone. |
| 8 | Network disappears during mutation | Lease expiry stops further actions; partial result is logged. |
| 9 | Backup command lies | Restore test, independent location, and artifact verification gate action. |
| 10 | Agent loops 10,000 times | Per-run calls, time, concurrency, and spend caps stop it. |
| 11 | Memory says owner approved a rule | Memory is evidence, not authorization. |
| 12 | Two agents collude | Inter-agent messages are authenticated and each tool grant is independent. |
| 13 | New MCP server appears | It is quarantined until manifest, signature, permissions, and tests pass. |
| 14 | Dependency has a critical CVE | Runtime use is blocked if the affected artifact is reachable and exploitable. |
| 15 | macOS process reads browser data | OS-level permissions and data-class policy deny access. |
| 16 | Safe-looking command expands via shell substitution | Execute argv directly; do not pass through a shell by default. |
| 17 | `terraform plan` hides a destructive module | Parse the plan and inspect resource-level diff, not command verb only. |
| 18 | Human approves wrong asset | Approval screen binds exact asset, diff, hash, scope, and expiry. |
| 19 | Alert feed repeats unchanged CVE | Deduplication suppresses noise but re-alerts on severity/exploitability change. |
| 20 | Host itself is owned | Bastion reports trust failure and cannot claim local evidence is clean. |
| 21 | Cloud model receives secrets in context | Redaction and data policy block transmission before the API call. |
| 22 | Critical file changes without an agent | File/integrity watcher creates an incident independent of agent logs. |
| 23 | Audit ledger is deleted | Hash checkpoint and remote append-only copy reveal the gap. |
| 24 | Patch fixes CVE but breaks recovery | Staging, canary, health checks, and rollback gate release. |
| 25 | Owner is unavailable for a genuine outage | Pre-authorized narrow emergency playbook may run; no general break-glass. |
| 26 | Scanner costs more than the risk | Scheduler budgets itself and downgrades to hash/advisory checks. |
| 27 | A malicious PDF contains instructions | Parser output stays data; no automatic tool call follows it. |
| 28 | Agent asks to disable Bastion | Self-protection policy denies; only an owner-controlled local kill switch can change enforcement. |
| 29 | New model scores better but is untrusted | Model registry requires evaluation, pinning, permissions, and rollback. |
| 30 | Everything passes but credentials were stolen yesterday | Detection and control plane cannot guarantee past compromise; incident response remains mandatory. |

## Recommended Bastion shape

```text
sources -> inventory + hashes -> deterministic scanners -> evidence store
                                      |                         |
agent -> capability gateway -> policy/risk gate -> sandboxed action runner
                                      |                         |
                         alerts / approvals / incident capsule
                                      |
                         optional local LLM analyst
```

### Five planes

1. **Enforcement plane** — preserve the existing gateway, add structured
   capabilities, argv-only execution, leases, egress policy, and fail-closed
   defaults.
2. **Observation plane** — inventory repositories, processes, packages, models,
   tools, credentials metadata, network destinations, and policy versions;
   store hashes and provenance.
3. **Detection plane** — deterministic checks first: secrets, dependency/CVE,
   IaC, permissions, integrity, anomalous tool calls, and runtime events.
4. **Response plane** — alert, quarantine, revoke lease, rotate credential via
   an external provider, create a capsule, and suggest a reversible fix. No
   autonomous destructive remediation.
5. **Research plane** — scheduled feed ingestion and quarantined web research;
   normalize, deduplicate, score reachability, and produce a short digest.

### Token-minimal operating loop

- Every 5 minutes: cheap health/integrity deltas and gateway status.
- Hourly: changed-file, process, dependency-lock, and policy checks.
- Daily: advisory synchronization, full inventory diff, and one compact digest.
- Weekly: restore test, red-team regression corpus, policy review, and coverage report.
- LLM calls only for new/changed evidence, ambiguous findings, clustering, and
  human-readable summaries; cache by content hash and never resend unchanged
  evidence.

### Risk contract

`risk = privilege + blast_radius + irreversibility + uncertainty + data_exposure + cost`

- R0: read-only local, allow.
- R1: low-impact mutation, allow with ledger.
- R2: reversible or bounded mutation, auto-harden then allow.
- R3: sensitive/high blast radius, exact-scope human approval.
- R4: destructive/credential/policy weakening, deny by default; narrowly
  scoped break-glass with stronger approval and post-incident review.

The score never overrides a hard deny. Unknown target, unknown egress,
unknown cost, missing recovery, or unverifiable approver are fail-closed.

## Minimum viable build order

1. Add a signed/hash-chained policy and ledger format plus coverage/status CLI.
2. Add asset discovery and scheduled delta scans; keep findings local and
   deduplicated.
3. Add sandboxed read-only scanner runner with default-deny egress and resource
   limits.
4. Add source-to-sink DLP and capability grants to the gateway.
5. Add advisory ingestion and reachability-aware prioritization.
6. Add notification adapters and stronger approval identity; retain Telegram
   only for bounded risk.
7. Add restore/red-team regression checks and only then consider safe,
   reversible auto-remediation.

Do not start with a dashboard, autonomous patching, a general-purpose agent,
or a custom vector database. They add cost and attack surface before the
control invariants exist.

## Sources

- NIST AI RMF and Generative AI Profile: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Playbook: https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook
- NIST Cyber AI Profile draft: https://csrc.nist.gov/pubs/ir/8596/iprd
- OWASP Top 10 for Agentic Applications: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/
- OpenAI, designing agents to resist prompt injection: https://openai.com/index/designing-agents-to-resist-prompt-injection/
- Docker Engine security: https://docs.docker.com/engine/security/
- Docker rootless mode: https://docs.docker.com/engine/security/rootless/
- Docker seccomp: https://docs.docker.com/engine/security/seccomp/
- Open Policy Agent: https://www.openpolicyagent.org/docs
- OpenTelemetry: https://opentelemetry.io/docs/
- SLSA provenance: https://github.com/slsa-framework/slsa-github-generator
