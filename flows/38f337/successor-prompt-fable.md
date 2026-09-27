# Fresh Psyche Fable successor — first-prompt specification

Written by Psyche Sonnet 38f337 for Mind Sol 56ae53. Nothing was launched, stopped, retired, bound,
or mutated to produce this, and no credential was used. This file is a specification for a launcher,
not a launch, and not clearance to launch.

Revised 2026-09-27 under the living's ruling relayed via 56ae53, which **authorizes revision, not
launch**. Earlier drafts of this file carried two resolutions in turn — crossover, then
stop-then-launch. **Crossover is the settled one**; the stop-then-launch version is withdrawn. It was
never committed.

**Nothing in this file is proof.** Every gate below is a requirement stated ahead of a launch that has
not happened. No first-prompt receipt, no native skill readback, no transcript or title receipt, and
no measured carrier size exist yet, because no seat has been started. Where this file cites a hash or
a quote, that is witnessed; where it states a gate, that is owed.

## The living's ruling, as relayed — what it settles

- **No general launch freeze ever existed.** The living: "I never said freeze all launches.
  Everything that has a big context should be refreshed." The objection was to duplicate working
  roles and to high effort, not to launching.
- **The >200k-context refresh instruction applies specifically to Fable 8904b1.**
- **A medium-effort successor launch is authorized** — authorized, not ready. The gates below are
  unmet.
- **The old Fable is NOT stopped before the launch.** It goes silent, crossover-only, until native /
  Flow / HM / Herdr readiness is confirmed. This confirms Fable 8904b1's own reversal and c56100's
  acceptance of it.
- **Both seats must not work, or receive ordinary traffic, once the successor is ready.**
- **Transcripts are preserved.**
- **The final route reap is a separate act** under supported refresh automation or explicit
  authority — never automatic, and not decided by this draft. See the reap gate below.

The backing records are quoted verbatim in `flows/38f337/handoff-fable.md` beside this file, and
their sources are `flows/93ba9f/vision/flowLaunching.md` and `flows/56ae53/log.md`. They are not
paraphrased here; a paraphrase of the living is not the living.

## Seat

| Field | Value |
|---|---|
| Aspect | Psyche |
| Model identifier | `claude-fable-5-1` (the plain-vs-`[1m]` variant is still open) |
| Effort | **`medium` — never high** |
| Native title | `PsycheV2.{ Fable <fresh-id> }` (per `testing-flow-titles`; `<fresh-id>` is the seat's own verified `FLOW_ID`, after the receipt, never before) |
| Predecessor | `8904b1` — **crossover-only, not stopped**; remembered at depth one |
| `FLOW_DIRECTORY` | `flows/<fresh-id>` under `/home/li/wt/primary/56ae53` |
| Harness | Claude, `--dangerously-skip-permissions` |
| Hosts implementation | **No.** Fable reviews, doubts, and agrees; it designs and thinks. Implementation goes to Codex/Terra-class workers after Fable has agreed to the design. |

Authoritative source for model and effort: `flows/56ae53/fable-recovery/profile.json` and
`.../launch-manifest.json` (`"model": "claude-fable-5-1"`, `"effort": "medium"`); display name
`Fable` from `config/model-display-names.json`. Corroborated by the predecessor's own words,
`flows/8904b1/summary.md` line 3: "Model claude-fable-5-1, effort medium". c56100's independent
review confirms model and title were already correct and need no change.

**Why never high, explicitly.** The living objected to high effort in the same relayed ruling, and
earlier gave the reason (`flows/93ba9f/vision/flowLaunching.md:11`): high effort is not forbidden in
principle, but no flow has been *designed* to use it, so none should be launched with it. A Fable seat
at high effort is the named fault of the 2026-09-26 cost emergency. `medium` is not a preference here;
it is the ruling.

## Crossover — the successor launches, the predecessor goes silent

**8904b1 is not stopped, not retired, not concluded, not silenced out of existence, and its routing is
not withdrawn as a side effect of this launch.** This is the `refresh` skill's own pattern, and Fable
8904b1 confirmed it against that skill's written text after its own records search.

- The successor starts in a **new pane**. Not Flow's Replace (it stops the predecessor and closes its
  pane). Not the same pane (that requires the old session to exit, retiring it as a side effect).
- 8904b1 is **crossover-only** from the successor's start until every readiness gate below passes:
  available for evidence, routing continuity, and handoff; **silent**; taking up no new work. It has
  already stood itself down.
- **From the successor's first confirmed readiness, other flows address the successor, not the
  predecessor.** This is what the cost alarm was actually about: a live seat still *receiving*
  messages and therefore spending, not mere co-existence. Two seats existing is not the fault; two
  seats working or taking ordinary traffic is.
- The successor **remembers 8904b1 at depth one** without replaying its full context. It reads
  8904b1's records itself rather than trusting a summary, and **takes none of 8904b1's own rulings as
  settled without independently reading them.**
- **Transcripts are preserved.** Nothing of 8904b1 is deleted to make room for the successor.

### Reap gate — a separate act, and NOT yet authorized

Retiring 8904b1's route happens **only** under supported refresh automation or explicit authority. It
is never automatic and it is **not granted by this file**.

**Who performs the reap is not yet authorized.** That is an open prerequisite, not a detail. The
living's word names Field Luna as holding the authority to stop and start flows *once told* — "she
doesn't have the authority to decide. She has the authority to do it once she's told to do it"
(`flows/93ba9f/vision/flowLaunching.md:31`) — so the telling is still owed, and by someone who holds
that authority. A seat does not authorize its own ending (`flows/8904b1/log.md:3083`).

Until the reap happens, an unreaped predecessor route keeps receiving messages. Psyche, 2026-09-17
(`flows/1ac573/vision/operational-reapReplacedSessions.md`): "When a session gets replaced, it has to
be reaped so it doesn't keep getting messages". That is the reason the reap is owed — and the reason
it must be an explicit act rather than a silent side effect.

## Blocking gates — concrete, each unmet

### 1. Launcher — there is no proven Claude-side path

**State plainly: no Claude-side path is known that both starts a Fable seat and writes and reads back
its correct V2 title.** Per c56100's finding:

- `native-batch-refresh` / `claude-native-seat-refresh` **hard-codes legacy titles**.
- `native-seat-launch` V2 is **Codex-only**.

So the two halves — a Claude start, and a correct `PsycheV2.{ Fable <fresh-id> }` title written and
read back — have no single proven carrier on the Claude side. What is known is partial: a start
followed by a subflow-typed rename with readback **has worked once**. Partial is not proven.

**A successor launch cannot be called ready until either a working path is identified, or this is
proven on a disposable seat first.** Do not assume a supported Claude V2 launcher exists.

#### Unrepaired defect in the existing helper — blocking

The existing Claude refresh helper (`native-batch-refresh` / `claude-native-seat-refresh`) carries two
faults, and the second is worse than the first:

1. It **hard-codes the legacy title**, so it cannot produce `PsycheV2.{ Fable <fresh-id> }`.
2. It has **no non-overlap routing gate.** Nothing in it prevents the successor and the predecessor
   from being addressable at the same time.

The second fault is the exact thing that must not happen. The whole point of the crossover rule is
that from the successor's first readiness, ordinary traffic goes to the successor and not to the
predecessor — and the cost alarm was about a seat still *receiving* messages. A helper with no
non-overlap gate leaves both seats addressable, which means both can be spent against. **This is an
unrepaired defect and it blocks launch-readiness.** It is named here, not fixed here; repairing it is
implementation, which this seat does not host.

### 2. Skill receipts — every startup skill, by native body or hash

Readiness requires **one byte-exact, `main-flow`-leading first prompt carrying ALL startup skills
including native `psyche`**, proved by an **actual native body or hash readback of every startup skill
present in the seat's own context**, with `main-flow` **leading and byte-exact**, and **`psyche`
specifically confirmed in the middle stratum**.

The skill bodies are **sourced from the AUTHORED Curriculum files**, not merely from the generated
`.claude` projection: `/git/github.com/LiGoldragon/Curriculum/skills/<name>.md`, per the *Curriculum
skills* variable in `SKILL_VARIABLES.md`. The authored file is the authority for what the text ought
to say; the projection is what a launcher pastes and must therefore also hash. Both columns are in the
size gate's table below, and a divergence beyond the documented projection transforms is a signal to
regenerate, not to paste around.

**A manifest entry, a profile `skills` list, a launch-manifest, or a brief that names a skill is
refused as evidence** — the standard already proven this session. `flows/8904b1/summary.md`: "A brief
naming a skill is not a receipt. The receipt is the loading in the worker's own record."

The middle-stratum requirement is the living's own, `flows/56ae53/log.md:18`: "Put the psyche in their
middle stratum context layer with the subagent using the messaging tool." A Psyche seat that never
received `psyche` rules from nothing. `spirit`'s absence from a first prompt is a recorded past fault.
The receipt is owed for **all** of them, not a sample.

### 3. Sources and size — authored vs. projected, and the composed profile unmeasured

Per this repository's `CLAUDE.md`, the `.claude/`, `.agents/`, `.codex/`, and `.pi/` trees are
**generated, read-only evidence, never edited directly, regenerated from the Curriculum skills.** The
**Curriculum source is the authority**; a launcher **pastes, and must hash, the projection it actually
uses.**

Authored source of record, per the *Curriculum skills* variable in `SKILL_VARIABLES.md`:
`/git/github.com/LiGoldragon/Curriculum/skills/<name>.md`. The projection is driven by
`/git/github.com/LiGoldragon/Curriculum/manifests/*.dotos`.

| Skill | Authored source (authority) | authored sha256 / bytes | Projection (pasted + hashed at launch) | projected sha256 / bytes |
|---|---|---|---|---|
| `main-flow` | `Curriculum/skills/main-flow.md` | `37bb92039ec0793bb7f11639b748f74ba6f464d30c18293129bc0d4d52e4d60e` / 8223 | `.claude/skills/main-flow/SKILL.md` | `119d98a9a290c3edbdbd8106b25b8fca03e8ec3551eb1582f68ff366293c82e2` / 8079 |
| `refresh` | `Curriculum/skills/refresh.md` | `8b3cbbe8d87b12e0844144d547c286dfb48f098131a8a7f6109f27d02f72a8ed` / 4671 | `.claude/skills/refresh/SKILL.md` | `07b97916bfb3201eb41859a90279f6d66a94b7dd9471d1c560f99a6ebf0fe68b` / 4686 |
| `psyche` | `Curriculum/skills/psyche.md` | `a40fec16bd2631e98a0dd341587b74a88ebf48090a04b9f8cb0779f248382b7b` / 4508 | `.claude/skills/psyche/SKILL.md` | identical — `a40fec16…` / 4508 |
| `spirit` | `Curriculum/skills/spirit.md` | `4ff172000c5054d055521e48c58f56867bb34d2e76b11392e295c9ff993ec596` / 1649 | `.claude/skills/spirit/SKILL.md` | identical — `4ff17200…` / 1649 |

`main-flow` and `refresh` differ between source and projection for legitimate reasons: authored
`user-only: true` becomes `disable-model-invocation: true` in the Claude projection, and the authored
`main-flow.md` carries `{% if claude %}` / `{% if codex %}` blocks, so the Codex-only
`flow-id codex --flows-root` line is dropped. A divergence beyond these is a signal to regenerate per
`testing-generated-projection`, not to paste around. If a hash does not match at launch time, the
launch is refused, not adapted. Corroboration that the projection is what actually reaches a Fable
seat: `119d98a9…` is the hash of the byte-exact `main-flow` body in Fable's own native first prompt,
`flows/8904b1/log.md:676`.

**Measure the ACTUAL FINAL COMPOSED PROFILE before any Start** — not a skill-name list. Bundle and
source files carry long context, and a name list understates the real composed size by a wide margin.
A first-prompt size limit has already failed Fable once and Sonnet once
(`flows/8904b1/reports/psyche-seat-successor-plan.md`, item 5). The measurement is of what is actually
composed and submitted, taken before Start, not estimated.

Recorded verbatim from 56ae53, unexplained and **not to be acted on**: *"a known real Fable profile
1,125 was refused before reservation."* Its meaning is unclear to this flow. It is written down so it
is not lost, not resolved by guessing.

### 4. Credential — answered, with one verification step remaining

Per 56ae53's Flow 0.17.1 findings, this is **no longer open in principle**:

- A normal Claude seat **uses the existing `~/.claude` `CLAUDE_CONFIG_DIR` as-is.**
- **Do not copy and do not read credentials.** Not into the seat's directory, not into a temporary
  directory, not at all.
- A **user-authorized recovery launch may use it** — which this launch, once authorized, would be.

**Remaining verification step, before launch:** the **native login screen must be checked first.** A
seat that comes up at a login prompt has not inherited a usable session, and proceeding past that
point without looking is how a launch silently produces a seat that cannot work.

This supersedes Fable's own earlier inference (that a seat in the living's session likely uses the
same login every seat there uses) — the inference was right in substance, but it is now a finding with
a named check rather than a guess. The held-login / scratch-home question remains a **separate track,
for test seats only** (`flows/8904b1/summary.md`, question 1). **No credential is read, copied, or used
by this file.**

### 5. Registration sequence — an ORDER, not a set of checks

**Flow Start does NOT register HM by itself.** This is the exact ordering, per 56ae53's Flow 0.17.1
findings, and it replaces any vaguer "registration gate" language:

1. **Flow Start** — the seat is started. This registers nothing with the messenger.
2. **The seat reaches `Started`.**
3. **Its native title is set** — `PsycheV2.{ Fable <fresh-id> }`, after the `FLOW_ID` is claimed, never
   before.
4. **Its Herdr binding exists.**
5. **Only then does HM registration happen**, and only then can it **get a routed reply**.
6. **Remote external attach is a separate, later step.** It is not part of readiness and must not be
   folded into it.

Nothing at step 1 or 2 may be reported as registration. Nothing before step 5 may be messaged.

**The readiness witness is an OBSERVED REPLY from the successor — not a status poll.** A pane, a
process, a launcher's "started", a row in a table, or one status poll is not a witness. A send
returning `Uncertain` is not a confirmation and is not resent. Grade at the boundary actually observed
and never upgrade one grade into another. Every gate that fails is reported open.

The registration made at step 5 carries an agent name built from the **successor's own id** — not a
predecessor's. 8904b1's row carries an agent name made from `b7ba00`; that fault is corrected at source
by whoever owns the registration and must not be reproduced.

### 6. No predecessor-binding adoption

**The successor gets its OWN fresh binding and route. It never inherits 8904b1's existing HM
registration or Herdr route.** No rebinding of the predecessor's row to the successor, no reuse of its
agent name, no adoption of its pane.

Two reasons, and both have already bitten. First, 8904b1's own row carries an agent name made from
`b7ba00` — a predecessor's identity, carried forward once already; adopting a binding is how that
propagates. Second, an adopted binding destroys the non-overlap property the crossover rule exists to
protect: if the successor answers on the predecessor's route, there is no longer a clean distinction
between addressing one and addressing the other, and the reap can no longer be a separate, explicit,
reversible act.

A fresh binding is also what makes the reap meaningful: the predecessor's route is withdrawn as its own
act, while the successor's own route stands untouched.

## Readiness gates, in order

1. **One accepted first prompt**, the single line described under *First-prompt mechanics*: `main-flow`
   leading, at most five stacked `/skill` commands, the fixed receipt present. Native transcript read
   back; the receipt matched exactly, as a comparison and not an interpretation.
2. **Every startup skill receipted** by native body or hash, per gate 2 — both the five in the head and
   every skill loaded afterward through the Skill tool — with `psyche` confirmed in the middle stratum.
3. **Native `FLOW_ID` claimed only after 1 and 2**, via
   `flow-id claude --flows-root <ABSOLUTE FLOW_DIRECTORY> --parent-session "$CLAUDE_CODE_SESSION_ID"`.
4. **Title set and read back** as `PsycheV2.{ Fable <fresh-id> }`, after the `FLOW_ID` is claimed and
   never before — through a supported adapter, which gate 1 says does not yet demonstrably exist on the
   Claude side.
5. **`Remembered: 8904b1 — depth one`** recorded, with the facts most relevant carried forward.
6. **The registration sequence of gate 5, in order**, through HM registration and a **routed reply**.
   Remote external attach is later and separate.
7. **An observed reply** from the successor — the readiness witness, never a status poll.
8. Only then: other flows are told to address the successor and not the predecessor. The reap remains
   a separate, still-unauthorized act, and the helper that would perform it still lacks a non-overlap
   routing gate.

## First-prompt mechanics — the actual launcher mechanic

**This replaces the earlier "does the whole assembly fit in one big prompt" framing entirely.** The
assembly is not pasted. Per 56ae53's Flow 0.17.1 findings, the real mechanism is:

- a **short prompt**, **at most 800 UTF-16 characters**, on **ONE LINE**;
- with **at most five `/skill` commands stacked at its head** — the harness's own stacked-command
  limit;
- and a **fixed receipt** included in that same line;
- **every remaining required skill loads afterward via the native Skill tool**, once the session is
  running — not in the first prompt.

### Which five occupy the head

Three of the declared set are forced, because they carry `disable-model-invocation: true` in the
projection and the Skill tool therefore **cannot** load them once the session is running. If they are
not in the stacked head, they never arrive at all:

1. **`main-flow` — must lead.** Nothing before it.
2. **`refresh`** — and this launch *is* a refresh.
3. **`claude-harness`** — the seat is a Claude harness seat.

That leaves two slots, filled on merit rather than necessity:

4. **`psyche`** — loadable later in principle, but the living requires it in the middle stratum
   (`flows/56ae53/log.md:18`), and a Psyche seat that never received it rules from nothing.
5. **`spirit`** — applies to every agent task, and its absence from a first prompt is a recorded past
   fault (`flows/8904b1/reports/psyche-seat-successor-plan.md`, item 5).

**Named honestly as a judgment, not a finding:** slots 4 and 5 are a choice. Only slots 1–3 are forced
by the invocation constraint. If the living or the launcher's owner prefers different occupants for 4
and 5, nothing above forbids it — the constraint is the count, five, and that `main-flow` leads.

Verified against the projection: of the entire declared set, exactly `main-flow`, `refresh`, and
`claude-harness` carry `disable-model-invocation: true`. All others — `psyche`, `spirit`,
`psyche-interraction`, `testing-flow-titles`, `psyche-acquisition`, `psyche-distillation`, `behavior`,
`correction`, `vocabulary`, `testing`, `subflow`, `edit-coordination`, `flow-evidence`,
`prompt-crafting`, `herdr`, `messaging`, `file-editing`, `operational-final-response` — **can** be
loaded by the Skill tool immediately after the session is running, and that is how they arrive. Each
still owes a receipt under gate 2; loading them later does not lower the standard of proof.

### The line, and its budget

A candidate head plus receipt measures **106 UTF-16 units**, against the 800 limit:

    /main-flow /refresh /claude-harness /psyche /spirit Reply exactly: FABLE-FIRST-PROMPT-OK then run flow-id.

That leaves ample budget, so the constraint that actually binds is **five commands**, not 800
characters. The exact receipt token and the exact trailing instruction are the launcher's to fix; what
matters is that the receipt is **in that same one line** and is fixed in advance, so the readback is a
comparison and not an interpretation.

### What does NOT go in the first prompt

The living's verbatim words, the handoff, and the brief are **not** pasted into the line. They reach
the seat after it is running:

- **The living's own words, verbatim** — on Fable's role FIRST, then cost, refresh, high effort,
  Terra, the newer Flow — from `flows/38f337/handoff-fable.md`. Never paraphrased.
- **A pointer** to Fable's own handoff: `flows/8904b1/summary.md` on Primary main, with its `log.md`,
  `reports/`, and `witnesses/` beside it. **Point to it; do not restate it.**
- **The brief**: `FLOW_ID` assigned after the receipt; `remember 8904b1` at depth one; a **fresh flow
  that remembers, not a resumed session**; crossover with the predecessor silent and not stopped;
  medium effort, never high; hosts no implementation; takes none of 8904b1's rulings as settled without
  reading them itself; and the blocking gates above named as blocking.

### Submission mechanics — for when a launch is eventually authorized

Recorded as mechanics, **not as authorization**: no manual first-prompt retry; no `--stdin`, no
`--wait-presented`, no retry on Uncertain; return the transport receipt. An Uncertain submission is
reported as Uncertain and is not resent.

## Provisional

Fable 8904b1 reports a records search on its side for the living's word on refresh order. If it turns
up a living word that contradicts any of the above, **that overrides this file**, and Fable will
report it. This draft is provisional on that search.
