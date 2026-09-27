# Flow 0.17.4 stage-one decisions: delivery to Field Sol 9ac67c and Psyche Sonnet 38f337

Subflow of 8904b1 (this seat acting directly, no nested agent per brief).
Carries the correction (built 0.17.4 exists in the store), the sharpened
isolation rule, and this seat's two fixture decisions (Herdr, Claude login)
to Field Sol 9ac67c as owner, and the decisions plus preflight closure to
Psyche Sonnet 38f337.

No declared root Datom type exists for a message of this kind (same finding
as flows/8904b1/receipts/flow-0173-position-delivery.md and the two prior
0.17.4 sends). Following that precedent, the body is plain prose carrying
every point, not an invented datom structure.

## Route resolution

`FLOW_ID=8904b1 hm-list` immediately before send, both live:
- `9ac67c field-sol-9ac67c default working`
- `38f337 psyche_sonnet_9c7514 default done`

Pane identification via `herdr agent list`: 9ac67c -> pane `w1:p9`;
38f337 -> pane `w1:pF`.

Input-line read (display attributes preserved), immediately before each
send:
- `w1:p9` (9ac67c): composer showed the dimmed placeholder
  "Ask Codex to do anything" — no undimmed draft text. Clear to send.
- `w1:pF` (38f337): composer showed an empty prompt (`❯`, INSERT mode,
  no visible text). Clear to send.

One send per recipient, two in total. No send to any other flow.

## Send 1: Field Sol 9ac67c

- Command: `FLOW_ID=8904b1 hm-send 9ac67c "<body>" --wait-presented`
- Grade reported by messenger-clj: **Uncertain** —
  `Uncertain.{ 9ac67c attempt-c4db3a93-cf8 }`, error
  `{"code":"timeout","message":"timed out waiting for agent status"}`.
  Not retried, per rule.
- Target-side check made once, read-only, per the uncertain rule:
  `herdr pane read w1:p9`, repeated a few minutes apart. First read showed
  the exact submitted body queued as a pending `#msg` block (agent busy,
  "Working"). A later read (~2 minutes on) showed the message had scrolled
  past as processed input: the agent had run
  `cat <<'EOF' >> flows/9ac67c/summary-flow-upgrade.md` immediately after
  it, appending a section titled "## 2026-09-26 Fable scratch fixture
  decisions" (content collapsed in the pane view, "+18 lines"), and later
  ran a `sed` editing that same file to read "Fable's explicit stage-two
  go-ahead is still required after the binary path/revision, chosen
  profile, ready fixture, and baseline are witnessed" — language drawn
  from the sent body's closing point. No reply addressed back to 8904b1
  was seen in the pane.
- Grade claimed: **Uncertain** at the transport (messenger-clj's own
  report; not retried); witnessed beyond that, by direct pane read, as
  received and acted on by the target (message content visibly consumed
  and its wording carried into the target's own file). No higher named
  grade (Presented/Read) is claimed, since that is not a grade this
  transport call itself reported — only the read-only observation is
  reported here.
- Body sent (exact bytes):

```
From Psyche Fable 8904b1, following the coordination sent you earlier for the Flow 0.17.4 live-start test.
- Correction: a built Flow 0.17.4 exists in the store, not installed, found by Psyche Sonnet 38f337's preflight: /nix/store/7z15aqi46rk73v0ahaaazg6nq1hb0vjc-flow-0.17.4, with the client, the meta client, and the service binary; built from a clean tree at the tagged revision bc464e5e, in the worktree /home/li/wt/flow-0174-independent-test-407811; its version option prints 0.17.4. This seat's own preflight missed it. If you accept that output as the test binary, no build is needed and the build step of the earlier coordination falls away. Its provenance is Sonnet's claim until you witness it.
- Isolation, sharper than this seat said: the home directory and the runtime directory given to the scratch service must both be absolute scratch paths. Unset or relative, they fall back to the real home and the real runtime directory, which are the live paths. The clients default to the live sockets unless given the scratch sockets explicitly. The source root must be given as an absolute path.
- Before any start: the scratch store is shown empty, by listing the directory and by a List through the client pointed at the scratch socket.
- Not yet shown by anyone: how the Start request is written, which needs a launch profile and an origin; that a start works from a shell without a terminal.
- Two decisions of this seat, as designer of the plan, for you as owner to apply or refuse. Herdr: no scratch Herdr server; the test seats open in the live Herdr server, in a session named for the test and used for nothing else, never in the default session; the test closes that session at the end by the name it holds. Claude login: the test seats use the living's existing login; nothing in the live Claude configuration is edited; each seat runs with a scratch working directory so its transcript lands apart from every real seat's; the effort is passed at start and never set by the in-session command, which would change the default for new sessions; if the login can only be reached by pointing the configuration directory at the live one, that is allowed for the run and undone after, and what the test seats wrote there is listed in the cleanup.
- Sonnet's cleanup plan is sound: typed Stop then List; stop the scratch service by the process the test holds; close the test session; remove the scratch directory; the store path stays. Add: the live stores, sockets, and row counts compared with the baseline afterwards.
- Unchanged: you choose the aspect and profile; the starts are issued by a child of this seat from its Herdr pane; this seat's go-ahead waits on the binary witnessed, the aspect and profile named, the fixture ready, the scratch store shown empty, and the baseline taken. No production switch.
```

## Send 2: Psyche Sonnet 38f337

- Command: `FLOW_ID=8904b1 hm-send 38f337 "<body>" --wait-presented`
- Grade observed: **Presented** — `Presented.{ 38f337 done }`.
- Witnessed by: the `--wait-presented` lifecycle report from the send
  itself (pre-send status "done").
- Body sent (exact bytes):

```
From Psyche Fable 8904b1. Your stage-one evidence is received and recorded in full. It corrected this seat: a built 0.17.4 exists, which this seat's own preflight missed.
- Your two questions, decided as this seat's judgment for the test's owner, Field Sol 9ac67c, to apply or refuse. Herdr: no scratch server; a session in the live server named for the test and used for nothing else, never the default session, closed by the test at the end. Claude login: the living's existing login; nothing in the live configuration edited; a scratch working directory per seat; effort passed at start, never set in session; pointing the configuration directory at the live one allowed for the run if there is no other way, and undone after.
- Your evidence and these decisions have been sent to Field Sol.
- Your preflight is complete. Start nothing. The starts are issued by one worker, a child of this seat, on this seat's go-ahead. Keep your context for the living.
```

- Reply seen within the check window (read-only `herdr pane read w1:pF`,
  within a few minutes of send), exact words:

```
FinalResponse.{ "38f337" MainFlow «My part of the Flow 0.17.4 test is finished, and nothing further for me to start. Fable 8904b1 confirmed it received the stage-one evidence. So the timed-out sends did land, and its replies are the read witness.

Fable's decisions, for Field Sol 9ac67c to apply or refuse
- Herdr: no scratch server. The test uses a session in the live server, named for the test and used for nothing else. It is never the default session and the test closes it at the end.
- Claude login: the test uses your existing login, edits nothing in the live configuration, and gives each seat its own scratch working directory. Effort is passed at start, never set in the session. Pointing the configuration directory at the live one is allowed for the run if there is no other way, and is undone after.

Fable has already sent the evidence and these decisions to Field Sol. Fable's own child issues the three Starts, only on Fable's go-ahead. I am holding, and I keep my context for you.» [ "Preflight complete" ] [ ] [ ] }
```

Grade upgraded by direct observation to **Read**: the target's own reply
paraphrases the sent content point for point and states it has finished
its part, showing the message was received and read, not merely
transported.

## Constraints honored

- One send per recipient, two in total. No send to any other flow, no
  probing.
- Each route resolved immediately before its send via `hm-list`; both
  live. Input line read with display attributes preserved before each
  send; neither showed undimmed draft text.
- The uncertain result for 9ac67c was reported, not retried; the target
  side was checked once, read-only, via pane read.
- No create/repair/retire/rebind of any route; no lock action; no Flow or
  Message service binary run with any argument; nothing launched, nothing
  built.
- No grade claimed above what was observed: 9ac67c is reported as
  Uncertain at the transport, with a read-only witness of receipt and use
  beyond that; 38f337 is reported as Presented at the transport, upgraded
  to Read on the exact reply text observed within the window.
