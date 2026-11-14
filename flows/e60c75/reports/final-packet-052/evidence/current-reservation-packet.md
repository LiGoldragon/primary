# Current reservation packet

Observation window: 2026-11-05 22:13:19–22:16:46 UTC. This packet is a read-only reservation check; no fetch, mutation, allocation, publication, or body work occurred. No authoritative private reservation ledger was available, so absence from these observations is **UNKNOWN**, never clearance. The old `342` namespace capture remains timestamp-UNKNOWN.

## Requested coordinates

- Flow shared workspace: `flow-ethos`, `flow-meta`, `flow-native`, `flow-nexus`, `flow`, and retained/conditional `flow-defaults`: common `0.52.0` revision (retire defaults if not retained).
- `signal-flow`: requested `44.0.0`.
- `meta-signal-flow`: requested `60.0.0`.
- `sema`: requested `0.2.0`.
- `sema-engine`: requested `0.19.0`.
- `datom-codec` and conditional `datom-codec-derive`: requested `0.33.0`; derive remains `0.32.0` unless actual expansion delta is demonstrated.
- `protos`: requested `0.33.0`.
- Memory coordinates: `flow_nexus_runtime_policy` v1 / `flow-nexus-runtime-policy-v1`; `flow_nexus_resume_heads` v1 / `flow-nexus-resume-head-v1`; `flow_nexus_resume_attempts` v1 / `flow-nexus-resume-attempt-v1`; existing `flow_nexus_meta_metaflow_configuration` v6 / `flow-nexus-meta-metaflow-configuration-v6`.
- redb: package `4.3.0` retained; owned Git fork requested, exact ref/owner to be recorded from discovered repository, not invented.

## Local observations (each at 2026-11-05T22:13:19Z)

| Repository | prepared HEAD / local identity | local source URL evidence |
|---|---|---|
| flow | `916b54574ae0024b893a9f4252f2e97704db48c1` (`0.51` workspace; describe `flow-0.17.4-492-g916b545`) | origin `/git/github.com/LiGoldragon/flow` |
| signal-flow | `ce083f2ba9cc0bd928735ba4cc09e59965982e30` | no remote URL in worktree; proposal names GitHub source owner |
| meta-signal-flow | `281f5aa1b88cd43609c127cdf6f3c12645faf58b` | no remote URL in worktree; proposal names GitHub source owner |
| sema | `51d7927c872f0df12791bad8d39a4db6433b01a1` (`v0.1.0-11`) | origin `git@github.com:LiGoldragon/sema.git` |
| sema-engine | `9884905ff9c660ad97a35c524e42532d5c7bac90` (`v0.1.0-81`) | origin `git@github.com:LiGoldragon/sema-engine.git` |
| datom-codec | detached `4dff16b4f7412febc3b71aac8b49680cd20988cb`; cached `refs/remotes/origin/{HEAD,main}` both same | source URL held in prep custody: `https://github.com/LiGoldragon/datom-codec`; manifest `datom-codec 0.32.2` |
| protos | detached `15b41da8f2579e73ead59bc0c2b97529b8ac32d3`; cached `refs/remotes/origin/{HEAD,main}` both same | source URL held in prep custody: `https://github.com/LiGoldragon/protos`; manifest `protos 0.32.2` |
| redb | local registry `4.3.0`, import `1e985fb3c51126676047f295c8630b17229ef11d`, local registry ref `4936637de6faf266d02f479141c01c55190f4759` | no prior owned remote URL |

## Remote observations

Raw receipts are saved in this report directory as `current-reservation-*.ls-remote.txt`; SHA-256 receipts: `current-reservation-redb-github-receipt.json` is retained verbatim as connector JSON and `actual-maincheckcodec-derive-impact.md` records the conditional derive result; each records its own observation timestamp and URL. Known source URLs queried only: `https://github.com/LiGoldragon/flow.git`, `git@github.com:LiGoldragon/{sema,sema-engine,signal-flow,meta-signal-flow}.git`.

- Flow (22:13:19): remote has `next/waiting-acceptance-0.51-66ac59` at the prepared HEAD; no requested `0.52.0` tag observed. Current heads/tags are not a reservation ledger; requested version remains UNKNOWN.
- Sema (22:13:20): only `v0.1.0` tag; no `0.2.0` tag observed. UNKNOWN, no auto-bump.
- Sema-engine (22:13:21): no release tags in returned heads/tags; requested `0.19.0` UNKNOWN.
- Signal-flow (22:13:22): `next/a8f7-70a111` at `d3a5fbc...`; no `44.0.0` tag observed. UNKNOWN.
- Meta-signal-flow (22:13:24): `next/a8f7-70a111` at `8fcbf846...`; no `60.0.0` tag observed. UNKNOWN.
- Datom-codec (22:15:23) remote `main` is `f1796c7...`; no `0.33.0` tag observed. Protos (22:15:25) remote `main` is `103ed6b...`; no `0.33.0` tag observed. Raw receipts are `current-reservation-datom-codec.ls-remote.txt` and `current-reservation-protos.ls-remote.txt`. Requested `0.33.0` coordinates remain UNKNOWN; derive expansion delta remains conditional on the source-ledger actual-emission check, not an independent allocation.

## Current manifest observations

Read-only raw Cargo.toml content was checked at returned commit hashes; each raw response is saved as `current-manifest-*.txt` with its URL and timestamp. Observed package versions: datom-codec main `f1796c7...` = `0.32.12`; protos main `103ed6b...` = `0.32.2`; repository sema main `8d6748...` declares PACKAGE `memory 0.1.1`; repository sema-engine main `cd57ed...` declares PACKAGE `memory-engine 0.18.0`; signal-flow main `74f4da...` = `39.0.0`, next `d3a5fbc...` = `43.0.0`; meta-signal-flow main `939c9c...` = `49.0.0`, next `8fcbf8...` = `59.0.0`. Flow root Cargo.toml at main `8a83d9...` reports workspace `0.48.0`; this is not treated as the prepared 0.51 package identity. These are current manifest observations, not reservations or clearance; proposed numbers absent from manifests/tags remain UNKNOWN. Derive conditional evidence is separately recorded in `actual-maincheckcodec-derive-impact.md`.

## redb owner discovery

At 2026-11-05T22:13:40Z, the enabled GitHub repository search was queried narrowly for `redb user:LiGoldragon`. Search returned exact `LiGoldragon/redb`; `github_get_repo` at 22:13:48Z returned owner `LiGoldragon`, public, default branch `master`, permissions admin/maintain/pull/push/triage, clone URL `https://github.com/LiGoldragon/redb.git`. Verbatim supported get-repository connector result, including returned owner/permissions, is in `current-reservation-redb-github-receipt.json`; the earlier `.txt` is a summary, not the raw receipt. Catalogue visibility is limited to the authenticated accessible catalogue/search result; it does not establish that all owner repositories or private/unlisted owner ledgers were checked. This is supported owner-namespace evidence, not publication/allocation approval. A read-only `ls-remote` receipt at 22:13:56Z is `current-reservation-redb.ls-remote.txt`; it reports `master` at `f8e955a...` and no `flow-052-opening` ref. Therefore owned repository exists, but requested fork ref is unallocated/UNKNOWN; no ref was created or pushed.

## Collision and limits

No candidate is cleared by “not seen.” Existing remote branch/tag names and the stale 342 capture are collision evidence only; no automatic bump or substitute coordinate is authorized. Memory labels were not remotely checked and remain UNKNOWN. The four prep worktrees remain preparation-only under locks 25611–14. No all-owner ledger was found. Exact missing input for final allocation is the authoritative current reservation/owner ledger (or explicit owner confirmations) for each requested package/version and all four Memory coordinates, and the approved redb fork ref. Pinned derive-source check in `codec-derive-impact.md` finds no Budget construction or datom_form call in expansion; Budget field additions leave generated &mut Budget signatures unchanged. No derive source delta is currently required by the approved codec surface; any later observed expansion delta requires its own explicit conditional allocation.
1ee5ee8270b11a53a25d607ba2954d8d803f3be3e08cdb1fe298dd8f92b34fb0  /home/li/primary/flows/e60c75/reports/current-reservation-datom-codec.ls-remote.txt
56a4e394e67c0ac1854bc53c3e90ea47b3936ce4c46e591befc6378ce5bd07b5  /home/li/primary/flows/e60c75/reports/current-reservation-flow.ls-remote.txt
ca6b90fa7f92bd826f0cb99e278472801b2d62733a9c2ed661683ac80f6d494d  /home/li/primary/flows/e60c75/reports/current-reservation-meta-signal-flow.ls-remote.txt
333200daba1a2bc18d2ef5777b5912b505d39bd9b7044646f225684933cc14ea  /home/li/primary/flows/e60c75/reports/current-reservation-protos.ls-remote.txt
9edc3bc37ba6e336af4f3b6dafad8cb16f6eaa1fb641565ae5d16d7db954abc2  /home/li/primary/flows/e60c75/reports/current-reservation-redb.ls-remote.txt
fbde559d6cfc213e3bc3f877d7d5a037d3ca3ab94ec2e35381b2a4d5aad0ad97  /home/li/primary/flows/e60c75/reports/current-reservation-sema-engine.ls-remote.txt
1dc15cadfaccb07ec6f5c5bd89448fa22d53c41dd292530739d0f15967f786c6  /home/li/primary/flows/e60c75/reports/current-reservation-sema.ls-remote.txt
2a6c0a2a7d53ed5335f54642b5175ce75aaca153d769963cc66a6d0685e78b94  /home/li/primary/flows/e60c75/reports/current-reservation-signal-flow.ls-remote.txt
abd66410a03b962f900e2a9444289936706ed724411d91f38d1b827b06b51b90  /home/li/primary/flows/e60c75/reports/current-reservation-redb-github-receipt.json
9b591b45bee2d728d2284d8902dd0cc5d2ec30c3801990664ae3bd06473006ab  /home/li/primary/flows/e60c75/reports/actual-maincheckcodec-derive-impact.md

## Exact package-name boundary and reservation limitation

The prepared immutable dependency packages remain sema/sema-engine at their exact old revisions. Current remote main manifests in those repositories name memory/memory-engine. This is an observed name divergence, not authorization to rename the chosen baseline, repin to main, or allocate either package namespace. Primary/Core must make the final package/revision coordinate explicit. Current checks cover the listed remote heads/tags and selected manifested commits; private/unpublished reservations and all-owner claims remain UNKNOWN. No namespace is declared free.
