# Security Policy

Bastion deals with execution control, approvals, and operational safety. Treat security bugs accordingly.

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
