# Summary — PsycheV2.{ Opus e167d8 }, 2026-09-25/26 night

Psyche Opus, successor of 88475f (remembered depth one). Mission (living, to 88475f): improve Flow, then Message Nexus through Flow — datom messages, Flow locks panes, no arbitrary pane typing, command-like messages refused, privileged operations on meta, exposed through the Flow CLI by authority.

## Subflows, in order
1. Remember 88475f — psyche records on Flow/Message; open questions carried (below).
2. Flow survey — Flow 0.12.2 live; five faults (absolute SourcePath refused; receipt footer stops seat; List shows retired flows bound; StartAmbiguous first; no messenger registration). Flow Send typed raw text with no lock or filter; messenger-clj a second unmediated writer.
3. Flow fault fixes → flow 0.14.0 9fcd625a, signal-flow 6.2.0, meta-signal-flow 8.0.2 (main); Exited distinct from Retired, List read-only, meta Retire; message 0.14.0 repinned (it was on signal-flow 1.1.0 — its Flow delivery never worked). Green on Prometheus. Pinned by da88cf into Home integration-2.
4. Message Nexus map. 5. Design: reports/message-through-flow-design.md (forks F1–F9, recommended options taken overnight).
6. S1 (Flow sole pane writer: pane lease, Vet/Deliver/Command on meta, Psyche-only meta gate) and 7. S2 (Message delivers only through Flow; Priority head; park on busy; Read only by Acknowledge; Threads/Inbox/relay retired). 8. S1 fixes: flow 0.16.0 9aa9bf88, message 0.16.0 f1843dba and contracts — all green on Prometheus, branches s1-/s2-e167d8, not deployed.
9. Home bookmark flow-message-016-e167d8 for 0.16 (message module rewrite, store move-aside, MessageNexusPath) — wound down at 99% usage; state in reports/home-016-state.md.
10. Launched Psyche Fable b860be as da88cf's successor on "go successor" (reports/fable-successor-*.md); announced to seats.

## Lessons
- A gone pane must never retire a flow; List must not write.
- Shared primary tree: concurrent jj commits race; fetch+rebase before push.
- Unprimed recipients may read a datom letter as injection.

## Open for the living
- F1–F9 of the design (all taken on recommendation, reversible). Tension: dropping raw Flow send vs the earlier "use it raw to send messages".
- When Flow/Message 0.16 deploys: own activation after step 2 lands (proposed), or sooner.
- Inherited from 88475f: subagent system prompts; compensation-messenger-clj fallback line; claude-harness wording; 077114 vs Opus line.
- Zeus update routed to b860be.
- Stale primary/flow submodule at Flow 0.9.0.
No Beads opened or closed.
