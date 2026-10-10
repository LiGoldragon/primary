# Slice A4 — triad shape, naming, NOTA discipline, manifestation drift

*Kind: design-to-implementation audit · Topics: spirit-triad, meta-signal-rename, naming, nota-discipline, manifestation-currency · 2026-06-04 · system-designer lane (read-only audit sub-agent)*

## Intent Anchors

[The owner-signal to meta-signal rename is now active work, not tentative: run a deep rename pass that audits and updates the workspace guidance and affected contract repositories from owner-signal-* policy-contract naming to meta-signal-* where the policy-signal role is meant.] (Spirit 1567 High)

[Component triad means daemon + working signal + policy signal; the policy signal is the meta-signal-<component> contract.] (AGENTS.md hard override)

[Spirit gains an explicit CollectRemovalCandidates operation as a Signal root collecting all Zero-certainty records and emitting their summary form to a configurable output target. Separates discovery/extraction from the destruction concern in Remove.] (Spirit 1547 High)

[Operations that extract or emit content accept a customizable output-target enum as the final field. Variants: Stdout, Stderr, File(path). Not an error channel. Keeps the wire interface uniform across extraction operations.] (Spirit 1548 High)

[Spirit defines a small-record data type carrying core load-bearing fields — identifier, topics, kind, description summary, magnitude, daemon-stamped date and time. It is what variant-ladder short-form reads and CollectRemovalCandidates emit; what archiving and downstream tools consume.] (Spirit 1549 High)

[Spirit gains a RecordDefault short-form recording operation taking only fields agents commonly customize — topics, kind, description, magnitude — with defaults injected for the rest.] (Spirit 1550 High)

[Spirit operations should support a simpler-to-more-complex variant ladder — short forms with summary defaults for normal operations, complex forms with full metadata. Both shapes coexist as distinct operation roots; the complex root is canonical, the short root expands to a default form of the complex root.] (Spirit 1474 High)

[Medium certainty should be the normal default for routine Spirit captures unless the psyche wording, emphasis, repetition, or context justifies a higher or lower certainty.] (Spirit 1570 High)

[Landed means on main. Work on a branch has no material existence. Agents must never report pushed or branch-resident work as landed.] (Spirit 1568 Maximum)

## What the Spirit "triad" actually is on disk

There are TWO parallel runtime implementations and FOUR contract/legacy checkouts under `/git/github.com/LiGoldragon/`. The brief named `persona-spirit` as the daemon+CLI; that is correct, but the canonical worked example cited throughout `skills/component-triad.md` is the *other* repo, `spirit-next`. Distinguishing them is load-bearing for every finding below.

| Repo | Role | Version | Status |
|---|---|---|---|
| `persona-spirit` | production daemon + thin CLI (`spirit`, `persona-spirit-daemon`) | 0.3.0 | live line; CollectRemovalCandidates landed on main |
| `signal-persona-spirit` | working signal contract | 0.3.0 | live line; CollectRemovalCandidates landed on main |
| `owner-signal-persona-spirit` | policy leg (OLD name) | 0.1.0 | not renamed; 30+ inbound references |
| `spirit-next` | schema-derived runtime pilot (Signal/Nexus/SEMA) | 0.1.0 | engine work; canonical triad worked example |
| `core-signal-spirit` | legacy predecessor policy name | — | stale; should retire to meta-signal-spirit (operator 300) |

No `meta-signal-persona-spirit` and no `meta-signal-spirit` repo or directory exists. Both `ls` lookups returned "No such file or directory".

## (1) Triad shape — the meta-signal rename is NOT STARTED for the Spirit policy leg

The rule (component-triad.md §"meta-signal is the canonical policy-contract prefix"): the policy leg is `meta-signal-<component>`. Spirit 1567 (High) ratified the rename as active work. Operator report 300 (`reports/operator/300-meta-signal-rename-pass-2026-06-03.md`) ran the rename for the **upgrade** triad only and explicitly listed `owner-signal-persona-spirit` and `core-signal-spirit` in its "Remaining Gaps" section as untouched.

Verification: a grep for `meta-signal` / `meta_signal` / `MetaSignal` across all four spirit-triad repos (excluding `target/` and `Cargo.lock`) returns **zero matches**. A grep for `owner-signal` / `owner_signal` / `OwnerSignal` returns 30+ matches across `persona-spirit` alone, threaded through Cargo.toml, six source files, five test files, INTENT.md, ARCHITECTURE.md, README.md, and skills.md.

The rename is a decided, field-level change (the target name `meta-signal-persona-spirit` is fully determined by the rule — no psyche choice remains). It is therefore **portable** by the audit's portability rule. The concrete edit set, derived from the pattern operator 300 followed for the upgrade triad:

| Surface | Current | Target |
|---|---|---|
| Remote repo | `LiGoldragon/owner-signal-persona-spirit` | `LiGoldragon/meta-signal-persona-spirit` |
| Local checkout dir | `.../owner-signal-persona-spirit` | `.../meta-signal-persona-spirit` |
| Primary symlink | (none today) | `repos/meta-signal-persona-spirit` |
| Cargo `package.name` | `owner-signal-persona-spirit` | `meta-signal-persona-spirit` |
| Cargo `lib.name` | `owner_signal_persona_spirit` | `meta_signal_persona_spirit` |
| `persona-spirit/Cargo.toml:38` dep | `owner-signal-persona-spirit = { git = ".../owner-signal-persona-spirit.git" }` | `meta-signal-persona-spirit = { git = ".../meta-signal-persona-spirit.git" }` |
| Rust `use` sites | `use owner_signal_persona_spirit::{...}` in `daemon.rs:14`, `actors/policy.rs:7`, `actors/root.rs` (×6), `actors/owner.rs:4`, tests (`boundary.rs`, `actor_runtime.rs`, `daemon.rs`) | `use meta_signal_persona_spirit::{...}` |
| Schema identity | `owner-signal-persona-spirit:lib` | `meta-signal-persona-spirit:lib` |
| ARCHITECTURE / INTENT / README / skills prose | `owner-signal-persona-spirit` | `meta-signal-persona-spirit` |

This is a coordinated remote-rename + dependency-retarget slice that only an operator lane can land (it touches main across multiple repos and requires GitHub remote rename authority). A designer can stage the in-repo text edits on a feature branch; the remote rename and cross-repo Cargo retarget are operator integration. The `core-signal-spirit` legacy name is a separate retire-to-`meta-signal-spirit` slice (operator 300 named it).

Note the lingering ancestry-laden internal naming inside the policy crate that the rename should also fix: `owner-signal-persona-spirit/ARCHITECTURE.md` describes the request enum as `owner_signal_persona_spirit::Operation` and tests reference `OwnerSignalClient` (asserted-absent in `actor_runtime.rs:734`). The crate's own type is `Operation` (good — no ancestry), but the contract description and the `examples/canonical.nota` head names follow the owner verbs (`Start`, `Drain`, `Reload`, `Register`, `Retire`) which are fine and unaffected by the prefix rename.

## (2) Naming — the spirit triad source is clean

This is a strong positive finding. Scans for full-English-word violations and ancestry-carrying names across `persona-spirit/src`, `signal-persona-spirit/src`, and the schemas came back essentially empty:

- Abbreviations (`req`, `rep`, `cfg`, `ctx`, `addr`, `tmp`, `buf`, `idx`, `id` standalone): no genuine offenders. The only `id`-shaped hit is `caller.pid.value()` in `actors/root.rs:191`, where `pid` is a field on an external system-caller struct (`std`/OS-derived), exempt under naming.md exception 5.
- Ancestry: no `Intent*` types (the INTENT.md §"Naming inside this crate" rule is honored — `Entry` not `IntentEntry`, `RecordIdentifier` not `IntentRecordIdentifier`). No `recordIdentifier` field inside `Record`/`Entry`/`Summary`.
- The deployed schema's identifier vocabulary reads as English throughout: `RecordIdentifier`, `RemovalCandidateCollection`, `SkippedRemovalCandidate`, `RemovalCandidateSkipReason`, `RecordedTimeSelection`.

One naming observation worth flagging (not a violation, a design-coherence question): the working-signal schema (`signal-persona-spirit/spirit.schema:67`) defines the small/summary record as `RecordSummary`, while the policy contract has no equivalent. Spirit 1549 calls this the "small-record data type." `RecordSummary` is a good name — it does not carry the `Spirit`/`Persona` ancestry and describes what it IS. But see gap (4) below: the FIELDS do not yet match 1549's spec.

## (3) NOTA discipline — clean in source

- **No quotation-mark emission.** Greps for escaped-quote literals (`\"`) and for `write!`/`push_str`/`format!` carrying a quote across all three live spirit repos returned zero. Encoding routes through `nota-codec`'s `Encoder`, which structurally cannot emit `"` (per nota-design.md). The bin entrypoints `spirit-migrate-*.rs` use `encoder.into_string()` and `println!("{}", ...)` — the `{}` is a format placeholder, not a literal quote.
- **No labeled `(key value)` records.** The schemas use positional records and brace-maps for namespaces (`spirit.schema` namespace block is `Name body` pairs inside `{ }`, the correct NOTA form). The `RecordQuery`, `Entry`, `RemovalCandidateCollection`, `ArchiveTarget` shapes are all positional.
- **Single-argument rule honored.** `persona-spirit-daemon.rs` reads `SingleArgument::from_environment()`; the `spirit` / `spirit-next` CLIs are one-line `signal_frame::signal_cli!(...)` macro expansions. No flag parsing (`--`, `clap`, `StructOpt`) anywhere in `persona-spirit/src` or `spirit-next/src`. The `spirit-next` CLI does read `SPIRIT_NEXT_SOCKET` / `SPIRIT_NEXT_TRACE_SOCKET` env vars — these are env-var configuration, not argv flags, and are NOTA-embed-safe; component-triad.md treats env vars as an acceptable config surface, distinct from the forbidden argv-flag soup.

## (4) Manifestation currency — the central drift

The CollectRemovalCandidates arc (1541-1544, 1547) IS manifested on main and IS documented in BOTH `persona-spirit/ARCHITECTURE.md` (lines 51-60) and `signal-persona-spirit/ARCHITECTURE.md` (line 121) plus both INTENT.md files. The schema carries it (`signal-persona-spirit/spirit.schema:14`). This is good continuous-manifestation. But four newer decided intents (1548, 1549, 1550, plus the 1474 ladder and the 1570 default-certainty correction) are NOT reflected, and one of them contradicts the landed shape.

### 4a. Output-target enum drift (Spirit 1548) — DECIDED, landed shape is WRONG

The landed schema (`signal-persona-spirit/spirit.schema:64`) defines:

```nota
ArchiveTarget (Inline (File ArchivePath))
```

Spirit 1548 (Decision High) says the output-target enum variants are **Stdout, Stderr, File(path)** — "Not an error channel — Stderr is one option among normal outputs." The landed `Inline | File` is the older shape from before 1548. `persona-spirit/ARCHITECTURE.md:55-57` documents `ArchiveTarget::Inline` and `ArchiveTarget::File(ArchivePath)` — also stale relative to 1548.

This is the only place where I think the port is NOT a clean field-level decision, and I lean **blocked**. 1548 names three variants but the relationship to the existing `Inline` variant is ambiguous: is `Inline` *renamed* to `Stdout` (CLI prints the archive), is `Inline` *kept* alongside `Stdout`/`Stderr`/`File` (four variants — but 1548 lists exactly three), or does the daemon-written-`Inline`-reply-data semantics map to something 1548 didn't anticipate? The daemon currently distinguishes "inline reply data returned in `RemovalCandidatesCollected`" from "daemon writes a file." A `Stdout` target on a daemon-side operation is semantically odd — the daemon has no stdout the caller sees; the CLI does. So the mapping of 1548's `Stdout`/`Stderr` onto a daemon operation needs a psyche call. **blocked** — see open decision.

### 4b. Small-record type fields (Spirit 1549) — PARTIAL

1549 specifies the small record carries: identifier, topics, kind, description summary, magnitude, **daemon-stamped date and time**. The landed `RecordSummary` (`spirit.schema:67`) is:

```nota
RecordSummary [RecordIdentifier Topics Kind Description Certainty Privacy]
```

It carries identifier/topics/kind/description and TWO magnitudes (certainty + privacy) but NO date/time. The date/time live one layer out in `RecordProvenance [RecordSummary Date Time]` (line 68). So 1549's "small record carrying ... daemon-stamped date and time" is not the landed `RecordSummary`; it is closer to `RecordProvenance`. Whether 1549 wants date/time folded INTO the small record (changing `RecordSummary`) or whether `RecordProvenance` already IS the 1549 small-record is a naming/structure question, not a pure port. Also 1549 says "magnitude" (singular) where the landed shape has two magnitudes (certainty + privacy) — does the small record drop privacy? **blocked** on the field set + which existing type is the 1549 small-record.

### 4c. RecordDefault short-form + variant ladder (Spirit 1550, 1474, 1545) — MISSING

Greps for `RecordDefault`, `ShortForm`, `Today`, `variant-ladder` across all spirit source and schemas return nothing. The schema operation root vector (`spirit.schema:6-15`) has no short-form root. 1550 names the fields RecordDefault takes (topics, kind, description, magnitude) — that part IS field-level decided. But the defaults to inject are now CONTESTED: 1550 says "privacy Zero/open, daemon-stamped date/time" and lists magnitude as a customized field, while the NEWER Spirit 1570 (Clarification High) says **Medium certainty should be the normal default** for routine captures. If RecordDefault omits certainty and injects a default, that default is now Medium (1570), not whatever 1550 implied. And 1550's field list INCLUDES magnitude as customizable, while 1569 (Principle High) says agents should be able to OMIT routine fields "such as default certainty." So the question of which fields RecordDefault takes vs. injects is no longer the clean 1550 list. **blocked** on the final field/default split (see open decisions).

### 4d. Default-certainty correction (Spirit 1570) + privacy-usability (1571) — MISSING from docs

Both INTENT.md files state "certainty is required `Magnitude`" but neither names a DEFAULT, and the recent 1570 ("Medium default") and 1571 ("privacy filtering and default visibility must be clear before private use") are not manifested anywhere in the spirit docs. 1570/1571 are Clarifications that set direction but are not yet field-level (1570 says "unless wording justifies otherwise" — a heuristic the agent applies, not a schema field; 1571 is an aspiration). These are correctly NOT ported as code; they SHOULD land as INTENT.md prose. The INTENT.md prose update for 1570 (recording the Medium default heuristic) is **portable** — it just records decided direction.

### 4e. Source-ahead-of-deploy (Spirit 1568 honesty check)

The live deployed `spirit` binary (`~/.nix-profile/bin/spirit` → home-manager path) does NOT have CollectRemovalCandidates: a live call returns `cannot route command-line request: unknown request head: CollectRemovalCandidates`. The live daemon's `RecordQuery` is also 5-field (no PrivacySelection) — a live `Observe` with the 6-field source schema returns `unknown variant Any for enum ObservationMode`, and the 5-field form succeeds. So CollectRemovalCandidates and privacy filtering are **landed on main** (persona-spirit commit `7233075`, signal-persona-spirit `a69769b`) but **not deployed**. This is correct per 1568 ("landed means on main") — the source-on-main IS landed; the gap is a deploy/cutover step, not a manifestation drift. The next/main/previous side-by-side deploy substrate (persona-spirit INTENT.md §"Deployment") is what cuts a new build over. Flagging for honesty: any report or status that claims removal-candidate collection is "available" must say "landed on main, deployed binary predates it."

### 4f. spirit-next does not yet track the removal-candidate surface

`spirit-next/INTENT.md` line 206 claims spirit-next "tracks production Spirit 0.3 behavior where the schema surface reaches it." But `spirit-next/schema/lib.schema:2` operation root is `[Record Observe Lookup Count Remove LookupStash]` — no CollectRemovalCandidates, no ChangeCertainty, no certainty/time filtering. The pilot's "tracks 0.3" claim is aspirational, not current. Whether spirit-next SHOULD grow CollectRemovalCandidates is a design question (the pilot is meant to prove the schema-derived engine, not feature-match production); the INTENT.md wording overstates currency. A precise edit: soften line 206 to name WHICH 0.3 surface the pilot tracks (multi-topic, privacy, lookup/count) and which it deliberately does not yet (removal-candidate collection, certainty change, recency depth). That edit just records the true state and is **portable**.

## Bad patterns observed

1. **Stale triad-leg name in current ARCHITECTURE/INTENT/skills.** `persona-spirit/ARCHITECTURE.md:16`, `INTENT.md:32,153`, `skills.md:13,21,30,35,124` all name `owner-signal-persona-spirit` as the policy leg. Per AGENTS.md (these per-repo files are the canonical agent-context surface — READ and UPDATE) and Spirit 1567, current guidance should name `meta-signal-persona-spirit`. Fix: rename pass (gap 1) updates these in lockstep with the crate rename.

2. **ARCHITECTURE prose ahead of an undecided field shape.** `persona-spirit/ARCHITECTURE.md:55-57` documents `ArchiveTarget::Inline | File` as settled while Spirit 1548 has redirected the output-target enum to `Stdout | Stderr | File`. The doc is faithful to the LANDED code but stale to the DECISION. This is the correct continuous-manifestation behavior (doc tracks code, not unbuilt decisions) — flagged only so the 1548 reconciliation updates both code and doc together.

## Portability ledger

| Design (intent) | Status in source | Portable? |
|---|---|---|
| Meta-signal rename of policy leg (1567) | not started — zero meta-signal refs, repo still owner-signal | **portable** — target name fully determined; staged as designer feature branch, landed by operator (remote rename + cross-repo retarget) |
| CollectRemovalCandidates operation (1543/1544/1547) | implemented on main (commit 7233075 / a69769b); documented | implemented (port complete) |
| Output-target enum Stdout/Stderr/File (1548) | wrong shape landed (`Inline | File`) | **blocked** — Stdout/Stderr semantics on a daemon-side op + relation to existing Inline need a psyche call |
| Small-record data type fields (1549) | partial — `RecordSummary` exists, no date/time, two magnitudes | **blocked** — field set (date/time fold-in? drop privacy?) + which existing type IS the small record |
| RecordDefault short-form + variant ladder (1550/1474/1545) | missing | **blocked** — final field/default split contested by newer 1569/1570 |
| Medium default certainty (1570) | missing from docs | **portable** as INTENT.md prose (records decided heuristic; not a schema field) |
| Privacy default-visibility clarity (1571) | missing from docs | blocked as code (aspiration, not field-level); portable only as carry-uncertainty INTENT note |
| spirit-next "tracks 0.3" currency claim (line 206) | overstated | **portable** as INTENT.md correction (records true state) |
| Naming discipline (full-word, no-ancestry) | clean across triad source | implemented |
| NOTA discipline (no quotes, positional, single-arg) | clean across triad source | implemented |
| Deploy currency (1568 honesty) | source-ahead-of-deploy: live binary lacks CollectRemovalCandidates + privacy | not a manifestation gap — deploy/cutover step (operator) |
