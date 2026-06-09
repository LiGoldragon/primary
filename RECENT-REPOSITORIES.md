# Recent Repository Index

This workspace links repositories through `ghq` under `/git/github.com/...`.
`~/primary/repos` is only a symlink index; repository state stays in the ghq
checkout.

This is a broad checkout index, not the current architecture focus. For the
smaller active set used during Persona architecture sweeps, read
`protocols/active-repositories.md`.

Selection basis: on-disk LiGoldragon checkouts that are NOT archived on GitHub
and have a local commit on or after the cutoff. Regenerated 2026-06-09 from
authoritative GitHub archive state (`gh repo list`) + local `git log`.

Current cutoff: keep only repositories with a latest commit on or after
2026-04-22. Older repositories do not belong in this primary working set.

## Links

| Name | Last local commit |
|---|---|
| `AnaSeahawk-website` | 2026-04-27 |
| `arca` | 2026-05-30 |
| `ArtificialIntelligence` | 2026-05-18 |
| `BookOfLuna` | 2026-05-18 |
| `brightness-ctl` | 2026-05-09 |
| `caraka-samhita` | 2026-06-05 |
| `chroma` | 2026-06-08 |
| `chronos` | 2026-06-08 |
| `clavifaber` | 2026-06-08 |
| `cloud` | 2026-06-08 |
| `criome` | 2026-06-08 |
| `CriomOS` | 2026-06-07 |
| `CriomOS-emacs` | 2026-06-08 |
| `CriomOS-home` | 2026-06-08 |
| `criomos-horizon-config` | 2026-06-05 |
| `CriomOS-lib` | 2026-05-29 |
| `CriomOS-pkgs` | 2026-05-28 |
| `CriomOS-test-cluster` | 2026-05-25 |
| `domain-criome` | 2026-06-08 |
| `forge` | 2026-06-05 |
| `goldragon` | 2026-06-05 |
| `harness` | 2026-06-08 |
| `hexis` | 2026-05-13 |
| `horizon-rs` | 2026-06-08 |
| `introspect` | 2026-06-08 |
| `kameo` | 2026-05-13 |
| `kameo-testing` | 2026-05-14 |
| `kibord` | 2026-05-30 |
| `library` | 2026-06-05 |
| `lojix` | 2026-06-08 |
| `lojix-cli` | 2026-06-08 |
| `lore` | 2026-06-05 |
| `mentci-egui` | 2026-05-14 |
| `mentci-lib` | 2026-06-05 |
| `message` | 2026-06-08 |
| `meta-signal-agent` | 2026-06-08 |
| `meta-signal-cloud` | 2026-06-07 |
| `meta-signal-domain-criome` | 2026-06-07 |
| `meta-signal-lojix` | 2026-06-07 |
| `meta-signal-mind` | 2026-06-08 |
| `meta-signal-orchestrate` | 2026-06-08 |
| `meta-signal-persona` | 2026-06-08 |
| `meta-signal-repository-ledger` | 2026-06-07 |
| `meta-signal-router` | 2026-06-08 |
| `meta-signal-spirit` | 2026-06-08 |
| `meta-signal-terminal` | 2026-06-08 |
| `meta-signal-upgrade` | 2026-06-08 |
| `meta-signal-version-handover` | 2026-06-08 |
| `mind` | 2026-06-08 |
| `nexus` | 2026-06-08 |
| `nexus-cli` | 2026-06-05 |
| `nota-config` | 2026-06-08 |
| `nota-next` | 2026-06-08 |
| `orchestrate` | 2026-06-08 |
| `persona` | 2026-06-08 |
| `persona-pi` | 2026-05-24 |
| `persona-spirit` | 2026-06-08 |
| `qmkBinaries` | 2026-05-30 |
| `repository-ledger` | 2026-06-08 |
| `router` | 2026-06-08 |
| `schema-next` | 2026-06-06 |
| `schema-rust-next` | 2026-06-08 |
| `sema` | 2026-06-07 |
| `sema-engine` | 2026-06-08 |
| `signal` | 2026-06-08 |
| `signal-agent` | 2026-06-08 |
| `signal-cloud` | 2026-06-07 |
| `signal-criome` | 2026-06-08 |
| `signal-derive` | 2026-05-24 |
| `signal-domain-criome` | 2026-06-07 |
| `signal-forge` | 2026-05-24 |
| `signal-frame` | 2026-06-08 |
| `signal-harness` | 2026-06-08 |
| `signal-introspect` | 2026-06-08 |
| `signal-lojix` | 2026-06-07 |
| `signal-message` | 2026-06-08 |
| `signal-mind` | 2026-06-08 |
| `signal-orchestrate` | 2026-06-08 |
| `signal-persona` | 2026-06-08 |
| `signal-repository-ledger` | 2026-06-07 |
| `signal-router` | 2026-06-08 |
| `signal-sema` | 2026-06-08 |
| `signal-spirit` | 2026-06-08 |
| `signal-system` | 2026-06-08 |
| `signal-terminal` | 2026-06-08 |
| `signal-upgrade` | 2026-06-08 |
| `signal-version-handover` | 2026-06-08 |
| `spirit` | 2026-06-09 |
| `substack-cli` | 2026-05-01 |
| `system` | 2026-06-08 |
| `terminal` | 2026-06-08 |
| `terminal-cell` | 2026-06-08 |
| `TheBookOfSol` | 2026-06-08 |
| `triad-runtime` | 2026-06-08 |
| `upgrade` | 2026-06-08 |
| `version-projection` | 2026-06-08 |
| `WebPublish` | 2026-05-30 |
| `whisrs` | 2026-05-11 |

## Below cutoff (non-archived) — prune candidates

These local checkouts are not archived on GitHub but have not been touched
since before the cutoff. Confirm intent, then archive or refresh:

| Name | Last local commit |
|---|---|
| `annas-mcp` | 2026-02-22 |
| `BookMaker` | 2026-02-12 |
| `maisiliym` | 2026-04-18 |
| `pi-delegate` | 2026-04-03 |
| `TheBookOfGoldragon` | 2026-02-23 |
| `wiki` | 2025-09-10 |

## Archived-but-checked-out — local clutter (34, 2026-06-09)

These repositories are archived on GitHub yet still have local `/git`
checkouts. They are pruning candidates (re-cloneable from the archive if ever
needed); the intentional reference archives among them
(`criomos-archive`, `lojix-archive`, `nexus-spec-archive`) may be kept
deliberately. Removing the rest declutters the working set per Spirit `bds6`.

```
arbor Armbian-RockPi4B-NixOS aski askic aski-cc 
askicc aski-core astro-aski atom awesome 
corec criomos-archive domainc horizon-next kameo-testing-assistant 
lojix-archive mentci-tools ndi nexus-spec-archive noesis 
noesis-schema orchestrator schema-core semac sema-upgrade 
signal-executor signal-sema-upgrade synth-core test-city veric 
veri-core vscode-aski webpage workspace 
```
