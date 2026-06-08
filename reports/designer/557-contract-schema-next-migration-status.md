# 557 — contract → schema-next migration status

designer, 2026-06-08. Answering "did operator migrate all the contracts to
schema-next?" The contract migration (the `signal-<component>` /
`meta-signal-<component>` crates moving from hand-written / `signal_channel!`
generation to schema-next-derived types) is a **third, distinct axis** from the
two the operator's recent work touched:

- **A — daemon shell** → emitted triad runtime (terminal, router: done/in-flight).
- **B — execution** → nexus / remove `signal-executor` (pending; `555`).
- **C — contracts** → schema-next-derived (this report).

The answer for axis C is **no — it is early, and most contracts, including the
terminal contracts the operator just built a daemon shell for, are not
migrated.**

## Method

Heuristic scan of the 40 local `signal-*` / `meta-signal-*` contract repos
under `/git/github.com/LiGoldragon`: a repo is treated as schema-next-derived
when its `Cargo.toml` depends on `schema-(rust-)next` **and** it has a generated
`src/schema/` directory; `signal_channel!` in `src` marks the old
contract-generation macro (the operator's "contract-generation debt"). The
combination is a strong indicator, not a proof — a repo could emit elsewhere —
but the headline holds across spot-checks.

## Result

Of the 40, **9 are schema-next-derived**, and **8 of those 9 are hybrids** that
still carry `signal_channel!`:

| Schema-next-derived | still has `signal_channel!`? |
|---|---|
| `signal-cloud`, `meta-signal-cloud` | yes (hybrid) |
| `signal-orchestrate`, `meta-signal-orchestrate` | yes (hybrid) |
| `signal-upgrade`, `meta-signal-upgrade` | yes (hybrid) |
| `signal-domain-criome`, `meta-signal-domain-criome` | yes (hybrid) |
| `meta-signal-router` | **no — the only cleanly-migrated contract** |

Everything else is **not** schema-next-derived. The component working/meta
contracts still on the old generation include both halves of: **terminal,
spirit, message, mind, lojix, system, harness, introspect, repository-ledger,
agent, persona, version-handover** — plus `signal-router` itself (only its
*meta* contract migrated; the working contract did not — an asymmetry worth a
second look).

(Infrastructure crates in the `signal-` namespace are not component contracts
and are out of scope for axis C: `signal-frame` (frame mechanics, keep),
`signal-sema` (classification vocabulary, keep+rename per `555`), `signal-core`
(being split/retired), `signal-derive` (macros), `signal-executor`
(deprecated/archived), `signal-engine-management`, `signal-forge`.)

## Terminal specifically

The audited slice (`556`) migrated terminal's **daemon shell** (axis A) and the
daemon now generates its own `src/schema/signal.rs` from a local
`schema/signal.schema` via `schema-rust-next`. But the **contract crates**
`signal-terminal` and `meta-signal-terminal` are **not** migrated: both still
use `signal_channel!`, have no `schema-(rust-)next` dependency, and no generated
`src/schema/`. So terminal imports the hand-written `signal_terminal::` contract
while *also* generating a parallel schema-view inside the daemon — a duplication
that the contract migration (axis C) would collapse. The operator's recent work
did not claim axis C for terminal, so this is a gap to schedule, not a
mis-statement.

## Read

Axis C is at roughly a quarter coverage and mostly hybrid. The genuinely
finished example is one half of one component (`meta-signal-router`). The
cloud / orchestrate / upgrade / domain-criome families are partway (schema-next
types alongside leftover `signal_channel!`). The bulk — terminal, spirit,
message, mind, lojix, system, harness, introspect, repository-ledger, agent,
persona, version-handover — has not started. If "migrated to schema-next" is to
become an acceptance gate the way signal-executor removal is (`555`), the same
`ng1x`/`v3um` standard applies: a contract is migrated only when
`signal_channel!` is gone and the published types are schema-derived — not when
a `.schema` file merely exists beside the hand-written crate (several
non-migrated repos already have an unused `.schema`).
