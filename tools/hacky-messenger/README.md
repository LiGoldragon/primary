# Hacky Messenger

Plain-string flow messaging through the installed Herdr. No new daemon, socket,
or terminal multiplexer. Requires Python 3, Bash, Herdr, and Orchestrate.

From primary:

```sh
export PATH="/home/li/primary/tools:$PATH"
export FLOW_ID=6034cc # use your own flow ID
hm-register 6034cc messaging-builder-1 --session messaging-build
hm-list
hm-send 6034cc 'Hello from another flow'
hm-send 6034cc 'Wait until its prompt is presented' --wait-presented
hm-send-abrupt 6034cc 'Stop the current turn and read this'
```

`hm-register FLOW AGENT [--session SESSION]` finds an existing live named agent.
Without a session it searches all running Herdr sessions and rejects ambiguous
names. Re-registering the same terminal is harmless; conflicting reassignment
is refused. Start/place agents using Herdr itself, then register them here.
Agents outside Herdr cannot receive these messages; they must first be placed
in Herdr. This does not move or restart a primary flow automatically.

If a live Herdr agent has already been renamed while its Flow, pane, terminal,
session, harness, and native thread are unchanged, rebind its display name
without creating a new Flow registration:

```sh
hm-rebind FLOW NEW_AGENT_NAME --old-name OLD_AGENT_NAME --session SESSION \
  --pane-id PANE_ID --terminal-id TERMINAL_ID --agent HARNESS \
  --native-thread EXACT_NATIVE_THREAD
```

`hm-rebind` reads the existing Flow binding under the same Orchestrate registry
reservation used for registration and delivery. It requires the supplied old
route and native thread to match the record exactly, then requires exactly one
live Herdr agent with `NEW_AGENT_NAME` at the same session, pane, terminal, and
harness. It refuses a changed identity, a duplicate registered name in that
session, absent or ambiguous live target, retirement, and same-name requests.
The JSON replacement is atomic: a validation or write failure retains the old
record.

Pane moves to a new tab, including within the same workspace, can change
Herdr's pane ID. For one exact live Flow,
`hm-move` holds the same registry reservation used by delivery while it moves
the terminal and follows the verified new pane ID:

```sh
hm-move FLOW DEST_WORKSPACE --session SESSION --pane-id OLD_PANE \
  --terminal-id EXACT_TERMINAL --name EXACT_AGENT_NAME --agent HARNESS \
  --native-thread EXACT_NATIVE_THREAD --process-pid WITNESSED_FOREGROUND_PID
```

The caller must obtain these values from the current HM registration and live
Herdr pane/process metadata immediately before invoking it. It checks the old
binding, native thread, agent, terminal, process PID and destination. The move
creates a new tab in the requested workspace, preserving the terminal and
process. A route hold is persisted before Herdr acts, so a crash or uncertain
move result blocks later `hm-send`. On a post-move validation failure it moves
the same terminal back and rebinds the *new* returned pane ID; Herdr does not
restore the original ID. If compensation cannot be verified, delivery remains
held for manual route repair. It never retires or restarts the Flow. Use one
Flow at a time and verify the resulting HM and Herdr records before another
move. A route hold is not evidence that a Flow has ended.

`hm-list` enriches Herdr's live agents with registered flow IDs and shows stale
registrations separately. `hm-send FLOW MESSAGE` resolves exactly that Flow,
checks the target's Herdr identity, readiness, terminal, and foreground native
thread, then sends a `Machine.Relay` provenance envelope through `herdr agent
prompt`. Quote the message as one shell argument. It prints
`Transported.{ FLOW STATUS }`; `--wait-presented` uses Herdr's five-second
wait and prints `Presented.{ FLOW STATUS }`. Neither grade is a read receipt.

If the Flow has no binding or has a launcher/supervisor transition record,
`hm-send` waits up to ten seconds (override with `--hold-seconds`) while the
registry may be updated. It never falls back to another route. Expiry writes a
durable pending attempt and returns `Held.{ FLOW NotRegistered|InTransition
attempt-ID }`. `RouteHold`, process mismatch, blocked, and identity failures
also send nothing. An uncertain post-prompt result is never retried.

`tools/msg` is retained as a compatibility entrypoint and now delegates to
`hm-send`; it no longer uses the failed central messenger pane.

`supervisor.py --stdin` accepts newline-delimited Herdr pane events from one
Field-run `events.subscribe` process. `pane_exited`, `pane_closed`, and a null
agent status mark the registered binding `exited`; `pane_moved` marks it in
transition. The supervisor does not delete registrations or retire Flows.

## Retirement gate

Ordinary `hm.py deregister` is route repair: it does **not** mean the Flow has
ended. A confirmed retirement must first create an evidence-bound marker with
the exact Flow, Herdr route, native thread, and SHA-256 of a retained lifecycle
receipt:

```sh
hm-retire FLOW --session messaging-build --pane-id w1:p1 \
  --terminal-id term_exact --name exact-agent --agent claude \
  --native-thread exact-native-thread --evidence /absolute/receipt.md \
  --evidence-sha256 exact_sha256
```

After a separately witnessed deregistration, use `hm.py import-retirement` with
the same arguments to preserve that retirement. It never contacts Herdr. A
retired Flow is rejected before HM lists an agent or submits a prompt; malformed
marker storage also rejects delivery. New registrations require an exact native
thread and reject a thread named by any retirement marker. A fresh successor
uses a distinct Flow ID and native thread; a reused display name alone is not
blocked.

`hm-send-abrupt FLOW MESSAGE` supports Codex only: Escape, then prompt (which
supplies text and Enter). It rejects blocked, missing, replaced, and unsupported
agents before sending input. There is no separate soft queue in this version.
Ordinary prompt timing is the recipient harness's behavior.

Registration lives in `~/.local/state/hacky-messenger/FLOW.json`, outside Git.
`HM_REGISTRY` selects another shared registry directory; all communicating flows
must use the same one. The record retains session, pane, terminal identity,
agent name, and harness. Orchestrate reserves this directory during registration
and delivery; contention fails visibly rather than retrying a message. `FLOW_ID`
identifies the calling flow for the reservation. Registration defaults to the
flow being registered when FLOW_ID is absent.

A successful send reports **submitted**, not read or completed. Check recipient
acknowledgement for end-to-end confirmation. Timeout or lost replies can mean
uncertain delivery: never blindly retry. Hard-abrupt can send Escape and then
fail on prompt, which is explicitly reported. Identity checking and prompt are
separate Herdr calls, so a terminal replacement race remains possible. Messages
are bounded to 64 KiB and reject terminal control characters except newline/tab.

Retire a registration by reserving the registry directory with Orchestrate and
removing that flow's JSON file. There is intentionally no automatic reassignment
of a stale flow to a new terminal.

Run the checks:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tools/hacky-messenger -v
```

`check.nix { inherit pkgs; }` exposes the same gate for a consumer's Nix checks.
The unit tests fake Herdr; production delivery evidence is recorded separately
under `flows/6034cc/reports/`.
