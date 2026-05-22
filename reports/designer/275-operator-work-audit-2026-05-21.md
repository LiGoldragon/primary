# 275 - Operator work audit 2026-05-21

*Designer audit. Three commits landed today responsive to /252 and
/269: persona engine-manager `4e928892` on main; signal-persona-spirit
`d7b22bfb` and persona-spirit `d1c76108`, both on
`operator/spirit-response-protocol` only — not on main, not in the
deployed user-profile binary. Headline finding: the Magnitude
migration matches /269 exactly (Certainty deleted outright, High
witness proves the widened vocabulary works), but the binary at
`/home/li/.nix-profile/bin/spirit` still rejects `High` because it
was built from `694452a` pre-migration — the new contract has not
been merged or deployed. The persona engine-manager contract-consumer
slice landed cleanly; the /252 internal rename (file/struct/socket
names from `supervisor*` to `engine_manager*` / `engine_management*`)
is half done — wire-vocabulary in signal-persona is current, but
persona-daemon itself still ships `src/supervisor.rs`,
`src/supervision_readiness.rs`, and seventeen
`*_supervision_socket_*` identifiers. Record 70 in the spirit sema
database authorises the ItemPriority collapse explicitly; no further
psyche decision needed for that. Sema-upgrade's three open questions
(authority, self-upgrade, open placement) reduce to one psyche
decision (open placement) — the others have answer signal already in
intent records 38 / 70 / 72.*

## 1. Audit summary

Three commits landed today against open designer reports.

**Persona engine-manager** at `/git/github.com/LiGoldragon/persona`
commit `4e928892` (titled "persona: migrate engine manager to current
signal contracts") on **main**. Diff: 21 files, +662 / -417. The
slice migrates the daemon's consumer code (manager.rs, request.rs,
schema.rs, transport.rs, supervision_readiness.rs and fixture/test
files) onto the new contract surface in signal-persona — specifically
the `engine::Operation`/`engine::Reply` types and the renamed
`Launch`/`Retirement`/`Action` records.

**Spirit Magnitude migration** at
`/git/github.com/LiGoldragon/signal-persona-spirit` commit `d7b22bfb`
and `/git/github.com/LiGoldragon/persona-spirit` commit `d1c76108`.
**Both commits are on branch `operator/spirit-response-protocol`,
not on main.** signal-persona-spirit's `main` is at `cda5469` and
persona-spirit's `main` is at `5f83a1d`. The migration has not been
merged. The deployed `spirit` binary (built from CriomOS-home from
`persona-spirit@694452a` per bead `primary-ojxq`) still rejects
`High`: `spirit '(Record (test Decision "test" "test" High "test"))'`
returns `Error: InvalidSpiritRequest { reason: "unknown variant
'High' for enum 'Certainty'" }`. The migration is implemented
correctly; the deployment hasn't picked it up.

**ItemPriority resolution.** The operator deferred this question to
psyche citing /269's framing as a "psyche decision". Intent record
70 in spirit's sema database explicitly authorises the collapse;
the parenthetical "(and any other small-vocabulary ordinal enum
reaching for the same concept)" covers ItemPriority directly. No
further psyche decision is needed on whether — only on whether to
prioritise it now vs. later.

Total: one bead update gap (k2mh entry doesn't list the /252 internal
rename gap explicitly), one branch-not-on-main coordination gap
(persona-spirit pair), one already-resolvable open question
(ItemPriority), and two new minor ugliness patterns flagged below.

## 2. Engine-manager audit (commit 4e928892)

### 2a. What landed

The diff is a faithful consumer-side migration onto the renamed
signal-persona surface (contract commit `92b33ad1` per bead k2mh).
Specifically:

- `src/manager.rs` imports `signal_persona::engine::{Operation,
  Reply}` and matches against `Operation::Query(Query::Catalog(_))`,
  `Operation::Start(_)`, `Operation::Stop(_)`, `Operation::Launch(_)`,
  `Operation::Retire(_)`, `Operation::Tap(_)`, `Operation::Untap(_)`.
- The reply variants drop `Engine*` and `Supervisor*` prefixes
  consistently: `EngineLaunchAccepted` → `Launched`,
  `EngineRetirementRejected` → `RetireRejected`,
  `SupervisorActionAccepted` → `ActionAccepted` etc. Matches the
  workspace ancestry rule in `skills/naming.md`.
- `src/request.rs` rewrites the NOTA codec on `PersonaRequest` and
  `PersonaOutput` using explicit `start_record`/`end_record`/
  `expect_record_head` framing (rather than the previous
  derive-only path). New `ObserverSubscriptionOpened` variant
  added to `PersonaOutput` per the universal Tap mandate.
- `src/schema.rs` adds hand-written `NotaEncode`/`NotaDecode` for
  `EngineEventReport` (previously derived) and switches its
  body-kind sum to `NotaEnum` (the mixed unit/data enum derive
  that replaced `NotaSum` per primary-6wmo).
- Tests are updated to the new vocabulary across `tests/daemon.rs`,
  `tests/manager.rs`, `tests/manager_store.rs`, `tests/request.rs`,
  `tests/state.rs`.

Cargo and Nix verification both passed per bead k2mh's 2026-05-21
18:46 comment.

### 2b. What's pending per /252

Comparing /252's three rename axes against the current persona repo:

- **Axis 1 (signal-persona wire types).** Landed in signal-persona
  `92b33ad`. Types renamed: `SupervisionOperation` →
  `engine_management::Operation`, the umbrella concept name
  `EngineManagementUnimplemented*`, `EngineManagementProtocolVersion`
  are all present in `src/lib.rs`. Done.
- **Axis 2 (persona-internal `EngineSupervisor` actor → `EngineManager`,
  `src/supervisor.rs` → `src/engine_manager.rs`).** Not landed.
  Persona still ships:
  - `src/supervisor.rs` containing `EngineSupervisor` actor
  - `src/supervision_readiness.rs` with `ComponentSupervisionReadiness`
  - `pub mod supervision_readiness; pub mod supervisor;` in
    `src/lib.rs:18-19`
  - Seventeen `supervision_socket_*` identifiers in `src/engine.rs`
    (lines 222-223, 411, 476-485, 567-571, 600, 619-622, 649-650,
    702-703, 743-748, 779-782)
  - Eight `*.supervision.sock` filename constants in `src/engine.rs`
  - `EngineSupervisorInput` import in `src/transport.rs:20`
  - ARCHITECTURE.md lines 477, 496-497, 557-578, 602-608, 725-748
    still contain "supervision" in the role text where it means
    the engine manager's relation with components.
- **Axis 3 (persona-spirit ARCH text).** Not in scope of this
  commit (separate repo); confirmed in §3 below that persona-spirit
  has not touched supervisor-vocabulary in its ARCH.

The bead `primary-k2mh` 18:46 comment lists "manager request path
is not yet modeled through signal-executor component-local Commands"
and "legacy wire_* shims still use signal_core" and "persona CLI
is still manual, not signal_cli!" — but **does not name the /252
internal rename gap** (seventeen lingering `supervision_socket_*`
identifiers, `src/supervisor.rs` not renamed, ARCHITECTURE.md text
not edited). That's a substantive omission from the gap list. The
internal rename is the second-largest pending /252 item after
wire-vocabulary (which is done).

### 2c. New observability surface — good pattern

The diff adds `Operation::Tap(_) | Operation::Untap(_) =>
Reply::ActionRejected(...)` honest-no-op handling at
`src/manager.rs` and `ObserverSubscriptionOpened` to the
`PersonaOutput` enum (`src/request.rs`). This matches the universal
Tap/Untap mandate per intent record 23 (workspace.nota
2026-05-21T10:00Z, "of course! debug the debugger!") and the
no-op-as-explicit-command rule per persona.nota
2026-05-20T15:00:00Z. Good.

## 3. Spirit Magnitude migration audit

### 3a. What landed across both repos

**signal-persona-spirit @ d7b22bfb** (4 files, +26 / -25):
- Deletes the `Certainty` enum outright (`src/lib.rs`, lines 208-215
  in the prior shape). No type alias, no transitional shape — the
  no-transitional-shapes rule per ESSENCE is satisfied cleanly.
- Adds `use signal_sema::{Magnitude, SemaObservation};` (was just
  `SemaObservation`).
- Two field-type changes: `Entry::certainty: Certainty` →
  `Entry::certainty: Magnitude`; `RecordSummary::certainty: Certainty`
  → `RecordSummary::certainty: Magnitude`. **Field name stays
  `certainty`**, which matches /269 §6 — field carries the
  dimension, type carries the scale.
- `Cargo.lock` re-pins signal-sema from `25476a3` to `22b036a` (the
  commit that added Magnitude).
- `examples/canonical.nota` adds one `Record (workspace Decision
  "high summary" "high context" High "high quote")` line, exercising
  the previously-rejected High variant.
- `tests/round_trip.rs` removes the `Certainty` import, adds
  `Magnitude`, and adds a high-magnitude round-trip witness.

**persona-spirit @ d1c76108** (7 files, +40 / -18):
- `src/actors/classifier.rs`: ClassificationPolicy's `fallback_certainty`
  field type flips from `Certainty` to `Magnitude`. Default value
  changes from `Certainty::Minimum` to `Magnitude::Minimum`. Good.
- `src/store.rs` test fixture switches `Certainty::Maximum` to
  `Magnitude::Maximum`.
- `tests/actor_runtime.rs`, `tests/daemon.rs`, `tests/sema_projection.rs`
  similarly migrated.
- `tests/boundary.rs` adds the live witness — see §3c.

### 3b. Match against /269

Item-by-item against /269:

- §3 type definition (seven variants Minimum..Maximum, NotaEnum +
  Archive + Ord derives, signal-sema home, `magnitude.rs` module):
  matches signal-sema `22b036a` (already validated in audit /272).
- §6 "delete the Certainty enum outright (no type alias)": **matches**
  signal-persona-spirit `d7b22bfb` lines 208-215 deletion.
- §6 "field stays certainty: (the dimension), type is Magnitude
  (the scale)": **matches** Entry and RecordSummary changes.
- §6 "caller changes — persona-spirit daemon and tests import
  Certainty directly (tests/sema_projection.rs, tests/daemon.rs,
  tests/actor_runtime.rs, src/actors/classifier.rs, src/store.rs).
  Each import switches to Magnitude from signal-sema": **matches
  exactly** — five consumer files updated.
- §6 "the seven High records in intent/*.nota stop being drift the
  instant the wider Magnitude lands": **conditionally** — true at
  the source level on the branch, but the **deployed binary** is
  pre-Magnitude and still rejects High records on parse.
- §4 (`Magnitude` unwrapped, not `SizeMagnitude`): the operator
  took the designer lean. No psyche ratification yet.
- §8 Q1 (name ratification), Q3 (reserved variant gap), Q4
  (rename-only vs alias): operator implementation followed designer
  leans on all three without explicit psyche confirmation. None
  contradict intent; all are conservative readings.

### 3c. The live witness (the load-bearing test)

`persona-spirit/tests/boundary.rs:218-237` adds:

```rust
#[test]
fn persona_spirit_client_accepts_high_magnitude_and_observes_it_back() {
    let fixture = StoreFixture::new("high-magnitude");
    fixture
        .reply_text(
            "(Record (workspace Decision \"high summary\" \"high context\" High \"high quote\"))",
        )
        .expect("high-magnitude entry persisted");

    let reply = fixture
        .reply_text("(Observe (Records (None None SummaryOnly)))")
        .expect("records observed");

    assert_eq!(
        reply,
        "(RecordsObserved ([(1 workspace Decision \"high summary\" High)]))"
    );
}
```

This is the witness `/269` §"Migration impact" called for: a record
carrying `High` writes through the full client→daemon path and reads
back unchanged. It runs through `StoreFixture` (the live persona-spirit
client/runtime fixture), not a unit-only round-trip. Quality is good.

The witness does NOT exercise: subscriptions on High records, Ord
comparisons on Magnitude values, or the migration of the seven
existing `High` records in `intent/*.nota`. Those are out of scope
for this slice.

### 3d. Branch vs main vs deployed state

| Repo | Magnitude branch | main | Deployed user-profile binary |
|---|---|---|---|
| signal-sema | n/a (Magnitude on main) | `22b036a` (has Magnitude) | n/a (library, not deployed) |
| signal-persona-spirit | `d7b22bfb` (has Magnitude) | `cda5469` (still has Certainty) | n/a |
| persona-spirit | `d1c76108` (has Magnitude) | `5f83a1d` (still has Certainty) | `694452a` (pre-Magnitude) |

The deployed `spirit` CLI built from CriomOS-home pinning is at
`694452a`, which predates this migration by five commits. Live test:

```
$ spirit '(Record (test Decision "test" "test" High "test"))'
Error: InvalidSpiritRequest { reason: "unknown variant `High` for enum `Certainty`" }
```

Confirms the deployed binary still rejects High. Until the operator
merges `operator/spirit-response-protocol` into main and CriomOS-home
re-pins, the seven High records in `intent/*.nota` remain rejected
and any agent submitting High records through the deployed CLI hits
the same error.

### 3e. Bead k2mh's missing gap

Bead `primary-ojxq` 18:53 comment correctly names the work landed
("designer/269 Magnitude migration through Spirit … delete Certainty
… High round-trip witness … operator/spirit-response-protocol
branch"). It does not name "branch not on main; deployed binary
unchanged; intent/*.nota High records still rejected by deployed
spirit" as the *remaining* status. That's the gap from the
bead-versus-reality reading.

## 4. ItemPriority resolution (intent record 70 verbatim)

The operator wrote: "Should signal-persona-mind::ItemPriority
collapse into signal_sema::Magnitude too? Designer leans yes, but
/269 marks that as a psyche decision, so I did not touch mind."

**This is wrong on the gating.** Intent record 70 in spirit's sema
database explicitly authorises the collapse. Verbatim record (queried
via `spirit '(Observe (Records (None None WithProvenance)))'`,
provenance shape: `((70 component-shape Decision <summary> Maximum)
<context> 2026-05-21 14:22:20 <quote>)`):

> Universal Magnitude type — replace per-component Certainty enums
> **(and any other small-vocabulary ordinal enum reaching for the
> same concept)** with a single Magnitude type living in the
> workspace's shared-data-type-library (signal-core or whatever the
> workspace's shared-typed-record crate is). Magnitude has 7
> variants: Minimum, VeryLow, Low, Medium, High, VeryHigh, Maximum.
> Binary cost is identical regardless of variant count because rkyv
> serialises to a fixed-byte discriminator; using 7 universally is
> free. Systems can choose to action only on the subset they care
> about (e.g., only Minimum/Medium/Maximum); the variant set is
> the schema, the consumption is per-component policy. ... Supersedes
> the Maximum/Medium/Minimum-only Certainty enum currently in
> signal-persona-spirit (and likely elsewhere). Resolves the
> certainty-drift finding from /267 by widening the vocabulary
> rather than mapping High onto Maximum.

The parenthetical clause **"(and any other small-vocabulary ordinal
enum reaching for the same concept)"** directly names ItemPriority's
shape: five-variant ordinal `Critical / High / Normal / Low /
Backlog`, closed-set, unit-variant, ordered. Same shape as Certainty,
same concept (a position on a coarse magnitude scale), same drift
risk.

**Conclusion: ItemPriority collapse onto Magnitude IS authorised
by intent record 70. No further psyche decision needed for the
"whether" — only for sequencing ("do this now vs. after sema-upgrade
lands" is operator/designer territory, not psyche).**

/269 §"Q2 ItemPriority collapse" was filed before record 70 had been
written; the report's "psyche's call" framing reflects the state at
the time. With record 70 landed, that question is closed.

The mapping for the collapse is the obvious one from /269 §7 path 1:
`Critical → Maximum`, `High → High`, `Normal → Medium`, `Low → Low`,
`Backlog → Minimum`. Field name `priority:` carries the dimension,
type is `Magnitude`. No bits lost.

## 5. Other Magnitude-collapse candidates (workspace scan)

Workspace-wide scan for small-vocabulary ordinal enums that "reach
for the same concept" as Certainty/ItemPriority. The diagnostic is:
unit-variant, closed-set, the variants name a position on a single
ordered scale (rather than category labels).

| Crate | Enum | Location | Variants | Ordinal? | Verdict |
|---|---|---|---|---|---|
| signal-persona-mind | `ItemPriority` | `src/lib.rs:555-562` | Critical/High/Normal/Low/Backlog | Yes | **Collapse candidate** — authorised by record 70 |
| signal-persona-mind | `Confidence` | `src/graph.rs:496-502` | Asserted/Cited/Tested/Disputed | **No** (categorical, not ordinal — Disputed is not above or below Asserted) | Keep |
| signal-persona-system | `SystemHealth` | `src/lib.rs:262-266` | Running/Degraded/Stopped | Sort of (Running > Degraded > Stopped in "how alive") | **Possibly** — same shape as a magnitude on a health axis. Three variants, ordered, no payload. |
| signal-persona-system | `SystemReadiness` | `src/lib.rs:268-272` | Ready/Starting/Unavailable | Sort of | **Possibly** — same shape (readiness axis, three-step). |
| signal-persona-harness | `HarnessHealth` | `src/lib.rs:230-234` | Running/Degraded/Stopped | Same as SystemHealth | **Possibly** (duplicate of SystemHealth's shape) |
| signal-persona-harness | `HarnessReadiness` | `src/lib.rs:237-241` | Ready/Starting/Unavailable | Same as SystemReadiness | **Possibly** (duplicate) |
| signal-persona-introspect | `ComponentReadiness` | `src/lib.rs:105-109` | Ready/NotReady | Boolean dressed as enum | Keep (not magnitude — pure binary, the no-payload boolean case from `skills/typed-records-over-flags.md`) |
| signal-persona-mind | `ItemStatus` | `src/lib.rs:544-552` | Open/InProgress/Blocked/Closed/Deferred | **No** (categorical — Blocked is not "above" Open) | Keep |
| signal-persona-orchestrate | `HarnessKind` | `src/lib.rs:162` | (not inspected; named "Kind") | **No** (probably categorical) | Keep |
| signal-persona-router | `RouterChannelStatus` | `src/lib.rs:266` | (not inspected) | Probably categorical | Likely keep |

The cleanly-confirmed second candidate is `ItemPriority`. The
duplicated `SystemHealth`/`HarnessHealth`/`SystemReadiness`/`HarnessReadiness`
pairs are interesting: each repeats the same three-variant ordinal
shape across two crates. /269's framing — "the variant set is the
schema, the consumption is per-component policy" — applies. Whether
they migrate is a deeper design question (do Health and Readiness
deserve their own universal types, or fold both onto Magnitude with
the dimension carried by the field name like `health: Magnitude`,
`readiness: Magnitude`?). Probably the latter, given record 70's
universalising rationale, but two new candidates emerge for the
psyche:

- Health / readiness scales appear duplicated across `signal-persona-system`
  and `signal-persona-harness`. Same shape, same concept. Collapse?
- If yes, the field-name-carries-dimension principle says
  `system.health: Magnitude` and `harness.health: Magnitude` and a
  consumer matching `>= Magnitude::Medium` means "at least
  partly healthy" across both components. That reads cleanly.

These extensions warrant a follow-up designer report (or a
short addendum to /269) — they are NOT load-bearing for this audit.
The clean answer for the audit is: **ItemPriority is collapse-ready
under record 70; health/readiness pairs are candidates worth a
fresh designer pass.**

## 6. Sema-upgrade open questions vs intent

The operator named /270's remaining "authority / self-upgrade /
open-placement" questions. Walking each against current intent:

### 6a. Authority — who owns sema-upgrade?

**Answered from intent (partially).** Intent record 38
(persona.nota 2026-05-19T15:30:00Z): "Spirit owns mind in the
authority graph. supervisor → spirit → mind → orchestrate →
router/harness/terminal." Intent record 67 (persona.nota
2026-05-20T14:50:00Z) clarifies "engine management is what we're
naming things that have to do with the persona daemon, which is
the engine manager."

Sema-upgrade is **workspace infrastructure under every persona
daemon** (per /270 §9 question 5). Not a persona-cognitive
component, so it doesn't slot into the spirit→mind→orchestrate
chain. The natural owner is the **engine manager** (persona-daemon)
itself — sema-upgrade is the runtime that bridges deploys, and the
engine manager is the role that owns deploy infrastructure. /270
§9 question 5 already states "owner caller is likely the engine
manager directly" as a designer lean.

**Verdict: lean-confirmed from intent**, not psyche-decided.
Designer lean is "engine manager owns sema-upgrade authority";
psyche could ratify quickly.

### 6b. Self-upgrade — how does sema-upgrade upgrade itself?

**Not in intent.** This is a clean bootstrap problem the psyche
hasn't addressed. /270 §9 question 3 names two paths: (a) recursive
(it calls itself), (b) hand-written code-path because it's the
bottom of the stack. The recursive path is elegant but pre-supposes
that sema-upgrade's contracts are stable enough to be self-applied;
the hand-written path is conservative but admits an asymmetry in
the workspace's universal upgrade mechanism.

**Verdict: needs psyche decision.** Material for the chat reply.

### 6c. Open placement — where in the persona graph?

**Not in intent.** /270 §1-3 puts sema-upgrade alongside but
*beside* the persona components. Each persona daemon's boot path
consults sema-upgrade before opening its sema database. The
relationship is "every persona daemon is a Signal client of
sema-upgrade at startup," not "sema-upgrade is in the persona
authority chain at a particular position." That said, the question
of where in the **engine boot order** sema-upgrade slots is open:
must it start before persona-daemon (so persona-daemon can consult
it at boot)? If yes, sema-upgrade is engine-pre-zero infrastructure.

Related intent: record 17 (persona.nota 2026-05-19T14:00:00Z)
states spirit is "the last one to start" in the persona engine
boot order. Symmetric question for sema-upgrade: is it the
**first** to start? Plausible from /270 §5 (every other daemon
asks it `Inspect` before serving), but psyche hasn't stated it.

**Verdict: needs psyche decision.** Material for the chat reply.

## 7. New patterns observed (the good)

1. **Live boundary witness for vocabulary widening.** The
   `persona_spirit_client_accepts_high_magnitude_and_observes_it_back`
   test in `persona-spirit/tests/boundary.rs:218-237` is the right
   shape for any vocabulary-widening pilot — exercise a previously-
   rejected value end-to-end through the real client/daemon path.
   This pattern should propagate to future vocabulary migrations
   (the ItemPriority collapse should land with an
   `accepts_critical_magnitude_and_observes_it_back` test in
   persona-mind, etc.).

2. **Outright deletion of Certainty, no transitional alias.**
   `signal-persona-spirit/src/lib.rs` diff shows the Certainty enum
   removed in its entirety (lines 208-215 in the pre-state). No
   `pub type Certainty = Magnitude;` alias was inserted. Matches
   ESSENCE "backward compatibility is not a constraint" and /269
   §6's explicit "rename-only, no alias" lean. The operator did
   not weaken the design with a transitional shape.

3. **Field name `certainty:` preserved at use sites.** Per /269 §6
   the *field* (dimension) name stays `certainty:` while the *type*
   (scale) becomes `Magnitude`. The operator implemented this
   exactly. Establishes the pattern for ItemPriority collapse
   (field stays `priority:`, type becomes `Magnitude`) and any
   future health/readiness collapse (`health: Magnitude`,
   `readiness: Magnitude`).

4. **Universal Tap/Untap mandate honoured in persona daemon.**
   `src/manager.rs` adds `Operation::Tap(_) | Operation::Untap(_)`
   to the match. The handler returns `ActionRejected` for now
   (persona's observer surface isn't wired yet), which is honest
   placeholder behaviour. Better than a panic and matches the
   "debug the debugger" principle (record 23, workspace.nota
   2026-05-21T10:00Z).

5. **Hand-written codec for `EngineEventReport`.** The persona
   commit replaces the previous derive-only codec on
   `EngineEventReport` with explicit
   `start_record("EngineEventReport")` / `expect_record_head`
   framing. Reads as English; matches the workspace's preference
   for typed records over generic dispatch. This is the right
   shape when a record has nested record children that need
   ordering control.

## 8. Ugly patterns / philosophy deviations (the bad)

1. **`src/supervisor.rs` and `src/supervision_readiness.rs` remain
   in persona.** /252 axis 2 was explicit: `src/supervisor.rs` →
   `src/engine_manager.rs`, `EngineSupervisor` → `EngineManager`.
   The contract-side wire vocabulary has migrated cleanly to
   `engine_management`; the daemon's internal module path still
   says `supervisor`. This is workspace-discipline drift in
   exactly the place /252's risk note (search-and-replace traps)
   flagged — manual review required. The wire is right; the impl
   is half done. The bead doesn't list this as a remaining gap.
   Per `skills/beauty.md` §"if it isn't beautiful, it isn't done":
   isn't done.

2. **Seventeen `supervision_socket_*` identifiers in `src/engine.rs`.**
   Filename constants like `mind.supervision.sock`,
   `orchestrate.supervision.sock` etc. (lines 478-485) and field
   names `supervision_socket_path`, `supervision_socket_mode`
   (lines 600, 619-622, 649-650, 702-748). Per /252 §1.4 these
   are ABI break candidates (Nix derivations carry the env-var
   names). The contract surface renamed but the runtime
   path-construction code hasn't. The internal `supervision_socket`
   field on `SpawnEnvelope` (signal-persona @ 92b33ad still
   exposes `engine_management_socket_path` per the grep
   confirmation in §3 earlier) and the persona-side
   `supervision_socket_path` field do not match. There's a
   contract-vs-runtime disagreement on field names. Possibly
   internal mapping covers it; the disagreement is itself ugly.

3. **Bead k2mh's remaining-gaps list omits the /252 internal
   rename.** The bead enumerates "wire_* shims still use
   signal_core; persona CLI is still manual, not signal_cli!;
   manager request path is not yet modeled through signal-executor
   component-local Commands" — three real gaps. But the seventeen
   supervision identifiers plus the unrenamed module files are
   the larger pending /252 axis. A reader of the bead would not
   know /252's internal rename is incomplete.

4. **Branch-not-on-main coordination drift on persona-spirit.**
   The Magnitude migration sits on `operator/spirit-response-protocol`
   in both signal-persona-spirit and persona-spirit. There is no
   stated reason this couldn't have landed on main — the only
   psyche question was Q2 (ItemPriority), which the operator
   declined to act on, leaving the Certainty-only slice that has
   no open question. The branch parking is itself a transitional
   shape and accumulates rebase cost. Per ESSENCE "the cost of a
   wrong shape compounds": branch divergence has the same shape.

5. **Bead k2mh's PR/branch state not surfaced to deploy.** The
   deployed `spirit` binary on `/home/li/.nix-profile/bin/spirit`
   is at `694452a`, five commits behind even the persona-spirit
   `main` tip (`5f83a1d`), and seven commits behind the Magnitude
   tip on the branch. The intent log records show seven `High`
   entries that the deployed daemon rejects on parse — these are
   the records /267-v2 first surfaced. Per record 70's framing,
   these records are first-class the moment the deployed binary
   carries Magnitude. They are not first-class today. This is
   an end-to-end gap that needs surfacing — the new contract is
   built but not deployed.

Counts: **5 good patterns; 5 ugly / unfinished patterns.** Score
is slightly negative because the unfinished work hasn't been
surfaced in beads or chat, and the deployed-binary gap actively
blocks the substrate replacement the psyche prioritised.

## 9. Intent-clarity-critical points needing psyche decision

Each is described with enough substance that the psyche can engage
without opening the report.

### 9a. Should sema-upgrade-daemon start before persona-daemon in the engine boot order?

**The question.** /270 puts sema-upgrade beside persona components,
not in the cognitive chain. Every persona daemon consults
sema-upgrade at boot before opening its sema database (per /270 §5).
If sema-upgrade is the consult-target, it must be up before any
caller wakes up — so it must be **the first daemon** in the boot
order. This is symmetric to record 17 (persona.nota
2026-05-19T14:00Z, "spirit is the last one to start"): sema-upgrade
might be the first.

**Why it matters.** The engine-manager boot graph (in persona/ARCH
manifest section) declares an explicit start order based on
dependencies. If sema-upgrade is engine-pre-zero (i.e., the
engine-manager starts sema-upgrade before any other persona
daemon), it has to land **before** any of the existing persona
daemons can integrate Approach C schema-version reading on their
boot path. This sequences the next several months of work.
Alternative: sema-upgrade isn't a persona daemon at all but a
systemd-level peer the engine-manager doesn't own — different
authority model, different placement.

**What intent suggests.** Record 17 explicitly orders spirit last,
indicating the psyche thinks about engine boot order. /270 §9
question 5 names the engine manager as the lean owner of
sema-upgrade authority. /270 §5 explicitly puts sema-upgrade in
the inspect-before-serve path, which only works if sema-upgrade
is up before the inspector. Designer lean: sema-upgrade is the
first persona daemon to start, owned by the engine manager.

**Load-bearing fork.** Whether sema-upgrade is *in* the persona
graph at all (and thus subject to engine-manager lifecycle), or
*outside* it as a systemd peer the engine-manager calls into,
shapes the boot dependency graph, the recovery semantics if
sema-upgrade itself fails, and the authority surface.

### 9b. How does sema-upgrade upgrade itself?

**The question.** /270 §9 question 3: recursive self-application
(sema-upgrade upgrades sema-upgrade using its own machinery) vs.
hand-written bootstrap path (acknowledging sema-upgrade is the
bottom of the upgrade stack).

**Why it matters.** Recursive elegance is appealing — universal
mechanism eats itself. But it requires sema-upgrade's contracts
to stabilise first; an in-flight contract change to sema-upgrade
itself would risk corrupting the workspace's universal upgrade
machinery during the upgrade. The hand-written path concedes the
bottom-of-stack asymmetry: sema-upgrade is special and its own
schema migrations are handled by code-path before sema-upgrade
ever runs.

**What intent suggests.** No intent record speaks to this. /270
§9 question 3 designer lean is "hand-written path until
sema-upgrade's contracts stabilise, then dogfood once." The
"dogfood once" framing is reasonable but introduces a flip-point
that needs flagging.

**Load-bearing fork.** This is a foundational architectural
decision; the answer determines whether the workspace's universal
upgrade mechanism has a self-reference or an acknowledged
boundary. Has knock-on effects on /263's schema-specification
language (does it have to describe its own evolution rules?).

### 9c. Does the operator merge `operator/spirit-response-protocol` now, or does it wait?

**The question.** The Magnitude migration sits on the branch in
both spirit repos. No open psyche question gates it. The operator
declined to also touch ItemPriority because /269 framed that as
psyche-decision territory — but record 70 already resolved
ItemPriority. The branch can be merged today.

**Why it matters.** The deployed `spirit` binary still rejects
`High`. The intent log has seven `High` records the spirit binary
will not accept. The substrate-replacement intent (record 26,
persona.nota 2026-05-20T15:00Z: "spirit becomes the canonical
intent-record substrate; the .nota files retire once spirit
ships") is actively blocked by the deploy gap. The longer the
branch sits, the longer the substrate replacement is gated on
nothing — there is no remaining open question on the slice
itself.

**What intent suggests.** Record 26 makes the substrate
replacement explicit. Record 70 makes ItemPriority's collapse
authority explicit. The path is: (1) merge the current branch to
land Spirit's Magnitude on main; (2) ship ItemPriority's collapse
in a follow-up slice; (3) bump CriomOS-home to redeploy the new
spirit binary; (4) the seven `High` records become first-class.

**Load-bearing fork.** Does the psyche want the branch held while
the broader Magnitude-everywhere migration consolidates (one big
merge), or merged now (small slices, fast cadence)? Workspace
default is fast cadence (record 56, workspace.nota
2026-05-19T17:30Z, "We're moving fast now"). Designer lean: merge
now.

### 9d. Health / readiness collapse onto Magnitude (record 70 extension)

**The question.** Beyond ItemPriority, four ordinal enums of the
same shape live in signal-persona-{system,harness}: SystemHealth,
SystemReadiness, HarnessHealth, HarnessReadiness. All are
three-variant ordinal scales (Running/Degraded/Stopped and
Ready/Starting/Unavailable respectively). Record 70's
parenthetical authorises collapse of "any other small-vocabulary
ordinal enum reaching for the same concept" — but Health and
Readiness reach for slightly different concepts than Magnitude
("how well is the daemon running" vs. "how high is the rank").

**Why it matters.** If the answer is "all magnitudes are
Magnitude," then `health: Magnitude` and `readiness: Magnitude`
become the pattern with the field name carrying the dimension —
following /269 §6's design exactly. The duplication across
system/harness disappears. Cross-component observers can write
`>= Magnitude::Medium` and have it mean "at least partially
healthy" uniformly across both daemons.

If the answer is "Health and Readiness are their own scales
because the operational semantics differ from rank," then
signal-sema gets two more universal types (`Health`, `Readiness`)
and the per-component duplicates retire onto them.

**What intent suggests.** Record 70 frames Magnitude as
"shared-typed-record-library of our most used data types that are
just the same on so many components." That argues for one universal
Magnitude and field-name-carries-dimension. Designer lean: collapse
to Magnitude.

**Load-bearing fork.** This determines whether signal-sema grows
a Magnitude-only vocabulary leaf or a small family of universal
ordinal types. Cheap to ask now; expensive to undo later.

## 10. Recommended next operator slices

In priority order:

1. **Merge `operator/spirit-response-protocol` in both spirit
   repos to main**, gated on the open-question 9c. Single slice;
   no remaining design ambiguity.

2. **Bump CriomOS-home spirit pinning so the deployed spirit
   binary picks up Magnitude.** Unblocks the seven `High`
   intent-log records and the substrate-replacement work.

3. **Complete /252 axis 2 inside persona.** Rename
   `src/supervisor.rs` → `src/engine_manager.rs`, `EngineSupervisor`
   → `EngineManager`, the seventeen `supervision_socket_*`
   identifiers, the eight `.supervision.sock` filename constants,
   the ARCHITECTURE.md text, and the env-var names (Nix-side
   atomic update per /252 §5 risk notes). Update bead k2mh's
   gaps list to reflect this.

4. **ItemPriority → Magnitude collapse in signal-persona-mind**
   (record 70 authorises; no psyche gate). Follow the
   signal-persona-spirit shape: delete `ItemPriority` outright,
   import `Magnitude`, the field stays `priority:`. Add a live
   witness in persona-mind exercising `Critical` (the previously-
   highest variant) and `Backlog` (the previously-lowest)
   end-to-end through whichever daemon ingests opening records.

5. **Health/Readiness collapse decision via psyche** (9d), then
   collapse if confirmed.

6. **Sema-upgrade boot-order + self-upgrade decisions** (9a, 9b),
   then begin sema-upgrade triad scaffolding per /270.

## 11. References

- Operator commits: persona `4e928892`, signal-persona-spirit
  `d7b22bfb`, persona-spirit `d1c76108`.
- `reports/designer/252-engine-management-rename.md` — the
  authoritative rename design.
- `reports/designer/269-universal-magnitude-type-design.md` — the
  Magnitude design the Spirit slice implements.
- `reports/designer/270-sema-upgrade-component-design.md` — the
  sema-upgrade design with the three open questions /268's framing
  references.
- `reports/designer/272-audit-of-operator-state-2026-05-21.md` —
  prior audit, names the Magnitude landing in signal-sema and the
  consumer-migration-not-started gap.
- `reports/designer/273-schema-migration-synthesis-post-operator-151.md`
  — Schema-migration synthesis; absorbs operator/151's refinements
  into the sema-upgrade picture.
- `reports/designer/274-forge-skeleton-reconciliation.md` —
  unrelated to this audit but read for completeness.
- `intent/component-shape.nota` — engine-management rename intent
  records (2026-05-20T14:30Z, 14:50Z).
- `intent/persona.nota` — spirit / engine-manager / substrate-
  replacement intent records 17, 26, 38, 67.
- Spirit sema database (queried via
  `spirit '(Observe (Records (None None WithProvenance)))'`) —
  intent record 70 (component-shape Decision, Magnitude
  authorisation) authorises ItemPriority collapse and reaches
  beyond.
- `bd show primary-k2mh` — engine-manager triad migration bead
  (gaps list does not include /252 internal rename).
- `bd show primary-ojxq` — persona-spirit triad bead (Magnitude
  migration recorded; branch-vs-main coordination not surfaced).
- `signal-persona/src/lib.rs` lines 480-499 — `engine_management`
  module landed in contract.
- `persona/src/manager.rs`, `persona/src/request.rs`,
  `persona/src/schema.rs`, `persona/src/supervisor.rs`,
  `persona/src/supervision_readiness.rs`, `persona/src/engine.rs`
  — diff sites and unfinished rename sites.
- `signal-persona-spirit/src/lib.rs`,
  `signal-persona-spirit/tests/round_trip.rs`,
  `signal-persona-spirit/examples/canonical.nota` — the spirit
  contract Magnitude migration.
- `persona-spirit/tests/boundary.rs:218-237` — the load-bearing
  live witness.
- Live deployed-binary check:
  `spirit '(Record (test Decision "test" "test" High "test"))'`
  returns `Error: InvalidSpiritRequest { reason: "unknown variant
  'High' for enum 'Certainty'" }` — confirms the deployed binary
  still rejects High; the migration is on a branch, not in the
  user-profile binary.
