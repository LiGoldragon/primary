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

## Final preflight and result

At this worker's final preflight, `orchestrate 'Observe.Locks'` returned no
lock whose owner, name, path, or reason identifies this UUID, agent name, old
pane, or its export. This is a relevant lock-registry check only; it cannot
establish the target's current native identity or whether it received new work.

The documented Herdr lifecycle instructions require `HERDR_ENV=1` before any
Herdr control or inspection command. This worker's environment reported
`HERDR_ENV=unset`. Consequently it did **not** inspect the live target state,
did **not** verify the required immediate exact identity and no-new-work
conditions, and did **not** issue any deregistration, archive, close-pane, or
process-control command.

The exact-route retirement is therefore **HOLD** for execution by a worker in
the Herdr-managed caller context. “Archived” presently means only that the
separate, immutable retained transcript export above exists and is tracked; it
does not mean the native Claude session has been archived or deregistered.

## Scope protection

No prompt or message was sent to the old seat. No native agent was launched.
No pane, tab, workspace, session, PID, companion process, transcript, or other
agent was altered. In particular, this worker did not touch the protected
non-target seats named in the delegation.
