# Flow restart

## A harness that locks itself out of relaunching its own flow is a design defect; how flows are restarted must be decided; it is a command sent to Flow, and if the flow ID matches the flow's provenance, that is all the authority needed

Context: typed to primary Psyche opus (this flow, 9993b5) on 2026-09-17 in the mid-turn message that also carries the caller-identity vision (callerIdentity.md, same date); the same message asked this flow to confirm it had remembered and situated itself. Speculation on the harness lockout is the living's own reading of what may have happened when Fable f55ec8 and its Opus 5 recovery subflow both had classifier refusals for `claude --bg` launches and `--resume`. Logged by the main flow before acting.

> I don't know. Maybe something happened where the harness thought that only the core layer had authority to restart flows or something, but it locked itself out of relaunching its own flow. We need to decide on how flows are restarted. It just needs to be a command sent to Flow, and if the flow ID matches the flow's provenance, then we can restart it. That's all the authority you need.

-- psyche, typed.
