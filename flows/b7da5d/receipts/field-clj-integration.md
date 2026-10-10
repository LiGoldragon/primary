# field-clj integration receipt — 2026-09-25

## Source and consumer state

- GitHub canonical `field-clj` `main`: `d12dc35ee05ef2b8c936fb1e7c2b82a11e0e24bc`, subject `field-clj: clj-build 9c1778b`.
- Canonical source declares `#commit [message [path ...]]` and `#commit-to [message [path ...] remote-url]`; the former is the required supported smoke form.
- `/git/github.com/LiGoldragon/CriomOS-home` is clean at local and remote `main` `2ab91c1ecba56b54b6f0112c7747033f4cb0ab22`.
- Its Medium CLI package wiring already includes `inputs.field-clj.packages.${system}.default`; its lock still pins field-clj `212cf38f67a3f6729169902bb490e61880e204cb`. The required declarative delta is therefore that one input-lock update, but it was not made.
- Live `field-luna-heartbeat.service` remains `masked` and `inactive`.

## Coordination

`orchestrate 'Observe.Locks'` showed no lock covering canonical CriomOS-home paths. It did show lock `6094`, owned by `00f95a`, for the HM state directory. The active collaboration graph did not expose e51411 as a route; parent was asked to obtain its Flow-activation handoff. No shared Home claim, mutation, build, or activation occurred while that handoff remained unwitnessed.

## Local package witness

A fresh shallow clone of canonical field-clj at `d12dc35` passed both commands with local builds forced (`--option max-jobs auto --option builders '' --option substituters https://cache.nixos.org`):

- `nix flake check -L`: success, evaluated package and test derivations; no check build was needed because outputs were already available.
- `nix build -L --no-link .#default`: success.

## One smoke invocation

Exactly one invocation used the built package on primary:

```text
FLOW_ID=b7da5d field-clj '#commit ["b7da5d: field-clj smoke" ["flows/b7da5d/receipts/field-clj-smoke.md"]]'
```

It returned `#success` with local commit `b86aa25951f7a147e8a35726d528a094bcaf6e6b`, path list containing only the fixture, and `:main :pushed :present`. An independent `git ls-remote origin refs/heads/main` returned the same commit.

## Requested clj-build check

Fresh clone at requested `01126ad41b8f06ebd1469db30e89efc7dc74b649` ran `nix flake check -L` with the same forced-local options. It failed in `example-uberjar`: copying AOT classes into read-only `staging/` was denied. The initial failing derivation was `0xf3dcdsj3ylmr2wb9l9jc2kvcqqk2jk-example-uberjar.drv`; this is the known staging-permission defect and is distinct from field-clj at its newer `d12dc35` pin.
