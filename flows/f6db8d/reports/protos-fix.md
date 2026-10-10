# protos — string round trip, orphaned tests, iterative traversal

Subflow of main flow f6db8d. Repository `/git/github.com/LiGoldragon/protos`,
held under Orchestrate Lock 1105 `ProtosStringRoundTrip` for the duration of the
work and released on completion.

- Before: **0.29.1** at `b543678cfc8609529cea7174eb4af8a64daa54ad`
- After: **0.30.0** at `e8701521a37c698d6a2eb933618b9d5d1c6f6ffb`, pushed to `main`

Authority read whole: `/home/li/primary/Vision/protos.md`. The `protos` skill
describes an older design (curly quotes as the string delimiter, a `Protoform`
root, `Delineation`, `Situated`, a guillemet map); it was not used as authority.

## What was wrong, and what it is now

### 1. A guillemet string carrying a backslash did not round-trip

Witnessed by the substrate audit (§1.1, `witnesses/substrate/probes.md`): the
writer escaped only `»` and emitted every backslash raw, while the reader
treated `\` as an escape. 9.2 % of built guillemet strings failed to read back,
and the failure reached real data through `Datomizable for String`.

The reader and the writer now share one escape rule, stated once on
`Escaping for Boundary` in `src/core.rs`:

- A backslash escapes the boundary's own glyphs and itself, and nothing else.
  Guillemets escape `\\` and `\»`; parentheses escape `\\`, `\(` and `\)`.
  `\X` for any other X stays a literal backslash followed by X.
- Escaping is **minimal**: the writer prefixes a backslash only where leaving
  the glyph bare would read back as something else — a backslash whose next
  glyph is escapable (or which ends the content), and a closer that the
  boundary cannot hold bare. So `«C:\Users\ada»` and `(a (b) c)` are written
  verbatim, and `«a\»` becomes `«a\\»`.
- Guillemets do not nest, so every `»` inside is escaped and `«` never is.
  Parentheses are read by balance, so only an unbalanced parenthesis is
  escaped.

The two branches of the reader (one per boundary) and the two branches of the
writer collapsed into one rule each. The parentheses writer was already correct;
the guillemet writer was the same function with the logic missing, which is why
the two now share it rather than sitting side by side.

Two reading behaviours changed with it, both required by the round trip:

- `«a\\b»` now reads as `a\b`. It previously read as `a\\b`, which made the
  backslash unrepresentable.
- A trailing `\` at end of text inside guillemets is now `Unclosed('«')`,
  matching the parentheses branch. It previously pushed the backslash and then
  failed as `Unclosed` one step later, so the refusal is the same, reached
  sooner.

`Canonicalizable` measures an opaque leaf by writing it with the same routine,
so extents cannot drift from the writer.

### 2. Four of five committed test files were never compiled

`autotests = false` with one registered target left `delineation.rs`,
`textualization.rs`, `deep.rs` and `scale.rs` uncompiled and written against a
removed API. `autotests = false` is gone; every file in `tests/` is now a target.
One explicit `[[test]]` entry remains, for `scale.rs`, which needs
`harness = false` because it drives its own bounded child processes and reports
growth rather than pass/fail per case. No reason to keep `autotests = false` was
found: it was suppressing the orphans rather than serving anything.

All four files were rewritten against the current design — one structure per
text, `Protos` with extents on every node, `Error`/`Problem` rather than
`Fault`/`Refusal`, guillemets rather than curly quotes, `canonicalize` rather
than `situate`. `cargo test` goes from 18 tests to 49 plus the six size probes.

| target | tests | what it holds |
|---|---|---|
| `tests/protos.rs` | 18 | unchanged; the suite that was already running |
| `tests/delineation.rs` | 15 | the reader: every rule, every problem, every extent |
| `tests/textualization.rs` | 12 | the writer: canonical spacing, both escape rules, five round-trip properties |
| `tests/deep.rs` | 4 | every traversal over a 100 000-deep and a 50 000-wide tree |
| `tests/scale.rs` | 6 probes | peak memory across 1 000 / 10 000 / 100 000, each in a capped child |

### 3. The property round-trip test the brief asked for

`tests/textualization.rs` carries five proptest properties: guillemet content
and parentheses content, each over a 16-glyph alphabet of exactly the glyphs
that decide an opaque region (`\ « » ( ) { } [ ] < > ;` space, newline, `a`,
`猫`) and again over arbitrary `.*`; and an opaque leaf of each boundary placed
between bare siblings inside braces, where a mis-escaped closer would swallow
what follows rather than refuse. Each builds, canonicalizes, prints, reads back,
and compares the whole node including its extent.

**Seen failing first.** With the writer and reader temporarily restored to their
0.29.1 behaviour, five of the twelve tests in that file fail with exactly the
audited symptom, and the parentheses properties keep passing:

```
test an_opaque_leaf_keeps_its_siblings_apart ... FAILED
test only_a_closing_guillemet_or_an_ambiguous_backslash_is_escaped ... FAILED
test an_opaque_leaf_among_siblings_round_trips ... FAILED
test any_guillemet_content_round_trips ... FAILED
test arbitrary_guillemet_content_round_trips ... FAILED
test any_parentheses_content_round_trips ... ok
test arbitrary_parentheses_content_round_trips ... ok

minimal failing input: content = "\\"
  left: Err(Error { extent: Extent { start: 0, end: 5 }, problem: Unclosed('«') })
 right: Ok(Opaque { ..., content: "\\" })    "\\" wrote "«\\»"
```

### 4. Clone, PartialEq and Debug overflowed the stack on a deep tree

Found while migrating `deep.rs`, which asserted in the old design that the
recursive structural traits are iterative. The current `Protos` derived them.
Witnessed: cloning a 20 000-deep built tree aborts with `stack overflow`.

This is not a property the old test invented. `Drop` (`src/dropping.rs`), the
writer and `canonicalize` are all already written with explicit stacks, and
`tests/protos.rs` exercises print and drop at 100 000 deep. Clone, comparison
and showing were the three that had been left recursive. `src/traversing.rs`
now implements all three iteratively; the derives are removed. A read tree can
never exceed the reader's depth bound of 256, so this only ever bit trees built
in memory — which is the direction a dialect's ascent travels.

### 5. The README described a design that no longer exists

It documented curly quotes, `Potential`, `Conceivable`, `Situation`,
`Delineation`, `Refusal`, and an eleven-module anatomy against a crate whose
`src/` holds two files. Rewritten to the current design, with the escape rule
stated as a table.

## Decisions made on the living's behalf

1. **Minimal escaping, not universal escaping.** `Vision/protos.md` says only
   "A closing guillemet inside a string is escaped with a backslash, so the
   ascent never refuses"; it is silent on the backslash itself, which must be
   escapable for any string to round-trip. The reader already treated `\` as an
   escape introducer for both boundaries, and the parentheses writer already
   escaped minimally and was already correct under a property test. Extending
   that same rule to guillemets keeps one rule in the crate instead of two, and
   keeps opaque content as close to verbatim as the boundary allows — which is
   what "every glyph inside is content" asks for. The alternative, escaping
   every backslash unconditionally, would also round-trip but would make
   `«C:\\Users\\ada»` of an ordinary path and would have left the two boundaries
   behaving differently. Recorded in the module documentation on `Escaping`.

2. **`+4` was not fixed here, and does not belong here.** The brief listed it,
   but protos has no notion of an integer at all — `grep -i integer src/` is
   empty. The defect is `Scalar for i64` in `datom-codec/src/composition.rs`
   (audit §1.7), and `Vision/datom.md`, not `Vision/protos.md`, is its
   authority. A sibling subflow of f6db8d holds Orchestrate Lock 1107
   `DatomCodecSubstrateFixes` over `/git/github.com/LiGoldragon/datom-codec`
   and that tree already had `src/composition.rs` modified. Editing it would
   have collided with in-flight work and produced two version bumps racing on
   one main. Left to lock 1107 — and that subflow did fix it: its report
   `flows/f6db8d/reports/datom-codec-fix.md` records `+4` refused under the
   test `integers_refuse_a_leading_plus`, released in datom-codec 0.26.0.

3. **Clone, PartialEq and Debug made iterative rather than the test weakened.**
   Migrating `deep.rs` faithfully required the property to hold. The alternative
   — asserting the traits at a depth the derives survive — would have been a
   test that witnesses nothing.

4. **`Debug` prints one line whatever the alternate flag asks.** An iterative
   writer cannot carry per-node indentation without carrying the depth into its
   own output, and `{:#?}` on a 100 000-deep tree is not a thing anyone wants.
   The non-alternate output is byte-identical to what the derive produced;
   `{:#?}` no longer indents. Stated in the doc comment on the impl.

5. **`scale.rs` kept, with its deep-reading probes replaced.** Its old
   `read-brackets`, `read-chain` and `read-chain-enclosed` modes read 100 000
   levels deep, which the current reader refuses by design at depth 256. They
   were replaced with `read-wide-nest` (wide at two levels), `clone-deep` and
   `canonicalize-deep`, which probe the same linear-memory question against
   structures the current design can actually hold.

6. **0.30.0, a minor bump.** The text a given structure writes changed, and the
   structure a given text reads changed, for any content carrying a backslash.
   That is a change to the format on the wire, breaking at 0.x, so minor rather
   than patch.

## Left standing, deliberately

- **`Problem::MissingHead` appears unreachable.** The reader raises it only
  inside the run loop, which is entered only when the run has no empty segment
  (so cannot begin with a separator) or ends in exactly one separator before an
  opener (so has a head). A leading `.` or `<` never reaches that loop: `.a`,
  `.{ 1 }` and `.` are all read as bare runs, and `<` is dispatched to the
  angled enclosure before `bare_or_headed` sees it. It is declared in
  `protos.ethos`, so removing it changes the generated contract and wants the
  living's word. No test asserts it; its absence is noted here instead.
- **`Vector<Text>` alone is `Multiple`.** A constrained head with no separator
  after it resets and becomes a bare run plus an angled enclosure, which at the
  top level is a second structure. That is the current reader's rule and
  `tests/protos.rs` already depends on it; `tests/delineation.rs` now states it
  explicitly. It is the same tension the audit raises for ethos (§2.1) and is
  not settled here.

## The gate

Run locally, no remote builders (`nix flake check -L --option builders ''`).

`nix flake check -L --option builders ''` — no remote builders, every check
built locally: `protos-build`, `protos-test`, `protos-fmt`, `protos-clippy`,
`protos-doc`, plus the four `runCommand` guards and `generated-contract`.

The first run failed, and that failure is worth recording: the flake's source is
a clean git source, so the then-untracked `src/traversing.rs` was absent from the
build and `mod traversing;` did not resolve. The work was committed and the check
re-run; `cargo test` alone would never have caught it.

```
protos-test> running 4 tests      (deep)          test result: ok. 4 passed; 0 failed
protos-test> running 15 tests     (delineation)   test result: ok. 15 passed; 0 failed
protos-test> running 18 tests     (protos)        test result: ok. 18 passed; 0 failed
protos-test> running 12 tests     (textualization) test result: ok. 12 passed; 0 failed
protos-test> ok   read-vector:        1000 -> 2444 kB, 10000 -> 3692 kB, 100000 -> 17832 kB (bound 37548 kB)
protos-test> ok   read-wide-nest:     1000 -> 2756 kB, 10000 -> 6764 kB, 100000 -> 48232 kB (bound 79260 kB)
protos-test> ok   build-nested:       1000 -> 2440 kB, 10000 -> 3692 kB, 100000 -> 16988 kB (bound 37604 kB)
protos-test> ok   build-vector:       1000 -> 2444 kB, 10000 -> 3660 kB, 100000 -> 17776 kB (bound 37068 kB)
protos-test> ok   clone-deep:         1000 -> 2536 kB, 10000 -> 4472 kB, 100000 -> 26988 kB (bound 47960 kB)
protos-test> ok   canonicalize-deep:  1000 -> 2424 kB, 10000 -> 3564 kB, 100000 -> 15468 kB (bound 35908 kB)
all checks passed!
```

Before the flake, run in the working tree: `cargo test` (49 tests plus the six
probes, all green), `cargo fmt --check` (clean), `cargo clippy --all-targets --
-D warnings` (clean), `RUSTDOCFLAGS=-D warnings cargo doc --no-deps` (clean).
The `generated-contract` check passes unchanged: `protos.ethos` declares the
public data anatomy, which this change does not alter — the same types, the same
variants, the same positions.

## Sources

- `/home/li/primary/Vision/protos.md` — read whole; the authority for the
  delimiters, the escape rule, the layers and canonical print.
- `/home/li/primary/flows/f6db8d/reports/substrate-audit.md` §1.1, §1.2, §1.7 —
  the claims fixed here, each witnessed by the audit subflow, not by this flow.
- `/home/li/primary/flows/f6db8d/witnesses/substrate/probes.md` — the audit's
  reproductions; not re-run here, since the new property tests reproduce the
  same failure from inside the repository's own gate.
- `/home/li/primary/flows/f6db8d/log.md` — the main flow's wave 1 dispatch,
  which places datom-codec with a sibling subflow.
- `orchestrate 'Observe.Locks'`, observed twice — Lock 1105 acquired for this
  work; Lock 1107 `DatomCodecSubstrateFixes` observed held by f6db8d over
  datom-codec, and Lock 1106 `EthosZeroDefectFix` over ethos-zero.
- The repository itself at `b543678` and the gate output above — this flow's own
  observations.
