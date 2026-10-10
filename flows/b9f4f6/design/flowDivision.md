# Dividing the flow model by thinking task — three frameworks

Design document, flow b9f4f6, 2026-09-02. Proposal for the psyche;
nothing here is ruled. Evidence is in this flow's reports
(reports/reasoningTraceOntologies.md, reports/cognitiveArchitecture
Ontologies.md, reports/flowCompositionOntologies.md, reports/
psycheRecords.md); every external claim below is traceable to a URL
there. Flow readings are marked as such.

## Ground already standing (psyche records)

- A flow is one bounded LLM context; a subflow is also a flow; a flow
  running a subflow is still active through its subflows; subflows
  use their parent's lane. Athena is composed through the internal
  dialogue of flows.
- Ruled: a phase is its own flow, with its own top stratum. Adopted:
  the terminology abduce / deduce / induce.
- Drafting, not ruled: different top stratums for different jobs;
  deciding-whether and acting as separate jobs.
- Notion: types × phases, some re-used; three phases a guideline.
- The general machine is three parts, fractal: agglomerate multiple
  types → create a coherent type → convert it to another type.
- Difficulty tiers read/write × trivial/ordinary/demanding/critical
  grade the difficulty of getting it right, not the consequence of
  error.
- The manager's context is gold; the manager keeps its hands clean;
  children escalate.
- A claim is relayed as a claim; a thing is verified only by a
  witness.

## What "bleeding edge" turned out to mean

Three lineages are alive in 2025–2026 work, and they cut the thinking
along three different lines. No unified ontology of thinking for AI
exists (the cognitive-architecture report, §12f): benchmark taxonomies
use one cut, metacognition research another, agent-architecture
practice a third, and they do not cite each other. The three
frameworks below are those three cuts, each made coherent on its own
terms.

## Framework 1 — by inference office: abduce / deduce / induce

**Principle of division.** What the thinking does to a claim.
Abduction proposes an explanation or a plan; deduction draws out what
must follow if it holds; induction tests the consequences against the
thing itself. Peirce's cut; the psyche's adopted terminology.

**The flows.** Three flows, one per office, each with its own top
stratum: the abductive flow is programmed to generate and select
among hypotheses (economy of research: which guess is cheapest to
test); the deductive flow to derive consequences without inventing
new content; the inductive flow to run the test and report surprise
or fit.

**What crosses.** Abduce → deduce: a hypothesis, stated as a
hypothesis. Deduce → induce: predictions, each one checkable. Induce →
abduce: a verdict, and the surprise that seeds the next round. Each
crossing is the "coherent type" of the three-part machine; the
receiving flow agglomerates it with its own inputs.

**Composition.** A cycle in time (Peirce's methodeutic): the phases
are siblings in sequence, and the cycle repeats until the inductive
verdict stops it. Fractal: Peirce gives every inference three inner
steps (colligation, observation, judgment), which is the three-part
machine again inside each flow.

**Evidence for.** Deductive, inductive, and abductive competence are
empirically dissociable in LLMs — strong deduction does not predict
strong abduction (2025 abductive-reasoning survey; LogiGLUE,
Multi-LogiEval). Reasoning traces show a constructive → evaluative
phase shift that is detectable and exploitable (TRACES 2026; the
commitment-boundary paper 2026: everything after commitment is
epiphenomenal, up to 55% of the trace). ReasonOps 2026 finds
hypothesizing regularly precedes inferring, a generate-and-test
schema, and that deduction dominates traces (ReasoningFlow: 41% of
edges) while induction is rare — the offices are unequally exercised
when left in one flow.

**Evidence against, and unknowns.** No paper tests whether putting
the offices in separate calls beats interleaving them in one call at
equal compute (the trace report, closing section). ReasonOps shows
reflective operators help on hard problems and harm on easy ones —
so a fixed three-flow cycle over-thinks the trivial. The multi-agent
scaling study (Anthropic, Dec 2025) finds sequential coordination
costs up to −70% while decomposable parallel work gains up to +80%;
the abduce → deduce → induce pipeline is sequential coordination and
must earn its cost by what crosses being a coherent type, not a lossy
summary (the data-processing-inequality argument, Tran & Kiela 2025).

## Framework 2 — by level: reflective / algorithmic / autonomous

**Principle of division.** Who decides what thinking is needed,
versus who does it. Stanovich's tripartite mind, sharpened by
Nelson–Narens monitoring/control and resource-rational metareasoning.
The reflective level detects that the default will not do, chooses
the kind and amount of thinking, and stops it; the algorithmic level
does the chosen thinking; the autonomous level answers without
deliberating.

**The flows.** The reflective flow holds no object work: it reads the
task, estimates difficulty, picks the kind (framework 1) and the tier,
sets the budget, dispatches, and reads the monitoring signal that
comes back. The algorithmic flows are the existing tiers: ordinary,
demanding, critical. The autonomous flow is the trivial tier — fetch
or apply, no deliberation.

**What crosses.** Downward: the brief, carrying kind, tier, and
budget, and nothing the child does not need. Upward: the result, and
a monitoring signal separate from it — confidence, unknowns, "reading
cannot settle it", "the tier was wrong". The reflective flow acts on
the signal (expand, prune, repair, stop, abstain — CoT2-Meta's five
controls); the algorithmic flow never re-tiers itself.

**Composition.** A two-level loop, monitor up and control down; the
reflective flow is the parent of every flow it tiers. Recursion:
an algorithmic flow that dispatches becomes reflective toward its own
children — the manager's context is gold at every level.

**Evidence for.** TRIAGE 2025 is the strongest single finding across
the three reports: extended reasoning improves accuracy but degrades
the model's control of its own budget — "binding the budget breaks
triage" for nearly every model. MIRROR 2025: models monitor above
chance but fail to act on their monitoring (the knowing-doing gap);
external architectural constraint cuts confident failure by 76% while
showing the model its own calibration does nothing. Cognitive
Foundations 2025 (192,000 traces, 18 models): models possess
meta-cognitive controls but do not deploy them spontaneously; external
guidance gains up to 66.7% on complex problems. "When More Thinking
Hurts" 2026: the negative flip, extended thinking harmful past ~7K
tokens on easy problems. Rational metareasoning (Griffiths et al.
2024): value-of-computation allocation cuts tokens 23–42% at equal
accuracy, with the savings on easy problems. Difficulty is readable
before solving (hidden-state probes 2025; routers >2× cost cut at
<1% loss). Structural-alignment bias (ACL 2026): tools in context
drive invocation of irrelevant tools 42–90% of the time — the
deciding-whether judgment is contaminated by the ability to act,
which is the psyche's own observation of 2026-08-30.

**Evidence against, and unknowns.** Whether the knowing-doing gap is
fundamental to the architecture or an artefact of training is
unknown. Difficulty estimation is crude and tested mainly on
benchmarked domains; on genuinely novel tasks it is untested. No
working configurator (LeCun) exists; the reflective flow is a design
we would build, not one we can copy.

## Framework 3 — by stance: maker / witness / reviewer

**Principle of division.** A flow's relation to the product being
judged: its own, or another's. The maker produces the artifact and a
claim about it. The witness observes the thing itself — runs the
test, the probe, reads the code — and reports what was observed,
not what was claimed. The reviewer reads the maker's claim and the
witness's observation and rules. The maker never witnesses its own
product. This is the generator–verifier lineage, and it is the
psyche's own claim/witness distinction made into flows.

**The flows.** Maker (any flow that produces), witness (a flow whose
top stratum permits observation only and forbids repair), reviewer
(a flow that rules on claim plus observation and returns accept /
reject / where it is wrong).

**What crosses.** Maker → witness: the artifact and the claim, and
the claim is labelled as another's. Witness → reviewer: the
observation, with what could not be observed left unknown. Reviewer
→ maker (or the parent): verdict and error location — location, not
just verdict, because localization is the proven bottleneck.

**Composition.** A gated loop (evaluator–optimizer) or a pipeline
with a gate; the stance of each flow is fixed by its top stratum, so
the same flow cannot drift from maker into checker.

**Evidence for.** The Self-Correction Illusion 2026 (ten models):
models correct byte-identical errors at a median 17% when the error
is in their own thought and at +53 points when the same content is
relabelled as external; role tag alone accounts for ~30 points.
Self-Refine, Reflexion, and Chain-of-Verification give negative or
small lifts. Maker–checker 2026: self-approval causes grade drift
without quality gain; 70% of production loops verify
deterministically rather than by LLM review — the witness, not the
reviewer, carries the load. Error localization, not correction, is
the bottleneck (2023, replicated). Aider architect/editor: +23.9
points from splitting proposer and applier across two calls. The
generation–verification gap (ICLR 2026): separate verification helps
most at medium difficulty; strong generators make errors weak
verifiers cannot see.

**Evidence against, and unknowns.** In Tree-of-Thoughts the generator
matters more than the discriminator — investing in checkers over
makers has limits. Same-model debate is illusory consensus (up to 72%
of facts erased; conformity strengthens with rounds): the witness must
observe the thing, not argue with the maker. Whether training-time
verification survives the role-label effect is unknown.

## How the three relate in flow-flows

They are three orthogonal cuts, and a flow-flow is where all three
appear at once. Each cut answers a different question, and each lives
on a different edge of the tree:

- **Level (framework 2) is the vertical cut.** Every parent–child
  edge is a level boundary: the parent is reflective toward its
  children, the child algorithmic or autonomous toward its task. The
  tiers are the object-level gradient the parent chooses from.
- **Office (framework 1) is the temporal cut among siblings.** The
  parent sequences abductive, deductive, and inductive children; each
  phase is its own flow with its own top stratum, as ruled. The
  parent holds the cycle; no child holds more than one office.
- **Stance (framework 3) is the identity cut among siblings.** The
  flow that made a thing is never the flow that witnesses it. This is
  the reason framework 1's phases must be separate flows rather than
  stretches of one: the inductive flow witnessing the abductive
  flow's guess is exactly the external-relabelling that restores
  correction.

The three-part machine is not a fourth cut; it is the shape of every
flow whatever its cut — agglomerate the inputs, form the coherent
type, convert it for the receiver — and the coherent type is what
crosses each boundary.

Fractal: a child that dispatches is a flow-flow in its own right and
reproduces all three cuts one level down. So "types × phases, some
re-used" (the notion) reads as: the offices are the phases; the levels
and stances are the types; the same office recurs at every level.

A worked example, this flow read through the three cuts: this parent
was reflective (it tiered five children: two read-ordinary, three
read-demanding) and did no object work; the children were makers of
reports, and the parent consumed their reports as claims; the flow
that witnessed ceb3b9fd's transcript was a different flow from the
one that summarised it. What is missing here, and would be present in
a realization flow-flow: an inductive child that witnesses a maker's
output, and a reviewer distinct from the parent.

## Where the divisions land on what exists

- The aspects (design, realization, investigation, steward) are
  names for continuity, not cuts; they say what a flow is about, not
  which office, level, or stance it holds. A design flow-flow and a
  realization flow-flow both contain all three cuts.
- The tiers are framework 2's object-level gradient and stay as they
  are. One conflict to settle: the deployed read-critical line is "A
  missed detail changes the conclusion.", which the psyche called
  "really bad" on 2026-08-19; the approved line was "Reading cannot
  settle it. A probe must be designed and run." (reports/
  psycheRecords.md §4c). No record resolves it.
- "Deciding whether" now splits into three different yes/no's: the
  reflective flow decides whether and how much to think; the
  abductive flow decides what to propose; the reviewer decides
  whether the proposal stands. The psyche's 2026-08-30 draft
  ("deciding-whether, then mutable action") is closest to the first.

## Anatomy questions for the psyche

1. Are the three cuts to stand together, as proposed, or is one of
   them the division and the others features of it?
2. Which yes/no did "deciding whether" mean on 2026-08-30 — the
   reflective (should we think, how much), the abductive (what to
   propose), or the reviewer's (does it stand)?
3. The witness: is it a flow with a top stratum that forbids repair,
   or a tool run (a test, a probe) that a reviewer flow invokes?
4. What is the smallest flow-flow — is a trivial task allowed to be
   a single autonomous flow with no office cycle and no witness?

## Intent candidates

Two lines look broader than any topic; each would guide many
decisions. Should either be Intent?

- The flow that decides how to think never does the thinking.
- The flow that made a thing never witnesses it.
