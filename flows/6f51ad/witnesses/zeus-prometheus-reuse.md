# Zeus Prometheus output reuse — 2026-09-28

Current source: CriomOS `1a9f5fdf89af4ec38015824fca2fe36847f2f4db`.

Evaluated system derivation:
`/nix/store/qn67ny8mixnnazdyf3wjjv92lgshgf69-nixos-system-zeus-26.11.20260813.0e251e2.drv`.
Expected system output:
`/nix/store/wk4qr8cf2bkjszrb86jp076caif15jpn-nixos-system-zeus-26.11.20260813.0e251e2`.

The exact multi-output derivations were:

- `/nix/store/2npxr57piqkyv546whw9mdyd1lzq4lhr-qtwebengine-6.11.1.drv`
- `/nix/store/ciqigjiwyq9ld8fils53zv6fx15q0ykl-webkitgtk-2.52.5+abi=6.0.drv`

Before reuse, Prometheus had their primary outputs but lacked four required sibling
outputs.  Ouranos had all four exact paths, which were copied through the existing
authenticated `ssh-ng://nix-ssh@prometheus.goldragon.criome` route:

- `/nix/store/lfzaifrqgazf06kr4lngn5q9j7j8rpr3-qtwebengine-6.11.1-dev`
- `/nix/store/40gdpqryk4d9pkrxk57cm6lkpppvpd4g-webkitgtk-2.52.5+abi=6.0-debug`
- `/nix/store/5sh5nnz019nkz1gmj261s4xbp6q9ybb2-webkitgtk-2.52.5+abi=6.0-devdoc`
- `/nix/store/v00hnls4g413a1lkv9zwgsr80z6kmzrp-webkitgtk-2.52.5+abi=6.0-dev`

Prometheus verified all four paths after the copy. The transfer used a per-command
signature override because the authenticated Ouranos paths lacked a key trusted by
the Prometheus store; no global Nix configuration changed.

Nixpkgs is unchanged from the initial and prior Zeus source snapshots:
`f83fc3c307e74bc5fd5adb7eb6b8b13ffd2a36e1`, Nar hash
`sha256-cCO8aTqss5x9Ky8GWkpY0Hy5fyTZEbtifSUV8QjSzic=`.

The current direct Prometheus realization restarted after verification as
`zeus-build-1a9f5fdf.service`, PID 408142. Zeus itself was not changed.
