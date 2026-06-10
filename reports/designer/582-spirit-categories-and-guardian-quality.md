# Spirit — a category catalog to bless, and how good the agent-guardian is

Two psyche questions, answered together because they turn out to be the same
question from two ends: **(A)** a concrete category catalog to replace the 12
abstract gerunds, and **(B)** a quality grade on the agent-guardian. They connect:
the category catalog *is* the guardian's retrieval foundation, and the guardian's
deepest weakness is the record bundle it gets shown. Fix the catalog and wire
retrieval to it, and the guardian's judgment improves structurally — not by a
better prompt.

Grounded in live read-only counts (deployed v0.8.0, 2026-06-10, 1418 records), the
578 design, the 581 audit, operator's 355 review, and a verbatim read of
`src/guardian.rs` + the `agent` / `signal-agent` components. Method: a 6-agent
fan-out (two catalog derivations that merge-and-stress-test, three guardian graders).

## Part A — the category catalog to bless

**Replace the 12 gerunds** (`Being Knowing Meaning … Expressing` — 6 of which hold
zero records, `Meaning` holds 65%) **with 15 grounded work-domain categories.** The
design spine from 578 §6/§7 stays: a *closed*, *coarse*, *multi-membership* (`Vec`)
filter, enlargement-gated, with the *keyword layer* (asterisk spans, already built
at `store.rs:902-926`) carrying precision within a category.

| Category | ~records | Covers (head topics) |
|---|---:|---|
| `schema` | ~441 | schema-language, namespace, macro, enum, struct, newtype, roots, variants, form |
| `spirit-intent` | ~214 | spirit, intent, certainty, importance, supersession, the guardian/auditor, capture-discipline |
| `workspace-process` | ~206 | orchestrate, workflow, roles/lanes, reports, beads, chat-vs-report, dispatch policy, AGENTS.md |
| `signal-wire` | ~177 | signal, nexus, sema, codec, rkyv frame, router, mail (mechanism), meta-signal, envelope |
| `nota` | ~162 | nota-next, delimiters, brackets/braces/pipes, symbol, string, vector, bare-atom rules, parser |
| `infra-deploy` | ~152 | cloud, criomos, nix, deploy, prometheus, zeus, cluster, secrets, two-stack |
| `component-shape` | ~140 | component-triad, daemon, runtime, contract-daemon-split, one-arg startup, CLI-as-first-client |
| `persona-llm` | ~86 | persona-pi, local-llm, harness, browser-use, model, the agent-daemon Call→Completion plumbing |
| `testing` | ~59 | tests, fixtures, verification, vm-testing, trace/tracing, process-boundary tests |
| `rust-code` | ~54 | rust-emission, methods/traits, free-function ban, lowering, crate-layout, schema-emits-into-impl |
| `repo-vcs` | ~44 | repository, version-control, branches, worktree, jj, integration, commit-whole-working-copy |
| `naming-language` | ~33 | naming, readability, vocabulary, full-English-word rule, no-ancestry-in-names |
| `agent-behavior` | ~28 | autonomy, transient-error retry, subagent dispatch, effort, focus, keep-working |
| `personal-affairs` | ~24 | assistant, counselor lanes' *public* rules (private substance stays out of records) |
| `forge-build` | ~12 | forge, build-system, CI, artifact production — **probationary** (fold into `infra-deploy` if it stays < ~15) |

**Balance:** largest bucket `schema` at **31%** (vs the gerunds' 65%), and *every*
category holds real mass — no dead buckets. `schema` is the irreducibly densest real
domain; splitting it would just re-fragment the ~20 `schema-*` shards 580 found, so
~30% is the honest floor (578 §3 accepted this). Multi-membership dilutes it further
in practice: ~1832 tags over ~1418 records, so a `schema` record co-tags
`nota`/`rust-code`/`signal-wire`.

**Stress test** — filing the 15 hardest real records (the ones that were ambiguous
under the gerunds): **12 clean, 3 keyword-resolved → 20% ambiguity, down from 81%.**
The 3 borderline cases ("schema-generated Rust emits into `src/schema`" →
`rust-code`; "daemon takes one rkyv startup" → `component-shape`; "no backward
compatibility pre-production" → `workspace-process`) are exactly the designed
multi-membership zone where the keyword layer carries precision — not catalog
defects.

**The confusable-pair boundary rules** (the part worth getting right, because they're
where mis-filing happens):

- `schema` vs `nota` — *type/legality/enum-form* → `schema`; *delimiter/atom/quote
  mechanics* → `nota`. (This fusion is what made `Meaning` hold 924.)
- `schema` vs `rust-code` — *the NOTA shape that drives emission* → `schema`; *where
  emitted Rust lands / method-only / crate-layout* → `rust-code`.
- `signal-wire` vs `component-shape` — *what crosses the socket* → `signal-wire`;
  *process shape / who may parse / startup contract* → `component-shape`. (`rkyv`
  frame = `signal-wire`; one-rkyv-*startup* = `component-shape`.)
- `spirit-intent` vs `workspace-process` — *a Spirit daemon property / record axis /
  guardian internals* → `spirit-intent`; *a rule agents follow about reports/lanes* →
  `workspace-process`.
- `persona-llm` vs `agent-behavior` — *the model/harness substrate* → `persona-llm`;
  *model-agnostic conduct* → `agent-behavior`.
- The bare word `mail` collides — `mail`+`signal`/`router` → `signal-wire`;
  `mail`+`assistant`/`email` → `personal-affairs`. The keyword/co-text layer splits it.

**Enlargement / retirement:** closed set, new categories vetted through the same
guardian one level up (is this genuinely new, or "schema wearing a hat?"). A keyword
that recurs across many records *and* many categories is the signal to promote it
(`macro` and `trace` are the near-term watch; a project-name axis is the likeliest
16th). `forge-build` is the symmetric case — on explicit probation with a fold trigger.

**Four things for the psyche to confirm** (the catalog's open questions):

1. **Accept `schema` at 31%**, or carve a thin `schema-emission` slice into
   `rust-code`? My lean: accept it — it's the real densest domain and multi-membership
   dilutes the guardian bundle anyway.
2. **`forge-build` as a 15th category now**, or start it folded into `infra-deploy`
   and let the enlargement gate re-promote it on evidence? (12 records; either is fine.)
3. **Cross-cutting design disciplines** ("no backward compat pre-production", "single
   best shape") — filed under `workspace-process`, or do they deserve a dedicated
   `design-discipline` category? My lean: `workspace-process` for now.
4. **Bootstrap migration must NOT reuse the substring heuristic** (`engine.rs:794-882`
   — the one that reached 6/12 and sank everything into `Meaning`). The topic→category
   remap needs a psyche-blessed reviewable table run through the agglomeration
   machinery, per operator 355 §4.

## Part B — how good is the agent-guardian?

Short answer: **the engineering is good; the guardianship is weak.** Graded by layer:

| Layer | Grade | One line |
|---|---|---|
| Agent component + signal-agent transport | **good** | clean, type-safe, fail-closed, secrets-correct v1 |
| Spirit-side guardian path | **good** | fail-closed, panic-free, strict parse; operational gaps |
| The guardian's actual judgment (prompt + retrieval) | **weak** | asks the right question, can't reliably answer it |

### What is genuinely good (the plumbing)

- **Fail-closed is complete and real.** Every error path — socket down, malformed
  output, agent rejection — maps to a typed `GuardianRejected`. `Propose` never
  silently becomes an admit. No silent-accept gap anywhere. This is the single most
  important property and it holds.
- **NOTA output is *enforced*, not just requested**, on both sides: the agent
  validates the completion parses (`Document::parse`), retries once with the error fed
  back, then rejects with `InvalidNotaOutput`; spirit independently re-parses the
  verdict. Prose cannot leak into the typed verdict (`agent/engine.rs:171-187`,
  `guardian.rs:197-199`).
- **Secret discipline is clean.** Only an env-var *handle* is ever stored (nix, rkyv,
  lockfile, logs all handle-only); the key is resolved at call time into a
  redacted-`Debug` type and sent bearer-only to the TLS endpoint. Matches the 354
  claim exactly.
- **Binary-startup discipline is correct** — daemon takes one rkyv archive, NOTA
  confined to the `agent-write-configuration` deploy edge, meta-tier frame bounded.
- **Strict verdict parse** rejects chatty/empty/prose output (exactly-one-root NOTA).
- Provider abstraction is right-sized (one OpenAI-compatible provider by config, an
  offline fixture provider so the default build needs no network/key).

### The headline operational defect (new — not in 581)

**[high] The blocking guardian socket call runs inside spirit's single serializing
engine-actor mailbox with no `block_in_place`.** So the *entire spirit daemon stalls*
for the full LLM round-trip on every gated `Propose` — every other Record/Query/Count
queues behind it. The SEMA path correctly wraps blocking work in
`tokio::task::block_in_place` (`nexus.rs:544`); the guardian call (`guardian.rs:127-155`
via `nexus.rs:605`) does not. This violates the workspace's own
no-blocking-in-actor-handlers rule. Not a corruption or safety bug — a throughput
cliff under any concurrency. Minimal fix: the same `block_in_place` the SEMA path
already uses.

### Other operational gaps (medium/low)

- **[high] Retrieval is unbounded** — a `Meaning` proposal stuffs ~924 records into
  one prompt. No cap, no ranking truncation. (This is question A's problem wearing a
  guardian costume.)
- **[medium] No `MaximumFrameLength` cap on the working transport** (the meta tier was
  bounded to 1 MiB; the working socket wasn't) — a large length-prefix drives a big
  pre-allocation. Emitter-level fix, lands once for every triad component.
- **[medium] No agent-side call timeout/budget** — the only deadline is spirit's
  socket timeout; a slow provider leaves an orphaned, unaccounted in-flight call.
- **[medium] No test covers the malformed/socket/timeout fail-closed paths** — only
  Accept and Reject(NonIntent) are tested; the fail-closed behavior is asserted nowhere.
- **[low] Timeout is mislabeled `HarnessUnavailable`** (`HarnessTimedOut` is dead code).
- **[low] The LLM is called *before* the cheap exact-duplicate check** — wastes a
  round-trip on duplicates.
- **[low] The guardian discards `stop_reason`** — a length-truncated completion that
  still happens to parse as a verdict is accepted as if clean.

### The weak layer — the judgment itself (prompt + retrieval)

The prompt graded **weak**: *right job named, wrong job enforceable.* The system line
asks exactly the 578 §4 question and demands a typed verdict — correct framing. But:

- **Undefined criteria.** "contradiction, compound intent, non-intent, unclear
  privacy, unclear category, retrieval insufficiency" are named with zero definitions,
  zero examples, no few-shot. The model invents what each means.
- **Output grammar underspecified.** One example string; the closed
  `GuardianRejectionReason` atom set is never given, and the mandatory double-`Reject`
  nesting is never explained. A model that emits a single `Reject`, an invented reason
  atom, or one word of prose produces valid NOTA that *fails the typed verdict parse* —
  and the agent's retry loop only checks "is it any NOTA," not "is it a
  `GuardianVerdict`." So a legit arrow gets bounced (fail-closed, but lossy) on a
  formatting miss with no type-aware retry.
- **Temperature unpinned** (`guardian.rs:184` → provider default ~1.0). The same
  proposal+bundle can Accept on one run and Reject on the next. A consistency gate
  wants temperature 0. 581 §4 flagged "zero discretion realized by a non-deterministic
  guardian" — this is *why*: it's a sampled yes/no.
- **Retrieval is the deepest flaw, and it's upstream of the prompt.** Category-only
  seeding (keyword/text hard-coded to `Any`) makes the bundle simultaneously **too big**
  (924 unranked records for `Meaning`) and **too narrow** (a contradicting record in a
  *different* category is never shown). The prompt cannot judge consistency against a
  bundle that structurally omits the contradiction.

Concretely, this guardian **would wrongly accept** a real contradiction whose
conflicting record lives in a different category (the seed never includes it), a
misattributed paraphrase-duplicate (text matching is off), and a confidently-worded
task-order dressed as a Decision ("non-intent" is undefined). It **would wrongly
reject** a legit `Meaning`-tagged arrow (volume manufactures spurious "tension"), a
valid arrow on a formatting technicality, and a genuine first arrow in an empty
category (read as "retrieval insufficiency").

### The connection between the two questions

The guardian's weak layer is mostly **not a prompt problem — it's the retrieval/category
problem from Part A.** A guardian is only as good as the bundle it's shown. So the
highest-leverage guardian fix is the *same* work as the catalog fix:

1. Bless the grounded catalog (Part A) → the seed bundle becomes ~tens of relevant
   records, not 924.
2. Wire `guardian_records_for` to union category **+ keyword + full-text** on the
   proposal's own description (the extractor is built, unused) → cross-category
   contradictions become visible.
3. *Then* the prompt fixes (pin temperature 0; embed the closed reason set + exact
   verdict grammar generated from the enum; make the agent's NOTA retry type-aware
   against `GuardianVerdict`) turn a sampled, lossy yes/no into a reliable one.

## What the psyche decides, and what operator does

**Psyche (intent-level):**

1. **Bless the 15-category catalog** (Part A) — or adjust it — and answer its four
   open questions (`schema` at 31%, `forge-build` status, design-discipline category,
   reviewable-mapping migration). This is the highest-leverage single decision; the
   guardian can't be trustworthy on the gerund index.
2. Confirm the gate-reach intent from 581 (clarify + supersede must be guarded) — still
   standing.

**Operator (ordered — aligns with 355's order, with the new concurrency bug inserted):**

1. **Wrap the guardian call in `block_in_place`** (the new high-severity concurrency
   bug — minimal fix, matches the SEMA pattern). Cheap, do it first.
2. **Fix guardian retrieval** — union keyword + full-text on the proposal's text, and
   **cap + rank** the bundle (top-N by certainty+importance+similarity). This is
   operator 355's #1 and unblocks the guardian's judgment.
3. **Bless-then-migrate categories** off a reviewable mapping (after psyche §1), not the
   substring heuristic.
4. **Guard clarify + supersede**; give the dead reasons live paths (581 §4 / 355 §2-3).
5. **Prompt hardening** — temperature 0; closed reason set + exact grammar from the
   enum; type-aware NOTA retry against `GuardianVerdict`; definitions for the boundary
   cases (forward-law-vs-negation, task-order-vs-intent, empty-bundle-is-admissible).
6. Hardening: `MaximumFrameLength` on the working transport; agent-side call timeout;
   fail-closed path tests; map timeout → `HarnessTimedOut`; run duplicate-check before
   the LLM.
7. (Defer, deliberately) the §4a broker — sound to carry until a second judgment
   consumer (the auditor) or higher volume arrives; track the missing channel auth +
   budget accounting so it isn't forgotten.

**Spirit-gate capture candidate** (unrecorded, awaiting psyche): once the catalog is
blessed, that's a Decision worth recording — *Spirit categories are grounded
work-domains, not abstract taxonomies* — together with its first instance (the
15-category set). I'll record it on your word, not before.

Workflow run `wf_2c3d7cd8-7e7` (6 agents: 2 catalog + merge/stress-test, 3 guardian graders).
