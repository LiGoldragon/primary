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
