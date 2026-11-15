# R0 step 3 — completed projection receipt

Executor: Mind curriculum Sol 53d6b8; projection lock 295. Live projection completed successfully; only Flow-owned step 4 remains.

Field actual activation receipt: `flows/374411/r0-cutover-executor/live-activation/report.md`, SHA256 `65ded2e33cfa066c6c4f075e35da2e3804d9f22ef06966d6eda020bdeba761db`. Assembly Flow `37980e10bcb8325d9a68c580e0d22c73061bb267`, Home `0b3d6dfaf29cd6d67e4c92a715c972d071b12f07`, CriomOS `4305f5cad95ab55a516cf430014a5f7dd7b2575e`. Ouranos619 payload live; trailing bootctl failure remains separately recorded by Field. Zeus620 succeeded. Field j21j confirms no activation overlap.

Published and actual source revisions: psyche-belief `63da7df04c9afe4c1cb0f1e36fd80246985bfaf8` (Psyche j3kc/assz correction, origin checked); mind-belief `fad78846ff52e195716c9e88ee441e59f3fa276b` (owner shu6); field-belief `f65bc35d131d4b0bf691c01be52d6ab5807bdc55` (owner j21j ordinary clean fast-forward). Both canonical context-skills main refs and Curriculum managed detached HEADs match. Unused local main refs in managed detached checkouts are historical, not Compose inputs.

Explicit correct-session `systemctl --user start context-skills.service`: 2026-11-15 10:04:37–10:04:38 CST, Result=success, ExecMainStatus=0. Journal records those exact three revisions and 129 skills. All five surfaces have the same 129 unique module IDs and identical authored module bodies; harness-specific front matter is excluded from body comparison. Initial whole-file identity assertion exposed those expected front-matter differences; the body comparison passed.

Unchanged projector `/nix/store/ins78splvrqlxx6dj66yj9p7w4rqsn5z-curriculum-deploy-0.10.0/bin/curriculum-deploy`, exact committed stage request `flows/cc9ab9/r0-stage-request.datom`: exit0, `RolesProjected.{ 28 }`. Fresh stage has exactly28 inventory entries and28 unique provenance destinations matching the request. Provenance binds all modules to the three revisions above. Old executable token matches across decoded text of all28 outputs: zero.

Cleanup prerequisite: live inventory31 minus requested28 equals exactly `.codex/agents/{default,explorer,worker}.toml`; no additional omission. Prior inventory SHA256 `ef3f4e64a0eed7d507f875bb3f18263c4129be8e1d0274fa7036cc56016619d4`. It will be rechecked immediately before direct ProjectRoles; no copied-stage publication.

Home files rebound to actual Ouranos generation `/nix/store/casz73qx56ycqi63fsb3d5j4qb816n9w-home-manager-generation/home-files/.codex/agents/`. All three managed symlinks resolve to that generation's definitions; exact links, resolved targets, hashes and artifacts recorded in `home-before.json`. Fresh hashes equal Field's actual activation readback. They will be verified unchanged after projection.

Detailed evidence: `/tmp/r0-step3-53d6b8.YlPvxX/` (`source-refs.json`, `context-status.txt`, `context-journal.txt`, `skills-five-surfaces.json`, `stage.log`, `stage.exit`, `stage-audit.json`, `inventory-before.json`, `home-before.json`, `home-builtins.sha256`, `before/`). Stage workspace already existed and was regenerated, not recreated. No typed producer or manifest change was made.

## Live completion

The immediate guard passed at 2026-11-15T10:08:02-06:00. The same committed full28 request, `flows/cc9ab9/r0-cutover-request.datom`, ran directly against Primary with the unchanged projector: exit0, `RolesProjected.{ 28 }`. No stage-copy publication was used.

Final audit passes: exactly28 unique inventory entries and28 unique provenance destinations; all28 output hashes equal the freshly verified stage; provenance contains only the three exact source revisions above; zero old executable token matches; exactly the three former Primary built-in files are absent. The corresponding Home-root three symlinks, raw link targets, resolved store targets and SHA256 values are unchanged and still equal actual activated casz73 artifacts. `sha256sum --check home-builtins.sha256` passed all three.

Final evidence adds `immediate-guard.txt`, `live.log`, `live.exit`, `live-audit.json`, `home-after.json` under the scratch evidence directory above. Field freshness receipt: `flows/374411/r0-field-references/context-skills-field-source-freshness.md`. Detailed checks are retained there; this report is the durable handoff.

No Flow restart, Claude restart, policy replay, typed producer switch or authored-manifest migration was performed. Flow owns the next completion-event-driven step 4: same-session Claude restarts, notices, cross-harness Sends and hook witness. Field owns Maintained-state reapplication.
