# Verification: Curriculum, Orchestrate, Lojix and Energy (2026-11-14, about 09:00–09:30)

Everything here was run read-only. No switch, restart, Configure, Lock or commit was made. The scratch directory is `/tmp/tmp.ye82GabJ9w`: logs, bare clones in `repos/`, and the sources at the live revisions in `src/`.

## Summary

| claim | verdict |
|---|---|
| ouranos runs Orchestrate 0.39.0 (ef4fe80) and Curriculum 8881cc1, healthy | **verified** |
| zeus runs Orchestrate 0.39.0, store upgraded on open, serves | **verified** |
| zeus runs Curriculum 8881cc1 | **partly verified.** The CLI binary is present. No curriculum-nexus unit exists on zeus, so nothing there answers |
| Curriculum and Orchestrate generated from their Ethos **by ethos-zero 28** | **failed for Curriculum.** It uses ethos-zero 27 (8c95310), as does signal-curriculum-nexus 4358aa1. **Verified for Orchestrate:** 28 (970459d) |
| the running code uses the generated types, with no hand-written twins | **verified** for both, with small edges listed below |
| Lojix being moved onto its Ethos on branches | **failed.** No branch exists, and the order never reached the flow |
| Energy step one done on branches | **verified.** All five heads build green on prometheus. The branch has also moved past step one |

## 1. What runs

### ouranos (local, user units)

- `systemctl --user show orchestrate-nexus`:
  - `ExecStart=…/ag9lqzvk0wrrmh906wy2pb4p76lnipkr-orchestrate-0.39.0/bin/orchestrate-nexus`
  - `ActiveState=active`, `NRestarts=0`, started `03:44:44`
- `systemctl --user show curriculum-nexus`:
  - `ExecStart=…/gdhrg5g05438iykqkn3hwcfwvhszlcfa-rust_curriculum-0.1.0/bin/curriculum-nexus`
  - active, `NRestarts=0`, started `03:44:48`
- **Store paths to revisions.** The derivation's `src` was compared with `nix flake metadata github:LiGoldragon/<repo>/<rev>`, using `diff -rq`:
  - **Curriculum.** The running src `31jdn79…-source` differs from the 8881cc1 tree `0q6d4lbn…-source` only by `Cargo.nix`, `.gitignore` and `.beads/.gitignore`, which the filter removes.
  - **Orchestrate.** The running nexus src `w57hsp69…-source` (Cargo.lock, Cargo.toml, crates, rust-toolchain.toml) has no file that differs from ef4fe80 `64hw8qan…`. The only lines are "Only in ef4fe80".
- **One build per component.** The `orchestrate` wrapper on PATH execs `ag9lqzvk…-orchestrate-0.39.0/bin/orchestrate`, the same path as the unit. The `curriculum` wrapper (`wksqh2p3…`) execs `gdhrg5…/bin/curriculum`, the same build as the Nexus.
- **Home generations.** The release generation is 1157 (`c7hjhgav`). Generations 1158 and 1159 came after it, from the Flow releases. All three carry the same two ExecStarts.
- **Lock pins.** CriomOS main 949c450 and CriomOS-home main pin `curriculum-source` 8881cc11ef4e and `orchestrate` ef4fe80b98a8. Both originals are bare `github` URLs.
- **Journal since the switch.** `journalctl --user -u orchestrate-nexus -u curriculum-nexus --since 03:40` has 9 lines, all stop, start and `orchestrate-nexus ready`. Nothing matches error, fail, panic, refus or warn.
- **One failed user unit, not in this lane.** `context-skills.service` fails with `not a module source: /tmp/…/psyche-belief/vision/account`. It has failed 18 times since `2026-11-13T20:42`, which is before these releases. It runs a babashka `generate.clj`, not Curriculum.

### zeus (`ssh root@zeus.goldragon.criome`)

- **li's user manager was already running** when I arrived: session 424, background, started at 09:04. I did not start it.
- `systemctl --user -M li@ show orchestrate-nexus`:
  - `ExecStart=…/ag9lqzvk…-orchestrate-0.39.0/bin/orchestrate-nexus`
  - active, `NRestarts=0`, started `09:04:45`
- **Home generations 41 to 44** (`baaa2p5f`, `dhsp58b4`, `24459mp9`, `jlyfa1mj`, the current one) all name ag9lqzvk.
- **Curriculum.** `systemctl --user -M li@ show curriculum-nexus` gives `ActiveState=inactive`, `FragmentPath=` (empty). The Home has no curriculum unit at all; the user units are only `orchestrate-nexus.service` and `wispr-flow.service`. The closure does hold `gdhrg5…-rust_curriculum-0.1.0` and the `wksqh2p3…-curriculum` CLI.
- **Upgrade journal**, from `journalctl … _SYSTEMD_USER_UNIT=orchestrate-nexus.service --since 03:49`:
  - `03:55:26 orchestrate-nexus upgraded /home/li/.local/state/orchestrate-nexus/orchestrate-nexus.memory from the sema format to the memory format`. It appears once.
  - It is followed by 15 `ready` lines through `09:04:46`, one per login.
  - Nothing matches error, fail, panic, refus, mismatch or "start limit".
- **The store file.** `stat` gives inode `28879478` (unchanged), 303104 bytes. A string grep finds both `__memory_*` and `__sema_*` names in the file, which settles nothing because the old pages remain. The upgrade line and the serving Nexus are the evidence.
- **Rollback copy.** It is present in `/root/orchestrate-rollback-2e404d/`.
- No failed user units.

## 2. Live read-only queries

| host | command | decisive output |
|---|---|---|
| ouranos | `orchestrate 'Observe.Locks'` | `Observed.Locks.[ { 129 curriculumPauseHandover706b16 … } …` with 11 Locks, exit 0. This matches the 12 at the stop minus Lock 172, which was released |
| ouranos | `curriculum 'ResolveSkills.[ spirit:core:0 intent:design:0 ]'` | `SkillsResolved.[ spirit:core:0 intent:design:0 ]`, exit 0 |
| ouranos | `curriculum 'ComposeRole.{ general-purpose ClaudeAgent }'` | `RoleComposed.{ general-purpose ClaudeAgent sonnet High Unrestricted …`, exit 0 |
| ouranos | `curriculum --claude-agent-markdown general-purpose` | `curriculum accepts exactly one inline Datom request`, exit 1. The renderer is removed, as claimed |
| zeus | `runuser -u li -- env XDG_RUNTIME_DIR=/run/user/1001 …/orchestrate 'Observe.Locks'` | `Observed.Locks.[]`, exit 0 |
| zeus | `runuser -u li -- …/curriculum 'ResolveSkills.[ spirit:core:0 ]'` | `cannot connect to Curriculum Nexus …`, exit 1. `/run/user/1001` holds no `curriculum` directory, so there is no Nexus on zeus |

## 3. Is the Ethos used? (sources at the live revisions)

### Orchestrate ef4fe80: verified

- **ethos-zero version.** `Cargo.toml:19` pins `ethos-zero … rev = "970459d"`, which is 28.0.0 in Cargo.lock.
- **Build checks.** The committed Rust is checked against fresh generation in:
  - `crates/orchestrate-nexus/build.rs` (memory.ethos to `src/memory.rs`);
  - `crates/orchestrate/build.rs` and `crates/orchestrate-meta/build.rs` (client.ethos to `src/generated/client.rs`).
- **The contracts are generated too.** signal-orchestrate e4fda9b and meta-signal-orchestrate 27ac19c each have a `build.rs:17` assertion, "src/generated/signal.rs is stale; regenerate it from ethos/signal.ethos". Neither has a hand-declared type outside `src/generated`.
- **Running paths use the generated types:**
  - `store/record.rs:16` re-exports `crate::memory::{StoredLock, StoredMetadata, …}`;
  - `store/normalize.rs:9` works on the contract's `LockRequest` and `LockRejection`;
  - `transport/session/contract.rs:10-14` speaks `signal_orchestrate::{Input, Output}` and `meta_signal_orchestrate::{Input, Output}`;
  - `orchestrate/src/main.rs:7,14` uses the generated `ClientFailure` and the contract's `Input` and `Output`.
- **No twin of a contract or store type remains.** The hand-written types are runtime machinery: actors, socket claims, error enums, `DefaultConfiguration`.
- **Edges:**
  - `store/normalize.rs:84` has `struct NormalizedLockPath(String)`, an internal newtype beside the contract's `LockPath`.
  - The file names are string literals in code, at `defaults.rs:15-19`.
  - The lock still carries ethos-zero 19.2.0, pulled in by `signal` 10.3.0 and not by Orchestrate.

### Curriculum 8881cc1: types verified; the version claim fails

- **ethos-zero version.** `Cargo.toml:43` pins `ethos-zero … rev = "8c95310"`, and `Cargo.lock:156-157` says `version = "27.0.0"`. The same holds for signal-curriculum-nexus 4358aa1 (`Cargo.lock:73-74`). So "generated by ethos-zero 28" does not hold for Curriculum.
- **Build checks.** `build.rs` checks `curriculum.ethos`, `memory.ethos` and `emission.ethos` against `src/generated.rs`, `src/memory.rs` and `src/emission.rs`.
- **Running paths use the generated types:**
  - `service.rs:6-9` answers through `signal_curriculum_nexus::{Answering, Input, Output, …}`;
  - `memory.rs` holds the generated `SkillMemory.{ Option<Roles> }`;
  - `roles.rs:2-4` validates and composes from the generated `RoleDefinition` and `Roles`;
  - `registry.rs:2-3` uses the generated `ModuleDeclaration`, `ModuleKind` and the Emission's `RefreshProgram`/`RefreshOutcome`.
- **No wire or file-format twin remains.**
- **Edges, all hand-written runtime types:**
  - `registry.rs:110-114` has `SkillEntry { name: String, dependencies: Vec<String> }`, with `pub type ResolvedSkill = SkillEntry` at line 116. The registry carries module identities as bare `String`, unwrapping `ModuleIdentity` at `service.rs:116-117` and rewrapping it at `service.rs:62`.
  - `registry.rs:18-46` has a hand `MODULE_KINDS` list and `word()` table over the generated `ModuleKind`.
  - `client.rs:13-31` has a hand `ClientError`. Orchestrate generates its client failure from `client.ethos`; Curriculum does not.
  - The generated `Emission`/`Outcome` enums in `src/emission.rs` are compiled but nothing dispatches on them. The 2e404d q10q report says this too.

## 4. Lojix and Energy

### Lojix: failed, not started

- **No branch exists.** `git for-each-ref --sort=-committerdate` on fresh bare clones of lojix, signal-lojix and meta-signal-lojix shows no branch newer than 2026-11-12. lojix main is `da0ad8a` (11-12), signal-lojix main `bd5d250` (11-09), meta-signal-lojix main `1b0aaeb` (11-09). The local clones and `/git/worktrees` hold no Lojix Ethos worktree either.
- **The order never reached the flow.** `flow-nexus 'Queues'` shows `{ Mind curriculum Opus }` still holding the order: `Soft.Order.{ yjj2 «Well done on a7im. Next on the Ethos line, in his order: Lojix (kc4e), then Energy (juh8)…» }`, then `Soft.Notice.{ hpf6 «Change to yjj2: … Yours is Lojix alone…» }` and five notices from Mind flowNexus Opus.
  - The flow is asleep: herdr shows no pane for it.
  - Soft does not wake an asleep flow, so it has never read the order.
  - Its last file is `/home/li/primary/flows/2e404d/reports/release-orchestrate.md` at 03:57.
- **Lojix is unchanged on main.** `src/runtime_model.rs` holds 113 hand-declared `pub struct`/`pub enum` types, the first being `DeploymentTransport` at `:82`. `Cargo.toml:53` pins ethos-zero `c2653dd`, the generation 16 era, and `ethos/ingress.ethos` is the only Ethos file.
- **What closes it.** A wake of `{ Mind curriculum Opus }` (MiddleAbrupt), or a fresh order. I sent nothing, since this lane changes nothing.

### Energy: verified, and it has moved past step one

- **Branch heads (`ethos-565bc8`):**
  - **signal-energy-nexus:** `e0eb9b7` (step one), then `5c1ff2f` ("0.6.0: Redeemed answers Redeem, Refused declared once and named; the digest moves once", 06:28).
  - **meta-signal-energy-nexus:** `fb69426`, then `fa3e3de` (0.6.0, 06:29).
  - **energy-nexus:** `0b9e6b4` (06:20), which still pins the step-one contracts e0eb9b7 and fb69426 (`Cargo.toml:10-11`).
  - So the 0.6.0 contract heads are not yet taken up by energy-nexus. The work is in progress: Mind flowNexus Opus 565bc8 reads as working in herdr.
- **Gates.** I ran `nix run nixpkgs#nix-fast-build -- --remote li@prometheus.goldragon.criome --no-nom --flake github:LiGoldragon/<repo>/<full-rev>#checks.x86_64-linux`. Logs are `/tmp/tmp.ye82GabJ9w/gate-*.log`, exits in `gate-exits.txt`:
  - signal-energy-nexus e0eb9b7: exit 0 (`test`)
  - meta-signal-energy-nexus fb69426: exit 0 (`test`)
  - energy-nexus 0b9e6b4: exit 0 (`nexus-dependency-boundary`, `test`)
  - signal-energy-nexus 5c1ff2f: exit 0 (`test`)
  - meta-signal-energy-nexus fa3e3de: exit 0 (`test`)
  - The flakes expose only these checks, so the gate builds no package.
- **The package builds.** `nix build --max-jobs 0 github:LiGoldragon/energy-nexus/0b9e6b4…#packages.x86_64-linux.default` exited 0 and gave `/nix/store/jciqz1j5…-cargo-package-0.0.1`, built on prometheus.
- **The Ethos is used in the contracts.**
  - Both contracts' `build.rs:23` assert "… is not what ethos-zero generates from ethos/<name>.ethos".
  - The contract's `Cargo.lock:87-88` has ethos-zero 28.0.0. The 22.0.0 in the same lock comes from signal, signal-flow and flow-ethos.
  - `grep wire!|macro_rules` over both contracts' `src` finds 0 matches.
- **energy-nexus itself still has hand-written stores and emissions,** as the report says, which leaves step two:
  - `crates/core/src/lib.rs:8,14,57`: `Latest`, `Configuration`, `Memory` (rkyv, the store);
  - `crates/emission/src/lib.rs:1-29`: the `wire!` macro, with `Emission`, `Outcome` and the rest by hand;
  - `crates/translator/src/lib.rs:25`: `Programs`, the translator store;
  - `crates/translator/src/cli.rs:14,20`: `CliConfiguration` and `ConfigurationRefusal`.
- Energy is not live and was not claimed live. Energy main is unchanged at `2623947`.

## Not checked

- **The 2e404d memory-engine proofs and the byte-identity claims.** These are the zeus copy, the ouranos 148-Lock store and the Energy hand-against-generated test. I took the test pass as their evidence and did not rerun the bwrap proofs.
- **"CriomOS-home checks red on main at codex-next.nix:16".** My `nix eval …#checks.x86_64-linux --apply builtins.attrNames` on 39c8660 stops earlier, at `no system input was provided`. I did not reproduce the nix-eval-jobs path, so this is unverified.
- **That the live Home was built on prometheus** and not locally. This is unknown; I saw only that the store paths match.
- **The zeus store's format.** The string grep is inconclusive, as above. I did not open the store with a tool.
