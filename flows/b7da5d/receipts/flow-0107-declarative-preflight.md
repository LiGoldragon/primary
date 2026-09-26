# Flow 0.10.7 declarative preflight

- Canonical Flow `main` fetched as `8df890ba1bc34a9bd575e75ab4796b4e0dc7b0fd`; package and Nexus both answered `0.10.7` after a local build with remote builders disabled and only the public cache substituter.
- Focused CriomOS-home Flow module check passed through direct Nix evaluation with local building enabled and remote builders disabled.
- CriomOS-home `main` was advanced to `5d647e967968579887d7dd6d74a0690b64a2d316`, pinning Flow `8df890ba1bc34a9bd575e75ab4796b4e0dc7b0fd` and restoring the managed user package/unit. CriomOS `main` was advanced to `f09f3c8367b93f778cd9ce1483b83dd2d9486832`, pinning that Home revision. Both pushes were fetched back from their remotes.
- Managed activation was not attempted. The pushed CriomOS consumer evaluated with the supplied Lojix materialized inputs fails in `modules/nixos/metal/default.nix:21`: `attribute 'hardware' missing` at `horizon.node.machine.hardware`. The used Horizon materialization records June 19, whereas current CriomOS requires that field.
- Existing 0.10.5 profile, user unit, and reversible override were intentionally preserved. No production message was sent.
