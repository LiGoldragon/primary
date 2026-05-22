# 290 - Persona ARCH diff suggestions for operator (post-/287 distribution)

*Designer report for the operator. Persona was the one repo skipped in the
/287 → ARCH distribution wave (subagent dispatched per spirit record 221)
because operator had six files in flight in the persona working copy. This
report carries the proposed diff for `persona/ARCHITECTURE.md` so the
operator can fold the edits into their next commit cycle when their
in-flight work settles.*

## TL;DR

`persona/ARCHITECTURE.md` §1.6.7 already covers persona-as-upgrade-orchestrator
substance (records 208, 209, 210) — including the four-socket model, manager
messages, quarantine gate, and a sequence-diagram of the protocol drive. The
gaps vs /287 substance are vocabulary normalization and contract-naming —
small additions, no large structural rewrite needed.

## §1 Proposed additions

### §1.A — Name `owner-signal-version-handover` as the contract behind §1.6.7's owner-socket operations

Current state (§1.6.7 "Manager messages"): the table lists `HandleOwnerVersionHandover`
dispatching `AttemptHandover` / `ForceFlip` / `Rollback` / `Quarantine` as
Kameo-internal operations. The wire contract these come from is **not named**.

Diff (add to §1.6.7 above the "Manager messages" table, or as a
sub-paragraph after it):

```markdown
**Owner contract.** The administrative operations Persona receives on its
owner socket — `AttemptHandover`, `ForceFlip`, `Rollback`, `Quarantine` —
are carried by the `owner-signal-version-handover` contract crate (per
intent record 214). The contract is signal-only: no daemon code, no
storage. Persona's manager owns the dispatch from
`HandleOwnerVersionHandover` into the four operation handlers above.
```

Why: record 214 explicitly creates `owner-signal-version-handover` as the
home for these operations; without naming it in persona ARCH, a reader can't
trace from the Kameo message dispatch to the wire contract.

### §1.B — Vocabulary normalization to "main / next" (record 181)

Current state: `src/upgrade.rs` socket paths use `current_*` /
`next_*` (e.g. `current_owner_socket_path`, `current_upgrade_socket_path`).
The ARCH table inherits this naming.

Per spirit record 181, canonical workspace vocabulary is **"main / next"**.

Diff: optional rename in the ARCH text. Source code naming is operator's
call (Rust field names may stay if the cost of renaming outweighs the
inconsistency); the ARCH text uses "main / next" canonically when
referring to the version pair conceptually, and parenthesizes
the field names as historical artifacts:

```markdown
| Socket | Used by |
|---|---|
| `current_owner_socket_path` (the **main** version's owner socket) | Recorded for audit; ... |
| `current_upgrade_socket_path` (the **main** version's private upgrade socket) | Persona's `HandoverDriver` opens a client to this path and walks ... |
| `next_owner_socket_path` (the **next** version's owner socket) | Recorded for audit; ... |
| `next_upgrade_socket_path` (the **next** version's private upgrade socket) | Recorded for audit; ... |
```

Alternative: rename Rust fields `current_*` → `main_*` in `src/upgrade.rs`
(plus matching test/struct names) and remove the parenthetical. Operator's
call on whether to do the rename — the smart-handover code is the canonical
worked example for the workspace, and naming consistency helps future
agents map between ARCH and code.

### §1.C — Reference `VersionProjection` + `CommitSequence` as the upstream pieces

Current state: §1.6.7 explains Persona's drive of the protocol but doesn't
name **why** the protocol needs `commit_sequence` (the database high-water
mark for replay) or `VersionProjection` (the per-type conversion trait
the next daemon uses to project records during the state copy).

Diff: add a short paragraph in §1.6.7 just before the mermaid sequence
diagram:

```markdown
**Upstream pieces.** The handover protocol Persona drives depends on two
upstream contracts/crates. (1) The next daemon uses `VersionProjection`
(in the `version-projection` crate, peer to `signal-sema`) to project
each record from main's schema into next's schema as it copies state.
(2) The marker exchanged in `AskHandoverMarker` / `ReadyToHandover`
carries the source-side `commit_sequence` (the durable per-database
monotonic write counter in `sema-engine`); this is the high-water mark
that lets next replay deltas N+1 forward without losing in-flight
writes during the copy window.
```

Why: a reader of persona ARCH should be able to trace from "Persona drives
the handover" to "what mechanisms make this possible." Today the trace
stops at the wire; this diff carries it to the trait + storage layer.

### §1.D — Cross-reference §1.6.7 sequence diagram with /287 §3

The sequence diagram in §1.6.7 (lines 510-533, `actor psyche` driving
through Persona owner socket) is **operationally complete** — it shows
Persona-as-orchestrator + driver + store events + target current upgrade
socket. The /287 §3 sequence diagram is **conceptually focused** — it
shows the Current ↔ Next exchange directly, with Persona as a single
participant at the top.

These are two valid views; no contradiction. No diff proposed —
documenting that they coexist and complement.

## §2 Contradictions found

**None blocking.** §1.6.7 is consistent with /287 substance. The persona
ARCH was written WITH records 208/209/210 in mind (the section's opening
paragraph cites them explicitly).

Minor framing nit, not a contradiction: §1.6.6 "Engine-level migration"
explicitly notes that ordinary component upgrades go through §1.6.7
(not engine-level migration); this is correct per /287 + records 208/209/210
and shouldn't be touched.

## §3 What this diff is NOT proposing

- No structural rewrite of §1.6.7 (the section's shape is sound).
- No new sections (the gaps are small additions inside §1.6.7).
- No changes to §1.5 (Engine Manager Model), §1.6.1-1.6.6 (filesystem
  ACL trust, ConnectionClass, channel choreography, owner sockets,
  cross-engine routes, engine-level migration as substrate). These
  layers are upstream of the upgrade orchestration and stand
  independently.
- No source-code-side renames (operator's call on `current_*` → `main_*`
  in `src/upgrade.rs`).

## §4 Recommended operator workflow

When operator's six in-flight files settle (`ARCHITECTURE.md`,
`TESTS.md`, `flake.nix`, `src/manager.rs`, `src/upgrade.rs`,
`tests/manager.rs`):

1. Apply the §1.A diff (`owner-signal-version-handover` contract naming).
2. Decide on the §1.B vocabulary normalization — text-only or full
   Rust-side rename. If the latter, batch with the source edits in
   the same commit.
3. Apply the §1.C diff (`VersionProjection` + `CommitSequence` upstream
   pieces paragraph).
4. Commit the ARCH edits separately from the implementation changes
   (per `~/primary/skills/jj.md` standard flow — one commit per
   logical change).

## §5 Bead pickup

Designer files a bead pointing operator at this report. The bead closes
when the §1.A / §1.B / §1.C edits land in `persona/ARCHITECTURE.md` and
the persona repo is committed + pushed.

## See also

- `~/primary/reports/designer/287-version-handover-component-explained.md` — the canonical visual reference
- `~/primary/reports/designer/289-arch-distribution-from-287-2026-05-22.md` — the cross-repo distribution wave (five other repos already done)
- `~/primary/reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md` — the canonical spec
- Spirit records 181 (main/next vocabulary), 208, 209, 210, 214 (owner-signal-version-handover), 221 (this distribution wave)
- `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md` §1.6.7 — the section being amended
