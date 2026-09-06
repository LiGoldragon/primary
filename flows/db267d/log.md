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
- Diagnosis witnessed on Zeus, read-only over one-shot root SSH; no
  root login session left behind (`who` empty). bird's Claude Desktop
  launches and is authenticated. Two independent defects, both in our
  own `owned-agents/claude-desktop/` packaging in CriomOS-home:
  (1) the `asar pack` repack after patching carries no `--unpack`, so
  upstream's unpacked set is discarded and
  `node_modules/node-pty/prebuilds/linux-x64/pty.node` is stored
  inside the archive where it cannot be dlopen'd; the pty-host worker
  exits 1 and every in-app session dies. Broken since at least Sep 1
  and present in the previous build too. (2) `patch-runtime.mjs`
  injects an `initLocalBinary` that references bare minified
  identifiers from the enclosing bundle scope; valid in
  claude-desktop 1.40609.1, broken in 1.46388.2, so its own
  TypeError is caught and re-reported as
  `[CCD] LOCAL OVERRIDE: declared binary unavailable`. Disconfirmed
  the obvious reading: that binary exists, is executable by bird, and
  `fs.access(path, X_OK)` as bird returns OK.
  Refuted: auth, credentials, launcher, GPU, generation/profile
  mismatch, the Criome cloud runtime (absent from Zeus), and
  `claude-remote-control` (ran clean, exited 0). Claude Code in the
  terminal is unaffected and is bird's working path right now.
  Unknown and unlinked: `orchestrate-nexus.service` exits 1 silently
  in bird's session.
- Dispatched a subflow to fix both defects and to strengthen
  `checks/claude-desktop-declared-cli` and the runtime-contract check
  so either defect fails the build instead of the runtime.
- Both defects fixed and pushed to CriomOS-home `ceeaaf4272ea`, with
  both claude-desktop checks green. The repack now derives its
  `--unpack` glob from upstream's own asar header unioned with
  `**/*.node`; the injected `initLocalBinary` obtains `node:fs`
  itself, references no bundle-scope identifier, distinguishes an
  internal failure from a genuinely missing binary, and is executed
  at build time against a present path, an absent path, and a broken
  `require`, so bundle drift now fails the build. A third defect
  surfaced while proving: the runtime-contract check was already red
  on 1.46388.2 — it located the manager binding by assuming
  `,NAME=class{` where 1.46388.2 emits `var POn=class{` — which is
  why defect 2 shipped unnoticed.
- Dispatched a subflow to advance CriomOS's CriomOS-home pin, deploy
  bird's user environment (Realize through Lojix, activation through
  root -> bird if the SSH gap blocks SetProfile/ActivateNow), deploy
  li's user environment per the standing ruling, and verify on Zeus
  that bird's app actually works afterwards.
- The Claude remote-control server is out. Verified referent:
  `modules/home/profiles/min/claude-remote-control.nix` in
  CriomOS-home, a home-manager module gated on `user.size.min`
  declaring a systemd user service with `Restart=always` and
  `RestartSec=2s`. Nothing anywhere set its options and no host or
  user profile enabled it separately — the minimum-profile import in
  `modules/home/default.nix` was the only switch, which is how both
  bird and li got it. Deleted the module, its check, its import, its
  flake wiring, and its documentation; no stub and no disabled
  option. Codex's remote control is a different unit from a different
  package in `agent-intercom.nix` and was left alone; the one coupled
  site was CriomOS `checks/lojix-ownership`, a shared assertion site,
  where the Claude half became a negative assertion.
  CriomOS-home `1ae5da86`, CriomOS `a48f9cb8`, producer before
  consumer.
- Carry into deploy: home-manager drops the unit from the managed set
  but does not stop a running one, so each account that ran the old
  generation needs `systemctl --user disable --now
  claude-remote-control.service` once.
- Pre-existing and unresolved, found while evaluating and not caused
  by this flow: `checks/lojix-ownership` requires CriomOS and
  CriomOS-home to share one Orchestrate lock and they do not — root
  lock `5f016531`, Home lock `ac8a9266`, expectation `9585484`. No
  single value satisfies it, so it cannot be repaired by editing the
  expectation. Left for the psyche to rule on.
