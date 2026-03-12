# Contributing

Bastion is early. The bar is not "more features". The bar is clearer safety, better operability, and less accidental complexity.

## What to contribute

High-value contributions:

- provider adapters for real backup, deletion protection, and cost controls
- better command classification with tight tests
- policy simulation and replay tooling
- approval providers beyond console and Telegram
- stronger audit and incident storage backends
- examples for real infra or database stacks

Low-value contributions:

- vague framework churn
- abstractions without an operational use case
- cosmetic complexity that makes policy harder to reason about

## Development setup

```bash
python3 -m pip install .
python3 -m unittest discover -s tests
```

## Contribution rules

- Keep changes reversible and focused.
- Prefer plain, inspectable code over magic.
- Add or update tests when behavior changes.
- Update docs when user-facing behavior changes.
- Do not add secrets, local credentials, or machine-specific configs.

## Pull request guidance

Good pull requests usually include:

- what risk or limitation is being addressed
- why the change belongs in Bastion core rather than an external integration
- how the behavior was tested
- what new failure modes were considered

## Design standard

If a change makes safe actions slower and dangerous actions no safer, it should not land.
