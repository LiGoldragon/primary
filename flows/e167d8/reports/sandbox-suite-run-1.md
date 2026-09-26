# Flow/Message sandbox suite: run 1

Subflow of e167d8, 2026-09-26. The first run of the reusable semi-sandbox at
`tools/flow-message-sandbox/`, against Flow 0.16.0 `9aa9bf88e3ff` and
Message 0.16.0 `f1843dbaa63f` (both built by `nix build` from those
revisions; the builds ran on the Prometheus remote builder). Seats: Claude
Haiku 4.5 (`claude-haiku-4-5-20251001`, effort low) and Codex Luna
(`gpt-5.6-luna`, effort low), on the living's existing logins.

## How to run

    tools/flow-message-sandbox/flow-message-sandbox run [N ...]

It stands up an isolated Flow Nexus and Message Nexus. Each has its own HOME
(store) under `~/.cache/flow-message-sandbox/<run>/`, its own sockets under
`/run/user/1001/<run>/`, and a capped user scope. It also stands up a Herdr
session named after the run, with five seats bound by `MetaBindExisting`.
It then runs the scenarios, tears everything down, and checks that nothing is
left. `up`, `scenarios <run> N...` and `down <run>` split the same steps.
The results are in `~/.cache/flow-message-sandbox/<run>/results.{md,json}`,
with pane and transcript evidence in `evidence/`.

## Results

The full run is fms-b904ee. Scenario 4 was run again as fms-0b34b2 after a
test-harness fix, described below the table.

| # | Scenario | Verdict | Observed |
|---|---|---|---|
| 1 | Soft to idle Haiku | pass | `Presented`; the recipient replied with the word |
| 2 | Soft to working Luna | pass | `Parked`, then `ReceiptObserved … Presented` on rest; the transcript holds the letter exactly once |
| 3 | MiddleAbrupt to working Codex and Claude | pass | both `Transported` (not parked); Codex took it as a steer; both replied |
| 4 | HardAbrupt interrupt | Codex pass, Claude **fail** | Codex: `Observed Presented`, reply after 5 s of a 90 s sleep. Claude (rerun): `Unobserved Transported`; the letter waited until the foreground `sleep 90` ended (reply after 105 s) |
| 5 | /compact, `!`, ESC, CR bodies | pass | `SendRejected.BodyRefused` HarnessCommand ×2 and ControlCharacter.67 / .76; no marker in the pane; the pane text did not change; Flow `Vet` refuses too |
| 6 | Two senders, one pane at once | pass | one `Presented`, the other `Parked`, then landed; each letter is whole and alone in the Codex transcript |
| 7 | Acknowledge by MessageId | pass | the recipient ran `message 'Acknowledge.<id>'` from its letter and the receipt became `Read`; a non-recipient got `MessageRejected.NotRecipient` |
| 8 | Withdraw before delivery | pass | another flow got `NotSender`; the sender got `Withdrawn`; the receipt stayed Withdrawn through rest and a further turn; the body never reached the transcript |
| 9 | Message restart with a parked letter | pass | new PID; the letter landed after the restart; exactly one copy in the transcript |
| 10 | Recipient pane closed mid-delivery | pass | parked letter settled `Refused.RouteUnavailable`; `List` says `Exited`; `ResolveRecipient` answers FlowUnavailable; a new Send is refused; a same-labelled unbound pane never received the letter |
| 11 | Flow Start of a Claude Haiku seat | **fail** | the seat replied exactly `FLOW_LAUNCH_RECEIPT_V2`, yet Start answered `StartAmbiguous.{…}`, and the seat never continued into its brief |
| 12 | Flow Start of a Codex Luna seat | expected-fail | `StartRejected.BindingRefused`, the known fault |
| 13 | 64 KiB body and psyche letter | pass | 65 536 bytes arrived byte-exact once in the Codex transcript (sha256 fa13a07a…). `Psyche.{ context verbatim }` with `"`, `'`, curly quotes, `«…\»` and `\` arrived intact in the Claude transcript (the closing guillemet is datom-escaped as `\»` in the pane text) |

Teardown checks for both runs all came back true. Each process was stopped by
PID and by its run-unique scope unit. No process carries the run's Herdr mark.
The session is deleted and its directory is gone. The socket directory,
stores and homes are removed. `seat/flows` holds only what it held before the
run. Every Herdr session that existed before the run (`default`,
`messaging-build`) still exists. No production socket, store or seat was
addressed: every client ran with the sandbox `FLOW_*`/`MESSAGE_*` sockets, and
the Nexuses ran with the sandbox HOME and XDG_RUNTIME_DIR.

## Product defects

1. **Flow Start (Claude) does not witness a correct launch receipt.** In three
   runs (fms-9bc4f7 twice, fms-b904ee), Haiku answered exactly
   `FLOW_LAUNCH_RECEIPT_V2` and Start returned `StartAmbiguous` with an
   `Existing` transcript cursor. The brief continuation then failed in two
   different ways:
   - In one run, Flow typed `continue` into the composer and never submitted
     it.
   - In another run, Flow typed nothing.

   Either way the seat idles with its brief unbegun. A successful Start still
   needs a second prompt from someone.
2. **HardAbrupt does not interrupt Claude during a foreground tool call.**
   Flow's `[ esc esc ]` interrupt left the recipient in Working
   (`Unobserved`), and the letter was answered only after the tool finished.
   Against a model turn with no running tool, the same keys did interrupt
   (fms-9bc4f7: `Observed`). Codex interrupts in both cases.
3. **Flow Start (Codex) is refused with `StartRejected.BindingRefused`.** This
   is the known fault, reproduced against a private app-server.
4. **The refusal reason names the wrong lifecycle.** A Send to a flow that
   `List` reports as `Exited` is refused as `RecipientRefused.{ … FlowStopped }`.
   The Deliver refusal vocabulary has no Exited reason, so it names Stopped,
   which is Flow's own act.

Two notes that are not defects:

- After a Message restart, the MessageId counter restarts at `…000`. Ids stay
  distinct only because of the timestamp prefix.
- A MiddleAbrupt to a recipient that is already working is graded
  `Transported`, never `Presented`, because Herdr cannot show it reacting.

## Harness facts found while building it

These were fixed in the suite, not in Flow or Message.

- Herdr refuses `agent start --executable` for any client its own config does
  not list. The suite passes the configured `codex-stable-flow-client` with
  `--remote` pointed at a private `codex app-server --listen unix://…`.
- The flow-id claim marker needs a 32-hex identity, in UUID v4 form for
  Claude. With a hand-written marker, every route read answers Unknown.
- Unprimed seats treat a datom letter as a prompt injection. Every seat is
  primed with an appended system prompt (Claude) or developer instructions
  (Codex).
- Claude asks once whether to trust its seat directory. The suite uses one
  stable directory, `~/.cache/flow-message-sandbox/seat`, and answers the
  question on the first run.
- `systemd-run --user` needs the real XDG_RUNTIME_DIR. The Nexus gets the
  run's own directory through `env`, in the same process.
- Claude moves a long `sleep` to the background and ends its turn, so a
  recipient that is "working" is no longer working. This produced a false
  Claude verdict for scenario 4 in fms-b904ee. It was fixed by asking for a
  foreground sleep and checking Working at the moment of the send, then
  scenario 4 was rerun.
- Codex's app-server fetches plugin marketplaces into `~/.codex/.tmp` when it
  starts. Stopping its scope ends that fetch.

## Moving it into persona-test

The persona-test skeleton's `packages/message-flow.nix` is the target. Moving
the suite there takes these steps:

1. Add the Python modules as the runner's drive, for example through
   `pkgs.writers.writePython3Bin`, with herdr, codex and claude as runtime
   inputs.
2. Take the Flow and Message packages from `flake.lib.components` instead of
   `Pins.build`.
3. Keep the scenarios unchanged.

One tension is left for the living. compensation-nix, and the persona-test
stub, copy login files into a temporary HOME. This brief said never to copy
them. Copying would also cut the seats off from the living's Herdr
executable allowlist, from Codex's trusted `/home/li` and hooks answers, and
from the stable Claude seat trust. The move therefore needs one of two
rulings:

- which files are copied, or
- that the runner keeps HOME and isolates only the Nexus homes, as this suite
  does.

## Sources

- Runs: `~/.cache/flow-message-sandbox/fms-b904ee/` and `fms-0b34b2/`
  (results.json, results.md, run.log, evidence/). Development runs
  fms-9bc4f7, fms-019d37, fms-ce264b, fms-ae64a5 and fms-5f6f5c were torn
  down clean.
- Flow source at 9aa9bf88: `crates/flow-nexus/src/herdr.rs` (claim marker
  grammar, route checks) and `herdr/launch.rs` (Claude/Codex launch
  arguments, receipt footer).
- The S2 end-to-end test commands of this flow's earlier subflow (the Claude
  transcript of e167d8, subagent a43d94423714d46fb).
- Herdr config `~/.config/herdr/config.toml` `[agents] codex_executables`.
