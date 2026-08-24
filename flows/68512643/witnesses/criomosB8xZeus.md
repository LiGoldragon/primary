# CriomOS-b8x Zeus deployment and live-state evidence

Method: implementation-subflow typed-Lojix queries and read-only strict-SSH
probe via `root@zeus.goldragon.criome`, after terminal deployment records,
returned to this flow on 2026-08-24.

The deployed immutable source is CriomOS
`ab005ef8bc8828e1f92563cbb4bb966c2adda5bc`. Its CompleteHost request used
proposal `/git/github.com/LiGoldragon/goldragon/datom.dotos`, Ethernet Nix
store URI `ssh-ng://root@192.168.18.95`, and Yggdrasil activation destination
`root@zeus.goldragon.criome`:

```text
Deploy.Host.(goldragon zeus CompleteHost <proposal> github:LiGoldragon/CriomOS?rev=ab005ef8bc8828e1f92563cbb4bb966c2adda5bc (ssh-ng://root@192.168.18.95 root@zeus.goldragon.criome) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 TestActivation RequireImmutable Some.@/etc/nix/machines [])
```

Deployment 56 was rejected immediately as `FlakeReferenceMalformed`, with no
target action. Correct TestActivation 57 was accepted `(1294 1294)` and
terminal `Succeeded` `(1327 1327)`. Only then was ActivateNow submitted:
deployment 58 accepted `(1332 1332)`, terminal `Succeeded` `(1365 1365)`, and
its source is Current.

Afterward, the persistent profile equals `/run/current-system` at the final
closure. `/run/booted-system` remains the preceding closure because no reboot
occurred; `loader.conf` defaults to new `nixos-d98b084…`. System state is
`running` and failed units are empty. `home-manager-li` and
`home-manager-bird` are `active`/`exited`; embedded generations are
`/nix/store/4jc98xzh500ckvd523l3dial4ik5ansm-home-manager-generation` and
`/nix/store/njps7ivyq9g573gjhdmh9dmx4kn4z8j7-home-manager-generation`.
Both resolve Codex 0.149.1 and Claude Code 2.1.241.

Standalone roots are distinct historical links: li points to
`/nix/store/xiy7dqy22hqay06qhr62hnbb9sy1g95j-profile`, bird to
`/nix/store/kpmb8rp0xsl0wnn286z2nriigx8879sj-profile`. They are not embedded
generation paths, but both resolve the same Codex 0.149.1 executable; no
stale-version mismatch is witnessed.
