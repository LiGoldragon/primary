# Zeus Nix configuration

Method: probe `sed -n '1,160p' /etc/nix/machines`; `nix config show`; and code
read `/git/github.com/LiGoldragon/goldragon/datom.dotos`.

Observed:

- `/etc/nix/machines` contains the exact remote builder entry
  `ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux ...`; the request
  field used by successful durable deployments is `Some.@/etc/nix/machines`.
- Nix reports `system = x86_64-linux`, `builders = @/etc/nix/machines`,
  `builders-use-substitutes = true`, `max-jobs = 1`, and `fallback = true`.
- Global Nix substituters are `http://nix.prometheus.goldragon.criome` and
  `https://cache.nixos.org/`. The Lojix request's extra-substituter vector is
  independent of these global settings; successful durable deployment 27 used
  `[]`.
- The production proposal declares Zeus with `Some.X86_64` metal and the
  `NixBuilder None` node service. Prometheus is the declared `NixBuilder`/cache
  node (`NixBuilder Some.6`, `NixCache`) and is the configured builder.

Inference: the exact request builder is `Some.@/etc/nix/machines`, whose active
remote machine is Prometheus. The exact request extra-substituter vector is
`[]`; do not duplicate the global substituters in that vector.

## Sources

- `/etc/nix/machines` — direct builder witness
- `nix config show` — direct local Nix configuration witness
- `/git/github.com/LiGoldragon/goldragon/datom.dotos` — direct proposal read
- `flows/01a02b46/witnesses/zeusUpdateShape.md` — prior source/shape context
- `flows/7a9f4c12/reports/zeusDualRoutePreflight.md` — prior Zeus preflight
- `flows/01a02b6a` — this flow
