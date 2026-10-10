# Ouranos Flow 0.10.7 Evaluate-only materialization

## Status

Offline packet complete. No Lojix socket was contacted, no deploy was submitted, and no host, profile, pin, or activation state was changed.

The request in `lojix-evaluate.request` is the exact disconnected `CompleteHost` + `Horizon` + `Evaluate` request that decoded, actualized the proposal, encoded to the portable Signal wire, and restored byte-for-byte under Lojix `a67f5773979fb2e90727486d24dd300980f914c7`.

## Producer and proposal

- Authoritative Goldragon remote `main`: `8c4d03de76907f590072c0998b00037330ebcd82`, independently read back through GitHub.
- Producer output: `/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom`.
- File admission properties: absolute, basename `horizon-definition.datom`, regular file, non-symlink, mode `0444`, 6079 bytes.
- SHA-256: `d280c719030bd066e23d1f003e804d73d699756dae18776114551cac201040e8`.
- The output was freshly requested from Goldragon `.#horizon-definition` with `--max-jobs 0`, `--option builders @/etc/nix/machines`, and `--option fallback false`. The output already existed and resolved to the store path above.
- Goldragon pins Horizon `ee8d6f8d27eb6e200504807971ffdd26aaca7ed1`; the compatible Lojix producer revision `a67f5773979fb2e90727486d24dd300980f914c7` pins the same Horizon revision and the matching meta wire `b500561f0ce813917366997581412b7a79aebc99`.

The retired `proposal.datom`, stale full-os/base-host/os-only trees, and `flows/eb7bae/materialization-20260924/lojix-preflight.request` were not used.

## Decode, projection, and wire evidence

- Horizon `ee8d6f8d` CLI decoded the exact proposal and projected `goldragon/ouranos` successfully.
- Full projection SHA-256: `10333ac7bad0ab3d0d5e820826ca0f888846c88e8394adc81983481b38bdcaec`.
- The projected value contains `node.machine.hardware`: 12 cores, ThinkPadT14Gen5Intel, chip generation 12, 32 GiB RAM.
- It preserves `openCodeTesting`, proving this is not the rejected Direct-mode capability loss.
- It projects `x86_64-linux`, `ouranos.goldragon.criome`, and the Prometheus builder view. The bounded projection fields are recorded in `ouranos-projection-witness.json`.
- The exact request was passed to the immutable Lojix `a67f5773` `lojix-meta` client with a deliberately nonexistent socket. It reached socket connect and failed only with `io error: No such file or directory`, proving text decode and proposal actualization completed without a request leaving the process.
- A disconnected integration witness then cloned the actualized query, Signal-encoded it, restored it as `meta_signal_lojix::Query`, and asserted equality. Result: `1 passed; 0 failed`.

## Request fields

| Field | Exact value | Evidence |
|---|---|---|
| Cluster / node | `goldragon` / `ouranos` | current Goldragon projection |
| Composition / mode / action | `CompleteHost` / `Horizon` / `Evaluate` | requested selector and Lojix 7 contract |
| Proposal | store path above, SHA-256 above | fresh producer output and file admission check |
| Secrets | `NoSecrets` | public Horizon evaluation; no secret authority supplied |
| Immutable target | `github:LiGoldragon/CriomOS?rev=f09f3c8367b93f778cd9ce1483b83dd2d9486832` | CriomOS remote `main`, GitHub readback |
| Transport | `ssh-ng://root@ouranos.goldragon.criome` / `root@ouranos.goldragon.criome` | current SSH configuration resolves root, hostname, port 22; same explicit CompleteHost pair previously succeeded |
| Output selector | `nixosConfigurations.target.config.system.build.toplevel` | current CriomOS complete-host selector and prior succeeded request family |
| Backend | `NixosSystemdBootV1` | Host contract; inert for `Evaluate` |
| Source policy | `RequireImmutable` | full 40-hex CriomOS revision |
| Builder | `Some.@/etc/nix/machines` | regular mode-0444 file naming `ssh-ng://nix-ssh@prometheus.goldragon.criome`; fresh producer build used it |
| Extra substituters | `[]` | no additional request-owned substituter supplied |

## Consumer chain and gate

- Flow `8df890ba1bc34a9bd575e75ab4796b4e0dc7b0fd` exists remotely and is version 0.10.7.
- Home `5d647e967968579887d7dd6d74a0690b64a2d316` pins that exact Flow revision. Current Home `main` is one descendant commit ahead; it was not substituted into this chain.
- CriomOS `f09f3c8367b93f778cd9ce1483b83dd2d9486832` is remote `main`, pins Home `5d647e96`, and transitively carries Flow `8df890ba`.
- That CriomOS revision still pins Lojix `c4bba4fa12408c39ff745b0773468cd32a74403f`, whose Horizon/meta producer pair is the older incompatible `40d04d25` / `35deec4e`. The corrected request producer is Lojix `a67f5773`. Therefore the packet must be consumed by the corrected `a67f5773` client/Nexus; `f09f3c83` is the immutable evaluation target, not evidence that its embedded Lojix is compatible with the proposal.
- Any later activation of `f09f3c83` would restore its embedded old Lojix pin. Consumer owner b7da5d must resolve that pin coherence before activation. This packet authorizes neither that edit nor activation.

## Expected evaluation result

If the request is actually submitted to the compatible Lojix consumer, `Evaluate` should materialize the four CompleteHost inputs and return a canonical `/nix/store/...drv` derivation path for `nixosConfigurations.target.config.system.build.toplevel`, then finish without building, copying, changing a profile, or activating. The exact derivation path is unresolved because no Lojix evaluation was submitted. No realized closure is expected from `Evaluate`; Lojix source explicitly marks `Evaluate` as the only Host action that does not produce a closure.
