# Typing-gate purge — occurrence search

Scope searched: authored skill sources under
`/git/github.com/LiGoldragon/Curriculum/skills` (authoritative; `.claude/`,
`.agents/`, `.codex/`, `.pi/` are generated projections, reported separately),
`AGENTS.md`, `CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`, `ARCHITECTURE.md`,
`design/`, `protocols/`, `roles/`, `tools/` (incl. the named launcher/refresh
tools), `Vision/`, `Intent/`, and under `flows/`: every `refresh-inject.md`,
`first-prompt*.txt`, `profile.json`, `handoff*`, payload files, and the named
`log.md` files (d8df70, e51411, 9ddcbc, eb7bae, 836818, 752e0f, b80e55,
6288d1, 47764b).

Patterns: living/human/user "types"/"typing" a command, "type /", keyboard,
keystroke, "typed by the living" as a gate, "ask the user to run" /
"run ... themselves", "manually"/"by hand" in launch/gate contexts,
approve/approval where a human keystroke in a pane is meant. Also
`disable-model-invocation` / `user-invocable` in skill sources and tools.

Judgment key: (a) the idea as a live gate — must die. (b) provenance mark or
factual/historical account — keep. (c) unclear.

## Result summary

- (a) gate hits in currently-authored, forward-facing material: **0**.
- No skill source, tool, inject list, first-prompt payload, profile.json, or
  design doc currently asserts that a human must type a harness command,
  press a key, or manually grant a permission to clear a gate.
- The idea's only remaining textual traces are inside historical logs and one
  pre-ruling handoff, all dated accounts of what already happened, most of
  them already self-superseding.

---

## `/git/github.com/LiGoldragon/Curriculum/skills/skill-designing.md`

- Line 53-56: "`user-only: true` — the skill enters only through the user's
  typed prompt; the flow cannot load it. It deploys as
  `disable-model-invocation: true` in Claude Code and as $-name-only
  injection in Codex." — **(c) unclear / mechanism description.** This
  documents the harness-level flag itself (the thing the psyche called "an
  obsolete piece of equipment" mechanism), not an instruction that a human
  must clear a flow's gate by typing. It is the definition other files below
  build on. Not a gate assertion by itself; flagged for the psyche/skill
  owner to decide whether the `user-only` skill type should be redesigned
  away entirely now that no gate may depend on a human keystroke.

Skills carrying `disable-model-invocation` (via `user-only: true` in the
authored source, confirmed present as `disable-model-invocation: true` in
every generated `.claude/skills/*/SKILL.md` projection): **field, realization,
main-flow, design, refresh, voice-psyche, skill-designing.**

Count: (a) 0, (b) 0, (c) 1.

---

## `/git/github.com/LiGoldragon/Curriculum/skills/main-flow.md`, `refresh.md`, and other skill sources

Grepped in full for the purge patterns (living/human/user typing, keyboard,
keystroke, "typed by the living" as gate, manual/by-hand launch gates). No
occurrences. The `main-flow.md` refresh section and `refresh.md` describe
native-start receipts, source-hash audits, and title readback as the proof
of successor launch — no step names a human keystroke as the clearing
mechanism.

Count: (a) 0, (b) 0, (c) 0.

---

## `tools/` (native-seat-launch.mjs, claude-native-seat-refresh.py, canonical-title-alignment.mjs, prompt-relay, native-batch-refresh.mjs, compose-seat-prompt.py)

- `tools/native-seat-launch.mjs:301-304`: comment "Source material can
  accurately quote a slash command. Only the launcher-authored instruction
  header is prohibited from substituting a text token for the typed
  structured skill inputs below." — **(c) unclear.** "typed structured skill
  inputs" here means the structured skill payload the launcher itself sends
  through the app-server RPC (`structuredSkills(skills)`), not a human's
  keystrokes; it is guarding against the launcher *pretending* a skill was
  loaded by writing its name as a token. Not the purge target, but the word
  "typed" is doing unrelated, adjacent work worth a second look by whoever
  edits this file.
- No file in `tools/` instructs a human to type a slash command, press a key,
  or grant a permission by hand to clear a gate. `claude-native-seat-refresh.py`
  and `native-batch-refresh.mjs` inject `main-flow`/`testing-flow-titles`
  programmatically via `herdr agent prompt`, i.e. machine-driven, not living-driven.

Count: (a) 0, (b) 0, (c) 1.

---

## `AGENTS.md`, `CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`, `ARCHITECTURE.md`, `design/`, `protocols/`, `roles/`, `Vision/`, `Intent/`

All hits found were unrelated "approve/approval" (psyche/document approval,
kernel-quirk approval, spirit-capture approval) or "by hand"/"manually" in
non-gate engineering contexts (wiring code by hand, re-entering database
rows manually, a request submitted "by hand"). None frame a gate as cleared
by a human typing a harness command or pressing a key.

Count: (a) 0, (b) 0, (c) 0.

---

## `flows/1ac573/handoff.md` (dated 2026-09-17, before the purge ruling)

- Line 39: "`main-flow` could NOT be loaded: it is marked
  disable-model-invocation and refuses the Skill tool. **It must be invoked
  by the living typing `/main-flow`.** A successor must expect the same
  refusal and ask for it." — **(c) unclear, leaning (b).** Written five days
  before the living's 2026-09-24 ruling, as a factual account of that
  session's real, witnessed obstacle at the time. It is a `handoff*` file
  (in scope per the brief), not a `log.md`, so it is not automatically
  exempted as a historical log — but its content and dated framing are
  historical-record in character, not a live instruction to a current flow.
  Flagged rather than resolved because handoff files are read by future
  successors as guidance, and this line could still be read as endorsing the
  gate.
- Line 90: "...Codex worker `6034cc` submitted the command through `herdr
  agent prompt` at the living's request — it was **NOT typed by the
  living**, and this flow first misattributed it." — **(b) keep.** A
  self-correction recording that machine injection, not the living's
  keystrokes, produced a prior turn; supports the purge, does not restate it.
- Line 86: "the harness's own framing of an inbound message as coming from
  the user is not a reliable statement of origin... Nothing in the rendering
  distinguishes machine-injected input from the living's keystrokes." —
  **(b) keep.** Analysis of an origin-ambiguity hazard, factual, argues
  against ever trusting apparent "living typing" as such.

Count: (a) 0, (b) 2, (c) 1.

---

## `flows/9ddcbc/psyche-high-successor-20260924/first-prompt.txt` and its duplicate `flows/395aed/refresh-production/psychehigh-one-turn-20260920/first-prompt.txt`

Both are large injected payloads reproducing prior synthesis/log content.
Relevant lines (same in both copies):

- "Every psyche statement typed by the living to any flow is mirrored..." —
  **(b) keep**, provenance mechanism description (mirroring), not a gate.
- "...the Field rebuilds, restarts Flow on its fresh store, and submits the
  one request **by hand** for this morning's live container..." — **(b)
  keep**, describes a manual engineering step (submitting one request),
  unrelated to a harness-command/keystroke gate.
- "main-flow skill injected by the living's `/main-flow` on the fourth
  prompt (it is disable-model-invocation and could not be loaded earlier)." —
  **(b) keep**, dated historical account of what happened in an earlier
  turn, reproduced as inherited synthesis, not asserted as a required future
  gate.
- Several "the living typed '<words>'" lines (ports ruling, "yes to both,
  go", "bind the flows now") — **(b) keep**, provenance marks recording the
  content of the living's words, not a procedural gate.
- "...a later typed turn 'No I said flash book.' not from my subflow, read
  as **the living typing directly into that seat**." — **(b) keep**,
  observational provenance/attribution record.

Count (each file): (a) 0, (b) 6, (c) 0.

---

## `flows/eb7bae/psyche-medium-successor-20260924/first-prompt.txt`

- Line 7: "If a native-only skill requires its slash command, **name that
  exact gate rather than simulating it**." — **(b) keep.** This is
  anti-simulation instruction (do not fake-load a gated skill), not an
  instruction to have the living type the command; it tells the successor to
  report the refusal honestly rather than resolve it by asking for a
  keystroke.

Count: (a) 0, (b) 1, (c) 0.

---

## Historical logs (records; not edited by this purge)

### `flows/752e0f/log.md`

- Line 14: full account of the living's ruling itself — "Make it very clear:
  I'm not going to type anything ever again." ... "no gate in the twelve-seat
  refresh may depend on the living typing a harness command; `/main-flow`,
  `/rename`, and permission grants are cleared by the machine, or the design
  that needs them is replaced." — **(b) keep.** This is the charter record;
  it is the source of the purge order, not an instance of the idea to purge.

### `flows/d8df70/log.md`

Six occurrences (lines 12, 49, 60, 86, 149, 336-337), all inside a dated
session log that itself narrates the idea's rise and its own supersession:
line 336-337 reads "Every earlier entry in this log that frames a step as
cleared by the living typing into a pane... is superseded. The machine
clears every gate... Do not carry the earlier framing into any successor." —
**(b) keep, all six.** This is a log (named in the search scope's log list)
and is the record of the idea's history and retraction, not a live
instruction.

### `flows/836818/log.md`

Four occurrences (lines 38, 79, 165, 179), all "the living typed '<words>'"
provenance marks recording the content of rulings relayed through other
seats. **(b) keep, all four.**

### `flows/e51411/log.md`, `flows/9ddcbc/log.md`, `flows/eb7bae/log.md`,
`flows/b80e55/log.md`, `flows/6288d1/log.md`, `flows/47764b/log.md`

No occurrences of any purge pattern.

### `flows/752e0f/vision/livingInput.md`

Not in the named log list but is the direct provenance source underlying the
752e0f log entry above (titled "The living does not type"), containing both
verbatim rulings quoted with the "psyche, typed" provenance mark. **(b)
keep** — this is the canonical record the purge itself rests on.

---

## Other `flows/` payload/profile files checked with no occurrences

`flows/108ab0/handoff.md` (only unrelated document-approval hits),
`flows/4a2502/handoff.md`, `flows/d8df70/refresh-inject.md`,
`flows/03e825/retained-field-refresh/profile.json`,
`flows/f55ec8/reports/handoffToSuccessor.md` (and its two copies under
`flows/f55ec8/handoff/successors-v7/...` and
`flows/b49251/handoff/psyche-medium-v1/...`, only unrelated
"pre-approved main-flow line" hits), `flows/9ddcbc/mind-sol-flow-psyche-20260923/profile.json`,
`flows/9ddcbc/psyche-medium-successor-20260924/first-prompt.txt`,
`flows/9ddcbc/psyche-high-successor-20260924/attempt-2/first-prompt.txt`,
`flows/6db4fe/*/profile.json`, `flows/6db4fe/field-sol-native/handoff.md`,
`flows/6fb948/self-refresh-20260922/{profile.json,handoff.md}`,
`flows/753e69/*/profile.json`, `flows/753e69/psyche-high-native/refresh-payload-1b8ac0.md`
(only unrelated "authority by prefix" approval hits), `flows/753e69/field-sol-of-753e69/handoff.md`,
`flows/0347d0/psyche-low-native/profile.json`,
`flows/03e825/refresh-round-20260922/psyche-high/profile.json`.

---

## Overall counts

- (a) must-die gate hits in currently-authored/live material: **0**
- (b) provenance/factual/log records: **~20** (mostly inside the nine named
  logs and the two first-prompt payload copies of 9ddcbc's synthesis)
- (c) unclear/flagged for owner judgment: **3** (`skill-designing.md`'s
  `user-only`/`disable-model-invocation` definition; `native-seat-launch.mjs`'s
  unrelated "typed structured skill inputs" comment; `flows/1ac573/handoff.md`
  line 39, pre-ruling handoff)
