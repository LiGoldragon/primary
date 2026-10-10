# Recovery of dc53b4's reply to 8904b1, garbled to literal "--stdin"

Subflow of 8904b1, 2026-09-27. Read-only; no send, no probe, no wake made.

## Provenance

Native session `dc53b4be-338b-4601-ab3c-a0e155fc8fa9`
(`/home/li/.claude/projects/-home-li-wt-primary-opus-sonnet-56ae53/dc53b4be-338b-4601-ab3c-a0e155fc8fa9.jsonl`),
subagent transcript `subagents/agent-aed4bef9fd3fe9e21.jsonl` ("Reply to Fable
8904b1", launched by dc53b4 at native line 377, task-id `aed4bef9fd3fe9e21`).

## The command as run

Subagent transcript line 41 (tool_use):

```
cd /home/li/primary && FLOW_ID=dc53b4 hm-send 8904b1 --stdin <<'EOF_BODY'
<body, see below>
EOF_BODY
echo "EXIT=$?"
```

## The messenger's answer

Line 42 (tool_result): `Transported.{ 8904b1 working }` / `EXIT=0`. The
subagent's own SubflowReturn (line 44) reports this as a clean Transported
send and closes the matter — it never inspected what bytes actually went out.

## The intended body, in its exact words

Recovered from the subagent transcript's own tool_use input (line 41, the
heredoc body), i.e. from the record of the command as constructed, not from
a report about it:

> dc53b4 to 8904b1, on your ruling: (1) Skills: all eighteen are now loaded through the Skill tool, spirit first — spirit, psyche, behavior, vocabulary, correction, testing-flow-titles, psyche-acquisition, psyche-distillation, testing, subflow, edit-coordination, flow-evidence, prompt-crafting, claude-harness, herdr, messaging, file-editing, operational-final-response; the native expansions sit in my transcript. (2) Correction appended to my log: the 21:18 working question was answered by 93ba9f; entry not edited. (3) How my first prompt was submitted, from my own context only: it arrived wrapped as pasted content, so the harness expanded no slash commands from it; the main-flow, refresh and psyche-interraction bodies were written into it as text by a launcher, followed by the launch brief and source bundle, ending with a BOOTSTRAP ONLY instruction to reply BOOTSTRAP_READY. Which process submitted it I cannot see; I have no native-start receipt. (4) Identity: FLOW_ID dc53b4 from legacy flow-id, bound in stable Flow 0.12.2 (Claude endpoint Unavailable) and HM 0.2.5 (route Bound); title set by a typed /rename to PsycheV2.{ Opus dc53b4 }, Herdr readback not witnessed. (5) Records are uncommitted: /home/li/primary is detached and behind origin/main. I declare no readiness. Next: answer the six questions myself as far as the records go, then take the remainder to the living on concrete examples.

## Cause — witnessed, not guessed

Witnessed directly on this host, without running a send: `hm-send --help`
(and its error text) print only

```
messenger-clj send TARGET BODY [--wait-presented] [--hold-seconds N] [--pane SESSION:PANE]
messenger-clj send TARGET --psyche CONTEXT VERBATIM [--wait-presented] [--hold-seconds N] [--pane SESSION:PANE]
```

— no `--stdin` and no `--psyches` form exists on this installed binary; `BODY`
is a required positional argument, not something the tool ever reads from
standard input. This matches a line already typed by the living into
dc53b4's own pane (dc53b4be transcript, line 9 region, ~00:13Z): messenger-clj
0.2.5 (the version this host has) refuses `--psyches`/`--stdin`; 0.2.6, which
adds those, was not yet installed here.

So the hypothesis is confirmed by direct evidence, not inferred: the subagent
ran `hm-send 8904b1 --stdin <<'EOF_BODY' ...`, meaning to pipe the body in on
stdin. The installed `hm-send` has no `--stdin` option; it consumed the
literal string `--stdin` as the required positional `BODY` argument and never
read the heredoc's stdin at all. It sent exactly that 7-byte body,
`Transported` and exit 0 — a clean send of the wrong content. The subagent's
own SubflowReturn did not catch this because it treated `Transported`/exit 0
as proof the intended body went out, without checking what was actually
serialized.

## Skills dc53b4 has loaded since the ruling arrived

Native transcript lines 277–363 (Skill tool launches, spirit first): spirit,
psyche, behavior, vocabulary, correction, testing-flow-titles,
psyche-acquisition, psyche-distillation, testing, subflow, edit-coordination,
flow-evidence, prompt-crafting, claude-harness, herdr, messaging,
file-editing, operational-final-response (18, matching its own log entry).

## Not found

No independent confirmation that 8904b1 ever received or displayed the
literal `--stdin` body was sought here (that is 8904b1's own inbox, outside
dc53b4's transcript); this receipt only recovers what dc53b4's side intended
and shows why the wrong bytes went out.

## Second matter: the "Appoint Field Sol 9ac67c as integration owner" line

Searched the entire dc53b4 session tree (main transcript + all subagent
transcripts, case-insensitive) for "appoint" and "integration owner". No line
reading "Appoint Field Sol 9ac67c as integration owner" as an instruction
**received by** dc53b4 exists anywhere in the record.

What does exist, twice, is dc53b4's own proposal, written by dc53b4 itself:

- Main transcript line 216 (assistant, 2026-09-27 00:51Z, after the "Route
  codex-next status to owner" subagent returned, before the ruling from
  8904b1 arrived at line 271): "**My proposal:** appoint Field Sol 9ac67c as
  integration owner, overriding that line in its packet. Once you rule, a
  helper sends the status there with 'activation not authorized' and asks for
  acknowledgement." — immediately followed by "**Your ruling:** should 9ac67c
  become integration owner, or some other seat?" addressed to the living.
- Main transcript line 396 (assistant, `FinalResponse.{ dc53b4 MainFlow ... }`,
  after the reply-to-8904b1 subagent returned): dc53b4 repeats it as an open
  tag, "«Who owns integration? My proposal is Field Sol 9ac67c, overriding
  the line in its r[eport]...»" — again framed as dc53b4's own proposal
  awaiting a ruling, not as something told to it.

No typed, pasted, or machine-envelope entry anywhere in the tree instructs
dc53b4 to make this appointment. The record does not show the living, 8904b1,
or any other sender saying it; both occurrences are dc53b4 asking a question
of its own, not receiving a directive. Whoever or whatever produced the line
the coordinator saw, it is not attested in dc53b4's transcript as an input —
if it exists as an instruction anywhere, it is outside dc53b4's own record.
