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
- Remembered: 0384e0 — depth 1. That flow deployed CriomOS 57ec0138
  to zeus (cluster goldragon, route zeus.goldragon.criome), Lojix
  generation 207, live NixOS generation 72, no reboot. li's user
  environment landed cleanly (Lojix generation 210). bird's did not:
  the Lojix daemon runs as li on ouranos and li's agent key is absent
  from bird's authorized_keys on Zeus, so deployments 212 SetProfile
  and 213 ActivateNow both recorded
  `Some.Failed.(Activate ActivationFailed)`. On the psyche's word
  "do a hot bypass for now to get it done", bird's generation was
  activated by hand over root -> su bird, and her profile link set
  manually to home-manager-32-link. bird's environment on Zeus is
  therefore undeclared state that the next ordinary deployment
  overwrites, and Lojix still records her Current generation as 167.
  The Claude Desktop breakage the psyche reported there —
  `[CCD] LOCAL OVERRIDE: declared binary unavailable at
  /nix/store/i9inl75s81bnmaczw8d89875z4g4i4n9-claude-code-2.1.261/bin/claude`
  — was never investigated; the psyche said "Actually, don't do
  anything" and the flow stopped. Also standing from that flow, its
  own words: "Whenever I say deploy, I always want [the user's
  environment] up to date and refreshed."
- The "cloud remote server" the psyche wants gone is, on a subflow's
  unverified reading, the `claude-remote-control` systemd user
  service in CriomOS-home, restarting every 2s. Dispatched a subflow
  to verify that referent and remove it from CriomOS and CriomOS-home.
