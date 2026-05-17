# orchestrate — Rust rewrite design

*Operator design report. The Rust port of `tools/orchestrate` with a
typed Nota role registry. Lands the workspace-coordination helper on
the same craft surface as every other Rust binary in the workspace,
and stages the eventual cutover to the `mind` CLI.*

Date: 2026-05-17

Author: second-designer-assistant

---

## TL;DR

`tools/orchestrate` is a 250-line bash script that reads a flat
`orchestrate/roles.list` and reads/writes per-lane lock files at
`orchestrate/<lane>.lock`. This report specifies the Rust rewrite
operator should implement: a typed crate that reads
`orchestrate/roles.nota` (typed Nota record per `nota-codec`),
exposes the same CLI surface (`claim`, `release`, `status`), and
writes the same lock-file format the shell helper produces. Existing
agents continue to invoke `tools/orchestrate` as today — the
behavior is preserved bit-for-bit; the implementation is the
substitution.

The rewrite is **the bridge** between today's shell helper and the
eventual `mind` CLI destination in `orchestrate/AGENTS.md`
§"Command-line mind target." After this rewrite lands, the next
move (out of scope for this report) is folding orchestrate vocabulary
into `signal-persona-mind` request/reply records, at which point
`tools/orchestrate` becomes a thin translator over `mind '<NOTA>'`.

---

## Current state (what operator inherits)

After report 1 of this lane and the migration that followed, the
workspace has:

| Surface | Path | Shape |
|---|---|---|
| Protocol doc | `orchestrate/AGENTS.md` | The canonical orchestration protocol. |
| Lock files | `orchestrate/<lane>.lock` | Plain-text per-lane state. Eleven files. |
| Role registry | `orchestrate/roles.list` | Bash-readable interim. One lane per line; optional `assistant-of:<main>` metadata. |
| Tool | `tools/orchestrate` | Bash. Reads `roles.list`, writes lock files, checks overlap, prints status. |
| Meta-skill | `skills/role-lanes.md` | How lane stacking works. |
| Tracking | `.beads/` | BEADS, transitional. |

The shell helper's role-list externalisation (commit
`81f5262fb149` and successor) is **the interim**. The Rust rewrite
replaces both the role-reading code and the lock-file manipulation.

---

## End-state design

### Crate layout

A new crate in the workspace's micro-component shape. Suggested
home and name:

- **Repo:** `github:LiGoldragon/orchestrate-cli` (or whatever
  the operator chooses; one-capability/one-crate per
  `skills/micro-components.md`).
- **Crate name:** `orchestrate-cli`.
- **Binary name:** `orchestrate` (no `-daemon` suffix — this is an
  interactive CLI per `lore/AGENTS.md` §"Binary naming").
- **Library half:** `orchestrate` (per `lore/AGENTS.md`
  `[lib] name = "<crate>"`).

The workspace continues to invoke the binary at `tools/orchestrate`.
The path is a symlink or thin shell wrapper that calls the Rust
binary; agents see no path change. Operator chooses the wiring
(direct path, Nix-installed binary, etc.).

### Configuration surface — `orchestrate/roles.nota`

`orchestrate/roles.nota` is a typed Nota record read on tool startup.
Worked example (target shape — pin via examples-first round-trip per
`skills/contract-repo.md`):

```nota
(Roles
  (MainRole operator)
  (MainRole designer)
  (MainRole system-specialist)
  (MainRole poet)
  (AssistantLane operator-assistant            assistant-of:operator)
  (AssistantLane second-operator-assistant     assistant-of:operator)
  (AssistantLane designer-assistant            assistant-of:designer)
  (AssistantLane second-designer-assistant     assistant-of:designer)
  (AssistantLane system-assistant              assistant-of:system-specialist)
  (AssistantLane second-system-assistant       assistant-of:system-specialist)
  (AssistantLane poet-assistant                assistant-of:poet))
```

(Designer reserves the right to revise the record shape — names,
field positions — through the contract-crate review. Operator
treats this as the proposed shape; the falsifiable form lands as a
test in the contract crate.)

### Typed records — request/reply

The CLI invocations decode into one Request record; the binary
prints one Reply record (matching the `mind` CLI shape and the
workspace's "one object in, one object out" rule).

```nota
# tools/orchestrate claim designer-assistant /home/li/primary/skills/foo.md -- "skill edit"
(Request
  (Claim designer-assistant
    (Scope /home/li/primary/skills/foo.md)
    "skill edit"))

# tools/orchestrate release designer-assistant
(Request (Release designer-assistant))

# tools/orchestrate status
(Request Status)

# Reply on success
(Reply (Claimed designer-assistant
         (Scopes /home/li/primary/skills/foo.md)
         (Conflicts)))

# Reply on overlap
(Reply (ClaimRejected designer-assistant
         (Overlap (Scope /home/li/primary/skills/foo.md)
                  (Held-by designer))))
```

These are the **proposed** records. Designer specifies the typed
shape; operator can land the falsifiable round-trip test
(`tests/<name>.rs`) in the contract crate before implementing the
behavior, per `skills/contract-repo.md` §"Examples-first round-trip
discipline."

### Lock-file format — preserved

The on-disk lock-file format stays exactly as the shell helper
writes it today, so concurrent agents and historical state remain
readable across the cutover:

- Plain text. Each line is one scope, optionally `<scope> # <reason>`.
- Empty file = idle lane.
- `<scope>` is either an absolute path or a bracketed task token
  (`[primary-f99]`).

The Rust binary parses, writes, and validates this format. The
shape lives in `orchestrate/AGENTS.md` §"Lock-file format" — the
authoritative reference.

### Typed errors — per-crate enum

Per `skills/rust/errors.md`: one `Error` enum for `orchestrate-cli`,
with `#[from]` conversions for foreign types. No `anyhow`, no
`Box<dyn Error>`. Variants name the failure modes:

- `UnknownLane(String)`
- `LockReadFailed { path: PathBuf, source: io::Error }`
- `NotaParseFailed { path: PathBuf, source: nota_codec::Error }`
- `ClaimOverlap { lane: LaneName, scope: Scope, held_by: LaneName }`
- `BeadsScopeForbidden(PathBuf)`
- … etc.

### Tests — Nix-backed

Per `skills/testing.md`:

- **Pure check** — Nota round-trip for `roles.nota`, request/reply
  records, lock-file parsing.
- **Stateful runner** — claim/release sequences exercised against
  a tempfile-rooted workspace; named flake output for inspection.
- **Chained derivation** (if applicable) — a smoke test that
  spawns the binary against a fake workspace and validates the
  end-to-end behavior.

Every test runs under `nix flake check` or a named flake output.

### Actor-system shape — defer if it stays one-shot

The current shell helper is one-shot: invoke, read state, write
state, exit. If the Rust rewrite preserves the one-shot CLI shape
(strong recommendation: keep it one-shot), no actor topology is
needed. If a long-lived daemon emerges (e.g. for inotify-driven
status), `skills/actor-systems.md` and `skills/kameo.md` apply at
that point.

---

## What changes for agents

**Nothing visible at the invocation surface.** The same commands
work:

```sh
tools/orchestrate claim <lane> <scope> [more-scopes] -- <reason>
tools/orchestrate release <lane>
tools/orchestrate status
```

The same lock-file format, the same role list (now typed), the
same overlap-detection rules. Agents continue invoking
`tools/orchestrate`; the implementation behind the path is the only
substitution.

The opportunity (out of scope for this report, but worth naming):
**better diagnostics**. The shell's overlap error today is
single-line:

> `Conflict: /home/li/primary/skills/foo.md overlaps /home/li/primary/skills (held by designer)`

A typed Rust implementation can surface the full picture — which
peer holds, what their reason is, the BEADS task they're working
— in a structured Reply record that the caller can format. Worth a
follow-up design conversation once the rewrite has landed.

---

## Out of scope — named explicitly

This rewrite is the bridge. It is **not**:

- **The `mind` CLI absorption.** Per `orchestrate/AGENTS.md`
  §"Command-line mind target", orchestrate vocabulary eventually
  becomes part of `signal-persona-mind`. That cutover is a
  separate, later move. After this Rust rewrite lands,
  `tools/orchestrate` can become a thin wrapper over
  `mind '<one NOTA record>'` invocations once the mind CLI
  implements the orchestrate verbs.
- **BEADS replacement.** `.beads/` and the `bd` command stay as-is.
  The Rust binary continues to call `bd --readonly list --status open`
  for the status output (or equivalent), the same way the shell does.
- **Lock-file format evolution.** The on-disk format is preserved
  exactly. If we want richer state (claim timestamps, agent
  identifiers), that's a separate design report and a coordinated
  migration.
- **Workspace path changes.** `tools/orchestrate` stays at that
  path. Lock files stay at `orchestrate/<lane>.lock`. Role
  registry stays at `orchestrate/roles.nota` (after this rewrite
  lands; `roles.list` retires).

---

## Operator checklist

Suggested order; operator decides the actual sequencing.

1. **Repo + skeleton.** Create `orchestrate-cli` repo with the
   workspace's standard layout (per `skills/rust/crate-layout.md`,
   `lore/rust/nix-packaging.md`). Land `ARCHITECTURE.md`, `AGENTS.md`
   shim, `skills.md`, `flake.nix`.
2. **Contract crate.** If a separate contract crate is warranted
   for the Request/Reply vocabulary, follow
   `skills/contract-repo.md`. Otherwise the records live in the
   main crate's `signal` module.
3. **Falsifiable specs.** Land the Nota round-trip tests for
   `roles.nota` and the Request/Reply records *first*, per
   `skills/contract-repo.md` §"Examples-first round-trip
   discipline."
4. **Lock-file parser/writer.** Implement and test against
   existing fixtures (the current `orchestrate/<lane>.lock` files
   are real-world examples).
5. **Role registry loader.** Read `orchestrate/roles.nota`.
   Validate every `AssistantLane` declares an `assistant-of`
   that's a declared `MainRole`.
6. **Overlap detection.** Path-nesting + task-token exact-match,
   matching the shell helper's `scopes_overlap` semantics
   (see current `tools/orchestrate` §`scopes_overlap`).
7. **CLI dispatch.** `claim` / `release` / `status` subcommands
   parse argv into Request records, then dispatch. (One CLI verb
   per Request variant, matching the workspace's Nota-CLI shape.)
8. **BEADS bridge.** `status` calls `bd --readonly list --status
   open --flat --no-pager --limit 20` and includes the output;
   `.beads/` claim attempts produce the existing rejection.
9. **Migration commit.** Replace the shell `tools/orchestrate` with
   a symlink to (or thin wrapper over) the Rust binary. Delete
   `orchestrate/roles.list`. Update `skills/role-lanes.md` to
   reference `roles.nota` as the live registry. Verify agents
   invoking `tools/orchestrate` see no change.
10. **Falsifiable witness.** A test that runs the Rust binary
    against a fixture workspace and asserts the lock files have
    the expected format (architectural-truth test per
    `skills/architectural-truth-tests.md`).

---

## Acceptance criteria

- `tools/orchestrate` invocations from agents produce the same
  lock-file contents and overlap-detection behavior as today.
- `orchestrate/roles.nota` is read on every invocation; adding a
  new lane requires only editing that file (plus creating the
  report subdirectory, per `skills/role-lanes.md`).
- All Nota records round-trip via `nota-codec`.
- Errors are typed per crate; no `anyhow` or `Box<dyn Error>` at
  any boundary.
- Tests pass under `nix flake check`.
- The binary respects the existing `.beads/` "never claim"
  invariant.
- `skills/role-lanes.md` is updated to reference `roles.nota`
  instead of `roles.list`.
- A follow-up commit removes `orchestrate/roles.list`.

---

## Why now — and why not just wait for mind

The shell helper has served well. Two pressures argue for the
rewrite over continuing to extend the shell:

1. **Adding a lane is currently a four-place edit.** Even with
   the role list externalised, the bash script's overlap-detection,
   usage string, and BEADS bridge each carry assumptions that need
   re-checking when the surface evolves. A typed Rust implementation
   reduces the surface to one config edit + one test addition.
2. **The shell can't read Nota.** The interim `roles.list` works,
   but every other typed surface in the workspace (lojix-cli's
   FullOs request, signal-persona-mind, …) is Nota. Keeping
   orchestrate on a flat-text registry sits sideways to the
   workspace's discipline.

Argument for waiting: **the `mind` CLI is the destination**, and
this rewrite is a bridge. The bridge has a cost. But the bridge
lands now-shape on the right surface; the mind CLI's orchestrate
absorption is a later contract conversation that benefits from
having the Rust shape already in place. The bridge crate becomes
the proving ground for the typed orchestrate vocabulary the mind
CLI eventually adopts.

---

## See also

- this workspace's `orchestrate/AGENTS.md` — the orchestration
  protocol the binary implements; §"Command-line mind target"
  for the eventual cutover.
- this workspace's `skills/role-lanes.md` — the lane mechanism;
  references `orchestrate/roles.list` today, `roles.nota` after
  this rewrite.
- this workspace's `tools/orchestrate` — the bash helper to be
  replaced.
- this workspace's `orchestrate/roles.list` — the interim role
  registry; retired by step 9 above.
- this workspace's `skills/rust/methods.md`,
  `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`,
  `skills/rust/parsers.md`, `skills/rust/crate-layout.md` — the
  Rust craft toolkit.
- this workspace's `skills/contract-repo.md` —
  examples-first round-trip discipline.
- this workspace's `skills/micro-components.md` — one capability,
  one crate, one repo.
- this workspace's `skills/testing.md` — Nix-backed pure /
  stateful / chained tests.
- `reports/second-designer-assistant/1-role-skill-consolidation-survey-2026-05-17.md`
  — the survey that led to the orchestrate/ directory move and
  named this Rust rewrite as phase 4.
