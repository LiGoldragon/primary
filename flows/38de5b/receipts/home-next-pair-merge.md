# Home next pair (Flow/Message 0.16) onto the next-deploy Home line — 2026-09-26

Subflow of 38de5b. W = witnessed here. Nothing deployed; no CriomOS pin changed; no Lojix request.

## Line chosen: CriomOS-home `integration-2-b860be` (not `integration-2-da88cf`)

Remote heads read with `git ls-remote` before the change (W):

| Repo | Bookmark | Rev | criomos-home pin |
|---|---|---|---|
| CriomOS | integration-2-b860be | 78121a03 ("pin Piper-free Home and Lojix 8.1.0") | Home 7e96dcf5 |
| CriomOS | integration-2-da88cf | fd0be3f0 | Home 98255d10 |
| CriomOS | bootstrap-b860be | dfb2c89c (deployments 35/36/37) | Home 7e96dcf5 |
| CriomOS-home | integration-2-b860be | 7e96dcf5 (Piper removal) | — |
| CriomOS-home | integration-2-da88cf | 8a60835c (Flow/message 0.14 pin) | — |
| CriomOS-home | flow-message-next-e167d8 | f35913c1 | — |

Ancestry (W, `git merge-base --is-ancestor`):
- Home: 8a60835c (da88cf) < 7e96dcf5 (b860be) < f35913c1. b860be's line already contains da88cf's (merge 5ed097a1); the lines have NOT diverged.
- CriomOS: fd0be3f0 (da88cf) is an ancestor of 78121a03 (b860be).

So the brief's expectation (da88cf's line is the successor) is reversed: b860be's Home line is the successor, and it is the Home that both the bootstrap already deployed (dfb2c89c, deployment 37 Realize Succeeded, receipt flows/b860be/receipts/lojix-35-37-2026-09-26.md) and CriomOS integration-2-b860be (the step-2 deploy after the Piper removal) pin. Mind Sol 00f95a's ruling in b860be's log also puts step-2 Home pins on integration-2-b860be. No third line was created: f35913c1 is a direct child of 7e96dcf5, so the "merge" is a fast-forward.

## Review of f35913c1 against 7e96dcf5 (W)

- Files: UPGRADES.md, checks/flow-message-next, flake.nix (+flow-next 9aa9bf88, +message-next f1843dba, +check), flake.lock, lib/stable-next-service.nix, modules/home/default.nix (+import), profiles/min/flow-message-next.nix.
- Lock: resolved per-root-input comparison differs only in the two new inputs flow-next and message-next; every existing input (flow, message, crane, fenix, ...) resolves identically (renumbered node names only).

## Checks on Prometheus (evaluation on ouranos, max-jobs 0, builders @/etc/nix/machines)

- `nix build path:<home>#checks.x86_64-linux.flow-message-next --override-input system path:/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/system` → `/nix/store/8mdzlxbdsqigk9g8gsva4ns87l6k75v9-flow-message-next` (drv 3d6c4kar…). The output was already realized (ultimate=false, registered 21 min earlier, i.e. from e167d8's identical-drv build); no fresh build line in this run, so the remote-build evidence is e167d8's, not mine. `--rebuild` is refused under max-jobs 0.
- Whole `nix flake check` of Home was not run: known pre-existing Blueprint failures (00f95a, da88cf reports); the named check was built instead.
- Ouranos home generation, CriomOS 78121a03 with transient `--override-input criomos-home github:LiGoldragon/CriomOS-home/<rev>` and the Lojix complete-host generated inputs (horizon, system, deployment, secrets):
  - before 7e96dcf5: drv zg2djngc… → `/nix/store/fh7fqv243as1pgw7rdypcssfp3a04jjr-home-manager-generation` (equals the bootstrap Home 31147a built — confirms same Home).
  - after f35913c1: drv aq6sc1cd… → `/nix/store/0qxxx3j5jdxsm97r3ia5008ad1bnp9rn-home-manager-generation` (already realized, ultimate=false; no fresh build lines).
- Generation diff (W): user units add only flow-configuration-next, flow-nexus-next, message-nexus-next; every shared unit file is byte-identical (cmp); bin adds only flow-next, flow-next-meta, message-next, message-next-meta; flow, flow-meta, flow-nexus, message, message-meta, message-nexus resolve to the same store paths.

## Landed (W)

- `git push --force-with-lease=integration-2-b860be:7e96dcf5 origin f35913c1:refs/heads/integration-2-b860be` → 7e96dcf..f35913c (fast-forward). `git ls-remote`: integration-2-b860be = f35913c1c34fb44746e1ad1de4e83c343ecd9ab5. integration-2-da88cf unchanged at 8a60835c.
- Orchestrate lock 7381 (scratch dir) acquired and released.

## Not done / owed

- CriomOS integration-2-b860be still pins Home 7e96dcf5; Field Sol b7da5d repins criomos-home to f35913c1 for the post-Piper ouranos deploy.
- Not witnessed live: next units starting, Deliver through next Flow.
