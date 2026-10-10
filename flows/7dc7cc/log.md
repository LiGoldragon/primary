# Flow 7dc7cc — localhost operating system redeployment

Parent session: 7dc7cc87-d125-4266-b767-6f424f4b8493

## Working instructions from the psyche

- Remember the preceding Zeus deployment flow (db267d) and the half-merged
  work cleaned up there.
- Full operating-system redeployment locally, for the localhost node.
- Home pinned to the latest stable version — without the unfinished
  half-done work from last night.
- Restart or reload the shell so the Wispr Flow widgets appear.
- Before deploying: catch up on available Claude Code code updates, and
  make sure the corresponding ChatGPT and Claude desktop apps are patched.
- "We need to talk about some skills."
- "Don't get lost chasing a rabbit down a deep hole. If you find yourself
  chasing a deep rabbit hole, then maybe just pause."

## Log

Remembered: db267d — depth 1.

- The "542442 renovation" is a three-repository schema change (horizon-rs
  producer, CriomOS, CriomOS-home). Its CriomOS-home half had landed on
  main alone, reading a schema the deployed producer does not emit.
- db267d branched that work off and rolled main back. The known-good line:
  CriomOS main = bc3c4917b5df7b4842bd12996ff46926476cdcd8, which pins
  CriomOS-home at ed958211e8bfaa4384aca6622d92bc9bdb429fa1.
- Preserved: home-datom-renovation-from-main-542442 (654144d71a51) and
  main-before-rollback-db267d (fde8a2d2).
- db267d deployed user environments only, on cluster goldragon node zeus,
  for bird and li. It performed no host deployment and no reboot; Zeus
  stayed on CriomOS 57ec0138, NixOS system generation 72.
- This is the mechanism the psyche's symptom points at: a user environment
  deployed without a following host deployment does not survive a reboot,
  because the system profile still carries the older pinned home.

App update picture (subflow, witnessed on this host):

- Claude Code: installed 2.1.258; declared in CriomOS-home 2.1.261; latest
  released 2.1.263. Packaged in CriomOS-home owned-agents/claude-code from a
  direct fetch, no flake input; a bump is the version and three hashes in
  hashes.json. No patches.
- Claude Desktop: installed 1.40609.1; declared 1.46388.2, which is current
  with upstream. The declared version carries db267d's two repairs — the
  asar unpack glob for pty.node, and the rewritten local-binary override.
  This host still runs the generation with both bugs.
- ChatGPT: installed equals declared, 26.901.31953. One fail-closed patch.
  Upstream's latest could not be reached, so currency is unverified.

So this host is behind its own declared source on two of the three apps.
Catching Claude Code up means bumping it to 2.1.263 on the rolled-back line.

This machine, witnessed:

- Identity: cluster goldragon, node ouranos, user li. Not zeus — db267d
  never touched this node, which is why last night's repairs are not here.
- Sockets /run/lojix/ordinary.sock and /run/lojix/owner.sock; daemon
  lojix-0.20.3 running since boot and answering.
- Lojix believes CompleteHost Current is generation 138 from CriomOS
  7cd12262 ("Advance modifier-safe Wispr helper"), and UserEnvironment
  Current is generation 204 from a66c9381, a revision not in the local
  CriomOS-home clone. No pins.
- The live system profile is generation 179, whose store path is not the
  one Lojix records for 138. Something advanced the system outside Lojix.
  The live home profile does match Lojix's 204.
- Both sources are clean and sit exactly on the rolled-back line:
  CriomOS bc3c4917, CriomOS-home ed958211, local equal to origin.
- The Wispr Flow application is in the deployed generation and a 1.6.7
  process survives from an older store path, but the noctalia bar widget
  is absent from the built config: no wispr-status plugin, enabled plugins
  are only ["criomos/listener-level"]. The declaration is gated on
  behavesAs.edge, and ouranos's horizon publication carries no role or
  capability data. So a redeployment alone may not restore the widget —
  dispatched to establish rather than assume.
- Shell is zsh with a ZDOTDIR chain under ~/.config/zsh; existing shells
  keep the old environment until re-sourced or replaced by a new login.

Claude Code caught up on the rolled-back line (subflow, witnessed):

- 2.1.261 -> 2.1.263 via the repository's own owned-agents/claude-code/
  update.py, hashes refreshed for all three declared platforms. The
  package was realized and the built binary reports 2.1.263.
- CriomOS-home main advanced ed958211 -> 2c4975027af1a3fd9d1da3a2c86e4b195c0b0472,
  pushed. No 542442 renovation commit was brought onto main.
- CriomOS main advanced bc3c4917 -> 07d2cf95abb3, pushed, with flake.nix,
  flake.lock and expectedHomeRevision consistently repinned to 2c497502.
- Full NixOS evaluation was not performed there: it needs the horizon and
  system inputs Lojix materializes at deployment time. The deployment is
  the first full evaluation, so a failure there is expected to surface then.

This is the line to deploy: CriomOS 07d2cf95, carrying CriomOS-home 2c497502.

The widget's disappearance, established (subflow, correcting the earlier
inference that behavesAs.edge was false):

- ouranos is declared species EdgeTesting in the goldragon proposal, and
  horizon-rs derives edge = true from that species. The gate passes; the
  widget is not gated off for this node.
- CriomOS 7cd12262 is an ancestor of bc3c4917, so nothing Wispr-related is
  lost by deploying the rolled-back line.
- The real cause: the wispr-status widget entered CriomOS-home on Sep 4
  (6f71a8b, iterated to c40ff0c), after the host generation this machine
  boots was built. The user environment deployed on Sep 5 carried it, but
  system generation 179 embeds a widget-less home-manager generation, and
  its home-manager-li.service re-activates that embedded generation at
  boot — overwriting the standalone profile. The reboot is what took it.
- So a user-environment deployment alone would be undone by the next
  reboot. The host deployment is the durable fix, and no declarative
  change is needed to restore the widget.

This is exactly the mechanism behind the psyche's vision entry, arrived at
independently from the deployed artifacts.

Deployment dispatched: CompleteHost ouranos from CriomOS 07d2cf95 —
realize, set boot profile, activate now — then UserEnvironment li from the
same line. No reboot; the psyche has not approved one.

Deployed (subflow, witnessed; verbatim requests and replies in
witnesses/ouranos-deployment.md):

- CompleteHost ouranos from CriomOS 07d2cf95 — Realize 227, SetBootProfile
  228, ActivateNow 229, each terminal Succeeded, boot profile set before
  activation.
- UserEnvironment li from the same line — Realize 230, SetProfile 231,
  ActivateNow 232, each terminal Succeeded.
- Verified: the wispr-status plugin files and bar placement are in the new
  generation and symlinked into the live home; claude-code 2.1.263;
  claude-desktop 1.46388.2 with pty.node correctly unpacked; Lojix's
  CompleteHost Current 229 and UserEnvironment Current 232 both match the
  live profiles and both record source 07d2cf95. The old divergence
  between Lojix's 138 and live 179 is closed.
- System generation 180's home-manager-li.service points at the same
  generation as the standalone profile, so the next reboot activates the
  right one. That is the durable repair the psyche asked for.
- No reboot, no compositor restart, no forced logout. The running
  noctalia-shell predates the deployment; whether it hot-reloads plugins
  was not established, so a fresh login may be needed for the widget to
  appear. Left for the psyche.

Owed to the psyche: approval for the operating-system skill line that
would carry the vision entry forward to later flows.
