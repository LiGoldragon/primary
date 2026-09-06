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
