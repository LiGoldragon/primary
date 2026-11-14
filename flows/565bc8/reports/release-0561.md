# Flow 0.56.1 released and switched: ouranos, then zeus

Flow 0.56.1 (the Codex wake fix) is live on ouranos with Lojix deployment 568. zeus runs its clients, deployment 570. Nothing needed rolling back. Evidence is in `/home/li/primary/flows/565bc8/release/`; paths below are relative to it. This flow had no Skill tool, so knowledge:lojix and knowledge:criomos-deploy were not loaded; the Lojix requests and scripts are the last release's (`/home/li/primary/flows/2e404d/release-orchestrate/scripts`), with only the CriomOS revision changed.

## Mains

| repository | before | main now | how |
|---|---|---|---|
| flow | 967f2f5 | **1e931e4325411ef90b0d1a045056ba4c1a336d37** (0.56.1) | fast-forward of codex-wake-565bc8 |
| CriomOS-home | 8e4ce43 | **61d67036dd0438d38aa452d00c87b3d36d02ed97** | fast-forward |
| CriomOS | 64f55ae | **a75bd6ce9b1693ff05e15fdf721f908e6e6a038b** | fast-forward |

- **flow 1e931e43** is 33986c83, 680dddb4 and 4fa6aba0 plus one commit, "Flow 0.56.1". It bumps the version where 0.56.0's commit did (`git show 40104be --stat`): Cargo.toml, the six flow crates in Cargo.lock and Cargo.nix, and flake.nix, and adds an UPGRADES.md entry that states no wire or store format change. Nothing else was merged. The 0.56.0 commit also moved flake.lock, but 0.56.1 changes no pin, so flake.lock is untouched.
- **Gate at 1e931e43:** nix-fast-build on the builder, exit 0. flow-nexus 920 passed, 0 failed, 8 ignored (933 passed with the other crates). Log: `/home/li/primary/flows/565bc8/gate-release-flow-1e931e43.log`.
- **CriomOS-home:** `nix flake update flow-0550` moved exactly one lock node, flow-0550 967f2f5 → 1e931e4. Message, energy-nexus, Orchestrate and Curriculum stay as on 8e4ce43.
- **CriomOS:** `nix flake update criomos-home` moved criomos-home and its flow-0550 node, 6 lines.
- **Gate for Home and CriomOS: the Home builds** on prometheus with the live inputs, as the last two releases did. CriomOS-home's own checks are known not to evaluate on this base.
  - Baselines reproduce the live generations: ouranos c7hjhgav (CriomOS 64f55ae with Home 8e4ce43) and zeus baaa2p5f (`before/home-build-*-baseline-*.log`).
  - New Home, built with overrides before any push to main: ouranos **s9h33z07kk58si344df0c2r2d1j32svw**, zeus **dhsp58b4jvahqh6c65va7s4q059j20r0** (`before/home-build-*-new-*.log`).
  - The pushed CriomOS a75bd6c, with no override, rebuilt the same two paths (`before/home-build-*-a75bd6c.log`).
  - Closure diff against live, on both hosts: `flow-configured: 0.56.0 → 0.56.1` and nothing else (`before/closure-diffs.txt`).

## Lojix generations

| host | Realize | ActivateNow | Current now |
|---|---|---|---|
| ouranos | 567 Succeeded | **568** Succeeded | s9h33z07, CriomOS a75bd6c (was 564, c7hjhgav, CriomOS 64f55ae) |
| zeus | 569 Succeeded | **570** Succeeded | dhsp58b4, CriomOS a75bd6c (was 566, baaa2p5f, CriomOS 64f55ae) |

## Rollback kept before the switch (`rollback/`)

- Lojix rollback requests at CriomOS 64f55ae: `rollback/lojix-ouranos-rollback-request.datom` and `rollback/lojix-zeus-rollback-request.datom`. They are the same requests as the activate ones with the old revision.
- Configuration, Metaflows, Queues and the herdr list read at the stop: `before/*-at-stop.*`.
- flow-nexus-0550.service stopped at 04:38:18 and the whole Nexus state directory (255 MB, flow.sema with it) was copied to `rollback/stopped-nexus-main/`. Every file's sha256 at the source, at the stop and in the copy is equal (`rollback/source-at-stop.sha256`, `stopped-nexus-main.sha256`, `source-after-copy.sha256`, `stop-state.txt`).
- The Curriculum context was copied (`rollback/curriculum-context-copy/`). Curriculum was not restarted by this switch.
- Flow was stopped from 04:38:18 and started at 04:39:50, down about 92 seconds. The store format is unchanged, so 0.56.0 also opens the store as it is now.

## Verification on ouranos (`after/`)

- **Version and unit:** flow-nexus 0.56.1, running `ifyrz7vl…-flow-configured-0.56.1` (PID 571605). flow-configure-0550 and curriculum-nexus are active. No user unit has failed (`after/failed-after.txt`).
- **Seats carried over:** the seven flows awake at the stop are Awake after, the same set (`before/awake-at-stop.txt` equals `after/awake-after.txt`). herdr's agent list is identical before and after.
- **Configuration:** all 18 families equal the readback taken at the stop (`after/configuration-comparison.txt`).
- **Journals:** `after/journal-flow.txt`, `journal-flow-to-now.txt` and `journal-configure.txt` hold nothing matching error, fail, panic, refus, mismatch, woke or "not recorded Awake".
- **Send round trip:** `Send.{ { Mind flowNexus Opus } Soft.Notice … }` answered `Sent.3af2`, and the journal shows it admitted at 1794652803 (`after/send-roundtrip.txt`, `queues-after.datom`).
- **Codex wake not exercised:** no Codex wake occurred between 04:39:50 and 04:49, so the fix is verified by its tests, the gate and the capsule and not yet by a live wake. The journal is the place to watch for "woke but is not recorded Awake", which should no longer appear for a Codex wake.
- No witness flows were launched. The Home change moves only flow-configured; the composition of the first prompts is unchanged.

## zeus (`zeus/`)

- Before: Home baaa2p5f, flow clients 0.56.0, no failed user units.
- After: home-manager profile dhsp58b4; `flow-nexus` and `flow-nexus-meta` resolve to `ifyrz7vl…-flow-configured-0.56.1`, the same package as ouranos; `flow-nexus --version` answers 0.56.1; no failed user unit (`zeus/after.txt`). zeus has no Nexus, so no Send was tried there.

## Anything that did not go as planned

- Nothing failed. A shell of mine was killed by a `pkill` I ran against my own wait loop; it affected nothing deployed.
- The unit and wrapper names still say 0550 and 0.55.0 while running 0.56.1, as before (a Home change outside this release).
- The zeus flow-nexus-0550 stub unit (unconditional MemoryMax block outside the AgentStack gate, chi4) is not fixed here.
- Not done, as the brief says: the capsule was not rerun; scenario 5 is the known ordering race. The Emission branch emission-565bc8 still waits to be rebased onto 1e931e4.
- Worktrees left: `/git/worktrees/flow-codex-wake-565bc8`, `/git/worktrees/CriomOS-home-codex-wake-565bc8` and `/git/worktrees/CriomOS-codex-wake-565bc8`, each equal to its main. Branches `codex-wake-release-565bc8` are pushed in CriomOS-home and CriomOS.
