# Skills Role Aliases — 2026-08-06

## Ruling

The skills repo's closed permission×depth role matrix is extended with
a new axis: **orchestrator aliases**. These are named roles consumed by
external orchestrators (e.g. Codex's built-in `default`, `explorer`,
`worker`) that map to existing depth tiers rather than defining their
own model/effort settings.

Mappings ruled for Codex V1 orchestrator:
- `default` → ordinary (gpt-5.6-luna, xhigh)
- `explorer` → ordinary (gpt-5.6-luna, xhigh)
- `worker` → demanding (gpt-5.6-terra, high)

The generator is extended to emit these alias files alongside the
cross-product agents. The Nix-managed duplicates in CriomOS-home
(lines 37–72 and 718–720 of `modules/home/profiles/min/default.nix`,
plus the enforcement check in `checks/ai-agent-launch-orchestration/`)
are removed once the skills repo delivers them.

## Context

Agent text: "Two options: 1. Extend the generator with a new axis for
Codex orchestrator roles (aliases that reference existing depth tiers)
— clean but changes the architecture. 2. Static files outside the
pipeline — quick but fights the repo's own principles."

Psyche chose option 1.
