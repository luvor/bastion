# Security Policy

Bastion deals with execution control, approvals, and operational safety. Treat security bugs accordingly.

## Security model

The attacker is assumed to know the complete source tree, documentation,
policy schema, prompts, command classifier, and deployment layout. Bastion's
security must therefore come from enforced boundaries rather than obscurity.

The current alpha model is:

- collector and status work are read-only;
- AI analysis is advisory and cannot approve or execute changes;
- secrets are never intentionally placed in the repository or evidence payload;
- mutation is mediated by the gateway and policy engine;
- unknown or unverifiable conditions degrade protection instead of becoming an
  implicit allow;
- local state is operational evidence, not proof that a compromised host is clean.

This project is not yet a complete endpoint detection and response product.
It does not by itself guarantee protection from a compromised OS, stolen
account, kernel exploit, malicious approved action, or failed recovery system.

## Supported versions

This project is early-stage. The latest version on `main` is the only supported line for now.

## Reporting a vulnerability

Please do not open a public issue for vulnerabilities involving:

- approval bypass
- policy bypass
- unauthorized execution
- credential exposure
- audit tampering
- break-glass escalation flaws

Instead, use one of these paths:

- GitHub Security Advisory reporting, if enabled on the repository
- a minimal GitHub issue asking for a private contact path without including exploit details

## Scope

The highest-priority reports are:

- ways to execute prohibited actions through Bastion
- ways to weaken policy without appropriate approval
- ways to bypass audit or incident creation
- ways to exfiltrate approval credentials or secrets

## Expected hardening direction

- stronger approval identity verification
- signed or tamper-resistant audit trails
- provider-native integrations for deletion protection and recovery guarantees
- signed release artifacts and verified installation flow
- tamper-evident local evidence with independent checkpoints
- stronger Mac runtime isolation and outbound-control integration
- regression tests for prompt injection, secret exfiltration, and tool misuse

## Maintainer release rules

- Never commit `.env`, credentials, private keys, tokens, local `.bastion` state,
  or raw personal telemetry.
- Review the staged diff before every release.
- Run the unit suite and static/security checks before publishing.
- Prefer protected branches and pull requests, even for a single maintainer.
- Publish a reviewed tag/release; clients should update to that exact revision.
- Treat every policy weakening as a security-sensitive change.
