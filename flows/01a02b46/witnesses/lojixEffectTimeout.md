# Ouranos Lojix effect timeout

Method: probe `hostname`; `systemctl show lojix-daemon.service -p ActiveState -p SubState -p ExecStart -p FragmentPath -p DropInPaths`; `systemctl cat lojix-daemon.service`; `stat -c '%n %s bytes %y' /run/lojix/startup.rkyv`; `readlink -f /proc/$(pgrep -xo lojix-daemon)/exe`; and `ps -eo pid,lstart,args | rg '[l]ojix-daemon'`.

Observed on the current Ouranos host:

- `hostname` is `ouranos`; the daemon service is `active (running)`.
- The generated unit is `/etc/systemd/system/lojix-daemon.service`, linked to `/nix/store/24m83nxzappj66d053qxgvp2fksr1ybd-unit-lojix-daemon.service/lojix-daemon.service`.
- Its `ExecStartPre` is the Lojix 0.17.5 writer with the exact typed request `ConfigurationWriteRequest.{/run/lojix/ordinary.sock 432 /run/lojix/owner.sock 384 /var/lib/lojix /var/lib/lojix/lojix.sema ouranos 2700 NoTestDefaults /run/lojix/startup.rkyv}`.
- Its daemon command is `/nix/store/kcg9m2zi17phw11w4vkjz1ffa41l450n-lojix-0.17.5/bin/lojix-daemon /run/lojix/startup.rkyv`; the running daemon executable resolves to that same Lojix 0.17.5 store path.
- `/run/lojix/startup.rkyv` exists, is 190 bytes, and was written at `2026-08-19 20:29:16.328028857 +0200`; the daemon process started at `2026-08-19 20:29:15`.

Method: code read `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix:23-27,88-101`, `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix-persona-development.nix:41-55`, `/git/github.com/LiGoldragon/CriomOS/flake.nix:94-97`, and `/git/github.com/LiGoldragon/CriomOS/flake.lock:2050-2072`.

The authored Nix module declares `services.lojix.effectTimeoutSeconds` as a required positive option at `lojix.nix:98-101`; it has no current module default. The PersonaDevelopment projection supplies `effectTimeoutSeconds = 2700` at `lojix-persona-development.nix:54`. The module interpolates that value into the typed startup request at `lojix.nix:26` and passes the generated archive path to the daemon at `lojix.nix:27`. CriomOS pins Lojix to `0d968da44bc0be8ed875b8546bebf52c3de53a81` in both `flake.nix:96` and `flake.lock:2064,2070`.

Method: code read `/git/github.com/LiGoldragon/lojix/src/lib.rs:258-278,938-946`, `/git/github.com/LiGoldragon/lojix/src/bin/lojix-write-configuration.rs:25-37,111-146`, and `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:938-946,972-985`.

The Lojix binary startup archive owns a typed `effect_timeout_seconds: u64`. The writer decodes the positional timeout and writes it to the rkyv archive; zero is rejected. Runtime construction projects the archived value into `EffectExecution::production`, which bounds external Nix, SSH, and activation effects. The running archive is therefore supplied by the active service's `2700` writer field, not by a runtime query or a client flag.

Method: code read `/git/github.com/LiGoldragon/CriomOS/checks/lojix-daemon-config-roundtrip/default.nix:30-84`, `/git/github.com/LiGoldragon/CriomOS/checks/lojix-ownership/default.nix:108-127,206-238`, and `/git/github.com/LiGoldragon/lojix/README.md:58-70`.

The round-trip check's fixture explicitly sets `2700` and asserts the projected value and startup request. The ownership check's explicit fixture does the same and checks the generated writer command. These are generated/evaluation test evidence, not additional production supplies. The Lojix README describes the startup request's timeout field but does not record living-psyche approval of its numeric value.

Method: code read `/git/github.com/LiGoldragon/lojix` commit `250c1e380ccff940e0408b3cb5857b026b6a61d8`, `/git/github.com/LiGoldragon/CriomOS` commits `1e9fc4fce140d415a964f7cb1683e47f54823e04`, `3de85f81464b3c4c04a4954f3643dc45111ab3c5`, `0683d00e72abe139ba72286e7db247e02825c972`, and current `93049a6e3eb7f66a23484402c96d835caa233b99` with `jj show`, `jj diff`, `jj file annotate`, and `jj file show`.

Provenance observations:

- Lojix commit `250c1e380ccff940e0408b3cb5857b026b6a61d8` (2026-07-29) introduced bounded external-effect execution and the typed startup timeout field; its focused tests use short `60`-second values.
- CriomOS commit `1e9fc4fce140d415a964f7cb1683e47f54823e04` (2026-08-10) contains an earlier `services.lojix.effectTimeoutSeconds` module default of `2700` in its historical snapshot. The current module no longer has that default; the current PersonaDevelopment projection explicitly supplies `2700`.
- CriomOS commit `3de85f81464b3c4c04a4954f3643dc45111ab3c5` (2026-08-10) introduced the current Horizon-derived PersonaDevelopment shape, including the explicit `effectTimeoutSeconds = 2700` projection visible in the current source.
- CriomOS commit `0683d00e72abe139ba72286e7db247e02825c972` (2026-07-29) carries the round-trip check that asserts `2700`; it is test evidence, not a living approval.

No source, generated source, daemon, startup archive, host, deployment, or timeout was changed by this trace. Orchestrate lane registration and path claim were attempted with the current brace syntax, but the local orchestrate socket returned `transport IO error: No such file or directory`; this witness was written after that coordination failure was recorded.
