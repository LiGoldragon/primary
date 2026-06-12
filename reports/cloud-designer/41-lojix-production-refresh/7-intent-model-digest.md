# 7 — Intent-model digest

How the INTENT layer works now, distilled for the orchestrator's own
reading. Every claim cites a file read or a command run.

## The Spirit gate — four outcomes

Per `~/primary/AGENTS.md:212-219` ("Run the Spirit gate on every psyche
prompt"), every psyche prompt is classified into **exactly one** outcome
before any reports, code, or chat. The same four are restated in
`skills/intent-log.md:43-54`:

1. **No capture** — pure question, tangent, task-only order, current-state
   reaction, or brainstorming without a settled want.
   (`AGENTS.md:213`; `intent-log.md:45-46`)
2. **Observe / refresh** — context is needed; "refresh intent" means
   *query/read recent Spirit records*, NOT write a record or edit
   `INTENT.md` / `ARCHITECTURE.md`. (`AGENTS.md:213-215`;
   `intent-log.md:47-49`)
3. **Ask** — durable meaning, kind, or privacy is unclear; ask the psyche,
   don't infer. (`AGENTS.md:215-216`; `intent-log.md:50`)
4. **Record** — an explicit durable Decision / Principle / Correction /
   Clarification / Constraint passes the gate. (`AGENTS.md:216-217`;
   `intent-log.md:51`)

Discriminator (`AGENTS.md:217-219`): "A working order is not intent: if
the statement dies when the task is erased, it's task state, not Spirit."
No-capture is the normal case; over-extension corrupts the load-bearing
intent layer (`intent-log.md:53-54`).

The five recordable kinds (`intent-log.md:64-72`): **Decision**
("we're going with X, not Y"), **Principle** ("X over Y as a general
rule"), **Correction** ("you were wrong about X; the right thing is Y"),
**Clarification** ("when I said X, I meant Y"), **Constraint**
("never do Z").

## The deployed binary

- `which spirit` → `/home/li/.nix-profile/bin/spirit`
- `readlink -f $(command -v spirit)` →
  `/nix/store/zi3kq5gszysg8fya6klcaqzvsa27ig1b-spirit/bin/spirit`
- `spirit Version` → `(VersionReported (0.9.5 (1225 17069869348949426690)))`
  — version **0.9.5**, build marker `1225`.

`Version` is a bare NOTA atom (`skills/spirit-cli.md:227-231`). Source:
`/git/github.com/LiGoldragon/spirit`, schema at `schema/signal.schema`.
The binary takes exactly ONE argument (`spirit-cli.md:18-36`): inline
NOTA wrapped in shell double quotes (argument starts with `(`), or a
path to a `.nota` file (argument does not start with `(`).

## Record grammar — exact, with a real example

`Record` carries a two-field `RecordRequest { Entry Justification }`
(live source `schema/signal.schema:133`). `Entry` has **seven positional
fields** (live source `schema/signal.schema:200`):
`Domains Kind Description Certainty Importance Privacy Referents`.
`Justification { StatementText context(Optional StatementText) }`
(line 132). NOTA positional records never omit a field
(`spirit-cli.md:82-85`).

```sh
spirit "(Record (([<Domain> ...] <Kind> [description] <Certainty> <Importance> <Privacy> [<referent> ...]) ([psyche statement] None)))"
```

- `Kind ∈ { Decision Principle Correction Clarification Constraint }`
  (`spirit-cli.md:92`)
- `Certainty ∈ { Zero Minimum VeryLow Low Medium High VeryHigh Maximum }`
  — the `Magnitude` ladder (`spirit-cli.md:93`; `intent-log.md:147`).
  `Medium` is the default; `Maximum` is for founding rules only
  (`intent-log.md:230-256`).
- `Importance` uses the same `Magnitude` ladder; it is **separate** from
  certainty — repeated attention raises importance, not certainty
  (`intent-log.md:199-214`). Skills disagree on the importance default
  (`spirit-cli.md:94-95` says `Minimum`; `intent-log.md:148` shows the
  ladder without a stated default — choose honestly from accumulated
  attention).
- `Privacy` uses the same ladder; `Zero` is open/public. Never put
  private personal substance in a `Zero` record (`spirit-cli.md:107-108`;
  `intent-log.md:57-61`).
- `Referents` is usually empty `[]` (`spirit-cli.md:104-105`).

Real example (`spirit-cli.md:29`):

```sh
spirit "(Record (([(Information Documentation)] Decision summary Medium Minimum Zero []) ([psyche statement] None)))"
```

Reply is terse and does not echo content: `(RecordAccepted abcd)` —
random lowercase base36 id, shortest collision-free, four-char minimum
(`spirit-cli.md:110-113`).

`(State [free-form text])` is the alternate write: the daemon classifies
raw psyche text and persists it through the same `Record` path
(`spirit-cli.md:217-225`).

## Observe grammar — exact, with a real example

`Observe`, `Count`, and `SubscribeIntent` carry the **eight-field
`Query`** directly (`spirit-cli.md:153-201`; live source
`schema/signal.schema:221`):

```text
(Observe (<DomainMatch> <KeywordMatch> <TextMatch> <ReferentSelection> <Kind?> <PrivacySelection> <CertaintySelection> <ImportanceSelection>))
```

- DomainMatch: `Any` | `(Partial [...])` | `(Full [...])`
- KeywordMatch: `Any` | `(AnyKeyword [...])` | `(AllKeywords [...])`
- TextMatch: `Any` | `(ContainsText [...])`
- ReferentSelection: `Any` | `(AnyReferent [...])` | `(AllReferents [...])`
- Kind?: `None` | `(Some Decision)`
- PrivacySelection: `Any` | `(Exact Zero)` | `(AtMost Low)` | `(AtLeast High)`
- CertaintySelection: `Any` | `(ExactCertainty Zero)` | `(AtMostCertainty Low)` | `(AtLeastCertainty Minimum)`
- ImportanceSelection: `Any` | `(ExactImportance Medium)` | `(AtMostImportance Low)` | `(AtLeastImportance High)`

Real example (`spirit-cli.md:193`):

```sh
spirit "(Observe ((Full [(Information Documentation)]) Any Any Any (Some Constraint) (Exact Zero) (AtLeastCertainty Minimum) Any))"
```

**Stash flow** (`spirit-cli.md:177-181`): `Observe` stashes non-empty
result sets and returns a `RecordsStashed` handle; retrieve the full
`RecordsObserved` payload with `(LookupStash 12)`. `(Lookup abcd)`
retrieves by identifier and bypasses observation filters (so it can read
a zero-certainty record by id). Ergonomic privacy shortcuts:
`(PublicRecords (<DomainMatch> <Kind?>))` and
`(PrivateRecords (<DomainMatch> <Kind?>))` (`spirit-cli.md:183-205`).

## NOTA bare-atom rules

From `~/primary/AGENTS.md:141-160` ("NOTA strings are bare atoms unless
they need delimiters; never emit quotation marks"):

- Use bare atoms at `String` positions whenever the string contains no
  whitespace, structural delimiter, `;;` comment marker, or pipe-close
  sequence. Broad punctuation stays bare: `@ * & ^ % < > : /` and a
  single `;`.
- Use `[text with spaces]` inline, or `[|text with [brackets]|]`
  bracket-safe / multi-line, only when a string needs delimiters.
- Bare-eligible strings stay bare: `schema` not `[schema]`. Redundant
  brackets around a bare-eligible string are **rejected** by the daemon
  (`spirit-cli.md:64-71`).
- The encoder structurally cannot emit `"`; quotation marks don't form
  strings in NOTA. So inline NOTA shell calls wrap the whole object in
  shell **double** quotes — `spirit "(Record (...))"` — which preserves
  apostrophes inside bracket strings; single-quoting is wrong
  (`AGENTS.md:154-160`; `spirit-cli.md:22-27`).
- `Option` is `Some`-wrapping: bare `None` or `(Some <value>)`
  (`spirit-cli.md:66-67`).
- NOTA records are **positional, not labeled** — type/head first, then
  fields in declared order; no `(key value)` keyword pairs
  (`AGENTS.md` Hard Overrides, "NOTA records are positional").

## Repo-intent manifestation rule

Capture is only the first half. Per `intent-log.md:95-106` and
`skills/repo-intent.md:70-98`: when an intent record affects a specific
repo's design, implementation, or test direction — whether scoped to that
repo OR a workspace-level rule that reaches it — that intent is
manifested into the affected repo's `INTENT.md` **as part of the work
cycle, not a deferred later pass**. Per-repo `INTENT.md` is the canonical
agent-context surface; if intent lives only in Spirit and chat, an agent
opening the repo reads stale framing and codes to the wrong shape
(`repo-intent.md:96-98`).

`INTENT.md` says WHY (psyche's stated goals/constraints/principles, 100%
backed by psyche statements, no inference); `ARCHITECTURE.md` says WHAT
the system IS (`repo-intent.md:5-7`). Verbatim psyche quotes go in
markdown italics; multi-paragraph verbatim uses an italicised blockquote
(`repo-intent.md:22`; `intent-manifestation.md:73-102`). Every repo
carries an `INTENT.md`; its absence is the first gap to fill — except a
purely-mechanical repo with no psyche input on direction
(`repo-intent.md:100-102`). On entering a repo: read its current
`INTENT.md`/`ARCHITECTURE.md`, query recent Spirit records, cross-check,
and close any manifestation gap on the same feature branch as the work
(`repo-intent.md:88-95`).

Manifestation destinations decision tree (`intent-manifestation.md:32-51`):
`ESSENCE.md` (universal founding rules) → `AGENTS.md` (per-keystroke
overrides) → `INTENT.md` (onboarding context) → `skills/<topic>.md`
(topic discipline) → `<repo>/INTENT.md` (project direction) →
`<repo>/ARCHITECTURE.md` (architectural decision). One record can land
in multiple destinations.

## Live-source cross-check

`rg` over `/git/github.com/LiGoldragon/spirit` confirms the skill docs
match the deployed contract exactly:
- `schema/signal.schema:200` — `Entry { Domains Kind Description Certainty Importance Privacy Referents }` (seven fields, as documented).
- `schema/signal.schema:133` — `RecordRequest { Entry Justification }`.
- `schema/signal.schema:132` — `Justification { StatementText context(Optional StatementText) }`.
- `schema/signal.schema:221` — `Query { DomainMatch KeywordMatch TextMatch ReferentSelection Kind PrivacySelection CertaintySelection ImportanceSelection }` (eight fields).
- `schema/signal.schema:45` — `Input` head list includes `State Record … Observe PublicRecords PrivateRecords Lookup Count … LookupStash CollectRemovalCandidates Tap Untap SubscribeIntent Version`.
