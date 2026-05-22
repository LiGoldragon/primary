# 19 — Refresh after prime-designer session, 2026-05-22

*Refresh of /18 after absorbing the prime-designer session that
dispatched parallel subagents under designer protocol (intent record
57) and produced /281/282/283/284 + 37 new spirit records (157-193).
/18's question list has substantial settlements; this report carries
forward only what's still open and adds the important new questions.
Light edit landed in `orchestrate/roles.list` (added `nota-designer`
+ documented specialized-role pattern).*

## 1. Frame

Between my /18 (around 13:00 local) and now (around 15:40), the prime
designer ran a heavy parallel-subagent session producing:

- **/281** updated — Pi headless research with banner noting the
  "depend on pi-ai" recommendation is SUPERSEDED by persona-llm-client
  direction (records 152+158).
- **/282** — workspace implementation status snapshot. ~30-35% of
  named architecture exists as code. 35-gap /249 inventory updated:
  3 closed, 8 partial, 24 open.
- **/283** — session summary; 17 reports reviewed, 35 bead-label
  cleanups, /269 dropped (substance preserved in skills + records).
  10 next-session beads filed. **Designer pivots to /249 gap-closure
  as primary focus next session (bead `primary-c2da`).**
- **/284** — per-type Migration trait specification. Migration crate
  + signal-version-coordination contract + MigrationIndex compile-time
  catalogue + cross-version recovery via persona-introspect. Worked
  example: Spirit 0.1.0 → 0.1.1 Certainty→Magnitude.

Parallel to the prime session, second-operator-assistant and
context-maintenance subagents ran heavy sweeps:

- ~100 stale reports retired.
- 35 bead labels cleaned up.
- `intent/*.nota` append flow officially retired in operator
  AGENTS.md (intent-via-Spirit-FIRST rule).
- Skill files updated (`skills/architecture-editor.md` gained §"Carrying
  uncertainty"; `skills/nota-design.md` created with canonical-NOTA
  rewrite of `skills/skills.nota`).

## 2. What's settled (since /18)

Mapping /18's Q1–Q27 against spirit records 157-193:

| /18 Q | Status | How |
|---|---|---|
| Q1 (Spirit cutover routing) | **SETTLED: dual-write** | Spirit record 163. |
| Q2 (Stop-old-start-new for migration 1) | **N/A** | Dual-write is the path. Single-step cutover is bypassed. |
| Q3 (EffectEmitted payload type) | **Still open** | Not addressed in 157-193. |
| Q4 (Lane-identifier reservation) | **SETTLED: not reserved** | Per second-operator/165 + /283's cleanup; intent 117/118 effectively superseded. /149's follow-up retires. |
| Q5 (Sema-upgrade self-upgrade bootstrap) | **Still open** | Standing-by per /283. Designer lean: hand-written first. |
| Q6 (Commit-sequence scope) | **Still open** | Per /283. Designer lean: per-database. |
| Q7 (Engine-manager Axis 2 timing) | **Still open** | Per /282 §10 #6. |
| Q8 (Magnitude collapse) | **SETTLED: yes via Unknown variant** | Spirit record 165 — add `Unknown` to `Magnitude`; Health/Readiness collapse via field-name-carries-dimension. Bead `primary-gjs5` carries the v0.1.2 widening. |
| Q9 (RejectionReason fanout) | **Still open** | Same slice as `primary-l3h5`. |
| Q10 (Forge boundary timing) | **Direction settled (intent 154); timing operator-scheduling** | Existing forge stays; forge-nix-builder extracts. |
| Q11 (Orchestrate executor migration timing) | **Still open** | Bead `primary-c620` in flight; per /283 the designer pivots elsewhere. |
| Q12 (Pi/DeepSeek wrapper shape) | **SETTLED: new component + Rust RPC baseline** | Records 157 (DeepSeek-into-persona-pi superseded), 158 (`persona-llm-client` is the new component — workspace-native lightweight LLM client library, embeddable in daemons), 175 (build Rust RPC wrapper for headless Pi as useful baseline alongside). |
| Q13 (Persona-pi vs sema-upgrade vs Spirit priority) | **SETTLED: /249 gap closure first** | Spirit record 166. Designer pivot. |
| Q14 (`persona-listen` 11 questions) | **Still open + new design** | Records 159+162 affirm component direction (`persona-listen` + `persona-speak`) but the 11 questions still need triage. |
| Q15 (STT model — Gemma 4 audio?) | **Still open** | Verification not done. |
| Q16 (Agent identity before Criome) | **Partially settled** | Record 125 says BLS-from-day-one; record 134 says pre-Criome ephemeral BLS key migrates cleanly. `second-designer/150` carries the design. |
| Q17 (Mind channel-choreography verbs) | **Still open — /249 Gap #1** | One of the 24 open /249 gaps. |
| Q18 (Lojix vision gaps) | **Still open** | 8 gaps per `system-assistant/28`. |
| Q19 (Bird→Zeus authority scope) | **SETTLED: LiGoldragon main** | Spirit record 176 — Bird/Zeus uses LiGoldragon main by default, not per-user branches. First allowed action set still open follow-up. |
| Q20 (owner-signal-persona repo) | **Still open** | /282 confirms 3 missing (harness, message, system); persona engine-manager has no owner repo. |
| Q21 (Lane registry format extension) | **Resolved by convention** | Bare lines used for specialized lanes (cluster-operator, nota-designer); comment added to `roles.list` this session. |
| Q22 (Asymmetric Spirit release) | **Still open** | Spirit ordinary at v0.1.1, owner at v0.1.0. Likely intentional (no owner schema change) but unconfirmed. |
| Q23 (Designer protocol coverage for parallel-mains) | **SETTLED: lanes share persona** | Spirit record 173 — designer lanes are different windows into the same persona; share context through workspace files plus per-session work summaries. All parallel-main designer lanes inherit designer-protocol carve-out. |
| Q24 (nota-designer / cluster-operator registration) | **Closed for now** | Both lanes registered as bare lines in `roles.list`; specialized-role pattern documented this session. Typed registry handles role-vector form natively. |
| Q25 (Concept-designer lane) | **SETTLED: ephemeral, not persistent** | Spirit record 147 — concept designer is an ephemeral occasional invocation, not a persistent named lane. |
| Q26 (Criome owner-session encryption priority) | **Still open** | Behind /249 gap closure pivot. |
| Q27 (Old operator /108-/135 cleanup) | **SETTLED** | Done in context-maintenance sweeps. |

**Net: 11 settled / 1 resolved by convention / 2 N/A or partial / 13 still open from my /18.**

## 3. Still-open questions from /18

Carried forward unchanged:

- **Q3 — EffectEmitted payload type**. Typed `Effect` (component-local)
  or universal `SemaObservation`? 7+ pending observable blocks across
  mind/router/message/introspect/system/terminal/harness wait on this.
- **Q5 — Sema-upgrade self-upgrade bootstrap**. Designer lean:
  hand-written until contracts stabilise.
- **Q6 — Commit-sequence scope**. Per-database or per-component?
- **Q7 — Engine-manager Axis 2 timing**. Land-now or defer-explicitly?
  Bead `primary-k2mh` doesn't currently list this axis.
- **Q9 — RejectionReason fanout** for sema-upgrade daemon (5 variants
  on `primary-l3h5`).
- **Q11 — Orchestrate executor migration timing**. Continue
  `primary-c620` slice or pause for Spirit cutover?
- **Q14 — persona-listen / persona-speak 11 questions** (component
  name, buffer window, voice enrolment, gesture, marker vocabulary,
  triad shape, wife's parallel persona, laptop-side process, etc.).
- **Q15 — STT model verification**. "Gemma 4 multi-modal" — actually
  audio-input? Substitute Phi-4-mm / Qwen2-Audio / Ultravox / Voxtral?
- **Q16 — Agent identity timing** — start with BLS ephemeral keys
  now or wait for Criome?
- **Q17 — Mind channel-choreography verbs** (`/249` Gap #1).
- **Q18 — Lojix vision gaps** — 8 items per `system-assistant/28`.
- **Q20 — owner-signal-persona repo** — engine-manager has none;
  intentional?
- **Q22 — Asymmetric Spirit release** — owner at v0.1.0 deliberate?
- **Q26 — Criome owner-session encryption priority** — relative to
  /249 gap closure.

## 4. Important new questions from /282/283/284

### From /284 (per-type Migration trait spec)

These are designer-leans waiting for psyche confirm:

- **N1 — Crate name `migration`**? `/284` §8 lean: yes (full English
  word at signal-sema's tier of generality). Two alternatives
  considered (`migration-trait`, `versioning`).
- **N2 — Historical contract versions as sibling repos**?
  `signal-persona-spirit-v0-1-0` as a separate git repo, frozen,
  added to `MigrationIndex`. Alternative: feature-flagged sub-crates.
  `/284` lean: sibling repos.
- **N3 — `signal-version-coordination` as separate crate**? Lean:
  separate (triad-style, round-trip-testable).
- **N4 — `owner-signal-version-coordination`**? Lean: don't ship yet.
- **N5 — PeerCheck on each component's working contract OR on
  `signal-version-coordination`**? Lean: PeerCheck on each component
  (component-specific), CoordinateBack on signal-version-coordination
  (universal).
- **N6 — `CONTRACT_VERSION` before the schema generator exists**?
  Lean: hand-edited const computed by a small CLI tool that hashes
  the schema file; discipline that const must be re-run on every
  contract edit.

### From /282 (implementation status snapshot)

- **N7 — `persona-llm-client` design**: library vs triad? Spirit
  records 157+158 settled the direction but not the shape. Bead
  `primary-lyc8` PARKED.
- **N8 — `persona-listen` + `persona-speak` triad shape**;
  `signal-real-time` storage format (record 162 says probably native
  real-time, not Sema). Bead `primary-voz5` PARKED, bead `primary-m8xv`
  PARKED.
- **N9 — Missing owner-signal-* repos** (now 3: harness, message,
  system). Emergence criteria unwritten. `/249` Gap #9.
- **N10 — Spirit-to-mind owner-contract verb set** (`/249` Gap #1).
  Blocks the moment integration begins.

### From /283 (session housekeeping)

- **N11 — Designer pivot ratification**. Per record 166 the designer
  pivots to /249 gap closure (bead `primary-c2da`). Confirm or
  redirect. New-component design tasks (`primary-lyc8` llm-client,
  `primary-voz5` listen+speak, `primary-m8xv` real-time) are PARKED
  by default.
- **N12 — `signal-sema/ARCHITECTURE.md` uncommitted edits** in
  `/git/.../signal-sema/` — Magnitude vocabulary section. Land?
  Bead `primary-gjs5` carries the Unknown widening follow-up.

### From spirit records 177-193 (multi-version dispatch protocol)

Most are settled decisions, but two deserve flag:

- **N13 — Migration trait placement decision** (record 188) — `/284`
  proposes a new `migration` crate; awaits psyche confirm before
  implementation.
- **N14 — Version handover protocol** (records 186-193) — explicit
  daemon protocol for cross-daemon cutover; after handover, main is
  private-upgrade writable only. Design fleshing-out needed; `/284`
  is the canonical spec but the actual cutover protocol bead doesn't
  exist yet.

## 5. AGENTS.md discipline changes this session

Per /283:

- **Operator landed**: intent-via-Spirit-FIRST rule. No more
  `intent/*.nota` append fallback during normal work. `intent/` is
  legacy file substrate; do not append.
- **Designer landed**: "No harness-dependent memory" → "No
  harness-dependent memory; session-scoped tools land in workspace
  files." TaskCreate / agent-UI / scratchpad allowed but substance
  must land in workspace files before session ends (intent record 172).

## 6. Workspace edits I landed this session

Small focused changes within third-designer Structural authority:

- `orchestrate/roles.list`: `nota-designer` registered as bare line
  (cluster-operator was already added by another lane); comment block
  extended to document the specialized-role / role-vector pattern
  per intent records 156 + 174. Bare-line convention chosen until the
  typed persona-orchestrate registry takes over.

No edits to skills/role-lanes.md or AGENTS.md role table yet — those
are larger sweeps that should bundle with the /249 gap-closure pivot.

## 7. Next pickup priorities (updated from /18 §8)

Spirit cutover questions are resolved at the routing level (dual-write
per intent 163); the operator-side work is the dual-write wrapper
implementation. The next-wave queue shifts:

1. **Spirit dual-write wrapper** — bead `primary-chpq`. Operator slice.
   Direction settled (intent 163); implementation only.
2. **`primary-c2da` /249 gap-closure sweep** — DESIGNER PRIMARY FOCUS
   per record 166. Re-read /249, update with /282 deltas, prioritize
   24 remaining gaps, close one at a time.
3. **persona-orchestrate executor migration** — `primary-c620`,
   `second-operator/166` 9-step plan. Operator slice; independent
   of cutover.
4. **u8vo epic decomposition** — split into per-contract beads.
   Designer slice (mine or another designer parallel-main).
5. **`primary-ib5n` sema-upgrade architecture merge** — canonical
   merge of /263, /270, /273, /279, /284 substance + bead.
6. **`primary-gjs5` Magnitude Unknown widening for v0.1.2** —
   signal-sema/ARCHITECTURE.md edits + code.
7. **persona-introspect Package 1** — bead `primary-li7a`,
   `second-designer/144`. Awaits Q3 (EffectEmitted payload).
8. **Engine-manager Axis 2 re-audit** — `primary-k2mh` audit partly
   stale; check current source first.
9. **Foundation hygiene pile** — `primary-k3bu`, `primary-77hh`,
   `primary-u0lh`, `primary-uy7o`, `primary-dzrn`.
10. **Per-type Migration trait implementation** — Operator pickup
    from `/284` spec; depends on N1–N6 psyche confirmations.

Parked (per intent 166):
- `primary-lyc8` persona-llm-client design
- `primary-voz5` persona-listen + persona-speak design
- `primary-m8xv` signal-real-time capability design
- `primary-u7gc` persona-pi/ARCH from /266

## 8. References

**Reports added this refresh window:**
- `/282` — workspace implementation status snapshot
- `/283` — prime designer session summary
- `/284` — per-type Migration trait specification
- `/281` — Pi headless research (banner-updated, partially superseded)

**Spirit record numbers absorbed:** 157-193 (37 records, 14 settling
prior /18 questions, 12 introducing new concerns, 11 housekeeping).

**Prior third-designer reports:**
- `/17` — situation and questions (mostly superseded by /18 then /19).
- `/18` — audit synthesis post triple-audit (Q1, Q4, Q8, Q12, Q13,
  Q19, Q21, Q23, Q24, Q25, Q27 closed since publish).

This report retires when the picking-up agent has triaged N1–N14 +
the still-open Q list and the next concrete designer slice
(`primary-c2da` /249 gap-closure) is underway.
