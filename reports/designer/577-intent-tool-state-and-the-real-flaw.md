# Intent tool (Spirit) — empirical state and the real flaw

Frame: the psyche asked to discuss why Spirit feels bloated and capped, and
why *"we need more intent clarity, and the tool we created for it is flawed."*
This report records the empirical state of the deployed Spirit (v0.4.0),
gathered live from the running daemon, corrects two wrong assumptions, and
reframes the problem. The headline: **the fix is already decided intent —
logged roughly twenty times — and unbuilt.** Companion to `574-state-of-everything/`
(the broad fleet audit) and `576-cross-lane-context-maintenance` (the report
sweep). The guardian-gate design that follows from it lands in `578`.

## 1. Deployed mechanics — there is no retrieval cap

Gathered live from `spirit-daemon.service` (v0.4.0) and source at
`/git/github.com/LiGoldragon/spirit`.

- **Store:** `~/.local/state/spirit/spirit.sema`, a single redb-style
  `sema-engine` file, ~1.25 MB, table `records`, schema version 1.
- **`Entry` is exactly five fields** (`src/schema/signal.rs`): `topics`, `kind`,
  `description`, `magnitude`, `privacy`. **No timestamp, no weight, no
  relations** — grep for any of them returns nothing. This directly
  contradicts `skills/spirit-cli.md:78` ("the daemon stamps date/time
  itself"); the deployed schema carries no time field at all.
- **No cap on retrieval.** `Store::observe` loads every record, filters, and
  returns the whole matching `Vec` — no `take`/`limit`/`truncate` anywhere in
  the read path. `Count` is literally `observe(query).len()`. Verified live: a
  query on `schema` returned **all 385** matching records in one 148 KB blob.
- **Matching is exact-topic-string equality**, by-kind, by-privacy — *not*
  full-text and not even substring. `TopicMatch::matches` does
  `entry_topic == topic`. An agent only finds a record if it guesses the exact
  topic word — itself a driver of re-logging.
- **Retrieval is two-step:** `Observe` stashes the full result and returns
  `RecordsStashed (handle count marker)`; `LookupStash handle` returns the
  whole payload.
- **Mutation ops exist** (the store is *not* append-only): `Remove` (hard,
  irreversible — redb reuses freed pages within hours), `ChangeCertainty` (set
  magnitude; a removal-candidate marker), `ChangeRecord` (replace the entry
  under the same identifier), `CollectRemovalCandidates` (archive candidates to
  a meta-configured target, then retract). **No typed `Supersedes`/`Negates`
  relation** — supersession is a manual convention (a `Correction` naming the
  old text), confirmed by `skills/intent-maintenance.md:43`.

So the felt "cap" is real as a *symptom* but wrong as a *mechanism*. Nothing is
hidden; the problem is the opposite — a topic query dumps 150–385 full records
on you with no ranking, recency, or summary. The retrieval isn't truncated; it
is **undistilled**. You cannot fix undistilled by raising a cap.

## 2. The bloat, in numbers

- **1400 records** total (1393 public, 7 private).
- By kind: Decision 498, Principle 383, Clarification 200, Correction 191,
  Constraint 121.
- **1315 distinct topic strings**, averaging 2.85 topics/record.
- Fattest topics: `schema` 384, `nota` 155, **`spirit` itself 150**,
  `workspace` 92, `signal` 83, `component-shape` 58, `sema` 51, `persona` 47,
  `schema-language` 43, `cloud` 39, `reports` 38.
- Description verbosity: median 253 chars, mean 331, max 2012; 275 records over
  500 chars, 87 over 800. **463,933 total description characters.**
- Near-duplicate restatement: at least 8 clusters / 16 records inside the
  self-design pool alone (a conservative jaccard≥0.34 threshold; heavily
  paraphrased restatements fall below it and are more numerous).

## 3. The real flaw — the vicious cycle

Bloat → a topic query returns an unranked 150-record dump → the querying agent
doesn't read to the end, so it doesn't see the intent already there → it logs
again (a near-restatement) → more bloat → worse retrieval. Eager logging is not
only an agent-discipline failure; it is **partly caused by the bloat itself**,
because exact-topic matching plus undistilled dumps mean agents can't find what
already exists. Periodic cleanup sweeps cannot win against capture-time
eagerness; the gate has to move to the door.

## 4. The irony — the fix is already decided intent, unbuilt

The thesis the psyche is reaching for is already logged across ~20+ records,
several of them near-duplicates of one another. Verbatim from the store:

- `[spirit] Constraint` — *"Intent capture should become denser and less
  verbose: durable records should preserve the clarified intent without
  carrying large verbatim blocks that bloat output and become lossy to work
  with."*
- `[workspace] Decision` — *"the spirit intent log requires garbage collection;
  older intent that is now contradicted by newer intent must be retired so the
  log stays a true source of current intent rather than a historical
  accretion."*
- `[spirit,capture,guardian,clutter] Decision` — *"Spirit capture is a blocking
  gate not an advisory check: the guardian must vet and admit a proposed record
  before capture succeeds, so duplicates, contradictions, compounds, and
  non-intent are resolved or refused at the door rather than admitted and
  cleaned up later."*
- `[spirit,…,auditor,automation] Decision` — *"Intent agglomeration and refresh
  is triggered by an automated auditor that auto-proposes refreshes; the psyche
  confirms the retire of source records."*
- `[intent-maintenance,certainty-agglomeration] Principle` — *"Intent should be
  refreshed by agglomeration: combine many lower-certainty records … into a
  single fresh higher-certainty record … shrinks how much agents must read."*
- `[intent,logging,discipline,overcorrection] Correction` — *"Agents must not
  respond to Spirit overcapture by avoiding Spirit entirely; the correct
  discipline is the conservative capture gate."*
- Plus records explicitly calling for `relations` and `weight` fields that the
  deployed schema does not have.

The blocking capture-gate, the auditor, garbage collection, agglomeration,
denser capture, the weight and relations fields — **all decided, none built.**
The proof the tool is broken is that it could not converge its own design: the
cure for "Spirit accumulates redundant records" exists *as ~20 redundant
records*. The two capabilities that would have prevented that duplication —
semantic retrieval and a reconciliation primitive — are exactly what the
duplicated records ask for.

## 5. Resolved architecture

The daemon is constrained to take one rkyv message and never parse NOTA — so
the intelligence cannot live in it. The resolution honours that:

- **Daemon stays dumb** — store, exact-match filter, admit/remove/change. Fast,
  mechanical, no judgment.
- **A guardian at the write door** (agent-grade): vets a proposed record —
  non-intent? compound? duplicate? contradiction? — and refuses or reconciles
  *before* admission. Prevents new bloat. (Designed in `578`.)
- **An auditor at rest** (agent-grade, periodic): agglomerates existing records
  and proposes retirements; the psyche confirms. Distills accumulated bloat.
- **Query points at the distilled surface**, not the raw dump. `INTENT.md`
  already names the three surfaces "increasing in distillation": the Spirit
  store (raw), per-repo `INTENT.md` (synthesised), `ESSENCE.md` ("the gold of
  the gold"). Authority for agents should resolve against the distilled canon,
  with the store as provenance.

Every piece maps onto something the architecture already names. The store
exists; the three surfaces exist; the auditor is "coming, shape decided." What
is missing is the *pump* (auditor) and the *door* (guardian) — both decided,
neither built — plus the schema fields (`weight`, `relations`, a timestamp) the
records ask for.

## 6. The plan — distill, then gate, then automate

A capture-guardian cannot run a sane duplicate-check against a 1400-record
store; its "is this already said?" query would be hitting the very mess. So:

1. **Manual agglomeration pass first** (dispatched 2026-06-10; witness in
   `579`) — fold the worst topics' clear repeats into canonical high-magnitude
   records, mark the redundant sources as removal candidates (reversible only;
   no hard delete; the irreversible collection is the psyche's call). Get the
   store small.
2. **Build the guardian** (`578`) — stop new bloat at the door.
3. **Build the auditor** — automate the rest-time distillation loop.

The manual pass is the auditor's job, run by hand the first time.

## 7. Documentation divergences found

- `skills/spirit-cli.md:78` claims the daemon stamps date/time; the deployed
  schema has no time field. Doc describes something unbuilt.
- The doc's query-syntax examples (`(Any [])`, `(Count ((Any []) …))`) are
  wrong; the deployed shape is `(Count (Any None (Exact Zero)))`. An agent
  copying the doc gets a parse error.

Both flagged to a doc-fix agent (2026-06-10).
