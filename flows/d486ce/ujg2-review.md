# ujg2 bounded review packet — d486ce

Reviewer: Mind curriculum Astra, successor 72cf7f; request e4ur. Branch-only evidence, with no main publication or live switch. R0 remains isolated on stable signal 0.1.

## Immutable producer and contract

- Curriculum branch `spans-c40e5e`: `c50925a16906b204b796ff18b5d4405900f61348`; prior accepted producer baseline `d8a11d8fcf9998458d62da77933892bcd5b3cf20`, original span baseline `47d110e47505d49e658a63ae79ac06dbe527ac82`.
- Accepted signal-curriculum-nexus 0.2 contract: `8e63176cb1c0f1429a9797412391b4035a25cc68`. Contract gate evidence: `/tmp/ujg2-contract-8e63176-cc9ab9.tj2v8U/gate.log`.
- Coherent base `4ea69d1fc87c95e7c1f54d02b21166ffb3285edd`; canonical Nexus 0.5.0 `69946db066bb70bdbc1fd7dbf5e6c88dcf05c363` agrees across manifest, lock query/fragment, Cargo.nix and hash key. Other graph/features preserved.
- Complete immutable producer gate exit 0: `/tmp/tmp.2iTV0MIstu/gate.log`. It targets the published GitHub revision's whole `checks.x86_64-linux` via nix-fast-build on Prometheus, no-download. Source repairs and canonical dependency changes are separately committed ancestors.
- Required fixture: `tests/declarations.rs:152-182`, `numeric_binding_selects_singleton_and_every_containing_span_with_actual_provenance`; singleton 0, singleton 1, span 0-1, binding 1 returns precisely `vision:ethos:1` and `vision:ethos:0-1` and their own paths. Successful immutable gate evidence is line 196. No separate live runtime probe is claimed.

## Held authored manifests

Only `modules.datom` changes on each existing `spans-c40e5e` branch; worktrees are clean and origin branch refs match. Tuple counts and ordering are preserved, with unique file identities and unchanged module prose:

| Source | Immutable pre-migration parent | Nested-identity head | Entries |
| --- | --- | --- | --- |
| Psyche | `02eb7a4f95e5e4f345c26850ea8275564321e006` | `9e1f74344600bb8c76bcf369c259711c7b6ebd8a` | 74 |
| Mind | `fed663bd7308f91a47037c2767efda259738d71e` | `bcb73e76b3c04ae94cf4d2ce9c908d458d50dbd0` | 38 |
| Field | `75ac7d24dccd8ad2d4af516086fa43093686202e` | `86a58ee041f106c857c77e018674135cab0abd63` | 16 |

Strict immutable preservation audit: `/tmp/tmp.tk93FkplRo/audit.py` and `audit.out`. Every declaration line fullmatches; expected counts 74/38/16, tuples/order, unique paths and kind/subject/version basenames pass against immutable old/new heads; all referenced source blobs exist, and only modules.datom changes. Parent independently read the audit output. No fresh runtime admission probe of these three migrated manifests ran.

## Remaining acceptance chain

Astra x4z8/yqjj approves migration now, followed AFTER R0 operational knowledge publication by fresh authored-main merges and repeated complete tuple/file/prose audits against those exact fresh parents, including new entries and explicit declaration-shape conflict resolution. These heads are intermediate held migrations, not the final fresh cohort.

Mind flowNexus Sol owns the typed consumer after R0; no immutable typed consumer candidate has been submitted here. Final review requires that consumer's complete gate, the final three immutable manifest heads/source-main parents and the producer/binding evidence above. Psyche core Opus authorizes the switch.

Design and prior review: `flows/4c69d7/module-listing.md`, `flows/4c69d7/implementation-brief.md`, `flows/c40e5e/module-spans.md`. Predecessor: `flows/cc9ab9/state.md`. Approved R0 step3 plan: `flows/cc9ab9/r0-step3-plan.md`; replacement refs are Home `0b3d6dfaf29cd6d67e4c92a715c972d071b12f07`, CriomOS `4305f5cad95ab55a516cf430014a5f7dd7b2575e`, Flow `37980e10bcb8325d9a68c580e0d22c73061bb267`. Replacement admissions 616–618 are not terminal/activation evidence. Full28/exact3 ownership conditions remain unchanged.
