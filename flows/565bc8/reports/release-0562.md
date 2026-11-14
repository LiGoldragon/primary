# Flow 0.56.2 (the Emission step) released and switched: ouranos, then zeus

Flow 0.56.2 is live on ouranos with Lojix deployment 572 and on zeus with deployment 574 (clients only). Nothing needed rolling back. Evidence is in `/home/li/primary/flows/565bc8/release-0562/`; paths below are relative to it. The procedure is the 0.56.1 release's (`/home/li/primary/flows/565bc8/reports/release-0561.md`), with its scripts copied into `scripts/` and only the revisions and paths changed. This flow had no Skill tool, so knowledge:lojix and knowledge:criomos-deploy were not loaded.

## Mains

| repository | before | main now | how |
|---|---|---|---|
| flow | 1e931e43 | **eabddc8d29ddd30b4665065cec4bee57ea7410ce** (0.56.2) | fast-forward of emission-565bc8-b 0d39641b plus the release commit |
| CriomOS-home | 61d67036 | **20d46eda079771586c610d6e55df074a3fafecf1** | fast-forward |
| CriomOS | a75bd6ce | **63e95f132bcd2812c409c7a4d07dbc55e921334b** | fast-forward |

- **flow eabddc8d** is the seven Emission commits plus one: "Flow 0.56.2". It bumps the version where 0.56.1's commit did: Cargo.toml, the six flow crates in Cargo.lock and Cargo.nix, and flake.nix. UPGRADES.md has the entry, stating no wire, store or behaviour change. No pin moved, so flake.lock is untouched. Worktree `/git/worktrees/flow-emission-565bc8-b`, branch `release-0562-565bc8`, pushed.
- **Gate at eabddc8d:** nix-fast-build on the builder (prometheus), exit 0. flow-nexus 920 passed, 0 failed, 8 ignored, the same counts as 0.56.1. Log: `gate-eabddc8d.log`.
- **CriomOS-home:** `nix flake update flow-0550` moved exactly one lock node, flow-0550 1e931e4 to eabddc8. Branch `emission-release-565bc8`.
- **CriomOS:** `nix flake update criomos-home` moved criomos-home and its flow-0550 node, 6 lines.
- **Gate for Home and CriomOS: the Home builds** on prometheus with the live inputs, as the last releases did.
  - Baselines reproduce the live generations: ouranos s9h33z07 and zeus dhsp58b4 (`before/home-build-*-baseline-*.log`).
  - New Home, built with overrides before any push to main: ouranos **rpvdvc5sx49w4nmsy0n2fa7yghk4k5wp**, zeus **24459mp92nxni7vvys9j5ms7a9miqkkn** (`before/home-build-*-new-*.log`).
  - The pushed CriomOS 63e95f1, with no override, rebuilt the same two paths (`before/home-build-*-63e95f1*.log`).
  - Closure diff against live, on both hosts: `flow-configured: 0.56.1 to 0.56.2` and nothing else (`before/closure-diffs.txt`).

## Lojix generations

| host | Realize | ActivateNow | Current now |
|---|---|---|---|
| ouranos | 571 Succeeded | **572** Succeeded | rpvdvc5s, CriomOS 63e95f1 (was 568, s9h33z07, a75bd6c) |
| zeus | 573 Succeeded | **574** Succeeded | 24459mp9, CriomOS 63e95f1 (was 570, dhsp58b4, a75bd6c) |

## Rollback kept before the switch (`rollback/`)

- Lojix rollback requests at CriomOS a75bd6ce: `rollback/lojix-ouranos-rollback-request.datom`, `rollback/lojix-zeus-rollback-request.datom`.
- Configuration, Metaflows, Queues and the herdr list read at the stop: `before/*-at-stop.*`.
- flow-nexus-0550.service stopped at 05:42:18 and the whole Nexus state directory was copied to `rollback/stopped-nexus-main/`; every file's sha256 at the source, at the stop and in the copy is equal (`rollback/stop-state.txt`). The Curriculum context was copied (`rollback/curriculum-context-copy/`); Curriculum was not restarted.
- Flow was down from 05:42:18 to 05:43:49, about 91 seconds. The store format is unchanged, so 0.56.1 also opens it as it is now.

## Verification on ouranos (`after/`)

- **Version and units:** flow-nexus 0.56.2, running `nwwm7mri...-flow-configured-0.56.2` (PID 654687). flow-configure-0550, curriculum-nexus and flow-nexus-0550 are active. No user unit has failed (`after/failed-after.txt`).
- **Seats carried over:** the seven flows awake at the stop are Awake after, the same set (`before/awake-at-stop.txt` equals `after/awake-after.txt`).
- **Configuration:** all 18 families equal the readback taken at the stop, Counters included (`after/configuration-comparison.txt`).
- **Journals:** flow, configure and Curriculum hold nothing matching error, fail, panic, refus, mismatch, woke or "not recorded Awake" (`after/journal-*.txt`). The only lines are the old unit's stop and the new unit's start.
- **Send round trip:** `Send.{ { Mind flowNexus Opus } Soft.Notice ... }` answered `Sent.8jp5`; the journal shows it admitted at 1794656647.849 (`after/send-roundtrip.txt`, `after/journal-flow-send.txt`). The request left the queue and its text is in this flow's own pane, typed there by the live Flow (`after/pane-read-roundtrip.txt`). This covers the Emission-typed Herdr socket prompt.
- **Herdr pane listing against Flow's own view:** `herdr agent list` shows 7 panes before the stop and after the switch, identical in pane, harness, native session, display name and status (`after/herdr-comparison.txt`); the only raw difference is my own pane's spinner glyph. Flow's Metaflows view has the same 7 flows Awake, each with the id shown in its pane title (`after/awake-after.txt`, `after/herdr-agents-after-send.txt`). This covers Herdr's typed command line.
- **Not exercised live:** a Launch (the typed harness command line and the pane shell line), a handover archive Git run (the archive is `ArchiveUnconfigured` on ouranos) and a Curriculum query after the switch. These are covered by the gate and the 8/22 capsule, and no witness flow was launched.

## zeus (`zeus/`)

- Before: Home dhsp58b4, flow client 0.56.1, no failed user units.
- After: home-manager profile 24459mp9; `flow-nexus` and `flow-nexus-meta` resolve to `nwwm7mri...-flow-configured-0.56.2`, the same package as ouranos; `flow-nexus --version` answers 0.56.2; no failed user unit (`zeus/after.txt`). zeus has no Nexus, so no Send was tried there.

## Anything that did not go as planned

- Nothing failed. `flow-nexus-meta --version` is not a command (it reads the flag as an Input), so zeus/after.txt ends with that refusal; the package path shows the version.
- The unit and wrapper names still say 0550 and 0.55.0 while running 0.56.2.
- The zeus flow-nexus-0550 stub unit (unconditional MemoryMax block outside the AgentStack gate, chi4) is not fixed here.
- Worktrees left: `/git/worktrees/flow-emission-565bc8-b`, `/git/worktrees/CriomOS-home-emission-0562-565bc8` and `/git/worktrees/CriomOS-emission-0562-565bc8`, each equal to its main. Pushed branches `release-0562-565bc8` (flow) and `emission-release-565bc8` (CriomOS-home).
