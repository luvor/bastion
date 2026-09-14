# Bastion competitive research

Scope: one private repository, one independently installed instance per Mac,
Apple Silicon, Full Disk Access, local MBP MiMo, read-only by default.

## What to borrow

| Project | What it does | Bastion should borrow |
|---|---|---|
| [Objective-See BlockBlock](https://objective-see.org/products/blockblock.html) | Watches common macOS persistence locations and alerts when a new persistent component is added. | A first-class persistence inventory and diff, not just a nightly file scan. |
| [Objective-See LuLu](https://objective-see.org/products/lulu.html) | Blocks unknown outbound connections and supports allow/block lists. | Egress findings and explicit destination approvals; do not build a network extension in v1. |
| [Objective-See KnockKnock](https://github.com/objective-see/KnockKnock) | Enumerates persistently installed software like macOS AutoRuns. | Explainable persistence report with path, signer, hash, and first-seen time. |
| [Google Santa](https://github.com/google/santa) | macOS binary and file-access authorization system. | Signed binary identity, allow/deny/quarantine states, and a local decision cache. |
| [osquery](https://github.com/osquery/osquery) | Exposes process, file, and macOS Endpoint Security event data through queryable tables. | Structured evidence packets and event-driven deltas; use osquery when installed, do not duplicate its whole schema. |
| [Promptfoo](https://www.promptfoo.dev/docs/red-team/quickstart/) | Red-teams AI apps for injections, jailbreaks, RAG poisoning, and custom policies. | A tiny pinned regression corpus for Bastion/MiMo and agent/tool integrations. |
| [OPA](https://www.openpolicyagent.org/docs) | Policy-as-code engine that evaluates structured input. | Keep hard decisions deterministic and versioned; consider OPA only after Python rules become a bottleneck. |
| [Docker rootless/seccomp](https://docs.docker.com/engine/security/rootless/) | Reduces daemon/container privilege and restricts system calls. | Run hostile scanner/research jobs rootless, no host mounts, bounded resources, and no network by default. |
| [Apple Gatekeeper](https://support.apple.com/en-hk/guide/security/sec5599b66df/web) | Checks signatures, notarization, alteration, and download provenance. | Treat signer/notarization as evidence in risk scoring, never as a complete trust decision. |

## What not to copy

- Do not reimplement an antivirus engine.
- Do not install a kernel/system extension for the first milestone.
- Do not give MiMo raw secrets or unrestricted shell access.
- Do not auto-block every unknown process; this creates alert fatigue and self-inflicted outages.
- Do not make a dashboard before the collector, policy, evidence, and alert loop works.
- Do not use Telegram emoji as the security control; it is only a fast visual signal.
- Do not run downloaded research code on the protected Mac.

## Best combined product

`BlockBlock-style persistence + LuLu-style egress evidence + Santa-style binary identity + osquery-style events + Promptfoo-style AI regression + Bastion policy/audit/approval.`

That combination is a personal AI security control plane, not a claim of full
EDR equivalence. The native macOS security stack remains the base layer.

## First vertical slice

1. A signed, read-only Mac collector.
2. Inventory: LaunchAgents, LaunchDaemons, applications, packages, shell
   profiles, SSH metadata, Keychain metadata, firewall/FileVault/Gatekeeper
   state, and recent network destinations.
3. Hash-based state and finding deduplication.
4. Nightly `launchd` scan plus cheap heartbeat.
5. Telegram alerts with `🛡️ BASTION SECURITY` prefix and severity symbols.
6. Native menu-bar status: protected, scanning, attention, or protection
   degraded — derived only from actual collector state.
7. MiMo receives only redacted new findings and returns classification and
   explanation; it cannot approve or execute changes.

The mascot is a UX layer over this state machine. It must never display
"protected" when the collector is stale, permissions are missing, the ledger
is unwritable, or the last scan failed.
