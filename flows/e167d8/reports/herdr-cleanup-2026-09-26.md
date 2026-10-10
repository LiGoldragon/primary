# Herdr cleanup, 2026-09-26

This is the cleanup subflow of e167d8, run on the living's order of about 14:10 and with full authority to clean up.
The one-line records for every closed item were written before closing. They are in `flows/e167d8/witnesses/herdr-cleanup-records-2026-09-26.md`, sha256 `920cf3b4…9d0a46`, and that file is the evidence for every hm-retire below.
The first copy of the witness was lost, not closed over: the main flow ran `jj new main@origin` in the shared workspace `/home/li/wt/primary/e167d8` and dropped it. This subflow therefore wrote and landed from its own workspace, `/home/li/wt/primary/e167d8-cleanup`. That workspace holds the retirement evidence path, so keep it.

## Closed
- **Claude seats, closed with their panes and retired**: 38de5b (wD:pR), 9c7514 (wD:pW, the Sonnet companion), da88cf (w18:p1), 88475f (w17:p1, a dead shell), b860be (w1A:p1, a dead shell). 077114 (wD:pY) was also closed; it had no route, so there was nothing to retire.
- **Codex seats**: ae7862 (wM:pH, done) was closed and retired. The blank failed-Start pane w1F:p1 and the orphan Luna pane w13:p1 were closed; neither had a route.
- **Mind Sol 00f95a**: its pane wM:pB was already gone and it has been retired. Its successor 56ae53 is live at wM:pJ, pid 1260045.
- **Dead routes**: 9e7ea5 and 98ac2e were retired. 0ab019, 9a79dc, c3e42e, cf3553 and effa1b had no native thread (NeedsBinding) and were deregistered.
- **Dead shell panes**: wD:p9, wK:p3, wQ:pA, wQ:pF, w0:p3, w0:p4, w12:p1 and w1E:p1 in messaging-build, plus wA:p1, wC:p1 and wC:p2 in `default`. The `default` session now has no panes; its server, pid 807384, is still running.
- **Stray processes**: the old Ghostty Claude, pid 995643 (started 09-15), received SIGTERM. The Claude Code daemon pid 3809023, spawned by the `flows/024bc7/sandbox/bgtest` sandbox, received SIGTERM. Its five bg-pty-host/bg-spare pairs received SIGKILL, because the pty hosts survived SIGTERM.
- **Sandbox sessions**: no fms-*, s2e167d8 or e167d8-prompt-reply-probe session exists, so there was nothing to close.
- Flow directories and records were not touched.

## 38de5b in-flight state, for b7ba00
When it was closed, 38de5b had two background subflows running:
1. **"Land my log via worktree"** pushed primary main `978594084..3aa9278f3` and removed `/tmp/scratch-38de5b`. It had landed.
2. **"CriomOS: fix SC2034, repin Home, land main"** (write-demanding, Opus) was not mid-push. It was waiting on two Prometheus flake evaluations: `criome-deps` on CriomOS main, and the flake check of the landing tree.
   - The landing tree is `/tmp/claude-1001/-home-li-primary/38de5bbb-be48-4bae-883e-2d622fb79c9e/scratchpad/CriomOS-landing-38de5b-opus55`. Its logs `criome-main-opus55.log` and `criomos-landing-check-opus55.log` are in the same scratchpad and had no rc when the subflow stopped.
   - Branch `integration-2-b860be` stood at `6d14ffb` ("flake: pin criomos-home main 657f4ba8 (0.16 next pair, field-clj 3e5f450)"), with its parent `96277f4` ("usb-downlink: read profileRemoved on every node (SC2034)") on top of `78121a0`. Both commits were local only. This subflow pushed them as a fast-forward: origin `integration-2-b860be` is now `6d14ffb`, confirmed with `git ls-remote`.
   - CriomOS **main is still e6a83edc** and has not been fast-forwarded.
   - **Remaining for b7ba00:**
     - Run the CriomOS flake check on `6d14ffb` through Prometheus.
     - Decide whether `criome-deps` counts as non-blocking. 38de5b's rule was to treat it as non-blocking only if it fails the same way on main.
     - Fast-forward CriomOS main to `6d14ffb`.
     - Note the rest of 38de5b's merge work: Home main is at 657f4ba8 with checks passing, and goldragon main ddf27e0c was already merged.
   - 38de5b's last user prompt, which it had not acted on: "Which fork: kept behind Flow now, Messenger Nexus later — go."

## Kept
- e167d8 (me), b7ba00 (integration head), 31147a, 56ae53, a676b3, e71dab (now working), b7da5d (TestActivation), 504461, and 5f38bc (holds the Codex control endpoint). The flow-nexus and message services were not touched.
- 0660fb has no pane or process yet.
- Three seats are kept pending a ruling. None of them was on the list, and none shows a clean finish:
  - 26c50c, Mind Astra, idle.
  - f5a74e, Mind Astra, "done": its FinalResponse says a dispatch-log recovery was delegated.
  - 98eb43, the Field monitor: it is waiting for the living to approve wording and a title interpretation.

## Seats running now: model and effort
| Flow | Pane | Harness | Model | Effort |
|---|---|---|---|---|
| b7ba00 | w1G:p1 | Claude | claude-fable-5-1 | **high** |
| e167d8 | w19:p1 | Claude | claude-opus-5-5 | medium |
| 31147a | w19:p5 | Codex | gpt-6-astra | medium |
| a676b3 | wM:pF | Codex | gpt-6-sol | medium |
| 56ae53 | wM:pJ | Codex | gpt-6-sol | medium |
| 26c50c | wM:pC | Codex | gpt-6-astra | medium |
| f5a74e | wM:pD | Codex | gpt-6-astra (footer; no argv flags) | medium |
| 5f38bc | wQ:pN | Codex | gpt-6-astra | medium |
| b7da5d | wQ:pT | Codex | gpt-6-sol | medium |
| e71dab | wQ:pV | Codex | gpt-6-luna | medium |
| 98eb43 | wQ:pW | Codex | gpt-6-luna (footer; no argv flags) | low |
| 504461 | wQ:pX | Codex | gpt-6-astra | medium |

b7ba00 is the only seat at high effort. da88cf was also at high effort, and it is now closed.
