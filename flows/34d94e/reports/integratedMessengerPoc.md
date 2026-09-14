# Integrated Message POC: daemon boundary

Codex implementation report, 2026-09-14. This is an isolated-branch POC, not deployment or the completed automatic harness relay.

Later state: [messengerReadiness.md](/home/li/primary/flows/34d94e/reports/messengerReadiness.md) supersedes this snapshot's coupled-submission limitation and branch tips. [hookOrdering.md](/home/li/primary/flows/34d94e/reports/hookOrdering.md) supplies actual hook-field and ordering evidence.

## Published source

- Message: `266f92d2871c`, branch `integrated-messenger-poc-34d94e`.
- signal-message: `5d9baa086379`.
- meta-signal-message: `e1cfbab9ba03`.

These follow the already merged fixture described in `messengerIntegration.md`. The new POC branches have not been merged to main or activated. Message's running user service remains the separately observed 0.11.1 executable.

`SubmitPrompt` now enters through the daemon's actual Unix connection. The resolver checks the kernel peer PID and registered PID/start-time ancestry, then checks an explicit source-to-destination permission. The resolved source is retained in the durable record. The identity used for dedupe and observation is destination, source, and source-event identifier, with length framing rather than ambiguous concatenation.

Delivery writes a producer-owned `Signal<PromptRelayDelivery>` containing source, destination, origin and the typed envelope, including original raw text. `ObservePromptReceipt` names source, event and destination; the connection must resolve to that destination. A successful transport write and an authenticated observation operation remain distinct states.

Review exposed an ordinary-socket registry bypass: a caller could replace an allowed source's process pin. With a nonempty relay permission list, the POC now rejects runtime identity/endpoint mutations. The trusted sandbox parent must initialize the registry before daemon startup. This is a bounded process-identity check under trusted filesystem/bootstrap control; it does not establish isolation from a hostile owner of the same Unix account.

The changed record uses a new `prompt_relay_v2` family. Old relay rows are not interpreted as having a known source. Preservation of the old relay family is structural; this change has no independent populated-v5-relay conversion witness and does not automatically replay those legacy rows.

## Executed evidence

The implementation and independent test worker report the coherent Cargo suite passing 31 tests, including eight relay cases and two ingress test entries. The ingress witness uses separate child processes for source, destination and another registered agent, with real Unix sockets and PID/start-time pins. It covers:

- Allowed source-to-destination delivery and the complete decoded delivery frame.
- Unregistered submission and a registered but unpermitted source.
- Attempts to reseat or rebind the allowed identity through the ordinary socket.
- Source/other-agent observation rejection, wrong source/event rejection by the destination, and an exact-key accepted observation.
- Duplicate admission with no second delivery and peer/receipt kinds with no outbound delivery.
- Bounded child-output waits and child/daemon cleanup.

The relay cases also distinguish two permitted sources using the same event identifier and retain their distinct records after reopening the store.

Root directly ran separate Nix validation against this coherent source:

- Evaluation, execution session58628: `timeout --signal=TERM --kill-after=30s 180s nix eval --no-write-lock-file --raw '.#checks.x86_64-linux.default.drvPath'`, exit0. Derivation: `/nix/store/qqbpmv3xlwk6can6pq4l01097qhqaaf2-message-test-0.12.0.drv`.
- Build, execution session44575: `timeout --signal=TERM --kill-after=30s 600s nix build --no-write-lock-file --max-jobs 0 --no-link '.#checks.x86_64-linux.default'`, exit0. Output: `/nix/store/rh4gjwmw95j2ypjv5g0w3qiycnx4syzy-message-test-0.12.0`. The log identifies the configured Prometheus builder; local builds were disabled.

This is the default Nix check, not all flake checks. The earlier worker-interrupted 30-second evaluation was not a passing check; the root's retained executions above supersede that incomplete attempt.

## Remaining harness boundary

No prompt-submit hook is installed. No real unmarked human prompt has been automatically delivered by this POC. The authenticated receipt tests exercise separate destination processes; they do not establish that Claude or Codex recorded a new user turn.

Current registry readiness only establishes a bound, non-dead endpoint. The eventual adapter must observe actual harness busy/dirty state. Delivery is still coupled to submission; bounded admission must be separated from downstream attachment before a hook can safely return while its recipient is busy.

Claude's documented `UserPromptSubmit` input has session and transcript paths plus prompt text, but no prompt UUID. A reader found `promptId` in the actual transcript schema; whether the user record exists before this hook returns remains unproved. Hashing prompt text would collapse two identical human prompts. The proposed capture must use a witnessed source-event identity, fail closed when it cannot establish one, and never invent a new identity to retry an ambiguous delivery.

A new sandbox session can take an explicit `--settings` hook file. This does not retrofit a launch flag into the existing Fable process. A watched-file reload is a separate capability, with no current-session opt-in witness here. The next bounded proof should establish hook/transcript ordering and durable admission before attempting the living's live prompt. Typed kind and registered process identity remain separate from proof of human authorship.

## Sources

- [Message engine](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/engine.rs)
- [Relay persistence and keys](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/relay.rs)
- [Distinct-process ingress tests](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/tests/prompt_relay_ingress.rs)
- [Relay fixtures](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/tests/relay_fixture.rs)
- [Merged fixture evidence](/home/li/primary/flows/34d94e/reports/messengerIntegration.md)
- [Host deployment proposal](/home/li/primary/flows/34d94e/reports/messengerDeploymentPlan.md)
- [Claude hook reference](https://code.claude.com/docs/en/hooks), consulted by the read-only integration worker.
- [Claude settings reference](https://code.claude.com/docs/en/settings), consulted by the read-only integration worker.
