---
title: 552 — Legacy intent salvage — mining component-shape.nota
role: designer
variant: Audit
topics: [intent, spirit, legacy-nota, component-shape, component-triad, signal, sema, salvage]
description: |
  Mining report for component-shape.nota (65 legacy records). Surfaces the few
  core, durable, not-too-specific design ideas genuinely at risk of loss on
  deletion — those NOT already in the deployed Spirit store and NOT manifested
  into ESSENCE / AGENTS / per-repo INTENT / skills. Propose-only.
---

# 552 — Mining component-shape.nota

## Scope

One file scanned: `/tmp/intent-text/component-shape.txt` (`intent/component-shape.nota`),
65 records. This is the densest architecture file in the legacy substrate — the
Signal/Sema/Nexus three-layer model, the contract-local-verbs direction, the
component-triad legs, the CLI shape, owner/meta-signal authority, and the
signal-frame/executor migration history. The vast majority is already deep in
the live guidance layer and the deployed Spirit store; this audit isolates the
four ideas that fell through.

## Salvage candidates

### 1. Configuration is always a Mutate — daemon config is integral state, not optional state

- **Kind:** Principle
- **Proposed topics:** `[component-triad daemon-configuration mutate policy sema]`
- **Proposed description:** Daemon configuration is always a Mutate: the way a
  daemon is configured is integral durable state, not optional side-state, and
  it changes through the same authority chain (owner/meta-signal Mutate) as any
  other state mutation. Configuration is policy state in the sema-engine DB, not
  a special non-state input.
- **Proposed certainty:** High (legacy wording is Maximum, but the underlying
  general principle is well-supported by adjacent ratified records; High is the
  honest carry for the generalised form).
- **Supporting verbatim:** [the config is a mutate. All the config should be a
  mutate command because it's changing something that is a part of the daemon.
  The way the daemon is configured is not some optional state.]
- **Preservation check:** Queried Spirit `(Partial [config configuration
  daemon-configuration mutate policy meta-signal])` — `cgd8` says configuration
  changes through the meta-signal socket and config verbs live in the
  meta-signal contract, and `ur16`/`1dpi` cover the bootstrap/standby model;
  NONE state that configuration *is a Mutate* / is integral non-optional state.
  Grepped `ESSENCE.md AGENTS.md INTENT.md skills/` for
  `config.*mutate|not.*optional state|configuration.*integral` — empty.
- **At-risk rationale:** The socket-level rule (config goes through meta-signal)
  is preserved, but the deeper modeling principle — configuration is a Mutate on
  durable policy state, not a privileged out-of-band knob — is the load-bearing
  reason the socket rule holds. Without it, agents re-introduce "config is
  special, not state" framing. It is the only place this principle is stated.

### 2. Verbs are cheap — prefer many named domain verbs over one collapsing verb

- **Kind:** Principle
- **Proposed topics:** `[signal contract naming variant-discipline classification-words]`
- **Proposed description:** Verbs are cheap and clarifying — do not fear adding
  them. When the choice is between one verb covering many sub-actions and
  multiple verbs each naming a sub-action, prefer multiple named verbs; the
  split makes the contract's logic clearer than collapsing sub-actions under a
  single broad verb. Applies generally to contract operation-root design.
- **Proposed certainty:** High
- **Supporting verbatim:** [I think the split is better. I don't think we have
  to be afraid of verbs. I think they'll make everything more clear.] and
  [every domain has its own verbs … prefer multiple verbs naming each
  sub-action].
- **Preservation check:** Queried Spirit `(Partial [signal-shape
  variant-discipline naming logic-separation classification-words])` and
  `(Partial [variant variants enum-variant split signal-tree])` — `7l7l`
  establishes contract operation roots are domain verbs (not Sema words), but
  NOTHING states the granularity principle that splitting into more verbs is
  preferred over collapsing. Grepped guidance for `verbs are cheap|afraid of
  verbs|split.*collaps|multiple verbs` — empty.
- **At-risk rationale:** `7l7l` answers "what vocabulary" (domain verbs, not the
  six Sema words) but not "how many / how granular." The split-over-collapse
  bias is a distinct, recurring design call (it settled the persona-mind
  Grant/Extend/Revoke split against a single Adjudicate verb) and would be lost.

### 3. Every accepted operation lowers to a NonEmpty named command — no empty plans

- **Kind:** Principle
- **Proposed topics:** `[lowering nexus sema execution command observation]`
- **Proposed description:** Every accepted operation lowers to a NonEmpty
  sequence of explicitly-named component commands — no-ops, validations, and
  idempotent applies lower to named commands (e.g. RecordIdempotentApply,
  CheckProposalAgainstCurrent), never to empty plans. Three reasons: the
  structural type already says NonEmpty so a zero-command lowering weakens the
  contract; every operation must leave an executor-visible witness for Sema
  observation coverage; and a named command makes the semantics explicit (an
  idempotent apply differs from a successful apply even when neither changes
  durable state).
- **Proposed certainty:** High
- **Supporting verbatim:** [Every accepted operation lowers to NonEmpty<Command>.
  No-ops, validations, and idempotent applies lower to explicit named commands,
  not empty plans … every operation must have an executor-visible witness for
  Sema observation coverage.]
- **Preservation check:** Queried Spirit `(Partial [lowering command nexus sema
  execution witness operation])` and the broad sema query — the three-engine
  model (`g3f2`, `r6zg`, `t2iy`), the contract-operation/component-command/
  Sema-classification three layers (`7l7l` and adjacent), and ToSemaOperation
  projection are all present, but NONE state the no-op-as-explicit-named-command
  / NonEmpty-lowering rule. Grepped guidance for `NonEmpty.*Command|no-op.*
  command|idempotent.*apply|empty plan|executor-visible witness` — empty.
- **At-risk rationale:** This is a sharp, durable execution-model invariant that
  governs how the Nexus lowers operations to Sema-observable commands. It is the
  reason observation coverage is complete (no silent no-ops). It survives the
  specific signal-frame migration that produced it and is found nowhere else.

### 4. Mind-orchestrate authority follows the mind-body autonomy analogy

- **Kind:** Principle
- **Proposed topics:** `[mind orchestrate authority autonomy component-triad]`
- **Proposed description:** The Mind-to-Orchestrate authority relationship
  follows the human mind-body analogy: Orchestrate (body) has substantial
  autonomy and does much of its work without Mind's intervention, while Mind
  (mind) does much that never touches Orchestrate. Mind's authority surface
  lives at the override-and-instruct level, NOT at the level of low-level
  routine operations — Mind reaches across only when its cognitive judgment
  needs to redirect Orchestrate, and does not micromanage Orchestrate's own
  machinery. Channel choreography and low-level routing are orchestrator work,
  not mind work.
- **Proposed certainty:** Medium (the authority chain is settled; the analogy is
  a design anchor the psyche offered, and the lane/component names are partly
  in flux — Medium is the honest carry).
- **Supporting verbatim:** [think of the human mind vs the body; the body does
  many things mindlessly, and the mind does many things that dont involve
  controlling the body, while it still can override the body and instruct it to
  do things it wouldnt do on its own] and [There's no need for the mind to take
  care of all of this low-level operation. This is orchestrator work.]
- **Preservation check:** Queried Spirit `(Partial [mind orchestrate router
  authority autonomy body harness])` — `ckhx`/`bcca`/`5fd6` cover terminal/cell
  lifecycle ownership and orchestrate's coordination identity, but NONE carry
  the mind-body autonomy principle. `skills/component-triad.md` carries the
  authority CHAIN ("mind owns orchestrate; orchestrate owns router and harness")
  but NOT the autonomy/interrupt-only principle behind it. Grepped guidance for
  `mind.*body|mindlessly|override.*body|micromanage` — only the flat chain
  statement, not the autonomy boundary.
- **At-risk rationale:** The chain (who owns whom) is preserved; the PRINCIPLE
  that determines what flows across that authority edge (Mind interrupts only at
  cognitive-judgment moments; Orchestrate runs its own machinery) is the design
  anchor that keeps the contract surfaces from bloating Mind with low-level
  routing verbs. It is the rationale future agents need when deciding whether a
  new operation belongs on Mind's owner contract or stays inside Orchestrate.

## Already preserved / dropped

The bulk of `component-shape.nota` is well-preserved or too specific. Scanned
and confirmed safe to delete:

- **Component-triad legs + CLI-is-not-a-leg** (records 1, 2, 41, 51): preserved
  in `AGENTS.md` "Component triad means daemon + working signal + meta policy
  signal" and `skills/component-triad.md`; Spirit `pb1g`, `e2px`, `kvg1`.
- **Two authority contracts (working + owner/meta-signal), every stateful
  component has a meta/owner contract** (records 1, 42, 43, 44): preserved in
  `skills/component-triad.md` (policy/working state and surfaces) and Spirit
  `hnpo`, `r9qy`, `pb1g`, `cgd8`. Owner-signal naming is itself superseded →
  meta-signal (`hnpo`).
- **One-argument rule / no flags / NOTA-or-file / daemon binary boundary**
  (records 5, 47, 49): preserved as a hard override in `AGENTS.md`
  ("Component processes take exactly one argument") and Spirit `e6ri`, `pjvv`,
  `1dpi`, `2kep`, the CLI env-var carve-out in `tpvu`/`yn6g`.
- **CLI is a pure NOTA↔Signal translation bridge, thin client, two-socket
  dispatch, generated dispatch layer, naming = daemon minus -daemon, split
  nix packages** (records 46, 48, 50, 52, 60, 61, 62, 63): preserved across
  `skills/component-triad.md`, `skills/naming.md` (binary naming), and Spirit
  `4oev`, `cf30`, `js6b`, `nkyh`, `latq` (two-socket runner), `dre8`.
- **Contract-local public verbs (Query/Message), NOT database execution verbs;
  Sema classification forbidden on the wire** (records 7, 8, 9, 11, 12, 13,
  16): the spine is preserved by `7l7l` (Sema words forbidden as contract
  roots; operation roots are domain verbs; Sema derived internally) plus the
  receiver-dispatched-verb idea is implicit in the per-component command model.
- **Three-layer model: Contract Operation / Component Command / Sema Operation
  (payloadless classification); ToSemaOperation projection; engine = reusable
  framework over component Command** (records 34, 35, 36, 39): heavily preserved
  — `7l7l`, `l6zw`, `3d5z`, `a71r`, `t2iy`, `g3f2`, `r6zg`, plus the strict
  triad-engine separation.
- **signal-core → signal-frame rename; signal-sema; frame mechanics only;
  signal_channel! macro modifications; observable block / OperationReceived /
  EffectEmitted; AcceptedOutcome split; engine-failure → Accepted+BatchAborted;
  BatchErrorClassification; ObservedLowering** (records 14, 15, 17, 18, 19, 21,
  24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 37, 38, 54, 56): these are
  migration-history Decisions — most are too specific (exact trait surfaces,
  exact variant fields, named report pointers, churn authorizations) and the
  durable residue (signal-frame name, schema-emitted streaming, plane-gating)
  is in Spirit `gb95`, `brgo`, `3got`, `maeq`. Drop as transient/specific.
- **Claim by directory or explicit file list, no minus-handoff** (record 6):
  preserved by Spirit `29s6`/`q402` (lock selectively; reports claim-exempt)
  and `orchestrate/AGENTS.md`.
- **Mind-to-Router → Orchestrate-to-Router authority correction; channel
  choreography is orchestrator work** (records 20, 53, 57): the chain is in
  `skills/component-triad.md` ("orchestrate owns router and harness"); the
  residual autonomy principle is salvaged as candidate 4 above. The specific
  Grant/Extend/Revoke/Deny verb placement is too specific (and persona-prefixed
  surfaces are deprecated per `k1i1`).
- **Macro emits clean unprefixed names; disambiguate via Rust modules, not an
  opt-in prefix knob; macro auto-generates OperationKind + From impls**
  (records 64, 65): substantially preserved by the no-redundant-ancestry rule
  (`AGENTS.md`, `skills/naming.md`) and the schema-emitted-nouns discipline
  (`skills/abstractions.md`); the macro-specific "no opt-in knob, use modules"
  application is a weaker-version-only gap, judged not worth a record — the
  general ancestry rule governs it.
- **Missing owner-signal-persona-* repos are intentional; Mind lifecycle verbs
  may live in the supervisor** (records 22, 59): transient state observations /
  open questions, not durable design. Mind lifecycle is now reframed by the
  bootstrap/standby model (`ur16`, `1dpi`). Drop.
- **Tap/Untap mandatory for persona components; universal observer hook on
  every daemon** (records 17, 38): the observability/trace infrastructure is
  heavily preserved (`tpcm`, `jaz4`, `nkyh`, `tpvu`, `cf30`); the
  persona-specific mandatory-Tap detail is too specific and persona-prefixed
  surfaces are deprecated. Drop.
- **Lane/labor split, repo-creation authorizations, "continue your work",
  "consider report N", implementation greenlights** (records 19, 23, 26, 27,
  28, 29, 40): pure working orders — die when the task is erased. Not intent.
  Drop.
