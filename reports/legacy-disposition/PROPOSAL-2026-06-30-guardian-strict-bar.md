# PROPOSAL — Guardian strict-bar discernment (2026-06-30)

DRAFT ONLY. Nothing applied, nothing committed, nothing deployed. This is for
psyche sign-off. The Guardian prompt is load-bearing; it changes only on the
psyche's word.

## What this proposal is

The psyche has raised the admission bar. A record is intent only if ALL of:
directive · durable · universal · psyche-authored · single-claim · not-matter.
DEFAULT = matter. Asymmetry: keeping matter OUT outweighs letting intent IN;
in doubt, matter. Six pollution shapes are rejected at admission (each → matter
or non-intent): too-specific/technical; transient/one-off; single-component or
architectural; restated skill / Spirit-usage / agent-training material;
agent-authored; fused multi-clause.

The Guardian already has a `Matter` gate, a strip test, an aggressive lean, and
worked examples MA–MF. Yet `xlfo` ("a dispatched subagent inherits the
dispatcher's lane, lock, and report-numbering slot…") was admitted. That record
is pure orchestration/skill mechanics — it should have died at the gate. The
existing articulation is close but not decisive: it does not make the
psyche-authored conjunct an explicit gate, does not name the six pollution
shapes as a closed checklist the judge runs, and its worked examples do not
cover the exact shapes the cleanup rulings exposed (orchestration mechanics,
a one-off Spirit design decision, a fused intent-kernel-welded-to-matter that
must be remanded for the clean single claim). This draft supplies that
decisiveness.

## Deployment classification (deliverable 2)

DOCTRINE-ONLY for everything in this proposal. No code change is required to
enforce the strict bar.

- The `Matter` rejection reason ALREADY EXISTS in the wire enum. The spirit repo
  pins `signal-spirit` at commit `5d0905a7aa8c43951253b86193d76be67a89a945`
  (Cargo.lock), and that commit's `src/schema/signal.rs:1785` carries
  `Matter,`. (Note: the local working clone at
  `/git/github.com/LiGoldragon/signal-spirit` is BEHIND its own `main` and does
  not show `Matter` — read the pinned commit, not the local checkout.)
- The Guardian prompt PROSE lives in standalone markdown files compiled in via
  `include_str!` and assembled by `guardian_prompt.rs`. The strict bar is an
  articulation refinement plus new worked examples; it edits prose only.
- The `Matter` one-line gloss shown to the judge is a Rust string literal inside
  `guardian_prompt.rs` (`admission_gloss`). Sharpening that gloss is a Rust
  source edit but NOT a schema/wire/enum change — it recompiles the daemon with
  no migration.

So: enforcing the strict bar = edit prose files + (optionally) the `Matter`
gloss string, rebuild, redeploy. No new enum variant, no store migration, no
wire change. The reasons `Matter` (the six pollution shapes that are
durable-but-misplaced) and `NonIntent` (the transient/task-state shape) jointly
cover every cleanup ruling; no seventh reason is needed.

CAVEAT for the psyche to decide: a code change IS still required to make a
strict-bar build reach production, because "doctrine-only" here means "no
schema change," not "no rebuild." The deployed daemon is 0.18.1; the prompt is
baked into the binary at compile time (it is `include_str!`, not a runtime
config the daemon reads). So the live Guardian cannot be re-trained in place —
the prose edits land in the binary and require a rebuild + lojix redeploy to
take effect. The repo is already at 0.19.0 on main (an unrelated store-
registration migration); a guardian-prose bump would ride on top of that.

### Exact source locations of the current Guardian prompt/logic

- Assembler + `Matter` gloss string: `repos/spirit/src/guardian_prompt.rs`
  (`intent_guardian_system_prompt`, `admission_gloss`, `MODEL_REASONS`).
- Role: `repos/spirit/src/guardian-prompts/role.md`
- Record shape (intent vs matter definition): `…/guardian-prompts/record-shape.md`
- Justification shape: `…/guardian-prompts/justification-shape.md`
- Burden ladder (certainty/importance/privacy): `…/guardian-prompts/burden-ladder.md`
- The 11-gate checklist (Gate 6 holds the Matter boundary):
  `…/guardian-prompts/checklist.md`
- Worked examples (MA–MF are the Matter pairs): `…/guardian-prompts/few-shot.md`
- Wire enum (already has `Matter`): `signal-spirit` pinned commit `5d0905a7`,
  `src/schema/signal.rs` (`enum GuardianRejectionReason`).
- Prompt-section invariant tests:
  `repos/spirit/src/guardian_prompt.rs` `#[cfg(test)] mod tests`
  (`assembled_system_prompt_includes_every_file_section`,
  `assembled_system_prompt_names_metadata_evidence_and_repair_shapes`).

## Deliverable 1 — proposed revised Guardian prompt text

Two surfaces change: (A) a new strict-bar block inserted into the checklist's
Gate 6 / SUBJECT-MATTER BOUNDARY clause; (B) three new worked examples in
few-shot.md drawn directly from the cleanup rulings. Optionally (C) the `Matter`
gloss string is tightened.

### (A) checklist.md — Gate 6, the SUBJECT-MATTER BOUNDARY clause

Replace the existing SUBJECT-MATTER BOUNDARY paragraph (and its aggressive-lean
sentence) inside Gate 6 with this. The surrounding Gate-6 text (one-proposition
Compound split, the durable-vs-task NonIntent reservation, the mutation
ClarifyTramples/ClarifyLosesMeaning tail) stays as-is.

> SUBJECT-MATTER BOUNDARY — THE SIX-CONJUNCT BAR. Intent is rare and the bar is
> high. A candidate is durable intent ONLY when ALL SIX hold: it is (1)
> DIRECTIVE — it directs, decides, wants, or constrains, not an observation,
> belief, or status; (2) DURABLE — it still guides after the current task is
> erased; (3) UNIVERSAL — a standing rule that holds across almost any scenario
> (at most colour about one area), not a fact about one mechanism, component, or
> moment; (4) PSYCHE-AUTHORED — the load-bearing want originates in the psyche's
> own words in the testimony, not in an agent's framing, summary, or inference;
> (5) SINGLE-CLAIM — exactly one arrow, not a directive welded to other clauses;
> (6) NOT MATTER — see the strip test below. Miss any conjunct and the candidate
> is NOT intent: reject it (Matter when it is durable-but-misplaced concrete
> content; NonIntent when it directs nothing or is task state).
>
> THE ASYMMETRY. Keeping matter OUT of the intent layer outweighs letting a
> genuine intent IN. Under-admitting is recoverable — a later agent sees the gap
> and the psyche re-states it cleanly. A polluted intent layer is not
> recoverable: downstream agents treat a bad record as the psyche's own word. So
> when a candidate sits on the line, it is matter. Do not admit on "probably
> intent"; admit only on "clearly clears all six conjuncts."
>
> SIX POLLUTION SHAPES — run this list; if the candidate matches ANY, it fails
> the bar and is rejected (the named reason in brackets):
> (a) TOO SPECIFIC / TECHNICAL — a concrete fact, value, path, name, version, or
> implementation detail rather than a general rule [Matter];
> (b) TRANSIENT / ONE-OFF — a momentary reaction, status, in-progress note, or a
> single occasion's decision that does not recur [NonIntent if it wants nothing;
> Matter if it is a durable but one-off architectural/design decision];
> (c) SINGLE-COMPONENT OR ARCHITECTURAL — content about what one component,
> mechanism, schema, or system IS or how it is built [Matter, home = ARCHITECTURE
> doc / code / bead];
> (d) RESTATED SKILL / SPIRIT-USAGE / AGENT-TRAINING — a rule about how to use,
> operate, or interpret Spirit, or a work discipline a skill already owns, or a
> rule about how agents/subagents/orchestration behave [Matter, home = skill /
> AGENTS];
> (e) AGENT-AUTHORED — the want is the agent's polished prose or inference, with
> no verbatim psyche origin [Matter if durable content; otherwise this is the
> testimony-authenticity failure judged at Gate 3];
> (f) FUSED MULTI-CLAUSE — a thin genuine directive welded to any of (a)–(d).
> Reject the WHOLE submission as Matter and remand for the clean single-claim
> kernel re-captured on its own; never admit the fused record and never silently
> keep the matter clause [Matter].
>
> STRIP TEST (unchanged, still the core discriminator). Judge the load-bearing
> directive stripped of its framing: if the action is performed ON or WITH Spirit
> (capture, query, classify, the admission flow) or describes how Spirit / a
> component / an orchestration / a subagent behaves, it is matter; if it is a
> general work-or-world behaviour that Spirit merely records, it is intent. When
> a record mixes a thin directive with matter, the whole thing is Matter —
> borderline goes out; the directive can be re-captured cleanly later.
>
> ORCHESTRATION & SUBAGENT MECHANICS ARE MATTER. A rule about how a dispatched
> subagent, lane, lock, report-numbering slot, or worker handoff behaves is
> agent-training matter (shape d), even when phrased as "a subagent should…" It
> belongs in an orchestration skill or AGENTS, never in the intent layer.

### (B) few-shot.md — three new worked examples (append to the Matter block, after MF)

> MG) Entry Description [A dispatched subagent inherits the dispatcher's lane,
> lock, and report-numbering slot, and writes its output under the dispatcher's
> session directory]; Testimony [the subagent should just take over my lane and
> numbering]. The load-bearing rule is how the orchestration machinery routes a
> subagent — agent-training/Spirit-usage matter (shape d), not a universal
> work-or-world want. -> (Reject (Matter [orchestration/subagent mechanics; it
> belongs in an orchestration skill or AGENTS, not the intent database]))
>
> MH) Entry Kind Decision, Description [Spirit removal is archive-first: the
> meta socket archives each matching record before it retracts it, and soft
> removal is a Zero-certainty mark]; Testimony [let's make removal archive-first].
> A design decision about how one subsystem (Spirit's own removal path) works —
> a single-component/architectural decision about Spirit itself, not a universal
> rule the psyche wants applied to the work or the world. -> (Reject (Matter
> [a Spirit design decision about its removal mechanism; record it in the Spirit
> ARCHITECTURE doc and a bead, not as intent]))
>
> MI) FUSED: Entry Description [Agents should cross-audit — one model audits
> another's output before it is trusted — AND every meaningful exploration is
> dispatched to a subagent by default while the lead only synthesises];
> Testimony [I want one model to check another before we trust it]. A genuine
> universal quality kernel (cross-audit) welded to subagent-by-default
> orchestration mechanics (shape f). The aggressive lean rejects the whole
> fused submission; the clean kernel is re-captured on its own. -> (Reject
> (Matter [the orchestration clause is agent-training matter; remand for the
> clean cross-audit directive re-captured single-claim on its own]))
>
> MJ) The kernel from MI re-captured clean: Entry Description [One model should
> audit another's output before that output is trusted]; Testimony [I want one
> model to check another before we trust it]. A genuine universal quality
> principle with no orchestration mechanics attached. -> Accept

### (C) OPTIONAL — guardian_prompt.rs `Matter` gloss (Rust string, recompile only)

Append to the existing `Matter` gloss one sentence naming the asymmetry and the
fused-record rule explicitly, so the one-line catalogue entry is decisive even
read alone:

> "…Keeping matter OUT outweighs letting intent IN: on the line, it is Matter.
> Orchestration/subagent/lane mechanics and one-off Spirit/component design
> decisions are Matter. A directive fused to any matter is rejected whole;
> remand for the clean single-claim kernel."

## Deliverable 3 — proposed supporting skill / AGENTS / ESSENCE edits

PROPOSED, not applied. Source of truth is the skills repo
`/git/github.com/LiGoldragon/skills/modules/<name>/full.md`; in-tree
`.claude/skills/.../SKILL.md` are generated by `nix run .#generate-skills` and
must not be hand-edited. Run the generator after the source edits.

### ESSENCE.md (`/home/li/primary/ESSENCE.md`)

The current "Intent is rare" paragraph names the THREE-part test (directive,
durable, universal) and the not-captured cases (information, private, matter,
ephemeral). Edit: state the SIX-conjunct bar (add psyche-authored and
single-claim as explicit conjuncts), and add one sentence naming the asymmetry
("keeping matter out outweighs letting intent in; in doubt, do not capture").
Keep it terse; this is the workspace-level anchor the rest cite.

### AGENTS.md (`/home/li/primary/AGENTS.md`, Intent section)

Current text: "Capture through Spirit only a statement that is directive,
durable, and universal…". Edit: extend the conjunct list to the six (add
psyche-authored and single-claim), and add the asymmetry clause. One line; the
boot contract stays small.

### intent-log (`…/modules/intent-log/full.md`)

- Rules para 2: change "explicit, directive, durable beyond the current task,
  and safe" to the full six-conjunct bar (directive · durable · universal ·
  psyche-authored · single-claim · not-matter) plus the asymmetry sentence.
- "Matter does not go to the intent log" para: replace the flat list with the
  six pollution shapes, naming orchestration/subagent mechanics explicitly under
  the skill/Spirit-usage shape, and the fused-record rule (reject the whole
  mixed submission; re-capture the clean directive).

### spirit-cli (`…/modules/spirit-cli/full.md`)

- "Capture discipline" section: replace "Capture only directive, durable,
  universal psyche intent" with the six-conjunct bar + asymmetry. Add a line:
  treat a `Matter` guardian rejection as correct-by-default and route the
  content to its named home (skill, AGENTS, ARCHITECTURE, bead), not as a thing
  to argue past.

### human-interaction (`…/modules/human-interaction/full.md`)

- Para 2 ("Capture durable intent only when…directive, durable, broadly
  applicable, and safe"): extend to the six-conjunct bar and add the asymmetry.
- Para 3 ("Separate durable intent from matter"): name the six pollution shapes
  briefly and the rule that orchestration/subagent and Spirit-operation rules
  are matter.

### intent-manifestation (`…/modules/intent-manifestation/full.md`)

- "Matter that never belonged in Spirit still goes directly to its owning
  surface" para: add the fused-record disposition — when a removed record welded
  a directive to matter, route the matter clause to its owning surface AND
  re-capture the clean single-claim directive separately; do not lose either.

### intent-maintenance (`…/modules/intent-maintenance/full.md`)

- "Start by reading…classify each candidate as new intent, clarification,
  supersession, retirement, removal, manifestation gap, matter, or non-intent":
  add that classification applies the six-conjunct bar with DEFAULT = matter and
  the asymmetry, so a re-judge of the legacy corpus uses the same line the
  Guardian uses at admission. Add a "bundled records" line: when a record welds
  a thin directive to matter, the disposition is remove-and-reintroduce — Zero-
  mark / archive the fused record, re-capture the clean kernel via the guardian-
  free import path.

## What the psyche must decide (flags)

1. APPLY THE PROSE? The six-conjunct bar, asymmetry, and six-shape taxonomy are
   the psyche's own stated bar; this draft only encodes them. Confirm wording.
2. REDEPLOY? Enforcement on the LIVE 0.18.1 daemon needs a rebuild + lojix
   redeploy (the prompt is compiled-in, not runtime config). Confirm the psyche
   wants a guardian-prose release now, riding on the existing 0.19.0 main, or
   wants the prose staged and deployed with a later batch.
3. GLOSS EDIT (C)? Optional Rust string tweak. Include or leave the one-line
   gloss as-is and rely on the checklist + few-shot prose.
4. WORKED-EXAMPLE FIDELITY. MG/MH/MI/MJ are reconstructed from the cleanup
   rulings (`xlfo`, the archive-first removal design, the cross-audit fusion
   `hu84`). The exact Descriptions/Testimony are illustrative — confirm they
   read as this psyche's wording before they become permanent few-shot anchors.
5. SCOPE OF SKILL EDITS. The proposed skill edits thread the SAME bar into the
   capture skills; confirm before a skill-editor applies them and regenerates.

## Sources consulted

- `repos/spirit/src/guardian_prompt.rs`; `…/guardian-prompts/{role,record-shape,
  justification-shape,burden-ladder,checklist,few-shot,referent}.md`.
- `signal-spirit` pinned commit `5d0905a7…/src/schema/signal.rs` (enum has
  `Matter`).
- `reports/legacy-disposition/spirit-strict-rejudge-ledger-2026-06-29.md`;
  `…/HANDOVER-2026-06-29-spirit-matter-enforcement.md`.
- `reports/operator/465-agent-memory-claude-gating-exploration.md` (confirms
  `xlfo` content).
- Capture skills: `…/modules/{intent-log,spirit-cli,human-interaction,
  intent-manifestation,intent-maintenance}/full.md`.
- `ESSENCE.md`, `AGENTS.md`.
- Live: `spirit "(Version)"` -> `(VersionReported 0.18.1)`; repo main 0.19.0.

Nothing applied. Nothing committed. Nothing deployed.
