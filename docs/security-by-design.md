# Bastion security by design

## The core assumption

Assume the adversary has the full source code. They may know the prompts,
policy rules, file paths, alert format, scanner cadence, and integration
details. Bastion is secure only if that knowledge does not grant authority.

Public visibility can improve auditability; secrecy of implementation is not a
security boundary.

## Trust hierarchy

```text
owner identity / OS controls
          ↓
policy + capability + scope
          ↓
execution gateway
          ↓
sandbox / provider controls
          ↓
agent and model output
```

An LLM can propose a tool call, classify evidence, or explain an alert. It
cannot grant itself permission, turn an unknown into an allow, or approve its
own action.

## Invariants

1. No secret is required in Git, prompts, logs, telemetry, or Telegram.
2. Read-only is the default capability.
3. Every mutation names an actor, exact target, scope, reason, and expiry.
4. Unknown identity, destination, cost, or recovery state fails closed.
5. A compromised analyst cannot weaken enforcement.
6. A stale or missing collector status is degraded, never protected.
7. High-risk actions create evidence before execution.
8. Recovery is tested, not merely declared.
9. Updates are reviewed and pinned to a known release.
10. A local clean result never proves a previously compromised host is clean.

## Public repository policy

The repository may be public. Runtime secrets and user-specific state stay
outside Git: API keys, SSH keys, passwords, cookies, Telegram tokens, local
inventory, process/network history, incident evidence, policy overrides,
approval identities, signing keys, and release credentials.

## Cheap effective operating mode

- constant: heartbeat and cheap state checks;
- nightly: full read-only inventory and posture scan;
- on change: send only new findings to the local MBP analyst;
- weekly: restore test and adversarial regression suite;
- never: send unchanged evidence or let the model perform autonomous mutation.

## What this does not claim

Bastion is a control plane, not a magical shield. It does not replace macOS
security features, MFA, password management, backups, patching, or incident
response. It cannot guarantee safety after the host, owner account, or trusted
approval channel has already been compromised.
