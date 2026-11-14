# Curriculum's Ethos move, released on ouranos

Curriculum 1b6c454 and flow 967f2f5, both on build-base 9706bad, are live on ouranos. The switch was Lojix deployment 562, which completed Succeeded. Nothing needed rolling back, and no other host was touched. I followed `/home/li/primary/flows/896bac/rmmd/release/steps.md` in order. The evidence is in `/home/li/primary/flows/2e404d/release/`, and the paths below are relative to it.

**Skills were not loaded.** This flow had no Skill tool, so knowledge:lojix and knowledge:criomos-deploy could not be loaded as the brief asked. The flow that ran the last switch (e3a7d1) had the same gap. I went ahead anyway, using its Lojix requests unchanged except for the CriomOS revision (`ouranos/*-request.datom`).

## Heads

| repo | before | after |
|---|---|---|
| CriomOS-home main | 5809dde | **d140957ea2dbfcfce77281a21231d1df6fefd607** (fast-forward) |
| CriomOS main | c521835 | **032f84ee494ae56230543199e6436291572d295d** (fast-forward) |

- The other mains were already where the brief said and were not pushed: build-base 9706bad, signal-curriculum-nexus 4358aa1, Curriculum 1b6c454, flow 967f2f5 and curriculum-deploy 832bde7 (`before/mains-before.txt`, `mains-after.txt`).
- **CriomOS-home** (branch curriculum-ethos-2e404d): `nix flake update curriculum-source flow-0550` moved exactly four lock nodes:
  - curriculum-source, e3ffb31 → 1b6c454;
  - its base, af6ab8a → 9706bad;
  - flow-0550, 40104be → 967f2f5;
  - its base, 8aa29e1 → 9706bad.
- **CriomOS**: `nix flake update criomos-home` moved criomos-home and the same four nodes beneath it. It is in the same form as c521835.
- **Home builds** on prometheus with the live inputs (`before/home-build-*.log`):
  - c521835 with Home 5809dde reproduced the live i95whysp, which confirms the build inputs.
  - Home d140957 built **pkxvlf56wj29qrqqbabcrvz5klxjp8dh**, and the relocked CriomOS 032f84e rebuilt the same path.
- **Closure difference from live** (`before/closure-diffs.txt`, `before/unit-diffs.txt`):
  - rust_curriculum (+19.5 KiB) and the flow-configured store path.
  - The curriculum-nexus unit got a new ExecStart and a new CURRICULUM_ROLES_FILE store path. The roles.datom content is byte-identical.
  - The flow-nexus and configure units changed only their package paths.

## Rollback kept (`rollback/`)

- **Lojix before:** Current was 558 (i95whysp, CriomOS c521835). The rollback request at c521835 is `rollback/lojix-ouranos-rollback-request.datom`.
- **Readbacks:** a full configuration readback and a metaflows readback were taken just before the stop (`before/configuration-before.datom`, `before/metaflows-at-stop.datom`).
- **Flow state:** Flow stopped at 02:37:11.97 with exit 0 and read inactive. The whole Nexus state directory was copied to `rollback/stopped-nexus-main/`, and its checksums match the source at the stop (`rollback/stop-state.txt`, `*.sha256`).
- **Curriculum context:** copied while Curriculum ran (`rollback/curriculum-context-copy/`). It is identical to e3a7d1's copy, and identical to the live context after the switch.

## Switch, through lojix-meta (`ouranos/`)

- **Realize, deployment 561:** Submitted → Building → Completed, Succeeded.
- **ActivateNow, deployment 562:** Submitted → Building → Copying → Activated → Completed, Succeeded.
  - Lojix now lists 562 as Current: pkxvlf56, CriomOS 032f84e, home-manager-1156.
- **Waiting:** each wait read the Lojix watcher's events line by line until the deployment's Completed event (`scripts/deploy-watched.sh`).
- **Flow downtime:** about 87 s, from 02:37:12 to 02:38:39.
- **Curriculum restart:** curriculum-nexus restarted on the new package (m1591dkv…) at 02:38:35–39, and its refresh step ran first.

## Checks after (`after/`)

- **Seats carried over.** The awake set at the stop equals the awake set after, eight flows. Each has its pane and an Active seat (`inspect-awake.datom`).
  - Mind flowNexus Opus (565bc8) is in that set but was not awake at the 02:31 snapshot. Flow woke it at 02:37:11, just before the stop, and it carried over.
  - `Queues` answers.
- **Configuration**, compared family by family (`configuration-comparison.txt`): 17 of 18 families are identical. Only Counters moved (17066 → 17073), from ordinary traffic.
  - The 02:30 recheck against e3a7d1's after-readback likewise differed only in Counters.
- **Named checks** (`named-checks.txt`):
  - 40 permaflows, with intent:scratch:0 on all 40.
  - Psyche core Fable's row is unchanged.
  - The five AskUserQuestion rows are present, and so is the Mind sourceNexus Opus row.
- **Journals** (`journal-*.txt`):
  - flow-configure-0550 replayed all ten files, each answering Configured.
  - The energy-translator re-subscribed to Flow's turn ends at 02:38:39.
  - Nothing matches error, fail, panic, refus or mismatch.
  - No user unit has failed.
- **curriculum-nexus answers.** ResolveSkills and ResolveSources over Psyche core Fable's 27 live modules match the answers from before the switch byte for byte, apart from the renamed reply head, SkillsResolved / SourcesResolved (`curriculum-resolve-comparison.txt`).
  - The old CLI (ngd353k), run against the new Nexus, answers byte-identical to before. This confirms on the live system that the wire bytes are unchanged.
- **Witness** (`witness/`): one fresh Claude flow, Field protos Sonnet, flow a9855e, launched with `Predecessors.0`. The wait was on Flow's own `Observe.TurnEnds` events (`scripts/witness-launch.sh`).
  - Its system prompt starts with the whole predicted one, followed only by Flow's identity lines. It equals the e3a7d1 witness 996539's byte for byte, apart from the Flow ID.
  - Its first prompt carries the predicted 16 modules whole and in order.
  - It answered its brief and then slept at its rest. It now reads Asleep with no seat and no pane.

## Anything off

- **The Flow test instance disappeared, cause unknown.** It was under /run/user/1001/flow-testing (a curriculum-nexus as PID 242193, a flow-nexus-daemon as PID 253731). It was listening at 02:31 and was gone by 02:38, and the journal says nothing about either PID. Unknown: whether the activation ended it, or whether it was a test run that finished on its own.
- **Not moved, by choice:**
  - CriomOS-home's `primary.inputs.curriculum` (26e14b2), which earlier Curriculum releases also left alone.
  - flow's own curriculum pin (4695835), which belongs to flow's lock and its tests.
- **The `curriculum` CLI on PATH changed** (ngd353k → sdnmyai), so its replies now print SkillsResolved / SourcesResolved. Anything that matches on the old reply names would need to change.
- **One leftover watcher, now killed.** An extra foreground Lojix watcher I started to wait on deployment 561 stayed alive after its match. I killed it; nothing else was affected.
- **Four ancient deployments still read Copying.** Lojix lists ouranos deployments 38, 46, 50 and 124 as still in Copying. They predate this work.
- **Worktrees left:** `/git/worktrees/CriomOS-home-curriculum-ethos-2e404d` and `/git/worktrees/CriomOS-curriculum-ethos-2e404d`, each equal to its main. The branches curriculum-ethos-2e404d are pushed in both repositories.
- **zeus is untouched**, still at Current 560, CriomOS c521835 (`after/zeus-untouched.txt`). Its CriomOS main has now moved past what it runs.
