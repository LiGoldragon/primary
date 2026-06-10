# Skill — spirit CLI

How to call the deployed `spirit` binary to capture and observe psyche intent.

## What it is

`spirit` captures psyche statements as typed records and serves
observation/subscription queries. The active production binary is the
schema-derived `spirit` component at version `0.4.0`, installed in the
user profile as `~/.nix-profile/bin/spirit`. The user service is
`spirit-daemon.service`, listening under `~/.local/state/spirit/`.

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

The wrapper sets `SPIRIT_SOCKET`; the daemon configuration carries the
ordinary and meta socket paths. There are no CLI flags for sockets or
configuration. Inspect the active wrapper with
`readlink -f $(command -v spirit)` and the user service with
`systemctl --user status spirit-daemon.service`.

## Read the wire shape from the pinned source

The active implementation is `/git/github.com/LiGoldragon/spirit`, with
generated Signal/Nexus/SEMA types under `src/schema/`. `signal-spirit`
still provides the binary daemon startup configuration type and remains
an active dependency. Do not infer the wire shape from old
`persona-spirit` documents — read the deployed `spirit` source pinned by
`CriomOS-home/flake.lock`.

```sh
rg -n '"spirit"' /git/github.com/LiGoldragon/CriomOS-home/flake.lock
cd /git/github.com/LiGoldragon/spirit
rg -n "pub struct Observe|pub enum Input|pub struct VersionReport" src/schema
```

## Encoding rules

Records are **untagged** (`NotaRecord`): enum variants carry a head,
record bodies do not. `Option` is `Some`-wrapping — bare `None` or
`(Some <value>)`. `Topic`, `Description`, and `StatementText` are
`NotaTransparent String` newtypes — bare tokens when possible, bracket
strings when they contain whitespace or punctuation. Bracket
identifiers (`[abcd]`) so codes starting with a digit stay valid.

## Recording intent

A v0.4.0 record carries a vector of topics, one agent-clarified
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

The reply is terse and does not echo content:
`(RecordAccepted ([abcd] (...)))` or the same shape with a different
short code. Spirit mints random lowercase base36 identifiers and shows
the shortest collision-free code with a four-character minimum. Cite and
pass the short code the daemon returns.

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

**Collect removal candidates** — archive matching records to the
owner-configured archive database, then remove them from the hot store:

```sh
spirit "(CollectRemovalCandidates (((Full [stale]) (Some Decision) (Exact Zero))))"
```

The reply `(RemovalCandidatesCollected ([...] [...] [...]))` carries
archived `RecordSummary` values, removed identifiers, and skipped
candidates. Archive location is not a working-signal argument; the
owner configures it through the meta socket.

## Observing records

`Observe` carries a generated three-field `Query` directly:

```text
(Observe ((<TopicMatch>) <Kind?> <PrivacySelection>))
```

- **TopicMatch**: `(Any [])` no filter, `(Partial [a b])` matches
  any requested topic, `(Full [a b])` matches every requested topic.
- **Kind?**: `None` or `(Some Decision)`.
- **PrivacySelection**: `Any`, `(Exact Zero)`, `(AtMost Low)`,
  `(AtLeast High)`.

`Observe` currently stashes non-empty result sets and returns a
`RecordsStashed` handle. Use `LookupStash` with that handle to retrieve
the full `RecordsObserved` payload. Use `PublicRecords` and
`PrivateRecords` for the ergonomic privacy-scoped shortcuts.

```sh
spirit Version
spirit "(Observe ((Full [spirit]) None (Exact Zero)))"
spirit "(PublicRecords ((Full [spirit]) None))"
spirit "(PrivateRecords ((Partial [spirit]) None))"
spirit "(Lookup [abcd])"
spirit "(LookupStash 1)"
spirit "(Count ((Any []) None (Exact Zero)))"
```

Two recurring wrong shapes:

- `Search` is not a production request head.
- `(Observe (Records ...))` is the retired production shape; live
  schema-derived `Observe` takes `Query` directly.

## Other operations

```sh
spirit "(State [free-form psyche statement text])"   # lowers to an Assert sema observation
```

`Version` is a bare NOTA atom, not a Unix flag:

```sh
spirit Version
```

`SubscribeIntent` opens a long-lived intent event stream. `Tap` and
`Untap` expose the observer surface over operation/effect observations.

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
- `skills/nota-design.md` — positional-record encoding rules.
- `/git/github.com/LiGoldragon/spirit` — active component source;
  `tests/process_boundary.rs` and `tests/nix_integration.rs` show the
  live wire shape.
- `/git/github.com/LiGoldragon/signal-spirit` — daemon startup
  configuration contract consumed by the active component.
