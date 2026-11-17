# 0v72 source packet — actual post-Energy parents

For Field core, under 5uyy revising held zaht. Source is committed in isolated worktrees; **gate, publication and runtime remain held**. Scoped Orchestrate lock **370**, owner **f35dfe**, covers only the two new worktrees. Exact acquisition echo: `/tmp/browser-f35dfe.DEQupE/lock.receipt`. No other lock/worktree/branch was altered. Field core's fresh actual receipt is `/tmp/energy-post639-parent.gJKLJhvv/receipt.txt`, 2026-11-17 00:45:49Z; it binds actual integrated Home lbi7 and system2p5x, not the stale user profile. Field core alone owns deployment and the later configuration/Fable/live comparison.

## Committed references

- Home worktree `/git/worktrees/home-handover-once-f35dfe`, branch `field/f35dfe-home-once`.
- Direct actual Home parent `39face790daf37b5949c1bf067599cbf52e56321`.
- Configuration-removal commit `a52366151c9c39d7aac241d6701becb96463aa97`, directly on that actual parent.
- Home final `3d242cd6cf3cdb93b953579af7ae2247bf3f8a79`, directly on the removal commit; only the Flow locked triple changes in this second commit.
- Consumer worktree `/git/worktrees/criomos-handover-once-f35dfe`, branch `field/f35dfe-consumer-once`.
- Consumer final `1ff53f67e40d15d3dae5e071f19f9b3b79636487`, **directly** on actual `669b38611b5cf022714fdf06953a069995503b4e`.

Both new worktrees are clean. Old clean `field/c3bedd-home-once` at1527 and `field/c3bedd-consumer-once` at667 were preserved. No main branch, remote, tag, shared source, package, account, secret, global configuration, Flow lifecycle or production harness was changed. No Nix evaluation/build/shell or heavy gate was launched. The only Nix operations were read-only store metadata and hashes of exact source archives; their baseline checks reproduce the existing Home lock hash and the already-green Flow source-store hash.

## Exact source and graph evidence

Scratch directory: `/tmp/browser-f35dfe.DEQupE`.

- `approved-removal.patch` is `git diff --binary dd56502ee0914c86e6b23bb6a95d9aaa329ac4e1 1527d33063a55670348a572fd1f7febd823fc95a`.
- `applied-removal.patch`, generated from the staged actual-parent worktree, is **byte-identical** (`cmp` exit0). The eleven resulting path blobs/modes also equal approved1527; every unrelated tree entry and Energy lock byte is unchanged.
- `home-exact.diff`: full actual39face..final Home binary diff, twelve paths total (eleven approved configuration/fixture paths plus `flake.lock`).
- `consumer-exact.diff`: full actual669..final consumer binary diff; only `flake.lock`.
- `source-audit.json`: ancestry, exact node/field differences, all-edge invariance, unrelated tree equality, hashes, clean state and locked triples.
- `normalized-flow-closure.json`, `normalized-energy-closure.json`: logical closures with arbitrary lock-node labels removed and follows edges resolved. Home and consumer closures compare equal for both Flow and Energy. All graph edges are unchanged from their actual parents; no unrelated node moved or union was introduced.
- `SHA256SUMS`: checksums of both exact diffs, both removal patches, normalized closures and machine audit. These are source receipts, not a green gate.

The first comparison attempt used unstaged `git diff`, which omits a newly added fixture and therefore failed comparison. The staged complete diff then compared identically; no source patch correction or scope expansion occurred.

### Locked triples

| Logical input | Revision | NAR hash | lastModified |
|---|---|---|---|
| New Home (consumer) | `3d242cd6cf3cdb93b953579af7ae2247bf3f8a79` | `sha256-6nOeIQjUMn2mPRMZl0goxQI7+WA9yoRC5nFsSbJRd54=` | 1794876788 |
| Flow (Home and consumer) | `61242e2dfe7db8f472e5b1d353f857d7d3bbc464` | `sha256-+FsLUAzXYyiCVrFDdL3pxSVRA/uin98Ao/c8HLUI1tA=` | 1794874604 |
| Energy (unchanged Home and consumer) | `761a9119dd78eb2020040bc897e885a378c00b95` | `sha256-MEIdz1nnlubI0CO+fcUtOySyYr3TRGcGlCqF2kRAtbY=` | 1794875707 |

Home changes exactly `nodes.flow-0550.locked.{rev,narHash,lastModified}`. Consumer changes exactly `nodes.criomos-home.locked.{rev,narHash,lastModified}` and `nodes.flow-0550.locked.{rev,narHash,lastModified}`. Every input edge, original URL and other node is byte/structure-preserved. The existing shared Flow node is necessary through `criomos-home.inputs.flow-0550`; no root direct Flow input is added. The pre-existing historical pinned original elsewhere in the graph is unchanged and outside this scope; changed input originals stay bare repository URLs.

## Proposed whole projected-Home gate — NOT RUN

The installed launcher's help was read; it supports the exact flags below. This follows the retained successful projected-Home recipe in `/tmp/b30c1b-memory-owned-config.FbPf5e/gate.log`, lines1–6, including remote evaluation, one worker,16384MiB and the exact generated-system override hash confirmed remotely by Field core. It selects the entire `checks.x86_64-linux`, including `checks/flow-memory-configuration/default.nix`; it is not a narrowed fixture-only gate.

```sh
/nix/store/hpnzk4zly83kir2gli94ai6yhm9nxw0y-nix-fast-build-2.0.4/bin/nix-fast-build --remote prometheus.goldragon.criome --no-nom --no-download --eval-workers 1 --eval-max-memory-size 16384 --max-jobs 1 --flake 'git+file:///git/worktrees/home-handover-once-f35dfe?rev=3d242cd6cf3cdb93b953579af7ae2247bf3f8a79#checks.x86_64-linux' --override-input system 'path:/tmp/offload/1541ef-generated-inputs/system?narHash=sha256-KW3DUTifDJ6m2JuYiTVtJz+9ieAgqjCb46wgrMqxJJU=' --result-file /tmp/browser-f35dfe.DEQupE/gate-results.json --result-format json
```

Proposed supervision: one foreground owned process/group, stdout+stderr retained in scratch `gate.log`, exact UTC start/end/PID/group/exit in `gate-receipt.json`, JSON results retained even on failure, and the launcher's actual remote temporary-directory cleanup receipt retained. No parallel evaluator/build or automatic source retry. Source/gate errors return to Field core for a fresh decision; no runtime switch is attempted. A local source URL is archived/copied by the retained launcher before remote evaluation; the generated `system` override must remain available on Prometheus at the exact hashed path. Any override mismatch or inaccessible source is a refusal/gap, not permission to choose another graph.

**Required next event:** Field core independently reviews these exact diffs/audit and issues the single exclusive heavy-gate event. After green and explicit publication clearance, producer Home branch must be published before consumer branch; neither is published now. Field core then owns fresh parent re-read and Lojix Evaluate → Realize → Activate, configuration/Fable identity and natural-witness proof. Lock370 remains held for this finite source/gate custody pending Field core's instruction; no model, gate, watcher, build or observer process remains running from this packet.

## Independent frwm draft

The same uninstalled draft `flows/437627/knowledge/harness-idle/0.md` includes the app-server A1–A5 third witness and bounded B1–B4 plan, documented in primary commit `da27bd524`. This does not arm B1 or any harness, app-server, nix shell or provider call. Its unverified controls remain explicit UNKNOWN. It does not expand this source/gate scope.
