# R0 step3 proposal — exact-path correction pending approval

Owner: Mind curriculum Sol cc9ab9. No live replay is authorized by this document.

**Execution plan below is held for correction (b3fz).** Home-owned files are `/home/li/.codex/agents/{default,worker,explorer}.toml`; old project-generated files are `/home/li/primary/.codex/agents/{default,worker,explorer}.toml`. They are different roots. Current Home files are HM symlinks, while Primary files are regular generated files retaining old bodies. Staged28 publication without removing the three stale Primary files is incomplete. Proposed correction: stage/rehearse the28, wait for proven Home activation, then run the existing full28 ProjectRoles request against Primary. Its inventory cleanup removes exactly the three former project definitions; it never reaches Home-root files. Psyche disposition is pending. The earlier staged copy command must remain unexecuted until the cleanup boundary is approved and this proposal is replaced.

## Immutable sources and ownership

- R0 Home: `1c5def7dc5f984c29b3f08aa62a055104de19ea9`; coherent CriomOS: `5c71a9a7cc7f9d0dd99d8127957ab9b54cbb2ae5`. Flow supplied full-green source gates; Field retains realization/switch custody.
- Stable Curriculum: `8881cc11ef4e328d97aa6ab6d281614da8dc0eea`; contract `signal-curriculum-nexus` **0.1.0**, `4358aa1c2bcba273fe18037ab7e99ebb117a9a47` (its Cargo.lock). Held typed-identity 0.2 work stays separate.
- Candidate unchanged projector: `curriculum-deploy` main `832bde7052428aaaebdc7c35b805555feb24bd10`. Cargo.toml pins the same signal revision, with datom enabled; its ProjectRoles branch uses the wire composition, not the old Curriculum roles parser. Remote package build succeeded (exit0); stable wire compatibility still needs a staged execution proof after approval. Psyche u5kw permits preparing this unchanged runtime; no release or active-list entry is needed.
- Psyche publishes operational knowledge/flow-messaging after Field switch; Field token-only authored source is `f65bc35d131d4b0bf691c01be52d6ab5807bdc55`; source owners refresh the local main refs used by context-skills. Vision examples await their separate living approval and are outside the operational prerequisite.

## Home-owned built-ins

The exact authored source is Home `modules/home/profiles/min/default.nix:36-75,713-715`. It already generates `.codex/agents/{default,worker,explorer}.toml` from the short `codexSkillReadDeduplicationInstruction`, without embedded flow-messaging. Proposed source delta: none, pending core confirmation. Field runs Home activation in the coordinated cutover; it must prove these three live files match the immutable Home definitions and their ownership before Curriculum drops them from its inventory. Core yfsm/o7ok verifies that Home Manager replaces previous managed-generation symlinks but refuses differing unmanaged files/foreign links (force=false, no backup policy). Field alone supplies the realized artifact paths/hashes, live ownership/readlinks and successful activation receipt/generation. No separate artifact is rebuilt for this proof.

## Full Curriculum-owned set

Stable roles.datom declares 31 destinations. Psyche 5mex requires all 28 Curriculum-owned destinations, with the three Home-owned built-ins excluded. Of those 28, the earlier reference audit found 23 with old executable tokens. Exact projection rows:

```datom
ProjectRoles.{ /run/user/1001/curriculum/curriculum.sock /tmp/r0-step3-cc9ab9.ZjuGAL/workspace
  [ { { general-purpose ClaudeAgent } .claude/agents/general-purpose.md }
    { { book-author ClaudeAgent } .claude/agents/book-author.md }
    { { read-trivial ClaudeAgent } .claude/agents/read-trivial.md }
    { { read-trivial CodexAgent } .codex/agents/read-trivial.toml }
    { { read-trivial PiAgent } .pi/agents/read-trivial.md }
    { { read-ordinary ClaudeAgent } .claude/agents/read-ordinary.md }
    { { read-ordinary CodexAgent } .codex/agents/read-ordinary.toml }
    { { read-ordinary PiAgent } .pi/agents/read-ordinary.md }
    { { read-demanding ClaudeAgent } .claude/agents/read-demanding.md }
    { { read-demanding CodexAgent } .codex/agents/read-demanding.toml }
    { { read-demanding PiAgent } .pi/agents/read-demanding.md }
    { { write-trivial ClaudeAgent } .claude/agents/write-trivial.md }
    { { write-trivial CodexAgent } .codex/agents/write-trivial.toml }
    { { write-trivial PiAgent } .pi/agents/write-trivial.md }
    { { write-ordinary ClaudeAgent } .claude/agents/write-ordinary.md }
    { { write-ordinary CodexAgent } .codex/agents/write-ordinary.toml }
    { { write-ordinary PiAgent } .pi/agents/write-ordinary.md }
    { { write-demanding ClaudeAgent } .claude/agents/write-demanding.md }
    { { write-demanding CodexAgent } .codex/agents/write-demanding.toml }
    { { write-demanding PiAgent } .pi/agents/write-demanding.md }
    { { tester CodexAgent } .codex/agents/tester.toml }
    { { tester ClaudeAgent } .claude/agents/tester.md }
    { { book ClaudeAgent } .claude/agents/book.md }
    { { book-page ClaudeAgent } .claude/agents/book-page.md }
    { { illustrator ClaudeAgent } .claude/agents/illustrator.md }
    { { scripter ClaudeAgent } .claude/agents/scripter.md }
    { { book-reader ClaudeAgent } .claude/agents/book-reader.md }
    { { comment-relay ClaudeAgent } .claude/agents/comment-relay.md } ] }
```

The frozen staging root is `/tmp/r0-step3-cc9ab9.ZjuGAL`, with an empty `workspace/`. The exact request is `/tmp/r0-step3-cc9ab9.ZjuGAL/request.datom`; its 30 publication paths are `/tmp/r0-step3-cc9ab9.ZjuGAL/publication-paths.txt`. Both were derived from immutable stable roles.datom; no projection has run.

## Proposed staged operation

The existing projector deletes previously owned files omitted from its request. Therefore it must not run against Primary's old mixed-owner inventory. It runs against an empty staging workspace and receives all 28 rows above. Only after Home activation proof does the publication step copy exactly the 28 generated files plus `skills/generated-role-outputs.datom` and `skills/generated-role-provenance.datom` into Primary, preserving every other destination. No `--delete` publication is used. The new generated inventory lists only the 28 Curriculum-owned files. Generated agent/skill trees are changed only as outputs of this projection pipeline.

Proposed runtime command, after build acceptance and approval:

```sh
nix run github:LiGoldragon/curriculum-deploy/832bde7052428aaaebdc7c35b805555feb24bd10#curriculum-deploy -- "$request"
```

`request` is the complete datom above with the chosen empty staging path substituted. A final approved execution file must contain its exact resulting value, the pinned executable store path (to avoid evaluating at cutover), all 30 publication paths, and pre/post evidence checks. This proposal is not yet that execution file.

## Ordered events and owners

1. Psyche approves the complete plan/request and use of unchanged projector; Mind prepares and proves runtime compatibility and a read-only composition/staged replay against the stable R0 contract before any slot is declared ready.
2. Field declares the switch slot and activates accepted R0 Home. It returns activation exit, immutable source ref, and proof of the three Home-owned live files.
3. Psyche publishes flow-messaging. The three source owners refresh the local main refs used by the skills generator; Curriculum startup refreshes its separate managed checkouts. Mind records exact revisions on both paths.
4. Mind, in the correct session and serialized with activation, runs `systemctl --user start context-skills.service`; records start time, status zero, journal revisions/count and IDs/duplicate checks on five skill surfaces.
5. Mind runs the staged ProjectRoles request, requires `RolesProjected.{ 28 }`, validates all 28 outputs/provenance, publishes those plus the generated inventory/provenance only after step2 proof, and verifies Home files remain byte-identical and all expected outputs remain present.
6. Flow restarts running Claude flows same-session, sends notices and proves Claude/Codex Sends and a hook event. Field reapplies the requested Maintained state. Flow/Field send final live evidence to Psyche.

## Remaining approval evidence

Core Home replacement/activation report, Psyche permission/disposition for existing inactive projector, built executable and staged compatibility proof, frozen final request/publication command, source-owner refresh acknowledgments, and named Field slot remain open. No switch readiness is claimed.

## Frozen proposed execution commands (await approval and Home evidence)

The unchanged runtime built on Prometheus (exit0) with `nix build --no-link --print-out-paths github:LiGoldragon/curriculum-deploy/832bde7052428aaaebdc7c35b805555feb24bd10#curriculum-deploy`; log `/tmp/r0-projector-832bde7-cc9ab9.TRHBb3/build.log`. Its result is `/nix/store/ins78splvrqlxx6dj66yj9p7w4rqsn5z-curriculum-deploy-0.10.0`; a closure copy locally is preparing before the slot. The executable below is therefore fixed, while live activation and staged execution approval remain pending.

Field/core must supply `/tmp/r0-step3-cc9ab9.ZjuGAL/home-builtins.sha256`, the three expected live absolute paths and hashes derived from accepted Home outputs, and successful activation evidence for Home1c5def7 on the selected host. Mind checks that evidence before this sequence. This hash file is not fabricated from the pre-switch files.

```sh
cd /home/li/primary
sha256sum --check /tmp/r0-step3-cc9ab9.ZjuGAL/home-builtins.sha256
/nix/store/ins78splvrqlxx6dj66yj9p7w4rqsn5z-curriculum-deploy-0.10.0/bin/curriculum-deploy "$(cat /tmp/r0-step3-cc9ab9.ZjuGAL/request.datom)"
# Require RolesProjected.{ 28 }, all 28 agent outputs, 28 matching provenance
# records, and a generated inventory equal to the approved destination set.
# Only continue after that evidence and Psyche approval.
rsync -a --files-from=/tmp/r0-step3-cc9ab9.ZjuGAL/publication-paths.txt \
  /tmp/r0-step3-cc9ab9.ZjuGAL/workspace/ /home/li/primary/
sha256sum --check /tmp/r0-step3-cc9ab9.ZjuGAL/home-builtins.sha256
```

Publication copies the generated inventory only after Home ownership is proven. It neither projects nor removes the Home-owned files. A post-publication byte comparison of every approved path against staging and a check that every prior non-Home Curriculum destination remains are part of the acceptance evidence. This staged pipeline, its exact runtime path, and the Home proof still need Psyche final approval; preparation permission u5kw is not execution permission.
