*Kind: Triage · Topic: schema-stack-substance-triage · Date: 2026-05-24 · Lane: designer*

# 319 / 1 — Schema-stack substance triage (Subagent A)

## §1 Frame

Subagent A slice per the orchestrator frame at
`./0-frame-and-method.md` §2.2. Twelve report entries
(ten files + two directories) carrying schema-stack substance are
triaged against the **current target direction** (frame §6):
short header (spirit 388), sema short header (390), NOTA schema
language (391), schema component as triad (397-400), MVP even-byte
scope (392). Per §3 of the frame, every DROP cites the permanent
home where the substance now lives; every KEEP names a
substance-rationale or design-rationale-guard reason.

The big-picture finding is that the **canonical version-handover
spec layer has migrated cleanly** — version-projection ARCH owns
the trait + types, signal-upgrade ARCH owns the merged contract,
upgrade ARCH owns the daemon scaffold — but the **macro
convergence + per-component-namespace + recursive Help + pre-typed
envelope + recursive schema language** layer is still in active
design state, with most substance still load-bearing in its
report homes and ready for second-designer's forward `/319` to
absorb.

## §2 Triage decision table

The compact result; per-row rationale follows in §3.

| # | Path | Substance status | Action | Target home (if MIGRATE) | Rationale guard? | Reason |
|---|---|---|---|---|---|---|
| 1 | `263-schema-specification-language-design.md` | IN-FLIGHT | KEEP | n/a (carries forward as rationale into `/319`) | YES | Enumerates Cap'n-Proto-vs-this competing design + worked example; foundation for spirit 391 NOTA schema language; new direction reshapes but does not delete |
| 2 | `279-nota-schema-language-and-version-hash.md` | IN-FLIGHT | KEEP | n/a (carries forward as rationale into `/319`) | YES | Enumerates per-component-vs-per-record-vs-workspace-root hash granularity alternatives; content-addressable schema hash mechanism feeds spirit 391 + schema component |
| 3 | `285-versionprojection-trait-and-handover-protocol-specification.md` | LANDED | KEEP (STATUS-BANNER candidate) | substance in `version-projection/ARCHITECTURE.md` + `signal-upgrade/ARCHITECTURE.md` | YES | Enumerates four crate-placement alternatives (signal-sema vs sema-engine vs signal-core vs new crate) chosen on rationale; canonical specification protected by /315 §1 marker; substance landed in ARCH but the alternatives matter |
| 4 | `287-version-handover-component-explained.md` | LANDED | KEEP (STATUS-BANNER candidate) | substance in `version-projection/ARCHITECTURE.md` + `signal-upgrade/ARCHITECTURE.md` (handover sequence diagram, three-socket layout) | NO | Pure pedagogy/explainer — six-pieces overview, sequence diagram, phase walkthrough — protected by /315 §1; one-stop reference for future agents who need the architecture without reading three reports |
| 5 | `305-nota-user-guide-and-codec-architecture/` (directory, 4 files) | LANDED | DROP | substance in `nota/README.md` (user-facing syntax) + `nota-codec/README.md:1-96` + `nota-codec/ARCHITECTURE.md` + `skills/nota-design.md` + `skills/nota-schema-docs.md` | NO | Three-file user guide + codec architecture; nota-codec README + ARCH carry the codec split; nota/README.md carries the syntax; skills carry the discipline; report fully absorbed |
| 6 | `305-v2-design-64bit-signal-per-component-namespacing.md` | LANDED | KEEP (STATUS-BANNER candidate) | substance in `signal-frame/ARCHITECTURE.md:289-298` (referenced by name at line 297) | NO | The per-component namespacing correction landed in signal-frame ARCH §5.2; ARCH explicitly references this report by path — keep until ARCH absorbs the full reasoning and the report-reference can drop |
| 7 | `307-design-golden-ratio-namespace-split.md` | IN-FLIGHT | KEEP | n/a (ready for absorption; bead `primary-v5n2` ready per operator/169) | YES | Enumerates four cutoff alternatives (100/156 vs 98/158 vs 64/192 vs 96/160) with rationale; signal-frame ARCH:299-311 sketches the split but explicitly defers detail "once that design completes"; macro-impl bead `primary-v5n2` consumes this when landing |
| 8 | `308-design-pretyped-envelope-and-tap-anywhere.md` | IN-FLIGHT | KEEP | n/a (ready for absorption; bead `primary-2cjv` ready per operator/169) | YES | Enumerates three envelope-shape alternatives (Option A/B/C, recommends C); `ExchangeFrame::body` currently single-field (`signal-frame/src/frame.rs:53-55`), `micro: u64` NOT yet in code; bead is operator-ready, design carries forward |
| 9 | `312-design-recursive-help-on-every-enum.md` | IN-FLIGHT | KEEP | n/a (ready for absorption; bead `primary-ezqx` slot per `/317-4 §2.1` includes Help slots) | NO | Recursive-Help shape differs from skill `component-triad.md:377-399` (which still describes the flat `/298` `(Help Main)` + `(Help (Verb …))` form); the recursive design is not yet in any ARCH or skill — load-bearing for the macro convergence epic |
| 10 | `315-design-sema-upgrade-and-handover-current-state.md` | LANDED | KEEP (STATUS-BANNER candidate) | superseded for daemon shape by `/318` (per /318 §6 see-also); substance partly in version-projection/signal-upgrade ARCH; partly in /317 audit; /315 itself carries the protection-banner for /285 + /287 | NO | The Persona-absorbs-vs-separate-daemon decision (§2.1) is superseded by spirit 369 (Decision Maximum) — upgrade triad exists; the protection-banner role for /285 + /287 still loads weight; carries forward briefly |
| 11 | `317-sema-upgrade-and-macro-convergence-audit/` (directory, 5 files) | IN-FLIGHT | KEEP | n/a (active design for `primary-ezqx` epic per operator/169) | NO | Last-24-hours design; the 11-slot consolidated macro convergence picture (`/317-4 §2`) is the active operator target; second-designer's `/319` is downstream consumer; not yet absorbed into signal-frame ARCH |
| 12 | `318-upgrade-merger-and-persona-prefix-rename/` (directory, 5 files) | IN-FLIGHT | KEEP | n/a (active execution per operator/169; Wave-4 partially landed) | NO | Last-24-hours design; Wave-1 + Wave-4 partially landed (U2/U3/U4/U5/U6 closed; R10 + R11 + R12 + U7 + Persona meta still open); design carries the rename inventory + dependency graph + 4-crate structural design that operators consume |

## §3 Per-row rationale

### §3.1 Row 1 — `/263` schema specification language

**Status:** IN-FLIGHT. The schema-language design feeds spirit
record 391 (NOTA schema language) — one of the four targets
called out in frame §6 — and through it feeds spirit records
397-400 (schema component).

**Action:** KEEP with design-rationale guard.

**Substance verification:**

- The report explicitly enumerates the Cap'n-Proto-vs-this-language
  comparison (`/263:89-122`) — multiple alternatives evaluated.
- The three-layer separation (`/263:36-52`) is design rationale
  for why the schema-layout layer exists at all.
- The schema-change classification (zero-cost / append-only /
  structural) at `/263:218-282` is the vocabulary the diff
  classifier emits — load-bearing for the schema component's
  upgrade-planning leg.
- The worked example (spirit master vs deployed at `/263:284-410`)
  is concrete-test-case substance, not duplicated anywhere.

**Why KEEP not MIGRATE:** Spirit 391 + 397-400 reshape the schema
language target around a schema-component daemon that exposes
macros to signal-side + sema-side. The current `/263` shape (NOTA
top-level declarations + Blake3 content address + diff classifier
emit) is the foundation second-designer's `/319` rewrites. Until
the schema component itself has a target ARCH, this is the
canonical NOTA-schema-language reference.

**Why design-rationale guard fires:** explicit Cap'n-Proto vs
this-language comparison; multiple syntax alternatives sketched
across §"Sketch of the syntax". Per `skills/context-maintenance.md`
§3a, reports enumerating competing design alternatives are
load-bearing as rationale even after the chosen design migrates.

### §3.2 Row 2 — `/279` NOTA schema language + version hash

**Status:** IN-FLIGHT. Spirit 391's NOTA schema language target +
spirit 398's "schemas stored in efficient binary form" both build
on this report's content-addressable mechanism.

**Action:** KEEP with design-rationale guard.

**Substance verification:**

- Five questions answered (`/279:1-11`) — the grammar, canonical
  encoding under Blake3, what the hash binds to (per-component vs
  per-record vs workspace-root), storage shape, dispatch protocol.
- Per-component-vs-per-record-vs-workspace-root granularity
  trade-off at `/279:204-247` — enumerates three alternatives,
  picks per-component.
- The Leaf/Branch/Newtype/Channel split at `/279:36-101` is the
  vocabulary the schema-component's library face will expose.
- Schema header table shape (`/279:264-292`) + sema-upgrade
  dispatch protocol (`/279:294-319` plus continuation) carry
  storage + runtime mechanisms still load-bearing.

**Why KEEP not MIGRATE:** No permanent home yet for the
schema-language design. `nota-codec/ARCHITECTURE.md` carries the
codec (Token / Decoder / Encoder) not the schema language.
`signal-frame/ARCHITECTURE.md` carries the wire kernel, not the
schema language. The schema component (spirit 397-400) is the
prospective permanent home — `/319` second-designer's forward
design synthesises this.

**Why design-rationale guard fires:** §"4 What the hash binds to"
(`/279:204-247`) explicitly enumerates Merkle-leaf alternatives.
§"5 Storage shape" weighs header-table vs per-record-prefix.

### §3.3 Row 3 — `/285` VersionProjection trait + handover protocol spec

**Status:** LANDED. Implementation landed per operator/158
(`/285:46-58` confirms commits 69bd2dd0 + f2dfe3b4 + e0a7153c +
060982d0 + 677206d5), and the merger landed per /318 Wave-4
(operator/169 confirms `primary-l3h5.2` through `.6` closed).

**Action:** KEEP with STATUS-BANNER candidate.

**Substance verification:**

- The `VersionProjection<Source, Target>` trait is in
  `version-projection/src/projection.rs` per
  `version-projection/ARCHITECTURE.md:22` (cited).
- `ContractVersion([u8; 32])` Blake3 schema hash is in
  `version-projection/ARCHITECTURE.md:32` (cited).
- The handover-protocol records (`HandoverMarker`,
  `MirrorPayload`, `DivergencePayload`, `RecoveryRequest`) now
  live in `signal-upgrade/src/lib.rs:202-256` and the
  `signal-upgrade` channel macro at `:312-316` carries the
  operations.
- Per-operation policy (`WritePolicy` / `ReadPolicy` /
  `SubscribePolicy` / `PerOperationPolicy`) is in
  `version-projection/ARCHITECTURE.md:27-30` (cited).

**Why KEEP not DROP:** Per `/315 §1`, /285 carries a protection
status as "the canonical spec." Per the design-rationale guard
(`skills/context-maintenance.md` §3a), §1.1 of /285 explicitly
enumerates four crate-placement alternatives
(signal-sema / sema-engine / signal-core / new
`version-projection`), chose the new crate, and documents why
the rejected alternatives lose. Rejected-alternative reasoning is
not in ARCH and would not be — that is what makes the report
load-bearing as rationale.

**Why STATUS-BANNER candidate:** The substance landed cleanly;
future agents reading /285 should see a banner naming
`version-projection/ARCHITECTURE.md` + `signal-upgrade/ARCHITECTURE.md`
as the live homes. The orchestrator synthesis (`/319/4`) can
decide whether to land the banner this commit or defer.

### §3.4 Row 4 — `/287` Version handover component explained

**Status:** LANDED. The handover protocol it explains is
implemented + merged into the upgrade triad per /318 Wave-4.

**Action:** KEEP with STATUS-BANNER candidate (no rationale guard
needed).

**Substance verification:**

- The six-pieces big picture (`/287:24-48`) is documented across
  `version-projection/ARCHITECTURE.md:101-113` (boundary diagram)
  and the merged `signal-upgrade/ARCHITECTURE.md:18-32` (working
  shape).
- The three-socket layout (`/287:50-67`) is captured in
  `signal-version-handover/ARCHITECTURE.md` (still present, even
  though the merger means new code uses signal-upgrade) and
  documented per spirit 369.
- The handover sequence (`/287:70-106`) is preserved by the
  protocol records in `signal-upgrade/src/lib.rs:202-316`.

**Why KEEP not DROP:** Per `/315 §1` and the rationale stated in
/287's own first paragraph, this report is **the canonical visual
reference** for the version-handover stack — six-piece diagram +
sequence diagram + phase walkthrough. ARCH files carry per-repo
substance; no single ARCH file carries a six-component overview.
The frame's intent is "second-designer's forward design absorbs";
until that absorption surfaces an overview-and-explainer ARCH
file, /287 holds load-bearing pedagogical weight. Note: /287 is
NOT design-rationale-guard territory — it does not enumerate
competing alternatives; it explains the chosen design. The KEEP
is pedagogical, not rationale.

**Why STATUS-BANNER candidate:** When the upgrade-triad ARCH is
fleshed out beyond the U1-scaffold-only state
(`upgrade/ARCHITECTURE.md:22-39`), the six-piece picture lands
there and /287 retires. Today it is still load-bearing.

### §3.5 Row 5 — `/305-nota-user-guide-and-codec-architecture/` (directory)

**Status:** LANDED. All four files' substance is in permanent
homes.

**Action:** DROP.

**Substance verification per file:**

- `0-presentation.md` (NOTA user guide overview). User model
  (records / enums / options / completeness / containers / maps)
  is in `nota/README.md` per the spec-only-syntax-repo design;
  the system-map at `/305/0:19-41` reflects the deployed split.
- `1-user-notation-model.md` (NOTA text model). Three structural
  delimiters + value-position discipline at `/305/1` are captured
  in `nota/README.md` (the spec-only-syntax repo) and in
  `skills/nota-design.md` (workspace NOTA discipline).
- `2-rust-codec-and-derive-architecture.md` (codec + derive
  architecture). The split (nota-codec public crate + nota-derive
  proc-macro impl crate) is in `nota-codec/README.md:1-96` and
  `nota-codec/ARCHITECTURE.md`. The trait list + Encoder/Decoder
  shape is in `nota-codec/README.md:30-50`.
- `3-component-usage-and-tests.md` (component-side usage). The
  single-NOTA-argument rule + nota-config startup helper is
  workspace-wide policy captured in `skills/component-triad.md`
  §"The single argument rule" and `AGENTS.md` hard-overrides.

**Why DROP without rationale guard:** No design-alternative
enumeration; pure user-guide + codec-architecture explainer.
Permanent homes exist for every substance unit (nota repo
README + nota-codec README + nota-codec ARCH + skills/nota-*).
Per `skills/context-maintenance.md` §2 "Drop", substance is "stale
or already captured elsewhere"; here it's the latter.

### §3.6 Row 6 — `/305-v2` per-component namespacing

**Status:** LANDED. The per-component namespacing correction
landed in signal-frame ARCH §5.2.

**Action:** KEEP with STATUS-BANNER candidate.

**Substance verification:**

- The correction itself (spirit record 326, per-component not
  workspace-wide) is in `signal-frame/ARCHITECTURE.md:289-298`,
  which explicitly cites this report by path at `:297`.
- Universal data variants (U8 / U16) at slot level are in
  `signal-frame/ARCHITECTURE.md:329-345` (§5.3 Universal data
  variants).
- The four-channel example diagram + provenance discussion at
  `/305-v2:30-100` are illustrative substance not duplicated in
  ARCH.

**Why KEEP not DROP:** The ARCH text at signal-frame:289-298 is
compact ("namespace is per-component, not workspace-wide; same
byte value on different channels means different verbs"); the
full reasoning (why provenance solves it, what the four-channel
illustration shows, the contrast with the wrong workspace-wide
framing) lives only in this report. The ARCH cites this report
by path — that citation should not break.

**Why STATUS-BANNER candidate:** Add a banner naming
`signal-frame/ARCHITECTURE.md:289-345` as the canonical landed
home; readers see the supersession-by-absorption and find the
chosen shape in ARCH while keeping the original rationale here.
ARCH-side: the citation at signal-frame:297 can drop once the
ARCH-only narrative is judged complete; until then /305-v2 holds
the rationale weight.

### §3.7 Row 7 — `/307` Golden-ratio namespace split

**Status:** IN-FLIGHT. The macro implementation is bead
`primary-v5n2` (ready per operator/169 ready list + `/317-4 §2.1`).

**Action:** KEEP with design-rationale guard.

**Substance verification:**

- Four cutoff alternatives evaluated at `/307:46-50` — 100/156 vs
  98/158 vs 64/192 vs 96/160 — three rationales for picking
  100/156 at `/307:54-80`.
- The macro mechanism sketch (compile-time
  `assert_triad_sections!` enforcement, section pre-allocation,
  golden-ratio constants) carries forward to bead
  `primary-v5n2` per `/317-4 §2.1`.
- The single-socket-per-component analysis (golden-ratio split
  enables one-socket dispatch) is exploration substance not
  duplicated anywhere.
- `signal-frame/ARCHITECTURE.md:299-311` carries a 13-line summary
  of the split + explicit deferral to this report
  ("Detailed mechanism lands in `reports/designer/307-…` once
  that design completes").

**Why KEEP not MIGRATE:** ARCH explicitly defers detail to this
report; the macro PR that absorbs the substance has not yet
landed (`primary-v5n2` open). When the macro PR ships and the
ARCH section grows to absorb the four-cutoff rationale, the
report retires.

**Why design-rationale guard fires:** explicit enumeration of
four cutoff alternatives; the rejected alternatives are
load-bearing as rationale (especially the power-of-2 temptation
at `/307:75-80` — future agents will ask "why isn't this
64/192?").

### §3.8 Row 8 — `/308` Pre-typed envelope + tap-anywhere

**Status:** IN-FLIGHT. `ExchangeFrame::body` is still a
single-field struct in code (`signal-frame/src/frame.rs:53-55`,
no `micro: u64` field); bead `primary-2cjv` is ready per
operator/169.

**Action:** KEEP with design-rationale guard.

**Substance verification:**

- Three envelope-shape alternatives at `/308:43-91` — Option A
  (per-variant prefix) vs Option B (header above body) vs
  Option C (top-level struct field) — recommends C with reasoning.
- The chosen `Frame { micro: u64, body: FrameBody }` shape at
  `/308:92-100` is the operator-side target for `primary-2cjv`.
- The tap-anywhere observability section (`/308:1-40` plus
  continuation) lays out tap points operator will wire as
  `primary-bann` (per `/317-4 §7` "Tap-anywhere observability
  beyond what `primary-3cl1` lands").

**Why KEEP not MIGRATE:** The substance has not landed in code
(verified at signal-frame/src/frame.rs:53-55); the report is
itself the design substrate the operator implementation reads.
Per `/317-4 §2.1`, bead `primary-3cl1` + `primary-2cjv`
implement Frame reshape — until the implementation lands and
signal-frame ARCH absorbs the chosen shape, this report carries
load-bearing design weight.

**Why design-rationale guard fires:** Three envelope-shape
alternatives explicitly enumerated with per-option rationale;
the rejected options (per-variant prefix, header-above-body)
matter for future readers asking "why not Option B?".

### §3.9 Row 9 — `/312` Recursive Help on every enum

**Status:** IN-FLIGHT. The recursive-Help design is not yet
absorbed anywhere; the older flat-Help-at-contract-level form
from `/298` is what `skills/component-triad.md:377-399` still
documents.

**Action:** KEEP.

**Substance verification:**

- `/312:14-25` explicitly contrasts the new recursive form with
  the older flat form from `/298`; the older form is what the
  skill currently teaches at `component-triad.md:381-389`.
- The recursive Help-walks-the-enum-tree mechanism (`/312:48-80`)
  with `Help` at the END of the path (a noun, not a verb) is
  the substance bead `primary-8r1j` will implement per
  `/317-4 §2.1`.
- The `signal_channel!` auto-injection pattern (Help variant
  added to every emitted enum, doc-comment-driven HelpReply) is
  what makes the recursive form macro-implementable — load-bearing
  for the macro convergence epic.

**Why KEEP not MIGRATE:** Two reasons. First, the recursive form
is not yet in any ARCH or skill file — `skills/component-triad.md`
still describes the older two-operation flat form. Migrating
without first reconciling the older form would land
contradictory rules. Second, the macro implementation
(`primary-ezqx` epic, Help slots per `/317-4 §2.1`) has not
landed; the report is the operator-side substrate.

**Why no design-rationale guard:** `/312` proposes the recursive
form as the right shape; it does not enumerate competing
alternatives with side-by-side weighing. It is a single-direction
design report; KEEP because the substance is unmigrated, not
because rejected-alternatives load weight.

### §3.10 Row 10 — `/315` Sema-upgrade and handover current state

**Status:** LANDED partly; SUPERSEDED partly.

**Action:** KEEP (briefly, then retire when /318 absorption
completes).

**Substance verification:**

- §1 protection banner for /285 + /287: still load-bearing —
  this is the marker that keeps /285 + /287 from being
  garbage-collected naively.
- §2.1 Persona-absorbs-vs-separate-daemon decision: SUPERSEDED
  by spirit 369 (Decision Maximum) per /318 frame §1. The upgrade
  triad exists; the Persona-absorbs lean was the right interim
  call but the long-term shape is separate daemon (the merged
  `upgrade` triad).
- §2.2 owner-signal-version-handover entry: SUPERSEDED — the
  contract now exists on disk (`/317-1 §2.3` confirms 228 lines +
  248 test lines). The /318 §3.3 cleanup bead C3 explicitly
  targets this update.
- §2.3 Mirror payload typed shape: SUPERSEDED — spirit 274
  (Maximum) settled the question (raw bytes); the /318 §3.3
  cleanup bead C3 retires the Possible-features entries.
- §2.4 Recursive bootstrap: still open; not yet absorbed.
- §3-§4 type-family split + commit-sequence: already absorbed
  per /315's own §3-§4 (cited landing commits).

**Why KEEP not DROP:** §1's protection-banner role for /285 +
/287 is load-bearing — without /315, the garbage-collection
case for /285 + /287 strengthens spuriously. §2.4 (recursive
bootstrap) is the only remaining open question not absorbed
elsewhere.

**Why retire (eventually):** After /318 Wave-4 completes
(operator/169 confirms most of it has landed) AND C3 cleanups
ship (Mirror Possible-features retire from 3 ARCH files;
owner-handover docs update), /315's load-bearing role narrows
to §2.4 recursive bootstrap. That one open question can migrate
into the upgrade triad's ARCH Possible-features. Then /315
retires entirely.

**Why no design-rationale guard:** /315 is consolidation + state
report, not a multi-alternative design. The KEEP is for the
protection-banner role + the §2.4 unresolved question.

### §3.11 Row 11 — `/317` Sema-upgrade + macro convergence audit (directory)

**Status:** IN-FLIGHT (last 24 hours).

**Action:** KEEP — directory unit.

**Substance verification:** All five files are recent and active.

- `0-frame-and-method.md` (11,246 bytes) — meta-report frame;
  retires with the directory.
- `1-sema-upgrade-path-audit.md` (48,402 bytes) — concrete gap
  analysis ("designed-vs-in-code per concern" matrix) feeding
  operator beads `primary-wdl6` (v0.1.0 retrofit) and the new
  pre-migration-step bead per `/317-1 §4`.
- `2-macro-current-state-audit.md` (38,911 bytes) — per-bead
  status for all 8 macro beads + the 5-slot convergence map;
  this IS the source operator/169's ready list consumes.
- `3-next-as-dependency-design.md` (42,007 bytes) — fresh design
  for spirit 366's next-as-dep upgrade path; carries Cargo
  rename rule + grammar + per-payload walker + reverse direction
  + first frozen v0.1.0 crate beads.
- `4-overview.md` (19,996 bytes) — synthesis + 11-slot
  consolidated picture + landing-order Gantt.

**Why KEEP not MIGRATE:** The substance is the active execution
plan for `primary-ezqx` (macro convergence epic, ready per
operator/169) and feeds the Spirit pilot blockers. Nothing in
ARCH absorbs the 11-slot picture; until the macro PR lands and
signal-frame ARCH absorbs the LogVariant + HelpReply types +
section-allocation rules, this directory is the canonical
substrate. Second-designer's `/319` is downstream consumer (per
the frame's non-overlap note).

**Why KEEP per-unit (not per-file):** the 5-file directory is one
meta-report per `skills/reporting.md` §"Meta-report directories"
— the directory IS the report; it garbage-collects as one unit.
Per the slice contract option ("triage as a unit OR per-file if
substance differs"), the five files share one substance arc
(audit-design-synthesis); per-file split would over-formalize.

**Why no design-rationale guard:** the audit + design pair is
forward-looking, not alternative-enumerating. The KEEP is
substance-not-yet-migrated.

### §3.12 Row 12 — `/318` Upgrade merger + persona-prefix rename (directory)

**Status:** IN-FLIGHT (last 24 hours; partial landing in code per
operator/169).

**Action:** KEEP — directory unit.

**Substance verification:** All five files are recent and the
rename + merger is partially executed.

- `0-frame-and-method.md` (13,447 bytes) — orchestrator frame;
  retires with directory.
- `1-rename-inventory-and-dependency-graph.md` (54,928 bytes) —
  29 affected repos + dependency graph + topological order.
  Operator reads this per-bead while landing R1-R12.
- `2-rename-tooling-and-mechanics.md` (27,835 bytes) — Cargo +
  Nix + ghq + jj mechanics; the worked example operators use as
  reference.
- `3-upgrade-triad-structural-design.md` (62,938 bytes) — the
  4-crate structure + 9-operation merged contract; landed
  partly (`signal-upgrade`, `owner-signal-upgrade`, `upgrade`
  scaffolds exist per ARCH files I verified).
- `4-overview-and-bead-list.md` (18,777 bytes) — operator-bead
  list (R1-R12, U1-U7, C1-C3) + recommended landing order.

**Why KEEP not MIGRATE:** Per operator/169, R10 (agent triad
rename, psyche-confirm pending), R11 (spirit triad rename,
gated on Spirit cutover), R12 (Persona meta catch-up + CriomOS
repin), U7 (CriomOS deploy), and C3 cleanups are all still open.
The bead list + dependency graph are the active execution
substrate. The structural design (file 3) carries enough
substance that the upgrade triad's ARCH files (`upgrade/ARCH`,
`signal-upgrade/ARCH`, `owner-signal-upgrade/ARCH`) defer to it
implicitly — those ARCH files are scaffold-only today
(`upgrade/ARCHITECTURE.md:51-53` says "Scaffold only").

**Why KEEP per-unit:** Same reasoning as /317 — meta-report
directory, one substance arc, garbage-collects as one unit.

**Why no design-rationale guard:** /318/3 is a forward design
that picks one shape (4-crate merger) without sketching multiple
alternative crate-decompositions. The KEEP is substance-not-yet-
migrated.

## §4 Cross-cutting observations

### §4.1 Where the schema-stack substance currently lives

The current target direction (frame §6) maps to permanent homes
as follows. For each spirit record, the table notes whether the
substance has landed in a permanent home or is still in a report.

| Spirit | Concern | Substance home today | Status |
|---|---|---|---|
| 388 | short header (64-bit, 8 enums) | nowhere in ARCH/skill yet; sketched in `signal-frame/ARCHITECTURE.md:258-300` as the verb-namespace structure | NOT-YET-ABSORBED |
| 390 | sema short header | nowhere yet | NOT-YET-ABSORBED |
| 391 | NOTA schema language | `/263` + `/279` (reports only) | NOT-YET-ABSORBED |
| 392 | MVP even-byte 7-sub-enum scope | nowhere yet | NOT-YET-ABSORBED |
| 397 | schema component as triad | nowhere yet | NOT-YET-ABSORBED |
| 398 | schemas stored binary not NOTA text | nowhere yet | NOT-YET-ABSORBED |
| 399 | schema type library + macros (signal + sema faces) | nowhere yet | NOT-YET-ABSORBED |
| 400 | macro library may be separate repo | nowhere yet | NOT-YET-ABSORBED |

The clean read: the **forward direction is entirely
unabsorbed** today. Second-designer's `/319` forward design IS
the absorption work. This triage's KEEP recommendations preserve
the rationale + substance that `/319` will rest on.

### §4.2 Migration risk — what would break if /285 or /287 were dropped

Per `/315 §1`, /285 and /287 are protected as the canonical spec
+ canonical visual reference. If either dropped without first
landing equivalent substance in the upgrade-triad ARCH:

- Future agents reading `version-projection/ARCHITECTURE.md`
  would not find the four-crate-placement rationale (why a NEW
  crate, not signal-sema / sema-engine / signal-core).
- Future agents reading `signal-upgrade/ARCHITECTURE.md` would
  not find the six-piece system map. ARCH files carry per-repo
  substance; no single ARCH carries the cross-repo overview.

The orchestrator synthesis (`/319/4`) should either:

(a) leave both reports KEEP-with-STATUS-BANNER (lowest risk;
substance preserved + supersession marked), OR

(b) defer the question to when the upgrade-triad ARCH is fleshed
out beyond U1 scaffold-only state — the scaffold itself
(`upgrade/ARCHITECTURE.md:23-29`) explicitly says "U4 consumes
this crate after U2 and U3 have populated the working and owner
contracts" — so the daemon's full ARCH lands after operator
work that has not yet shipped.

**Recommended path:** option (a). Banner naming the live ARCH
homes + KEEP. Both reports retire naturally when the upgrade
triad's daemon ARCH absorbs the overview substance.

### §4.3 Migration opportunity — /305 directory drops cleanly

Of the 12 inventory rows, the cleanest DROP candidate is row 5
(`/305-nota-user-guide-and-codec-architecture/` directory). All
four files' substance is in permanent homes; no design-alternative
enumeration; no protection-banner role; no unresolved questions.

The orchestrator synthesis can land this DROP in the same commit
as the per-row STATUS-BANNER additions without risk to other
substance.

### §4.4 What carries forward to second-designer's `/319`

The substance second-designer's forward `/319` needs to consume
is concentrated in:

- `/263` + `/279` — schema-language design (the foundation
  spirit 391 reshapes).
- `/317-4 §2` — 11-slot consolidated macro convergence picture
  (the macro layer the schema component's library face will
  invoke).
- `/318/3` — 4-crate upgrade structure (the precedent for what
  a "schema component triad" looks like in this workspace).
- `/305-v2` + `/307` + `/308` + `/312` — per-component
  namespacing + golden-ratio split + pre-typed envelope +
  recursive Help (the macro mechanisms the schema component's
  macro face will use).

The triage preserves every report carrying second-designer's
upstream substance. Nothing required for `/319` retires this
sweep.

## §5 Hard-constraint compliance

- READ-ONLY on code + ARCH (HARD): no edits made to any file
  except this triage report.
- Every DROP cites permanent home (HARD): row 5 cites
  `nota/README.md` + `nota-codec/README.md:1-96` +
  `nota-codec/ARCHITECTURE.md` + `skills/nota-design.md` +
  `skills/nota-schema-docs.md`.
- Design-rationale guard applied (HARD): rows 1, 2, 3, 7, 8
  flagged YES on guard; per `skills/context-maintenance.md` §3a,
  these get STATUS-BANNER not DELETE.
- /285 + /287 + /317 + /318 special-handling per slice contract
  (HARD): /285 + /287 verified canonical homes in
  `version-projection/ARCHITECTURE.md` + `signal-upgrade/ARCHITECTURE.md`;
  /317 + /318 KEEP because last-24-hours and substance still in
  active state.
- File:line citations on every substance-migration claim (HARD):
  applied (signal-frame/src/frame.rs:53-55,
  version-projection/ARCHITECTURE.md:22 + :27-30 + :32 + :101-113,
  signal-upgrade/src/lib.rs:202-256 + :312-316,
  signal-frame/ARCHITECTURE.md:289-345 + :299-311,
  component-triad.md:377-399, etc.).
- No emojis; no `---` horizontal-rule lines (HARD): complied.
- jj headless rule (HARD): not invoked; this slice is read-only.
- Mermaid label discipline (HARD): no mermaid diagrams in this
  report (the inventory shape is tabular, not visual).
- No `/nix/store` filesystem search (HARD): not needed for this
  triage.

## §6 See also

- `./0-frame-and-method.md` — orchestrator frame carrying intent
  context (spirit 388-400), slice contract (§2.2), and method
  per `skills/context-maintenance.md`.
- `./2-working-artifacts-triage.md` (Subagent B, pending) —
  sweeps + handovers + audit working-artifact triage.
- `./3-separate-concerns-triage.md` (Subagent C, pending) —
  non-schema-stack concerns triage.
- `./4-overview-and-retirement-list.md` (orchestrator synthesis,
  pending) — consolidated triage + migrations + retirements.
- `skills/context-maintenance.md` §2 (drop/forward/migrate/keep
  table) + §3a (design-rationale guard) + §"Anti-patterns" —
  the discipline this triage operationalizes.
- `skills/reporting.md` §"Meta-report directories" — the unit-
  triage discipline /305-NOTA-user-guide-directory, /317, /318
  follow.
- `reports/operator/169-post-318-refresh-and-next-work-2026-05-24.md`
  — operator's confirmation of /318 Wave-4 partial landing +
  current ready-list (`primary-2cjv`, `primary-ezqx`, agent
  track) the triage cross-references.
- `reports/operator/158-version-handover-foundation-implementation-2026-05-22.md`
  — operator's confirmation of /285 implementation landing
  (commits cited inline at /285:46-58).
- Canonical homes consulted:
  - `signal-frame/ARCHITECTURE.md:258-345` — three-tier sizing +
    verb-namespace structure + Tier 2/Tier 3 + observability tiers.
  - `version-projection/ARCHITECTURE.md` — projection trait +
    policy + index + ContractVersion.
  - `signal-upgrade/ARCHITECTURE.md` — merged working contract
    (catalogue verbs + handover-protocol verbs).
  - `owner-signal-upgrade/ARCHITECTURE.md` — merged owner
    contract.
  - `upgrade/ARCHITECTURE.md` — U1 daemon scaffold.
  - `nota-codec/README.md` + `nota-codec/ARCHITECTURE.md` —
    Rust codec implementation home.
  - `nota/README.md` — NOTA syntax spec.
  - `skills/component-triad.md` §"Help operations" + §"Triad
    shape" — current skill text reflecting the older /298 flat
    Help form (the contrast that makes /312 still load-bearing).
  - `skills/context-maintenance.md` — discipline this triage
    operationalizes.
- Spirit records cited:
  - 326-327 (per-component byte-0 namespace + golden-ratio split
    direction) — /305-v2 + /307 substance.
  - 274 (Mirror payload raw bytes Maximum) — /315 §2.3 + /317
    cleanup target.
  - 359/363/364/365 (Help noun at end of path + CLI single-NOTA-
    argument) — /312 substance.
  - 366 (next-as-dep upgrade path Maximum) — /317 next-as-dep
    design substance.
  - 367 (macro convergence bundle Maximum) — /317 frame
    substance.
  - 369-371 (upgrade triad merger + reporting commit-tree rule +
    component-naming Decision Maximum) — /318 substance.
  - 388-392 (short header + sema short header + NOTA schema
    language + MVP even-byte scope) + 397-400 (schema component
    triad) — second-designer's `/319` forward target.
