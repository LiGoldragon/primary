# messenger-clj 0.2.6 one-shot probe

Performed by Field Sol `9ac67c` at 2026-09-27T09:08:11Z under the explicitly authorized one-shot `--stdin` probe.

## Candidate and preflight

- Candidate command path: `/nix/store/37jlvv66px2407h4pshgg808n0100rlh-messenger-clj-0.2.6/bin/hm-send`, resolving to `messenger-clj` in the same closure.
- Candidate derivation: `/nix/store/d1vh77n2ibc9k3dmap6drjck588rpgv0-messenger-clj-0.2.6.drv`.
- Its help documents `send TARGET --stdin`; no `--version` assumption was made.
- With the per-command candidate path prefix, `command -v hm-send` returned the candidate path.
- Before the attempt, `FLOW_ID=9ac67c hm-list` showed `9ac67c field-sol-9ac67c default working` and `c56100 mind_sol_c56100 recovery-56ae53 idle`.
- The recipient marker is `/home/li/primary/flows/.c56100.flow-id`, correlating `c56100` with native Codex identity `01a0e0a170757cc2928d13fc56100504`; the live process command resumes UUID `01a0e0a1-7075-7cc2-928d-13fc56100504`.

## One invocation

The sole invocation used subprocess argv
`[candidate-hm-send, "c56100", "--stdin"]` and input bytes exactly
`HM026_PROBE_20260927_9AC67C_BODY`, with no newline. It exited `1` before submission:

```text
messenger-clj: Set FLOW_ID to your own flow ID before sending
```

`FLOW_ID=9ac67c` was accidentally absent from the subprocess environment. Therefore this is a rejected local precondition, not a submitted, transported, presented, or read message. No retry was made.

## Postcondition witness

- The default executable remained `/home/li/.local/bin/hm-send`, resolving to the old 0.2.5 closure `/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5/bin/messenger-clj`.
- The message daemon remained PID `13885` using `/home/li/.local/state/message/message-daemon.signal`; the message nexus remained PID `90762`.
- The message state directory and signal file remained present. No Home activation occurred.
- Recipient body observation is unknown because no submission occurred. The attempted body and literal `--stdin` cannot be recipient-delivered on the observed local precondition failure.

Rollback was inherent: the candidate `PATH` prefix was scoped to the one command and had ended before postcondition verification.
