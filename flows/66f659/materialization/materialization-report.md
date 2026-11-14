# Lojix A/B/A materialization result

## Result

All three Astra-approved, materialization-only `Deploy.Host Realize RequireImmutable` stages succeeded. Each stage had a node watcher armed before submission, reached `Completed Some.Succeeded` through that watcher, and was queried exactly once after its terminal event. No deployment polling, activation, test activation, profile or boot change, `/etc` switch, service action, network test, source edit, pin, or owner configuration was performed.

| stage | revision | watcher | deployment | terminal |
|---|---|---:|---:|---|
| A | `d7957edc0b71a19faa20b4dfb714432df2d57833` | 67 | 539 | `Some.Succeeded` |
| B | `2abc8e21dd249a9d2ab4aaf1d9c012b4dba0c628` | 68 | 540 | `Some.Succeeded` |
| A repeat | `d7957edc0b71a19faa20b4dfb714432df2d57833` | 69 | 541 | `Some.Succeeded` |

## Realized aggregates

Lojix job-state artifacts identify the realized derivations and outputs. Read-only Nix database queries independently confirm each output's deriver and each derivation's output:

- A and A repeat derivation: `/nix/store/zkr9zf2ipqz3d0k9q92r4mn22wyparhg-nixos-system-ouranos-26.11.20261107.f4a03c0.drv`
- A and A repeat output: `/nix/store/hv1s2y9qryfypcxrcjgk78i4kl63jrns-nixos-system-ouranos-26.11.20261107.f4a03c0`
- B derivation: `/nix/store/3lkhdhnl6wsfv7m0pw697kx33kwjxxfg-nixos-system-ouranos-26.11.20261107.f4a03c0.drv`
- B output: `/nix/store/6gndl3zpqzxmaii8iak0ispdh232h77m-nixos-system-ouranos-26.11.20261107.f4a03c0`

The A request and A-repeat request are byte-identical (`sha256 4a44f2ea2c62dce7c8bf27756e69d5019279dbcbe10d8aed29e40935cbdd505d`). Lojix job state associates deployment 541 with the same A derivation and output, establishing derivation and store-output reuse. The retained daemon journal records only terminal pipeline messages and does not segregate Nix compiler output by deployment, so absence of repeated compilation is not independently established from logs; it remains unclaimed.

## Preserved running state

Before and after the materializations:

- system profile: `/nix/store/2qp14k4s71z76icbzgsdfxfmqqd3h0ql-nixos-system-ouranos-26.11.20261107.f4a03c0`
- runtime: `/nix/store/50d4ivvi47c59fwc3g20fqs0kxby273s-nixos-system-ouranos-26.11.20261107.f4a03c0`
- `lojix.service`: active/running, PID 1637, invocation `cab761e707f94dfeb26321aa7b6599e7`

No `lojix WatchDeployments` process remained at the final check.

## Evidence

The directory `/home/li/primary/flows/66f659/materialization/` contains the exact request datoms and hashes, watcher streams, admissions, one post-terminal record per deployment, pre/post running-state checks, bounded job-state association result, root/deriver validation, and this report. Secret contents were not retained.
