---
title: 301 - Codex session recovery tail
role: operator
variant: Research
date: 2026-06-04
topics: [codex, session-recovery, operator, handoff]
description: |
  Recovery note for the oversized Codex operator saved session that
  freezes on resume. Identifies the local session file, explains the
  likely resume failure mode, preserves the recovered tail, and gives
  a short bootstrap prompt for starting a fresh agent without loading
  the full transcript.
---

# 301 - Codex session recovery tail

## Question

The psyche asked whether the saved Codex/Claude conversation objects
are called sessions, whether very large saved histories cause resume
problems, and whether the tail of the failing Codex `operator` session
can be recovered without loading the full session.

## Terminology

Codex CLI uses **session** in its command surface:
`codex resume` says it resumes a previous interactive session, and
`codex fork` says it forks a previous interactive session. The local
index field is `thread_name`, and the OpenAI Codex manual also uses
**threads** in the execution-model topic map. So the practical naming is:
session for the saved local CLI object; thread for the broader
conversation/workflow concept.

Claude Code uses **conversation** in `claude --resume` help, but also
uses **session** for `--session-id`, display names, and persistence.
So "session" is a normal word for both harnesses, with "conversation"
also normal on Claude's command line.

Sources checked:

- `codex --help`, `codex resume --help`, `codex fork --help`
- `claude --help`
- OpenAI Codex Manual at `https://developers.openai.com/codex/codex-manual.md`

Local versions:

- Codex CLI: `codex-cli 0.136.0`
- Claude Code: `2.1.161`

## Local Findings

The failing Codex `operator` saved session is:

`/home/li/.codex/sessions/2026/05/06/rollout-2026-05-06T15-24-17-019dfd75-ef1b-7d63-952e-1f0e69c538f0.jsonl`

It is `2.2G` on disk. That is far larger than the 300 MB Claude
session the psyche mentioned.

The matching Codex index entries are:

- `019dfd75-ef1b-7d63-952e-1f0e69c538f0` / `operator`, updated
  `2026-05-10T12:14:44.717439127Z`
- `019dfd75-ef1b-7d63-952e-1f0e69c538f0` / `operator`, updated
  `2026-05-10T19:10:31.778782661Z`

The file itself has records through `2026-06-03T19:14:45.032Z`.
The index is stale or only partly reflects later continued writes.

The large Claude Code primary session currently visible is:

`/home/li/.claude/projects/-home-li-primary/4250cbdc-e17a-43d8-b581-3d3b1511fa17.jsonl`

It is `301M` on disk and was updated `2026-06-04 09:53`.

Codex also has a `319M` local `logs_2.sqlite`, but the immediate
resume risk is the 2.2G JSONL session file.

## Failure Mode

The model context window is not the same thing as the local saved
history file size. A CLI can compact, summarize, or omit old content
for the model while still keeping a large JSONL transcript on disk.

Resume can still fail before the model even matters if the TUI or
session loader tries to:

- scan a multi-GB JSONL file,
- parse huge compacted records,
- rebuild display history,
- index prior tool calls,
- materialize a large transcript in memory.

The recovered tail contains at least one huge `compacted` record whose
`replacement_history` embeds a large prior history payload. That kind
of line can make even tail inspection noisy if tools print it without
care. The safe recovery pattern is to stream the file and extract only
bounded fields.

## Recovered Tail

The final Codex message, at `2026-06-03T19:14:45Z`, says:

Deep rename slice is done and verified.

Report:
`/home/li/primary/reports/operator/300-meta-signal-rename-pass-2026-06-03.md`

Pushed commits:

- `primary` `c1b7f17d` - canonical guidance now says
  `meta-signal-<component>`.
- `meta-signal-upgrade` `fe465fa0` - repo/crate/schema/build/generated
  refs renamed from `owner-signal-upgrade`.
- `upgrade` `640be3f2` - dependency/imports retargeted to
  `meta-signal-upgrade`.
- `signal-upgrade` `e1fbcf8b` - architecture text updated.

Verification named in the final message:

- all operator claims released;
- all four touched repos committed and clean;
- `main@origin` at the new commit in each touched repo;
- `repos/meta-signal-upgrade` points to
  `/git/github.com/LiGoldragon/meta-signal-upgrade`;
- malformed tentative rename wording in `skills/component-triad.md`
  is gone.

Remaining explicit gaps:

- the rest of the `owner-signal-*` fleet still needs coordinated
  rename slices;
- `core-signal-spirit` still needs its own coordinated rename slice;
- historical reports were not mass-edited.

The compacted pre-tail shows the immediate request that led into the
final work: the psyche told the operator to use a subagent for a deep
rename pass, first auditing anything that might need name changing,
then sending the subagent to do it.

## Current State Check

Primary is clean:

- working copy has no changes;
- `main@origin` is `c1b7f17dada6 primary: adopt meta-signal policy
  contract naming`.

Touched repo heads checked:

- `/git/github.com/LiGoldragon/meta-signal-upgrade`:
  `fe465fa045cd meta-signal-upgrade: rename upgrade policy contract`
- `/git/github.com/LiGoldragon/upgrade`:
  `640be3f25258 upgrade: depend on meta-signal-upgrade`
- `/git/github.com/LiGoldragon/signal-upgrade`:
  `e1fbcf8ba3f8 signal-upgrade: point architecture at meta policy
  contract`

## Fresh-Agent Bootstrap

Use this as the starting prompt for a new operator session instead of
resuming the 2.2G Codex transcript:

```text
Continue from reports/operator/300-meta-signal-rename-pass-2026-06-03.md.
The last operator session finished the upgrade-triad rename from
owner-signal-upgrade to meta-signal-upgrade and verified primary,
upgrade, signal-upgrade, and meta-signal-upgrade are clean and pushed.
Next operator frontier: coordinate the remaining owner-signal-* fleet
rename slices and the separate core-signal-spirit to meta-signal-spirit
slice. Do not mass-edit historical reports. Start by auditing current
active repos and dependencies, then handle one coherent triad/fleet
slice at a time.
```

## Safe Extraction Commands

These commands recover bounded information without invoking resume:

```sh
codex resume --help
jq -r 'select(.thread_name|test("operator";"i")) | [.updated_at,.id,.thread_name] | @tsv' ~/.codex/session_index.jsonl
du -h ~/.codex/sessions/2026/05/06/rollout-2026-05-06T15-24-17-019dfd75-ef1b-7d63-952e-1f0e69c538f0.jsonl
tail -n 80 ~/.codex/sessions/2026/05/06/rollout-2026-05-06T15-24-17-019dfd75-ef1b-7d63-952e-1f0e69c538f0.jsonl | jq -r 'select(.type=="event_msg" or .type=="response_item") | [.timestamp, .payload.type, .payload.role, ((.payload.message // .payload.item.content // .payload.content // "") | tostring | gsub("\n";" ") | .[0:240])] | @tsv'
```

Avoid `codex resume operator` for this file until the session loader
can be proven to handle multi-GB histories.
