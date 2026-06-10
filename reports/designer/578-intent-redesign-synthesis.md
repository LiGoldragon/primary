# Intent-tool redesign — the guardian and the two-layer model

Synthesis of a live design conversation (2026-06-10) on what Spirit should
become. Companion to `577` (empirical state of deployed Spirit v0.4.0) and
`579` (the first manual agglomeration pass). Nothing here is built yet; this is
the converged design. Decisions are marked **[decided]** (settled in
conversation) or **[open]** (a call the psyche still owes, or my lean awaiting
confirmation).

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
  replacement *happens* as an action and *announces itself* as a correction
  event to subscribers, then evaporates. The "this replaced that" lives exactly
  as long as the notification.
- **[decided] State = rest, stream = motion.** This is how intent becomes "the
  psyche at rest": query at any instant and you get a coherent, contradiction-free
  body, by construction — because the guardian won't admit anything that breaks
  consistency.
- **[decided] Spirit gets subscriptions** so agents stay current; correction is
  one event type on that stream.

## 4. The guardian — the write gate

- **[decided] The daemon is the gate; an agent is the brain.** On a capture the
  daemon gathers the relevant existing records, hands the bundle to an agent,
  and acts on the verdict. The daemon routes and executes; it never parses NOTA
  (the CLI already typed the record) and never judges.
- **[decided] The guardian's verdict is binary: yes or no.** *Yes* = no conflict,
  admit. *No* = conflict or any smell — with a reason and references to the
  records concerned. It makes **no resolution calls** and has zero discretion;
  it never decides to suppress anything. (This is what makes it safe: it can
  never wrongly overwrite intent.)
- **[decided] On a no, the proposing agent acts** — revise to remove the
  conflict, drop it, or come back with an explicit, named supersede.
- **[decided] Two write paths.** *propose* — subject to the yes/no gate, succeeds
  only if consistent with everything already there. *supersede* — the explicit
  follow-up that names the record(s) it replaces; that act suppresses the old
  arrow and fires the correction event.
- **[decided] Supersede is still consistency-checked.** Superseding X with R
  checks R against everything *except* the named target X. Consistent with the
  rest → admit; still conflicts with an un-named Y → no, name Y too. Supersede
  cannot be a side door for injecting inconsistency; the always-consistent
  invariant holds through it.
- **[open — lean: park] The daemon→agent handoff.** *park*: the daemon shelves
  the proposal as pending, replies "got it, pending," a guardian agent works the
  shelf and tells the daemon admit/drop; the daemon stays a pure store plus an
  inbox, no outbound LLM call. "Blocking gate" is still satisfied — the record
  is not *admitted* until vetted. *block* (alternative): the daemon calls the
  agent live and stalls for the verdict.

## 4a. The agent — a harness library, not a daemon

- **[decided] The agent is a library, not a daemon.** The constraints forced it:
  daemons never parse NOTA and can't sit in the text path, so the daemon part of
  an "agent" has nothing left to do. What remains is a reusable **harness
  library** — the judgment machinery: render the prompt, call the model, parse
  the answer, retry. The guardian, the auditor, and the topic-enlargement gate
  are all the same shape, so the harness is the workspace's general judgment
  primitive — a shared, client-grade library, not a triad component.
- **[decided] The harness is the only NOTA-speaker, and it's a client.** A
  consumer builds a harness *process* from the library plus its own signal types,
  so the harness is the only thing that knows signal-spirit. It renders a NOTA
  prompt — context records as NOTA, plus a prelude showing the expected NOTA
  response shape — **calls the model directly**, takes the NOTA answer, parses it
  into the typed verdict, and hands that back to Spirit. Spirit only ever
  exchanges *signal* with the harness; every daemon stays pure signal.
- **[decided] The harness is a separate process.** It can't be embedded in
  Spirit — Spirit's process would then be speaking NOTA. So Spirit (a daemon)
  talks to the harness (a client process) in signal; the harness owns the whole
  text/NOTA world.
- **[decided] Prelude and parser come from one schema.** What the prelude tells
  the model to emit is exactly what the parser decodes — they can't drift,
  because both fall out of the one verdict type. A malformed response just fails
  the parse and retries.
- **[open] Governance.** Keys, token budget, rate limits, model routing. If
  centralized, it's a **signal-only** daemon that vends grants and keys but never
  touches a prompt — the harness still makes the actual call. Only worth it once
  there is more than one consumer; a single consumer configures locally.
- **[deferred] Signal-forwarding** (opaque sized envelopes routed without being
  decoded) is a real, useful pattern — for a future broker/router daemon, not
  for the agent, which needs none of it.

## 5. Retrieval and completeness

- **[decided] Completeness is the retrieval's job, not the guardian's nose.** The
  bundle = topic-matches + content-matches on the proposed record's own text, so
  a misattributed record still lands in the bundle (found by what it says, not
  its tag).
- **[decided] The guardian also has query access** — the bundle is a seed, not a
  cage. It chases concrete leads: the proposal names something specific; a bundle
  record points elsewhere; the proposal is about a concept the bundle does not
  cover.
- **[decided] Completeness is not guaranteed, and need not be.** Guardian =
  high-recall best-effort at the door; auditor = at-rest backstop catching the
  residue (the paraphrase-dup with no shared topic or word). Two gates, two
  moments.

## 6. Topics — closed and broad

- **[decided] Topics become a closed, curated, broad set.** `schema` yes;
  `schema-language`, `record-deletion` too specific. Small and stable. This turns
  topics from leaky free-text (1315 distinct strings today) into a trustworthy
  index, so "everything on this topic" is reliably complete.
- **[decided] New topics go through an enlargement process** — the same gate as
  the guardian, one level up: a proposed new topic is vetted against the existing
  ones (genuinely new, or `schema` wearing a hat?).
- **[decided] Broad topics are a coarse domain filter, not a precision filter**
  (`schema` returns ~384) — which is *why* a finer discriminator (keywords) is
  needed underneath.
- **Cost:** closing the set means curating the 1315 strings down to a canonical
  broad set first — the same agglomeration move, pointed at topics.

## 7. Keywords and text search — the discriminator

- **[decided] Three tiers of selectivity** over the same record: **topic** (broad
  domain, closed) → **keyword** (author-marked salient terms) → **full text**
  (safety net).
- **[decided] Keywords via markdown-style asterisk emphasis** — `*schema
  language*`. The specificity pulled out of topics relocates here. The LLM marks
  salient terms nearly for free as it writes, and the marks double as
  skimmability.
- **[decided] Full-text search returns whole records** (identifier + topics +
  text) so provenance stays intact — not a grep that loses source and formatting.
- **[decided] Keywords are a precision layer, not a completeness layer** — they
  depend on the author marking correctly, so full text + the auditor remain the
  recall floor. Keywords must never be load-bearing for recall.
- **[lean] Implementation:** derive keywords on the fly from the description (no
  stored field, no drift); case-fold; a multi-word `*span*` is one phrase-unit.
  Keyword/substring first; semantic/embedding only if literal proves too weak.
- **[open — expected clean] Verify asterisks are inert in NOTA** (only brackets
  are special) so emphasis can live literally inside the `[description]` string.
- **[decided] Loop-closure:** a keyword appearing everywhere is the signal to
  enlarge the topic set — keywords feed the enlargement process.

## 8. The kinds

- **[decided] Kinds shrink toward forward-only.** `Correction` leaves the store
  entirely — it is an event type, not a record kind. What remains are arrows:
  Decision, Principle, Constraint.
- **[open] `Clarification`** is probably in the same boat as Correction
  (discussion-shaped — "to clarify the earlier point about X"); its content is
  just an arrow. Decide whether it stays a kind or exits.

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
- **[decided] The keystone is a magnitude-aware query.** `579` proved that
  marking removal-candidates does *nothing* to query output — the daemon's query
  ignores magnitude entirely. Make the query exclude tombstones and prefer high
  weight, and three things unlock at once: weight becomes real, collection
  becomes possible (you can finally select the Zero records to retire), and the
  guardian has something precise to query against. It is upstream of the guardian,
  the auditor, and the de-bloat.
- **[lean] Weight is the core anti-bloat mechanism** — repetition raises a weight
  instead of adding a record. No `weight` field exists today; magnitude is the
  proxy; lean toward adding a dedicated reaffirmation-count since the schema is
  being reworked anyway.

## 11. Still open

- The Spirit↔harness handoff: park (lean) vs block (§4).
- Governance home: a signal-only governance daemon vs local-to-the-harness —
  when shared budget across consumers becomes worth it (§4a).
- `Clarification`: keep as a kind or demote to an event (§8).
- Suppressed-arrow recoverability: archive outside the live intent vs destroy.
  Largely de-risked since supersede is always explicit and named, but archive-vs-
  destroy is unsettled (the deployed `CollectRemovalCandidates` already archives).
- Weight: dedicated field vs reuse `magnitude` (§10).
- Who curates the initial closed topic set (§6).
- Keyword search: keyword/substring first, semantic upgrade later if needed (§7).
