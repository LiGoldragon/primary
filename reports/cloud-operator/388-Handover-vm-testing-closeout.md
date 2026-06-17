---
title: 388 — VM testing closeout
role: cloud-operator
variant: Handover
date: 2026-06-17
topics: [vm-testing, criomos, horizon, test-cluster]
description: |
  Closeout for the cloud-designer report-55 VM-testing operator handoff:
  what landed on main, which gates passed, which gates remain blocked,
  and which live/Prometheus follow-on work remains authorization-gated.
---

# 388 — VM testing closeout

## Scope

The report-55 implementation handoff is landed through the safe hermetic
surface. The dependency order is complete: `horizon-rs` first, `CriomOS`
second, `CriomOS-test-cluster` last with cross-repo flake pins refreshed.
No live remediation, deploy, activation, router switch, or Prometheus live
operation was run.

## Landed mains

- `/git/github.com/LiGoldragon/horizon-rs` main and origin are at
  `087a3b6d` (horizon refresh plus multi-host test-VM support already
  integrated).
- `/git/github.com/LiGoldragon/CriomOS` main and origin are at
  `6646275d` (Unit 3 scoped image-exchange key emission is present).
- `/git/github.com/LiGoldragon/CriomOS-test-cluster` main and origin are
  at `18441971` (latest CriomOS pin, deploy-flake original-URL preservation,
  fixture canonicalization, current Lojix request shape, bounded SSH probe).
- Supporting pins are aligned: CriomOS root `criomos-home` is
  `865c47e1541022ef83f09d4dd214eba195b0d8d0`; both CriomOS and
  CriomOS-home resolve Chroma to
  `6879a393123ec147b2d8ddbe92caec498eb5646e`; test-cluster root Lojix
  resolves through `lojix_2` to
  `b1a05212e3a3e56e8cdd000adcc4b76b6de37a09`.

## Green gates

- `horizon-rs` current main: `cargo build`, `cargo test`, and
  `cargo clippy -- -D warnings` pass. The cargo test run executes 135
  tests across the repository test suite.
- `CriomOS` current main with temporary synthetic `system` and fieldlab
  `horizon` overrides: `image-exchange-keys-scoped-to-co-hosts`,
  `vm-testing-prometheus-policy`, `nspawn-role-policy`,
  `metal-firmware-policy`, `router-wifi-horizon-policy`, and
  `nix-role-policy` pass.
- Published `CriomOS-test-cluster` main `18441971` passes the relevant
  integrated gate set: `projections-match-fieldlab`,
  `pod-missing-super-node-rejected`,
  `multiple-tailnet-controllers-rejected`, `cluster-contracts`,
  `full-module-contracts`, `vm-mercury`, `lojix-deploy-smoke`,
  `vm-base-home`, `vm-dune`, and `vm-edge-desktop`.

## Known blocked gate

`CriomOS-test-cluster` `spirit-nspawn-can-build` still fails because the
Spirit/persona dependency path attempts to fetch private or missing
`github.com/LiGoldragon/nota-derive.git`. This is not a VM-testing
regression witness until the nota-derive access or dependency graph is
fixed.

## Subagent findings

The authorized reviewer subagents produced no usable review output: the
run ended failed with one connection error, one missing `progress.md`
assumption, and one context-size overflow. The implementation was therefore
reviewed and tested directly in the main lane.

## Working copy state

The code repositories checked at closeout have clean working copies and
local/remote main parity: `horizon-rs`, `CriomOS`, `CriomOS-test-cluster`,
`CriomOS-home`, `lojix`, `signal-lojix`, and `meta-signal-lojix`.

Primary had one tracked Pi continuation tattoo update under `.pi/continue/`
from the compaction/continuation mechanism while this report was written;
that is committed with this report so primary ends clean as well.

## Deferred live and Prometheus work

The live path that removes `LiveNotYetEnabled`, the real host-untouched
cycle, and Prometheus/goldragon wiring remain deferred. The safety envelope
still applies: no live run, deploy, remediation, activation, router switch,
or Prometheus host operation should run without explicit user authorization
naming the target and operation.
