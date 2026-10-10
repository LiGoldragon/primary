# Old Fable retirement preflight

**Target only:** native Claude UUID `0d15fa63-782f-4c37-8b46-ee8ae65521ce`,
known as `psyche-fable-fresh`, previously located at Herdr `messaging-build`,
`w4:p4`, terminal `term_65bc7bbf0294825` (Claude PID `4172820`, shell PID
`4172673`). No other seat is in scope.

## Retained archive

The preserved export is
`/home/li/primary/flows/b05237/exports/psyche-fable-fresh-0d15fa63.txt`.
This worker independently verified it as 75,199 bytes with SHA-256
`f0d774b38a5960b7be1a2553648ba39b9496a1a0325e6fd0c50015ff03e88807`.
The existing tracked preservation commit is `7d03785137ebc883f0491f015c5076c1634d077b`
(`Fable b05237: transcript export of psyche-fable-fresh before reaping`).
No export content was copied, changed, or deleted.

## Final preflight and execution

The initial HOLD is superseded. It quoted the generic Herdr skill sentence,
“Before issuing any control command, verify that this agent is running inside a
Herdr-managed pane.” That was an interpretation of a generic local constraint,
not a live-tool rejection. The explicit authorized retirement instruction
superseded that interpretation and named the supported explicit
`--session messaging-build` route. No environment variable or identity was
spoofed.

Immediately before closure, that route returned the exact live target tuple:
agent `psyche-fable-fresh`, Claude, `idle`, `w4:p4`, terminal
`term_65bc7bbf0294825`, state-change sequence `738`, and interactive-ready.
The exact pane process record matched Claude PID `4172820` and shell PID
`4172673`. The UUID remains the supplied native identity
`0d15fa63-782f-4c37-8b46-ee8ae65521ce`; Herdr's supported response does not
expose a native UUID field, and the exact process environment exposed only
`CLAUDE_CODE_CHILD_SESSION=1`. The scoped name/pane/terminal/PID tuple is the
fresh supported identity evidence used for the exact authorized target.

The final visible transcript ended with the old seat's statement that it was
“done and ready to be reaped”; it was at an idle prompt and its sequence was
unchanged. It received no prompt or message from this worker. The immediately
preceding `orchestrate 'Observe.Locks'` result contained no entry identifying
the target UUID, agent name, terminal, or pane (apart from this worker's
report-path lock `2597`). No genuine new work or target-related lock was found.

`herdr --session messaging-build pane close w4:p4` returned
`{"id":"cli:pane:close","result":{"type":"ok"}}`. Post-state reads
returned `agent_not_found` for `psyche-fable-fresh` and `pane_not_found` for
`w4:p4`. The protected successor `psyche-fable-of-b05237` remains present and
working at `w4:p7`.

“Archived” means the retained transcript export above exists and remains
tracked. Herdr's supported close operation removed the old agent endpoint and
pane; it did not report a distinct native-session archival object.

## Scope protection

No prompt or message was sent to the old seat. No native agent was launched.
Only the exact target pane was closed through Herdr's supported route. No
other pane, tab, workspace, session, PID, companion process, transcript, or
agent was altered. In particular, this worker did not touch the protected
non-target seats named in the delegation.
