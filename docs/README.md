# Bastion Docs

This documentation set is aimed at developers building with AI agents, not just using Bastion directly.

## Start here

- [Product Requirements Document](bastion-prd.md)
  - Full product scope, requirements, rollout, and success criteria.
- [Threat Model](threat-model.md)
  - Common failure modes for AI agents and the control layers that contain them.
- [Integration Playbook](integration-playbook.md)
  - Practical ways to put Bastion in front of tools, automations, and production paths.
- [Agent Safety Patterns](agent-safety-patterns.md)
  - Reusable design patterns for any AI builder who wants safer automation.
- [Security by Design](security-by-design.md)
  - Trust model and invariants that remain valid when the source code is public.
- [Mega AI SEC orchestration](mega-ai-sec-orchestration-2026-09-14.md)
  - 100 research tracks, 100 design debates, 100 synthetic attack experiments, and source links.

## Supporting guides

- [Contributing](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)

## Recommended reading order

1. Read the [PRD](bastion-prd.md) for the product model.
2. Read the [Threat Model](threat-model.md) to understand what Bastion is defending against.
3. Read the [Integration Playbook](integration-playbook.md) before wiring Bastion into real tools.
4. Use [Agent Safety Patterns](agent-safety-patterns.md) as a checklist for any agent project, even outside this repo.
