---
tool_versions:
  - [Spirit, "0.1.0"]
---

# Skill — spirit CLI

*The deployed `spirit` binary is the normal substrate for psyche
intent capture and observation. Agents call it directly. This skill
covers the live `Spirit 0.1.0` command shape and how to verify the
deployed wire shape when it drifts.*

## What this skill is for

`persona-spirit` is the persona component that captures psyche
statements as typed records and serves observation/subscription
queries. Its bundled thin CLI is named **`spirit`** and lives in the
user's nix profile as `~/.nix-profile/bin/spirit`. The daemon is
`persona-spirit-daemon`, run as a user service; it listens on a
unix-socket pair under `~/.local/state/persona-spirit/`.

The Spirit CLI is the normal substrate for intent capture
(`skills/intent-log.md`). Do not append new psyche intent to
`intent/*.nota` during normal work. If the daemon is unavailable,
surface that as a blocker; do not silently revive the legacy file
substrate.

## How to invoke

The spirit binary takes **exactly one argument** per the
single-argument rule (`skills/component-triad.md` §"The single
argument rule"). Two accepted shapes:

- **Inline NOTA string** — the argument is a NOTA expression starting
  with `(`. This is the default.
  ```sh
  spirit '(Record (workspace Decision "summary" "context" Maximum "verbatim quote"))'
  ```
- **Path to a NOTA file** — the argument does not start with `(`; the
  CLI reads the file's contents as the NOTA argument. Reserved for
  cases inline genuinely cannot handle: NOTA with embedded shell
  metacharacters too painful to escape, signal-encoded (rkyv) binary
  files, or a record large enough that the bash line becomes
  unreadable.
  ```sh
  spirit ./record.nota
  ```

The CLI replies on stdout with the daemon's typed `Reply` value as
NOTA text — `(RecordAccepted (...))`, `(RecordsObserved (...))`,
`(RequestUnimplemented (...))`, etc. Exit code is nonzero on
transport, parse, or daemon errors.

Sockets are discovered through `PERSONA_SPIRIT_SOCKET` and
`PERSONA_SPIRIT_OWNER_SOCKET` (set by the home-profile wrapper); no
flag, no config path, no positional socket argument. The wrapper is
itself a tiny shell stub that sets the env vars then execs the real
binary — visible via `readlink -f $(command -v spirit)` and
`nix derivation show`.

## The deployed wire shape — read it from the pinned source

The wire-side `Operation`, `Reply`, and supporting types live in the
`signal-persona-spirit` crate. The crate evolves quickly; agents must
not infer the wire shape from this skill's examples. Always read the
**deployed** version's source — the version the running daemon was
built against — not the current `main`.

To find the deployed pinning:

```sh
# Find the persona-spirit commit pinned by CriomOS-home (the build
# input that produced the deployed user-profile spirit).
grep -B 1 -A 12 '"persona-spirit"' \
    /git/github.com/LiGoldragon/CriomOS-home/flake.lock | head -30

# The persona-spirit commit then pins signal-persona-spirit by Cargo
# dependency; the rev is in its Cargo.lock at that commit.
cd /git/github.com/LiGoldragon/persona-spirit
git show <persona-spirit-rev>:Cargo.lock \
    | grep -B 1 -A 4 '"signal-persona-spirit"'

# Read the deployed signal-persona-spirit lib.rs:
cd /git/github.com/LiGoldragon/signal-persona-spirit
git show <signal-persona-spirit-rev>:src/lib.rs
```

The operator is actively reshaping the persona-spirit triad; main
will drift from production until the next CriomOS rebuild. *"we're
going to have to keep track of the interface"* —
`intent/spirit.nota` 2026-05-21.

## Operations on the ordinary channel (worked examples)

Examples below match the live `Spirit 0.1.0` wire shape as deployed
for the unsuffixed `spirit` command. When in doubt, read the
deployed source per the previous section.

Records are **untagged** per `NotaRecord` (the `ee90eef` codec
change). Enum variants carry a head; record bodies do not. `Option`
is `Some`-wrapping — `None` bare or `(Some <value>)`. `Topic`,
`Summary`, `Context`, `Quote`, `StatementText` are
`NotaTransparent String` newtypes — encoded as bare strings (no
ancestry wrapper).

**Record an intent entry** — daemon stamps date/time itself; clients
do not supply timestamps:

```sh
spirit '(Record (<topic> <Kind> "<summary>" "<context>" <Certainty> "<verbatim quote>"))'
# Kind ∈ { Decision Principle Correction Clarification Constraint }
# Certainty ∈ { Maximum Medium Minimum }
```

**Observe records** — query the store; filter by topic and/or kind;
choose summary-only or with-provenance:

```sh
spirit '(Observe (Records (None None SummaryOnly)))'
spirit '(Observe (Records ((Some "spirit") None WithProvenance)))'
spirit '(Observe (Records (None (Some Decision) SummaryOnly)))'
```

**Submit a free-form statement** — `State` lowers to an `Assert`
sema-classified observation:

```sh
spirit '(State "free-form psyche statement text")'
```

**Subscribe / unsubscribe** — `Watch` opens a long-lived stream;
`Unwatch` closes it. The CLI's single-call shape isn't well suited
to long subscriptions; for agent code prefer the typed client
library inside `persona_spirit::ordinary::SignalClient`. Tap/Untap
fanout is currently a no-op placeholder pending persona-introspect.

## On the substrate replacement

The legacy `intent/*.nota` files still exist as historical input
for agents that have not yet absorbed Spirit, but they are not the
normal write substrate.

- **Capture goes through `spirit`** — the only normal path for new
  psyche intent.
- **Topic vocabulary is shared** — pass the same topic strings
  (`workspace`, `spirit`, `signal`, `component-shape`,
  `persona`, …) the legacy `intent/` files use. The redb db carries
  the canonical record set; the `.nota` files are the prior
  snapshot.
- **No manual dual-writing** — do not log the same intent by hand to
  multiple Spirit databases or to legacy files. Version cutover and
  dual-write behavior must be implemented in code.
- **No migration logic inside spirit** — *"importing existing nota
  files STAYS THE FUCK OUT OF SPIRIT"*. A separate migration or
  upgrade tool may translate legacy records; Spirit itself remains
  the intent daemon and CLI.

## Substrate migration discipline

Generalises beyond intent capture. Applies to any closed-world enum
or typed-record migration where a permissive substrate (file with
free PascalCase tokens, untyped store) is replaced by a strict one
(rkyv-archived enum, typed redb engine). Four rules:

1. **Enumerate every closed-world enum on both sides before
   relogging.** Compare variant sets. Where they differ, design an
   explicit mapping. Don't assume parallel evolution kept the
   vocabularies aligned.
2. **The strict substrate is ground truth.** When the deployed
   daemon rejects a token the file accepted, the target shape wins
   — the permissive substrate was permissive by accident, not by
   design. Migration normalises; it does not bridge backward.
3. **Surface mismatches before bulk relog.** A dumb migration tool
   needs the mapping table baked in; even a no-import daemon
   (Spirit's case — record 70 widened `Certainty` to the universal
   `signal-sema::Magnitude` rather than narrow the writer) does not
   absolve the migration step of vocabulary auditing.
4. **The file substrate's older vocabulary may not round-trip into
   the newer typed substrate without explicit mapping.** Permissive
   parsers accept tokens the strict decoder later rejects; the
   gap surfaces only at the strict-substrate boundary. The sema
   database (record 74) is where the strict shape lives.

**Canonical pattern — two-submodule migration module.** Inside a
sema-upgrade migration module (one per component-version step):

- `mod historical` — private rkyv reproduction of the deployed old
  types. Every leaf and branch the source bytes need is redefined
  locally; no dependency on the old crate version. Lets the
  migration crate read source bytes deterministically without
  pinning the old contract crate.
- `mod current_shape` — same-name types binding the current crate's
  unchanged leaves, overriding only the fields that changed. Borrow
  current leaves from the live contract crate.
- **`From`-chain composes the conversion.** `StoredRecord ->
  StampedEntry -> Entry`, plus enum-to-enum maps for the leaves
  that changed (e.g. `historical::Certainty -> Magnitude`). One
  direction of typed flow; no per-field handwiring at the call
  site. Future sema-upgrade migration modules follow this shape.

## See also

- `skills/intent-log.md` — what gets logged, the five-kind taxonomy,
  the gold-mining discipline. Substrate-agnostic.
- `skills/intent-maintenance.md` — sweep / supersession discipline.
- `skills/intent-clarification.md` — when to ask the psyche.
- `skills/component-triad.md` §"The single argument rule" — why the
  spirit binary takes exactly one NOTA argument.
- `skills/nota-design.md` — positional-record encoding rules
  (untagged NotaRecord, `Some`-wrapping `Option`, PascalCase rules).
- `intent/spirit.nota` — psyche intent on the deployed spirit work
  and substrate goal.
- `/git/github.com/LiGoldragon/persona-spirit` — the component
  source. `tests/daemon.rs` is the best worked example for the wire
  shape.
- `/git/github.com/LiGoldragon/signal-persona-spirit` — the wire
  contract crate. `src/lib.rs` declares the channel.
