# External Horizon configuration implementation

## Delivered boundary

`criomos-horizon-config@7050afef14bcfe649c0d05bdaa681d1577cafc46` authors
only the public, cluster-neutral `HorizonConfiguration`: its generic node
catalogue and constants. It exports `composeHorizonDefinition`, a parameterized
derivation that accepts explicit configuration, cluster, system, and Horizon
composer inputs. It pins neither Goldragon nor a cluster. Its tested
`1f58fc5ef85d95c27049767726e25dc60b7009e5` ancestor has the identical tree and
NAR hash.

Goldragon owns the cluster-specific side: `ClusterDefinition`, the selected
generic-node names, and the thin composition/render owner. Its final published
source is `1f49f8dea50932cacc781d531c48b6d20805b439`. It invokes Horizon’s typed
composer over the two explicit public inputs and exposes the canonical child
rather than a flat store file:

`/nix/store/0in67wflv4rxnylf4hbpdmni3m5as4sl-horizon-definition/horizon-definition.datom`

The child is a 5,987-byte public document with SHA-256
`eac13fa803fa8db358dfd03fc9a7c1a74bca27970b37008be4eccc9873322947`.
Horizon `05879e7c1e5f637f78fbe26234b95213c77c59bc` decodes and composes it.
Lojix receives that one regular child as `ProposalSource`; it resolves the
selected node before projection and never infers catalogue, cluster, or sibling
paths. `SecretsInput` remains a separate privileged request authority.

Availability is distinct from membership: the catalogue contains generic Live
installer definitions, while a cluster receives only the generic names it
selects. Resolution rejects unknown selected names and local/generic name
collisions. The public document contains public facts and opaque secret
references only.

Goldragon’s rendered Synchronizer configuration names the same explicit
canonical child through `ClusterSource.HorizonDefinition` and retains dynamic
`ClusterRole.NixBuilder` selection. It does not replace the data-driven role
with a direct host. Synchronizer source `b42c9df295adccdd65381f8bd444147099036183`
passed its producer gate.

## Consumer and owner status

| Scope | Final source or owner | Evidence |
| --- | --- | --- |
| Horizon | `05879e7c1e5f637f78fbe26234b95213c77c59bc`, package 0.6.0 | Typed compose/projection suite and remote Nix packages passed. |
| Lojix | `7e29c37f51092e5a20abf88c670aabd2acee6e52`, package 0.21.0 | One-root Datom admission, four generated flake inputs, separate `SecretsInput`, framed clients, and v5 store boundary passed. Its merge tree equals the behavior/docs tree while retaining the prior main history. |
| Orchestrate | `ac8a92666f4abd8356522c4d52ab23ddcdff4c15`, package 0.30.0 | Current Datom structural frames, offline v1-to-v2 migration, restart and exclusive-open checks passed. |
| Claude Answers | `3a14cb12f885932de35a7ef7793e8a99a796c67f` | Current datom-codec/Protos generation and remote package checks passed; CriomOS-home is its declarative owner. |
| Curriculum deploy | `7cc3cb53a10ab6ada383ea647c1ac87d1409266d` | Current codec/generator checks passed; Primary’s flake is its actual owner and check-skills consumer, without an invented OS input. |
| CriomOS-home | `be20529823792d525659053399c31c040ce94bfb` feature | The exposed Horizon user adapter accepts the projected users vector; actual materialized Chroma checks passed. Main remains held for combined acceptance. |
| CriomOS | `add8a445052e9517a10eff7877ed7608aca871b2` feature | Four-input materialized Mercury evaluation and CompleteHost BuildOnly receipts are recorded; main remains held for combined acceptance. |
| CriomOS-test-cluster | `54f29d2b898eab6f110496adc11e214de9f044a3` feature | Nine current projections and negative composition fixtures passed earlier. The final C6 VM gate is attached and pending at this record’s update. |

The previous public `proposal.datom`/legacy configuration path is not an active
consumer boundary. Public composition now publishes `horizon-definition.datom`;
private files were neither read nor changed.

## Final C6 preflight and pending gate

A real Lojix BuildOnly request materialized `(fieldlab, mercury)`, `BaseHost`,
`NoSecrets`, the canonical fieldlab child, and immutable CriomOS
`f59d12116a19e8a44325fc9d97d64cccd06357c7` through the normal
`nixosConfigurations.target.config.system.build.toplevel` selector. It emitted
the four caller-owned `system`, `horizon`, `deployment`, and `secrets`
directories (0700). Its retained terminal replay returned
`(BootstrapTerminal.Succeeded)` with exit 0. The actual generated inputs
produced:

- derivation `/nix/store/mkqzyi7vsicjkxiv40wy4rd1n2dnd2gj-nixos-system-mercury-26.11.20260813.0e251e2.drv`;
- closure `/nix/store/rdlmvd1bhax248fzkgxwb5lq04bbivcd-nixos-system-mercury-26.11.20260813.0e251e2`.

The caller-owned 0700 preflight root is
`/tmp/lojix-c6-f59-fieldlab-mercury-542442.FUTmsp`; its durable journal is
`journal/.lojix-bootstrap-v5-e2c19d1a075a262b941e1edf8a18e7714de04849e40bccea3528b6bb1eecd632`
and its terminal evidence is `terminal.rkyv` with SHA-256
`a19589c84803a186d44f66d2e342797516278896a2c5991eacc465ae45973d38`.

The same real generated inputs evaluate the fixture-only
`add8a445052e9517a10eff7877ed7608aca871b2` successor to the identical Mercury
derivation and closure. The C6 driver no longer uses
the static 1eed fixture, and it no longer assumes legacy `Deployed`, `FullOs`,
or `Boot` reply terms. It now asserts `DeployAccepted`, `Queried`,
`BaseHost BootProfile Current`, `Completed`, and `Succeeded`, as well as target
profile and derivation equality.

Its isolated source replay serves only the exact add8 GitHub archive route over
fixture-local TLS, rejects unmatched routes, verifies the resolved source path,
revision, and NAR hash before daemon start, and leaves Lojix’s immutable GitHub
admission unchanged. The attached remote C6 VM build is the pending terminal
acceptance; this report does not treat its preflight as that result.

## Sources

- Living approval: user ordinal 532 and preceding proposal ordinal 525 in `/home/li/.codex/sessions/2026/09/05/rollout-2026-09-05T18-45-08-01a07275-a9f1-7d03-8662-24b542442db3.jsonl`.
- `reports/horizon-preservation.md`, `reports/final-source-inventory.md`, and the witnesses beside this report.
