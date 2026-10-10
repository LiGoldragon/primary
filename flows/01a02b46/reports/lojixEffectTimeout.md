# Ouranos Lojix effect timeout provenance

## Result

The currently running Ouranos `lojix-daemon.service` is Lojix 0.17.5 and is active. Its generated `ExecStartPre` writes `/run/lojix/startup.rkyv` from a typed request containing `ouranos 2700 NoTestDefaults`; the daemon then starts with that archive. The active service's value is therefore 2700 seconds per external effect. The live service and archive are evidence of what is running, not evidence that the living psyche approved that value.

## What was read

The live service was read with `systemctl show` and `systemctl cat`; the archive metadata and daemon executable/process were read with `stat`, `readlink`, and `ps`. The ordinary Lojix socket was queried with `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'`; it returned the current Ouranos records and marker, proving the local daemon answered. No owner request, deployment request, write, or activation was sent.

The authored path was read in the current CriomOS module and PersonaDevelopment projection. The module option is required and positive, while the PersonaDevelopment projection supplies the only current production `2700` assignment. The module interpolates the option into the writer's typed `ConfigurationWriteRequest`, and the daemon receives the generated rkyv archive. The Lojix source defines the archived field, writer, and runtime projection into bounded effect execution. The CriomOS flake pins Lojix commit `0d968da44bc0be8ed875b8546bebf52c3de53a81`.

Evaluation checks were read as generated-evidence consumers: the daemon round-trip and ownership fixtures also set/assert `2700`, but they do not supply the running production value. Commit history was read with `jj` in the Lojix and CriomOS repositories. The bounded-effect implementation entered Lojix in `250c1e380ccff940e0408b3cb5857b026b6a61d8`; a historical CriomOS module default appears in `1e9fc4fce140d415a964f7cb1683e47f54823e04`, while the current explicit PersonaDevelopment projection is carried by `3de85f81464b3c4c04a4954f3643dc45111ab3c5` and current descendants.

The psyche corpus was read at `psyche-raw/Vision/lojixOwnership.md`, `psyche-raw/Vision/setupIndependentInterfaces.md`, relevant `flows/*/vision` records, and the canonical current transcript. Those records contain rulings about Lojix ownership and typed CLI boundaries, but no exact living-psyche approval for a 2700-second timeout. The exact newer psyche entries are preserved separately in `flows/01a02b46/vision/zeusUpdate.md` with source-event timestamps `2026-08-23T08:41:15.810Z` and `2026-08-23T08:42:03.241Z`.

## What was written

Before any source/runtime action, the exact current correction and ruling were appended verbatim to `flows/01a02b46/vision/zeusUpdate.md`:

> what timeout? I never approved any timeout

> get rid of that timeout and resume your goal

Those records were committed and pushed on primary `main` as `b75ad15ef355` (`flows: record timeout correction and ruling`). This trace then wrote only the witness and this report. No source, runtime configuration, daemon, startup archive, host, deployment, or timeout was changed.

## Possible causes and unknowns

The value can be explained by at least two authored paths over time: the historical CriomOS module default of `2700`, and the current explicit PersonaDevelopment projection of `2700`. The live service may also be an older activation of a source revision; its active package and archive timestamps prove runtime state, not which source commit most recently produced the system. The exact activation derivation that produced the current `/nix/store` unit is not reconstructed here.

The current service proves that `2700` is running, and code proves how it flows into the archive and runtime executor. It does not prove who first chose the number, whether a prior agent introduced it, whether a generated projection was activated from a different source revision, or whether any exact living-psyche approval exists. No exact approval was found in the psyche sources read. The newer ruling authorizes getting rid of the timeout and resuming the goal, but this subflow performed no implementation or deployment action.

## Sources

- [Ouranos Lojix service witness](../witnesses/lojixEffectTimeout.md)
- [current psyche correction and ruling](../vision/zeusUpdate.md)
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix:23-27,88-101`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix-persona-development.nix:41-55`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:94-97`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock:2050-2072`
- `/git/github.com/LiGoldragon/CriomOS/checks/lojix-daemon-config-roundtrip/default.nix:30-84`
- `/git/github.com/LiGoldragon/CriomOS/checks/lojix-ownership/default.nix:108-127,206-238`
- `/git/github.com/LiGoldragon/lojix/src/lib.rs:258-278,938-946`
- `/git/github.com/LiGoldragon/lojix/src/bin/lojix-write-configuration.rs:25-37,111-146`
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:938-946,972-985`
- `flows/01a02bb6/reports/copyClosureDiagnosis.md`
- `flows/01a02bb6/witnesses/transportAndLink.md`
- `flows/3cb84d07/witnesses/lojixController.md`
- `250c1e380ccff940e0408b3cb5857b026b6a61d8` (Lojix)
- `1e9fc4fce140d415a964f7cb1683e47f54823e04`, `3de85f81464b3c4c04a4954f3643dc45111ab3c5`, and `0683d00e72abe139ba72286e7db247e02825c972` (CriomOS)
