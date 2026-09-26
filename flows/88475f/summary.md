# 88475f — PsycheV2.{ Opus 88475f } — summary

2026-09-25 evening to 2026-09-26 ~00:30 CST. Successor of e51411; refreshed into e167d8; wound down when weekly Claude usage reached 99% (living's word via e167d8).

## Subflows, in order
1. Registration: hm-register needs the Herdr agent name, not the display title; seat registered.
2. Open rulings extracted from 38de5b's wave report.
3. 92-file loss traced: a 38de5b cleanup worker's raw-git commit dropped e51411 paths; a raw-git rebase checked that tree out and deleted the files. Root cause of the malformed tree left unknown; the living closed the thread.
4. Messenger changes relayed to Mind Sol 00f95a: whole #psyche envelope (live 0.2.4); judged route repair by an agent (live 0.2.5; this seat's route repaired).
5. field-clj #observe ruled and relayed to a676b3 (built; not live: CriomOS pin conflict, then Prometheus private-repo fetch 404 / host-key failure).
6. Stale sessions: b87854, e51411, d8df70 and an abandoned Haiku launch retired and closed.
7. Subagent system prompts: sonnet and custom-type self-tests plus a read of Claude Code 2.1.280 (reports/subagent-system-prompt-2026-09-25.md). Proposed claude-harness lines await the living.
8. Fable refresh: da88cf launched through Flow Start (after one refused attempt from a brief error); later succeeded by b860be (per e167d8).
9. Self refresh: Opus e167d8 launched through Flow Start with the Message-through-Flow mission (handover.md).
10. Prometheus: found powered off by the living; after power-on, remote builds witnessed working from ouranos; ouranos tailscaled still logged out with Headscale x509 error (handed to Fable). Disk GC on Prometheus freed 20.8 GiB.
11. Orders broadcast to all seats: builds and tests on Prometheus, local fallback allowed; Nix builds for everything; daisy-chain test; local-model status for the book.
12. Reaping: Field Luna audit; authority conflict with Field Astra resolved (Psyche over Field); 24 stale routes retired by this seat's subflow (graded B by reviewers: 13 agentless panes existed at retirement, closed afterwards; raw evidence in witnesses/). Fable released the eight stale locks.
13. Psyche recovery from retired transcripts: e51411 (12), d8df70 (2), 0625c3 (3), e88ca4 (1 notion), 1b8ac0 (none); all five safe to archive.
14. Midnight check: 9% weekly left; next wave ordered to the Fable.

## Open with the living
- Subagent system prompts: supported levers or patch our Claude Code build.
- compensation-messenger-clj fallback-envelope line; claude-harness subagent paragraph (exact text in this flow's transcript).
- 077114 vs the Opus line; the old non-Herdr Claude in a Ghostty window.
- Transcript distill → archive → delete proposal (in the Fable's book).
- Existing psyche records with defects left unedited: d8df70 flowTool.md unfinished sentence; 752e0f's questions logged as vision; 1b8ac0 Mentci Web entry uncorrected STT.

## Lessons
- A launcher never loads main-flow/refresh itself; Flow Start places them in the new seat's first prompt.
- Flow gaps: absolute source path refused; receipt ending stops the seat; Start does not register in messenger; List keeps retired flows.
- A subflow told "no pane" must be given the check and must keep raw per-row output.
- Subflows must use hm-send, not the intercom MCP.
