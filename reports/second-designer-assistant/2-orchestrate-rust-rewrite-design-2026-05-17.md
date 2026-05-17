# `tools/orchestrate` — Rust port as thin signal-persona-mind client

*Operator design report. The Rust port of `tools/orchestrate`,
narrowed: a thin signal-persona-mind client that preserves the
on-disk lock-file format during the shell-helper era, then becomes
a wrapper as `persona-mind` and `persona-orchestrate` take over
canonical state and machinery. No new contract crate; no new typed
vocabulary; the records already exist in `signal-persona-mind`.*

Date: 2026-05-17 (revised in place after report 4)

Author: second-designer-assistant

---

## TL;DR

`tools/orchestrate` today is a 250-line bash script that reads a
flat `orchestrate/roles.list` and reads/writes per-lane lock files at
`orchestrate/<lane>.lock`. This report specifies the Rust port:
**a thin client that imports `signal-persona-mind` for the typed
record vocabulary (`RoleClaim`, `RoleRelease`, `RoleObservation`,
`ActivitySubmission`) and writes lock files at the same paths as
the shell helper, preserving format bit-for-bit.**

What's **out of scope** for this rewrite (and tracked in a
separate designer bead per report 4):

- Inventing new typed Request/Reply vocabulary for orchestrate.
  The vocabulary lives in `signal-persona-mind` already.
- The orchestration **machinery** — agent spawning, supervision,
  conflict resolution policy, scheduling across executors,
  escalation. That's `persona-orchestrate`'s scope.
- A new contract crate `signal-persona-orchestrate`. Same — owned
  by the separate persona-orchestrate design work.

The rewrite remains the **bridge**: shell → Rust, lock-file-shape
preserved, then later the lock-file side effect drops as
`persona-mind` becomes the canonical store and
`persona-orchestrate` is the daemon driving the verbs.

**Why this scope cut:** report 4
(`reports/second-designer-assistant/4-persona-orchestrate-control-plane-2026-05-17.md`)
established that orchestration machinery is its own component
(`persona-orchestrate`), distinct from `persona-mind`. The Rust
port of `tools/orchestrate` doesn't need to anticipate the
machinery — it just needs to write the same records `persona-mind`
already understands, and keep the lock-file shape working for the
shell-helper era.

---

## Current state (what operator inherits)

After reports 1, 3, and 4 of this lane and the migrations that
followed, the workspace has:

| Surface | Path | Shape |
|---|---|---|
| Protocol doc | `orchestrate/AGENTS.md` | The canonical orchestration protocol. |
| Lock files | `orchestrate/<lane>.lock` | Plain-text per-lane state. Eleven files. |
| Role registry | `orchestrate/roles.list` | Bash-readable interim. One lane per line; optional `assistant-of:<main>` metadata. |
| Tool | `tools/orchestrate` | Bash. Reads `roles.list`, writes lock files, checks overlap, prints status. |
| Meta-skill | `skills/role-lanes.md` | How lane stacking works. |
| Existing typed records | `signal-persona-mind/src/lib.rs:418-580, 1756-1760` | `RoleClaim`, `RoleRelease`, `RoleHandoff`, `RoleObservation`, `ActivitySubmission`. Already implemented in the daemon (`persona-mind/src/text.rs:242-782`). |
| Tracking | `.beads/` | BEADS, transitional. |

The shell helper's role-list externalisation (commit
`81f5262fb149` and successor) is **the interim**. The Rust port
replaces both the role-reading code and the lock-file manipulation.

---

## End-state design — thin client, no new crate

The Rust port replaces `tools/orchestrate` *in place*. The path
stays as `tools/orchestrate`. Two implementation shapes work:

- **Single-binary shell wrapper.** A Rust binary
  (e.g. `tools/orchestrate-bin`) does the work; `tools/orchestrate`
  becomes a 3-line bash shim that exec's the binary. Lower friction
  during build / development.
- **Direct binary at the path.** `tools/orchestrate` is the Rust
  binary, no shell shim. Cleaner; requires the build to drop the
  binary at exactly that path.

Operator chooses. The behavior is identical either way.

### What the binary does

1. **Reads the role registry.** Today `orchestrate/roles.list`; once
   the Nota format lands, `orchestrate/roles.nota`. The reader
   parses both forms (one routine, one being introduced) so the
   binary can run during the transition.
2. **Decodes argv into a `signal-persona-mind` request record.**
   - `tools/orchestrate claim <lane> <scope> [...] -- <reason>` →
     `MindRequest::RoleClaim(RoleClaim { lane, scopes, reason, ... })`.
   - `tools/orchestrate release <lane>` →
     `MindRequest::RoleRelease(RoleRelease { lane, ... })`.
   - `tools/orchestrate status` →
     `MindRequest::RoleObservation(RoleObservation)`.
3. **Resolves overlap.** Reads all peer lock files, applies the
   existing path-nesting / task-token-exact-match overlap rules,
   surfaces conflicts in the reply.
4. **Writes lock files.** On successful claim/release, writes
   `orchestrate/<lane>.lock` in the existing format (one scope per
   line, `# <reason>` annotation). This is a **side effect** of
   the request — the records are the source of truth in
   `signal-persona-mind`'s shape, the lock files are a serialised
   projection for the shell-helper era.
5. **(Future) calls into `persona-mind` directly.** Once
   `persona-mind` is the canonical store for claim/release records,
   the binary sends its decoded `MindRequest` to the daemon's Unix
   socket instead of (or alongside) writing lock files. This is the
   second move, after `persona-mind`'s canonicalisation lands.

### What the binary explicitly does NOT do

- **Define its own typed vocabulary.** No `(Request (Claim …))` /
  `(Reply (Claimed …))` records authored here. Everything decodes
  into `signal-persona-mind`'s existing `MindRequest` /
  `MindResponse` shape.
- **Build its own contract crate.** No `signal-persona-orchestrate`
  introduced as part of this rewrite. (A future contract repo with
  that name is in scope for the separate `persona-orchestrate`
  design — see report 4 §"The contract — what
  signal-persona-orchestrate covers" — but unrelated to this
  rewrite.)
- **Spawn or supervise agents.** No process management. No
  scheduler. No dead-agent recovery. Those belong to
  `persona-orchestrate`.

### Lock-file format — preserved

The on-disk lock-file format stays exactly as the shell helper
writes it today. The shape lives in `orchestrate/AGENTS.md`
§"Lock-file format" — that section is the authoritative reference.

### Typed errors — per-crate enum

Per `skills/rust/errors.md`: one `Error` enum, with `#[from]`
conversions for foreign types. No `anyhow`, no `Box<dyn Error>`.
Variants name the failure modes:

- `UnknownLane(String)`
- `LockReadFailed { path: PathBuf, source: io::Error }`
- `RoleRegistryParseFailed { path: PathBuf, source: ParseError }`
- `ClaimOverlap { lane: LaneName, scope: Scope, held_by: LaneName }`
- `BeadsScopeForbidden(PathBuf)`
- ... etc.

### Tests — Nix-backed

Per `skills/testing.md`:

- **Pure check** — `signal-persona-mind` request decode for each
  CLI verb; argv → `MindRequest` round-trip; role-registry
  parsing; lock-file format round-trip.
- **Stateful runner** — claim/release sequences against a
  tempfile-rooted workspace; named flake output for inspection.
- **Chained derivation (optional)** — end-to-end CLI smoke test.

---

## What changes for agents

**Nothing visible at the invocation surface.** The same commands
work:

```sh
tools/orchestrate claim <lane> <scope> [more-scopes] -- <reason>
tools/orchestrate release <lane>
tools/orchestrate status
```

Same lock-file format, same role list, same overlap-detection
rules. Agents invoke `tools/orchestrate`; the implementation
substitution is invisible.

The forward opportunity (not part of this rewrite): when
`persona-orchestrate` is in flight, agent claims can transparently
route through the orchestrator's `AcquireScope` verb (per report
4), which decides the policy and emits the `RoleClaim` record on
success. The CLI surface stays the same; the routing path gets
smarter.

---

## Out of scope — named explicitly

This rewrite is the **persistence-side bridge**. It is **not**:

- **`persona-orchestrate`.** The orchestration-machinery component
  is its own designer-scope design (see report 4). Operator
  picks up `persona-orchestrate` implementation later, *after*
  designer's contract design lands.
- **`signal-persona-orchestrate`.** Same — the contract crate
  belongs to the persona-orchestrate work.
- **Vocabulary invention.** `signal-persona-mind` already owns the
  record types. The rewrite imports them, doesn't redefine them.
- **The `mind` CLI absorption.** Eventually `tools/orchestrate` may
  retire entirely once `mind '<NOTA>'` becomes the canonical entry
  point. Out of scope for this rewrite.
- **BEADS replacement.** `.beads/` and `bd` continue. The Rust
  binary keeps calling `bd --readonly list --status open` for
  status output.
- **Lock-file format evolution.** Preserved exactly.
- **Workspace path changes.** `tools/orchestrate` stays where it
  is.

---

## Operator checklist

Suggested order; operator decides actual sequencing.

1. **Skeleton.** Pick a home for the Rust binary — either a new
   small crate or as a `[[bin]]` entry on an existing crate
   (operator's judgement per `skills/micro-components.md`).
2. **Import signal-persona-mind.** Add as a dependency. No new
   contract crate to write.
3. **Falsifiable specs.** Land argv → `MindRequest` round-trip
   tests; lock-file format round-trip tests; role-registry
   parsing tests. All under `nix flake check`.
4. **Lock-file parser/writer.** Implement against existing
   fixtures (the current `orchestrate/<lane>.lock` files are
   real-world examples).
5. **Role registry loader.** Read `orchestrate/roles.list` today;
   accept `orchestrate/roles.nota` once that file is introduced
   (a separate, parallel piece of work — operator may end up
   landing both at once, or in sequence).
6. **Overlap detection.** Path-nesting + task-token exact-match,
   matching the shell helper's `scopes_overlap` semantics
   (current `tools/orchestrate` §`scopes_overlap`).
7. **CLI dispatch.** `claim` / `release` / `status` subcommands;
   one per supported `MindRequest` shape.
8. **BEADS bridge.** `status` invokes `bd --readonly list --status
   open --flat --no-pager --limit 20`; `.beads/` claim attempts
   produce the existing rejection.
9. **Migration commit.** Replace the shell `tools/orchestrate`.
   Verify agents see no behavior change. The shell version stays
   in git history.
10. **Architectural-truth witness.** A test that runs the binary
    against a fixture workspace and asserts lock files match the
    expected format (per `skills/architectural-truth-tests.md`).

---

## Acceptance criteria

- `tools/orchestrate` invocations produce identical lock-file
  contents and overlap-detection behavior as the shell version.
- Argv decodes into `signal-persona-mind`'s existing `MindRequest`
  shape — no parallel vocabulary introduced.
- `orchestrate/roles.list` is read on every invocation (today).
- All Nota records round-trip via `nota-codec`.
- Errors typed per crate; no `anyhow` or `Box<dyn Error>` at any
  boundary.
- Tests pass under `nix flake check`.
- The binary respects the existing `.beads/` "never claim"
  invariant.

---

## See also

- this workspace's
  `reports/second-designer-assistant/4-persona-orchestrate-control-plane-2026-05-17.md`
  — the report that drove this scope cut. Mandatory read for the
  operator picking up this work.
- this workspace's
  `reports/second-designer-assistant/3-persona-orchestrate-research-2026-05-17.md`
  — the prior research framing; superseded in part by report 4.
- this workspace's `orchestrate/AGENTS.md` §"Command-line mind
  target" — the destination this rewrite stages toward.
- this workspace's `tools/orchestrate` — the bash helper to be
  replaced.
- this workspace's `orchestrate/roles.list` — the interim role
  registry the binary reads.
- this workspace's `skills/rust/methods.md`,
  `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`,
  `skills/rust/parsers.md`, `skills/rust/crate-layout.md` — Rust
  craft.
- this workspace's `skills/testing.md` — Nix-backed pure /
  stateful / chained tests.
- `/git/github.com/LiGoldragon/signal-persona-mind/src/lib.rs:418-580,1756-1760`
  — the typed record vocabulary the binary imports.
- `/git/github.com/LiGoldragon/persona-mind/src/text.rs:242-782` —
  the daemon's existing request parsing for the same vocabulary
  (illustrates the shape the CLI is decoding into).
- BEADS `primary-68cb` — the operator pickup bead, updated to
  match this revised scope.
