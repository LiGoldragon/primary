# 86 · Handoff from context reset — 2026-05-08

Status: handoff for next-session-me. The user is about to
restart me on a fresh context. This report is the
**single index** to the current state of the design pair's
work. Read this first; then read the 5 required files in §3;
then act on §6.

Author: Claude (designer)

---

## 0 · TL;DR

You are the **designer** in the design pair (user + you).
The implementation pair (operator/Codex + new
assistant/Codex) is now bootstrapped and shipping work.

Two load-bearing user decisions landed today (2026-05-08):

- ✅ **A.2 — harness boundary text language = Nexus.**
- ✅ **A.5 — Commands naming = noun-form.**

A bold-letter ban on new text formats landed in
`skills/language-design.md` §0 — refuse any "PersonaText",
"HarnessText", etc. on sight.

Your queue (§6):
1. designer/87 convergence with operator/83 + assistant/82
   (~30 min)
2. signal-persona-orchestrate MVP contract design
3. signal-persona-terminal scaffold under Nexus discipline
4. Open Bucket A items: A.1 ZST exception, A.3 terminal
   adapter protocol, A.6 Authorization shape, A.7 snapshot
   vs log-replay, A.8 nota-codec::expect_end home

---

## 1 · Where you are

**Workspace:** `/home/li/primary/`. Git repo. `jj` for VCS
(use `jj commit -m`, never `jj describe @`; **read `jj st`
before every commit** — commit-bundling races have bit me
multiple times).

**Roles** (per `protocols/orchestration.md`):
- `designer` — you. Lock file: `designer.lock`. Reports:
  `reports/designer/`.
- `operator` — Codex. Lock: `operator.lock`. Reports:
  `reports/operator/`.
- `assistant` — Codex (new role, just bootstrapped).
  Lock: `operator-assistant.lock`. Reports: `reports/operator-assistant/`.
- `system-specialist` — any. Lock: `system-specialist.lock`.
- `poet` — any. Lock: `poet.lock`.

**Design pair you + user:** authors contracts, skills,
ESSENCE/AGENTS/protocols, design reports. Slow & deep.

**Implementation pair operator + assistant:** writes Rust,
tests, runs nix flake check, maintains per-repo
ARCHITECTURE.md / skills.md drift fixes, mechanical
refactor passes. Fast & broad.

The model is in `reports/designer/81-three-agent-
orchestration-with-assistant-role.md`. Read it.

---

## 2 · Today's pulse — what landed (2026-05-08)

### Designer (me) landed:
- `reports/designer/79` — architecture audit (41 ARCH.md
  files; 8 missing Inbound/Outbound sections per
  operator/77 §2 skeleton)
- `reports/designer/80` — open-questions inventory (23
  questions; A.2 + A.5 now resolved inline)
- `reports/designer/81` — three-agent orchestration model
  with `assistant` role
- `skills/language-design.md` §0 update — **"No new text
  formats. Ever."** bold-letter rule
- Sweep: PersonaText / "named projection" / "harness text
  language" stale refs across designer/68, /70, /72, /80
- BEADS: `primary-kxb` commented (2 of 4 sub-questions
  resolved); filed `primary-28v` (noun-form sweep) +
  `primary-b7i` (body→Nexus migration)

### Operator (Codex) landed:
- Wire-integration: `persona-system`, `persona-message`,
  `persona-router` use portable git Cargo deps + consume
  `signal-persona-system`. Three repos green.
- `reports/operator/83` (renamed from /82) —
  feedback on designer/81; 8 substantive points + 1
  disagreement (operator must run `nix flake check`
  *before* push; assistant verifies independently *after*).

### System-specialist landed:
- `assistant` role infrastructure: `skills/operator-assistant.md`,
  `AGENTS.md` update, `protocols/orchestration.md` update,
  `tools/orchestrate` role list, `reports/operator-assistant/`
  directory. Commit `651413a7`.

### Assistant (Codex, new) landed:
- `reports/operator-assistant/82` — feedback on designer/81 (mode A
  default, audit-first lane, single daily summary +
  dedicated reports for structural findings)
- `reports/operator-assistant/85` — first audit of operator's
  signal-persona-system integration. **Key finding:**
  `DeliveryGate` exists in `persona-router/src/delivery.rs`
  consuming `signal_persona_system::{FocusObservation,
  InputBufferObservation, InputBufferState}`, but
  `RouterActor` (in `src/router.rs`) doesn't use it yet
  — daemon still reads NOTA lines + `RouterInput::from_nota`.
  This is the next architectural-truth witness target.

### Poet (Claude subagents) landed:
- `reports/poet/84` — vision-OCR trial of
  caraka-1922-nirnaya-sagar.

---

## 3 · Required reading (5 files, ~1500 lines total)

Read these end-to-end. They are the minimum context to act.

1. **`ESSENCE.md`** — workspace intent. Always upstream.
2. **`AGENTS.md`** — workspace agent contract. Includes
   the new `assistant` role.
3. **`reports/designer/81-three-agent-orchestration-with-
   assistant-role.md`** — the working model for the
   design pair / implementation pair split.
4. **`reports/operator/83-operator-feedback-on-assistant-
   orchestration.md`** — operator's adjustments to
   designer/81 (8 substantive points; convergence pending
   in your queue).
5. **`reports/operator-assistant/82-three-agent-orchestration-
   feedback.md`** — assistant's answers to the 6 questions
   in designer/81 §11 (Mode A default, audit-first lane).

After those 5, you'll have the joint working model.

---

## 4 · On-demand reading (when topic comes up)

| When you need... | Read |
|---|---|
| Any text-format question | `skills/language-design.md` §0 (bold-letter rule) |
| Open questions / decisions still pending | `reports/designer/80` (post-update; A.2/A.5 marked resolved) |
| Architecture-file gaps | `reports/designer/79` |
| Current Task A/B assignment with operator | `reports/designer/78` |
| Channel inventory | `reports/operator/77` §4 |
| Apex Persona design | `reports/designer/4` |
| Sema kernel architecture | `reports/designer/64` |
| Assistant's first audit findings (router gap) | `reports/operator-assistant/85` |
| Contract repo design conventions | `skills/contract-repo.md` |
| Architectural-truth test discipline | `skills/architectural-truth-tests.md` |
| jj discipline (load-bearing) | `skills/jj.md` |
| Reporting conventions | `skills/reporting.md` |
| Rust enforcement (verb-belongs-to-noun, ZST rule, etc.) | `skills/rust-discipline.md` |
| Designer role itself | `skills/designer.md` |

---

## 5 · Skip end-to-end (snapshots — read only if user asks for history)

These are durable history but mostly superseded by current
reports. Each has a stale-banner at the top pointing to
its successor.

| Stale | Superseded by |
|---|---|
| `reports/designer/68` (workspace amalgamation snapshot) | `/79` + `/80` + `/81` |
| `reports/designer/70` (code stack amalgamation snapshot) | `/80` + `/81` |
| `reports/designer/72` (harmonized implementation plan) | `/78` (Task A/B) + `/80` (open questions) + `/81` (orchestration) |
| `reports/designer/73` (signal-derive research) | Defunct decision: defer signal-derive |
| `reports/designer/76` (macro + parallel plan) | `/78` (convergence) + `/81` (orchestration) |

These have stale-banners; trust the banners.

---

## 6 · Designer pair queue — pick up here

### 6.1 · designer/87 — convergence with operator/83 + assistant/82 (~30 min)

Like designer/78 was for operator/77. Short. Lock in:
- Mode A default; Mode B for path-disjoint mechanical
- Audit-first for assistant
- Daily-summary + dedicated-report split
- Cross-review threshold (~80 LoC + 6 always-full triggers)
- Operator runs `nix flake check` before push; assistant
  verifies independently after (concede operator/83 §8)
- Assistant's channel preference: signal-persona-system
  audit done → `primary-0cd` warm-up → persona-harness /
  signal-persona-harness next → not signal-persona-terminal
  yet (per operator/83 §4)

This becomes the joint working model.

### 6.2 · `signal-persona-orchestrate` MVP contract design

Per designer/81 §4.2 + operator/77 §4. Operations already
known (designer/64 §4 + designer/4 §5):

- `Claim(role, scope, reason)` →
  `ClaimAccepted` | `ClaimRejected(reason)`
- `Release(role)` → `Released`
- `Handoff(from, to, scope, reason)` →
  `HandoffAccepted` | `HandoffRejected`
- `Observe(role)` →
  `Observation { active_scopes, active_tasks }`

**Naming under noun-form discipline** (per A.5):
- `RoleClaim`, `ClaimAcceptance`, `ClaimRejection`
- `RoleRelease`, `ReleaseAcknowledgment`
- `RoleHandoff`, `HandoffAcceptance`, `HandoffRejection`
- `RoleObservation`

This unblocks operator's Task 2 (persona-orchestrate first
slice) to start in parallel with Task 1.

### 6.3 · `signal-persona-terminal` scaffold

Now unblocked (A.2 = Nexus). Per designer/81 §4.1, can
ship the channel surface even though the typed Nexus body
migration in signal-persona-message is its own follow-up
(`primary-b7i`).

**Per operator/83 §4 caveat:** scaffold must be described
as "typed contract carrying Nexus payload" — never as
a new text language.

### 6.4 · Bucket A items still open

- **A.1 ZST exception** for `Bind`/`Wildcard`/`Tail`/etc.
  — needs user judgment.
- **A.3 terminal adapter protocol** — internal PTY vs
  Signal at boundary. Designer leans Signal.
- **A.6 First Authorization shape** — becomes blocking
  after operator's Task 1.
- **A.7 Snapshot vs log-replay** — same.
- **A.8 nota-codec::expect_end** home — cleanup.

Surface these to the user when conversation pulses near
them. Don't pre-design.

### 6.5 · Implementation pair's queue (for awareness, not your work)

- **Operator:** continue `persona-router` migration so
  `RouterActor` actually uses `DeliveryGate` (per
  assistant/85 §3.1). Then Task 2 (persona-orchestrate
  first slice).
- **Assistant:** warm-up `primary-0cd` (endpoint.kind
  enum) → audit operator's next slice → maybe
  signal-persona-harness consumer.

If user asks "what's the implementation pair doing?",
point at operator/83, assistant/82, assistant/85.

---

## 7 · Active workspace state (snapshot 2026-05-08 evening)

### 7.1 · Locks (gitignored runtime state)

Lock files are gitignored. Read with `tools/orchestrate
status` or `cat <role>.lock`. State at handoff time may
have shifted; always re-check.

### 7.2 · Channel inventory

| Contract | Status |
|---|---|
| `signal-persona-message` | ✅ shipped (needs `MessageSubmission` rename + body→Nexus migration) |
| `signal-persona-system` | ✅ shipped (needs `FocusSubscription` rename) |
| `signal-persona-harness` | ✅ shipped (needs `MessageDelivery`, `InteractionSurfacing`, `DeliveryCancellation` renames) |
| `signal-persona-terminal` | ⏳ to design (your queue §6.3) |
| `signal-persona-orchestrate` | ⏳ to design (your queue §6.2) |

### 7.3 · Operator's pipeline

- ✅ Task A — persona-store retirement
- ✅ Wire-integration (3 repos consume signal-persona-system)
- 🔄 Task 1 in progress — `persona-router` ractor + sema +
  use of `DeliveryGate` from `RouterActor` (assistant/85
  §3.1 found this gap)
- ⏳ Task 2 — `persona-orchestrate` first slice (gated on
  signal-persona-orchestrate contract from your §6.2)
- ⏳ End-to-end nix-chained witness

### 7.4 · BEADS — relevant open

| Bead | What |
|---|---|
| `primary-kxb` | Open architectural decisions — 2 of 4 resolved (A.2 + A.5 today); 2 still open (ZST exception + terminal protocol) |
| `primary-28v` | **NEW today** — noun-form rename pass across signal-persona-* contracts |
| `primary-b7i` | **NEW today** — `body: String` → typed Nexus record migration |
| `primary-0cd` | endpoint.kind closed enum (assistant warm-up) |
| `primary-0p5` | persona-sema typed Tables (P1, load-bearing) |
| `primary-2w6` | persona-message off polling onto persona-sema (P1) |
| `primary-3fa` | FocusObservation contract convergence (designer half done in /80; operator/assistant rename pass needed) |
| `primary-186` | persona daemons adopt ractor (operator's Task 1 covers RouterActor) |
| `primary-tlu` | Persona\* prefix sweep |
| `primary-4zr` | sema kernel hygiene batch |
| `primary-9h2` | critical-analysis role — substantially resolved by `assistant` role; meta-question remains |

---

## 8 · Decisions locked in 2026-05-08

| # | Decision | Reasoning |
|---|---|---|
| A.2 | Harness boundary text = **Nexus** | "Nota is the format; Nexus is the Nota-implemented vocabulary; Nexus is basically all the text we use" — user verbatim |
| A.5 | Commands naming = **noun-form** | "Messages are things; verbs are when things are run through an engine — those are method names" — user verbatim |
| Bold-letter rule | `skills/language-design.md` §0 | Refuse any "PersonaText" / "HarnessText" / "MessageLang" etc. on sight; CLI sugar must desugar 1:1 to Nexus |
| Two-pair model | designer/81 + operator/83 + assistant/82 | Design pair (user + you) authors; implementation pair (operator + assistant) implements |
| Mode A default | operator/83 + assistant/82 | Operator-leads / assistant-reviews for safety-critical paths; Mode B (channel-disjoint) only for mechanical |
| Operator nix-checks before push | operator/83 §8 disagreement | Concede: operator runs `nix flake check` BEFORE push; assistant verifies AFTER as second layer |

---

## 9 · Critical state-of-mind for next-you

1. **You are the design pair half.** Don't drift into
   implementation. If the user pulses an implementation
   question, write a design output (skill / contract /
   report) — let the implementation pair execute it.

2. **Don't redesign during conversation.** When the user
   pulses, capture the decision in a durable file
   (skill, contract, report). Never just "remember it"
   — memory is harness-private (per `AGENTS.md` §"No
   harness-dependent memory").

3. **`jj st` before every commit.** Commit-bundling
   races have bit me 3+ times today (designer/76 noted;
   designer/81 itself got bundled into system-specialist's
   commit). Use partial-commit flow if anything unrelated
   is in the working copy.

4. **No new text formats. Ever.** When you see "PersonaText"
   or "harness text language" in a discussion, refuse on
   sight per `skills/language-design.md` §0.

5. **Noun-form for typed records.** `MessageSubmission`,
   not `SubmitMessage`. This is now the discipline.
   Verbs are method names.

6. **The exploratory-question rule.** From the system
   prompt: "For exploratory questions, respond in 2-3
   sentences with a recommendation and the main tradeoff.
   Present it as something the user can redirect, not a
   decided plan." Honor this — keep chat tight.

---

## 10 · How to bootstrap quickly on next session

```
1. Read THIS report end-to-end (you are now)
2. Read ESSENCE.md
3. Read AGENTS.md
4. Read reports/designer/81-three-agent-orchestration-with-
   assistant-role.md
5. Read reports/operator/83-operator-feedback-on-
   assistant-orchestration.md
6. Read reports/operator-assistant/82-three-agent-orchestration-
   feedback.md
7. Skim reports/operator-assistant/85-signal-persona-system-
   integration-audit.md (the router gap)
8. Run `tools/orchestrate status` to see live claims
9. Run `bd list --status open --limit 25` to see live BEADS
10. Pick from §6 queue and propose to user
```

Total: ~30 min reading, then act.

---

## 11 · See also

- `~/primary/ESSENCE.md` — workspace intent
- `~/primary/AGENTS.md` — agent contract; `assistant` role
- `~/primary/protocols/orchestration.md` — claim flow
- `~/primary/skills/designer.md` — your role
- `~/primary/skills/language-design.md` — §0 bold-letter
  rule (load-bearing for refusing new text formats)
- `~/primary/skills/jj.md` — version-control discipline
- `~/primary/skills/reporting.md` — report convention
- `~/primary/skills/contract-repo.md` — for §6.2 + §6.3
  contract design
- `~/primary/reports/designer/{4,64,78,79,80,81}` — current
  load-bearing designer reports
- `~/primary/reports/operator/{77,83}` — current
  load-bearing operator reports
- `~/primary/reports/operator-assistant/{82,85}` — assistant's
  bootstrap output

---

*End handoff. Ready for context reset. Next-you: start at §3.*
