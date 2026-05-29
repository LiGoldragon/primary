---
tool_versions:
  - [Spirit, "0.3.0"]
---

# Skill — spirit CLI

*The deployed `spirit` binary is the normal substrate for psyche
intent capture and observation. Agents call the unsuffixed CLI
directly. This skill covers the live `Spirit 0.3.0` command shape
and how to verify the deployed wire shape when it drifts.*

## What this skill is for

`persona-spirit` is the persona component that captures psyche
statements as typed records and serves observation/subscription
queries. Its bundled thin CLI is named **`spirit`** and lives in the
user's nix profile as `~/.nix-profile/bin/spirit`. The daemon is
`persona-spirit-daemon`, run as a user service; it listens on a
unix-socket pair under `~/.local/state/persona-spirit/<version>/`.

The Spirit CLI is the normal substrate for intent capture
(`skills/intent-log.md`). Do not append new psyche intent to
`intent/*.nota` during normal work. If the daemon is unavailable,
surface that as a blocker; do not silently revive the legacy file
substrate.

## Deployment slots — `spirit`, `spirit-vX.Y.Z`, `spirit-next`

Spirit is **deployed side-by-side**. The user profile installs a
versioned wrapper per tagged release plus a `spirit-next` slot for
the in-flight authoring branch, and the unsuffixed `spirit` symlink
points at whichever versioned wrapper is the current production
target. Each daemon has its own segregated state directory
(`~/.local/state/persona-spirit/<version>/`), its own sockets, and
its own redb database — they never share files. A typical profile:

```text
spirit            -> spirit-vX.Y.Z       (production — the MAIN slot)
spirit-vX.Y.Z     -> installed           (current production daemon)
spirit-vX.Y.Z-1   -> installed           (older side-by-side, retained)
spirit-vX.Y.Z+1   -> installed           (newer side-by-side, under test)
spirit-next       -> (slot)              (in-flight authoring branch)
```

This is the next/main/previous vocabulary (workspace discipline)
applied at the deployment-naming layer: **what is being authored IS
next**; **the current published baseline IS main**; **previous is
the prior release retained for handover**. Tag-suffixed wrappers
(`spirit-v0.2.0`, `spirit-v0.3.0`, etc.) are explicit diagnostic and
testing surfaces. The unsuffixed `spirit` is the production binding
and the normal command for agents. Intent capture uses `spirit`, not
a version-suffixed wrapper. Cutover is an alias change, not a
destructive replace.

Use a tag-suffixed wrapper only when deliberately testing or
inspecting that version's segregated daemon/database. When in doubt
about what `spirit` currently points at, `readlink -f $(command -v
spirit)` resolves the chain.

## How to invoke

The spirit binary takes **exactly one argument** per the
single-argument rule (`skills/component-triad.md` §"The single
argument rule"). Two accepted shapes:

- **Inline NOTA argument** — the argument is a NOTA expression starting
  with `(`. This is the default. **Wrap the whole NOTA expression in
  shell double quotes.** NOTA strings come from bracket forms
  exclusively (`[text]` or `[|text|]`); there is no `"` inside any
  valid NOTA expression. The shell double quote is therefore the
  clean outer argument boundary, and apostrophes inside the
  description survive untouched. Single-quoting the argument is wrong
  — it loses apostrophes.
  ```sh
  spirit "(Record ([workspace] Decision [summary] Maximum))"
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
NOTA text — `(RecordAccepted ...)`, `(RecordsObserved [...])`,
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

Examples below match the live `Spirit 0.3.0` wire shape as deployed
for the unsuffixed `spirit` command. When in doubt, read the
deployed source per the previous section.

Records are **untagged** per `NotaRecord` (the `ee90eef` codec
change). Enum variants carry a head; record bodies do not. `Option`
is `Some`-wrapping — `None` bare or `(Some <value>)`. `Topic`,
`Description`, and `StatementText` are `NotaTransparent String`
newtypes — encoded as bare tokens when possible, or bracket strings
when they contain whitespace or punctuation.

**Record an intent entry — description-only, multi-topic shape.**
A v0.3.0 record carries a vector of topics, one agent-clarified
`Description`, a `Kind`, and a `Magnitude`. No verbatim field, no
context payload, no client-supplied timestamp. **The daemon stamps
date/time itself.**
The agent clarifies the psyche's wording into the description before
recording — that is the agent's job, and it is what keeps the intent
log dense and searchable rather than verbose and lossy:

```sh
spirit "(Record ([<topic> ...] <Kind> [description] <Magnitude>))"
# Kind ∈ { Decision Principle Correction Clarification Constraint }
# Magnitude ∈ { Zero Minimum VeryLow Low Medium High VeryHigh Maximum }
```

The reply is **terse — no echo**: `(RecordAccepted N)` where `N` is
the assigned identifier. The acknowledgement deliberately does not
echo the submitted intent content; the wire reply is token-cheap.

**Remove an intent entry** — delete one stored record by numeric
identifier through the daemon:

```sh
spirit "(Remove 1088)"
```

The reply is `(RecordRemoved 1088)`. Use this for records that should
not remain in the active store at all; use `Correction` or
supersession when lineage should remain visible.

**Topics are user-creatable strings carried in a vector** at the wire
layer — any new topic word a `Record` uses is registered. No
pre-declared enum of topics; pick the topic words that fit, reuse
existing words when they cover the substance.

**Observe records** — query the store. This is the live production
`Spirit 0.3.0` record-query shape. `Records` filters by topic
selection, optional kind, and certainty. Topic selection is `(Any [])`
for no topic filter, `(Partial [a b])` for records matching one or
more requested topics, and `(Full [a b])` for records matching every
requested topic. Certainty selection is `Any` for no certainty filter,
`(Exact Zero)` for removal candidates, `(AtMost Low)` for a
low-certainty review band, or `(AtLeast High)` for high-certainty
records. `Minimum` remains weak but real intent; do not use it as the
removal-candidate marker. The old three-field record query still
decodes as compatibility input, but agents should emit the four-field
shape.
`RecordIdentifiers` selects by numeric identifier: `Exact` selects one
record; `Range` is inclusive, so `(Range (1050 1060))` returns records
1050 through 1060 when present. Use `SummaryOnly` for compact summaries
and `WithProvenance` when you need daemon-stamped date/time:

```sh
spirit "(Observe Topics)"
spirit "(Observe (Records ((Any []) None Any SummaryOnly)))"
spirit "(Observe (Records ((Partial [spirit search]) None Any SummaryOnly)))"
spirit "(Observe (Records ((Full [spirit search]) None Any WithProvenance)))"
spirit "(Observe (Records ((Any []) (Some Decision) Any SummaryOnly)))"
spirit "(Observe (Records ((Any []) None (Exact Zero) WithProvenance)))"
spirit "(Observe (Records ((Any []) None (AtMost Low) SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Exact 1053) SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Range (1050 1060)) SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Range (1050 1060)) WithProvenance)))"
```

**Submit a free-form statement** — `State` lowers to an `Assert`
sema-classified observation:

```sh
spirit "(State [free-form psyche statement text])"
```

**Subscribe / unsubscribe** — `Watch` opens a long-lived stream;
`Unwatch` closes it. The CLI's single-call shape isn't well suited
to long subscriptions; for agent code prefer the typed client
library inside `persona_spirit::ordinary::SignalClient`. Tap/Untap
fanout is currently a no-op placeholder pending persona-introspect.

## The daemon's single-argument configuration

The daemon binary `persona-spirit-daemon` honors the same
single-NOTA-argument rule. Its argument is a positional 9-field
record:

```
("/path/to/spirit.sock"
 "/path/to/owner.sock"
 "/path/to/upgrade.sock"
 "/path/to/persona-spirit.redb"
 <magnitude-limit:int>
 None None None None)
```

Three Unix sockets (ordinary, owner, upgrade), one redb database
path, one magnitude limit, four `None`-slot extension points
reserved for future configuration fields. No flags. The CriomOS-home
module is what authors this tuple per release; the daemon's
`ExecStart` line is the canonical witness:

```sh
systemctl --user cat persona-spirit-daemon-vX.Y.Z.service
```

Future configuration fields land by filling one of the `None` slots
in the contract crate, not by adding a flag. When the schema-driven
substrate matures, a `spirit-daemon-config.schema` will emit this
configuration record from a schema declaration rather than
hand-authored positional parsing — but the contract shape (one
positional record argument) is stable.

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
