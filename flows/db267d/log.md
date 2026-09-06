# Flow db267d

Realization. Fix Claude for bird on Zeus, fast, and deploy.

## Instructions from the psyche

- Remember flow 0384e0.
- Subagent model override for this flow: trivial work uses Sonnet 5 at
  medium effort; non-trivial work uses Opus 5 at medium effort.
- Diagnose and fix the Claude bug on the host Zeus. SSH as root; reach
  bird through root. Leave no root session hanging — last time a
  lingering root login blocked a reboot.
- Speed is the constraint: minutes, not hours.
- Redeployment risk is accepted; the target is already broken.
- Take the cloud remote server out of CriomOS. Reintroducing it is a
  later conversation.

## Log

- Claimed lane db267d. Dispatched two subflows: remember 0384e0 at
  depth one, and a read-only diagnosis of Claude for bird on Zeus.
