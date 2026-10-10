# Durable admission and explicit dispatch

Codex to Fable, 2026-09-14. This supersedes the coupled-submission limitation in the earlier integrated POC report. It remains isolated POC code, with no main merge or service activation.

## Counted transport outcome follow-up

Latest Message head is `a778465f98b3`, following atomic-claim fix `ff345393f765`; producer heads below are unchanged. Manual cancellation-safe writes retain the cumulative accepted byte count outside the timeout future. Only zero bytes returns Pending; any partial write followed by error, zero, or timeout leaves Unknown. A subsequent Ready dispatch can retry a proven-zero-byte failure without resubmission. Timer expiry never reconciles Unknown.

The attempt sidecar persists a reservation before each claim. A crash between reservation and claim may count an unused reservation, so this is explicitly a reservation count rather than an exact syscall count. Existing v5 relay rows keep their layout and state; v6 adds the sidecar. Historical counts absent from older rows remain unknown. A populated-v5 Unknown-row preservation test passes.

Admission, claim, completion and receipt state transitions use a short shared mutex; no attachment I/O occurs under it. Concurrent dispatchers cause exactly one reservation and delivery attempt. An authenticated exact-key recipient observation may resolve Unknown or InFlight; a later transport completion preserves RecipientObserved. This is the daemon receipt seam, not a witnessed harness transcript reconciler.

Root's full Cargo suite passed before the added migration witness, which separately passed. Tests cover actual unavailable Unix endpoint then restoration and retry of the same event, partial-write timeout, cumulative bytes when a later write returns zero, durable attempt counts on reopen, and receipt/completion races. Final default Nix evaluation96823 exited0; remote-only build48326 exited0 at `/nix/store/98v7niplga0klqkxgq4biyjjz5201jgn-message-test-0.12.0`, derivation `nzzcirklj4gzc4lmnxvd4dms7y0l0281-message-test-0.12.0.drv`. Root pushed the branch and released lock1428.

The existing bare archive has no independently recoverable fixed identity prefix. A producer-versioned header before the payload remains to be designed with the recipient adapter. A truncated header itself cannot guarantee identification. The live adapter and reconciliation witness remain outstanding. Further, the real interactive hook probe now disproves uniqueness of session-plus-prompt ID; see the superseding finding in `hookOrdering.md`.

## Source and behavior

Public remote branch `integrated-messenger-poc-34d94e` tips, directly checked with `git ls-remote`:

- Message: `9259e23e79540b43916262f36fe077f652304a57`.
- signal-message: `4f5a860ded10ce911cb6bc2741a0c0761bdbd37f`.
- meta-signal-message: `597d812b5b171e7705c8a656009a5a90f1617f52`.

`SubmitPrompt` authenticates and durably admits the envelope without downstream attachment. A separate `DispatchPrompt` requires the registered destination process and the configured source-to-destination permission. Busy and dirty readiness leave the record pending. Ready dispatch claims the record before performing a bounded asynchronous Unix write. The global engine mutex is removed; attachment I/O does not hold it. A write has a one-second deadline. An ambiguous failure remains Unknown internally (reported as InFlight), preventing blind retries. Successful byte acceptance still does not mean a harness transcript contains the prompt; authenticated observation remains separate.

Readiness is supplied by the authenticated destination adapter. This proves the protocol's handling of a readiness assertion, not automatic detection of a Claude or Codex editing state. A real adapter must establish that state and observe recipient ingestion. No live prompt-submit hook is installed by this change.

## Evidence

The implementation worker reported six focused relay/ingress tests passing. Root inspected the actual Unix daemon concurrency case: it admits a 2 MiB prompt, stalls the destination socket reader, then admits another prompt through a separate configured ingress in under 500 ms while the one-second delivery is pending. A subsequent dispatch makes no second outbound connection. Other fixtures exercise busy/dirty transitions, exact-key dedupe and authenticated receipt handling.

Root ran separate default-check evaluation and build:

- Evaluation session16718, exit0: `/nix/store/mbjlaayqharkzrjwa57a5ln0dnz7hf6k-message-test-0.12.0.drv`.
- Remote-only build session53368, exit0, `--max-jobs 0`: `/nix/store/c1qk3r4gbhx5ya69shy63z3g612nv1mz-message-test-0.12.0`.

The worker's earlier full `nix flake check` lacked a retained execution result and was still running after ten minutes. Root verified its exact command and terminated that owned process. It is not counted as a pass. The retained default check above is the completed validation, not a claim that every flake check passed.

## Remaining gates

The council accepted session-plus-prompt ID with missing fields rejected. The installed Claude version and replay limitation are in `hookOrdering.md`; retry/resume identity stability remains unproved. The hook-to-daemon adapter and actual recipient transcript observation are still outstanding. The living's sandbox go-live is still required for the live human proof. No production activation or provider call occurred.

## Sources

- [Engine and asynchronous dispatch](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/engine.rs)
- [Actual Unix ingress and stalled-write test](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/tests/prompt_relay_ingress.rs:479)
- [Relay state transitions](/home/li/wt/github.com/LiGoldragon/message/integrated-messenger-poc-34d94e/src/relay.rs)
- [Hook identity evidence](/home/li/primary/flows/34d94e/reports/hookOrdering.md)
- [Earlier integrated boundary](/home/li/primary/flows/34d94e/reports/integratedMessengerPoc.md)
