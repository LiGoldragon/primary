# Capsule Nexus naming migration: gated branches

Request: Psyche core Opus `tsk5`. GitHub rename confirmation: `sbhr` and Result `nx74`. Approved vision: psyche-belief `e66f43e6a12b8d64411c25cb1f1eed21a2716c16`.

## Published candidates

All five source branches are `rename/capsule-cdc93e`, owned by flow `cdc93e`. They remain branches; no component/Home merge or live switch was performed.

| Repository under LiGoldragon | Published candidate | Remote checks |
| --- | --- | --- |
| capsule-nexus | `929f63fa5f2fa3e415bac290b9fd85564ba6040a` | PASS, 31 attributes |
| signal-capsule-nexus | `7fc8ea7ccc23f04d1c654d32280c113958882d8b` | PASS, 8 attributes |
| meta-signal-capsule-nexus | `5d609360750234802993ffc8fb4618f4e65fc390` | PASS, 9 attributes |
| capsule-nexus-tests | `e04cb19775b5a71753a7da4548145806601dfbea` | PASS, 1 attribute; 32 tests |
| CriomOS-home | `97634ef83021357c8625bdc55c437e4e173fceb4` | PASS, 98 attributes; checks-only projected fixture |

The four GitHub repositories were renamed exactly as confirmed in `capsule-rename-inventory.md`. GitHub redirects retain access to old repository URLs. Each naming branch began at that repository's published GitHub main, not an event candidate. Component baseline: `c0bcca1358d914f2ba35076318a8ab8f9a08aec2`; ordinary: `813d3298616f83fbeb3951b850da51fba3b01498`; meta: `2d96171cf65c6b7f64754b4cc94496d3d90216af`; tests: `07df7cf2bf9cb6e0795ca624a7fc33ec5c77a169`; Home: `e7a4157ee06f1365ec6a408ed5b14218719c10d0`.

## What changed

- Component/package/import identities moved from herdr-nexus to capsule-nexus. Public clients are `capsule` and `capsule-meta`; process helpers are `capsule-place`, `capsule-pair`, and `capsule-translator`. The component's daemon remains the internal package/executable `capsule-nexus-daemon`.
- Component sockets are `capsule.sock`, `capsule-meta.sock`, `capsule-translator.sock`, and `capsule-meta-translator.sock`. Source, generated contracts, check scripts, executable paths, documentation and external socket assertions agree.
- The typed backend emission remains `Herdr`. Backend command spelling, HerdrPath configuration, backend fixtures and backend behavior retain their herdr identity.
- Client argument semantics and the implementation architecture remain the published baseline's, explicitly approved by Result `tthk`; this release claims naming and its gates, not a completed architectural/event repair.
- Home changes one authored module selector: `vision:herdr-nexus:1` to `vision:capsule-nexus:0`. The `herdrNexus` permaflow address is unchanged. Generated skill trees were not edited.
- Existing external scenarios retain their assertions. Fixture plumbing now uses the published baseline's PlaceName/place_name and Dispatcher constructor/dispatch API. No test was removed. Its old injection patch still applies with zero fuzz.

## Shared build coordination

Core Sol owns the additive build-base registry change, now canonical at `13319ba1e92fd85fc9b7c646f55d57875ae52b3d`. Old contract identities remain for unmigrated consumers. Core's report is `flows/1541ef/build-base-capsule-registry/report.md`.

The component pins the published renamed contract source revisions `dc941e72a31f7084f80b6fa8fe9aa49963acb4a1` and `b8fde9e2be92f75945a208208d4b93d6e5fd7e69`, which the registry names. Contract branch tips are lock-only descendants selecting the coordinated base. Their own Cargo.lock graphs match their published-main baselines after changing only the package names. Remote regeneration of their Cargo.nix files matched byte for byte.

The component's original Cargo graph lacked dependency edges demanded by the newer shared Tokio/Mio feature unions. Its wire manifest now carries net/signal/tracing and Mio/log edges; Cargo.lock and Cargo.nix were regenerated remotely. New registry dependencies were aligned to the existing canonical set, including Mio 1.2.3 and log 0.4.34. No shared registry was changed by this flow, no git dependency other than the renamed contracts was advanced, and no event implementation was adopted.

## Consumer findings and boundaries

Flow integration owner Mind flowNexus Opus answered `a4n0`: Flow currently drives the backend directly and has no component crate/flake/socket/CLI binding to rename. Its unrelated test-environment term capsule is unchanged. No Flow code edit was necessary; k7jy reservations and recovery82 were untouched.

The separate translator repository has no old component identity in the inspected working trees or fresh published-main manifests. The component's own translator crate was renamed and gated. Mind curriculum Opus answered `r5pr` that it holds neither translator nor Home source custody; the isolated Home branch above is this flow's one-line consumer update.

`metaflow/deployment.nix` remains untouched, as Opus ordered. No broken metaflow pin was observed. Opus owns the authored active-projects and nix-rust-builds module updates after the names stand.

The external tests retain their existing rust-build/crane gate for this naming release, explicitly authorized by Result `tthk`. Its separate build-base migration is bead `primary-b7mi`; it was not folded into this change.

## Gate reproduction and evidence

Each gate ran against the full published revision in the table, on Prometheus, via:

```sh
nix run github:Mic92/nix-fast-build -- \
  --remote prometheus.goldragon.criome --no-nom --no-download \
  --eval-workers 1 --flake "github:LiGoldragon/$repository?rev=$revision#checks.x86_64-linux"
```

The contract/component gates include `checks.default` and the individually named checks. Every final command exited 0. Cargo.nix regeneration and compilation happened on the builder, not the laptop.

Home used Field's retained OS-projected system fixture, only for `checks.x86_64-linux`, with default test Horizon stubs and no secrets override. Both the original `/var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system` and the existing builder copy `/tmp/offload/1541ef-generated-inputs/system` were freshly verified as `sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=` before the gate. No new materialization or copy was needed. Field Result `r17u` and Core notice `mt0t` supplied the route; the prior nested invocation is retained in `flows/1541ef/home-codex-fixture-evidence/full-gate-e7a4157e.log`.

The Home invocation additionally used `--always-upload-source --eval-max-memory-size 16384 --override-input system 'path:/tmp/offload/1541ef-generated-inputs/system?narHash=sha256-KW3DUTifDJ6m2JuYiTVtJz%2B9ieAgqjCb46wgrMqxJJU%3D'`. This proves the checks fixture, not a complete target Home build or deployment.

Raw logs remain in `/tmp/capsule-rename.OD0JT7/`: `ordinary-final-gate.log`, `meta-final-gate.log`, `component-aligned-gate.log`, `external-aligned-gate.log`, `home-projected-gate.log`. Earlier failed attempts are retained there too: missing initial registry entries, missed public-binary check paths, shared graph attachment gaps, old fixture API names and old socket assertions were corrected before the final green revisions. The initial bare Home evaluation refused the intended missing system input; it was replaced by the verified projected-fixture gate, not by invented inputs.

## Custody

New source paths were reserved by Orchestrate lock 253; the isolated Home worktree by lock 255. Existing dirty canonical checkouts, pinned22, event/backend candidates and their locks were preserved. Component bead `herdr-nexus-6kl` is closed for this bounded naming task. Review/merge and deployment remain with the requesting owners; this report grants no activation authority.
