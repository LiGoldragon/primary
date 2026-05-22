# Skill — spirit CLI

*The deployed `spirit` binary is the substrate-in-progress for psyche
intent capture and observation. Agents call it directly. This skill
covers invocation, the wire shape that is currently deployed, and
how to find the wire shape when it drifts.*

## What this skill is for

`persona-spirit` is the persona component that captures psyche
statements as typed records and serves observation/subscription
queries. Its bundled thin CLI is named **`spirit`** and lives in the
user's nix profile as `~/.nix-profile/bin/spirit`. The daemon is
`persona-spirit-daemon`, run as a user service; it listens on a
unix-socket pair under `~/.local/state/persona-spirit/`.

The Spirit CLI is the substrate the workspace is moving onto for
intent capture (`skills/intent-log.md`). The legacy
`intent/<topic>.nota` shell-append flow remains a fallback while the
deployed pilot has its kinks worked out, but the spirit CLI is the
intended default. *"I want to start using it right away so we can
work out the kinks"* — `intent/spirit.nota` 2026-05-21.

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

Examples below match the wire shape as of the spirit pinned in
CriomOS-home on 2026-05-21 (persona-spirit `694452a`,
signal-persona-spirit `b89731f`). When in doubt, read the deployed
source per the previous section.

Records are **untagged** per `NotaRecord` (the `ee90eef` codec
change). Enum variants carry a head; record bodies do not. `Option`
is `Some`-wrapping — `None` bare or `(Some <value>)`. `Topic`,
`Summary`, `Context`, `Quote`, `StatementText` are
`NotaTransparent String` newtypes — encoded as bare strings (no
ancestry wrapper).

**Record an intent entry** — daemon stamps date/time itself; clients
do not supply timestamps (`intent/persona.nota` 2026-05-20T21:53Z):

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
fanout is currently a no-op placeholder pending persona-introspect
(`intent/persona.nota` 2026-05-20T20:00Z).

## On the substrate replacement

The legacy `intent/<topic>.nota` flow (`skills/intent-log.md`
§"Recording is a lock-free shell append") still exists and is read
by agents that haven't yet absorbed the spirit substrate. During
the kink-working-out window:

- **Capture goes through `spirit`** — the default for new psyche
  intent.
- **Topic vocabulary is shared** — pass the same topic strings
  (`workspace`, `spirit`, `signal`, `component-shape`,
  `persona`, …) the legacy `intent/` files use. The redb db carries
  the canonical record set; the `.nota` files are the prior
  snapshot.
- **`.nota` append remains a fallback** when the daemon is
  unreachable or a kink prevents capture — flag the fallback in
  chat so the kink surfaces.
- **No migration logic inside spirit** — *"importing existing nota
  files STAYS THE FUCK OUT OF SPIRIT"* (`intent/persona.nota`
  2026-05-20T15:30Z). The existing log is not retroactively
  imported; agents re-log relevant past intent by hand if it
  matters.

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
