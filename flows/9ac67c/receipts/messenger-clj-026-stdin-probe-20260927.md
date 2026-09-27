# Corrected messenger-clj 0.2.6 stdin probe

One authorized probe, executed by Field Sol 9ac67c on 2026-09-27. The prior
local pre-submission failure cited by the authorizing instruction is preserved
and was not retried; this is the sole corrected invocation.

## Preflight

- Candidate executable: `/nix/store/37jlvv66px2407h4pshgg808n0100rlh-messenger-clj-0.2.6/bin/hm-send`.
- The invocation's child environment explicitly set `FLOW_ID=9ac67c` and put
  that candidate `bin` directory first in `PATH`. Prepared command evidence
  printed exactly that Flow ID and executable path before the send.
- Fresh Messenger route readback named `c56100` as
  `mind_sol_c56100`, session `recovery-56ae53`, state `idle`.
- Fresh Flow readback resolved c56100's native UUID as
  `01a0e0a1-7075-7cc2-928d-13fc56100504`, with the same
  `recovery-56ae53` Messenger route at `w1:p3` and terminal
  `term_65c6d6c5c3aac3`.

## One invocation

The exact stdin bytes were the 35-byte, newline-free UTF-8 body:

```
HM026_PROBE_20260927_9AC67C_R1_BODY
```

The actual argv was candidate `hm-send`, `c56100`, `--stdin`. It used no
`--wait-presented` flag.

| Observation | Result |
| --- | --- |
| Exit | `0` |
| stdout | `Transported.{ c56100 idle }` |
| stderr | empty |
| Retry | none |

## Grades

- Submitted: no separate Submitted terminal grade was emitted.
- Transported: witnessed by the exact stdout above.
- Presented: not requested and not observed.
- Read: not observed. One passive `herdr pane read --session recovery-56ae53
  w1:p3` inspected the visible pane tail and found neither the marker nor the
  literal string `--stdin`. It therefore supplies no body/read witness.

## Post-observation

- The invoking shell's ordinary `hm-send` resolution again pointed to the
  effective installed 0.2.5 executable:
  `/nix/store/p8mz1msm8lxiahnw6sfipi8m258x1q3z-messenger-clj-0.2.5/bin/messenger-clj`.
  The candidate PATH selection was child-only.
- Stable Message remained active with PID `13885`, executing
  `/nix/store/i66j8l0vk6i3bhd0r968dbm7ckllnryf-message-0.14.0/bin/message-daemon`
  against `/home/li/.local/state/message/message-daemon.signal`. The next
  Message nexus remained PID `90762` at its existing 0.17.0 store path.
- This work issued no Home command, source change, profile switch, service
  action, registry import, build, evaluation, or activation. It therefore
  made no Home change; no independent Home before/after state comparison was
  needed to establish the bounded command's scope.
