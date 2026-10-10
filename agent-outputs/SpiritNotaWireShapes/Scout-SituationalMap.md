# Scout Situational Map: Spirit 0.18.1 NOTA Wire Shapes (signal + meta sockets)

## Task and scope

Map the EXACT NOTA wire shapes accepted by the deployed `spirit` CLI (signal
socket) and `meta-spirit` CLI (meta socket) for Spirit "0.18.1", source-reading
only. No CLI was run against the live store. Covers: ChangeCertainty, Count,
Observe (query + reply), record reply shape, CollectRemovalCandidates,
Remove/Retire existence, and deployed store/socket/archive paths.

## Provenance and version pinning (read this first)

The brief names "0.18.1". The wire shapes live in two git-dependency contract
crates, not in the `spirit` repo directly. The pinning facts:

- `spirit` repo working tree at `/home/li/primary/repos/spirit` is at
  `version = "0.19.0"` (Cargo.toml line 1 region; HEAD commit `43d6a06`).
  Commit `f64bc8a` is the literal `spirit: 0.18.1` commit (confirmed:
  `git show f64bc8a:Cargo.toml` → `version = "0.18.1"`).
- Signal contract crate `signal-spirit`: BOTH 0.18.1 and 0.19.0 Cargo.lock pin
  the SAME rev `5d0905a7aa8c43951253b86193d76be67a89a945`. So the signal-socket
  NOTA shapes are byte-identical between 0.18.1 and 0.19.0. The vendored
  checkout is `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/`.
- Meta contract crate `meta-signal-spirit`: 0.18.1 pins rev
  `83415f2203cccde02290258f28dfac8152857f82`; 0.19.0 pins
  `98704a3573cd22aec80349b6b16b82fb2ada6499`. THESE DIFFER. The meta `Input`
  enum gained `ObserveHead` and `ObserveHeadObject` in the 0.19.0 rev. For
  0.18.1 the meta `Input` is exactly `Configure | Import |
  CollectRemovalCandidates` (no ObserveHead). All meta shapes below are read
  from the 0.18.1 rev `83415f2` at
  `/home/li/.cargo/git/checkouts/meta-signal-spirit-218ef8a834c9b65d/83415f2/`.
- The `spirit/src/schema/sema.rs` and `spirit/src/schema/nexus.rs` files are
  byte-identical across `f64bc8a..HEAD` (`git diff` → 0 lines). Only
  `engine.rs` differs (90 lines, behavioral, not wire-shape).

Interpretation: every NOTA wire string below is valid for the deployed 0.18.1
CLIs. The deployed binaries are stripped nix-store paths whose version label was
not recoverable from the `.drv`, so version identity rests on the lock-rev proof
above, not on a binary version string.

## NOTA projection rules observed (grounding for every example)

From the generated contract source and concrete test literals:

- A Rust enum's UNIT variant projects as a BARE ATOM: `Decision`, `Maximum`,
  `Zero`, `Any`, `None`. Not `(Decision)`.
- A single-field tuple newtype is TRANSPARENT in NOTA: `Certainty(Magnitude)`,
  `ExactCertainty(Certainty)`, `Observe(Query)`, `Count(Query)`,
  `ChangeCertainty(CertaintyChange)`, `RecordIdentifier(String)` all flatten —
  the wrapper name does not appear; only its inner projection does.
- A multi-field struct projects as a POSITIONAL record `(f1 f2 ...)` in
  declaration order.
- A `Vec<T>` projects as `[a b c]` (square-bracket list); empty is `[]`.
- An enum variant carrying data projects as `(VariantName <payload>)`, e.g.
  `(Full [...])`, `(Some Constraint)`, `(AtLeastCertainty Minimum)`,
  `(Exact Zero)`.
- `Option<T>` projects as `None` or `(Some <T>)` (see `SelectedKind` field).

Concrete witness of these rules (a real `Record` wire literal in
`/home/li/primary/repos/spirit/tests/socket_negative.rs:9`):

```
(Record (([(Technology (Software (Intelligence AgentSystems)))] Decision [text must not be daemon wire] Maximum Minimum Zero []) ([text must not be daemon wire] None)))
```

Here the inner `Entry` is `([domains] kind [description] certainty importance
privacy [referents])` with `Maximum Minimum Zero` = the three Magnitude fields
projected as bare atoms.

## How each CLI frames the wire (the outer envelope)

OBSERVED FACT — the CLIs parse the user's NOTA string DIRECTLY as the socket's
top-level `Input` enum; there is NO extra outer `Operation`/`Maintenance`/`Input`
wrapper to type yourself. The variant name IS the record head.

- `spirit` CLI: `/home/li/primary/repos/spirit/src/bin/spirit.rs:101-103` —
  `self.text.parse::<Input>()` where `Input` is
  `spirit::schema::signal::Input` (re-export of `signal_spirit::schema::signal::Input`).
  Socket env var `SPIRIT_SOCKET`, CLI fallback default `/tmp/spirit.sock`
  (spirit.rs:38). Inline NOTA arg or `--nota-file`/signal-file are read the
  same way (spirit.rs:71-89).
- `meta-spirit` CLI: `/home/li/primary/repos/spirit/src/bin/meta-spirit.rs:70-71`
  — `self.text.parse::<MetaInput>()` where `MetaInput` is
  `spirit::schema::meta_signal::Input` (re-export of
  `meta_signal_spirit::schema::meta_signal::Input`). Socket env var
  `SPIRIT_META_SOCKET`, CLI fallback default `/tmp/meta-spirit.sock`
  (meta-spirit.rs:32-33).

The signal `Input` enum (the full operation set) is at
`signal-spirit .../schema/signal.rs:1960-1984`:
`State, Record, Propose, Clarify, Supersede, Retire, ResolveClarification,
Observe, PublicTextSearch, PublicRecords, PrivateRecords, Lookup, Count,
ChangeCertainty, BumpImportance, ChangeRecord, RegisterReferent, LookupStash,
Tap, Untap, SubscribeIntent, Version, Marker`.

The meta `Input` enum (0.18.1) is at
`meta-signal-spirit .../schema/meta_signal.rs:301-305`:
`Configure, Import, CollectRemovalCandidates`.

## 1. ChangeCertainty (signal socket)

Source types (signal.rs):
- `Input::ChangeCertainty(ChangeCertainty)` (line 1974)
- `pub struct ChangeCertainty(CertaintyChange);` (line 266) — transparent
- `pub struct CertaintyChange { record_identifier: RecordIdentifier, certainty: Certainty }` (lines 1565-1568)
- `pub struct RecordIdentifier(String);` (line 578) — transparent; id is a BARE ATOM
- `pub struct Certainty(Magnitude);` (line 1206) — transparent
- `pub enum Magnitude { Zero, Minimum, VeryLow, Low, Medium, High, VeryHigh, Maximum }` (lines 1943-1952)

EXACT input NOTA (head is `ChangeCertainty`, NOT wrapped in any other enum; the
`CertaintyChange` record projects positionally as `(<id> <Magnitude>)`):

```
(ChangeCertainty (<record-identifier> <Magnitude>))
```

Concrete working literal (witness `tests/generated_signal_plane.rs:337,348` —
round-trips through `parse::<Input>()` and `to_string()`):

```
(ChangeCertainty (003g Zero))
```

So the brief's guessed shape `(ChangeCertainty (<id> <Magnitude>))` is CORRECT.
The id is a bare atom (the record identifier string, e.g. `003g`); the Magnitude
is a bare atom from the 8-value set above. There is NO outer `Input`/`Operation`
wrapper.

Reply: `Output::CertaintyChanged(CertaintyChanged)` →
`CertaintyChanged(CertaintyChangeReceipt)` →
`CertaintyChangeReceipt { record_identifier: RecordIdentifier, certainty: Certainty }`
(signal.rs:1576-1579). Projects as `(CertaintyChanged (<id> <Magnitude>))`.

## 2. Count (signal socket)

Source: `Input::Count(Count)` (signal.rs:1973); `pub struct Count(Query);`
(line 258) — transparent, so a Count takes a FULL 8-field Query (NOT an empty
arg).

EXACT input NOTA:

```
(Count (<8-field-query>))
```

Concrete working literal (witness `tests/nix_integration.rs:723`):

```
(Count ((Full [(Technology (Software (Operations Deployment)))]) Any Any Any (Some Decision) (Exact Zero) (AtLeastCertainty Minimum) Any))
```

Reply: `Output::RecordsCounted(RecordsCounted)` (signal.rs:2004) →
`RecordsCounted(CountedRecords)` (line 418) → `CountedRecords(RecordCount)`
(line 734) → `RecordCount(Integer)` (line 602). All transparent, so it projects
as a single nested integer. Witness `tests/operator_271_closed_claims.rs:195,412`
asserts the reply text contains `RecordsCounted CountedRecords` with value `4`.

EXACT reply NOTA shape:

```
(RecordsCounted <N>)
```

where `<N>` is a bare u64 (e.g. `(RecordsCounted 4)`). The brief's expectation
`(RecordsCounted N)` is correct.

## 3. Observe (signal socket) — the 8-field Query

Source: `Input::Observe(Observe)` (signal.rs:1968); `pub struct Observe(Query);`
(line 218) — transparent. The `Query` struct (signal.rs:1878-1887), fields IN
ORDER:

1. `domain_match: DomainMatch`
2. `keyword_match: KeywordMatch`
3. `text_match: TextMatch`
4. `referent_selection: ReferentSelection`
5. `selected_kind: SelectedKind`  (`SelectedKind(Option<Kind>)`, line 1859 → `None` or `(Some <Kind>)`)
6. `privacy_selection: PrivacySelection`
7. `certainty_selection: CertaintySelection`
8. `importance_selection: ImportanceSelection`

Field-variant projections:
- `DomainMatch` (lines 1095-1099): `Any` | `(Partial [<DomainScope>...])` |
  `(Full [<DomainScope>...])`. `Partial(DomainScopes)`, `Full(DomainScopes)`,
  `DomainScopes` is a Vec of `DomainScope`, transparent → `[...]`.
- `KeywordMatch` (1151-1155): `Any` | `(AnyKeyword [<Keyword>...])` | `(AllKeywords [...])`.
- `TextMatch` (1179-1182): `Any` | `(ContainsText <SearchText>)`.
- `ReferentSelection` (1123-1127): `Any` | `(AnyReferent [...])` | `(AllReferents [...])`.
- `SelectedKind` (1859): `None` | `(Some <Kind>)` where
  `Kind = Decision | Principle | Correction | Clarification | Constraint` (1920-1926).
- `PrivacySelection` (1222-1227): `Any` | `(Exact <Magnitude>)` |
  `(AtMost <Magnitude>)` | `(AtLeast <Magnitude>)`. (Inner `Exact(Privacy)`,
  `Privacy(Magnitude)` both transparent → bare Magnitude atom.)
- `CertaintySelection` (1259-1264): `Any` | `(ExactCertainty <Magnitude>)` |
  `(AtMostCertainty <Magnitude>)` | `(AtLeastCertainty <Magnitude>)`. (Inner
  `ExactCertainty(Certainty)`, `Certainty(Magnitude)` transparent.)
- `ImportanceSelection` (1296-1301): `Any` | `(ExactImportance <Magnitude>)` |
  `(AtMostImportance <Magnitude>)` | `(AtLeastImportance <Magnitude>)`.

The certainty-filter variant names the brief asked about are exactly
`AtLeastCertainty` and `ExactCertainty` (and `AtMostCertainty`), each taking a
bare Magnitude atom.

### Requested concrete examples

"Observe all records with certainty at least VeryLow" (broadest match on every
other field). The certainty filter is field 7 = `(AtLeastCertainty VeryLow)`;
all other fields set to their widest `Any`/`None`:

```
(Observe (Any Any Any Any None Any (AtLeastCertainty VeryLow) Any))
```

"Observe all records with certainty exactly Zero":

```
(Observe (Any Any Any Any None Any (ExactCertainty Zero) Any))
```

Witnessed pattern (real test literal `tests/process_boundary.rs:1032`,
round-tripped through the daemon) shows the exact field layout with both an
`ExactCertainty` and another field non-`Any`:

```
(Observe ((Full [(Information Documentation)]) Any Any Any (Some Correction) (Exact Zero) (ExactCertainty Zero) Any))
```

and (line 647) the `AtLeastCertainty` form:

```
(Observe ((Full [(Information Documentation)]) Any Any Any (Some Constraint) (Exact Zero) (AtLeastCertainty Minimum) Any))
```

INTERPRETATION / CAUTION on the all-`Any` examples: the all-`Any`/`None`
examples I give are constructed by reading each field's `Any`/`None` variant
from source, not copied from a test literal. Every test literal in the tree
pins `privacy_selection` to `(Exact Zero)` (the daemon's
`default_observation_privacy`, lib.rs:733-735) rather than `Any`. The all-`Any`
forms are valid NOTA per the grammar, but if you want a value the daemon's own
default-observation path emits, field 6 is `(Exact Zero)` and field 7 default is
`(AtLeastCertainty Minimum)` (`default_observation_certainty`, lib.rs:750-751).
To dump records at certainty exactly Zero you specifically override field 7 to
`(ExactCertainty Zero)`; note the default privacy floor `(Exact Zero)` only
surfaces nominal-privacy records — to see all privacies use field 6 = `Any`.

## 4. Observe reply shape

Source chain: `Output::RecordsObserved(RecordsObserved)` (signal.rs:2001) →
`RecordsObserved(ObservedRecords)` (line 394) → `ObservedRecords(RecordSet)`
(line 704) → `RecordSet(Vec<ObservedRecord>)` (line 1903) →
`ObservedRecord { record_identifier: RecordIdentifier, entry: Entry }`
(lines 712-715). `Entry` (lines 1541-1549) fields IN ORDER:

```
Entry = (domains kind description certainty importance privacy referents)
      = ([<Domain>...] <Kind> <description-text> <Magnitude> <Magnitude> <Magnitude> [<Referent>...])
```

So each returned record projects (within the reply list) as:

```
(<record-identifier> ([<domains>] <Kind> [<description>] <certainty-Magnitude> <importance-Magnitude> <privacy-Magnitude> [<referents>]))
```

and the whole reply is:

```
(RecordsObserved [ (<id1> <entry1>) (<id2> <entry2>) ... ])
```

Field-by-field for the brief's ask: id = `RecordIdentifier` (bare atom);
domains = Vec of `Domain` (square-bracket list of domain-scope records);
kind = bare `Kind` atom; description = `Description(String)` (bracketed text);
certainty / importance / privacy = bare `Magnitude` atoms (note the wire ORDER
is certainty, importance, privacy); referents = Vec of `Referent` (string) as a
square-bracket list. The `Entry` description and string fields are the
`[ ... ]`-bracketed text seen in the `socket_negative.rs` witness above. NOTE:
the `Entry` carries NO separate "referents count"; `referents` is the trailing
Vec field.

## 5. CollectRemovalCandidates (META socket, 0.18.1)

Source chain (meta_signal.rs at rev 83415f2):
- `Input::CollectRemovalCandidates(CollectRemovalCandidates)` (line 304)
- `CollectRemovalCandidates(CollectRemovalCandidatesRequest)` (line 51) — transparent
- `CollectRemovalCandidatesRequest(RemovalCandidateCollection)` (line 282) — transparent
- `RemovalCandidateCollection { record_query: RecordQuery, justification: Justification }`
  (signal.rs:1333-1336)
- `RecordQuery(Query)` (signal.rs:1344) — transparent, so the query is the SAME
  8-field Query as Observe/Count
- `Justification { testimony: Testimony, reasoning: Reasoning }` (signal.rs:829-832);
  `Testimony(Vec<VerbatimQuote>)` (813); `VerbatimQuote { quote_text: QuoteText,
  optional_antecedent: Option<Antecedent> }` (802-805) → `([quote] None)` or
  `([quote] (Some [antecedent]))`; `Reasoning(String)` (821).

So the META input projects with TWO nested layers transparent and then the
2-field `RemovalCandidateCollection` record:

```
(CollectRemovalCandidates (<8-field-query> (<testimony> <reasoning>)))
```

where `<testimony>` is `[ ([quote-text] None) ... ]` and `<reasoning>` is
`[reasoning-text]`.

EXACT working NOTA to "collect (archive-then-retract) all records at certainty
exactly Zero" (the removal-candidate floor). The query uses
`(ExactCertainty Zero)` in field 7 (this is exactly what the daemon's
`removal_candidate_certainty()` helper builds, lib.rs:754-755). All-wide form:

```
(CollectRemovalCandidates ((Any Any Any Any None Any (ExactCertainty Zero) Any) ([([collect zero-certainty removal candidates] None)] [collect zero-certainty removal candidates])))
```

Witness of the query/justification construction (not the NOTA literal, but the
typed builder the test uses, `tests/collect_removal_candidates.rs:87-112`):
`removal_candidate_query` sets `certainty_selection =
CertaintySelection::removal_candidate_certainty()` = `(ExactCertainty Zero)`,
`privacy_selection = default_observation_privacy()` = `(Exact Zero)`,
`selected_kind = (Some Decision)`, `domain_match = (Full [...])`,
`importance_selection = Any`; the `Justification` is one `VerbatimQuote` with a
`None` antecedent plus a `Reasoning` string.

Reply: `Output::RemovalCandidatesCollected(RemovalCandidatesCollected)`
(meta_signal.rs:316) → `RemovalCandidatesCollected(RemovalCandidatesCollectedReceipt)`
(line 75) → `RemovalCandidatesCollectedReceipt { removal_candidates_collection:
RemovalCandidatesCollection, database_marker: DatabaseMarker }` (lines 290-293).
`RemovalCandidatesCollection { removal_archive_records, removed_identifiers,
skipped_removal_candidates }` (signal.rs:1428-1432). Projects as:

```
(RemovalCandidatesCollected (([<archived-record>...] [<removed-id>...] [<skipped>...]) (<commit-sequence> <state-digest>)))
```

### Archive-then-retract confirmation (does it archive into spirit.archive.sema first)

YES — confirmed from source:
- `spirit/src/engine.rs:776-806`, `collect_removal_candidates`: doc says
  "archive every record matching the supplied query into the SEPARATE archive
  database ... then physically retract it from the live log. This is the ONLY
  physical-deletion path; it runs with NO guardian, on the owner-only meta
  plane". It calls `store().collect_removal_candidates(...)`.
- `spirit/src/store/mod.rs:623-665`, the store primitive: for each matching
  record it calls `archive.archive_record(...)` FIRST, and only on `Ok(())`
  calls `self.remove(&identifier)` (lines 637-638). An archive failure produces
  a `SkippedRemovalCandidate` with reason `ArchiveFailed` and the record is NOT
  removed (lines 653-657). So archive strictly precedes retraction per record.
- The archive opens at the owner-configured target; the DEFAULT archive path is
  derived as `<live-stem>.archive.sema` (`store/mod.rs:545-556`): live stem
  `spirit` → `spirit.archive.sema`. This matches the on-disk
  `/home/li/.local/state/spirit/spirit.archive.sema` (see section 7).

INTERPRETATION on "archive store name": the archive uses a sema-engine keyed
table and is unversioned (`store/archive.rs:24-26`). The LIVE store's
`RecordFamily::STORE_NAME` is `"spirit:sema"` (sema.rs:1115); I did not find a
distinct hardcoded archive store-name constant, so I treat the archive's
identity as the derived `spirit.archive.sema` FILE rather than a separate
internal store name. (Weak point flagged.)

## 6. Remove and Retire

- `Remove`: OBSERVED ABSENCE. There is NO `Remove` variant in the signal
  `Input` enum (signal.rs:1960-1984), the meta `Input` enum
  (meta_signal.rs:301-305), or anywhere in either schema file (`rg '\bRemove\b'`
  over both returned nothing). The brief's statement "Remove does NOT archive"
  cannot be confirmed because no `Remove` op exists; the operation that performs
  physical removal is `CollectRemovalCandidates` (meta socket), and it DOES
  archive first (section 5). The lower-level store method is `remove(...)`
  (store/mod.rs:1029), an internal helper that retracts from the live log; it is
  reached only through the archive-then-retract primitive and the
  supersede/clarify replacement paths, never as a standalone wire op.
- `Retire`: EXISTS on the SIGNAL socket. `Input::Retire(Retire)`
  (signal.rs:1966); `Retire(Retirement)` (line 202);
  `Retirement { record_identifier: RecordIdentifier, justification: Justification }`
  (signal.rs:1735-1738). EXACT input NOTA:

  ```
  (Retire (<record-identifier> (<testimony> <reasoning>)))
  ```

  Reply `Output::Retired(Retired)` → `Retired(RetirementReceipt)` →
  `RetirementReceipt(RecordIdentifier)` (lines 1746), projects
  `(Retired <record-identifier>)`. Retire is guardian-relevant: it carries a
  `Justification` and flows through the guardian admission boundary (the
  guardian rejection reasons in `GuardianRejectionReason`, signal.rs:1779-1800,
  include supersede/retire-adjacent reasons). INTERPRETATION: "Retire is
  guardian-gated/slow" is consistent with the source (it is a
  justification-bearing working-socket op subject to guardian admission), but I
  did NOT trace the engine arm that runs the guardian specifically for `Retire`
  in this pass, so the "slow / guardian-gated" claim is plausible-but-not-
  fully-traced. What IS firmly confirmed: Retire does NOT physically delete +
  archive; `CollectRemovalCandidates` is "the ONLY physical-deletion path"
  (engine.rs:779). Retire is a logical retirement (it produces an
  `IntentRetired` event, signal.rs:951).

## 7. Deployed store / socket / archive paths

CONFIRMED DIRECTLY from the deployed daemon configuration on disk. The
systemd user unit `~/.config/systemd/user/spirit-daemon.service` runs
`/nix/store/lqzm2lc8ar8f7qk19bkap3ghwsgalz10-spirit/bin/spirit-daemon` with
config arg
`/nix/store/hvj1par51fs5w3rrfbgp8rx2j09yqq9m-spirit-daemon-configuration/spirit.config.rkyv`.
The deployed config rkyv (read via `strings` on the active
`/home/li/.local/state/spirit/spirit.config.rkyv`) contains these path literals:

- signal socket: `/home/li/.local/state/spirit/spirit.sock`
- meta socket:   `/home/li/.local/state/spirit/meta-spirit.sock`
- live store:    `/home/li/.local/state/spirit/spirit.sema`
- (also `/home/li/.local/state/agent/agent.sock` = guardian agent socket; model
  refs `criomos-local` / `gemma-4-26b-a4b`)

On-disk `ls /home/li/.local/state/spirit/` confirms all four exist live:
`spirit.sock` (socket), `meta-spirit.sock` (socket), `spirit.sema` (5.1 MB,
the live store), `spirit.archive.sema` (774 KB, the archive). The archive path
is NOT in the config strings — it is the DERIVED default `<live-stem>.archive.sema`
(store/mod.rs:545-556) sitting next to the live store, which is why it lands at
`/home/li/.local/state/spirit/spirit.archive.sema`. The directory also holds
removal/gc backups (`spirit.archive.sema.preremoval-631-...`,
`spirit.archive.sema.gc-prebackup-zerocert-...`), consistent with prior
zero-certainty CollectRemovalCandidates runs.

So all four brief-asserted paths are CONFIRMED:
- live: `/home/li/.local/state/spirit/spirit.sema` ✓
- archive: `/home/li/.local/state/spirit/spirit.archive.sema` ✓ (derived)
- signal sock: `/home/li/.local/state/spirit/spirit.sock` ✓
- meta sock: `/home/li/.local/state/spirit/meta-spirit.sock` ✓

NOTE on CLI defaults vs deployed: the CLIs' built-in fallback socket defaults
are `/tmp/spirit.sock` and `/tmp/meta-spirit.sock`. To hit the DEPLOYED daemon
you must export `SPIRIT_SOCKET=/home/li/.local/state/spirit/spirit.sock` and
`SPIRIT_META_SOCKET=/home/li/.local/state/spirit/meta-spirit.sock` (or rely on
whatever environment the deployed shell already sets). This is a real
gotcha: a bare `spirit '(Count ...)'` with no env hits `/tmp`, not the live
store.

## Files and commands consulted

- `/home/li/primary/repos/spirit/src/bin/spirit.rs` (CLI parse → `Input`)
- `/home/li/primary/repos/spirit/src/bin/meta-spirit.rs` (CLI parse → `MetaInput`)
- `/home/li/primary/repos/spirit/src/schema/sema.rs` (the sema re-export layer)
- `/home/li/primary/repos/spirit/src/engine.rs:776-813` (collect_removal_candidates, guardian/archive doc)
- `/home/li/primary/repos/spirit/src/store/mod.rs:545-556, 623-665, 1029` (archive path derivation; archive-then-retract; remove)
- `/home/li/primary/repos/spirit/src/store/archive.rs` (separate archive db, unversioned)
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/schema/signal.rs` (ALL signal wire types; rev pinned by both 0.18.1 and 0.19.0)
- `/home/li/.cargo/git/checkouts/signal-spirit-44a4bfaa970650f7/5d0905a/src/lib.rs:730-776` (default/removal-candidate selection helper values)
- `/home/li/.cargo/git/checkouts/meta-signal-spirit-218ef8a834c9b65d/83415f2/src/schema/meta_signal.rs` (0.18.1 meta wire types)
- `/home/li/primary/repos/spirit/tests/socket_negative.rs:9,37` (concrete Record NOTA)
- `/home/li/primary/repos/spirit/tests/process_boundary.rs:647,1032` (concrete Observe NOTA, both certainty forms)
- `/home/li/primary/repos/spirit/tests/nix_integration.rs:723` (concrete Count NOTA)
- `/home/li/primary/repos/spirit/tests/generated_signal_plane.rs:337,348` (concrete ChangeCertainty NOTA round-trip)
- `/home/li/primary/repos/spirit/tests/operator_271_closed_claims.rs:179,195,412` (Output enum order; RecordsCounted reply value)
- `/home/li/primary/repos/spirit/tests/collect_removal_candidates.rs:87-112,124-164` (removal query + justification builder; archive-then-retract test)
- Git: `git diff f64bc8a..HEAD -- src/schema/sema.rs src/schema/nexus.rs` (0 lines); `git show f64bc8a:Cargo.lock` (0.18.1 lock revs)
- `~/.config/systemd/user/spirit-daemon.service` (ExecStart, config arg)
- `strings /home/li/.local/state/spirit/spirit.config.rkyv` (deployed paths)
- `ls -la /home/li/.local/state/spirit/` (live sockets + .sema files)

## Checks run and results

- `git diff f64bc8a..HEAD` on `sema.rs`/`nexus.rs` → 0 lines (wire shapes
  identical 0.18.1→0.19.0 on signal plane). PASS.
- `rg '\bRemove\b'` over signal.rs + meta_signal.rs → no matches (no Remove op).
- meta `Input` enum diff 83415f2 vs 98704a3 → 0.19.0 adds `ObserveHead`,
  `ObserveHeadObject`; 0.18.1 has only `Configure/Import/CollectRemovalCandidates`.
- Deployed config strings → confirmed all four paths; on-disk `ls` → confirmed
  all four files/sockets exist.
- Did NOT run `spirit`/`meta-spirit` against the live store (per brief).

## Blockers, unknowns, follow-up

- WEAK: the deployed binary's literal version label (0.18.1 vs 0.19.0) is NOT
  recoverable from the stripped nix-store binary or its `.drv` env. Version
  identity rests on the lock-rev proof. If you need certainty about which `spirit`
  binary is live, note the systemd unit binds the daemon at store path
  `lqzm2lc8...-spirit`, while the profile `spirit` CLI is a DIFFERENT store path
  `pj3avhr4...-spirit`; both could be built from either tag. The signal wire is
  identical across the two tags regardless, so the signal NOTA strings are safe;
  the only version-sensitive surface is the META `Input` set (ObserveHead exists
  only in 0.19.0). If the deployed daemon is actually 0.19.0, the meta socket
  ALSO accepts `ObserveHead`/`ObserveHeadObject`; the three ops documented here
  work on both.
- WEAK: archive internal store-name constant not located; archive identity given
  as the derived file path. Verify if a downstream caller needs a store name
  string rather than a file path.
- NOT FULLY TRACED: the engine arm that runs the guardian specifically for the
  signal `Retire` op (the "guardian-gated/slow" claim is plausible but
  unverified in this pass). What is firmly source-backed: Retire is logical (no
  physical delete), CollectRemovalCandidates is the only physical-deletion path
  and archives first with NO guardian.
- The all-`Any`/`None` Observe and CollectRemovalCandidates examples are
  grammar-constructed from per-field source, not lifted from a test literal;
  real test literals always pin `privacy_selection` to `(Exact Zero)`. Both
  forms are valid NOTA.
