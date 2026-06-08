---
tool_versions:
  - [Spirit, "0.5.2"]
---

# Skill — spirit CLI

How to call the deployed `spirit` binary to capture and observe psyche intent.

## What it is

`persona-spirit` captures psyche statements as typed records and serves
observation/subscription queries. Its bundled thin CLI is `spirit`, in
the user's nix profile at `~/.nix-profile/bin/spirit`. The daemon is
`persona-spirit-daemon`, a user service listening on a unix-socket pair
under `~/.local/state/persona-spirit/<version>/`.

`spirit` is the sole substrate for intent capture. There is no
file fallback; the old `intent/*.nota` substrate is retired. If the
daemon is unavailable, surface that as a blocker.

## How to invoke

The binary takes exactly one argument (the one-argument rule —
`skills/component-triad.md`). Two accepted shapes:

- **Inline NOTA** — argument starts with `(`. The default. Wrap the
  whole expression in shell double quotes. Valid NOTA never contains
  `"` (strings come from bracket forms `[text]` / `[|text|]`), so the
  shell double quote is a clean boundary and apostrophes inside the
  description survive. Single-quoting is wrong — it loses apostrophes.
  ```sh
  spirit "(Record ([workspace] Decision [summary] Maximum))"
  ```
- **Path to a NOTA file** — argument does not start with `(`; the CLI
  reads the file as the NOTA argument. For records with embedded shell
  metacharacters or too large to keep the bash line readable.
  ```sh
  spirit ./record.nota
  ```

The CLI replies on stdout with the daemon's typed `Reply` as NOTA text
— `(RecordAccepted ...)`, `(RecordsObserved [...])`, etc. Exit code is
nonzero on transport, parse, or daemon errors.

Sockets come from `PERSONA_SPIRIT_SOCKET` and
`PERSONA_SPIRIT_OWNER_SOCKET`, set by the home-profile wrapper — no
flag, no config path, no socket argument. The wrapper is a shell stub
that sets the env vars then execs the real binary; inspect with
`readlink -f $(command -v spirit)`.

## Deployment slots

Spirit deploys side-by-side. The profile installs a versioned wrapper
per tagged release plus a `spirit-next` slot for the in-flight branch;
the unsuffixed `spirit` symlink points at the current production
wrapper. Each daemon has its own state directory, sockets, and redb
database — they never share files.

```text
spirit            -> spirit-vX.Y.Z       (production — the MAIN slot)
spirit-vX.Y.Z     -> installed           (current production daemon)
spirit-vX.Y.Z-1   -> installed           (older side-by-side, retained)
spirit-vX.Y.Z+1   -> installed           (newer side-by-side, under test)
spirit-next       -> (slot)              (in-flight authoring branch)
```

This is the next/main/previous vocabulary at the deployment layer:
what is being authored is `next`, the published baseline is `main`,
`previous` is the prior release retained for handover. Intent capture
uses the unsuffixed `spirit`, never a version-suffixed wrapper. Use a
tag-suffixed wrapper only when deliberately testing that version's
segregated daemon/database. Cutover is an alias change, not a
destructive replace. `readlink -f $(command -v spirit)` resolves what
`spirit` currently points at.

## Read the wire shape from the pinned source

The active ordinary Spirit contract on main is `signal-spirit`. Older
deployed profiles may still pin the retired `signal-persona-spirit` crate
until the production daemon rebuilds. Do not infer the wire shape from this
skill's examples — read the **deployed** contract source named by the
running daemon's `Cargo.lock`, not whichever repo is freshest on `main`.
`main` drifts from production until the next CriomOS rebuild.

```sh
# persona-spirit commit pinned by CriomOS-home (built the deployed CLI):
grep -B 1 -A 12 '"persona-spirit"' \
    /git/github.com/LiGoldragon/CriomOS-home/flake.lock | head -30

# that commit pins the ordinary Spirit contract in its Cargo.lock:
cd /git/github.com/LiGoldragon/persona-spirit
git show <persona-spirit-rev>:Cargo.lock \
    | rg -B 1 -A 4 '"signal-spirit"|"signal-persona-spirit"'

# read the deployed contract from the repo Cargo.lock names:
cd /git/github.com/LiGoldragon/signal-spirit
git show <signal-spirit-rev>:src/lib.rs
# Older deployed profiles may still require:
# cd /git/github.com/LiGoldragon/signal-persona-spirit
# git show <signal-persona-spirit-rev>:src/lib.rs
```

## Encoding rules

Records are **untagged** (`NotaRecord`): enum variants carry a head,
record bodies do not. `Option` is `Some`-wrapping — bare `None` or
`(Some <value>)`. `Topic`, `Description`, and `StatementText` are
`NotaTransparent String` newtypes — bare tokens when possible, bracket
strings when they contain whitespace or punctuation. Bracket
identifiers (`[abcd]`) so codes starting with a digit stay valid.

## Recording intent

A v0.5.2 record carries a vector of topics, one agent-clarified
`Description`, a `Kind`, a certainty `Magnitude`, and a privacy
`Magnitude`. No verbatim field, no context payload, no client
timestamp — **the daemon stamps date/time itself**. The four-field
form is public shorthand defaulting privacy to `Zero`; the five-field
form sets privacy explicitly. The agent clarifies the psyche's wording
into the description before recording — that keeps the log dense and
searchable rather than verbose and lossy.

```sh
spirit "(Record ([<topic> ...] <Kind> [description] <Magnitude>))"
spirit "(Record ([<topic> ...] <Kind> [description] <Certainty> <Privacy>))"
# Kind      ∈ { Decision Principle Correction Clarification Constraint }
# Magnitude ∈ { Zero Minimum VeryLow Low Medium High VeryHigh Maximum }
```

Privacy uses the same `Magnitude` ladder on a privacy axis. `Zero`
means open/public (the workspace default); higher values narrow the
audience. Never put private personal substance in a `Zero` record.

The reply is terse and does not echo content: `(RecordAccepted abcd)`
or `(RecordAccepted [1234])` depending on whether the encoder can print
the identifier bare. v0.5.2 mints random lowercase base36 identifiers
and shows the shortest collision-free code (4-7 chars). Cite and pass
the short code the daemon returns.

**Topics are user-creatable strings in a vector** — any new word a
`Record` uses is registered; no pre-declared enum. Pick broad reusable
words and let the vector carry multiple concepts: prefer
`[intent logging]` over `[intent-log]` when both `intent` and
`logging` are real topics. Keep a compound topic only when the compound
is the established name of one thing.

**Shorthand stays typed.** Any future shorthand (`RecordPublic`,
`RecordPrivate`, `Search`) is a distinct typed NOTA operation that
fills defaults and lowers to the full record — never shell flags or a
second CLI syntax. NOTA positional records do not omit fields. Until
such heads exist in the deployed contract, do not invent them in live
calls.

## Removing and changing records

```sh
spirit "(Remove [abcd])"                    # -> (RecordRemoved [abcd])
spirit "(ChangeCertainty ([abcd] Zero))"    # -> (CertaintyChanged ([abcd] Zero))
```

`Remove` deletes a record entirely — use it when nothing should remain
in the active store. Setting certainty to `Zero` is the **recoverable**
removal-candidate nomination: the record stays queryable and is
restored by changing certainty back to a non-zero `Magnitude`. Use
`Correction` or supersession when lineage should stay visible. Use hard
`Remove` only after review.

**Collect removal candidates** — archive exact-`Zero` records, then
remove them from the hot store:

```sh
spirit "(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (ArchiveDatabase Default)))"
spirit "(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (ArchiveDatabase (Path [/tmp/spirit-removal-candidates.sema]))))"
spirit "(CollectRemovalCandidates (((Any []) None (Exact Zero) Any (Exact Zero) SummaryOnly) (Print StandardOutput)))"
```

The reply `(RemovalCandidatesCollected ([...] [...] [...]))` carries
archived `RecordSummary` values, removed identifiers, and skipped
candidates. The query is constrained to exact `Zero` certainty and
exact `Zero` privacy; broad queries are rejected. `ArchiveDatabase
Default` writes the daemon-derived archive; `(Path [...])` a
caller-selected one; `Print StandardOutput`/`StandardError` writes no
archive and returns typed material for the CLI to render. Archive
failure returns skipped candidates (e.g. `[([abcd] ArchiveFailed)]`)
and leaves those records queryable.

## Observing records

`Observe` always carries one `Observation` variant — usually `Records`.
The query shape is:

```text
(Observe (Records ((<TopicSelection>) <Kind?> <CertaintySelection> <RecordedTimeSelection> <ObservationMode>)))
```

- **TopicSelection**: `(Any [])` no filter, `(Partial [a b])` matches
  any requested topic, `(Full [a b])` matches every requested topic.
- **Kind?**: `None` or `(Some Decision)`.
- **CertaintySelection**: `Any`, `(Exact Zero)`, `(AtMost Low)`,
  `(AtLeast High)`. `Minimum` is weak but real intent — do not use it
  as the removal-candidate marker.
- **RecordedTimeSelection**: `Any`, `Shallow`, `Recent`, `Deep`,
  `VeryDeep`, `(Since (YYYY-MM-DD HH:MM:SS))`, `(Until (...))`,
  `(Between ((...) (...)))`. Qualitative depths apply after
  topic/kind/certainty matching and return the newest matches at that
  depth, so quiet topics reach farther back than active ones.
- **ObservationMode**: `SummaryOnly` for compact summaries,
  `WithProvenance` when you need daemon-stamped date/time.

The `Records` query has no privacy field and means exact `Zero`
privacy by type. Use `PrivateRecords` / `PrivateRecordIdentifiers` for
elevated reads. `RecordIdentifiers` selects by exact code `(Exact
[abcd])`; identifier ranges are not live in the random-identifier era —
use `Records` with recency windows for history.

```sh
spirit "(Observe Topics)"
spirit "(Observe (Records ((Any []) None Any Recent SummaryOnly)))"
spirit "(Observe (Records ((Partial [spirit search]) None Any Any SummaryOnly)))"
spirit "(Observe (Records ((Full [spirit search]) None Any Any WithProvenance)))"
spirit "(Observe (Records ((Any []) (Some Decision) Any Any SummaryOnly)))"
spirit "(Observe (Records ((Any []) None (AtMost Low) Any SummaryOnly)))"
spirit "(Observe (Records ((Partial [spirit]) None Any Deep SummaryOnly)))"
spirit "(Observe (Records ((Partial [spirit]) None Any (Since (2026-05-30 00:00:00)) SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Exact [abcd]) SummaryOnly)))"
spirit "(Observe (PrivateRecords ((AtMost Low) ((Any []) None Any Any SummaryOnly))))"
spirit "(Observe (PrivateRecordIdentifiers ((AtMost Low) ((Exact [abcd]) SummaryOnly))))"
```

Two recurring wrong shapes:

- `Search` is not a production request head.
- `(Observe ((Any [...]) ...))` omits the `Records` variant; the daemon
  expects a PascalCase observation name after `Observe`, not a bare
  query record.

## Other operations

```sh
spirit "(State [free-form psyche statement text])"   # lowers to an Assert sema observation
```

`Watch` opens a long-lived stream; `Unwatch` closes it. The CLI's
single-call shape suits subscriptions poorly — for agent code prefer
the typed `persona_spirit::ordinary::SignalClient`. Tap/Untap fanout is
a no-op placeholder pending persona-introspect.

## Daemon startup is binary-only

The CLI accepts NOTA because it is the human/agent text edge; the
daemon does not. Daemon startup is exactly one pre-generated
signal-encoded/rkyv message — inline NOTA and `.nota` paths are
rejected before daemon decoding. A deploy helper (CriomOS-home) may
author configuration from typed NOTA source, but it encodes the binary
startup signal before launching. A virgin daemon can receive an initial
`Configure` as binary signal; after configuration, restarts self-resume
from persisted SEMA state. New configuration fields land as typed
fields in the startup schema or as authenticated meta-signal messages —
never flags, never daemon NOTA parsing.

Old service definitions may show a positional NOTA tuple — that is
legacy drift to migrate, not the rule to copy. The witness:

```sh
systemctl --user cat persona-spirit-daemon-vX.Y.Z.service
```

## Substrate migration discipline

Applies to any migration where a permissive substrate (file with free
PascalCase tokens, untyped store) is replaced by a strict one
(rkyv-archived enum, typed redb engine). Four rules:

1. **Enumerate every closed-world enum on both sides before
   relogging.** Compare variant sets; where they differ, design an
   explicit mapping. Don't assume parallel evolution kept the
   vocabularies aligned.
2. **The strict substrate is ground truth.** When the daemon rejects a
   token the file accepted, the target shape wins — the permissive
   substrate was permissive by accident. Migration normalises; it does
   not bridge backward.
3. **Surface mismatches before bulk relog.** A dumb migration tool
   needs the mapping table baked in; even a no-import daemon does not
   absolve the migration step of vocabulary auditing.
4. **Older vocabulary may not round-trip without explicit mapping.**
   Permissive parsers accept tokens the strict decoder later rejects;
   the gap surfaces only at the strict-substrate boundary.

**Canonical pattern — two-submodule migration module** (one per
component-version step):

- `mod historical` — private rkyv reproduction of the deployed old
  types. Every leaf and branch the source bytes need is redefined
  locally, with no dependency on the old crate version, so the
  migration crate reads source bytes deterministically.
- `mod current_shape` — same-name types binding the current crate's
  unchanged leaves, overriding only the fields that changed.
- **A `From`-chain composes the conversion** — `StoredRecord ->
  StampedEntry -> Entry`, plus enum-to-enum maps for the changed leaves
  (e.g. `historical::Certainty -> Magnitude`). One direction of typed
  flow; no per-field handwiring at the call site.

## No manual dual-writing or in-CLI migration

Do not log the same intent by hand to multiple Spirit databases —
version cutover and dual-write are implemented in code. Importing
legacy nota files stays out of Spirit; a separate migration tool may
translate legacy records, but Spirit itself remains the intent daemon
and CLI. Pass the same broad topic strings (`workspace`, `spirit`,
`signal`, `component-shape`, `persona`, …) the deployed store already
uses; the redb database carries the canonical record set.

## See also

- `skills/intent-log.md` — what gets logged, the five-kind taxonomy,
  the gold-mining discipline.
- `skills/intent-maintenance.md` — sweep / supersession discipline.
- `skills/nota-design.md` — positional-record encoding rules.
- `/git/github.com/LiGoldragon/persona-spirit` — component source;
  `tests/daemon.rs` is the best worked example for the wire shape.
- `/git/github.com/LiGoldragon/signal-spirit` — active ordinary Spirit
  wire contract; `src/lib.rs` declares the channel.
- `/git/github.com/LiGoldragon/meta-signal-spirit` — active Spirit meta
  policy contract for privileged lifecycle/configuration traffic.
