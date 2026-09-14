# Bastion mega AI SEC / CyberSec orchestration

Date: 2026-09-14

## Honest scope

This artifact is a 100/100/100 research and red-team program. The 100 research items are bounded questions with source directions, not 100 fabricated claims of completed deep research. The debates are decisions to settle. The experiments are synthetic local attack hypotheses. No live target, credential, production system, destructive action, or external scan is allowed.

## Agent roles

| Role | Responsibility |
|---|---|
| Lead architect | owns invariants and rejects untestable claims |
| Threat researcher | maps primary sources and recent incidents |
| Mac endpoint engineer | owns Apple Silicon, TCC, launchd, EndpointSecurity |
| AI security engineer | owns prompt, memory, tools and model boundaries |
| Detection engineer | owns telemetry, baseline, diff and severity |
| Identity engineer | owns capabilities, leases, approvals and MFA |
| Supply-chain engineer | owns SBOM, signatures, CI and releases |
| Privacy engineer | owns redaction, retention and local-only mode |
| Incident responder | owns containment, recovery and evidence |
| Red-team operator | attacks only synthetic local fixtures |
| Blue-team reviewer | checks that every finding is reproducible |
| Cost engineer | owns token, call, runtime and alert budgets |
| UX guardian | ensures mascot never lies about status |
| Release guardian | owns tests, tags, rollback and branch policy |
| Skeptic | tries to falsify every security claim |
| Integrator | reviews patches and runs acceptance checks |

## Orchestration contract

```text
research -> source verification -> threat model -> debate -> architecture -> synthetic attack -> patch -> regression -> release evidence
```

Every result must include source/fixture, boundary, precondition, expected control, observed result, severity, and regression test. Agent output is evidence for review, never authorization.

## 100 research tracks

| # | Research track | Expected output |
|---:|---|---|
| 1 | goal hijack | AI agent threats — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 2 | tool misuse | AI agent threats — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 3 | identity abuse | AI agent threats — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 4 | supply-chain poisoning | AI agent threats — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 5 | unexpected code execution | AI agent threats — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 6 | memory poisoning | AI agent threats — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 7 | inter-agent spoofing | AI agent threats — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 8 | cascading failure | AI agent threats — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 9 | human trust exploitation | AI agent threats — SLSA — define one enforceable invariant and one measurable test. |
| 10 | rogue behavior | AI agent threats — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 11 | direct injection | Prompt and context — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 12 | indirect web injection | Prompt and context — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 13 | email injection | Prompt and context — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 14 | PDF/image metadata | Prompt and context — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 15 | Unicode/HTML hiding | Prompt and context — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 16 | system prompt leakage | Prompt and context — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 17 | context boundary | Prompt and context — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 18 | instruction hierarchy | Prompt and context — SLSA — define one enforceable invariant and one measurable test. |
| 19 | model-output injection | Prompt and context — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 20 | Lies-in-the-Loop | Prompt and context — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 21 | Apple Silicon boot chain | Mac platform — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 22 | Secure Enclave/SKP | Mac platform — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 23 | FileVault | Mac platform — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 24 | SIP/SSV | Mac platform — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 25 | Gatekeeper | Mac platform — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 26 | XProtect | Mac platform — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 27 | TCC/FDA | Mac platform — SLSA — define one enforceable invariant and one measurable test. |
| 28 | Keychain | Mac platform — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 29 | launchd | Mac platform — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 30 | EndpointSecurity | Mac platform — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 31 | process ancestry | Endpoint telemetry — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 32 | exec events | Endpoint telemetry — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 33 | file create/write | Endpoint telemetry — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 34 | rename/unlink | Endpoint telemetry — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 35 | login items | Endpoint telemetry — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 36 | system extensions | Endpoint telemetry — SLSA — define one enforceable invariant and one measurable test. |
| 37 | listening ports | Endpoint telemetry — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 38 | outbound connections | Endpoint telemetry — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 39 | Unified Log | Endpoint telemetry — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 40 | browser extensions | Endpoint telemetry — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 41 | password manager | Identity and secrets — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 42 | passkeys | Identity and secrets — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 43 | hardware MFA | Identity and secrets — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 44 | OAuth scopes | Identity and secrets — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 45 | short-lived tokens | Identity and secrets — SLSA — define one enforceable invariant and one measurable test. |
| 46 | SSH agents | Identity and secrets — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 47 | API keys | Identity and secrets — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 48 | secret redaction | Identity and secrets — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 49 | credential rotation | Identity and secrets — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 50 | approval identity | Identity and secrets — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 51 | rootless sandbox | Isolation and network — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 52 | seccomp | Isolation and network — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 53 | VM boundary | Isolation and network — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 54 | resource quotas | Isolation and network — SLSA — define one enforceable invariant and one measurable test. |
| 55 | default-deny egress | Isolation and network — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 56 | DNS metadata | Isolation and network — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 57 | HTTP destination | Isolation and network — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 58 | localhost IPC | Isolation and network — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 59 | Unix sockets | Isolation and network — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 60 | network extensions | Isolation and network — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 61 | lockfiles | Supply chain — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 62 | SBOM | Supply chain — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 63 | provenance | Supply chain — SLSA — define one enforceable invariant and one measurable test. |
| 64 | artifact signatures | Supply chain — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 65 | GitHub Actions | Supply chain — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 66 | branch protection | Supply chain — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 67 | Dependabot | Supply chain — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 68 | CodeQL | Supply chain — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 69 | dependency review | Supply chain — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 70 | rollback | Supply chain — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 71 | capabilities | Policy and recovery — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 72 | least privilege | Policy and recovery — SLSA — define one enforceable invariant and one measurable test. |
| 73 | risk dimensions | Policy and recovery — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 74 | hard deny | Policy and recovery — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 75 | leases | Policy and recovery — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 76 | nonces | Policy and recovery — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 77 | break-glass | Policy and recovery — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 78 | backup freshness | Policy and recovery — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 79 | restore tests | Policy and recovery — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 80 | incident capsules | Policy and recovery — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 81 | nightly schedule | Operations and economics — SLSA — define one enforceable invariant and one measurable test. |
| 82 | event-driven deltas | Operations and economics — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 83 | token cache | Operations and economics — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 84 | LLM routing | Operations and economics — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 85 | alert deduplication | Operations and economics — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 86 | retention | Operations and economics — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 87 | privacy budget | Operations and economics — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 88 | coverage health | Operations and economics — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 89 | false positives | Operations and economics — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 90 | MTTD metrics | Operations and economics — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 91 | EchoLeak pattern | Cases and validation — OPA/OpenTelemetry — define one enforceable invariant and one measurable test. |
| 92 | malicious MCP content | Cases and validation — NIST AI RMF — define one enforceable invariant and one measurable test. |
| 93 | fake approval dialog | Cases and validation — OWASP Agentic Top 10 — define one enforceable invariant and one measurable test. |
| 94 | RAG poisoning | Cases and validation — OWASP AI Agent Cheat Sheet — define one enforceable invariant and one measurable test. |
| 95 | credential exfiltration | Cases and validation — OpenAI agent safety — define one enforceable invariant and one measurable test. |
| 96 | agent loop | Cases and validation — Apple Platform Security — define one enforceable invariant and one measurable test. |
| 97 | confused deputy | Cases and validation — Apple EndpointSecurity — define one enforceable invariant and one measurable test. |
| 98 | unsigned tool | Cases and validation — CISA OSS guidance — define one enforceable invariant and one measurable test. |
| 99 | stale clean status | Cases and validation — GitHub security guidance — define one enforceable invariant and one measurable test. |
| 100 | compromised host | Cases and validation — SLSA — define one enforceable invariant and one measurable test. |

## 100 debates

| # | Debate / provisional verdict |
|---:|---|
| 1 | goal hijack: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 2 | tool misuse: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 3 | identity abuse: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 4 | supply-chain poisoning: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 5 | unexpected code execution: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 6 | memory poisoning: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 7 | inter-agent spoofing: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 8 | cascading failure: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 9 | human trust exploitation: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 10 | rogue behavior: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 11 | direct injection: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 12 | indirect web injection: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 13 | email injection: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 14 | PDF/image metadata: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 15 | Unicode/HTML hiding: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 16 | system prompt leakage: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 17 | context boundary: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 18 | instruction hierarchy: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 19 | model-output injection: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 20 | Lies-in-the-Loop: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 21 | Apple Silicon boot chain: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 22 | Secure Enclave/SKP: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 23 | FileVault: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 24 | SIP/SSV: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 25 | Gatekeeper: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 26 | XProtect: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 27 | TCC/FDA: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 28 | Keychain: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 29 | launchd: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 30 | EndpointSecurity: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 31 | process ancestry: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 32 | exec events: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 33 | file create/write: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 34 | rename/unlink: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 35 | login items: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 36 | system extensions: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 37 | listening ports: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 38 | outbound connections: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 39 | Unified Log: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 40 | browser extensions: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 41 | password manager: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 42 | passkeys: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 43 | hardware MFA: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 44 | OAuth scopes: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 45 | short-lived tokens: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 46 | SSH agents: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 47 | API keys: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 48 | secret redaction: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 49 | credential rotation: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 50 | approval identity: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 51 | rootless sandbox: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 52 | seccomp: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 53 | VM boundary: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 54 | resource quotas: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 55 | default-deny egress: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 56 | DNS metadata: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 57 | HTTP destination: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 58 | localhost IPC: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 59 | Unix sockets: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 60 | network extensions: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 61 | lockfiles: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 62 | SBOM: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 63 | provenance: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 64 | artifact signatures: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 65 | GitHub Actions: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 66 | branch protection: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 67 | Dependabot: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 68 | CodeQL: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 69 | dependency review: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 70 | rollback: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 71 | capabilities: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 72 | least privilege: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 73 | risk dimensions: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 74 | hard deny: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 75 | leases: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 76 | nonces: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 77 | break-glass: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 78 | backup freshness: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 79 | restore tests: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 80 | incident capsules: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 81 | nightly schedule: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 82 | event-driven deltas: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 83 | token cache: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 84 | LLM routing: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 85 | alert deduplication: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 86 | retention: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 87 | privacy budget: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 88 | coverage health: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 89 | false positives: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 90 | MTTD metrics: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 91 | EchoLeak pattern: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 92 | malicious MCP content: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 93 | fake approval dialog: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 94 | RAG poisoning: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 95 | credential exfiltration: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 96 | agent loop: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 97 | confused deputy: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 98 | unsigned tool: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 99 | stale clean status: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |
| 100 | compromised host: maximize coverage or minimize privilege? Verdict: choose the smallest control that blocks the dangerous sink; expose coverage gaps. |

## 100 thought experiments

| # | Synthetic experiment / expected invariant |
|---:|---|
| 1 | Synthetic goal hijack attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 2 | Synthetic tool misuse attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 3 | Synthetic identity abuse attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 4 | Synthetic supply-chain poisoning attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 5 | Synthetic unexpected code execution attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 6 | Synthetic memory poisoning attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 7 | Synthetic inter-agent spoofing attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 8 | Synthetic cascading failure attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 9 | Synthetic human trust exploitation attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 10 | Synthetic rogue behavior attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 11 | Synthetic direct injection attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 12 | Synthetic indirect web injection attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 13 | Synthetic email injection attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 14 | Synthetic PDF/image metadata attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 15 | Synthetic Unicode/HTML hiding attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 16 | Synthetic system prompt leakage attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 17 | Synthetic context boundary attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 18 | Synthetic instruction hierarchy attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 19 | Synthetic model-output injection attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 20 | Synthetic Lies-in-the-Loop attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 21 | Synthetic Apple Silicon boot chain attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 22 | Synthetic Secure Enclave/SKP attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 23 | Synthetic FileVault attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 24 | Synthetic SIP/SSV attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 25 | Synthetic Gatekeeper attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 26 | Synthetic XProtect attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 27 | Synthetic TCC/FDA attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 28 | Synthetic Keychain attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 29 | Synthetic launchd attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 30 | Synthetic EndpointSecurity attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 31 | Synthetic process ancestry attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 32 | Synthetic exec events attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 33 | Synthetic file create/write attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 34 | Synthetic rename/unlink attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 35 | Synthetic login items attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 36 | Synthetic system extensions attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 37 | Synthetic listening ports attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 38 | Synthetic outbound connections attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 39 | Synthetic Unified Log attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 40 | Synthetic browser extensions attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 41 | Synthetic password manager attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 42 | Synthetic passkeys attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 43 | Synthetic hardware MFA attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 44 | Synthetic OAuth scopes attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 45 | Synthetic short-lived tokens attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 46 | Synthetic SSH agents attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 47 | Synthetic API keys attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 48 | Synthetic secret redaction attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 49 | Synthetic credential rotation attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 50 | Synthetic approval identity attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 51 | Synthetic rootless sandbox attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 52 | Synthetic seccomp attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 53 | Synthetic VM boundary attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 54 | Synthetic resource quotas attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 55 | Synthetic default-deny egress attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 56 | Synthetic DNS metadata attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 57 | Synthetic HTTP destination attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 58 | Synthetic localhost IPC attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 59 | Synthetic Unix sockets attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 60 | Synthetic network extensions attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 61 | Synthetic lockfiles attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 62 | Synthetic SBOM attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 63 | Synthetic provenance attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 64 | Synthetic artifact signatures attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 65 | Synthetic GitHub Actions attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 66 | Synthetic branch protection attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 67 | Synthetic Dependabot attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 68 | Synthetic CodeQL attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 69 | Synthetic dependency review attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 70 | Synthetic rollback attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 71 | Synthetic capabilities attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 72 | Synthetic least privilege attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 73 | Synthetic risk dimensions attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 74 | Synthetic hard deny attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 75 | Synthetic leases attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 76 | Synthetic nonces attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 77 | Synthetic break-glass attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 78 | Synthetic backup freshness attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 79 | Synthetic restore tests attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 80 | Synthetic incident capsules attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 81 | Synthetic nightly schedule attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 82 | Synthetic event-driven deltas attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 83 | Synthetic token cache attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 84 | Synthetic LLM routing attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 85 | Synthetic alert deduplication attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 86 | Synthetic retention attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 87 | Synthetic privacy budget attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 88 | Synthetic coverage health attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 89 | Synthetic false positives attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 90 | Synthetic MTTD metrics attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 91 | Synthetic EchoLeak pattern attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 92 | Synthetic malicious MCP content attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 93 | Synthetic fake approval dialog attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 94 | Synthetic RAG poisoning attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 95 | Synthetic credential exfiltration attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 96 | Synthetic agent loop attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 97 | Synthetic confused deputy attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 98 | Synthetic unsigned tool attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 99 | Synthetic stale clean status attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |
| 100 | Synthetic compromised host attack: attacker knows the code and supplies hostile input. Expected: no secret access, no unapproved mutation, evidence recorded, and degraded status when uncertain. |

## Recent attack patterns to model

- EchoLeak-style indirect prompt injection: external content attempts to move sensitive context to an attacker-controlled sink.
- Public GitHub/MCP content: hidden Unicode, HTML, Markdown, issue and PR text tries to influence an agent.
- Lies-in-the-Loop: attacker-controlled content manipulates the approval dialog or action description.
- Excessive agency: a read-only integration also exposes send/write functionality.
- Memory poisoning: hostile content persists and changes future agent behavior.
- Tool/supply-chain poisoning: a new server or dependency expands permissions or executes unexpected code.
- Rogue/cascading agent behavior: repeated calls multiply cost and blast radius.

These are defensive patterns, not exploit recipes.

## Safe self-pentest status

The local adversarial pass already found and fixed three issues:

1. Unknown commands such as `sh -c` now require R3 approval instead of receiving low-friction treatment.
2. `curl --data` no longer enters the read-only path.
3. Shadow mode logs without executing or requesting approval.

The regression suite now has 10 tests. Next additions should cover approval replay, action-digest mismatch, redacted evidence, tamper-evident ledger, and stale status.

## Target by design

- Assume complete source-code knowledge.
- Keep secrets outside Git, prompts, logs, telemetry, and Telegram.
- Treat the model as an untrusted planner.
- Make read-only the default.
- Make unknown identity, destination, scope, cost, or recovery fail closed.
- Separate collector, analyst, approval, and enforcement processes.
- Let a compromised analyst fail to weaken enforcement.
- Make mascot and Telegram status derive only from verified state.
- Prefer native macOS controls and mature tools over reimplementation.
- Publish blind spots and evidence with every security claim.

## Primary sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST Cyber AI Profile](https://csrc.nist.gov/pubs/ir/8596/iprd)
- [OWASP Agentic Top 10](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/)
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [OWASP Lies-in-the-Loop](https://community.owasp.org/attacks/Lies_in_the_Loop)
- [OpenAI prompt-injection guidance](https://openai.com/index/designing-agents-to-resist-prompt-injection/)
- [Apple Platform Security](https://support.apple.com/guide/security/welcome/web)
- [Apple EndpointSecurity](https://developer.apple.com/documentation/endpointsecurity)
- [Apple System Extensions](https://developer.apple.com/system-extensions/)
- [Objective-See BlockBlock](https://objective-see.org/products/blockblock.html)
- [Objective-See LuLu](https://objective-see.org/products/lulu.html)
- [North Pole Santa](https://github.com/northpolesec/santa)
- [osquery](https://github.com/osquery/osquery)
- [CISA OSS guidance](https://www.cisa.gov/news-events/news/cisa-government-and-industry-partners-publish-fact-sheet-organizations-using-open-source-software)
- [GitHub security recommendations](https://opensource.google/documentation/reference/github/security)
- [SLSA](https://slsa.dev/)

