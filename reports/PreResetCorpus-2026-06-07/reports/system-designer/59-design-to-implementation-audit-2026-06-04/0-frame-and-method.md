# 59 — Design-to-implementation audit (frame + method)

Kind: meta-report directory (frame + four audit sub-agents + adversarial verify + orchestrator psyche report).
Topics: spirit, audit, design-manifestation, implementation-gap, repetition, abstraction, rust-discipline, psyche-report.
Date: 2026-06-04.
Role: system-designer (orchestrator).

## Intent Anchors

[Production Spirit should implement an explicit collect-removal-candidates operation that archives or emits reviewed Zero-certainty records before retracting them from the hot store.] (Spirit 1543 Decision Maximum)

[Spirit removal-candidate collection should support an explicit output target for archive material, such as a file path or process stream, so another component can preserve the compact valued representation before hot-store removal.] (Spirit 1544 Decision High)

[Common Spirit operations should have short default forms that lower to the full data types, so agents do not have to compose every rarely-configured field for routine calls.] (Spirit 1545 Principle High)

[Spirit defines a small-record data type carrying the core load-bearing fields — identifier, topics, kind, description summary, magnitude, daemon-stamped date and time. The small record is what variant-ladder short-form reads and CollectRemovalCandidates emit; what archiving and downstream tools consume.] (Spirit 1549 Decision High)

[Spirit gains a RecordDefault short-form recording operation taking only fields agents commonly customize — topics, kind, description, magnitude — with defaults injected for the rest. Record remains the canonical full-fidelity operation; RecordDefault is the daily-use shortcut.] (Spirit 1550 Decision High)

[When something feels ugly, slow down and find the structure that makes it beautiful — special cases collapse into the normal case; repetition resolves into a single named pattern.] (ESSENCE §"Beauty is the criterion")

[Per spirit record 944: per-repo INTENT.md and ARCHITECTURE.md are the canonical agent-context surface — manifestation of psyche intent into them is part of the work cycle, not a deferred pass.] (continuous-manifestation discipline)

## Psyche directive

The psyche directed this session at a design-to-implementation audit:
acquire intent from Spirit and design from the architecture / intent
documents, read the recent designer + operator reports, then audit —
with sub-agents — to find design (especially intent, constraints,
architecture) that is present in the guidance layer but **missing
from the implementation**, and port it. Each sub-agent gets a numbered
entry in this meta-report; the orchestrator writes a psyche report at
the end. The agents and orchestrator look for bad patterns, winded
code, and repetition — repetition signals a missing abstraction. The
psyche report carries the low-down: how everything is going, what the
psyche needs to define further or better, plus propositions,
solutions, questions, visuals, and code with full context.

### Capture-first assessment

This turn's message is a **working order** (run an audit, write
reports), not durable psyche intent. Its two arguable principles —
*repetition signals a missing abstraction* and *design must be ported
from the guidance layer into code* — are already captured: the first
in `ESSENCE.md` §"Beauty is the criterion" ([repetition resolves into
a single named pattern]), the second in the continuous-manifestation
discipline (Spirit 944). No new durable intent to record — a valid
no-capture turn per `skills/intent-log.md` §"Working orders are not
intent".

## Method

Three movements, orchestrator-in-the-loop between them:

1. **Audit fan-out (this workflow, read-only).** Four sub-agents,
   each owning a slice, each writing a numbered report into this
   directory AND returning structured findings. Each gap is
   classified by **portability**: `portable` (design decided at the
   field level AND unimplemented AND safe to land without a new psyche
   decision) versus `blocked` (needs a psyche decision before code can
   be written — e.g. the Reading A/B question, an open parameter).

2. **Adversarial verify.** Every gap a sub-agent marks `portable` is
   challenged by an independent skeptic prompted to **refute**
   portability: is it truly decided at the field level, or does it
   carry an open parameter that needs the psyche? Default to `blocked`
   on doubt. This is the fence that stops the port phase from writing
   code the psyche has not authorised (the standing override: when
   intent on a question is unclear, ask — don't infer).

3. **Port + psyche report (orchestrator).** The orchestrator reads
   the verified findings, ports the genuinely-unblocked subset onto a
   feature branch in `~/wt` (designers branch; operators integrate —
   the orchestrator does not push to main), and writes the psyche
   report as the highest-numbered file here. Blocked gaps become the
   report's decision queue.

## Audit slate

| File | Agent | Slice |
|---|---|---|
| `1-spirit-production-triad-gap.md` | A1 | `signal-persona-spirit` + `persona-spirit` + the policy leg. Map intent 1474, 1541-1550 onto current source: CollectRemovalCandidates, OutputTarget, SmallRecord, RecordDefault, variant-ladder tier-1. Per-design implemented / partial / missing + portability. |
| `2-spirit-next-schema-parity.md` | A2 | `spirit-next` (+ `triad-runtime`, `schema-rust-next` as needed). Map the schema-derived intent (three-engine traits 1326-1336, typed trace 1489-1492, help namespace 1493, config convention 1494, REST-shape, push-mail) onto current source. Is the generated CLI/client trace adapter done (INTENT.md names it the open work)? Help namespace? Config convention? |
| `3-rust-discipline-and-repetition.md` | A3 | The psyche's specific ask. `persona-spirit` + `signal-persona-spirit` + `spirit-next`: rust-discipline violations (free functions, ZST namespaces, typed-domain-values, per-crate Error, hand-rolled parsers, methods-on-nouns) AND repetition across the triad that wants a named abstraction — concrete excerpts + proposed abstraction. |
| `4-triad-shape-naming-and-manifestation-drift.md` | A4 | Triad shape (daemon + working signal + policy signal), single-argument rule, bracket-string + positional-record discipline, full-English-word naming, names-don't-carry-ancestry, AND per-repo INTENT.md/ARCHITECTURE.md currency. The `owner-signal-persona-spirit` → `meta-signal-persona-spirit` rename gap is one concrete instance. |

## Source baseline (2026-06-04)

- `signal-persona-spirit` @ `a69769b` (origin/main) — removal-candidate collection landed.
- `persona-spirit` @ `7233075` (origin/main) — collect-removal-candidates handler landed.
- policy leg checked out as `owner-signal-persona-spirit` — the `meta-signal-persona-spirit` rename (primary commit c1b7f17d, operator report 300) has not reached this checkout.
- `spirit-next` local main `f95d74a` is ahead of origin/main `8461d37` (unpushed operator commits present locally).

## Lane coordination

Reports under `reports/system-designer/` are this lane's. Sub-agents
inherit the system-designer lane (Spirit 920 inheritance). The
parallel operator-lane work on this exact thread lives at
`reports/system-operator/189-production-spirit-collect-removal-candidates-2026-06-03/`
and `reports/system-operator/190-spirit-removal-candidate-open-problems-psyche-report-2026-06-03.md`;
this directory is the designer-side audit, cross-referenced not
duplicated. Per the designer/operator branch split: designer ports
onto feature branches in `~/wt`; operator owns main + integration.
