# Intent-tool redesign — the guardian and the two-layer model

Synthesis of a live design conversation (2026-06-10) on what Spirit should
become. Companion to `577` (empirical state of deployed Spirit v0.4.0) and
`579` (the first manual agglomeration pass). Nothing here is built yet; this is
the converged design. As of the end of the 2026-06-10 session **every open call
is resolved** — markers are **[decided]** or **[deferred]** (a future revisit,
not a present choice); §11 lists the residuals.

Naming: the design renames the deployed `topics` concept to **category**. Where
this report describes deployed v0.4.0 it still says `topics` (the literal field);
the forward design says `category`.

Per the discipline we worked out below, none of this was logged to Spirit as
intent — it is design-in-progress, and the ~20 existing self-design records are
already the bloat we are fixing. It lands here, in a report.

## 1. The frame

- **[decided] Authority hierarchy.** Live psyche → intent → everything else
  (reports, code, architecture). Intent outranks agents, reports, and code, but
  is itself subordinate to and correctable by the live psyche — because it is a
  *derived model* of the psyche. Reports are agent opinion, two derivations from
  ground truth, and can be flat wrong.
- **[decided] Intent is the psyche at rest.** Forward, settled, declarative.
  Spirit's flaw is that it is all *motion* — a pure accumulator (1400 records,
  undistilled) with no resting state.
- **Empirical corrections** (from `577`): there is no retrieval cap (queries
  return everything, unranked — 385 records / 148 KB for `schema`); matching is
  exact-topic-string + kind + privacy, never magnitude, never text; the store is
  `sema-engine`; `Entry` is 5 fields (topics, kind, description, magnitude,
  privacy) with no timestamp, weight, or relations. The fix is already decided
  intent, logged ~20× and unbuilt.

## 2. The nature of intent — the arrow principle

- **[decided] Intent is a forward arrow.** Generative, expanding; it states
  *this*, never *not that*. It does not reference what it replaces, disprove
  alternatives, or position itself in a debate.
- **[decided] The boundary is referential negation, not all negation.** A
  forward *law* is still intent (`NOTA emits no quotation marks` is a positive
  boundary the system has). What is excluded is a record defined *against another
  record*, a rejected alternative, or a debate — that is discussion.
- **[decided] Discussion belongs on the wire, not in the state.** Supersession
  and contradiction are discussion ("two agents talking"); they never live in a
  record's prose, and — see §3 — not in stored structure either.

## 3. The two-layer model — state vs stream

- **[decided] The store holds pure forward arrows, always mutually consistent.**
  This is the rest. No lineage, no contradiction, no correction records.
- **[decided] Change is a transient event on a subscription stream.** A
  replacement or clarification *happens* as an action and *announces itself* as
  an event to subscribers, then evaporates. The "this replaced that" lives
  exactly as long as the notification.
- **[decided] State = rest, stream = motion.** This is how intent becomes "the
  psyche at rest": query at any instant and you get a coherent, contradiction-free
  body, by construction — because the guardian won't admit anything that breaks
  consistency.
- **[decided] Spirit gets subscriptions** so agents stay current; correction and
  clarification are event types on that stream.
- **[decided] Events are ephemeral; history is durable** (operator `352` §5).
  Subscription events are throwaway delivery notifications. Operation history,
  retired arrows, and prior clarified wording are durable archive/journal data,
  kept *outside* the live intent query surface — so the live store stays pure
  while nothing is irrecoverably lost.

## 4. The guardian — the write gate

- **[decided] The daemon is the gate; an agent is the brain.** On a capture the
  daemon gathers the relevant existing records, hands the bundle to the harness
  (§4a), and acts on the verdict. The daemon routes and executes; it never parses
  NOTA (the CLI already typed the record) and never judges.
- **[decided] The guardian's verdict is binary: yes or no — with typed reasons.**
  *Yes* = no conflict, admit. *No* = conflict or any smell. The verdict carries a
  **typed reason** (enum), referenced `RecordSnapshot`s, and a short
  human-readable explanation — so a refusal is machine-actionable and testable,
  not free prose (operator `352` §4). Reasons: duplicate, contradiction, compound,
  non-intent, unclear-privacy, unclear-category, clarify-tramples,
  clarify-loses-meaning, supersede-target-missing, retrieval-insufficient. Typed
  reasons grant **no** discretion — authority stays binary; they just make the no
  usable. It makes no resolution calls and never decides to suppress anything.
- **[decided] On a no, the proposing agent acts** — revise to remove the conflict,
  drop it, or come back with an explicit, named supersede.
- **[decided] Three write operations.**
  - *propose* — a new arrow; passes only if consistent with everything already
    there.
  - *clarify* — refine an existing record's wording in place. The guardian judges
    whether it genuinely **clarifies** (same meaning, sharper words) versus
    **tramples** it into something unrelated, or **loses** important aspects —
    either of the latter two is a no. A trample means the agent actually wanted a
    supersede, not a clarify. Because a true clarify is meaning-preserving it
    can't introduce a new conflict, so it needs no global re-check. The record
    identifier stays stable; the prior wording is journaled to the archive
    (recoverable, out of the live surface) and a clarification event fires. The
    derived keywords re-index — expected, since the sharper wording carries the
    better terms (operator `352` §2).
  - *supersede* — explicitly name the record(s) being replaced; the old arrow is
    retired and a correction event fires.
- **[decided] Supersede is still consistency-checked.** Superseding X with R
  checks R against everything *except* the named target X. Consistent with the
  rest → admit; still conflicts with an un-named Y → no, name Y too. Supersede
  cannot be a side door for injecting inconsistency; the always-consistent
  invariant holds through it.
- **[decided] Retired arrows are archived, not destroyed.** A supersede (or an
  auditor retirement) moves the old arrow to a cold archive *outside* the live
  intent — invisible to queries (zero noise), but recoverable if a call was
  wrong. The deployed daemon already does this (`CollectRemovalCandidates`
  archives, then retracts).
- **[decided — block for now] The Spirit↔agent handoff is synchronous.** There is
  currently no way to call the proposing agent back, so it waits in the call for
  the verdict (block). On harness absence, model failure, malformed verdict, or
  timeout, the propose **fails closed** — rejected/errored, never admitted
  unjudged (admitting unjudged would break the consistency invariant). The exact
  transport is the lease-and-direct-channel flow in §4a; its failure modes
  (timeout / malformed verdict / harness absence) are the implementation contract
  to pin down (operator `352` §3). Park becomes possible once agent messaging
  exists; **[deferred]** revisit then.

## 4a. The agent daemon and the harness

LLM calls will live in many components, so the model machinery is centralized in
an **agent daemon** — but it brokers harnesses without ever touching a payload,
which is what keeps consumer signal out of it.

- **[decided] Two pieces.** The **agent daemon** owns the model machinery —
  connections, keys, token budget, rate limits, and a warm pool of harness
  processes. The **harness** is a per-component client process, compiled with that
  component's signal contract, and is the only thing that crosses signal ↔ NOTA.
  The agent daemon is a proper triad: `agent` + `signal-agent` +
  `meta-signal-agent`, configured (harness registry, keys, budget) by the
  meta-signal, virgin-start-and-wait like the others.
- **[decided] The harness is a separate process.** It can't be embedded in the
  component — the component (a daemon) would then be speaking NOTA. So the
  component talks to it in signal; the harness owns the whole text/NOTA world.
- **[decided] The daemon vends; it never ferries.** This is the move that keeps
  consumer signal out of the agent daemon: it hands the requesting component a
  *ready harness*, and the payload then flows component ↔ harness **directly**. The
  agent daemon is on the control path (lease + meter), never the data path.
- **[decided] The call, end to end** (Spirit's guardian as the example):
  1. Spirit → agent daemon: lease a guardian harness (`signal-agent`; no records).
  2. Agent daemon returns a **warm** Spirit-guardian harness from its pool — model
     connection open, full prelude loaded (NOTA basics + its own verdict schema,
     known at compile time), waiting only for the records — with its endpoint.
  3. Spirit → harness, **directly**, in signal-spirit: the records + question.
  4. Harness calls the model, parses the NOTA verdict, → Spirit **directly**: the
     typed verdict.
  5. Harness → agent daemon: done, tokens used; the lease ends.
- **[decided] Harnesses are opaque to the daemon, managed by identity.** The agent
  daemon launches, pools, meters, and restarts a harness binary without reading a
  byte of its contract. The registry — which binary is "Spirit's guardian harness"
  — is meta-signal config; adding a component means registering its harness binary.
- **[decided] Pools are per (component, role).** A harness compiled with one
  contract serves only that one, so the daemon keeps separate warm pools
  (Spirit-guardian, Spirit-auditor, …). A component with several judgment jobs
  registers several harnesses, each with its own verdict schema; the lease request
  just names the (component, role) id — still opaque to the daemon.
- **[decided — lease-per-call] Leasing and the lease contract.** A harness is
  leased for one call and returned to the pool — clean for budget accounting and
  fairness (stickiness is a later optimization, §11). A `HarnessLease` carries:
  lease id, harness endpoint, an unguessable **capability token**, a budget/model
  grant, an expiry, and the (component, role) identity (operator `352` §2–3). The
  warm harness holds no credentials at rest — the **grant is injected per lease**,
  so revocation and budget stay clean — and it rejects any payload whose token
  doesn't match its active lease, which authenticates the direct channel both
  ways.
- **[decided] Dependency graph.** agent daemon → `signal-agent` only (never a
  consumer contract); harness → its component's signal + `signal-agent` (to report
  usage); component → its own signal + `signal-agent`. The harness remains the
  sole signal ↔ NOTA crosser.
- **[decided] Failure splits by path.** The component sees model/harness failures
  *directly* on its channel and fails closed (rejects, never admits unjudged); the
  agent daemon handles process health — evict and restart a dead harness, refill
  the pool. Because it is control-path, an agent-daemon blip leaves in-flight
  harnesses working; only new leases wait — which is also why global rate-limiting
  belongs there.
- **[decided] Lease accounting is durable** (operator `352` §4). The daemon
  journals each lease's lifecycle — issued, started, completed, ended/expired. If
  a harness dies or never reports usage, the lease is marked expired/unknown and
  budget is charged conservatively, never silently lost.
- **[decided] Prelude and parser come from one schema.** What the prelude tells the
  model to emit is exactly what the parser decodes — they can't drift, both fall
  out of the one verdict type. A malformed response fails the parse and retries.
- **[deferred] Signal-forwarding** (opaque sized envelopes routed without being
  decoded) stays unneeded — the daemon vends, it doesn't ferry. Keep it for a
  future broker/router.

## 5. Retrieval and completeness

- **[decided] Completeness is the retrieval's job, not the guardian's nose.** The
  bundle = category-matches + content-matches on the proposed record's own text,
  so a misattributed record still lands in the bundle (found by what it says, not
  its tag).
- **[decided] The guardian also has query access** — the bundle is a seed, not a
  cage. It chases concrete leads: the proposal names something specific; a bundle
  record points elsewhere; the proposal is about a concept the bundle does not
  cover.
- **[decided] Completeness is not guaranteed, and need not be.** Guardian =
  high-recall best-effort at the door; auditor = at-rest backstop catching the
  residue (the paraphrase-dup with no shared category or word). Two gates, two
  moments.

## 6. Categories — closed and broad

- **[decided] Categories become a closed, curated, broad set** (renamed from
  `topic`). `schema` yes; `schema-language`, `record-deletion` too specific.
  Small and stable. This turns the index from leaky free-text (1315 distinct
  topic strings today) into a trustworthy one, so "everything in this category"
  is reliably complete.
- **[decided] New categories go through an enlargement gate** — the same gate as
  the guardian, one level up: a proposed new category is vetted against the
  existing ones (genuinely new, or `schema` wearing a hat?).
- **[decided] Broad categories are a coarse domain filter, not a precision
  filter** (`schema` returns ~384) — which is *why* a finer discriminator
  (keywords, §7) is needed underneath.
- **[decided] Curation: an agent proposes, the psyche decides.** Closing the set
  means first collapsing today's 1315 free-text topic strings into ~20 broad
  categories — the same agglomeration move, pointed at the index. An agent
  proposes the clustering from the data; the psyche edits and blesses the final
  set (it encodes the psyche's sense of the domains). One-time bootstrap;
  afterwards the enlargement gate handles new categories.

## 7. Keywords and text search — the discriminator

- **[decided] Three tiers of selectivity** over the same record: **category**
  (broad domain, closed) → **keyword** (author-marked salient terms) → **full
  text** (safety net).
- **[decided] Keywords via markdown-style asterisk emphasis** — `*schema
  language*`. The specificity pulled out of categories relocates here. The LLM
  marks salient terms nearly for free as it writes, and the marks double as
  skimmability.
- **[decided] Full-text search returns whole records** (identifier + categories +
  text) so provenance stays intact — not a grep that loses source and formatting.
- **[decided] Keywords are a precision layer, not a completeness layer** — they
  depend on the author marking correctly, so full text + the auditor remain the
  recall floor. Keywords must never be load-bearing for recall.
- **[decided] Implementation:** derive keywords on the fly from the description
  (no stored field, no drift); case-fold; a multi-word `*span*` is one
  phrase-unit. Keyword/substring first; **[deferred]** semantic/embedding only if
  literal proves too weak.
- **[deferred — expected clean] Verify asterisks are inert in NOTA** (only
  brackets are special) so emphasis can live literally inside the `[description]`
  string.
- **[decided] Loop-closure:** a keyword appearing everywhere is the signal to
  enlarge the category set — keywords feed the enlargement gate.

## 8. Kinds, operations, events

- **[decided] Kinds are forward arrows only:** Decision, Principle, Constraint.
  The two that used to be kinds move to where they belong — neither is a kind.
- **[decided] `Correction` is an *event*** — fired when a supersede retires an
  arrow; a notification on the stream, never a stored record.
- **[decided] `Clarification` is an *operation*** — the in-place refinement of a
  record's wording (the `clarify` op, §4). The guardian polices it: genuinely
  clarifies (admit) vs tramples into something unrelated, or loses important
  aspects (reject). So clarifying can't silently change or erode an arrow. It,
  too, fires an event so subscribers update their cached wording.
- The overall shape: **kinds** = what a record is (three forward arrows);
  **operations** = how the store changes (propose, clarify, supersede, retire);
  **events** = what subscribers hear (added, clarified, superseded/retired).
- **[decided] Migrating the existing kinds:** the deployed store's ~191
  Corrections and ~200 Clarifications get their *forward content extracted* and
  reclassified as Decision/Principle/Constraint; the discussion scaffolding
  ("not that, this" / "to clarify X") is dropped — the agglomeration rewrite rule
  (§9) run as a one-time migration over exported records (operator `352` §8).
- **[deferred] Lurking question:** whether *kinds* are needed at all, or whether
  Decision/Principle/Constraint are themselves one forward-arrow type. Bigger cut,
  separate day.

## 9. The auditor — the rest-time distiller

- **[decided] The auditor is the at-rest backstop.** It periodically agglomerates
  and proposes retirements; the psyche confirms. It is the pump between motion
  and rest, and it catches what the guardian missed.
- **[decided] Agglomeration rewrite rule:** when folding a cluster, emit the pure
  forward statement and drop the dialogue scaffolding (half of why the 191
  Corrections read as bloat is that they are shaped "actually, not that, this").

## 10. Build sequence

- **[decided] Distill → gate → automate.** (1) manual agglomeration pass first
  (done — `579`: 21 canonicals at Maximum, 43 sources marked removal-candidate,
  reversible); (2) build the guardian; (3) build the auditor.
- **[decided — already in source] Magnitude/certainty-aware query.** This was the
  keystone against deployed v0.4.0 (`577`/`579`: marking removal-candidates did
  nothing because the query ignored magnitude). Per operator `352`, **current
  Spirit source already has it** — `Query` carries `CertaintySelection`, ordinary
  observation hides zero-certainty records, and `CollectRemovalCandidates`
  collects on exact-zero. So the de-bloat path exists in source; it just isn't in
  the deployed binary yet.
- **[decided — real first build] Identifier-bearing observation.** Per operator
  `352` §1, the actual first gap: `Observe` returns `Entry` values *without*
  `RecordIdentifier` (only `Lookup` names a record). Guardian refusals, supersede,
  auditor retirement, and category migration all need query results that name the
  records they refer to. Introduce `RecordSnapshot { RecordIdentifier, Entry }`
  and make agent-facing queries return snapshots — before any guardian/auditor
  work.
- **[decided] Three axes, named exactly** (operator `352` §1 — the strongest
  schema warning). The deployed `Entry.magnitude` is overloaded; the breaking
  schema pass splits it:
  - **Certainty** — currentness/confidence; the axis queries already filter on
    (Certainty Zero = retired/removal-candidate). This is `magnitude`, renamed.
  - **Weight** — reaffirmation count / repetition-derived ranking force; a new,
    dedicated field, kept separate from Certainty (a rarely-stated arrow can be
    vital, an oft-repeated one minor).
  - **Importance** — intrinsic priority; **not added** unless the psyche
    explicitly wants it as a real domain field.
- **[decided] Weight mechanics** (operator `352` §6):
  - **Weight rises on duplicate-refusal, not guardian discretion.** A propose that
    duplicates an existing arrow X is refused (typed reason: duplicate, naming X)
    *and* bumps X's weight by one — repetition raises the canonical arrow's weight
    as a mechanical consequence of duplicate detection; the guardian stays pure
    yes/no and never "decides" to reweight.
  - **Monotonic under capture; adjustable by the auditor;** no automatic decay.
  - **Never via generic `ChangeRecord`** — a typed weight-update operation only.
  - **Ranking:** within a category, Certainty + Weight order the results;
    keyword/full-text refine. The exact formula is a tuning detail.

## 11. Resolved, and the residual

All six open calls from the session are settled:

- Handoff → **block** for now (no callback mechanism; §4).
- The agent → a **broker daemon + per-component harness**, vend-not-ferry, with
  governance/pool centralized in the daemon and leasing **per-call** (§4a).
- `Clarification` → a **clarify operation**, not a kind (§4, §8).
- Suppressed-arrow recoverability → **archive** (§4).
- Schema axes → **Certainty** (renamed `magnitude`) + dedicated **Weight**; no
  Importance axis unless explicitly wanted (§10).
- The index → renamed **category**; initial set **curated by an agent, blessed by
  the psyche** (§6).

Residual future-revisits (deferred, not present choices):

- Park handoff once agent messaging exists (§4).
- Harness leasing stickiness (keep-warm reuse) if the per-call handshake shows up
  as latency (§4a).
- Semantic/embedding keyword search if literal matching proves too weak (§7).
- Confirm asterisks are inert in NOTA (§7).
- Whether kinds are needed at all (§8).
