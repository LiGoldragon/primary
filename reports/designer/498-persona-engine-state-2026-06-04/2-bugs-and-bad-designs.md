---
title: 498/2 - Glaring bugs and bad designs still unaddressed on main
role: designer
variant: Audit
date: 2026-06-04
topics: [bugs, bad-designs, schema-next, schema-rust-next, spirit, persona-spirit, triad-runtime, dual-engine, abstraction-debt, repetition]
description: |
  Slice 2 of the state-of-the-engine assessment. Consolidates every known
  bug and bad design from designer 495 (1-5), system-designer 59/3, and the
  repetition sweep, re-verifies each against current main (not the audit
  worktree), and prioritises. Headline correctness bug: the schema-next dual
  lowering engine still drops bare-header payloads on the registry path, with
  the equivalence test green only because its fixture carries no bare header.
  Everything else is structural bad-design / abstraction debt; three production
  persona-spirit dedups are already staged on an unmerged branch.
---

# Slice 2 — glaring bugs and bad designs still unaddressed on main

The psyche asked what bugs and bad designs they have not addressed. This
slice re-verified every known finding against current `main` HEAD in each
repo (the prior 495 audit cited line numbers from the audit worktree; I
re-ran every grep against the live checkout). The repo formerly called
`spirit-next` is now `/git/github.com/LiGoldragon/spirit` (record 1588
rename); its source still carries the `spirit-next` crate/binary names.

The verdict in one line: **one correctness bug** (the schema-next dual
lowering engine), and **everything else is structural bad-design /
abstraction debt** — none of which is yet on main. Three of the production
persona-spirit dedups are already written on an unmerged branch
(`spirit-repetition-cleanups`); the rest await either an operator pass or a
psyche decision.

## Severity ladder and what each column means

- **bug (correctness)** — produces wrong output / drops data. There is
  exactly one.
- **bad-design (structure)** — correct output, but the structure invites
  the next bug, costs tokens, or violates a ratified discipline.
- **ratified-to-fix** — the fix direction is already at calibrated
  certainty in Spirit; the operator can act without a new decision.
- **needs-decision** — the shape of the fix is genuinely open and the
  psyche owns it.

## P1 — the one correctness bug

### B1. schema-next dual lowering engine drops bare-header payloads (the headline)

**bug (correctness). ratified-to-fix. severity: HIGH — silent wrong output.**

Verified present on `schema-next` main (HEAD `bff3d2b`). Two parallel
lowering engines share no code and disagree on bare-header payload
resolution:

- The typed source path (`SchemaSource::to_asschema`, `src/source.rs:112`)
  builds a `SourceTypeResolver::from_source` (`src/source.rs:965`) that
  collects every namespace name plus inline-declaration names up front, so a
  bare PascalCase header variant resolves to its same-named namespace
  payload. This is the multi-pass resolution record 1556 ratifies.
- The registry document path (`SchemaEngine::lower_source` →
  `AssembledVariant::lower`, `src/declarative.rs:1846-1850`) lowers a bare
  PascalCase variant straight to `payload: None` with no resolver, no
  namespace lookup, no forward-reference pass:

```rust
} else if self.object.qualifies_as_pascal_case_symbol() {
    Ok(EnumVariant {
        name: self.object.schema_name()?,
        payload: None,
    })
}
```

The intent [when a bare root variant name resolves to a declaration in the
schema namespace, the variant carries that same-named payload type] (records
1555/1562) is implemented on exactly one of the two paths. For an identical
schema the registry path yields `payload=None` and the source path yields
`payload=Some(...)` — the 495/2 probe confirmed this and the code is
unchanged.

**Why the green test suite still hides it.** The equivalence witness
`schema_source_lowers_to_same_asschema_as_direct_source`
(`tests/source_codec.rs:26`) asserts `lower_source` (registry) == `source().lower()`,
but its fixture (`tests/fixtures/spirit-crate/schema/lib.schema`) opens with
ONLY parenthesised header forms — `[(Record Entry) (Observe Query)]` and
`[(RecordAccepted RecordIdentifier) (RecordsObserved RecordSet)]` — never a
bare header name. So the two paths agree there by construction. The
header-resolution witness `root_header_bare_names_resolve_to_exported_namespace_payloads`
(`tests/source_codec.rs:48`) exercises ONLY the source path
(`artifact.source().lower(...)`), never `lower_source`. No test in the suite
asserts both paths agree on a bare-header payload — that is precisely the
record-1565 constraint witness that would have caught this.

**Note — a new `lower_source_with_resolver` (`engine.rs:362`) does NOT close
the gap.** Its `resolver` is an `ImportResolver` (cross-schema import
resolution), not a namespace type-resolver for bare-header payloads. The
registry path still routes through `lower_root_enum` → `AssembledVariant::lower`
and still hits the `payload: None` arm.

**Fix (ready for operator now).** Two-part: (1) route the registry path's
bare-PascalCase arm through the same `SourceTypeResolver` the source path
uses — or, per 495/2's preferred dissolution, make `SchemaSource` the one
lowering front-end and retire `lower_source`/`lower_document` as a second
engine; (2) land the missing witness — extend the equivalence test fixture
with a bare-header variant (or add a dedicated test) so both paths must agree
on the resolved payload. The dual-engine retirement is the structural cure
(it also dissolves B6); the resolver-route + witness is the minimal fix.
This is the bead-candidate P1.

## P2 — structural bad designs that invite the next bug

### B2. schema-rust-next emission is 504 hand-spelled `self.line(format!())` calls

**bad-design (structure). ratified-to-fix (RustItem model, record 1576). severity: HIGH leverage.**

Verified: `grep -c "self.line(" src/lib.rs` = **504**, in a 2687-line file
with no RustItem token model present (`grep` for `struct RustItem` /
`RustImplBlock` / `RustMatch` returns nothing). The declaration layer
(`RustModule`/`RustDeclaration`/`RustEnum`) honors the data-before-text
discipline (INTENT.md:238), but the ~80% of output that is impls / traits /
match arms is rendered by direct string templating with hand-counted
indentation (`"    "`, `"        "`, `"            "` literally spelled out).
The RustItem emission token model is **ratified** (record 1576/1584) but
**unbuilt**. This is the single highest-leverage refactor in the stack: it is
where every future emission bug will live. Tier-3 operator refactor (it is
production emission-engine code, not a designer port).

### B3. The triad daemon runner is hand-written in spirit; triad-runtime should own it

**bad-design (structure). ratified-to-fix (runner extraction, record 1574). severity: MEDIUM, latent-cross-component.**

Verified: `triad-runtime/src/` holds only `lib.rs` + `trace.rs` — no
runner, no `SignalDaemon`, no `triad_main!` (grep returns nothing). The whole
runner surface is hand-written in `spirit/src/daemon.rs:152` (`Daemon::run`):
accept loop, parent-directory creation, stale-socket removal, `Arc` sharing,
per-connection frame exchange, `eprintln!` error sink. Only `self.engine()`
and `engine.handle(input)` are component-specific. The generic triad runner
is **ratified** (record 1574) but **unbuilt**. Today there is exactly one
consumer (`spirit`), so the disciplined trigger — extract on the second
consumer — has not fired; but the runner is named as the destination in both
`triad-runtime` and `spirit` ARCHITECTURE files. Tier-3 operator feature.

### B4. Length-prefix framing copied across two crates; single-NOTA-argument hand-rolled twice

**bad-design (structure). ratified discipline; noun unratified. severity: MEDIUM.**

Two copies of the same 4-byte big-endian length-prefix framing, with the
constant declared twice: `triad-runtime/src/trace.rs:14`
(`const LENGTH_PREFIX_BYTE_COUNT: usize = 4;`) and
`spirit/src/transport.rs:10` (identical). `write_frame`/`read_frame` vs
`TraceFrame::to_bytes`/`read_from` are the same algorithm with the same
FrameTooLarge guard duplicated. Separately, the AGENTS.md single-NOTA-argument
rule is hand-rolled twice inside spirit: `daemon.rs:133`
(`DaemonCommand::single_argument`, typed error) and `bin/spirit-next.rs:44`
(`SpiritNextCli::single_argument`, `Box<dyn Error>` + string-literal error).
Both fold into the runner extraction (B3): a `LengthPrefixedFrame` codec and a
`ComponentArgument` noun in triad-runtime. The framing-codec and
component-argument nouns are UNRATIFIED-PROPOSE; the single-argument *rule* is
a ratified AGENTS.md hard override.

### B5. Four spirit error enums hand-write Display + Error + From instead of thiserror

**bad-design (structure). ratified-to-fix (thiserror is the named discipline). severity: MEDIUM, portable now.**

Verified: `spirit/Cargo.toml` does not depend on thiserror (`grep -c` = 0),
yet `triad-runtime` already uses it. The four spirit error enums hand-write
the full ceremony: `DaemonError` (`daemon.rs:26` Display, `:38` empty
`impl Error`, plus 7 `From` impls in that file), `DaemonCommandError`
(`daemon.rs:77/90`), `TransportError` (`transport.rs:31`), `ConfigurationError`
(`config.rs:105`). ~30 mechanical lines per enum that `#[error(...)]` +
`#[from]` + `#[derive(Error)]` dissolve. `skills/rust/errors.md` is canonical;
the spirit side is inconsistent with its own dependency tree. Tier-3 operator
fix, portable now.

### B6. schema-next: single-field→Newtype rule duplicated 3x; collection-reference lowering 3x

**bad-design (structure). ratified-to-fix (dissolve via one lowering front-end). severity: MEDIUM.**

The dual-engine root cause (B1) extends past the header arm. The
single-field→Newtype decision is spelled three times (`source.rs:475`,
`declarative.rs:1554`, `asschema.rs:1062`), and the `Vec`/`Optional`/`Map`
head dispatch three times (`source.rs:893`, `declarative.rs:1919`,
`asschema.rs:1106`). Each is a place the next `TypeReference` variant or rule
change must be made in triplicate or the paths diverge — the same latent
divergence class that became B1. The cure is the same: one lowering
front-end, or a single reference-lowering owner both engines call. Folds into
the B1 dissolution.

### B7. schema-rust-next: route() emission duplicated; three independent TypeReference walks; dead param

**bad-design (structure). ratified discipline; tier-3 cleanups. severity: LOW-MEDIUM.**

Verified on main: `emit_route_impl` (`lib.rs:1366`) and `emit_signal_frame_impl`
(`lib.rs:1390`) still emit a byte-identical `route()` match — one shared
`emit_route_method` dissolves it. Three hand-written recursive `TypeReference`
walks (`CollectionScan::collect_map_keys` `:680`, `references_private_type`
`:856`, `rust_type` `:2579`) want one `TypeReferenceWalk` / methods on
`TypeReference`. Dead parameter `let _ = type_name;` (`lib.rs:2223` in
`emit_split_sema_output_projection`) — drop the param and its two call-site
args. Also the lifecycle-hook trait preamble emitted 3x across the three
engine traits. All tier-3 operator cleanups; all subsumed once B2 (RustItem
model) lands.

## P2 — spirit (renamed spirit-next) pilot bad patterns

### B8. SpiritNextCli::run returns Box<dyn Error>; ConfigurationPath lossy; daemon stop() unreachable

**bad-design (structure). ratified discipline. severity: LOW-MEDIUM, portable now.**

All three verified on `spirit` main (HEAD `f95d74a`):

- `SpiritNextCli::run` returns `Box<dyn std::error::Error>`
  (`bin/spirit-next.rs:28`), as do `single_argument` (`:44`) and
  `read_single_argument` (`:51`). `skills/rust/errors.md` forbids
  `Box<dyn Error>` at a method boundary; the CLI wants a crate `Error` enum
  (argument-count / not-a-NOTA-value / parse / transport). The daemon side
  already does this with `DaemonCommandError`.
- `ConfigurationPath::new` does `path.as_ref().to_string_lossy().into_owned()`
  (`config.rs:20`) — a non-UTF-8 path is silently corrupted, and the
  wire/disk form is rkyv `Configuration`, so the lossy `String` is a real
  (narrow) wire hazard. `storage-and-wire.md` prescribes `WirePath(Vec<u8>)`.
- `Daemon::run` (`daemon.rs:152`) calls `engine.start()` then runs the accept
  loop forever; `engine.stop()` appears **nowhere** in `daemon.rs` (verified
  by grep). The loop only exits via the listener-error `Err` arm returning, so
  the record-1487 lifecycle stop hook is dead on the daemon path (exercised
  only in tests). A signal-handler → `engine.stop()` shutdown path makes the
  hook live. Not a correctness bug for the pilot (process exit releases redb),
  but it is the [release before notify] discipline unhonored.

These are portable tier-3 operator fixes; none needs a decision.

## P2/P3 — production persona-spirit repetition (system-designer 59/3)

Verified all four on `persona-spirit` main (HEAD `7233075`). **Important
staging note:** three of these are already written on the unmerged
`spirit-repetition-cleanups` branch (system-designer; awaiting operator
integration) — they are FIXED-ON-A-BRANCH, NOT-ON-MAIN, not unaddressed:

| Finding | On main? | On branch? |
|---|---|---|
| A1 civil-date algorithm x3 | yes | fixed (CivilInstant + From projections) |
| A3 five identical Infallible send-error helpers | yes | fixed (From<SendError<_, Infallible>>) |
| V2 argument-text free fn duplicated 2x | yes | fixed (SpiritArgument::into_nota_text) |
| A2 dispatch trace-shuttle x14 | yes | NOT on branch |
| A4 Effect <-> WorkingReply mirror | yes | NOT on branch |

### B9. Civil-date algorithm written 3x; five identical send-error helpers; argument-text 2x

**bad-design (structure). ratified discipline; FIXED ON BRANCH. severity: MEDIUM.**

Verified on main: the Howard Hinnant days-from-civil algorithm is
character-identical at `actors/clock.rs:91` (`CivilDate::from_unix_days`) and
`store.rs:480` (`HandoverCivilDate::from_unix_days`), plus the seconds-of-day
splitter copied in both `*Reading::from_unix_seconds`. Five
`SendError<_, Infallible>` → `Error::actor_runtime` helpers are identical
(`dispatch.rs:519-535`); only `store_send_error` (Error-reply, `:512`)
differs. The two `*_configuration_argument_text` free functions are
byte-identical (`daemon.rs` + `migration.rs`). **The
`spirit-repetition-cleanups` branch already fixes all three** (commits
`a030a10` CivilInstant, `efdc630` send-error From, `45e36cf`
SpiritArgument::into_nota_text). Action: operator integrates the branch —
this is a do-it-now bead, not a fresh design.

### B10. dispatch trace-shuttle x14; Effect mirrors WorkingReply

**bad-design (structure). A2 ratified-to-fix; A4 needs-decision. severity: MEDIUM.**

Verified on main and NOT on the cleanup branch:

- **A2** (`dispatch.rs`): the `snapshot → ask → into_parts → replace` shape
  repeats 14 times (verified: 14 `into_parts()`, 14 `self.trace.replace(trace)`).
  The verb belongs on `SharedTrace::ask_pipeline`. The refactor is
  behavior-preserving, but the generic bound across `Infallible`-reply and
  `Error`-reply actors is a real design choice — **partial-portable**, the
  operator can land it but should confirm the bound shape.
- **A4** (`observation.rs:39/91/119`): `enum Effect` (13 variants) is a
  hand-mirror of `WorkingReply`, with `from_reply` (`:91`) and `into_reply`
  (`:119`) as inverse 1:1 arm-for-arm maps (26 arms expressing one fact).
  `Effect` earns its existence via `ToSemaOutcome`, so the fix is
  `impl From` both ways AND asking whether the two should share a derive so
  the arm list is generated. **Blocked / needs-decision** — collapsing toward
  shared emission touches the `signal_channel!` schema surface (undecided
  whether the component-local executor enum should be schema-derived). This is
  the one persona-spirit repetition that needs a psyche decision.

## Consolidated priority list

| # | Finding | Class | File:line | Sev | Status |
|---|---|---|---|---|---|
| B1 | dual lowering engine drops bare-header payload | **bug** | `schema-next/src/declarative.rs:1846` | HIGH | ratified-to-fix; **P1 bead** |
| B2 | 504 self.line emission; no RustItem model | bad-design | `schema-rust-next/src/lib.rs` (504 calls) | HIGH | ratified (1576), unbuilt |
| B3 | runner hand-written in spirit | bad-design | `spirit/src/daemon.rs:152` | MED | ratified (1574), unbuilt |
| B4 | length-prefix 2x; single-arg 2x | bad-design | `transport.rs:10`/`daemon.rs:133`/`spirit-next.rs:44` | MED | rule ratified; noun unratified |
| B5 | 4 error enums hand-write Display/Error/From | bad-design | `spirit` daemon/transport/config | MED | ratified discipline; portable |
| B6 | newtype rule 3x; collection lowering 3x | bad-design | `schema-next` source/declarative/asschema | MED | folds into B1 |
| B7 | route() 2x; 3 TypeReference walks; dead param | bad-design | `schema-rust-next/src/lib.rs:1366/2223` | LOW-MED | folds into B2 |
| B8 | Box<dyn Error>; lossy path; stop() dead | bad-design | `spirit/src/bin/spirit-next.rs:28`, `config.rs:20`, `daemon.rs:152` | LOW-MED | portable |
| B9 | civil-date 3x; send-error 5x; arg-text 2x | bad-design | `persona-spirit` clock/store/dispatch | MED | **fixed on branch**, integrate |
| B10 | trace-shuttle 14x (A2); Effect mirror (A4) | bad-design | `persona-spirit/src/actors/dispatch.rs`, `observation.rs:39` | MED | A2 portable; A4 needs-decision |

## What is genuinely NEW vs consolidated

This slice found no new correctness bug beyond B1. Every structural item was
already named in 495 or 59/3; the slice's value is (a) re-verifying all of
them against current main rather than the audit worktree, and (b) the
staging clarity — B9 is already written on a branch and is integration work,
not design work; B10/A4 and B1's witness are the only items left that touch a
genuine decision or a schema surface. The headline remains: one silent
correctness bug (B1), and a large but ratified pile of abstraction debt whose
two keystones (RustItem model B2, triad runner B3) are decided-but-unbuilt.
