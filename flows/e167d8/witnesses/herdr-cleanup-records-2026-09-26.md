# Herdr cleanup: records taken before closing, 2026-09-26

The cleanup subflow of e167d8 recorded these one-line records on the living's order of about 14:10: "Just close all these sessions ... This needs to happen right now."
The first copy of this file was written before any closure. The shared workspace lost it, and it is restored here with the same content.
Session is `messaging-build` unless marked `default`.

## Closed seats with a route (retired or deregistered in messenger)
- 38de5b | wD:pR term_65c500aa730757c | Psyche Fable 38de5b (claude-fable-5-1 medium), crossover since b7ba00 took over. Native thread 38de5bbb-be48-4bae-883e-2d622fb79c9e. The coordinator ruled that it is closed anyway. See the in-flight state in the report.
- 9c7514 | wD:pW term_65c55829fcb1088 | companion Psyche Sonnet 9c7514 (claude-sonnet-5 low), pane titled "Psyche Opus 077114", idle. Native thread 9c7514c1-9da9-48b9-b5af-025c4f38f468.
- da88cf | w18:p1 term_65c5a260c79e78d | PsycheV2 Fable da88cf (claude-fable-5-1 high), crossover, said "Nothing is pending on this seat". Native thread da88cf8d-06f7-4a70-9c7a-e7c8cdb78908.
- 88475f | w17:p1 term_65c5883e612c88a | PsycheV2 Opus 88475f. Claude has exited and only the zsh shell remains. Native thread 88475fd7-e328-4e11-9094-db2139a08fe0.
- b860be | w1A:p1 term_65c5d073c6e318f | PsycheV2 Fable b860be. Claude has exited and only the zsh shell remains. Native thread b860be42-d89d-4eee-a0c2-216ec0107a86.
- 00f95a | wM:pB term_65c3ff8204dc373 (pane already gone) | Mind Sol 00f95a (codex), replaced by 56ae53. 56ae53 is live at wM:pJ, pid 1260045. Native thread 01a0d4ec-9746-7340-b60c-84300f95aa7c.
- ae7862 | wM:pH term_65c63fb4607a199 | Mind Astra ae7862 (gpt-6-astra medium). Gave its FinalResponse (independent review reported) and is done. Native thread 01a0de32-18a6-71b2-bcef-550ae7862537.
- 9e7ea5 | wK:p3 term_65be21c518a7932 | Mind Astra of 98ac2e ("Retained Mind High 9e7ea5"). Only the dead zsh shell remains and the route is STALE. Native thread 01a0bcea-a838-7421-ab1d-43c9e7ea522d.
- 98ac2e | wK:p1 term_65be107ba098b31 (pane gone) | Mind Astra of 0ab019, STALE. Native thread 01a0bcaa-6dcb-7c93-a9e2-49f98ac2e0e5.
- 0ab019 | wC:p1 term_65bc6d207da1421 (pane gone) | mind-astra-of-893603, STALE, NeedsBinding.
- 9a79dc | wE:p1 term_65bc71c76d0f723 (pane gone) | opus-review-of-af762b, STALE, NeedsBinding.
- c3e42e | w8:p1 term_65bc6110b49581c (pane gone) | field-sol-of-3b1574, STALE, NeedsBinding.
- cf3553 | w6:p1 term_65bc5b7c5368a1a (pane gone) | field-astra-of-33ba2b, STALE, NeedsBinding.
- effa1b | wC:p2 term_65bc91cf241bf2b (pane gone) | mind-sol-of-0ab019, STALE, NeedsBinding.

## Closed seats without a route
- 077114 | wD:pY term_65c588e0314a38b | Psyche Opus 077114 (claude-opus-5-5 medium), idle. It was unregistered: hm-list shows name psyche-opus-077114 with no flow.
- (none) | w1F:p1 term_65c643cd49aec9a | blank codex gpt-6-sol pane left by a failed Start ("This conversation is unavailable").
- (none) | w13:p1 term_65c429f01d0607b | codex gpt-6-luna with no thread ("This conversation is unavailable"), idle since 09-24.

## Closed dead shell panes (no agent process)
- wD:p9 | shell left by retired 836818 (Psyche Fable).
- wQ:pA | shell labelled "Field Medium 753e69"; 753e69 is retired.
- wQ:pF | shell in the deleted worktree field-high-refresh-753e69.
- w0:p3, w0:p4 | leftover operator shells (launch scripts for mind-sol-9ddcbc; a failed messenger attempt).
- w12:p1 | shell left by a disconnected codex resume of 01a0cfbd (old ~/.codex app-server).
- w1E:p1 | shell left by a terminated codex gpt-6-astra.
- default wA:p1 | shell in workspace "field-terra-bootstrap".
- default wC:p1, wC:p2 | shells in workspace "Psyche Medium Opus refresh" (a failed idle probe; "Psyche Medium (claim pending)").

## Stray harness processes outside Herdr
- pid 995643 | `claude --dangerously-skip-permissions` in a Ghostty zsh (ppid 995476, under ghostty 4578), cwd /home/li/primary, started 2026-09-15 09:41. This is the old Claude outside Herdr.
- pid 3809023 | Claude Code `daemon run --origin transient`, spawned by the sandbox `flows/024bc7/sandbox/bgtest`, started 2026-09-13. It has unclaimed bg-spare pairs 999171/999184, 1269161/1269176, 1482700/1482708, 2803665/2803682 and 883655/883671, and no live seat is connected to it.

## Sandbox sessions
- No fms-*, s2e167d8 or e167d8-prompt-reply-probe Herdr session exists. `herdr session list` shows only default and messaging-build, and no process or socket matches those names.
