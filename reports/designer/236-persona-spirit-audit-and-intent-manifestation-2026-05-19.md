# 236 — persona-spirit: audit and intent manifestation

*Deep review of the `persona-spirit` implementation as it stands
2026-05-19 17:00, paired with an intent-manifestation sweep
against the workspace intent surface. Two operator slices have
landed (raw triad scaffold + typed `Entry` decoder); the daemon,
classifier, and storage do not yet exist. Surfaces four questions
to the psyche; resolutions land in `intent/persona.nota` 17:30Z
(seven new records).*

## 0 · TL;DR

What's on disk:

| Surface | Status |
|---|---|
| `signal-persona-spirit` contract | Type-checked `PsycheStatement` + `Entry` + queries + subscriptions; round-trip tested |
| `owner-signal-persona-spirit` contract | Lifecycle + identity Mutates; tested |
| `persona-spirit` CLI | Decodes one `SpiritRequest`, returns typed `SpiritRequestUnimplemented` |
| `persona-spirit-daemon` | Binary entry; runtime errors out |
| `bootstrap-policy.nota` | One-line placeholder pointing at right-knowledge / right-action |
| `persona-spirit.redb` | Not opened |
| Classifier | Not present |
| Spirit→mind owner caller | Not present |

Every endpoint returns
`(SpiritRequestUnimplemented <Operation> NotBuiltYet)`. The daemon
does not pretend to exist.

**The audit's load-bearing finding:** the `Entry` type currently
carries `verbatim: Vec<Verbatim>`, following one psyche statement.
A later psyche statement contradicts this — *"each psyche
statement is its own top-level record … no nested vectors."*
Both records Maximum certainty; only the psyche can supersede.
Surfaced as Q1; psyche resolved to **separate records** —
restatement is signal by repetition. Detail in §4 + §7.

## 1 · What the operator has built (snapshot)

Operator reports landed: `/136 persona-spirit current system and
intent gaps`. Bead `primary-ojxq` has two progress comments
(foundation slice 12:37; typed Entry decoder 13:17).

### `signal-persona-spirit` — ordinary contract

Typed values (`NotaTransparent` newtypes over `String`):

```
IntentTopic           IntentSummary        IntentQuote
IntentContext         IntentTimestamp      IntentRecordIdentifier
PsycheStatementText   PsycheFocusArea      ClarificationQuestionText
ClarificationQuestionIdentifier            u64 SubscriptionTokens
```

Typed enums (PascalCase variants, `NotaEnum`):

```
IntentKind: Decision | Principle | Correction | Clarification | Constraint
IntentCertainty: Maximum | Medium | Minimum
IntentObservationMode: SummaryOnly | WithProvenance
PsychePresence: Active | Absent
SpiritOperationKind: …
SpiritUnimplementedReason: NotBuiltYet | IntegrationNotLanded
```

Typed records (positional `NotaRecord`):

```
PsycheStatement      { statement: PsycheStatementText }
Verbatim             { timestamp: IntentTimestamp, quote: IntentQuote }
Entry                { topic, kind, summary, context, certainty,
                       verbatim: Vec<Verbatim> }
IntentRecordQuery    { topic: Option<IntentTopic>, mode: IntentObservationMode }
IntentRecordObservation        { query: IntentRecordQuery }
IntentRecordSubscription       { topic, mode }
IntentRecordSummary  { identifier, topic, kind, summary, certainty }
IntentRecordProvenance { summary: IntentRecordSummary, context, verbatim: Vec<Verbatim> }
PsycheState          { presence, focus: Option<PsycheFocusArea> }
PsycheStatementAccepted   { captured: IntentRecordSummary }
PsycheStateObserved       { state: PsycheState }
IntentRecordsObserved     { records: Vec<IntentRecordSummary> }
ClarificationQuestionsObserved { questions: Vec<ClarificationQuestionSummary> }
PsycheStateSubscriptionOpened  { token, snapshot }
IntentRecordSubscriptionOpened { token, snapshot: Vec<IntentRecordSummary> }
SpiritRequestUnimplemented     { operation, reason }
PsycheStateChanged             (stream event)
IntentRecordCaptured           (stream event)
```

Channel:

```
request SpiritRequest {
    Assert    PsycheStatement, Entry
    Match     PsycheStateObservation, IntentRecordObservation, ClarificationQuestionPending
    Subscribe SubscribePsycheState opens PsycheStateStream,
              SubscribeIntentRecords opens IntentRecordStream
    Retract   PsycheStateSubscriptionRetraction, IntentRecordSubscriptionRetraction
}
```

### `owner-signal-persona-spirit` — owner-only contract

```
Mutate  StartSpiritOrder { generation }
Mutate  DrainAndStopOrder
Mutate  ReloadBootstrapPolicyOrder
Mutate  RegisterPsycheIdentity { name }
Retract RetirePsycheIdentity   { name }
```

Reply variants include `OwnerSpiritRequestUnimplemented`.

### `persona-spirit` — daemon repo

```
src/argument.rs        — one-argument boundary parser + flag rejection
src/error.rs           — typed Error enum
src/runtime.rs         — SpiritClient + SpiritRequestText + DaemonRuntime
src/bin/persona-spirit.rs            — thin CLI: decode → reply
src/bin/persona-spirit-daemon.rs     — daemon binary entry; runtime errors out
bootstrap-policy.nota                — `(SpiritRootIntent "…")` placeholder
tests/boundary.rs      — argument-count + decoder witnesses
ARCHITECTURE.md        — accurate; Status section names the not-built surfaces
```

`DaemonRuntime::run()` returns `Error::RuntimeNotImplemented`.

## 2 · Intent records relevant to spirit (manifestation table)

A record is "manifested" when its substance appears in the
behavior-shaping surface a reader would consult.

| # | Topic · timestamp | Substance | Manifested in | Status |
|---|---|---|---|---|
| 1 | persona · 2026-05-18T12:08:41 | mind owns STATE / orchestrate owns MACHINERY | /233 + orchestrate repo | Manifested |
| 2 | persona · 2026-05-18T12:23:18 | persona-orchestrate is a real triad | /233 + INTENT.md persona-orchestrate references | Manifested |
| 3 | persona · 2026-05-19T14:00 | spirit is new triad; apex; spawned last | /232 + INTENT.md "Persona-spirit is the apex" + persona-spirit/ARCH | Manifested |
| 4 | persona · 2026-05-19T14:00 | "persona is meta AI; what animates humans is spirit" | /232 §1 only | **Gap — ESSENCE-promotion candidate** |
| 5 | persona · 2026-05-19T14:00 | spirit is most important; implement now | bead `primary-ojxq` | Manifested |
| 6 | persona · 2026-05-19T15:30 | spirit owns mind; verb set develops | /232 §8 + persona-spirit ARCH | **Half-manifested — persona-mind/ARCH does not yet say "owned by spirit"** |
| 7 | persona · 2026-05-19T15:30 | bootstrap-policy.nota IS first intent / root of spirit | /232 §4 + bootstrap-policy.nota placeholder | Manifested (research arc deferred) |
| 8 | persona · 2026-05-19T15:30 | "no persona component works without LLMs" | /232 §8 only | **Gap — universal persona principle** |
| 9 | persona · 2026-05-19T15:30 | agent-CLI flow; NOTA arg | /232 §8 + AGENTS.md | Manifested |
| 10 | persona · 2026-05-19T15:30 | summary-first query surface | /232 §5 + contract | Manifested |
| 11 | persona · 2026-05-19T15:30 | richer supersession: negation / lowering / escalation / spirit guardian | /232 §8 only | **Gap — `skills/intent-maintenance.md` still binary** |
| 12 | persona · 2026-05-19T15:30 | "components in raw form first; integration follows" | /232 §8 only | **Gap — universal workspace principle** |
| 13 | persona · 2026-05-19T15:30 | "I love the intent protocol because I feel I'm not going to lose what I'm saying" | nowhere | **Gap — ESSENCE-promotion candidate** |
| 14 | persona · 2026-05-19T13:48 | proceed on spirit; stop when intent unclear | session-specific | n/a |
| 15 | persona · 2026-05-19T12:16 | move persona-orchestrate forward | bead `primary-hrhz` + /233 | Manifested |
| 16 | persona · 2026-05-19T13:08:11 | first slice = typed intent logging/querying with CLI type-checking | operator commits + Entry contract | Manifested |
| 17 | persona · 2026-05-19T13:08:11 | "verbatim object is going to be a vector ... struct" | signal-persona-spirit `Entry { verbatim: Vec<Verbatim> }` | **Superseded by Q1 resolution** |
| 18 | nota · 2026-05-19 19:45 | "each psyche statement is its own top-level record. … no nested vectors." | `intent/<topic>.nota` filesystem schema | Affirmed; now extended to persona-spirit |
| 19 | persona · 2026-05-19T14:45:43 | inside persona-spirit, intent is the domain — `Entry`, not `IntentEntry` | signal-persona-spirit Entry type | **Now generalised — every `Intent*` type drops the prefix** |

## 3 · Implementation audit against intent

What lines up cleanly with intent:

- **Spirit is a triad.** Three repos, contract pair, daemon + thin
  CLI. Component-triad invariants present.
- **One-NOTA-argument rule.** Both binaries parse exactly one
  `SingleArgument`; flag-style args rejected with witness tests.
- **Summary-first query surface.** `IntentObservationMode` carries
  `SummaryOnly | WithProvenance`.
- **Honest unimplemented replies.** No fake daemon behavior.
- **Owner contract carries policy reload.** `ReloadBootstrapPolicyOrder`
  exists, anticipating policy-state mutations.
- **No spirit→mind owner caller yet.** Aligns with intent #6.
- **No classifier yet.** Operator stopped at unclear intent.

What was unsettled and is now resolved by the 17:30Z intent
records:

- **`Entry.verbatim` shape.** Was the load-bearing contradiction.
  Resolved: separate records. The contract loses
  `Entry.verbatim: Vec<Verbatim>`; each Assert is one top-level
  record. See §4 + §7.
- **Identity on records.** Resolved: spirit mints; agents never
  supply. RecordIdentifier (post-rename) is output-only on the
  wire.
- **Authority of agent input.** Resolved: spirit is dumb storage;
  trusts agent typing; the guardian is a future arc.
- **Type naming.** Resolved: drop `Intent` prefix on every
  contract type unless removing it produces real ambiguity.

Smaller items:

- **Reply variant for `Assert Entry`.** Only
  `PsycheStatementAccepted` exists. The single-record resolution
  may want one consolidated `RecordAccepted` reply for both
  Assert variants.
- **`IntentTimestamp` is `String`.** Bead `primary-dzrn` (open)
  is the bare-ISO-8601 Timestamp type. Once it lands, swap.

## 4 · The verbatim-shape contradiction (now resolved)

Two psyche intent records, both `Maximum` certainty, disagreed
on restatement shape.

**Intent #17** (`intent/persona.nota`, 2026-05-19T13:08:11Z):

> *"every intent, because it can be restated, can have multiple
> verbatim references. So that the verbatim object is going to be
> a vector, and that because every verbatim entry is going to
> have a timestamp, it's going to be a struct."*

**Intent #18** (`intent/nota.nota`, 2026-05-19 19:45):

> *"Restatement shape for intent records: each psyche statement
> is its own top-level record … No nested vectors, no superfluous
> wrappers. Append-only (lock-free). Dedup is a query-time
> operation … Recency = the latest matching record's timestamp."*

**Resolution (intent/persona.nota 2026-05-19T17:30Z):**

> *"separate records then. repeated similar intents will mean
> stronger signal"*

Implication: spirit's `Entry` loses `verbatim: Vec<Verbatim>`.
Each Assert is a single top-level record (one timestamp, one
quote). Restatement is read-side: agents query, the read layer
clusters records by summary similarity, and repetition itself
encodes intensity. The data model uses repetition as the
load-bearing primitive instead of a per-record intensity field.

## 5 · Operator's five gaps, reviewed

| Gap | Substance | Resolution |
|---|---|---|
| 1 | Is `Entry` an aggregate record or an assertion event? | Resolved: assertion event. Separate top-level records. |
| 2 | Who mints `IntentRecordIdentifier` — agent or spirit? | Resolved: spirit mints; agents never supply. RecordIdentifier is output-only. |
| 3 | How authoritative is an agent-supplied `Entry`? | Resolved: agent-supplied input is authoritative. Spirit is dumb storage today. |
| 4 | First durable query surface? | Mostly settled: `(topic, mode)` first; filters follow when usage demands. |
| 5 | Filesystem projection in raw spirit? | Operator's lean (no projection at first) aligns with intent #12 ("raw form first"). |

## 6 · Manifestation gaps

The intent records that still need to land in their right
guidance file:

### Promotion to `ESSENCE.md` (resolved 17:30Z)

The psyche affirmed both promotion candidates; intent #13 gets
reshaped into impersonal form for essence placement:

- **Intent #4 (as-is):** *"What animates humans at the highest
  level is spirit; persona-spirit is the analog."*
- **Intent #13 (impersonal form, psyche-dictated):** *"The intent
  protocol prevents the loss of the psyche's important
  expression."*

Pending action: edit `ESSENCE.md` to add both.

### `skills/intent-maintenance.md` — richer supersession lifecycle

Currently presents binary supersession. Intent #11 expands to
negation / certainty-lowering / escalation. The 17:30Z resolution
clarifies that the **guardian sub-actor** is a future arc, not
today's daemon — but the lifecycle remains the eventual design.

Pending action: add a `## Forward — richer lifecycle` section to
`skills/intent-maintenance.md` describing the three transitions
and the guardian, noting they wait for the multi-agent auditing
arc.

### `persona-spirit/INTENT.md` — does not exist

The repo has AGENTS / ARCHITECTURE / skills / README / CLAUDE
files but no `INTENT.md`. Per `skills/repo-intent.md`, every repo
in the workspace's intent surface should carry one. Intent
records #3, #4, #6, #7, #8, #11 are spirit-specific and would
synthesise cleanly.

Pending action: create `persona-spirit/INTENT.md`.

### `persona-mind` — spirit-ownership not yet manifested

Intent #6: spirit owns mind. `persona-mind/ARCHITECTURE.md` does
not reflect this; no `INTENT.md` for persona-mind.

Pending action: deferred until spirit-to-mind owner work begins.
Per intent #6, the verb set develops with implementation.

### `INTENT.md` (workspace) — universal persona principles

- Intent #8 — *"no persona component works without LLMs."*
- Intent #12 — *"raw form first; integration follows."*

Pending action: short additions to workspace `INTENT.md`. The
LLM-intrinsic rule could become an AGENTS.md hard override
instead.

## 7 · Psyche resolutions (recorded 17:30Z)

Intent records appended to `intent/persona.nota`:

1. **Q1 — Restatement shape.** *"separate records then. repeated
   similar intents will mean stronger signal"* — Decision.
2. **Q1 rationale — repetition is signal.** *"repeated similar
   intents will mean stronger signal"* — Principle. Spirit's
   data model expresses intent intensity through repetition.
3. **Q2 — type naming.** *"intent record identifier is not good
   because spirit deals with intent. So it's repetition … At
   most it should be record identifier"* — Correction. Every
   `Intent*` type in `signal-persona-spirit` drops the prefix
   unless ambiguity returns.
4. **Q2 — identifier ownership.** *"Like you're talking about a
   unique identifier for recovering in the database. That's not
   an agent thing"* — Clarification. RecordIdentifier is
   spirit-internal; never an Assert input.
5. **Q3 — spirit is dumb storage.** *"the spirit is not a
   thinking thing. So it doesn't make decisions. That's the
   agent's job. … just going to be a dumb system. It just takes
   what it's given"* — Decision. Agent input is authoritative;
   the guardian sub-actor waits for the multi-agent auditing arc.
6. **Q4a — ESSENCE promotion of intent #4.** Yes; promote
   as-is.
7. **Q4b — ESSENCE promotion of intent #13.** Yes; psyche
   dictated the impersonal form for essence.

## 8 · Suggested next moves

For the operator (now unblocked on Q1–Q3):

1. **Contract rename sweep in `signal-persona-spirit`** — every
   `Intent*` type drops the prefix where unambiguous. Affected:
   `IntentRecordIdentifier` → `RecordIdentifier`;
   `IntentTopic` → `Topic`; `IntentSummary` → `Summary`;
   `IntentQuote` → `Quote`; `IntentContext` → `Context`;
   `IntentObservationMode` → `ObservationMode`;
   `IntentRecordObservation` → `RecordObservation`;
   `IntentRecordQuery` → `RecordQuery`;
   `IntentRecordSubscription` → `RecordSubscription`;
   `IntentRecordSummary` → `RecordSummary`;
   `IntentRecordProvenance` → `RecordProvenance`;
   `IntentRecordCaptured` → `RecordCaptured`. Keep
   `IntentKind`, `IntentCertainty`, `IntentTimestamp` only if
   shorter names would collide with general-purpose words.
2. **Flip `Entry` to per-statement record.** Drop
   `verbatim: Vec<Verbatim>`. Each Entry carries one timestamp
   and one quote inline. `Verbatim` as a named struct goes away
   (its fields fold into Entry).
3. **Drop the `Assert PsycheStatement` vs `Assert Entry`
   asymmetry on the reply side** — both produce one
   `RecordAccepted` reply with the spirit-minted record summary.
4. **Daemon socket + Kameo tree** per /232 §9 minus the
   `IntentClassifierActor` (Q3 says spirit doesn't classify).
5. **Sema-engine tables** for the per-statement record shape.
6. **`Assert` handlers + `Match` handlers** for the query
   surface settled in Gap 4.

For the designer:

7. **`ESSENCE.md`** — add the two promoted statements.
8. **`skills/intent-maintenance.md`** — add `## Forward — richer
   lifecycle` section.
9. **Workspace `INTENT.md`** — short additions for intent #8 +
   #12.
10. **`persona-spirit/INTENT.md`** — create.

Operator can pick up #1–#6 in any order; the rename sweep is
independent of the data-model flip.

## 9 · References

- `reports/operator/136-persona-spirit-current-system-and-intent-gaps.md`
  — operator's own audit; the five gaps in §3.
- `reports/designer/232-persona-spirit-new-component.md` — design
  spec.
- `intent/persona.nota` — 26 records as of 17:30Z (19 prior + 7
  new).
- `intent/nota.nota` — 2026-05-19 19:45 "Restatement shape"
  record (the workspace filesystem schema; now extended to spirit).
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` —
  the contract.
- `/git/github.com/LiGoldragon/persona-spirit/src/runtime.rs` —
  the CLI decoder + honest-unimplemented reply.
- `/git/github.com/LiGoldragon/owner-signal-persona-spirit/src/lib.rs`
  — owner contract.
- `skills/intent-log.md`, `skills/intent-maintenance.md`,
  `skills/intent-manifestation.md` — the discipline surfaces a
  resolution-driven sweep edits.
- `bead primary-ojxq` (persona-spirit triad implementation, P1) —
  operator pickup; rename sweep + flip + daemon work all land
  under it (or split into a follow-up bead).
- `bead primary-dzrn` (bare ISO-8601 Timestamp type) — open;
  unblocks `IntentTimestamp` → typed `Timestamp`.
