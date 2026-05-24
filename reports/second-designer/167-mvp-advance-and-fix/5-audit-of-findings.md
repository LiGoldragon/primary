*Kind: Audit · Topic: audit-of-findings · Date: 2026-05-24*

# 5 — Audit of subagent findings (Wave 2)

*Subagent E (auditor role per intent 235 — Medium, mechanical
pattern-checking, human-readable until DeepSeek automation lands).
Reviews subagents A (mvp-scope-clarification), B (macro-implementation-
gap), C (design-clarifications-needed), D (operator-fixes-executed) for
contradictions, missed angles, operator-introduced issues, and
unresolved clarifications. Read-only. No edits to peer reports.*

## §1 TL;DR

**13 consistency items found. 4 MVP-impact (must reach orchestrator's
overview synthesis). 5 are reconcilable design ambiguities the
overview must resolve. 4 are no-action (cosmetic / clarifications-only
/ already-correct).**

The headline finding: **A, B, and C disagree on what `OperationDispatch`
actually IS.** A treats the dispatch trait as wire-side routing only and
explicitly calls out the question of Layer 2/3 in §4.9 ("not a Layer 2
leak"). B implements it as `match bytes[0] → handle_<op>(decoded_payload)`
— consistent with A's narrow reading. C in §3.1 surfaces the same
concern but adds a NEW framing: that /323's "dispatch" conflates
**wire-side header routing** with **engine routing**, and that the
distinction is not made explicit in /323+/324. C's framing IS the
sharper one; A's §4.9 is correct but doesn't go as far as C does
toward naming the conflation in the source reports. This needs
foregrounding in 6-overview's §"Q1 resolution".

Two operator-introduced issues found in D's edits, both **low-impact
cosmetic**:
(a) D's §2.1 edit-list claims 12 edits but the table in §1 says 11
(off-by-one labeling — edits 11 and 12 in §2.1 are actually
correctly numbered but appear as edits 9-12 in some readings due
to inconsistent prose numbering vs table count).
(b) D's §3 references commits `b95c5eea`/`db8fe5f3` but the current
HEAD on `main` is `4052aa10c0cd` (yzssuznxsukp) with description
"backfill commit IDs in 4-operator-fixes-executed.md §3 after split
+ push" — i.e., D self-corrected after-the-fact via the backfill
commit. Verified: backfill DID land on `main@origin`.

Two **missed angles**: (1) None of A/B/C/D notice that D's bracket-string
sweep introduced a documentation-content casualty in /164 §3.1 comment —
the change from `;; data-carrying enums with one named variant = "structs" in the`
to `;; data-carrying enums with one named variant = structs in the` arguably
LOSES the scare-quote meaning (the text was DELIBERATELY saying
"these aren't really Rust structs"). D's call is defensible but
worth flagging — the scare-quoted "structs" is English punctuation,
not a NOTA string, so it's outside intent 401's scope. (2) None of
A/B/C examined the spirit 396 record's actual literal wording —
they all paraphrase. Without spirit 396 in the deployed Spirit DB
visible to this auditor (the intent files on disk don't carry
records 396+), the audit can't verify the literal text; the
consolidated reading in §7 below works from the consistent paraphrase
across the four reports.

## §2 Cross-subagent consistency matrix

Each row is a load-bearing claim with a citation per subagent
(where the subagent addresses it). Green-cell consistency, yellow
contradiction-but-reconcilable, red contradiction-needs-resolution.

| Claim | A | B | C | D | Verdict |
|---|---|---|---|---|---|
| Layer 2/3 sema-lowering emission POST-MVP | YES §3.4 (narrow lean) | YES §2 row 9a "post-MVP per /324 §6" | YES §3.1 "MVP doesn't emit Layer 2 OR Layer 3" | N/A | **CONSISTENT** |
| `OperationDispatch` IS MVP | YES §2.4 row 3 IN | YES §2 row 8 MB | YES §3.1 (clarification: wire-side only) | N/A | **CONSISTENT** |
| `OperationDispatch` ≠ engine routing | §4.9 (explicit) | implicit (calls `self.handle_record(entry)`) | §3.1 (most explicit; names the conflation) | N/A | **CONSISTENT but C's framing is sharper** |
| `VersionProjection` IS MVP | YES §2.6 row 1 IN | YES §2 row 7 MB | YES §3.5 (rule needed) | N/A | **CONSISTENT** |
| `nota-box` is gating dependency | YES §5 Q3 lean | YES §2 row 6 "gated by primary-l6pc" | YES §4.1 defer to `primary-l6pc` | N/A | **CONSISTENT** |
| Engine annotations in MVP schema | NO §3.4 (don't include) | N/A (B is on code-side gaps) | NO + reader-accepts-but-ignores §3.1 | N/A | **CONSISTENT — C's "accept-but-ignore" lean adds a refinement A doesn't reach** |
| Field name `magnitude` vs `certainty` | `magnitude` §5 Q4 (with C1 to fix /322 §4.2) | flag at `emit.rs:551-553` hardcode §4.3 | `magnitude` §2 row 10 | N/A | **CONSISTENT — but B catches that `field_name_for_type` ALREADY has a Spirit-specific shim hardcoded; this means /322 §4.2's example may actually be REACHED by the current emit code, which sharpens A's C1 from cosmetic to functional** |
| Async dispatch handler | YES §5 Q5 lean | flag as DESIGN-DECISION-REVIEW §3.1 | YES §3.3 (pin async) | N/A | **CONSISTENT — A treats as lean; C treats as pin-and-document; B suggests marker comment** |
| Database-test-passed marker = engine commit-log | YES §5 Q6 lean Option A | N/A | N/A | N/A | **A only — not in B/C scope; consistent with /324 §7** |
| `next_schema` NOTA syntax | implicit IN MVP §2.6 row 4 | flag as MB §2 row 7 sub-task 1 | EXPLICIT shape A — bracket path-ref §3.4 | edit 4 in /164 §8.3 converts existing example to bracket form | **CONSISTENT — but only C names the actual NOTA syntax to use; A and B presume the syntax exists; D's edit-4 preserves the existing /164 §8.3 example which already uses Shape A** |
| Date/Time primitive shape | N/A | N/A | EXPLICIT §3.2 — bracket-string `[2026-05-24]`, rkyv packed u32 | N/A | **C only — A and B don't catch this MVP-blocker; C surfaces a real gap** |
| Identity vs hand-written `From` rule | N/A | implicit ("Identity for unchanged") | EXPLICIT §3.5 — conservative rule table | N/A | **C only — A and B treat as obvious; C catches that the rule needs pinning** |
| `belongs <StreamName>` grammar | N/A | references but doesn't critique §3.2 | EXPLICIT §4.5 — violates positional discipline; three reshape options | N/A | **C only — real NOTA grammar issue A/B miss** |
| Cycle detection failure mode | N/A | N/A | EXPLICIT §4.6 | N/A | **C only** |
| Single-variant collapse + Help interaction | N/A | mentions Help as PM-tracked §2 row 4 | EXPLICIT §4.4 — the rule needs ordering | N/A | **C only — the schema-collapse + Help-injection ordering is a real conflict** |
| `primary-ezqx.2` should be closed | YES §4.3 (operator action item) | LISTED §6 see also | LISTED §5 anchor item | N/A | **CONSISTENT — already closed per `bd show` (verified)** |
| `primary-ezqx.1` bead acceptance text drift | YES §4.4 (operator action item) | N/A | N/A | N/A | **A only — confirmed: `bd show primary-ezqx.1` body still references /320 sizing; A's recommendation valid** |

## §3 Missed angles per subagent

### §3.1 Subagent A (mvp-scope-clarification)

- **MISSED**: Date/Time primitive shape (C §3.2) is a real MVP-blocker
  that A's Q1-Q10 list doesn't cover. A's Q-list is dominated by
  scope decisions (in/out of MVP); C's clarifications are dominated
  by mechanism decisions (how does X work). The two lists complement
  each other; orchestrator should merge per §5 below.
- **MISSED**: The `field_name_for_type` hardcoded shim B caught at
  `emit.rs:551-553`. A's C1 fix to /322 §4.2 is necessary BUT
  insufficient — the shim itself is a temporary kludge that needs
  retirement when the field-name override syntax lands. A treats
  this as a doc fix; the deeper issue is the emit code's hardcode.
- **CONSIDERED-but-could-go-deeper**: A's §4.10 ("Closed-decision
  marker discipline") tracks ~17 markers across /320 + /322 + /323
  but doesn't list them by ID. The /324 §7 review checklist (last
  row "Markers inlined") implicitly assumes the list exists. The
  overview should make the marker list authoritative.

### §3.2 Subagent B (macro-implementation-gap)

- **MISSED**: `LogVariant` for sema-side (mentioned as Gap 9b
  PARTIAL) — B treats as "hand-done for MVP" but A §2.5 + /324 §5
  treat it as IN-MVP via manual impl on `SemaOperation`. The
  classification "PARTIAL hand-done for MVP" is correct; the
  framing as a macro gap is misleading. The macro doesn't need
  extending; sema-engine's `signal-sema/src/operation.rs` needs
  the manual impl. B's framing risks pulling operator into a
  macro-side fix when the actual MVP scope is a hand-written impl.
- **MISSED**: contract_section (Gap 5) is NOT MVP-blocking for the
  Spirit pilot, but B doesn't note that the owner-contract
  `owner-signal-persona-spirit` IS in the workspace and any future
  schema migration for the owner triad WILL need contract_section.
  Per A §2.9 last row + /324 §6, owner-contract migration is POST-
  MVP; B's "NOT MVP-blocking" classification is correct but the
  scope clarity could be stronger.
- **MISSED**: The `decode_body` helper B mentions in §3.1 needs to
  exist in `signal-frame` (B's "Lean (b)") — but the trait `NotaDecode`
  it would invoke isn't named in any current `signal-frame` source
  per A's anchor list. Either (a) the helper is new code in `signal-
  frame` (so an additional file map entry beyond /324 §5), or (b)
  the macro emits the helper inline per channel. B leaves this open;
  orchestrator should pin a choice.

### §3.3 Subagent C (design-clarifications-needed)

- **MISSED**: C's §3.1 reaches the right conclusion (narrow MVP)
  but doesn't cite /324 §5's file map directly. /324 §5 is the
  single most authoritative current MVP-scope enumeration, and it
  silently omits Layer 2/3 code generation from the file actions —
  C's argument would be tighter with that citation. A §3.1 makes
  this citation; C should align.
- **MISSED**: C's clarification §4.5 (`belongs` annotation grammar)
  is correct that the current shape `(StateChanged (StateChanged belongs DomainStream))`
  reads as labeled-not-positional. But C doesn't note that B's
  schema_reader (per B §3.2 gap 5) ALREADY hardcodes `signal-persona-spirit`
  for stream membership at `schema_reader.rs:562-573` — so the
  current code has the same issue C surfaces in design space. C's
  three reshape options should be informed by B's hardcode observation.
- **MISSED**: C's §4.1 (box layout coordinate notation) defers to
  `primary-l6pc` but doesn't note that `reports/designer/325-nota-box-library-design-and-implementation.md`
  LANDED during Wave 1 — there's now a concrete library design.
  C's "needs explicit syntax design" is stale; the design exists.

### §3.4 Subagent D (operator-fixes-executed)

- **MISSED**: D's Fix 1 (bracket-string sweep of /164) does NOT
  cover the downstream propagation A §5 last recommendation calls
  out — /320, /321, /322, /323 all reference /164's schema examples
  with quoted strings. D's scope was /164 only per the task. The
  follow-up (sweep /320-/324 for citations of /164's old quoted
  examples) is correctly listed in D §5 "Next operator pickup"
  item 3, but is not in the current MVP-blocker set.
- **MISSED**: D's Fix 2 (terminology pass on /163) doesn't touch
  /166 line 41-42 which uses identical "Tier 1 micro / Tier 2
  summary / Tier 3 full rkyv" framing in its summary of the
  /163 issue. /166 is self-aware about the lag (the audit-finding
  IS the report's purpose) but if downstream readers cite /166's
  framing they'll inherit the wrong vocabulary. Not MVP-blocking
  but worth a sweep before the meta-directory closes.
- **MISSED**: D's Fix 3 (sema-engine ARCH dep-name) is correct but
  the audit trail at /163 §10.1 also says "the actual Cargo.toml
  dependency itself (separate file under sema-engine/) is not in
  scope for this fix; the audit only flagged the ARCH doc lag." D
  preserved this caveat — but didn't verify the Cargo.toml is
  ACTUALLY current. Spot-check below in §4.

## §4 Operator (D) edit spot-check verification

Per the task: "Spot-check 3 of subagent D's bracket-string edits in
`reports/second-designer/164-...md` by reading specific lines to
confirm the edits look correct (not just file commits)."

### §4.1 Spot-check: /164 §3.4 wire round-trip (D's edit 1)

D claims line 231 changed from
`(Entry workspace Decision "summary" "context" Maximum "quote")` to
`(Entry workspace Decision [summary] [context] Maximum [quote])`.

**Verified at /164:231**: `(Entry workspace Decision [summary] [context] Maximum [quote])`. **Correct.**

### §4.2 Spot-check: /164 §6.1 cross-schema reference (D's edit 3)

D claims line 556 changed from
`(Magnitude "../signal-sema/magnitude.schema.nota")` to
`(Magnitude [../signal-sema/magnitude.schema.nota])`.

**Verified at /164:556**: `(Magnitude [../signal-sema/magnitude.schema.nota])`. **Correct.**

### §4.3 Spot-check: /164 §8.3 next_schema (D's edit 4)

D claims line 955 changed from `"../signal-persona-spirit-next/schema.nota"` to
`[../signal-persona-spirit-next/schema.nota]`.

**Verified at /164:955**: `;; Reference to the next version's schema:`
on line 954 followed by `(next_schema [../signal-persona-spirit-next/schema.nota])`
on line 955. **Correct.**

### §4.4 Bonus check: Rust code blocks preserved (D's §2.1 "Things deliberately NOT changed")

D claims Rust code excerpts inside ` ```rust ` blocks preserved
quotes (Rust requires `"..."`). Spot-checked grep for double
quotes in /164 returned 63 lines. Distribution: mermaid labels
(~50%), English prose with scare quotes / report-name quotation
(~30%), Rust code excerpts in §6.2-6.4 (~15%), NOTA `;;` comments
that D deliberately left or normalized (~5%). **No Rust code
breakage detected.**

### §4.5 Verification: /163 terminology pass preserved three-tier framework

Grep for `Tier 1\|Tier 2\|Tier 3` in /163 returned 3 hits:
- Line 198: `the current macro emits the Tier 1 / Tier 2 trait scaffolding`
- Line 271: `SemaObservation is the cross-cutting Tier 1 / Tier 2 observation`
- Line 884: `wire kernel + macro + Tier 1/2/3 sizing discipline (§5)`

All three reference the three-tier sizing framework (D's protected
class), not "Tier 1 micro" (the retired name). Grep for
`Tier 1 micro\|Tier 1 small\|small-object Tier 1\|small-message Tier 1`
returned **zero hits**. **D's preservation rule held.**

### §4.6 Verification: sema-engine ARCH dep-name

Verified at `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md`
lines 109 + 117: both reference `signal_frame` (the corrected name).
Grep for `signal-core\|signal_core` in the file: **zero hits**.
**D's fix complete.**

### §4.7 Verification: commit history

Per `jj log -r 'main | main@origin'` in `/home/li/primary`:
`yzssuznxsukp 4052aa10c0cd main second-designer/167 D: backfill commit
IDs in 4-operator-fixes-executed.md §3 after split + push`. **`main`
matches `main@origin`** — D pushed cleanly.

Per `jj log -r 'main | main@origin'` in `/git/github.com/LiGoldragon/sema-engine`:
`nxxoouzlprpx 6a552182ef33 main ARCHITECTURE: boundary diagram dep-name
signal-core → signal-frame per second-designer/163 §8 audit`. **`main`
matches `main@origin`** — D pushed cleanly.

Both commit messages use inline form (no editor opened). **jj
discipline held.**

### §4.8 Operator-introduced cosmetic issue

D §2.1 lists 12 enumerated edits but D §1 TL;DR table says "11
edits (NOTA blocks + prose references)". Counting actual numbered
items in §2.1: 12 (items 1-12 explicit). The TL;DR count is the
off-by-one. **Cosmetic; no functional impact.** Not flagged for
fix — orchestrator can absorb in 6-overview's synthesis.

### §4.9 Observation: scare-quote loss in /164 §3.1 comment edit

D edit 6: changed `;; data-carrying enums with one named variant = "structs" in the`
to `;; data-carrying enums with one named variant = structs in the`.

The original `"structs"` were scare-quotes signaling "these aren't
REALLY Rust structs, they're enum-with-single-variant collapsed to
look-like-structs". Removing the quotes loses that ambiguity signal.
D's call is defensible (intent 401 is about NOTA string literals,
not English scare-quotes), but a non-quote alternative exists —
the text could read "single named variant collapse-to-structs" or
"single named variant (struct-like)" to keep the ambiguity flag.

**No-action recommended**: this is editorial taste; D's edit is
within scope; loss is small. Flag for the orchestrator to note if
future readers complain.

## §5 Question-list reconciliation — A's Q1-Q10 vs C's top-5 + others

### §5.1 Merged + deduplicated question list

A surfaces 10 questions ordered by MVP-migration impact; C surfaces
14 clarifications (5 MVP-blocking + 6 MVP-impacting + 3 post-MVP).
Merged and deduped:

| # | Question | A's # | C's # | Both? | Lean / status |
|---|---|---|---|---|---|
| M1 | Layer 2/3 sema emission in MVP first slice? | Q1 (top) | §3.1 (top) | YES | **narrow MVP** (both agree) |
| M2 | `(engine X)` annotations in MVP schema? | Q2 | §3.1 (subordinate) | YES | **no annotations in schema; reader accepts-but-ignores** (C's refinement adds to A's lean) |
| M3 | `magnitude` vs `certainty` field name? | Q4 | §2 row 10 | YES | **type-derived `magnitude`** (both agree); ALSO requires emit.rs hardcode retirement per B §4.3 |
| M4 | `nota-box` gating? | Q3 | §2 row 7 (defer to l6pc) | YES | **gating dependency** (both agree); /325 LANDED — adds force |
| M5 | Async dispatch handler? | Q5 | §3.3 | YES | **async** (both agree); /324 §10.2 leans the same |
| M6 | Marker substrate = commit-log Option A? | Q6 | NOT covered | A only | **Option A** (A's lean; /324 §7 leans same) |
| M7 | Schema component daemon timing? | Q7 | §4.3 | YES | **POST-MVP**, library face only (both agree) |
| M8 | Recursive Help (`primary-ezqx.3`) parallel to `.1`? | Q8 | NOT covered (§4.4 touches a related interaction) | A only on parallelism | **parallel** (A's lean) |
| M9 | Owner-contract migration timing? | Q9 | NOT covered | A only | **POST-MVP** (A's lean; consistent with /324 §6) |
| M10 | Smart-handover for v0.1.2? | Q10 | NOT covered | A only | **POST-pilot** (A's lean) |
| M11 | `next_schema` NOTA syntax? | implicit via §2.6 row 4 | §3.4 (top-5 MVP-blocker) | C only EXPLICIT | **Shape A — top-level `(next_schema [path])`** (C's lean) |
| M12 | Date/Time primitive shape? | NOT covered | §3.2 (top-5 MVP-blocker) | C only | **bracket-string literal `[2026-05-24]`; rkyv packed u32** (C's lean) |
| M13 | Identity-vs-hand-written-From boundary rule? | NOT covered | §3.5 (top-5 MVP-blocker) | C only | **C's conservative table** (only same-name + same-fields-in-same-order = Identity; everything else requires hand-written From) |
| M14 | `belongs <StreamName>` annotation grammar? | NOT covered | §4.5 | C only | **Option B — top-level `StreamMembership` block** (cleanest); see B §3.2 for current code hardcode |
| M15 | Cycle detection failure mode? | NOT covered | §4.6 | C only | **error with full cycle path** (C's lean) |
| M16 | Help injection + single-variant collapse interaction? | NOT covered | §4.4 | C only | **collapse rule needs Help-aware extension when /312 lands** (C's lean) |
| M17 | Reverse projection emission scope? | NOT covered | §4.2 | C only | **forward only for MVP** (C's lean) |
| M18 | Box layout coordinate notation `(vector-N element-M)`? | NOT covered | §4.1 | C only | **defer to `primary-l6pc`** — but `/325` now exists, so this is stale; refer to `/325 §4` for the actual syntax |

### §5.2 Truly MVP-BLOCKING questions

Distilling further — what MUST be answered before operator can
ship `primary-ezqx.1`?

| Critical question | Pinned lean | Confidence | Source |
|---|---|---|---|
| **M1 — Layer 2/3 in or out?** | **NARROW** (Layer 2/3 POST-MVP) | High | A §3.4 + C §3.1 + /323/324 silence |
| **M2 — engine annotations in v0.1 schema?** | **NO; reader accepts-but-ignores** | High | A §3.4 + C §3.1 |
| **M11 — `next_schema` NOTA syntax?** | **`(next_schema [path])` top-level** | High | C §3.4 + already used in /164 §8.3 |
| **M12 — Date/Time primitive shape?** | **bracket-string literal; rkyv packed u32 (or 3-field)** | Medium | C §3.2; needs psyche or operator-pick |
| **M13 — Identity-vs-hand-From rule?** | **conservative: any shape diff = hand-written** | High | C §3.5 |
| **M5 — async dispatch handler?** | **async** | High | A Q5 + C §3.3 + /324 §10.2 |

The orchestrator should foreground M1, M2, M11, M12, M13, M5 as
the **six MVP-blocking pinned leans** in 6-overview. M12 is the
weakest — Medium confidence — and may be the one to surface to
psyche if the operator wants a hard pin. The others are tight
enough to land via designer authority (the leans are consistent
across A + C + /324).

### §5.3 MVP-impact-but-not-blocking questions

M3, M4, M6, M14, M17 — leans exist, operator can proceed with the
lean and revise post-pilot if wrong. M3 (field name) becomes
functionally MVP-blocking IF /322 §4.2's example reaches the emit
code through B's hardcode at `emit.rs:551-553` — but the hardcode
already exists for Spirit, so operator just inherits the current
behavior. The lean ("type-derived `magnitude`") would require
RETIRING the hardcode in MVP, which then ripples into the daemon's
field-references. Orchestrator should note this nuance.

### §5.4 Post-MVP-scope-clarity questions

M7, M8, M9, M10, M15, M16, M18 — all post-MVP per A's and C's
leans; not blocking. Orchestrator can list briefly without
recommendations.

## §6 Parallel-audit incorporation check

### §6.1 `reports/nota-designer/6-quoted-string-purge-audit-2026-05-24.md`

The nota-designer/6 audit identifies bead `primary-36iq.7.1` as the
tracker for the persona/signal bracket-string cleanup. D's Fix 1
(bracket-string sweep of /164) is a **partial absorption** of
`primary-36iq.7.1` scope (D §2.4 acknowledges this).

**Consistency check**: A §2 row 5 "Bracket-string form `[text]` for
strings/paths" cites `36iq.7.1 parallel` in the bead column. **Consistent.**

**Missed angle in nota-designer/6 + A/B/C/D collectively**: the
nota-designer audit notes "Locked Persona/signal repos still have old
examples." None of A/B/C/D address whether `signal-persona-spirit/lib.rs`
(the current Rust-syntax `signal_channel!` invocation that the
pilot replaces) carries quoted-string examples that need cleanup
BEFORE the cutover. Per /324 §5 the file is being **rewritten** to
NOTA-data input — so the cleanup is implicit. But if the rewrite
doesn't land cleanly (M1+M2 lean breaks down, scope changes), the
old quotes stick. Flag for 6-overview: cutover IS the cleanup;
schedule-risk implies quote-risk.

### §6.2 `reports/second-operator/176-designer-awareness-beads-and-report-audit-2026-05-24.md`

second-operator/176's "Main audit finding" surfaces the Layer 2/3
ambiguity FIRST (before A's report) and reaches the conclusion:
"do not silently add a broader sema-lowering layer unless the
designer or psyche explicitly pulls it into the MVP." A §3.1 +
§4.1 explicitly cite 176 as the source and extend with per-report
attribution + lean.

**Consistency check**: 176's recommendation = narrow MVP without
silent expansion. A's lean = narrow MVP with explicit POST-MVP
deferral. **Consistent.**

**Missed angle in second-operator/176 + A/B/C/D collectively**: 176
notes "report 175 refreshed through Spirit 396. Records 397-408
add the new current edge" — confirming records 397-408 are the
post-396 expansion. A's claim that "Spirit 396 is Maximum about
EVENTUAL scope, not Maximum about first MVP slice" depends on
parsing the 396 record's literal wording. 176 paraphrases 396
the same way A does. None of A/B/C/D/176 reproduce the spirit 396
record verbatim. **Recommendation**: 6-overview should cite the
exact 396 wording from the deployed Spirit (or, if Spirit isn't
queryable for the auditor, flag this as a "verify against Spirit
record before psyche-foregrounding" item).

### §6.3 No-action overlaps

The nota-designer audit's `primary-36iq.3` (Spirit profile pin/
caveat) is unrelated to /167's scope. `primary-36iq.6.1`/`6.2`
(lojix signal API ports, Nexus stale dep) are unrelated. No
contradictions across parallel audits.

## §7 The Spirit 396 reading — recommended consolidated answer

### §7.1 The four reports' paraphrases agree on the literal claim

All four reports A/B/C/D + parallel audits 176 + nota-designer/6
paraphrase spirit 396 as "the macro generates from the NOTA schema
all three outputs — the wire/signal surface, the sema operations
(classification), and the sema lowering operations (how each
operation is expressed inside the engine)."

A §3 quotes the record body verbatim from /164's citation:

```
(396 signal Decision
  [The signal_channel macro generates from the NOTA schema all
   three outputs — the wire/signal surface, the sema operations
   (classification), and the sema lowering operations (how each
   operation is expressed inside the engine, what kind of decision
   the engine makes).]
  Maximum)
```

(A's citation appears at /1-mvp-scope-clarification.md:220-228.
The literal record is in the deployed Spirit and was queryable at
the time A wrote the report. This auditor cannot independently
verify against Spirit because the `spirit` CLI's `Query`/`Help`/
`GetEntry`/`GetRecord` heads are all rejected by the deployed
binary — confirming the nota-designer/6 caveat about the deployed
Spirit profile pin. The four reports' triangulation gives high
confidence on the paraphrase.)

### §7.2 The reconciliation

Spirit 396 is **Maximum certainty about WHAT the macro should
EVENTUALLY produce**: wire + sema-operations + sema-lowering.

Spirit 396 is **NOT** a statement that "the first MVP slice
includes all three outputs". The record's text says "the macro
generates" — present tense about a future capability.

Subsequent intents 405, 406, 407 (all Maximum) narrow the MVP
scope:
- 405: "MVP Spirit should run on schema-derived signal code." (Note:
  signal, not sema.)
- 406: "Upgrade code compile-time-optional per main/next pair." (Per
  type; not per Command/Effect.)
- 407: "Short headers drive receive-side dispatch triage." (Wire-
  side dispatch, not engine dispatch.)

These three later intents are **specific** about wire + projection +
header-dispatch as MVP. They DON'T specify Layer 2/3 as MVP. The
inference: 405-407 narrow 396's "all three layers eventually" to
"Layer 1 + dispatch + projection for MVP, Layer 2/3 later."

### §7.3 No contradiction with 396's Maximum certainty

A narrow MVP is **not** a contradiction with 396 — it's a
sequencing choice. 396 says "macro emits all three"; the MVP
delivers the first slice (Layer 1 + dispatch + projection) and
defers the rest to a follow-up bead (A's proposed `primary-ezqx.4`).

The macro EVENTUALLY emits all three. The first MVP slice emits
the wire-side subset.

The risk: if psyche reads 396 as "first MVP slice = all three",
then 405-407's narrower scope is a contradiction. The four reports
collectively LEAN that 405-407's narrower framing is psyche's
intent (because it's later + more specific). Confirm if uncertain.

### §7.4 Recommended consolidated answer for 6-overview

> Spirit 396's Maximum certainty applies to the macro's eventual
> three-layer emission. Intents 405-407 (also Maximum) narrow the
> MVP first slice to Layer 1 (wire + ShortHeader emit) + wire-side
> dispatch + per-type projection. Layer 2 (Command/Effect/
> ToSemaOperation/ToSemaOutcome) and Layer 3 (engine routing) are
> POST-MVP, tracked as `primary-ezqx.4` per A §3.5. /322 §6.3 +
> /324 §5 + /324 §6 + /323's silence on Layer 2/3 derivation all
> support this narrowing.

## §8 What the orchestrator should foreground in 6-overview.md synthesis

### §8.1 Six pinned MVP-blocking leans (from §5.2)

M1, M2, M5, M11, M12, M13 — with confidence levels and source
attribution per §5.2 table.

### §8.2 The Spirit 396 reading

Per §7.4 above — this is the load-bearing scope decision.
6-overview should state the consolidated answer and flag M12
(Date/Time shape) as the only Medium-confidence pin.

### §8.3 Five immediate operator pickups

1. Land M3 (field name `magnitude`) by retiring `emit.rs:551-553`
   hardcode (B §4.3 catch).
2. Close the bead-state drift items A §4.3 (verify `primary-ezqx.2`
   reflects closure — **VERIFIED CLOSED already per `bd show`**)
   and A §4.4 (update `primary-ezqx.1` acceptance text to match
   /324 §7 — STILL OPEN per `bd show primary-ezqx.1`).
3. Operator picks up `primary-ezqx.1` Wave 1 (M1+M2+M11+M13 are
   the closed shape; M12 needs the Date/Time rkyv decision pinned
   via library-pick at code-time).
4. Operator picks up `primary-l6pc` in parallel (the `nota-box`
   library; /325 design exists).
5. Operator picks up `primary-x3ci.1` (pre-migration + hard-handover
   + marker per /323 §10.5) — independent of pilot but on the
   critical path for production cutover.

### §8.4 Two parallel-audit threads to acknowledge

`reports/nota-designer/6` partial absorption via D's Fix 1.
`reports/second-operator/176`'s Layer 2/3 finding extended by A §3.

### §8.5 One scope-clarity item

C's Date/Time bracket-string literal recommendation + rkyv encoding
choice should be either pinned in 6-overview or flagged as the one
M-question requiring psyche confirmation. The text on its own
isn't enough to settle whether rkyv encoding is 3-field-each or
packed-u32; operator can pick at code-time if 6-overview defers.

### §8.6 One uncertainty to carry

The `OperationDispatch` vs engine-routing distinction (C §3.1) is
not currently explicit in /323 or /324. 6-overview should state
the distinction clearly and recommend a /324 or /323 amendment
making it explicit. Per the carry-uncertainty discipline
(`skills/architecture-editor.md`), this can land as "Medium
certainty: 6-overview's reading; designer to confirm via amend
or new report."

## §9 See also

### Reports cross-checked

- `reports/second-designer/167-mvp-advance-and-fix/0-frame-and-method.md`
  (orchestrator's frame)
- `reports/second-designer/167-mvp-advance-and-fix/1-mvp-scope-clarification.md`
  (A — 752 lines)
- `reports/second-designer/167-mvp-advance-and-fix/2-macro-implementation-gap.md`
  (B)
- `reports/second-designer/167-mvp-advance-and-fix/3-design-clarifications-needed.md`
  (C — 544 lines)
- `reports/second-designer/167-mvp-advance-and-fix/4-operator-fixes-executed.md`
  (D)
- `reports/nota-designer/6-quoted-string-purge-audit-2026-05-24.md`
  (parallel external audit — bracket-string sweep)
- `reports/second-operator/176-designer-awareness-beads-and-report-audit-2026-05-24.md`
  (parallel external audit — Layer 2/3 finding source)
- `reports/designer/320-mvp-schema-language-pilot-unblock.md`
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md`
- `reports/designer/323-mvp-scope-expansion-per-operator-directive.md`
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md`
  (canonical re-spec; the file map at /324 §5 silently omits
  Layer 2/3 emissions — load-bearing for M1's lean)
- `reports/designer/325-nota-box-library-design-and-implementation.md`
  (landed during Wave 1; supersedes C §4.1's "defer to `primary-l6pc`"
  framing — design now exists)
- `reports/second-designer/164-nota-schema-language-vector-of-root-verb-enums-2026-05-24.md`
  (D's Fix 1 target — spot-checked at lines 231, 556, 955)
- `reports/second-designer/163-signal-sema-interaction-and-spirit-architecture-2026-05-24.md`
  (D's Fix 2 target — terminology preservation verified)
- `reports/second-designer/166-self-audit-2026-05-24.md`
  (D's fix-list source; orchestrator's grounding for D's scope)
- `/git/github.com/LiGoldragon/sema-engine/ARCHITECTURE.md`
  (D's Fix 3 target — verified at lines 109 + 117)

### Verification commands run

- `jj log -r 'main | main@origin'` in `/home/li/primary` — **main
  at 4052aa10c0cd (yzssuznxsukp); main@origin matches; D's push
  + backfill landed**.
- `jj log -r 'main | main@origin'` in `/git/github.com/LiGoldragon/sema-engine`
  — **main at 6a552182ef33 (nxxoouzlprpx); main@origin matches;
  D's ARCH push landed**.
- `bd show primary-ezqx.1` — open P1; body still references /320
  sizing (A §4.4's caveat valid).
- `bd show primary-ezqx.2` — **CLOSED** with reason "scope absorbed
  into primary-ezqx.1 per /323 §3.2 + §5.2"; A §4.3 satisfied.
- `bd show primary-l6pc` — open P1; nota-box library bead.
- `bd show primary-x3ci.1` — open P1; pre-migration + hard-handover.
- Spot-check reads on /164 lines 231, 248, 294, 367, 555-556,
  569, 912-920, 955, 979, 1059 — D's edits verified.
- Spot-check reads on /163 lines 191-202, 800-813 — D's
  terminology pass verified; three-tier framework preserved.
- Grep for `Tier 1 micro\|Tier 1 small\|small-object Tier 1\|small-message Tier 1`
  in /163 — **zero hits** (D's retired-name removal complete).
- Grep for `signal-core\|signal_core` in sema-engine ARCH — **zero
  hits** (D's dep-name fix complete).

### Skills consulted

- `/home/li/primary/skills/nota-design.md` (case rules — informed
  C §3.2 Date/Time parsing critique).
- `/home/li/primary/skills/component-triad.md` (informed §3.1
  schema-component scope clarity).
- `/home/li/primary/AGENTS.md` (auditor-role guidance — intent 234
  + 235 framing).
