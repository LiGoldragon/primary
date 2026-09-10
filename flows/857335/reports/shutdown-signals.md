# Signal migration shutdown checkpoint

## Published producer heads

- `signal-standard` current schema/matching capability: `2c90fc9976b3af33f49cdf83bb33f7f246ae2b60` (v1.0.0). Local tests/fmt/clippy passed. The prior configured Nix invocation on `6688f8ca` exited 0 only after remote SSH failed and local fallback built; this is not remote-execution proof. The final-head configured matrix has no recorded exit.
- `signal-mirror` current contract plus typed carrier: `e6c565caac516dae3fc679ea5e110828580f3d57` (v1.0.0). Default tests passed before carrier addition; carrier API has local tests only.
- `meta-signal-mirror` current contract plus carrier and ordinary carrier pin: `bdc76bcdd09107a3d039ad434b772e3474861520` (v1.0.0). Default/Datom tests passed locally.
- `signal-introspect` version correction: `910b1e378098261784eedaf0ea920edb1ecc112c` (v1.1.0), remote gate outstanding.

## WIP runtime

`mirror` WIP is pushed under bookmark `wip-flow857335-signal-port` at `783be4b84c04d6b2ebb65c8f93fe140ba7d2646f`; it is intentionally not main/releasable. It contains current producer pins, partial named data conversion in engine/ledger/store/decision, and typed carrier work in daemon/service/shipper. `cargo check --no-default-features` fails; the latest durable captures are `witnesses/mirror-*-compile*.{log,exit}`. Shipper payload and response handling, service/daemon cleanup, config/lifecycle/package work, tests, and all gates remain unfinished.

Spirit implementation is durably preserved as WIP bookmark `wip-flow857335-spirit-port` at `5c53df2a94123794c597443a2fdd67bf45a045bd`; it is intentionally not main/releasable. It includes implemented and locally tested workspace split, typed signal migration, lifecycle/migration witnesses, and process fixtures. Its declared-feature closure, final package/lifecycle audit, immutable producer pins, remote Nix gates, and release review remain outstanding.

## Resume order

1. Acquire fresh Mirror producer/runtime locks; resume WIP bookmark in an isolated checkout.
2. Finish named `store`/`decision`, then error/daemon/service/shipper transport; retain offline-only historical migration.
3. Complete Mirror Nexus lifecycle/configuration split and tests before any release branch movement.
4. Run actual remote gates for final Standard, Mirror, Meta Mirror, and Introspect heads.
5. Resume Spirit feature/Nexus closure and re-pin only immutable green producers.

No protected Home paths were edited and no live deployment was performed.
