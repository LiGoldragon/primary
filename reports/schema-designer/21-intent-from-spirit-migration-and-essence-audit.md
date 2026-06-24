# 21 — Intent files deprecated: all intent driven from Spirit (`8rpu`); ESSENCE.md audit

*schema-designer · report 21 · the session that began as the `primary-7d8m`
epic (align schema-stack INTENT.md to the SpecifiedSchema era) and was
reframed by the psyche into a workspace-wide goal: deprecate every static
intent file and drive all intent from Spirit. Records the founding decision,
its supersession of two prior records, the surfaces now contradicting it, the
per-file audit method, and the first file audited (ESSENCE.md).*

## The reframe

The epic asked to align each schema-stack component's `INTENT.md` to the
SpecifiedSchema era. The psyche redirected: [intent files are being
deprecated, so we should just audit them for intent not in spirit, and do
intent-alignment sessions on their content based on what is in spirit and what
is in the files], then, on the scope question, [yes, all the files... driving
all intent from spirit is the new goal]. So the task is no longer *polish the
files* — it is *mine each file for durable intent not yet in Spirit, capture
the genuine gaps, then retire the file*.

## The founding decision — `8rpu`

Recorded (Supersede of `eny6` + `15df`):

> `8rpu` (Decision, High/High): [All intent is driven from Spirit: the static
> intent files — ESSENCE.md, the workspace INTENT.md, and every per-repo
> INTENT.md — are deprecated and their durable content migrated into Spirit.
> Agents read intent by querying Spirit scoped to the job: a broad domain
> query for essence-level universal context, narrower domain and referent
> queries for workspace or per-repo scope, so the tiering the files expressed
> becomes query scope rather than separate files. Every intent surface stays
> anchored to verified Spirit records, now by construction since Spirit is the
> single source. Per-repo ARCHITECTURE.md remains the kept-current file for
> architectural state, distinct from intent.]

What it superseded (both retired, lineage archived):

- `eny6` (Principle VeryHigh/High): [...each repo's INTENT.md is the first and
  most important file...]. Overturned. Its two kernels survive *transformed*:
  the universal/workspace/per-repo **file-tiering becomes query scope**, and
  **anchoring-to-Spirit is reinforced** (Spirit is now the sole source).
- `15df` (Correction High/Minimum): [...Per-repo INTENT.md files migrate off
  into Spirit gradually...]. Absorbed. Its surviving clause — per-repo
  ARCHITECTURE.md kept current for architectural state — is carried into
  `8rpu` as the boundary of what is *not* deprecated.

Certainty `High`: a firm, twice-stated new goal, not a stated universal axiom
(so not `Maximum`). Importance `High`: matches the superseded principle and
the intent-layer-wide blast radius. Exact query syntax is deliberately left as
design, not baked into the arrow.

## Consequence — surfaces now contradicting `8rpu`

These reference the deprecated files as canonical and need a manifestation
pass (separate from the file audits — this is updating the *discipline* layer,
not the intent layer):

| Surface | Stale framing |
|---|---|
| `AGENTS.md` | "A repo's INTENT.md is the first and most important file per repo"; the per-repo required-reading order |
| `ESSENCE.md` (lines 22–31) | lists per-repo INTENT.md as an intent-layer surface; "An agent entering a repository reads that repo's INTENT.md first — the canonical statement" |
| `skills/intent-log.md` | §"Capture is not done until it manifests into the affected repo's INTENT.md" — "Per-repo INTENT.md is the canonical agent-context surface" |
| `skills/repo-intent.md` | the per-repo INTENT.md discipline itself |
| `skills/skills.nota` | INTENT.md framing entries |

Open design question the psyche sketched but did not settle: **how agents read
intent without the files** — "the root ESSENCE.md is replaced by an `(All)` or
similar read from spirit `(Technology (Software All))`, etc (depending on the
job the query should obviously be larger)." That is a real design thread (the
session-start read contract becomes a scoped Spirit query); captured here as
design-to-resolve, not as firm intent.

## The per-file audit method

For each intent file, classify every substantive claim into three buckets:

- **Backed** — a Spirit record already holds the arrow → safe to drop from the
  file; no capture.
- **Gap** — genuine durable psyche intent with no Spirit backing → an
  alignment-session item; bring it to the psyche, confirm wording/kind/
  certainty, capture into Spirit.
- **Overturned** — superseded by current intent (e.g. `8rpu`) → delete from
  the file, do not capture.

The gaps drive the alignment sessions — one focused question per turn, the
psyche confirms or corrects, then the capture happens.

## File 1 — ESSENCE.md audit

| ESSENCE claim | Status | Spirit backing / disposition |
|---|---|---|
| Intent is primordial; agent's core work is clarify+capture intent | Backed (partial) | `qjrf`, `i59i` [intent logging dwarfs everything else]; no explicit "intent is primordial" **Maximum** axiom found — borderline, confirm in session |
| Psyche is the human; agent files are not psyche | Backed | core intent corpus; AGENTS.md override |
| Ask when unclear; don't infer; don't compose new intent from existing | Backed | `qjrf` [agents ask rather than generating plausible synthesis] |
| Intent layer outranks other surfaces; only psyche supersedes | Backed | core corpus |
| Agent reads repo's INTENT.md first — canonical, read before code (L29–31) | **Overturned** | superseded by `8rpu` — delete from file |
| Inferring intent is forbidden / bearing false witness | Backed (partial) | `qjrf`; candidate for an explicit **Maximum** axiom — confirm |
| Capture conservative; understate; short prompts mean go-ahead | Backed | `7hrd`, gate rules in `intent-log.md` records |
| Work instructions are not intent | Backed | `7hrd`, `krez` |
| **What I am building: priority ladder Clarity > Correctness > Introspection > Beauty (earlier wins)** | **GAP** | no record; adjacent `jys2` [target the best end-shape], `61ei` [beauty top-priority gate] — and `61ei` is in *tension* with beauty being #4 here |
| **Software eventually impossible to improve — the right shape, chosen carefully, observed cleanly** | **GAP** | adjacent `jys2`; the "impossible to improve" telos itself unrecorded |
| Not optimising for speed/features/MVP/ship-fast | Backed (partial) | `jys2` [not a historically-practical compromise]; the explicit "not minimum-viable / not ship-fast" wording is thin |
| **Not estimates — work described by what it requires, not how long** | **GAP** | no record |
| Beauty is the criterion; ugliness is the diagnostic | Backed | `61ei` [beauty must prevail as top-priority filter; audits apply the beauty filter as primary lens] |
| Naming: full English words; names don't carry ancestry | Backed | AGENTS.md override; near-certain **Maximum** records (verify) |
| Backward compatibility is not a constraint; binds only at declared boundaries | Backed | `c9fv` / `29pb` (cited report 19) |

Four confirmed gaps → alignment-session candidates: **(1)** the priority
ladder, **(2)** the "impossible to improve" telos, **(3)** no-estimates,
**(4)** the four design-value definitions. Two borderline (intent-primordial
and inferring-forbidden as explicit Maximum axioms) — worth confirming whether
the psyche wants them as standalone Maximum records.

The richest first item is **(1)**: the priority ladder is the heart of "What I
am building," it is unrecorded, and it carries an internal tension — ESSENCE
ranks Beauty #4 (lowest of four), while `61ei` and ESSENCE's own "Beauty is
the criterion" section make beauty a top gate. An alignment session resolves
both at once.

## Alignment session log

**Gap 1 — the priority ladder + beauty's rank — CAPTURED.** The psyche
confirmed the reconciliation: [capture the ladder, but frame beauty not as a
competing fourth priority that loses to the others, but as the completion-gate
that emerges when clarity, correctness, and introspection are right] /
[beauty is how you know you're finished]. First attempt as a fresh `Record`
drew a guardian `InsufficientWarrant` — the new arrow redefines beauty's role,
which the active `61ei` already held, so the guardian remanded to a maintenance
op. Resolved by **Supersede `61ei` → `4lkn`** (Principle, High/Minimum/Zero,
domain `(Technology (Software (Engineering Design)))`, referents `[design
beauty]`):

> `4lkn`: [The design-value priority ladder: Clarity, then Correctness, then
> Introspection, with the earlier value winning when these positive values
> trade off against each other. Beauty is the completion-gate of this ladder…
> how you know the work is finished, rather than a competing fourth priority…]

`4lkn` carries forward all of `61ei`'s content (beauty as primary audit lens,
the aesthetic qualities, the beyond-code reach into capture/report/substrate
discipline) and adds the three-value ordering plus the completion-gate
reconciliation — one coherent design-value principle rather than a ladder
record beside a beauty record. Certainty `High` (not `Maximum`): the ladder is
revisable — we just revised it — which is the signature of `High`, not a
founding axiom; offered to the psyche to elevate.

Lesson for the remaining gaps: when a gap's framing touches an arrow an
existing record already holds, expect the guardian to remand a fresh `Record`
to Supersede/Clarify. Check the neighborhood (shared referents/domain) before
choosing `Record` vs a maintenance op.

**Gap 2 — the telos — CAPTURED as `sj2c`.** The psyche restated the telos as
[best possible design], choosing the strong terminal reading over the soft
best-known one. Neighborhood read first surfaced that `zn2l` (a *Clarification*,
High/High) already references [the eventually-impossible-to-improve software of
the workspace essence … reached through the engine improving itself] — but no
*base* record held the telos; `zn2l` clarifies a telos that lived only in the
file. So the base was genuinely missing.

First attempt drew a guardian `TestimonyFabricated`: I had wrapped the bare
three-word answer in a long synthesized antecedent and a paragraph-length
description, which reads as agent prose laundered as testimony. Fixed by
binding the record tight to the phrase —

> `sj2c` (Principle, High/Minimum/Zero, referents `[telos design]`): [The build
> target is the best possible design: the design than which none better is
> possible, the terminal best the work aims at … the destination the design
> values serve.]

— with the testimony the bare [best possible design] and a short question as
antecedent. `sj2c` is the base telos; `zn2l` sits on top of it (mechanism),
`4lkn` is the value-priority it serves, `jys2`/`cam8` the frontier/ideal stance.

Lesson: terse psyche testimony must stay terse in the record. Inflating a
bare phrase with synthesized framing trips `TestimonyFabricated` — the
description is bound to the plain sense of the words, the elaboration goes in
reasoning, the antecedent stays a short question.

**Gap 3 — no-estimates — CAPTURED as `j8g6`.** The psyche confirmed with [yes I
agree] to the proposal. Captured as a Principle, affirmative-framed:

> `j8g6` (Principle, High/Minimum/Zero, referent `effort-sizing`): [Work is
> described and scoped by what it requires; the requirements define the work,
> in place of estimating how long it will take. Planning states what the work
> needs, not a duration.]

Two guardian round-trips on referents, both instructive: `[]` drew a hard
`Rejected EmptyReferents` (every record needs at least one referent), and
`[estimation workspace]` drew `ReferentGuardianRejected NonReferent`
("estimation is a concept, not a nameable particular") — whose reply usefully
dumps the full registered-referent set. The fix was the already-registered
`effort-sizing`, an exact-topic particular. Lesson: pick referents from the
registered set; abstract concepts (`estimation`) are rejected, named
particulars/practices (`effort-sizing`) are not.

ESSENCE.md itself is left untouched mid-audit; per `8rpu` the whole file is
retired once all its durable intent is in Spirit (plan step 5), not edited
piecemeal.

## Plan and sequence

1. ESSENCE.md alignment sessions on the four gaps (in progress — item 1 first).
2. Workspace `INTENT.md` audit (next root file).
3. The five `primary-7d8m` component `INTENT.md` files (the original epic,
   now folded in — audit each for intent-not-in-Spirit; Asschema-era content
   is *overturned*, SpecifiedSchema content should already be in Spirit).
4. The discipline-layer manifestation pass (AGENTS.md / skills) once the read
   mechanism is settled.
5. Retire each file after its durable intent is in Spirit.

`primary-7d8m` is updated to reflect that its component children are now "audit
INTENT.md into Spirit, then retire," not "align INTENT.md to SpecifiedSchema."
