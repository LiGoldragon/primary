# C2 workspace cleanup classification B — 2026-07-28

## Scope and boundary

Read-only classification of the 19 C2 paths named in
`recovery-map-2026-07-28.md`. No workspace was updated, snapshotted,
concluded, removed, pruned, claimed, fetched, committed, pushed, or otherwise
mutated. No bead command was run.

The classifications answer whether the *physical workspace* has a demonstrated
successor, not whether the underlying component or feature can be retired.
`Likely cleanup-eligible after approval` therefore means only that its empty
workspace may be concluded or removed later through the owner lifecycle, after
the C3/O4 gates. It never authorizes direct filesystem deletion.

All cleanliness observations used `jj status --ignore-working-copy`; all 19
reported no working-copy changes. The current working-copy change is an empty
change in every case. Parent-change ancestry was checked against the canonical
repository's local `main` (or `master` for Pi). The normal repositories' local
`main`, `main@git`, and `main@origin` matched at the observation point; this is
only last locally known remote state because no fetch occurred. The Pi
repository has no `main`: local `master`, `master@git`, and `master@origin`
matched, while `master@upstream` is a different commit.

“No unique artifacts” means no untracked or ignored non-metadata file was
found by comparing the physical tree with `jj file list -r @`, excluding `.jj`.
Tracked `.beads`, documentation, and reports are revision content, not
workspace-only material. This does not establish that a remote still holds any
last-known remote bookmark.

## Summary

| Classification | Count |
| --- | ---: |
| Preserve | 4 |
| Needs owner decision | 5 |
| Likely cleanup-eligible after approval | 10 |
| Unknown | 0 |

The four preserved paths contain unlanded deployment, migration, or test-stack
evidence. Five need an owner because their parent is not a canonical-main
ancestor (or Pi has no `main` successor); two of those also retain ignored,
rebuildable `node_modules` trees. The ten eligible-in-principle paths have a
canonical-main ancestor and no workspace-only material, but C3 still requires
an approved owner disposition and the controlled Orchestrate lifecycle witness
(O4) before reclamation.

## Per-workspace evidence

`Main successor` is affirmative only where the exact parent change ID is an
ancestor of the named canonical `main`. “Remote branch only” is durable
last-known remote retention of the parent branch, not proof that it landed on
canonical main.

| Physical path / Jujutsu workspace | Canonical repo; current / parent | Main successor and remote uncertainty | Artifacts, likely owner, retention value | Classification |
| --- | --- | --- | --- | --- |
| `/git/github.com/LiGoldragon/CriomOS-listener-criome-recovery` / `CriomOSListenerCriomeRecovery` | `CriomOS`; empty `nzopusol`; `xttzzykw` `d0030c66` “preserve criome configuration compatibility” | Yes: `xttzzykw` is an ancestor of aligned local `main` `smwxlmrl` `475bf5c2`. No fetch. | No unique artifacts. Likely owner: `li` (parent author). Recovery implementation is retained on canonical main; low workspace retention. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/CriomOS-spirit-domain-all` / `CriomOS-spirit-domain-all` | `CriomOS`; empty `vtkmppko`; `ksqpktzr` `f0fed0b7` “pin fixed Spirit v11 migration stack” | No canonical-main successor. Last-known remote branch `primary-2v5c.19-criomos-spirit-v11@origin` names this exact parent; no fetch. | No unique files, but the parent is the retained fixed deployment-stack pin. Likely owner: `li` / `primary-2v5c.19`. High retention. | Preserve |
| `/git/github.com/LiGoldragon/CriomOS-spirit-judge-deploy` / `CriomOS-spirit-judge-deploy` | `CriomOS`; empty `uvrrwzvo`; `xsupspmo` `1a6716b2` “retain remote judge chain evidence” | No canonical-main successor; no parent bookmark supplies a landing witness. No fetch. | No unique files, but parent changes the remote judge pin-chain check, cutover document, flake inputs, and lock. Likely owner: `li`. High deployment-evidence retention. | Preserve |
| `/git/github.com/LiGoldragon/CriomOS-home-laptop-colemak-merge` / same | `CriomOS-home`; empty `zytsmxqn`; `wunqwlsz` `329c93ec` “use keyd-owned laptop Colemak layout” | Yes: parent is an ancestor of aligned local `main` `wruxtovz` `f694b8ec`. No fetch. | No unique artifacts. Likely owner: `li`. Canonical main retains the configuration; low workspace retention. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/CriomOS-home-listener-criome-recovery` / `CriomOSHomeListenerCriomeRecovery` | `CriomOS-home`; empty `tzqnuukn` (workspace description: listener recovery); `lnuzyusl` `0347e395` “deploy bounded listener history” | Yes: parent is an ancestor of aligned local main. `ListenerHistoryRetentionHome*` is a locally conflicted bookmark, so its remote truth is not fresh. | No unique artifacts. Likely owner: `li` / Listener-history lane. The durable successor is canonical main, but recovery semantics warrant owner approval. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/CriomOS-home-listener-zddv4` / same | `CriomOS-home`; empty `wlzyvoxw`; `wvqvvuvk` `40641750` “wire Listener cancel shortcut” | Yes: parent is an ancestor of aligned local main. No fetch. | No unique artifacts. Likely owner: `li`. Canonical main retains the shortcut; low workspace retention. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/CriomOS-home-spirit-domain-all` / same | `CriomOS-home`; empty `ktuvtsxp`; `tzttolnr` `8cc609eb` “require remote Spirit deployment check execution” | No canonical-main successor. Last-known `spirit-judge-source-ready-home-20260710@origin` names the exact parent; no fetch. | No unique files, but parent is a deployment-check witness. Likely owner: `li` / Spirit deployment lane. High retention. | Preserve |
| `/git/github.com/LiGoldragon/CriomOS-test-cluster-spirit-domain-all` / same | `CriomOS-test-cluster`; empty `wmxwqosz`; `loqnzslr` `80d78b1f` “repin fixed Spirit v13 stack” | No canonical-main successor. Last-known `primary-2v5c.19-test-cluster-spirit-v11@origin` names the exact parent; no fetch. | No unique files, but the parent is a reproducible test-stack pin. Likely owner: `li` / `primary-2v5c.19`. High retention. | Preserve |
| `/git/github.com/LiGoldragon/lojix-inspect-store` / same | `lojix`; empty `nlyklrpr`; `pzlvswow` `ad9e273a` “add read-only store inspection” | Yes: parent is an ancestor of aligned local main `vpxlyzmt` `9adc6c75`, whose description is the later schema-one store migration. No fetch. | No unique artifacts. Likely owner: `li`. The inspection facility is on canonical main, so the separate empty workspace has low retention, subject to the still-unresolved O5 scope. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-mind-mind-judge-diagnostic` / same | `meta-signal-mind`; empty `qnrvlsmz` with diagnostic description; `snmvupky` `ee3afc10` architecture-doc change | Yes: parent is an ancestor of aligned local main `ymloxzyk` `20ecb445`. No fetch. | No unique artifacts. Likely owner: `li`; workspace description is the only diagnostic marker. Low retention once the owner confirms it is no longer an active lane. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-orchestrate-session-lane-clear` / same | `meta-signal-orchestrate`; empty `rwzkytsr`; `zqrnmxzr` `ffa58da6` “add session clear lifecycle contract” | Yes: parent is an ancestor of aligned local main `pqnrsnnq` `89b57090`. No fetch. | No unique artifacts. Likely owner: `li` / session-lane contracts. Source is retained on main; controlled lifecycle evidence under O4 still gates reclamation. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/mind-domain-all-repin` / same | `mind`; empty `nrlzkpvv`; `sqspvmrt` `845bb066` “repin migrated signal domain dependencies” | Yes: parent is an ancestor of aligned local main `wqqsysxr` `042550a0`. No fetch. | No unique artifacts. Likely owner: `li` / Mind dependency lane. Low workspace retention; underlying Mind deployment work is separate. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/orchestrate-session-lane-storage` / `session-lane-storage-migration` | `orchestrate`; empty `zyntqzyq`; `ummxznpw` `85af532f` “implement meta session lane lifecycle” | Yes: parent is an ancestor of aligned local main `qmtroomk` `83e09a13`. No fetch. | No unique artifacts. Likely owner: `li` / session-lane lifecycle. O4/C3 specifically require a controlled registry witness before any conclusion. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/orchestrate-writer-ordering` / same | `orchestrate`; empty `knvmxpvl`; `wymukxkw` `ddc1c8b6` “validate writer configuration before directory creation” | Yes: parent is an ancestor of aligned local main `qmtroomk` `83e09a13`. No fetch. | No unique artifacts. Likely owner: `li`. Code is retained on main; O4/C3 remain mandatory for workspace lifecycle. | Likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-domain-schema-dotted-syntax-pilot` / same | `signal-domain`; empty `luvxkpxs`; `lszolltz` `36ba3904` “migrate schema generics to dotted syntax” | No canonical-main successor. Last-known `signal-domain-dotted-syntax-pilot@origin` names the exact parent; no fetch. | No unique files, but parent changes schema, generated Rust, and Cargo metadata. Likely owner: `li` / dotted-syntax pilot. Material comparison/disposition is still required. | Needs owner decision |
| `/git/github.com/LiGoldragon/spirit-judge-hardening` / same | `spirit-judge`; empty `zuyylmxk`; `kmvkqwws` `f845fccb` “Remove bootstrap-only AGENTS pointer” | No canonical-main successor and no named remote bookmark at the parent. No fetch. | No unique files; parent deletes `AGENTS.md`. Likely owner: `li` / implementation worker provenance. Even a small unlanded deletion needs explicit disposition. | Needs owner decision |
| `/git/github.com/LiGoldragon/pi-subagents-nested-roles-preference-training` / same | `pi-subagents`; empty `xvroltxr`; `lxxolqty` `afde0f1f` “fail closed generated role policy” | No canonical `main`; parent is not an ancestor of canonical `master`. Last-known same-named branch is at `origin`; no fetch, and upstream differs. | Ignored `node_modules` only (17,777 files, about 187 MiB); substantive parent changes policy, code, docs, and tests. Likely owner: `li` / named training branch. | Needs owner decision |
| `/git/github.com/LiGoldragon/pi-subagents-nicobailon-closeout` / same | `pi-subagents`; empty `yzxkkmxo` with `approved-fork-integration` description; `qrwwpxwl` `fa93ed64` “Merge pull request #1 … forward-port” | No canonical `main`; parent is not an ancestor of local `master`. The merge message alone is not a local successor witness. No fetch. | No unique artifacts. Likely owner: Li Goldragon / approved-fork lane. Moderate retention until the canonical fork/branch disposition is established. | Needs owner decision |
| `/git/github.com/LiGoldragon/pi-subagents-nicobailon-optional-list-consistency` / `OptionalListConsistency` | `pi-subagents`; empty `wrkywqpk`; `lqkopuru` `3633afc3` “make listing optional for known roles” | No canonical `main`; parent is not an ancestor of local `master`. Last-known `preserve/pisubagents-acceptance-20260716@origin` retains it; no fetch, and upstream differs. | Ignored `node_modules` only (17,777 files, about 187 MiB); parent changes a skill, tool description, and test. Likely owner: `li` / preserve branch. | Needs owner decision |

## Safest three candidates for a later approved lifecycle conclusion

These are not deletion instructions. They are the strongest cases for a
future owner-approved C3 conclusion because the exact parent is incorporated
in canonical main, current workspace is empty and clean, and no unique
artifacts were found.

1. `/git/github.com/LiGoldragon/CriomOS-home-laptop-colemak-merge` — parent
   `wunqwlsz` is an ancestor of aligned `CriomOS-home` main; no artifacts or
   active workspace description remain.
2. `/git/github.com/LiGoldragon/lojix-inspect-store` — parent `pzlvswow` is
   an ancestor of aligned Lojix main, which now has a later store-migration
   commit; the inspection feature is retained canonically.
3. `/git/github.com/LiGoldragon/mind-domain-all-repin` — parent `sqspvmrt` is
   an ancestor of aligned Mind main; the workspace is empty with no local
   evidence beyond the already-landed dependency repin.

Before any of these is concluded or removed: obtain the owner disposition,
run the controlled O4 lifecycle witness, map the exact live registry record,
and use the owner lifecycle with a rejected conclusion unless an independently
approved landing applies.
