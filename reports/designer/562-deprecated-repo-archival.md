# 562 — deprecated repo archival: the delete-list

designer, 2026-06-08. Working list for the psyche-directed archival pass
(*archive = `gh repo delete` the remote + `mv` the local checkout into
`~/git-archive/`*). The psyche's rule: archive deprecated repos **regardless of
whether draft code still imports them** — that importing code changes anyway
(`ax2k`/`hehp`: validity from the target, not from usage).

The one hard limit on that rule: the **production island** (deployed
`persona-spirit`, CriomOS) must not lose a remote its lockfile still pins, or
the next production rebuild can't fetch it. So the set splits by *who still
consumes it*, established by reverse-dependency grep over every active
`/git/.../Cargo.toml` plus the production `persona-spirit/Cargo.lock`.

## Method note

The fan-out classification (`wm881txfb`) mostly failed — 4 of 5 agents didn't
return (heavy tool use + schema-constrained return is unreliable; same failure
that hit the fleet port agent). Only the Mentci/samskara cluster returned (all
separate-project, nothing to archive). This list is therefore built by **direct
reverse-dep inspection**, not the scan. It covers the persona-engine deprecated
set the psyche's context points at; a completeness sweep for other dead/stub
repos is still owed.

## Tier 1 — safe to archive now (deprecated, zero active/production consumers)

| Repo | Superseded by | Evidence |
|---|---|---|
| `signal-core` | `signal-frame` + `signal-sema` | `sema-engine` already moved to signal-frame/signal-sema; no active Cargo.toml importer remains. |
| `nota-codec` | `nota-next` | importers are all archived/deprecated (`lojix-archive`, `signal-sema-upgrade`, `schema`, `signal-core`); not production-pinned. |
| `nota-derive` | `nota-next` (StructuralMacroNode) | only `nota-codec` imports it. |
| `nota-serde-archive` | `nota-next` + rkyv | old serde bridge; serde is not the inter-component wire; no checkout/importer. |
| `nota-serde-core-archive` | `nota-next` + rkyv | same; shared serde kernel snapshot. |
| `nexus-serde-archive` | `nota-next` + rkyv | same; nexus serde snapshot. |
| `sema-codegen` | `schema-rust-next` | capnp-era codegen; no checkout, no importer; oldest push (Apr 6). |
| `prism` | `schema-rust-next` | sema-records→Rust projector; no active importer. |

## Borderline — likely archive, but confirm first

| Repo | Note |
|---|---|
| `schema` | superseded by `schema-next`; only self-importer — but `active-repositories.md` flags "future runtime schema triad authority remains unsettled." |
| `nota` | "text data format grammar spec"; no importer. May be the canonical NOTA **language-spec home** rather than dead — confirm it isn't before deleting. |

## Tier 2 — deprecated, but deleting the remote now breaks the active fleet

These are genuinely deprecated, but heavily consumed by **un-migrated** active
repos including **production `persona-spirit`**. Deleting the remote forces an
immediate fleet-wide break, not a clean archive.

| Repo | Active importers | Production-pinned? |
|---|---|---|
| `signal-persona-origin` | 15 (harness, persona-spirit, signal-agent, signal-introspect, persona, signal-mind, signal-harness, signal-system, introspect, meta-signal-persona, router, terminal, signal-persona, system, signal-engine-management) | **yes** (persona-spirit Cargo.lock) |
| `signal-engine-management` | 12 (introspect, mind, meta-signal-terminal, router, persona, system, terminal, signal-harness, persona-spirit, signal-system, signal-introspect, harness) | **yes** (persona-spirit Cargo.lock) |
| `signal` | nexus, signal-forge (+ separate-project mentci) | no |
| `signal-derive` | `signal` | no |

The right sequence for Tier 2 is to archive **after** its consumers migrate off
it (the contract-localization that `signal-message`/`signal-terminal` already
did for the origin/helper vocabulary, and the `n0ss` fold of
`signal-engine-management` into `signal-persona`/`meta-signal-persona`) — i.e.
as the fleet migration lands, not before. Unless the psyche wants the break now
as a forcing function.

## Already handled

The obvious ones are already archived (`signal-executor`, `signal-persona-spirit`,
`core-signal-spirit`, `owner-signal-sema-upgrade`, `sema-upgrade`,
`schema-core`, `horizon-next`, the `*-archive` history snapshots) — 34 repos
already in the archived set.
