# Peirce's system in a specialized-harness system

Design sketch, flow b9f4f6, 2026-09-02. Proposal for the psyche;
nothing here is ruled.

Origin of every part is marked:
- [Peirce] — Peirce's own division, as relayed by ceb3b9fd's
  lineage-depth subflow (sourced there from the Stanford
  Encyclopedia, the Internet Encyclopedia of Philosophy, and the
  Commens companion; some primary papers paywalled). Not witnessed
  by this flow.
- [psyche] — the psyche's records, path given.
- [research] — this flow's reports; paper named; numbers witnessed
  at source in reports/numbersWitness.md unless said otherwise.
- [composition] — this flow's own design inference.

## The harness this is drawn in [psyche]

- The Flow Nexus "sets up and starts a model flow: its working
  directory, system prompt, training files and instruction prompt"
  (Vision/flowNexus.md). The basic skills replace the prompt the
  harnesses build in.
- "every session gets its own authored top layer carrying its skills,
  standards, and main goal; the middle layer is everything typed
  afterward; tool calls carry no authoritative information inward;
  the built-in sub-agent tool is disabled in favor of a tool that
  asks the meta harness for another session — hierarchy optional,
  siblings possible" (vision-raw/gradientsOfAuthority.md,
  2026-08-10, the record's own summary of the dictated statement).
- "Top stratum is where we want universal invariants"
  (flows/7c3f0c1d/vision/gradientsOfAuthority.md, 2026-08-19).
- "a phase is its own flow, with its own top stratum"
  (flows/ceb3b9fd/vision/topStratum.md, 2026-08-30).
- The three-part machine: agglomerate multiple types → create a
  coherent type → convert it to another type; fractal
  (vision-raw/machineAnatomy.md, 2026-08-21).

So a specialized-harness system, in the psyche's own terms: the Nexus
starts each flow with a top layer authored for its job; a flow that
needs another flow asks the Nexus, and the new flow's top layer is
its own, not inherited.

## The shape [composition]

One inquiry is a flow-flow: a parent flow holding Peirce's methodeutic
[Peirce: the branch of his logic for how the three inferences chain
into inquiry], and three office flows the parent asks the Nexus for,
one office each. Each office flow has a top stratum authored for its
office; the universal invariants are the same in all three; the
office program differs.

    surprise C ──▶ ABDUCE ──hypotheses──▶ parent picks one
                                              │
                    ┌─────────────────────────┘
                    ▼
                 DEDUCE ──artifact + predictions──▶ INDUCE
                    ▲                                 │
                    └──── verdicts, where it failed, ──┘
                          new surprise C' → parent → ABDUCE again,
                          or stop

What crosses each boundary is a coherent type, converted for its
receiver: Surprise, Hypothesis, Prediction, Verdict. In the end shape
these are the Nexus's signals (nexus-rationale: binary signal is the
end shape, text a shim).

## The three office flows

Every inference has three inner steps — colligation (bring the
relevant propositions together), observation (contemplate what is
assembled), judgment (accept what it compels) [Peirce]. These are
the three-part machine inside each office flow [composition]:
colligation agglomerates, observation forms the coherent type,
judgment converts it into what the office emits.

### Abduce flow — the office that proposes

- **For** [Peirce]: "The surprising fact C is observed; but if A
  were true, C would be a matter of course; hence there is reason to
  suspect A is true." Its selection step is the economy of research:
  rank hypotheses by cost to test, intrinsic value, and effect on
  other inquiries. No "best explanation" anywhere in Peirce; the
  output is a license to conjecture, not knowledge (Gabbay & Woods).
- **Top stratum program** [composition]: the invariants; then: you
  are handed a surprise and the records; produce hypotheses, several,
  each in canonical form, ranked by economy; you do not decide which
  is true; you do not act on the world. Tools: read, search, write
  only under the flow's design directory. No mutation tools.
  Reason [research]: tools present in context drive irrelevant
  invocation 41.9–90.4% (ACL 2026, witnessed); the psyche's own
  observation that deciding-whether is confused by the ability to act
  (2026-08-30). Reason [Peirce lineage]: the collapse of abduction
  into "inference to the best explanation" merged generating with
  judging — the first mixture to forbid.
- **Middle (the brief)**: the surprise C stated as a surprise; where
  the records are; the grade wanted.
- **Emits**: Hypotheses — a ranked list, each with its cost to test.
- **Grades** [Eco, successor of Peirce] → tiers [composition]:
  overcoded (one known rule fits: trivial), undercoded (choose among
  known rules: ordinary, demanding), creative (invent the rule:
  critical).

### Deduce flow — the office that derives

- **For** [Peirce]: from a hypothesis taken as premise, derive what
  must follow. Two modes: corollarial (the conclusion is seen at once
  in the premisses) and theorematic (one must first experiment in
  the imagination — construct something — before the conclusion
  appears); Peirce called this distinction one of his most important
  discoveries. Most secure, least fertile.
- **Top stratum program** [composition]: the invariants; then: you
  are handed one hypothesis as premise; realize what follows from it
  and state, as predictions, what must be observable if it holds;
  you do not invent a new hypothesis — if the premise cannot be
  realized, return that as a finding; you do not witness your own
  product. Tools: read and write in the tree; run only for building,
  not for judging.
  Reason [research]: the architect/editor split (+23.9 points, Aider,
  relayed from the composition report, not witnessed at source);
  Claude Code's plan mode strips write tools from the proposing
  pass (relayed).
- **Middle (the brief)**: the chosen Hypothesis; the tier.
- **Emits**: the Artifact, and Predictions — each one a sentence
  naming what an observer must see, so the induce flow can check it
  without reading the deduce flow's mind.
- **Modes** [Peirce] → tiers [composition]: corollarial (the change is
  fully specified, or the approach is known: trivial, ordinary);
  theorematic (a construction is needed first: demanding, critical).

A composition to rule on: this reads realization as deduction — the
code is what follows from the design, and its tests are the
predictions. Peirce's deduction is a derivation, not an act; treating
the built artifact as the derived consequence is this flow's move.

### Induce flow — the office that tests

- **For** [Peirce]: test the predictions against experience; three
  grades by increasing security: crude ("all observed As were B"),
  qualitative (testing a hypothesis's predictions), quantitative
  (statistical sampling). Justified by one property: induction
  self-corrects in the long run.
- **Top stratum program** [composition]: the invariants; then: you
  are handed predictions and an artifact you did not make; observe
  the thing itself; report each prediction as held, failed (and
  where), or unobservable; report every surprise; you do not repair;
  you do not propose. Tools: run, probe, read; no edit in the tree
  (a scratch clone if a probe needs one).
  Reason [research]: a model corrects its own errors at 16.7% and
  the same errors at +53.3 points when they arrive as another's
  (witnessed); error localization, not correction, is the bottleneck
  (relayed); observation of the thing itself is the psyche's witness
  (vocabulary; behavior skill).
- **Middle (the brief)**: the Predictions; the Artifact's location;
  the grade wanted.
- **Emits**: Verdicts, one per prediction, with location of failure;
  and the new Surprise C', if any.
- **Grades** [Peirce] → tiers [composition]: crude (it ran, it reads
  right: trivial), qualitative (each prediction tested: ordinary,
  demanding), quantitative (sampled, repeated, property-tested:
  critical).

## The parent — methodeutic

- **For** [Peirce]: how the three chain into inquiry; the late axis
  of security against uberty — deduction most secure and least
  fertile, abduction most fertile and least secure, induction
  between.
- **Top stratum program** [composition]: main-flow as it stands, plus:
  hold the whole inquiry; ask the Nexus for one office flow at a
  time; hand each only its coherent type and its grade; choose the
  grade per office from the stakes; on Verdicts, either stop (secure
  enough for the stakes, or the economy says the next round costs
  more than it is worth) or hand the new Surprise to a fresh abduce
  flow. Never do an office's work.
  Reason [research]: a longer trace solves more problems without
  making the planner better at deciding which to attempt (TRIAGE,
  witnessed); models possess meta-cognitive controls but do not
  deploy them spontaneously, external guidance up to 66.7%
  (witnessed).

## What this changes in what exists [composition]

- The eight agent types read/write × trivial/ordinary/demanding/
  critical would become office × grade: abduce {overcoded, undercoded,
  creative}, deduce {corollarial, theorematic}, induce {crude,
  qualitative, quantitative} — eight programs, by coincidence the same
  count, but cut along the office first and the grade second. The
  read/write axis is absorbed: abduce and induce do not mutate the
  tree; deduce does.
- The aspects (design, realization, investigation) stay as names for
  what an inquiry is about; an inquiry of any aspect runs the same
  three offices.
- The design flow-flow and the realization flow-flow differ only in
  what the artifact is: a design document, or code.

## Against the evidence's multi-agent systems [composition, pending]

The negative multi-agent results relayed earlier (−70.0% on
sequential planning, witnessed) may rest on agents that shared one
top layer; a witness subflow is checking each paper's setup. If so,
none of that evidence tests this shape, where every office's top
stratum is a different program and the office flows are not spawned
by the harness's built-in tool but asked of the Nexus. Whether
specialized top strata rescue sequential coordination is, on this
flow's reading of the reports, untested by anyone.

## Anatomy questions

1. Is realization deduction — the code as what follows from the
   design, its tests as the predictions? Or is deduction its own flow
   between design and realization, deriving the predictions before
   anything is built?
2. Does the abduce flow emit several hypotheses ranked by economy,
   with the parent choosing (Peirce's shape), or one?
3. Does the induce flow's surprise return to abduction through the
   parent (methodeutic) or directly (the cycle without a holder)?
4. Do the eight agent types become office × grade?
