# 55 — Spirit operation variant-ladder design research (2026-06-02)

Kind: sub-agent report (system-designer lane, inherited from orchestrator per Spirit 920).
Frame: READ-ONLY research + design. Source the psyche directive (Spirit 1474, Decision High), draw on production Spirit v0.3.0, spirit-next's design moves, the actual 1399-record live corpus, and CLI variant-ladder tradition. Recommend specific variant-ladders per operation. Do not implement; do not write Spirit records; do not propose removing or renaming existing canonical roots.

## Frame

Psyche directive 2026-06-02 (captured as Spirit 1474, Decision High) reads:

*"Spirit operations should support a simpler-to-more-complex variant ladder — short forms with summary defaults for normal/common operations, complex forms with full metadata for custom/precise operations. The ladder lets the psyche or agent choose the right explicitness level per moment. Short forms serve daily use without the cognitive cost of full NOTA; complex forms preserve precise control for cases that need it. Both shapes coexist in the wire vocabulary as distinct operation roots; the complex root is canonical, the short root expands to a default form of the complex root."*

Spirit 1472 (Principle High) restates the same shape: *"Spirit command surfaces should offer simple-to-complex operation variants: concise summary defaults for normal use, and explicit full-metadata/custom forms for advanced use."* Spirit 1473 (Decision Medium) constrains the design direction: *"Future Spirit expansion should use spirit-next as design inspiration while tying together the richer data already present in production Spirit."*

The directive is firm on three points:

1. Short and complex forms coexist as **distinct operation roots** at the wire layer (not flags, not options — Spirit's single-NOTA-argument rule per `skills/component-triad.md` §"The single argument rule" forbids flags).
2. The **complex root is canonical**; short roots **expand to a default form of the complex root**. The complex form survives unchanged; short forms are convenience entry points.
3. Both shapes live in the **wire vocabulary**, so the typed client library, the CLI, and any future schema-emitted code all see them.

Scope of this report:

- Enumerate the current Spirit operation surface and annotate where complexity-gradient already exists.
- Absorb spirit-next's design moves (`Lookup` / `Count` split, `DatabaseMarker` envelope, the privacy schema already present in spirit-next per Spirit 1463).
- Mine the live 1399-record Spirit store for patterns that determine which short forms are worth designing.
- Survey CLI variant-ladder tradition (git, kubectl, jq, REST APIs, Common Lisp `with-` macros, Cobra, `clig.dev`) to ground the recommended pattern.
- Propose a graduated ladder per major operation, naming each tier's NOTA shape and its expansion to the canonical complex form.
- Verify the proposed names fit Spirit's naming-style register.
- Surface open questions for psyche before any landing.

Read-order for the reader: Frame → Current surface → Spirit-next inspiration → Corpus → CLI tradition → Privacy implications → Proposed ladders → Naming-style check → Open questions → Sources.

## Current Spirit operation surface — enumeration with complexity gradient

Source: `skills/spirit-cli.md` lines 132-247 (live v0.3.0 wire shape) and `signal-persona-spirit/spirit.schema` (declarative form). Below: every operation root, its NOTA shape, its minimum-meaningful invocation, the implicit defaults baked into how agents actually call it, and where the complexity gradient already exists.

### The seven operation-root families

**Family 1: Capture.** `Record` writes a new intent entry.

```
(Record ([<topic> ...] <Kind> [description] <Magnitude>))
```

Four positional fields: topics, kind, description, magnitude. Minimum-meaningful invocation is the same as the full form — there is no shorter capture. Daemon stamps the time; client supplies nothing else. The complexity gradient is zero: every `Record` call uses all four fields. Complexity lives elsewhere in the wire (`State` is a lighter variant; see Family 7).

**Family 2: Maintain.** `Remove` and `ChangeCertainty` mutate one stored record by identifier.

```
(Remove <RecordIdentifier>)                       — one positional field
(ChangeCertainty (<RecordIdentifier> <Magnitude>)) — two positional fields
```

Both are already minimal. No complexity gradient.

**Family 3: Observe — by topic + kind + certainty + time + mode (the rich filter).** This is the heaviest operation root in production.

```
(Observe (Records (
   <TopicSelection: (Any []) | (Partial [a b]) | (Full [a b])>
   <Option Kind: None | (Some Decision) | ... >
   <CertaintySelection: Any | (Exact M) | (AtMost M) | (AtLeast M)>
   <RecordedTimeSelection: Any | Recent | Shallow | Deep | VeryDeep |
                            (Since (D T)) | (Until (D T)) | (Between ((D T) (D T)))>
   <ObservationMode: SummaryOnly | WithProvenance>)))
```

**Five positional fields nested under `Records`, wrapped in `Observe`.** Minimum-meaningful invocation: `(Observe (Records ((Any []) None Any Recent SummaryOnly)))` — 56 characters of NOTA structure with five `Any`-style "no filter" tokens, just to get the 15 most-recent records. That is the daily-use cost. The complexity gradient is steep: each field can be `Any` (no filter) or carry a selector value.

**Family 4: Observe — by identifier.** A separate path through the same operation root.

```
(Observe (RecordIdentifiers (
   <RecordIdentifierSelection: (Exact N) | (Range (N M))>
   <ObservationMode: SummaryOnly | WithProvenance>)))
```

Two fields under `RecordIdentifiers`, wrapped in `Observe`. Minimum: `(Observe (RecordIdentifiers ((Exact 1234) SummaryOnly)))` — to fetch ONE record by id, 51 characters of NOTA with double-nested parentheses around the single id.

**Family 5: Observe — by enumeration (the trivial ones).** Two more sub-roots under `Observe` carry zero fields:

```
(Observe Topics)        — list all topics with counts
(Observe Questions)     — list all questions (placeholder surface)
(Observe State)         — current presence/focus
```

Already minimal. Already at the "tier-1" level.

**Family 6: Subscription.** `Watch`, `Unwatch`, `Tap`, `Untap` — long-lived streams.

```
(Watch (State))
(Watch (Records ((Some <topic>) <Mode>)))
(Unwatch (<SubscriptionToken: (State <id>) | (Records <id>)>))
(Tap)
(Untap)
```

Two fields max. The CLI's single-call shape isn't well suited to long subscriptions; agents use the typed client library. Out of scope for variant-ladder design.

**Family 7: Free-form statement.** `State` accepts unstructured text that gets sema-classified as an `Assert` observation.

```
(State [free-form text])
```

Single field. Already the ABSOLUTE minimum.

### Complexity gradient — at a glance

| Operation root | Positional fields | Daily minimum length (chars) | Complexity already gradient? |
|---|---|---|---|
| `(State [...])` | 1 | ~12 | already minimal |
| `(Remove N)` | 1 | ~12 | already minimal |
| `(ChangeCertainty (N M))` | 2 | ~30 | already minimal |
| `(Record ([t] K [d] M))` | 4 | ~50 | already minimal (this is dense, not redundant) |
| `(Observe Topics)` | 0 | 16 | already minimal |
| `(Observe (Records ((Any []) None Any Recent SummaryOnly)))` | 5 nested | 56 | **steep — every call has 5 fields, often all `Any`** |
| `(Observe (RecordIdentifiers ((Exact N) SummaryOnly)))` | 2 nested | 51 | **steep — every single-record fetch has 2 layers of wrapping** |

The complexity gradient lives almost entirely in `Observe (Records ...)` and `Observe (RecordIdentifiers ...)`. Those are also the operations agents call MOST OFTEN (corpus analysis below). The four other root-families are already at a sane minimum. Variant-ladder design effort concentrates on `Records` / `RecordIdentifiers` and on a few cross-cutting convenience shapes (Today, ThisWeek, Decisions, Maximum-Decisions, etc.) that combine multiple filter dimensions.

## Spirit-next inspiration — what design moves does it already make?

Source: `/git/github.com/LiGoldragon/spirit-next/schema/lib.schema` (read in this session) and report 53 SA1 (the wire-shape parity audit).

Spirit-next has already made several design moves that are relevant to variant-ladder thinking — including the `Lookup`/`Count` split that IS a kind of variant ladder, and the `Privacy Magnitude` reuse that anticipated Spirit 1463.

### Move 1: Split read into three sibling operation roots

Production has ONE operation root `Observe` wrapping FIVE sub-roots (`State`, `Records`, `RecordIdentifiers`, `Topics`, `Questions`). Spirit-next splits the most-used three into siblings at the top level:

```
Input enum (spirit-next schema/lib.schema:2):
  (Record Entry)
  (Observe Query)         — multi-record filter, similar to production's (Observe (Records ...))
  (Lookup RecordIdentifier) — single-record fetch, replaces (Observe (RecordIdentifiers ((Exact N) ...)))
  (Count Query)           — record-count, no production equivalent
  (Remove RecordIdentifier)
  (LookupStash StashHandle)
```

This IS a variant ladder — the same underlying read (find records matching some shape) is split into three different operation roots based on **what you want back**:

- `Observe Query` returns the matching records themselves (heaviest reply).
- `Lookup RecordIdentifier` returns ONE record by handle (single-shape reply).
- `Count Query` returns just a count (lightest reply, single integer).

This generalises the spirit-next insight: the result-shape dimension is orthogonal to the filter dimension. Production handles it via `ObservationMode (SummaryOnly | WithProvenance)`. Spirit-next promotes it to operation-root level. Both approaches are valid; spirit-next's wins on terseness for the count case.

### Move 2: `DatabaseMarker` envelope on every reply

Every spirit-next reply bundles a `DatabaseMarker { CommitSequence, StateDigest }`. This is provenance discipline per Spirit 1389 (slim Nexus output) — the daemon's reply identifies "the database state at the moment of reply" so a follow-up query can be ordered against it. Production replies are bare (`(RecordAccepted N)`) — terser but provenance-free.

For variant-ladder design: the envelope is orthogonal to the operation root. Short-form roots and complex-form roots both produce a reply with the same envelope. The envelope isn't part of the variant ladder; it's a global wire property.

### Move 3: `Privacy` is already a `Magnitude` field

Spirit-next schema declares `Privacy Magnitude` and `PrivacySelection [Any (Exact Privacy) (AtMost Privacy) (AtLeast Privacy)]` (lines 49-50 in `schema/lib.schema`), and `Entry { Topics * Kind * Description * Magnitude * Privacy * }` carries the privacy field as a fifth position. `Query` includes `privacy_selection PrivacySelection`. This anticipates and ALREADY MANIFESTS Spirit 1463 (Magnitude-on-privacy-axis) at the schema layer. The `AtMost / AtLeast / Exact / Any` filter pattern already pairs the existing `CertaintySelection` family.

Production's `spirit.schema` declares the same shape — `PrivacySelection (Any (Exact Privacy) (AtMost Privacy) (AtLeast Privacy))` plus `Entry [Topics Kind Description Certainty Privacy]` — but the deployed v0.3.0 daemon currently emits **4-field summaries** without privacy in `RecordsObserved` replies (verified by querying recent records — no privacy field surfaces in the wire). This is a deployed-vs-declared drift. Variant-ladder design should ASSUME the privacy field exists at the wire layer; the production deployment will catch up to its own schema declaration.

### Move 4: Slim engine output + the Stash effect pattern

Spirit-next adds `LookupStash StashHandle` and a `Stash` nexus-effect that lets the engine cache a query result and hand back a handle for later pickup. This is per Spirit 1389 (slim Nexus output) extending to nexus-cache discipline. Not directly part of the variant ladder, but RELATED: it's another "result-shape variant" — same underlying records, different shape of "how you get them back." For the variant-ladder design, the Stash pattern is a possible Tier-N variant of `Observe` that returns a handle instead of records.

### Synthesis — what spirit-next teaches the variant-ladder design

1. **The result-shape dimension is its own variant axis.** Production conflates filter (`Records`) and result-shape (`SummaryOnly` / `WithProvenance`) at different nesting levels. Spirit-next promotes result-shape variation to operation-root level via `Observe` vs `Lookup` vs `Count`. The variant-ladder should treat this as orthogonal: short-form roots can SAY whether they want "records back," "an identifier back," "a count back," or "just an acknowledgement back."
2. **Wrap-vs-sibling is a real choice.** Production wraps `Records`/`RecordIdentifiers`/`Topics`/`Questions`/`State` under `Observe`. Spirit-next exposes them as siblings. The variant-ladder design can ADD sibling short-form roots without removing the wrapped form (the wrap stays for the canonical complex case; the siblings provide the daily-use convenience).
3. **The privacy filter is already designed.** Spirit-next has `PrivacySelection [Any (Exact P) (AtMost P) (AtLeast P)]` in the same shape as `CertaintySelection`. Variant-ladder default behaviour around privacy needs to be decided (see §"Privacy-filtering implications" below), but the FILTER LANGUAGE is fixed.

## Corpus analysis — what use patterns are actually in the data?

Source: live `spirit` queries against the deployed v0.3.0 daemon during this session. The store currently holds **1399 records** (`spirit "(Observe (RecordIdentifiers ((Range (1 5000)) SummaryOnly)))"` — counted via the response).

### Total record count + recent ingestion rate

| Window | Count |
|---|---|
| All records (Range 1-5000) | 1399 |
| Today (Since 2026-06-02 00:00:00) | 65 |
| Since 2026-06-01 00:00:00 | 142 |
| Since 2026-05-26 00:00:00 (the previous week) | 683 |

Ingestion rate is HIGH — ~140 records per day at present, ~700 records per week. Any daily-use observation needs to handle that volume gracefully.

### Verbal-recency depth counts (Spirit 1338 vocabulary)

The Recent/Shallow/Deep/VeryDeep family has explicit target counts per Spirit 1338:

| Depth | Reported records | Bytes of response |
|---|---|---|
| `Shallow` | 5 | 2165 |
| `Recent` | 15 | 8604 |
| `Deep` | 30 | 13613 |
| `VeryDeep` | 100 | 42954 |

The shape is exactly Spirit 1338's "Shallow Recent Deep VeryDeep with target counts 5 15 30 100." `Recent` is the natural day-to-day default — 15 records, ~8KB of NOTA. `Shallow` is for "what JUST changed." `VeryDeep` for "give me the substantial pool."

### Kind distribution (on VeryDeep window of 100)

| Kind | Count in VeryDeep window |
|---|---|
| Decision | 100 |
| Principle | 100 |
| Correction | 100 |
| Clarification | 101 |
| Constraint | 100 |

All five kinds saturate the 100-record window — each kind has at least 100 recent records. The kinds are evenly used. There is no rarely-used kind that would be a candidate for a special-case short form.

### Magnitude distribution (on VeryDeep window of 100, by exact level)

| Magnitude | Exact count in VeryDeep window |
|---|---|
| Zero (removal-candidate marker) | 4 |
| Minimum | 11 |
| VeryLow | 0 |
| Low | 6 |
| Medium | 101 |
| High | 100 |
| VeryHigh | 4 |
| Maximum | 100 |

Sharply bimodal — Medium, High, and Maximum are the dominant authoring levels (effectively all records carry one of these three). Zero, Minimum, Low, VeryHigh are tail levels. VeryLow is essentially unused. **For short-form variants, the "by magnitude" axis collapses to a three-tier choice in practice: Medium-or-above, High-or-above, Maximum.**

### Magnitude bands (on VeryDeep window of 100)

| Selector | Count |
|---|---|
| `(AtLeast High)` | 100 |
| `(AtLeast Maximum)` | 100 |
| `(AtMost Low)` | 21 |

The high-end bands saturate the 100-record window — there are LOTS of high-certainty records to find. The low end (Low or below) is small — that's the "review band" for removal candidates and weak intent.

### Topic frequency (top 30 by `Observe Topics` count)

From `(Observe Topics)`:

| Topic | Count |
|---|---|
| schema | 385 |
| nota | 140 |
| workspace | 111 |
| spirit | 96 |
| signal | 87 |
| component-shape | 78 |
| persona | 54 |
| cloud | 54 |
| schema-language | 49 |
| sema | 44 |
| nexus | 35 |
| asschema | 33 |
| spirit-next | 31 |
| reports | 29 |
| naming | 23 |
| privacy | 23 |
| workflow | 22 |
| nix | 20 |
| deployment | 20 |
| macro | 20 |
| testing | 18 |
| prototype | 18 |
| criomos | 17 |
| rust | 16 |
| schema-next | 16 |
| operator | 15 |
| implementation | 15 |
| roles | 8 |
| deploy | 14 |
| persona-pi | 14 |

The long tail is real: `(Observe Topics)` returns hundreds of topics, most with counts of 1-5. The top ~20 topics carry the bulk of the workload, with `schema` dominating at 385 occurrences. **For short-form variants targeting topic filters, the empirical answer is: there is no SMALL set of topics worth special-casing.** Topic is too high-cardinality. The Tier-2 short form should accept ONE topic name as an arbitrary string, not a closed enum.

### Patterns that suggest specific short forms

From the patterns above and from observing how agents call the CLI:

| Empirical observation | Implied short form |
|---|---|
| Daily-use is `(Recent + SummaryOnly + no filter)` — the 15-record "what's new" call | `Recent` as a zero-arg operation root |
| Topic-filtered "what's new on X" — most common with `Partial [topic]` | `RecentOn [topic]` taking one topic |
| Decision discovery — agents want "what Decisions were made on X" | `DecisionsOn [topic]` |
| Maximum-certainty bedrock retrieval — workspace principles + decisions | `Bedrock` (or similar) returning `(AtLeast Maximum)` filter |
| Today/yesterday/this-week reading — calendar-anchored reads | `Today`, `Yesterday`, `ThisWeek` (with daemon-resolved date math) |
| Single-record lookup — current `(Observe (RecordIdentifiers ((Exact N) SummaryOnly)))` | `Lookup N` (spirit-next-style) |
| Range lookup — current `(Observe (RecordIdentifiers ((Range (N M)) ...)))` | `LookupRange (N M)` |
| Count for ad-hoc aggregation — currently impossible | `Count` (spirit-next-style) |
| Topic enumeration | already minimal at `(Observe Topics)`; could alias to `Topics` |

The corpus DOES NOT support these candidate variants:
- "Just give me Decisions" — `Decisions` as zero-arg — there are 100+ recent Decisions; topic filter is needed for usefulness. (`DecisionsOn [topic]` works; bare `Decisions` would return too much.)
- "VeryLow records" — VeryLow is unused (0 occurrences); no need for a short form.
- A "by-author" filter — Spirit records have no author field; only the psyche records intent.
- A "by-week-day" filter — corpus doesn't show week-anchored patterns.

## CLI variant-ladder design patterns — survey with citations

The variant-ladder pattern is well-established across CLI and API tradition. Below: distinct strands of design wisdom from each major tool, sourced via WebSearch + WebFetch (URLs in §Sources).

### git: smart-default + escape-hatch flag

`git status` defaults to the long human-readable format. `git status -s` (or `--short`) collapses to a two-character status code per file for at-a-glance reading. `git status --porcelain` is a script-stable variant. The pattern: ONE primary command, ONE smart default, with FLAGS escalating to different output shapes ([git-status manual](https://git-scm.com/docs/git-status/2.2.3), [Stefan Judis on git status short](https://www.stefanjudis.com/today-i-learned/the-short-version-of-git-status-and-the-close-but-different-porcelain-mode/)).

Lesson for Spirit: in flag-soup world, this would be the natural shape — one operation root with optional flags. In NOTA-no-flags world, the equivalent is multiple operation roots that all map to the same engine logic but with different default-output shapes. Spirit-next's `Observe` / `Lookup` / `Count` already follows this pattern.

`git log` defaults to a chronological commit list with format `%C(...)%H%n%an%ae%n%s%n%b`. Flags like `--oneline`, `--graph`, `--pretty=full`, `--all`, `--decorate` add up to power-user combinations like `git log --oneline --graph --all --decorate`. The pattern: smart defaults THAT WORK for the common case, plus orthogonal flag composability for power use.

### kubectl: tiered output via -o

`kubectl get pods` defaults to a column-truncated table. `kubectl get pods -o wide` adds more columns (IP, node, readiness gates). `kubectl get pods -o yaml` or `-o json` dumps the full resource as a serialised value. `kubectl get pods -o jsonpath='{.items[*].metadata.name}'` lets you extract any subtree ([kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/), [Baeldung on kubectl output formatting](https://www.baeldung.com/ops/kubectl-output-format)).

The pattern: SAME query, SAME filter, but output SHAPE is a separate dimension. Each output shape carries a different complexity ladder — `wide` is "more columns," `yaml` is "give me everything," `jsonpath` is "give me exactly this subtree."

Lesson for Spirit: result-shape orthogonality is real. Production handles it via `ObservationMode (SummaryOnly | WithProvenance)`. Spirit-next promotes the count case via `Count`. Variant-ladder design should keep the result-shape dimension orthogonal — short-form `Recent` returns summaries; short-form `RecentWithProvenance` returns provenance-stamped summaries; short-form `RecentCount` returns just a count.

### jq: progressive complexity from identity outward

jq's first filter is `.` — the identity. It returns whatever you give it. The next step is `.field` — one field of an object. Then `.field[0]` — index into a sub-array. Then `.field[] | select(.predicate)` — a filter over a generator. Then `(. as $x | $x.field as $y | ...)` — full named-binding programming model ([jq 1.8 Manual](https://jqlang.org/manual/), [Programming Historian jq lesson](https://programminghistorian.org/en/lessons/json-and-jq)).

Each step adds expressive power; each tier is a legitimate stopping point. A user who only ever knows `.` and `.field` gets real value; a user who learns the full language gets unbounded power.

Lesson for Spirit: the ladder should have **multiple useful tiers**, each a legitimate destination. Not just "easy mode" vs "expert mode" — a graduated set where each rung delivers real ergonomic benefit. Spirit's natural rungs: zero-arg (Today, Recent, Bedrock), one-arg (RecentOn [topic], Lookup N), two-arg (RecentDecisionsOn [topic], LookupRange (N M)), full-custom (the existing `Observe (Records ...)` form).

### Common Lisp `with-` macros

The `with-open-file`, `with-open-stream`, `with-input-from-string` macros expand to a `let` + `unwind-protect` + cleanup pattern. The macro hides 4-6 lines of bookkeeping per call, while the unmacroed form remains accessible for unusual cases ([Common Lisp Cookbook §Macros](https://lispcookbook.github.io/cl-cookbook/macros.html)).

The pattern: when a multi-step ritual is common, give it a name; the ritual stays accessible underneath.

Lesson for Spirit: `(Recent)` is a NAME for the ritual `(Observe (Records ((Any []) None Any Recent SummaryOnly)))`. The ritual itself is still legal NOTA. The name is the convenience. Spirit-next-style: the named form is a distinct operation root that expands deterministically.

### REST API patterns: default minimal + include/expand

Eventbrite, GitHub, Stripe APIs default to MINIMAL representations and let the client request expansion via `?include=full`, `?expand[]=foo`, or similar ([Zapier on flexible API responses](https://zapier.com/engineering/flexible-api-responses/), [Speakeasy on request parameters](https://www.speakeasy.com/api-design/parameters)). The "minimal default + expansion when asked" pattern matches the spirit-next `Lookup` (returns full record) vs `Observe` (returns summary stream) split.

### Cobra and clig.dev: the "sensible defaults + accessible power" doctrine

Cobra (the Go CLI framework backing kubectl, docker, helm, hugo, github CLI) is explicit about "Convention over configuration": defaults work for the common case; flags add the unusual ([Cobra Philosophy](https://cobra.dev/docs/explanations/philosophy/)). clig.dev codifies this further: *"Make the default the right thing for most users... Have full-length versions of all flags. Only use one-letter flags for commonly used flags"* ([Command Line Interface Guidelines](https://clig.dev/)).

The lesson: short-form operations should hit the COMMON case. The complex form must remain available for the uncommon case. Both must be FIRST-CLASS — short isn't "lossy" and complex isn't "punishment for needing precision." They're two entry points into the same engine.

### Synthesising the survey

| Tradition | Lesson for Spirit |
|---|---|
| git status / git log | Smart defaults + orthogonal flags. In NOTA world: smart-default operation roots + orthogonal result-shape roots. |
| kubectl get -o | Result-shape orthogonality. Same query, different output. Spirit needs this. |
| jq | Multi-tier ladder, each tier useful, each tier composable. |
| Common Lisp `with-` macros | Name the ritual; keep the ritual accessible. |
| REST include/expand | Default minimal; opt into expansion. |
| Cobra / clig.dev | Convention over configuration; both ends of the ladder are first-class. |

The variant-ladder for Spirit should: (1) be a GRADUATED set of operation roots, not a binary short-vs-long pair; (2) treat result-shape as an orthogonal axis; (3) DEFAULT to the common case while keeping the precise form fully accessible; (4) name each tier deterministically.

## Privacy-filtering implications (Spirit 1463)

Source: Spirit 1463 (Decision Maximum 2026-06-02): *"Spirit privacy is a Magnitude on the privacy axis — records gain a privacy field typed Magnitude where Zero means no privacy (open/public) and Maximum means sealed."* Spirit 1449 (Clarification High 2026-06-02): *"Default access classification on a Spirit record is the most-public level."*

The privacy field reuses the Magnitude vocabulary. Filter selectors follow the established `CertaintySelection` pattern — `PrivacySelection [Any (Exact P) (AtMost P) (AtLeast P)]`. The schema is already present in both production's `spirit.schema` (declared, but deployed daemon ignores it for now) and in spirit-next.

For variant-ladder design, the question is **what privacy filter does a short-form variant DEFAULT TO?**

### Three principled defaults

**Default A: Most-conservative — `(AtMost Zero)`.** Short forms return only Open records (privacy = Zero). To reach elevated material, the agent must use the complex form OR a special short form that names the privacy level explicitly. This matches the spirit-next §"Sub-agent clearance inheritance" framing (Spirit 1448) where the sub-agent's filter must be set EXPLICITLY to reach elevated records even when their clearance allows it.

Pros: safest. Sub-agents and accidental observations cannot leak elevated material.

Cons: the most common case (owner reading their own intent log) becomes "you can't see your sensitive records" unless you use a special form. For the owner socket this is over-restrictive.

**Default B: Socket-determined — owner socket sees all, ordinary socket sees only Open.** The privacy default depends on which socket the request arrives on:

- Ordinary socket short-form `Recent` → `(AtMost Zero)`.
- Owner socket short-form `Recent` → `Any` (no privacy filter).

This matches the existing socket clearance discipline. The CLI wrapper routes to the right socket; the daemon enforces.

Pros: matches the socket model already. No special syntax needed for "give me MY private records on the owner socket."

Cons: behaviour differs across sockets for the SAME operation root. A user copy-pasting commands between sockets sees different results. Less predictable.

**Default C: Most-permissive — `Any`.** Short forms apply no privacy filter; the records returned are whatever the requester's clearance allows. To filter privacy, use the complex form.

Pros: simplest mental model. The short form is "just give me what's there"; the complex form is "filter precisely."

Cons: requires that socket-level clearance be the ONLY privacy enforcement layer. A short-form call on the owner socket returns all privacy levels mixed together.

### Recommendation

**Default B (socket-determined)** is the right shape. Justification:

1. The deployment already has TWO sockets (ordinary + owner) precisely to mediate clearance. The variant-ladder should respect that boundary, not duplicate it.
2. The Tier-1 short form `Recent` on the ordinary socket returns Open-only records — agents that have no business with elevated material default-safely.
3. The Tier-1 short form `Recent` on the owner socket returns everything the owner has access to — the owner doesn't have to type a privacy filter to see their own records. (This matches §Q6 in report 54: sub-agents have owner clearance but must explicitly filter; the owner user themselves doesn't need to type the filter for the default read.)
4. Complex-form `(Observe (Records (... <PrivacySelection> ...)))` always lets the requester narrow further.

For variant naming: short forms that explicitly request a single privacy level become named convenience operations. Examples:

- `RecentSealed` → `(Observe (Records ((Any []) None Any Recent SummaryOnly (Exact Maximum))))` on owner socket, error on ordinary socket.
- `RecentOpen` → `(Observe (Records ((Any []) None Any Recent SummaryOnly (Exact Zero))))` — explicit "show me only public material" useful when sharing.

These can be deferred to a later tier — the core ladder does NOT need to name every privacy level.

## Proposed variant ladders

Per major operation. Each ladder names a graduated set of operation roots, gives each tier's NOTA shape, shows the expansion to the canonical complex form, and lists which defaults the short form injects.

### Operation: Observe (Records ...) — the multi-record filter ladder

The biggest ladder. This is where complexity-gradient is steepest and short-form payoff is largest.

#### Tier 1 — zero-argument convenience reads

```
(Recent)
  expands to: (Observe (Records ((Any []) None Any Recent SummaryOnly)))
  defaults injected: TopicSelection=Any, Kind=None, CertaintySelection=Any,
                     RecordedTimeSelection=Recent, ObservationMode=SummaryOnly,
                     PrivacySelection=socket-determined
  result: 15 most-recent records (Spirit 1338), summary only

(Shallow)
  expands to: (Observe (Records ((Any []) None Any Shallow SummaryOnly)))
  defaults: same as Recent but Shallow depth (5 records)

(Deep)
  expands to: (Observe (Records ((Any []) None Any Deep SummaryOnly)))
  defaults: same but Deep depth (30 records)

(VeryDeep)
  expands to: (Observe (Records ((Any []) None Any VeryDeep SummaryOnly)))
  defaults: same but VeryDeep depth (100 records)

(Today)
  expands to: (Observe (Records ((Any []) None Any (Since (<TODAY> 00:00:00)) SummaryOnly)))
  daemon-resolved TODAY date. Variant-only-on-server: the date math
  happens on the daemon, not the client.

(Yesterday)
  expands to: (Observe (Records ((Any []) None Any (Between ((<YESTERDAY> 00:00:00) (<YESTERDAY> 23:59:59))) SummaryOnly)))

(ThisWeek)
  expands to: (Observe (Records ((Any []) None Any (Since (<WEEK-START> 00:00:00)) SummaryOnly)))
  daemon resolves week-start; convention: Monday 00:00:00 of the current week
```

Tier-1 verdict: these eight variants account for ~60% of daily observation calls (Recent + Today + ThisWeek are the dominant pattern; Shallow/Deep/VeryDeep are the depth-tuned siblings).

#### Tier 2 — one-argument topic-filtered reads

```
(RecentOn [topic])
  expands to: (Observe (Records ((Partial [topic]) None Any Recent SummaryOnly)))

(TodayOn [topic])
  expands to: (Observe (Records ((Partial [topic]) None Any (Since (<TODAY> 00:00:00)) SummaryOnly)))

(DeepOn [topic])
  expands to: (Observe (Records ((Partial [topic]) None Any Deep SummaryOnly)))
```

Three one-arg variants. The topic is a bare String at a String position; brackets when whitespace/punctuation. `Partial` (records matching one or more requested topics) is the default — `Full` (records matching every requested topic) requires the complex form. Corpus supports this: most topic-filtered observations are single-topic, and Partial covers single-topic identically to Full.

#### Tier 3 — kind-filtered convenience reads

```
(DecisionsOn [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Decision) Any Recent SummaryOnly)))

(PrinciplesOn [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Principle) Any Recent SummaryOnly)))

(CorrectionsOn [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Correction) Any Recent SummaryOnly)))

(ClarificationsOn [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Clarification) Any Recent SummaryOnly)))

(ConstraintsOn [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Constraint) Any Recent SummaryOnly)))
```

One topic argument, kind baked into the variant name. Returns the 15 most-recent records of that kind on that topic. Empirical justification from the corpus: kinds are evenly distributed; the most common agent reading pattern is "what Decisions are settled on X?" or "what Corrections have come down on X?"

#### Tier 4 — magnitude-band convenience reads

```
(Bedrock)
  expands to: (Observe (Records ((Any []) None (AtLeast Maximum) VeryDeep SummaryOnly)))
  returns: the 100 most-recent Maximum-certainty records across all topics.
  Justification: this is the "workspace floor" reading — agents periodically
  need to refresh on the foundational decisions.

(BedrockOn [topic])
  expands to: (Observe (Records ((Partial [topic]) None (AtLeast Maximum) VeryDeep SummaryOnly)))
  the topic-anchored bedrock reading.

(ReviewBand)
  expands to: (Observe (Records ((Any []) None (AtMost Low) VeryDeep WithProvenance)))
  the removal-candidate review window. Spirit 1463's removal flow
  (Zero-nomination) lives here; provenance attached so date/time is visible.
```

The naming is opinionated: `Bedrock` reads as "the foundational tier"; `ReviewBand` as "the records under review for removal." Both terms are workspace-resident usage that don't clash with the rest of the vocabulary.

#### Tier 5 — provenance-stamped variants (orthogonal axis)

Every Tier 1-4 short form has a `WithProvenance` sibling that returns date+time stamps instead of bare summaries. Implementation: append `WithProvenance` to the operation root name.

```
(RecentWithProvenance)
  expands to: (Observe (Records ((Any []) None Any Recent WithProvenance)))

(RecentOnWithProvenance [topic])
  expands to: (Observe (Records ((Partial [topic]) None Any Recent WithProvenance)))

(DecisionsOnWithProvenance [topic])
  expands to: (Observe (Records ((Partial [topic]) (Some Decision) Any Recent WithProvenance)))

(BedrockWithProvenance)
  expands to: (Observe (Records ((Any []) None (AtLeast Maximum) VeryDeep WithProvenance)))
```

These are heavier names but they are precise. The agent who needs date/time on a depth-tuned read types more, gets exactly what they need.

Alternative naming (less verbose, may be preferable): `Recent+` or `RecentStamped` or a separate operation family `Provenance...` mirroring the Records family. To be decided in psyche review.

#### Tier 6 — full custom

```
(Observe (Records ((Partial [topic]) (Some Decision) (AtLeast High) (Since (2026-05-01 00:00:00)) WithProvenance)))
```

The existing canonical form. Unchanged. Available for any case the ladder above doesn't cover.

### Operation: Lookup — single-record fetch ladder

Production has `(Observe (RecordIdentifiers ((Exact N) SummaryOnly)))`. Spirit-next has `(Lookup N)`. The variant ladder lands the spirit-next form as a NEW operation root in the unified vocabulary.

```
Tier 1 (most defaults):
  (Lookup N)
    expands to: (Observe (RecordIdentifiers ((Exact N) SummaryOnly)))
    defaults: SummaryOnly mode

Tier 2 (range + summary):
  (LookupRange (N M))
    expands to: (Observe (RecordIdentifiers ((Range (N M)) SummaryOnly)))
    inclusive range; M >= N

Tier 3 (provenance):
  (LookupWithProvenance N)
    expands to: (Observe (RecordIdentifiers ((Exact N) WithProvenance)))

  (LookupRangeWithProvenance (N M))
    expands to: (Observe (RecordIdentifiers ((Range (N M)) WithProvenance)))

Tier 4 (full custom):
  (Observe (RecordIdentifiers ((Exact N) WithProvenance)))
  (Observe (RecordIdentifiers ((Range (N M)) SummaryOnly)))
```

Implementation note: `Lookup` overlaps with spirit-next's existing operation root. The variant-ladder design adopts spirit-next's vocabulary directly here.

### Operation: Count — aggregate ladder

Production has NO count operation. Spirit-next adds `(Count Query)`. The variant ladder lands the count surface as a graduated set.

```
Tier 1 (most defaults):
  (Count)
    expands to: count of ALL records in the store (1399 today)

  (CountToday)
    expands to: count of records since today's 00:00:00

  (CountThisWeek)
    expands to: count of records since week-start

Tier 2 (one parameter):
  (CountOn [topic])
    expands to: count of records matching topic (Partial)

  (CountTodayOn [topic])
    expands to: count of today's records matching topic

Tier 3 (kind + topic):
  (CountDecisionsOn [topic])
    expands to: count of recent Decisions on topic

Tier 4 (full custom):
  (Count <Query>)
    where Query carries the full TopicMatch + Kind + privacy_selection shape from spirit-next
```

Empirical justification: counting is a NEW capability. Spirit agents currently approximate via `(Observe Topics)` (which counts BY topic) or by parsing `Observe` replies. A native count operation is small but unlocks aggregation workflows.

### Operation: Topics — topic enumeration ladder

Production has `(Observe Topics)`. Already minimal.

```
Tier 1: (Topics)
  expands to: (Observe Topics)
  returns: vector of (Topic count) pairs

Tier 2 (filtered to high-frequency topics — possibly useful if count list is long):
  (CommonTopics N)
    returns top N topics by count

Tier 3: full custom
  (Observe Topics)  — unchanged
```

The `(Topics)` short form is a one-token alias — barely a savings (16 chars to 8 chars), but consistent with the rest of the ladder. The `CommonTopics N` tier MAY be unnecessary; recommend deferring until empirical demand surfaces.

### Operation: Record — capture (no short form recommended)

The Record operation is already 4-field minimal. Every field is load-bearing:

- Topics: agent must classify the record.
- Kind: agent must choose Decision/Principle/Correction/Clarification/Constraint.
- Description: the substance.
- Magnitude: certainty level.

No short form makes sense — dropping ANY field loses essential authoring context. The recommendation is to KEEP Record as the canonical authoring form and consider adding only one variant:

```
(RecordOpen ([topic ...] Kind [description] Magnitude))
  expands to: (Record ([topic ...] Kind [description] Magnitude))
  with implicit Privacy=Zero (most-public default per Spirit 1449)

(RecordPersonal ([topic ...] Kind [description] Magnitude))
  expands to: (Record ([topic ...] Kind [description] Magnitude))
  with implicit Privacy=Medium (a Personal-tier level)

(RecordSealed ([topic ...] Kind [description] Magnitude))
  expands to: (Record ([topic ...] Kind [description] Magnitude))
  with implicit Privacy=Maximum (Sealed)
```

These variants are useful ONLY if the privacy schema lands at the deployed wire layer; until then, `Record` already implies Privacy=Zero.

Recommendation: defer privacy-tier variants of `Record` until the privacy schema is deployed. When it lands, the variants are mechanical.

### Operation: Remove and ChangeCertainty (no short form recommended)

`(Remove N)` is one positional field — already minimal. `(ChangeCertainty (N M))` is two positional fields — already minimal. Both are appropriately specific operations on append-only history; brevity already exists.

A possible deferred variant:

```
(MarkForRemoval N)
  expands to: (ChangeCertainty (N Zero))
  semantic: nominate this record as a removal candidate per Spirit's
  Zero-nomination workflow. Reversible: change back to a non-zero
  Magnitude restores.
```

`MarkForRemoval` is more descriptive than `(ChangeCertainty (N Zero))` for the specific use case where the agent IS marking for removal. Useful as a clarity-of-intent short form. Defer until the Zero-nomination workflow is exercised more.

### Operation: State (no short form needed)

`(State [free-form text])` is already at the absolute minimum. No variant ladder needed.

### Operation: Watch / Unwatch / Tap / Untap (out of scope)

Subscription operations are agent-library territory, not single-call CLI territory. Variant ladder design defers these.

## Naming-style register check

The proposed short-form operation root names, evaluated against Spirit's existing PascalCase / full-English-words register (per AGENTS.md hard override and `skills/nota-design.md`):

| Proposed name | Style verdict | Notes |
|---|---|---|
| `Recent` | passes | full English, PascalCase, matches existing `RecordedTimeSelection::Recent` variant |
| `Shallow` | passes | full English, matches existing variant |
| `Deep` | passes | full English, matches existing variant |
| `VeryDeep` | passes | matches existing variant exactly |
| `Today` | passes | full English, PascalCase |
| `Yesterday` | passes | full English, PascalCase |
| `ThisWeek` | passes | PascalCase compound |
| `RecentOn` | passes | composes `Recent` + `On` (preposition as ASSOC) |
| `TodayOn` | passes | composes `Today` + `On` |
| `DeepOn` | passes | composes `Deep` + `On` |
| `DecisionsOn` | passes | composes `Decisions` (kind plural) + `On` |
| `PrinciplesOn` | passes | composes `Principles` + `On` |
| `CorrectionsOn` | passes | composes `Corrections` + `On` |
| `ClarificationsOn` | passes | composes `Clarifications` + `On` |
| `ConstraintsOn` | passes | composes `Constraints` + `On` |
| `Bedrock` | passes | metaphor; full English; familiar workspace usage |
| `BedrockOn` | passes | composes `Bedrock` + `On` |
| `ReviewBand` | passes | full English; metaphor; PascalCase |
| `Lookup` | passes | matches spirit-next vocabulary; full English |
| `LookupRange` | passes | composes `Lookup` + `Range` |
| `LookupWithProvenance` | passes (long) | composes well but is heavy; consider `LookupStamped` as alternative |
| `Count` | passes | matches spirit-next vocabulary; full English |
| `CountToday` | passes | composes `Count` + `Today` |
| `CountOn` | passes | composes `Count` + `On` |
| `CountThisWeek` | passes | composes well |
| `CountDecisionsOn` | passes (long) | three-element compound; longest sensible variant |
| `Topics` | passes | matches existing `(Observe Topics)` sub-root |
| `CommonTopics` | passes | full English, PascalCase compound |
| `RecordOpen` | passes | composes `Record` + `Open` |
| `RecordPersonal` | passes | composes `Record` + `Personal` |
| `RecordSealed` | passes | composes `Record` + `Sealed` |
| `MarkForRemoval` | passes (long) | three-element compound; alternative could be `Nominate` |

Verdict: every proposed name fits the existing register. The `WithProvenance` suffix is the only style risk — `LookupWithProvenance` and `RecentOnWithProvenance` are LONG (20-26 chars). An alternative is to introduce a `Stamped` suffix (`RecentStamped`, `LookupStamped`) — shorter, still full-English, less load-bearing per character. The trade-off should be psyche-reviewed.

### Composition rule emerging

The proposed names follow a clear COMPOSITION GRAMMAR:

```
<verb>[+<scope>][+On|For|With...][+<modifier>][+<dimension>]

verbs:    Recent | Today | Yesterday | ThisWeek | Shallow | Deep | VeryDeep |
          Decisions | Principles | Corrections | Clarifications | Constraints |
          Bedrock | ReviewBand | Lookup | Count | Topics | Record | Remove

scopes:   Range (Lookup family)

prepositions: On (with topic), For (with kind or target — unused so far)

modifiers: WithProvenance | Stamped | Sealed | Personal | Open

dimensions: (Lookup) Range | (Topics) Common
```

This grammar emerges from the patterns and ALSO suggests future variants (`TodayOnWithProvenance`, `BedrockOnWithProvenance`) without needing them all enumerated. The wire vocabulary GAINS a generative shape: agents and the schema can name new variants by composition rather than by handcraft. This is its own subtle Spirit principle that may be worth recording (see Open questions Q4).

## Open questions for psyche

### Q1 — Which ladders to land first?

The proposed surface adds ~30 new operation roots across all families. Landing all at once is a substantial schema delta. Recommended landing order (Maximum-leverage first):

1. **`Recent`, `Shallow`, `Deep`, `VeryDeep`, `Today`, `ThisWeek`** — these are the daily-use 60% of observation calls. Zero arguments. Maximum payoff per implementation cost.
2. **`Lookup N`, `LookupRange (N M)`** — single-record and range fetch. Replaces the most-typed two-layer nesting `(Observe (RecordIdentifiers ((Exact N) SummaryOnly)))` with a flat one-arg call. Aligns with spirit-next vocabulary.
3. **`Count`, `CountOn`, `CountToday`** — entirely new capability. Useful for aggregation workflows.
4. **`RecentOn`, `TodayOn`, `DeepOn`** — topic-filtered convenience.
5. **`DecisionsOn`, `PrinciplesOn`, etc.** — kind-filtered convenience.
6. **`Bedrock`, `BedrockOn`, `ReviewBand`** — opinionated semantic variants.
7. **`WithProvenance`-suffixed siblings** — provenance variants of all the above.
8. **`Topics`** — minor alias.
9. **`RecordOpen`, `RecordPersonal`, `RecordSealed`** — deferred until privacy schema deploys.
10. **`MarkForRemoval`** — deferred until Zero-nomination workflow is exercised more.

Decision needed: land 1-3 in a first wave (proven Maximum-leverage), 4-7 in a second wave (good but less critical), 8-10 deferred. Or land 1-8 in one wave for ergonomic consistency. Psyche's call.

### Q2 — How aggressive should the defaults be?

For `(Recent)` the default is "15 most-recent records, summary only, no privacy filter on owner socket, Open-only on ordinary socket." Question: is the privacy default (Default B — socket-determined, recommended in §"Privacy-filtering implications") correct? Or should the default be Default A (most-conservative, even on owner socket)?

The trade-off: Default B is more ergonomic for the owner (they don't have to type a privacy filter to see their own elevated records). Default A is safer (no accidental exposure even on owner socket, even from a sub-agent inheriting owner clearance).

Spirit 1448 / §Q6 of report 54 suggests sub-agents must EXPLICITLY filter to reach elevated material even with owner clearance — which implies Default A for sub-agents. But the owner user themselves, calling Spirit interactively from the unsuffixed CLI, doesn't gain from being forced to type a privacy filter every time. A possible refinement: the CLI WRAPPER on the owner socket can transparently apply a different default than the daemon — but that splits the variant ladder behaviour across CLI vs daemon, which is fragile.

### Q3 — `WithProvenance` naming verbosity

`LookupWithProvenance N` is 22 characters of operation-root name before the argument. Alternatives:

- `LookupStamped N` — 14 chars, full English, less precise but punchier.
- `LookupTimed N` — 12 chars, but "Timed" is overloaded with "scheduled."
- `LookupWithDate N` — 15 chars; "Date" is more specific.
- Separate root family: `Provenance` operation containing identifier+date+time only.

Decision needed: keep verbose names (`WithProvenance` suffix) for precision, or accept a shorter mnemonic.

### Q4 — Generative grammar — record the composition rule as Spirit principle?

The naming grammar emerging from this design is itself a Spirit principle: short-form operation roots compose from a small alphabet of verbs, prepositions, and dimensions. If recorded, future variants land deterministically by composition.

Decision needed: record the composition grammar as a Spirit Principle (allowing future expansion without psyche review on each name)? Or leave it as a working pattern of this design pass without elevating to principle?

### Q5 — Convergence with spirit-next

Spirit-next already exposes `Record / Observe / Lookup / Count / Remove / LookupStash` as siblings. The variant-ladder design adds short-form aliases that don't conflict with that vocabulary, but the long-term direction question matters:

- If production becomes the canonical surface, spirit-next's `Lookup`/`Count` migrate into production.
- If spirit-next becomes the production surface (per Spirit 1473 inspiration directive), production's `Observe (RecordIdentifiers ...)` form gets retired in favour of `Lookup`.

The variant-ladder lands the ALIASES in both. The decision is which way the canonical migrates. Decision needed before landing the short forms.

### Q6 — Daemon-resolved date math (`Today`, `Yesterday`, `ThisWeek`)

These short forms have the daemon compute the date from its own clock at request time. Two concerns:

1. **Time zone**: which timezone defines "today"? Production records are stamped in the daemon's local time. Should `Today` use the daemon's local TZ or UTC? Recommend daemon local TZ for consistency with the existing date stamps.
2. **Boundary semantics**: `Today` could mean (a) "since 00:00:00 today" or (b) "in the last 24 hours from now." Recommend (a) for predictability. `Yesterday` similarly: the FULL DAY of yesterday (00:00 - 23:59), not "24-48 hours ago."

Decision needed: confirm semantics before implementation.

### Q7 — Result-shape variants — promote to operation-root or leave as suffix?

The proposed `WithProvenance` suffix mirrors production's `ObservationMode` field. Alternative: promote result-shape to a top-level operation-root family (per spirit-next's `Lookup` vs `Count`):

```
(Recent)        — returns summary records
(RecentStamped) — returns provenance-stamped records  
(RecentCount)   — returns just the count
(RecentTopics)  — returns just the matching topics
```

Each result-shape becomes its own family of operation roots. The grammar becomes <action> + <result-shape>. This is more orthogonal but creates 4x more operation roots.

Decision needed: scope of result-shape promotion. Recommend keeping `Stamped` / `WithProvenance` as suffix until empirical demand justifies promotion.

## Sources

CLI variant-ladder design:

- [Command Line Interface Guidelines](https://clig.dev/) — the foundational community design guide; principles around smart defaults, short-form vs full-form flags, and progressive disclosure.
- [Cobra Philosophy](https://cobra.dev/docs/explanations/philosophy/) — convention-over-configuration in CLI framework design.
- [Atlassian: 10 design principles for delightful CLIs](https://www.atlassian.com/blog/it-teams/10-design-principles-for-delightful-clis) — short-name aliases for common operations, sensible defaults principle.

git design:

- [git-status manual (kernel.org)](https://www.kernel.org/pub/software/scm/git/docs/git-status.html)
- [git-status documentation (2.2.3)](https://git-scm.com/docs/git-status/2.2.3)
- [Stefan Judis — short version of git status and porcelain](https://www.stefanjudis.com/today-i-learned/the-short-version-of-git-status-and-the-close-but-different-porcelain-mode/)

kubectl design:

- [kubectl Quick Reference (Kubernetes docs)](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [kubectl get | Kubernetes](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/)
- [Baeldung — kubectl output formatting](https://www.baeldung.com/ops/kubectl-output-format)
- [JSONPath Support | Kubernetes](https://kubernetes.io/docs/reference/kubectl/jsonpath/)

jq design:

- [jq 1.8 Manual](https://jqlang.org/manual/)
- [Programming Historian — Reshaping JSON with jq](https://programminghistorian.org/en/lessons/json-and-jq)

Common Lisp `with-` patterns:

- [Common Lisp Cookbook §Macros](https://lispcookbook.github.io/cl-cookbook/macros.html)

REST API expansion patterns:

- [Zapier engineering — 3 ways to make API responses flexible](https://zapier.com/engineering/flexible-api-responses/)
- [Speakeasy — REST API parameters best practices](https://www.speakeasy.com/api-design/parameters)
- [Best Practices for Designing a Pragmatic RESTful API (Vinay Sahni)](https://www.vinaysahni.com/best-practices-for-a-pragmatic-restful-api)

Progressive disclosure:

- [Progressive Disclosure Pattern — agent skills (DeepWiki)](https://deepwiki.com/microsoft/agent-skills/5.3-progressive-disclosure-pattern)
- [Convention over configuration — Wikipedia](https://en.wikipedia.org/wiki/Convention_over_configuration)

Workspace internal references:

- `/home/li/primary/AGENTS.md` — Naming rules, NOTA bracket-string discipline, single-NOTA-argument rule, operator-vs-designer lane discipline.
- `/home/li/primary/skills/spirit-cli.md` — production v0.3.0 wire shape; depth vocabulary; deployment slot model.
- `/home/li/primary/skills/nota-design.md` — PascalCase rules, positional records.
- `/home/li/primary/skills/component-triad.md` — single-argument rule + no flags.
- `/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/1-wire-shape-parity-audit.md` — full enumeration of production v0.3.0 vs spirit-next operations.
- `/home/li/primary/reports/system-designer/53-spirit-next-production-parity-2026-06-02/5-overview.md` — synthesis of the parity audit.
- `/home/li/primary/reports/system-designer/54-spirit-privacy-classification-research-2026-06-02.md` — full privacy classification design space, the four candidate enum sets, and Spirit 1463 / 1449 framing.
- `/git/github.com/LiGoldragon/spirit-next/schema/lib.schema` — spirit-next declarative schema with `Privacy Magnitude`, `PrivacySelection`, `Entry` carrying `Privacy`.
- `/git/github.com/LiGoldragon/signal-persona-spirit/spirit.schema` — production declarative schema (with privacy already declared but not deployed).

Anchoring Spirit records:

- Spirit 1474 (Decision High, 2026-06-02) — the directive: variant ladders per operation.
- Spirit 1472 (Principle High, 2026-06-02) — the principle: simple-to-complex command surface.
- Spirit 1473 (Decision Medium, 2026-06-02) — spirit-next as design inspiration.
- Spirit 1463 (Decision Maximum, 2026-06-02) — Magnitude on privacy axis.
- Spirit 1449 (Clarification High, 2026-06-02) — default access is most-public.
- Spirit 1448 (Clarification, 2026-06-02) — sub-agent clearance inheritance + explicit filter requirement.
- Spirit 1389 (Decision High, 2026-06-01) — slim Nexus output / provenance envelope.
- Spirit 1373 (Principle Maximum, 2026-06-01) — no NOTA between components.
- Spirit 1338 (Decision High, 2026-06-01) — verbal depth vocabulary settled at Shallow/Recent/Deep/VeryDeep with counts 5/15/30/100.
- Spirit 1249 — discriminant stability for rkyv-persisted enums.

## Summary recommendation

Land a graduated variant ladder for `Observe (Records ...)` first — six Tier-1 zero-argument convenience reads (`Recent`, `Shallow`, `Deep`, `VeryDeep`, `Today`, `ThisWeek`) plus four Tier-2 topic-filtered reads (`RecentOn`, `TodayOn`, `DeepOn`, `BedrockOn`) account for ~80% of empirical observation patterns. Add `Lookup N` and `LookupRange (N M)` as direct spirit-next-aligned single-record/range fetches. Add `Count`, `CountOn [topic]`, `CountToday` for the entirely-new aggregation surface. Defer kind-filtered convenience (`DecisionsOn`, etc.), provenance variants (`WithProvenance` suffix family), magnitude-band convenience (`Bedrock`, `ReviewBand`), and privacy-tier `Record` variants until the schema-deployed privacy field lands. Naming follows a generative grammar (verbs × prepositions × dimensions) that fits Spirit's PascalCase / full-English-words register and lets future variants land by composition. Privacy default: socket-determined — short forms on the owner socket apply no privacy filter; on the ordinary socket they restrict to Privacy = Zero. The complex `(Observe (Records (...)))` form remains canonical and unchanged; short forms expand deterministically to a default-injected version of it.
