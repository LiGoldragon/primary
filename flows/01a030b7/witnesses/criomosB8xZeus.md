# CriomOS-b8x Zeus deployment and live-state witness

Method: implementation subflow typed-Lojix plus read-only strict-SSH probe via
`root@zeus.goldragon.criome`, after terminal records, returned 2026-08-24.

The exact consumer is `ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`. The typed
CompleteHost request used proposal `/git/github.com/LiGoldragon/goldragon/datom.dotos`,
Ethernet store URI `ssh-ng://root@192.168.18.95`, and Yggdrasil activation
destination `root@zeus.goldragon.criome`. Deployment 56 was immediately
`FlakeReferenceMalformed`, no target action. Correct TestActivation 57 was
accepted `(1294 1294)` then `Succeeded` `(1327 1327)`. Only afterward did
ActivateNow 58 accept `(1332 1332)` and succeed `(1365 1365)`; it is Current.

Persistent profile equals `/run/current-system` at final closure;
`/run/booted-system` is preceding closure, so no reboot. Loader default is
new `nixos-d98b084…`; system is running and failed units empty. Embedded
Home services li/bird are active/exited at distinct generation paths
`4jc98xzh…` and `njps7ivy…`; both resolve Codex 0.149.1 and Claude 2.1.241.
Standalone profile roots remain distinct historical links but resolve the same
Codex 0.149.1 executable, so no stale-version mismatch is witnessed.
