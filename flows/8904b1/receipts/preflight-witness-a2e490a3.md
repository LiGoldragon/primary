# Witness: stopped Sonnet-preflight subflow (agentId a2e490a3fc33b15e7)

Read-only review of the killed preflight's transcript and its one Explore
sub-subagent's transcript, plus live, read-only checks of current state.
Performed 2026-09-27 by a read-only subflow of 8904b1, at the direction of
main flow 8904b1 in response to 56ae53's request to confirm holdings.

Sources:
- Parent transcript: /tmp/claude-1001/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/tasks/a2e490a3fc33b15e7.output (148 lines, ends mid-turn with `[Request interrupted by user]` at 2026-09-27T00:19:00.328Z — confirms it was killed, not that it finished).
- Nested Explore subagent (agentId a58957e36a7d439b4), launched by the preflight to identify "Cap Terra": /home/li/.claude/projects/-home-li-wt-primary-56ae53/8904b10d-7f06-4e44-9342-3a8a2d7e17bd/subagents/agent-a58957e36a7d439b4.jsonl (171 lines, also ends on a tool_use with no final report — also cut off, not completed).
- Live checks: `ps -eo pid,ppid,etime,cmd` for the sub-agent id (no match); re-derived herdr `cli:agent:list` and stable-Flow `List.{}` output already captured inline in the parent transcript (line 53, line 97) — not re-queried live to stay read-only and avoid duplicate load, cross-checked instead against literal-string search.

## 1. State-changing acts

None found. Every Bash command run by the parent and by its Explore
sub-subagent was read-only: `ls`, `cat`, `grep`/`ugrep`, `sed -n`, `find`,
`wc`, `git log`/`git fetch`/`git ls-remote`/`git ls-tree`/`git cat-file -p`
(read remote refs, wrote no local ref changes beyond fetch updating a
remote-tracking pointer), `which -a hm-send hm-list flow flowctl message`
(existence check only, never invoked hm-send), `flow --version`/`flow
'List.{}'`/`flow-next 'List.{}'`, `herdr session list`/`herdr agent list`,
`curl` GET to an OpenCode server's `/session` endpoint (empty/no body, exit
0), and `mcp__agent-intercom__intercom_list` (failed: "Intercom broker
exited before startup with code 1" — no data returned, no state change).
No `hm-send`, `hm-register`, `hm-rebind`, `hm-retire`, `flow` mutation verb,
herdr session/pane create, or native `claude`/`codex`/`opencode` launch
command appears anywhere in either transcript. No file was written or
edited by either agent (no Write/Edit tool calls at all; the only Skill
calls were `subflow`, `herdr`, `messaging` — loading a skill, not a write).
One background Agent (Explore, read-only toolset, no Bash write found in
its own log either) was launched to research "Cap Terra"; that is the only
Task/Agent launch in the whole preflight.

## 2. Live now

No live process for the Explore sub-subagent (`ps` grep for its agent id
`a58957e36a7d439b4` returned nothing but my own grep command). No pane,
tab, or session in the herdr `agent list` snapshot the preflight captured
carries a name, cwd, or terminal title tied to 8904b1 other than the
preflight's own Fable pane (`psyche_fable_b7ba00`, pane `w1:p8`, terminal
title `PsycheV2.{ Fable 8904b1 }` — its own seat, not something it
started). Nothing else it could have started is visible as alive.

## 3. OpenCode

Touched only by reading: one `curl` GET to an OpenCode server's `/session`
listing endpoint (returned empty body, read-only), and multiple `grep`
reads of Codex/OpenCode-adjacent files (`.native-seat-receipts/field-terra-opencode-*.json`,
`~/.local/share/opencode` existence check via grep target only) and of
Codex rollout session *transcripts* under `/home/li/.codex-next/sessions/...`
(reading historical records of other sessions' content, e.g. searching
those files for "Cap Terra" / "flow17_cap_terra"). No OpenCode or Codex
session was created, resumed, or prompted; no write to any OpenCode state.

## 4. Current Sonnet holdings attributable to 8904b1

Checked (as captured live by the preflight, read-only): herdr `agent list`
(9 agents: codex primary/Luna/Astra/Sol seats, `mind-luna-139366`,
`mind-astra-6fe957`, the preflight's own `psyche_fable_b7ba00`
(8904b10d...), and one Claude agent `psyche_opus_e167d8` running in cwd
`/home/li/wt/primary/opus-sonnet-56ae53` — despite the directory name, its
agent/name and terminal title are Opus (`Psyche Opus (claim pending)`), not
Sonnet); stable-Flow `List.{}` (rows for 00f95a, 139366, 184bd8, 22e12b,
26c50c, 38de5b, 504461, e51411, 8904b1 itself — no Sonnet row, no row
naming 8904b1 as owner/parent besides its own); `flow-next`/`hm-list` were
looked up as CLIs but not queried for content in this transcript. No
launcher-state file, native-seat-receipt, or `.native-seat-receipts/`
entry names a Sonnet candidate owned by 8904b1 — the only receipt read
(`field-terra-opencode-current-...json`) is an unrelated OpenCode Terra
seat (model `gpt-5.6-terra`), not a Sonnet, and not owned by 8904b1.
Literal-string search of the whole parent transcript for `8904b1` finds
only its own session id; for `9c7514` (the Sonnet packet id named in
`flows/8904b1/log.md`) finds only the log-grep quoting the working
instruction, not any live row.

**No Sonnet candidate, native thread, pane, pane reservation, Flow row,
messenger row, or launcher reservation naming 8904b1 was found in any
checked location.**

## 5. Partial findings for Field recovery (the stopped preflight's own
unreviewed observations — not verified by this witness beyond noting where
they came from)

- Sonnet packet: `flows/56ae53/sonnet-recovery/{README.md,launch-manifest.json,profile.json,predecessor-handoff.md}`; preflight verified `profile.json`'s source-file sha256 manifest against the working tree (result not captured before the kill — command ran, no result line reviewed) and separately diffed `launch-manifest.json`/`README.md` against `origin/main` (a difference was being investigated; remote vs local content was printed but not concluded).
- "Cap Terra" identity: unresolved. `flows/8904b1/log.md` lines 36–42 are the operative instruction: "query Cap Terra for any live or pending Sonnet duplicate... Cap Terra is explicitly restricted to Opus." The Explore sub-subagent's last action (cut off, no conclusion) was chasing a literal string `flow17_cap_terra` found inside a Codex rollout transcript, `/home/li/.codex-next/sessions/2026/09/26/rollout-2026-09-26T18-07-33-01a0e030-3f85-7863-9e6d-ebce91e91145.jsonl`, as a possible referent — not confirmed. Also on record: a distinct "Field Terra" OpenCode seat exists (`.native-seat-receipts/field-terra-opencode-current-field-terra-opencode-of-1cb440.json`, model `gpt-5.6-terra`) which is a different named entity than "Cap Terra" and should not be conflated with it.
- Duplicate-check state per the log itself (not re-verified live by this witness): "independent process check found no Sonnet process" was already asserted in `flows/8904b1/log.md` line 42 before this preflight ran; the preflight's own `ps -eo pid,etime,args | grep -iE "claude|codex|opencode"` (line 61) result was not captured in the reviewed excerpts.

## Verdict

On the evidence: **no** — 8904b1 holds no Sonnet candidate, native thread,
pane reservation, or launcher reservation. The stopped preflight performed
no state-changing acts (no message sent, nothing launched, nothing
written), started nothing that is still alive, and only read OpenCode
records rather than operating on any OpenCode session.
