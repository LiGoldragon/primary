# Ouranos deployment 33–34 terminal receipt

- Immutable CriomOS request: `e6a83edc7e71254cae5a9d233c01fefc3f7f9b57`.
- The proposal was rooted through `/var/lib/lojix-proposals/horizon-definition-gcroot`; its canonical regular source was `/nix/store/p61bn3w1qgl3lhx5gm96crw1f1qlr0gg-horizon-definition/horizon-definition.datom`. The symlink source form was rejected before deployment creation; canonical-source Evaluate was accepted.
- Deployment 33 Evaluate: `Completed` / `Succeeded`, marker `{ 800 800 }`.
- Deployment 34 Realize: `Failed` / `BuildFailed`, marker `{ 820 820 }`.
- Derived requested target: `/nix/store/353n58zkn4h4isbdwl1m5j3x5kzyg8kc-nixos-system-ouranos-26.11.20260813.0e251e2.drv`.
- Builder: Prometheus via `ssh-ng://nix-ssh@prometheus.goldragon.criome`; no local fallback.
- Exact root cause: fixed-output `/nix/store/z3jvnm2s8p61rrjiqsv73nh3rwzmz8js-field-clj-deps.drv` hash mismatch. Specified `sha256-HNlkGVUe61CxFetUQ/bJwGuhAPAaTEgvk1FCgdpZ1MU=`; got `sha256-vsJ2Q7yDWpDQvAl1GlcIjRqKm0XxB4xv26H72BV9CtM=`.
- This was not a disk-space failure. No TestActivation, ActivateNow, cleanup, garbage collection, root removal, or retry was performed.
- b860be and e167d8 were sent the terminal report with `hm-send`; transport was accepted as `working`, but presentation was not witnessed.
