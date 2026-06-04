# Spirit privacy: mechanism discovery + record migration — 2026-06-04

## Frame

Per psyche 2026-06-04: test the deployed Spirit privacy setting, and —
as the personal-affairs pair's advisory lane — migrate any
mildly-private intent the counselor recorded earlier from public to
elevated privacy ("remove the old one, add a new one"). Infrastructure
intent stays public; personal intent gets a low privacy filter.

This report is the **counselor-lane mechanism + migration** writeup. It
converges with the assistant lane's parallel test
(`reports/assistant/4-spirit-privacy-setting-test-2026-06-04.md`, which
proved the basic public-hides / private-reveals behavior and the
type-rejection of a smuggled privacy selector) and adds: the
source-level wire grammar, the actual migration of the four real
private records (which the assistant deliberately left to counselor),
and the substrate-recommendation update. The private substance
(old→new identifier map + topics) lives in the private note
`private-repos/counselor-reports/reports/2-pre-rule-record-migration-2026-06-04.md`,
not here.

## Deployed version

`spirit` → `spirit-v0.4.1`. Source contract `signal-persona-spirit`
@ `a69769b`. **`skills/spirit-cli.md` front matter still says Spirit
0.3.0 — stale.** Privacy, verbal recency depths, recorded-time
queries, certainty change, and record removal all landed since 0.3.0.
(Open question 2 below: who updates the skill.)

## Privacy model — an axis, not a vault

| Property | Finding |
|---|---|
| Type | `pub type Privacy = Magnitude` — privacy reuses the universal 8-level Magnitude scale (Zero … Maximum), same widening pattern as Certainty |
| Meaning | privacy `Zero` = public; higher Magnitude = more private |
| Storage | `Entry` gained a trailing `privacy` field; **optional on decode** — absent → defaults `Zero` |
| Backward compat | old four-field `(Record (...))` calls still decode and land at privacy `Zero` (public) — no migration forced |
| Record-with-privacy | `(Record ([topics] Kind [description] <Certainty> <Privacy>))` — privacy is the 5th positional field on Entry |

The privacy boundary is **access-control at the query layer, not
confidentiality at rest.** All records — public and private — live in
the same Spirit redb storage plane. There is no separate database and
no encryption. Anyone with OS-level read access to the redb file reads
everything regardless of the privacy field. What privacy buys is:
default queries cannot accidentally surface private records, and the
public query path is *type-forbidden* from carrying a privacy selector.

## Query grammar — with vs without private results

The psyche's explicit question — how to query with vs without private
results — resolves to two distinct query families:

**Without private results (the default; what every ordinary agent sees):**

```sh
spirit "(Observe (Records ((Any []) None Any Any SummaryOnly)))"
spirit "(Observe (RecordIdentifiers ((Range (2573 2576)) SummaryOnly)))"
```

These use `PrivacySelection::default_observation_privacy() = Exact(Zero)`
internally. They return **only** privacy-Zero records. Private records
are invisible. Proven: an ordinary `RecordIdentifiers` query of the
migrated ids 2573-2576 returns `(RecordsObserved [])`.

**With private results (explicit opt-in via dedicated variants):**

```sh
spirit "(Observe (PrivateRecords ((AtLeast Minimum) ((Any []) None Any Any SummaryOnly))))"
spirit "(Observe (PrivateRecordIdentifiers ((Exact Low) ((Range (2573 2576)) WithProvenance))))"
```

`PrivateRecords` / `PrivateRecordIdentifiers` each take a
`PrivacySelection` **plus** the ordinary query body. The
`PrivacySelection` enum:

| Selector | Matches |
|---|---|
| `Any` | every privacy level (public + private) |
| `(Exact M)` | privacy exactly `M` |
| `(AtMost M)` | privacy ≤ `M` (e.g. `AtMost Low` = Zero…Low) |
| `(AtLeast M)` | privacy ≥ `M` (e.g. `AtLeast Minimum` = all actually-private) |

**Type-enforced boundary** (assistant report 4): trying to pass a
privacy selector into the *public* `Records` query is rejected —
`validation rejected PublicRecordQuery: public record queries cannot
carry elevated privacy`. So privacy isn't merely a default; the public
path structurally cannot reach private records.

## Two incidental findings

1. **Identifier reuse after removal.** Removing a record frees its
   numeric identifier for reuse. The assistant's synthetic test record
   was `2572`; after it was removed, this session's privacy-classification
   Principle capture was assigned the freed `2572`. Consequence: a Spirit
   identifier is **not** a stable handle across removals — an id can name
   a different record after an intervening removal. (Ties to the
   persona-spirit "intent removal irreversible under page reuse"
   architecture note.)
2. **No `ChangePrivacy` operation.** A grep of the deployed
   `signal-persona-spirit` finds no in-place privacy-change verb (unlike
   `ChangeCertainty`). Elevating an existing record's privacy is done by
   **remove + re-record** — exactly the flow the psyche specified. The
   cost: re-recording re-stamps the daemon date/time (the migrated
   records now read 2026-06-04, not their original 06-02) and assigns
   new ids. A future `ChangePrivacy` (mirroring `ChangeCertainty`) would
   let privacy elevation preserve id + original timestamp — a possible
   feature request to operator/designer (open question 3).

## Migration performed

The four pre-rule personal-affairs records flagged as **G8** in
`reports/counselor/3-privacy-audit-2026-06-02.md` (recorded by this
lane on 06-02, before the privacy rule had absorbed) were migrated from
privacy `Zero` (public) to privacy `Low`, via add-before-remove so the
intent was never absent from Spirit:

| Step | Result |
|---|---|
| Re-recorded 4 records at privacy `Low` (topics/Kind/Certainty preserved) | new ids 2573-2576 |
| Verified new ids hidden from ordinary queries | `(RecordsObserved [])` ✓ |
| Verified new ids visible via `PrivateRecordIdentifiers (Exact Low)` | 4 records, privacy `Low` ✓ |
| Removed the 4 old privacy-`Zero` originals | `(RecordRemoved)` ×4 ✓ |
| Verified originals gone from both ordinary and private query paths | confirmed ✓ |
| Verified full private-record set | exactly 2573-2576 ✓ |

The old→new identifier map and the topics are in the private note (they
hint at the psyche's private domains, so they stay out of this public
report per `skills/privacy.md` §"Public surface leak test"). The public
infrastructure records in the same id neighborhood (1431-1434 — the
privacy-policy decisions) were **not** touched; they are correctly
public.

This resolves audit report 3's G8 by **elevation rather than deletion**
— the intent survives, now access-gated.

## Substrate recommendation update

`reports/counselor/2-spirit-privacy-substrate-2026-06-02.md` recommended
G (private reports) → A (separate private-spirit daemon) → F
(encryption-at-rest). The deployed v0.4.1 privacy axis updates this:

- The brainstorm's **option C** (a privacy axis on `Entry`) is now
  **implemented and deployed** — and the query-layer type-enforcement
  answers my report-2 critique that B/C "leave private substance in the
  same DB." For the *accidental-default-leak* threat, query-layer
  enforcement is a real boundary. It does **not** answer the
  *DB-file-read* threat — that still needs encryption-at-rest (option F).
- Revised guidance: **privacy-Zero Spirit** for infrastructure intent;
  **privacy-elevated Spirit** for mildly-private intent when the psyche
  authorizes Spirit capture (as here); **private repositories** for
  substance the psyche wants out of Spirit entirely or at higher
  sensitivity; **encryption-at-rest** (option F) remains the end-state
  for true confidentiality.
- The **separate private-spirit daemon** (option A) is now *less urgent*
  — the single daemon's query-layer privacy covers the accidental-leak
  threat that motivated it. A's remaining value is full storage
  separation, which F (encryption) addresses more directly.

## Recommended counselor / assistant privacy default

Aligned with assistant report 4 §"Recommended assistant default", and
captured as Spirit Principle 2572:

- **privacy `Zero` (public):** infrastructure, agent-training,
  component design, rules meant to help all agents.
- **privacy `Low`:** anything even mildly personal — the psyche's
  logistics, business, family, friends, finances, location, plans.
- **higher Magnitude:** when the psyche frames the content as sensitive.

Applied by counselor and assistant by default, with agent judgment.

## Open questions for the psyche

1. **Income privacy level.** Record 2576 (consulting-revenue estimate)
   is at privacy `Low` per your "low filter" instruction. Income is
   arguably the most sensitive of the four — elevate it to `Medium` or
   `High`? One remove+readd if so.
2. **Stale skill doc.** `skills/spirit-cli.md` says Spirit 0.3.0; deployed
   is 0.4.1 (privacy, recency depths, recorded-time, certainty-change,
   removal all newer). `skills/skills.nota`'s privacy entry already
   mentions elevated Spirit privacy, so someone is tracking it — should
   counselor file a bead for designer to refresh `spirit-cli.md`, or is
   operator already on it?
3. **`ChangePrivacy` feature.** Want an in-place privacy-change operation
   (mirroring `ChangeCertainty`) so future elevations preserve the
   original id + timestamp instead of remove+readd? If yes, I'll frame it
   for operator/designer.

## See also

- `reports/assistant/4-spirit-privacy-setting-test-2026-06-04.md` — the
  assistant lane's mechanism test (public-hides/private-reveals,
  `PrivateRecordIdentifiers`, the type-rejection of a smuggled selector,
  recommended-default table). This report converges with it.
- `reports/counselor/2-spirit-privacy-substrate-2026-06-02.md` — the
  substrate brainstorm this report updates.
- `reports/counselor/3-privacy-audit-2026-06-02.md` — G8 (the four
  pre-rule records) resolved here.
- `private-repos/counselor-reports/reports/2-pre-rule-record-migration-2026-06-04.md`
  — the private old→new identifier map + topics.
- `/git/github.com/LiGoldragon/signal-persona-spirit/src/lib.rs` — the
  wire contract: `Entry` (≈l.378), `PrivacySelection` (≈l.574),
  `RecordQuery` decode (≈l.663), `Observation` enum (≈l.1096).
