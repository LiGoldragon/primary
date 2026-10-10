Presentation.{ «Harnesses and remote control» }

A harness is the program a model works inside: Claude Code, Codex, OpenCode. Flow decides everything about a session; the harness runs the model and reports what happened. Say "yes" to a number to land it; for two texts, name the number.

**1. Which harnesses**
Kind: vision. Module: vision-flow. Action: edit.
> Two harnesses run today, Claude and Codex. OpenCode is the open-source harness and the third seat. Pi is dropped.

Rests on: 27 Aug, 26 Sep, 4 Sep.

**2. The third harness**
Kind: vision. Module: vision-flow. Action: edit.
Text 1:
> The open-source seat is built on OpenCode now.

Text 2:
> The DeepSeek harness is tested against OpenCode before the open-source seat is built.

Rests on: 26 Sep for 1; 4 Sep for 2.

**3. One declaration per harness**
Kind: intent. Module: operating-system. Action: edit.
> Each harness is declared once and used everywhere. Desktop apps run that same build and never install one themselves.

Rests on: 25 Aug, 26 Aug.

**4. No wrapper**
Kind: knowledge. Module: claude-harness. Action: edit.
> Every harness is called by its own name, with prompts off set in its configuration. No wrapper adds the skip-permissions switch.

Rests on: 5 Sep.

**5. Flow chooses the id and title**
Kind: vision. Module: vision-flow. Action: edit.
> The harness's session id is the flow id. Flow picks it and the title before the session starts and puts both in the launch command, so no model spends a turn finding them. Subflows carry their parent's id.

Rests on: 26 Aug, 3 Oct, 1 Oct, 31 Aug.

**6. Hooks report only to Flow**
Kind: vision. Module: vision-flow. Action: edit.
> Every hook is a small program that sends one typed event, carrying the session id, to Flow and makes no model call. Flow alone decides what follows: reaping, books, quota.

Rests on: 30 Sep, 1 Oct.

**7. The hooks he has named**
Kind: vision. Module: vision-flow. Action: edit.
> Session start registers; session end unregisters and starts reaping. Idle moves a session to a new harness version, one at a time. After work, quota and context figures ride on the session's next message. A marked presentation block goes to be made into a book without a tool call. Every useful hook on every harness is written down first.

Rests on: 23 Sep, 29 Sep, 30 Sep, 18 Sep, 1 Oct.

**8. The silence timer**
Kind: vision. Module: vision-flow. Action: edit.
> A timer restarts each time he speaks and fires after 15 minutes of quiet.

Rests on: 19 Sep. The 15 is his "I don't know"; name another number if you like.

**9. His prompt copied to the other harnesses**
Kind: vision. Module: vision-flow. Action: edit.
Text 1:
> When he speaks to one harness, a hook copies his words to the others at once.

Text 2:
> His words go only to Flow, which decides who else hears them.

Rests on: 13 Sep for 1.

**10. Herdr layout**
Kind: vision. Module: vision-flow. Action: edit.
Text 1:
> One full-screen Herdr per layer, each on its own desktop, run by Flow.

Text 2:
> One Herdr run by Flow, with a space for each aspect, Mind, Psyche and Field, that can still message each other.

Rests on: 14 Sep, 24 Sep for 1; 19 Sep for 2.

**11. Remote reach**
Kind: intent. Module: operating-system. Action: edit.
Text 1:
> One remote server, rooted in his workspace, serves Claude and Codex together. Closing a desktop app kills no session.

Text 2:
> Each harness has its own remote server; a new one comes up beside the current one and becomes current once it works.

Rests on: 28 Aug for 1; 15 and 17 Sep for 2.

**12. What the harness never decides**
Kind: vision. Module: vision-flow. Action: edit.
> The harness never decides whether a subagent runs, which model, at what effort, nor its id, title, folder, system prompt, permissions, or start and end. Flow decides; the harness runs the model and reports events.

Rests on: 28 Sep for the first part; the rest is proposed.
