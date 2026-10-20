# Hard-coded Nix store paths: inventory, history, cause, resolving forms

Read-only investigation. Host clock at writing: 2026-10-18 19:30 CST (America/Mexico_City), on ouranos.
The living's ruling this answers: flows/d68c82/vision/criomos.md, "Never a hard-coded Nix path" (raw, 2026-10-19 01:07 by its own context line).
Provenance receipt evidence: unavailable (no PROVENANCE handoff exists); transcripts are named below by state root, start time and subflow agent path, never by thread ID.
The flow-evidence skill could not be loaded: this seat has no skill-loading tool. This file exists because the brief orders it.

Origin legend: W = witnessed by this investigation (code read, command run); C = claim by the named flow, relayed; I = this flow's inference.

## Method (W)

- 223 git repositories under /git/github.com/LiGoldragon deduplicated by origin URL to 218; `git fetch origin` succeeded for 217; LiGoldragon/nixpkgs (fork) failed and is excluded. Every repo was read at origin/main (mentci-web at origin/HEAD).
- Live scan: `git grep` at origin/main for `/nix/store/`, `builtins.storePath`, `storeDir`, `appendContext`, `unsafeDiscardStringContext`, `fetchClosure`, and bare 32-char nix-base32 `<hash>-<name>` in `*.nix`; plus profile paths (`/run/current-system/sw`, `/etc/profiles/per-user`, `/nix/var/nix/profiles`) as an adjacent class.
- The workspace repos primary, primary-next and secondary carry 7,531 matching lines, all in logs, reports, receipts, witnesses and tests of tools; none is in a `.nix` file. They are evidence, not Nix code, and are not counted below.
- History scan: `git log --all -G'/nix/store/[0-9a-df-np-sv-z]{32}-' -p` over `*.nix` and `owned-rust-exports.json` in every repo; `--all` includes jj keep refs. GitHub-side unreachable objects and other clones were not scanned.
- A parallel inventory exists: private-repos/flow-evidence/41fa34/nix-store-literals-20261018 (Mind Sol 41fa34, C): 43 matching `.nix` lines, 21 with a concrete identity. This scan agrees on the `.nix` lines and adds owned-rust-exports.json (12 lines read by Nix through `builtins.fromJSON`) and the `builtins.appendContext` forgery in lojix-test.

## 1. Live sites at origin/main

CriomOS-home origin/main 1517609a (2026-10-18 17:03 -0600); CriomOS 3951255 (17:04); lojix-test 5aece43 (2026-10-02).

Counts (W): 33 lines carry a 32-char store identity in Nix code or Nix-read data. 30 name real store objects (21 distinct objects); 3 are synthetic fixtures. Of the 30, 28 are production or evaluated sites and 2 are a check mirroring one of them. One further site forges string context (`builtins.appendContext`) on one of the literals.

### 1a. Production and evaluated literals (28 lines)

| Repo:path:line | Literal | What consumes it |
|---|---|---|
| CriomOS-home modules/home/profiles/min/codex-remote-control.nix:24 | `occupiedCodex` = wdj0sc…-codex-0.153.4/bin/codex | `codex-remote-control.service` ExecStart for li and Bird (line 130; `occupied` includes `birdTarget`, line 19) |
| codex-remote-control.nix:25 | `occupiedNextCodex` = zbznvq…-codex-next-0.158.0-alpha.9/bin/codex | the `codex` wrapper in li's home.packages (lines 28-35, 57) |
| codex-next.nix:16 | `occupiedCodex` = zbznvq…-codex-next-0.158.0-alpha.9/bin/codex | `codex-remote-control-next.service` ExecStart for li (line 95) |
| codex-next.nix:17 | `occupiedPrepare` = 58axnp…-codex-next-prepare (Bird) / dxqsqx…-codex-next-prepare (li) | ExecStartPre (line 94); the Bird branch is dead code since 240a3174 narrowed `occupied` to li |
| CriomOS-home modules/home/profiles/min/herdr.nix:53, :54 | 0s199v…-codex-stable-flow-client, x74szg…-codex-next-flow-client | text of `rotationPredecessorManagedHerdrConfig`, an admitted predecessor for the Herdr config adoption guard |
| CriomOS-home lib/primary-committer-hook-trust.nix:7 | bfqsxl…-nodejs-slim-24.19.0/bin/node, plus two /home/li/private-repos/flow-evidence paths | SessionStart hook `command` whose sha256 is the `trusted_hash`; merged into the candidate Codex config by codex-next-candidate.nix:12, :35-36 |
| CriomOS-home packages/harness-profile/default.nix:4 | `builtins.storePath` k6mwx3…-home-manager-path | `baseline` of `harness-home-profile` |
| harness-profile/default.nix:12 | `builtins.storePath` kds5yv…-chatgpt-26.901.51231 | `oldChatgpt` share leaves |
| harness-profile/owned-rust-exports.json:2,6,10,14,18,22,26,30,34,38,42,46 | baseline again, and cargo, clippy, rustfmt, rust-analyzer, rustc, rustdoc, gdb/lldb wrappers of Rust 1.97.1 | `ownedRustExports` argument (default.nix:6) |
| CriomOS modules/nixos/userHomes.nix:17,18,22,27,28,32 | Zeus predecessor home-manager-files, herdr-config.toml and Kvantum link targets for bird and li | `criomosHome.herdr.predecessorGeneration` and `kvantumDanglingLink`, set only when node is zeus (line 43) |
| lojix-test modules/immutable-converter-replay.nix:20 | l04p8r…-lojix-migrate-v5-v6-0.1.0 | `converter`, given forged context by `builtins.appendContext` at :21 |

### 1b. Check mirror (2 lines)

CriomOS-home checks/herdr-toast-delivery/default.nix:131, :132: the same two flow-client paths as herdr.nix:53-54.

### 1c. Synthetic fixtures (3 lines with hash shape, plus non-hash fixtures)

- CriomOS-home checks/bird-home-isolation/default.nix:154, :155 (`0123456789abcdfg…-nodejs`, `zyxwvsrq…-agent-intercom`); lojix flake.nix:343 (`aaaa…-lojix-test-candidate.drv`).
- Without hash shape: CriomOS-home checks/opencode-harness/default.nix:73, :76; checks/spirit-deployment/default.nix:453 (built from a computed hash); patches/herdr/codex-executable-selection.patch:457 (a comment); flow-test checks/flow-configure-nexus-no-binary.nix:14.
- I: these are data that stand for a store path in a test input; none names a store object. Whether the ruling covers them is a question for the living.

### 1d. Patterns, validators and comments (not literals; listed for the audit)

CriomOS-home modules/home/base.nix:109 (redaction regex); profiles/min/field-monitoring.nix:175 (glob); profiles/min/migrate-obsolete-spirit-judge-override.sh:38 (regex); profiles/min/pi-models.nix:229, :233 (regex); packages/messenger-clj-deployment/default.nix:11 (prefix test); checks/spirit-deployment/default.nix:429, :430, :442 (sed); checks/codex-next/default.nix:39 (grep); gates/claude-desktop-launcher-linkage/default.nix:61 (grep). CriomOS modules/nixos/nspawn.nix:72 (prefix test). lojix checks/target-store-realization.nix:144, :153, :154 (asserts). persona/Persona flake.nix:861, :992 (comments). CriomOS-test-cluster lib/deploy-flake.nix:23 (comment). CriomOS checks/flake-registry-shape/default.nix:39 uses `appendContext` to restore context taken from an evaluated option; it resolves.

### 1e. Adjacent class: stable profile paths (resolve at runtime)

CriomOS modules/nixos/normalize.nix:121, :122, :225; nspawn.nix:18, :192; checks/nspawn-role-policy/default.nix:82. CriomOS-home profiles/med/element.nix:19; profiles/min/flow.nix:45; profiles/min/spirit.nix:46; packages/flow-deployment/default.nix:138. CriomOS-test-cluster flake.nix:151-152; lib/standardTest.nix:67-68; lib/mkDeployTest.nix:507, :514; lojix flake.nix:398, :416. I: these name profile links that always resolve to the current generation; they are not store literals. Listed so the ruling can say whether it reaches them.

### 1f. Nix-generating code

No generator writes a store literal into a `.nix` file (W: lojix src hits are tests and the store-root validator at src/inspected_text.rs:123, :135). owned-rust-exports.json is the one generated data file Nix reads; its producer was not traced.

## 2. History

All commits in this scan are authored `li <li@goldragon.criome.net>` or `li <ligoldragon@gmail.com>`. None carries a trailer (W: `%(trailers)` empty for every one). The writing flow is therefore not in git; section 3 recovers it from transcripts for the Codex literals.

52 commits introduced a real literal; 69 commits touched one (added or removed), across 4 repos: CriomOS-home 44, CriomOS-test-cluster 13, lojix-test 10, CriomOS 2. 44 distinct real store objects were introduced over time; 21 remain at origin/main. Reachability of the 69: 19 reachable from origin/main, 13 from a remote branch only, 37 only from local jj keep refs (unpushed working-copy snapshots, mostly without description). Synthetic-only commits (lojix test stub, CriomOS-home lojix-run and bird-home-isolation fixtures) are excluded from these counts.

Every origin/main commit after an introduction keeps the literal: 85 commits on CriomOS-home main follow b3049b, 10 on CriomOS main follow 31d79d, 5 on lojix-test main follow a9d44a (W, `git rev-list --count`).

Literals that once existed and are gone from main (W): Flow 0.12.2/0.14.0/0.17.4, Message 0.17.0, flow-configure-next, herdr 0.8.2, harness 0.3.4, claude-code 2.1.284 (flow.nix, flow-message*.nix, checks/flow-service-path; removed from main by 0eda1b and 215139); messenger-clj 0.2.5/0.2.8 and two home-manager-files (messenger-clj.nix and its check; removed by 77244c); four earlier Zeus predecessors in CriomOS userHomes.nix (replaced by 31e6f4); six nixos-system-mercury closures and drvs in CriomOS-test-cluster lib/mkDeployTest.nix (branch datomic-horizon only); lojix-v5-v6-consumer-qualification in lojix-test.

A fix exists only locally (W): CriomOS-home 91dc62 "Resolve Codex endpoint executables and helpers from declared packages", 2026-10-18 19:13 -0600, child of 1517609a, held only by jj keep refs (with siblings 4fbd07 and b6f2ae). It removes the five Codex literals behind a new `criomosHome.codexEndpoints` module. It is not on any remote branch.

Table (repo, commit, date, literal lines +added -removed, reachability, message):

| Repo | Commit | Date | +/- | Reachable from | Message |
|---|---|---|---|---|---|
| CriomOS-test-cluster | 1a7e39 | 2026-09-06 | +1 -1 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | 223aee | 2026-09-06 | +1 -1 | remote-branch | C6: avoid derivation context in VM scripts |
| CriomOS-test-cluster | 54f29d | 2026-09-06 | +2 -0 | remote-branch | C6: materialize CriomOS through Lojix inputs |
| CriomOS-test-cluster | 98bec8 | 2026-09-06 | +2 -2 | remote-branch | C6: replay d15 input metadata exactly |
| CriomOS-test-cluster | a76b76 | 2026-09-06 | +2 -2 | remote-branch | C6: pin final CriomOS Clavifaber graph |
| CriomOS-test-cluster | b1e437 | 2026-09-06 | +2 -2 | remote-branch | C6: register the prebuilt Mercury closure |
| CriomOS-test-cluster | cb19fc | 2026-09-06 | +2 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | ccb7d6 | 2026-09-06 | +2 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | d69e72 | 2026-09-06 | +2 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | dbf419 | 2026-09-06 | +2 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | e231ac | 2026-09-06 | +2 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | e6fb64 | 2026-09-06 | +2 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-test-cluster | f2072e | 2026-09-06 | +2 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 377b86 | 2026-09-29 | +1 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 3a2a83 | 2026-09-29 | +1 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | d05022 | 2026-09-29 | +2 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | dadb9a | 2026-09-29 | +2 -0 | origin/main | Home-manage messenger compatibility bindings |
| CriomOS-home | 002589 | 2026-09-30 | +2 -0 | origin/main | Home: admit witnessed Messenger predecessor |
| CriomOS-home | 030424 | 2026-09-30 | +4 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 0eda1b | 2026-09-30 | +0 -2 | origin/main | Home: complete Codex role rotation for Flow |
| CriomOS-home | 181f38 | 2026-09-30 | +4 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 37ae58 | 2026-09-30 | +12 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 37e443 | 2026-09-30 | +4 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 49dce7 | 2026-09-30 | +4 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 5cc911 | 2026-09-30 | +0 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | a07be7 | 2026-09-30 | +4 -0 | origin/main | Home: admit witnessed Herdr rotation predecessor |
| CriomOS-home | b3049b | 2026-09-30 | +14 -0 | origin/main | Home: preserve occupied Codex rotation units |
| CriomOS-home | d1a3c7 | 2026-09-30 | +4 -0 | origin/main | Home: preserve occupied next Flow configuration |
| CriomOS-home | e7bc7c | 2026-09-30 | +2 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | ee5b1f | 2026-09-30 | +14 -0 | local-jj-only | (no description; jj snapshot) |
| lojix-test | 210015 | 2026-10-02 | +1 -1 | local-jj-only | (no description; jj snapshot) |
| lojix-test | 4e9f42 | 2026-10-02 | +2 -1 | local-jj-only | (no description; jj snapshot) |
| lojix-test | 9ec4d5 | 2026-10-02 | +2 -1 | origin/main | Reuse retained replay helper closure |
| lojix-test | a9d44a | 2026-10-02 | +1 -0 | origin/main | Replay immutable cea migration converter |
| lojix-test | c437aa | 2026-10-02 | +1 -1 | origin/main | Preserve replay converter input context |
| lojix-test | c79273 | 2026-10-02 | +1 -0 | local-jj-only | Replay immutable cea migration converter |
| lojix-test | df8902 | 2026-10-02 | +1 -2 | origin/main | Build replay helper when retained closure is unavailable |
| lojix-test | e6f7e0 | 2026-10-02 | +1 -0 | local-jj-only | (no description; jj snapshot) |
| lojix-test | ef336e | 2026-10-02 | +1 -2 | local-jj-only | (no description; jj snapshot) |
| lojix-test | efe049 | 2026-10-02 | +1 -0 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 1ce9ba | 2026-10-03 | +0 -4 | remote-branch | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | 1fb96d | 2026-10-03 | +0 -4 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 2ad35c | 2026-10-03 | +1 -0 | remote-branch | Home: enable the staged Flow and Message next pair for f1c841 |
| CriomOS-home | 325b2e | 2026-10-03 | +0 -4 | remote-branch | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | 4846e7 | 2026-10-03 | +2 -2 | remote-branch | Home: admit the witnessed Messenger predecessor |
| CriomOS-home | 5fed33 | 2026-10-03 | +0 -12 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 6c3370 | 2026-10-03 | +3 -2 | local-jj-only | Home: enable the staged Flow and Message next pair for f1c841 |
| CriomOS-home | 71f9a9 | 2026-10-03 | +0 -4 | remote-branch | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | 9497e4 | 2026-10-03 | +0 -12 | remote-branch | Home: Flow 0.23.0 and Message 0.19.0 as the regular pair (flow-nexus, flow-configuration, message-nexus on %t/flow, %t/message); next slot off; retire Flow 0.14 flow.nix and Message 0.14 message.nix |
| CriomOS-home | 95992f | 2026-10-03 | +0 -12 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | a34078 | 2026-10-03 | +0 -2 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | abde3b | 2026-10-03 | +3 -2 | local-jj-only | Home: admit the witnessed Messenger predecessor |
| CriomOS-home | b72b74 | 2026-10-03 | +1 -0 | local-jj-only | Home: enable the staged Flow and Message next pair for f1c841 |
| CriomOS-home | c87aa1 | 2026-10-03 | +0 -4 | remote-branch | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | f6cd35 | 2026-10-03 | +0 -4 | remote-branch | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | fbc14d | 2026-10-03 | +1 -0 | local-jj-only | Home: enable the staged Flow and Message next pair for f1c841 |
| CriomOS-home | 77244c | 2026-10-07 | +0 -4 | origin/main | Home: accept Home Manager generated messenger bindings |
| CriomOS-home | 798e30 | 2026-10-07 | +0 -4 | local-jj-only | Home: messenger bindings guarded by Home Manager's own link check; drop the one-migration pinned guard and force |
| CriomOS-home | e11475 | 2026-10-09 | +2 -1 | origin/main | Protect occupied Codex servers and scope Curriculum capability |
| CriomOS | 31d79d | 2026-10-10 | +6 -0 | origin/main | Qualify Zeus recorded Home adoption and coherent Curriculum roots |
| CriomOS-home | 0cee0a | 2026-10-12 | +1 -0 | origin/main | Declare exact committer proof-hook trust in the candidate user configuration |
| CriomOS-home | 215139 | 2026-10-13 | +1 -12 | origin/main | Unify Flow and Message in the declared Home environment |
| CriomOS-home | 2b0163 | 2026-10-13 | +1 -1 | origin/main | Bind the checked Ouranos profile to its accounted Home baseline |
| CriomOS-home | 289f39 | 2026-10-14 | +1 -0 | origin/main | Select the updated ChatGPT desktop in the declared Home profile |
| CriomOS-home | 8d0f36 | 2026-10-16 | +13 -1 | origin/main | Default Rust entrypoints to remote Nix builds and advance Flow/context cohort |
| CriomOS | 31e6f4 | 2026-10-18 | +4 -4 | origin/main | Record actual Zeus Home predecessors for guarded adoption |
| CriomOS-home | 4fbd07 | 2026-10-18 | +0 -5 | local-jj-only | (no description; jj snapshot) |
| CriomOS-home | 91dc62 | 2026-10-18 | +0 -5 | local-jj-only | Resolve Codex endpoint executables and helpers from declared packages |
| CriomOS-home | b6f2ae | 2026-10-18 | +0 -5 | local-jj-only | (no description; jj snapshot) |

## 3. How the Codex literals came to be

### 3a. Writer (W)

- `occupiedCodex` and `occupiedNextCodex` in codex-remote-control.nix, and `occupiedCodex` and `occupiedPrepare` in codex-next.nix, were first written by the subflow `/root/rotation_finish` of Field Astra d5b96b. Transcript: ~/.codex-next/archived_sessions, rollout started 2026-09-30T08:49:51 -0600, agent role write-ordinary. The spawn call requested gpt-6-luna at xhigh; the recorded turn context is gpt-5.6-terra at medium.
- The patch was applied at 14:52:39Z (record 111). jj snapshots ee5b1f and 37ae58 preceded commit b3049b, "Home: preserve occupied Codex rotation units", 08:53:23 -0600, parent 682508d4, now on CriomOS-home main.
- The same worker also wrote the Flow literals that were later removed (flow.nix `occupiedFlow`, `occupiedPath`, clients), d1a3c7 (flow-message-next), a07be7 (the Herdr predecessor literal still in herdr.nix:53-54), and 002589 (Messenger predecessor). d5b96b log.md:373 is the claim; the commit sequence in the table is the witness.
- The Bird branch of `occupiedPrepare` (58axnp…) and the widening of `occupied` to Bird were written by the subflow `/root/land_compensation` of Mind Sol 41fa34. Transcript: ~/.codex-next-8mkkxq293hk2/sessions/2026/10/08, rollout started 2026-10-08T11:13:35 -0600; patch at 2026-10-09T21:08:20Z; commit e11475, "Protect occupied Codex servers and scope Curriculum capability", 2026-10-09 15:09 -0600.

### 3b. What rotation_finish read, then wrote, in order (W, transcript records)

1. Its brief arrived as a NEW_TASK agent message whose payload is encrypted in both transcripts; its text is unavailable. The d5b96b log.md:371 claim: "dispatched rotation_finish with mandatory write-set lock and live-unit receipt."
2. Read NON_MANAGEMENT_AGENTS.md; the CriomOS-home and CriomOS AGENTS.md; flows/d5b96b/vision/codex-promotion.md, log.md, notion; flows/d5b96b/reports/codex-rotation-live-units.json (receipt faffc6, sha256 9caf8e…); Vision/modelRoles.md; flows/8a5caa/vision/codex.md.
3. Read the module sources and checks, then took Orchestrate lock 9714 on nine CriomOS-home paths.
4. Read the live unit files ~/.config/systemd/user/codex-remote-control.service, codex-remote-control-next.service, flow-nexus.service, flow-nexus-next.service. Their ExecStart lines carry the wdj0sc… and zbznvq… paths.
5. Reasoning summaries, in order: "Defining immutable live service units", "Inspecting exact live unit files for immutability", "Designing exact systemd unit patch", "Planning exact literal ExecStart paths". Its stated plan (record 75): "will make the frozen services literal preservation declarations while routing the new candidate through a separate hash-named unit."
6. Wrote the patch with the literals and the comments "The literal is the executable in the preserved live-unit receipt" and "Keep this definition byte-for-byte compatible with the occupied service." In flow.nix the same patch states the mechanism: "changing this byte would make sd-switch restart that process during the very activation meant to preserve it."

### 3c. The sentences upstream of the write, in order

The living's words, quoted from their records:
- 2026-09-30, flows/d5b96b/log.md:363, working instruction: "So, why did you stop working if you're not done? Do the rotation."
- 2026-09-30, vision record codex-promotion (file now gone from flows/d5b96b/vision; text recovered from Primary b734d7c37 and from the 14:16Z relay): "The stable becomes the next once all the flows have moved onto the next socket. If all the flows are on the next socket now, next can become stable, and then we can put the next version on next."
- 2026-09-30, notion, flows/d5b96b/notion/codex-update.md, relayed to Mind as NOTION at 14:16Z: "That way, we can move the next to the stable without changing the socket name, so it doesn't break any of the sessions. Maybe we can do that in a hacky way, with a bunch of comments on how we're going to fix it next time. … That way, we don't break our current sessions."

The skill: Curriculum skills/compensation-update.md at b7e15152, now field-context compensation/update.md:
- "Preserve the predecessor stable endpoint until migration is proved."
- "After the migration gate, promote by mapping stable to the already-running Next endpoint. Preserve its process, service, socket, state root, client route, and running sessions. Do not restart, recreate, rename, move, copy, or share its mutable state as part of promotion."

The flow-to-flow orders (hm-send texts, quoted from the transcripts):
- Field d5b96b to Mind 6f51ad, 14:26:06Z: "active Home generation 1036 accepts only --driver-version and always reloads systemd through sd-switch. sd-switch 0.6.4 has dry-run, timeout, and verbosity options, but no supported skip-reload, exclusion, or preserve-unit mode was found. … The artifact must keep live occupied stable PID1936 (0.153.4), Next PID1960 (0.158alpha9), and Flow PID607365/607363 definitions invariant, or demonstrate an sd-switch plan preserving all."
- Mind 6f51ad, subflow spirit_failure, to Field, 14:26:36Z: "We need byte/semantic comparison to ensure an sd-switch cannot replace PID1936/1960 or restart Flow."
- Field to Mind, 14:36:22Z: "Please resume the sole source worker now to preserve exact occupied live definitions while new launches use the role mapping … The user authorizes this bounded compensation while retaining legacy units unchanged; no generic approval gate is needed."
- Mind to Field, 14:36:39Z: "Accepted preservation correction. Source write set will anchor old stable/occupied Next/Flow generated definitions to your immutable live receipt".
- Field to Mind, 14:49:34Z, then the spawn at 14:49:51Z: "Field is reclaiming bounded source implementation under the Orchestrate lock with one implementation worker".

The sentence that led to the output: "Source write set will anchor old stable/occupied Next/Flow generated definitions to your immutable live receipt" (Mind 6f51ad). It answers Field's "definitions invariant" and "preserve exact occupied live definitions", which carry out compensation-update's "Preserve its process, service, socket, state root, client route, and running sessions. Do not restart, recreate …". The receipt holds store paths, so anchoring to the receipt means writing them.

For e11475, the upstream sentences (W, 41fa34 transcript):
- Field Sol 42265e, 2026-10-09 20:31Z: "Codex occupied guard is only homeDirectory=/home/li; active bird servers on Zeus are not automatically protected. I will compare actual new unit/executable/socket bytes before activation; please own any necessary declarative portability/protection fix".
- Psyche Core Secondary 445410, relaying the same at 20:32Z: "4. Protection gap: the Codex occupied guard checks only homeDirectory=/home/li, so active user bird servers on Zeus are not protected through activation. Extend the guard declaratively."
- 42265e, 21:06:58Z: "Current bird next unit instead ExecStartPre=/nix/store/58axnpgidzhnm7kdvfkikkjdhaycpxvg-codex-next-prepare. Broadening occupied routes bird to li script and changes unit bytes."

### 3d. The sentence the skills lack

No loaded skill or prompt sentence forbids a store literal in Nix code; none prescribes one either (W: searched psyche-context, mind-context, field-context, Curriculum and the CriomOS/CriomOS-home docs for store-literal, byte-for-byte, sd-switch and live-unit guidance). The nearest sentences, field-context compensation/nix-workflow.md, "Build and deploy reproducible source." and "Ask Nix or source, not the store filesystem.", do not name the case. CriomOS AGENTS.md:24 covers store paths in prose, code blocks and commit messages, not in Nix source.

Missing sentences (proposals; the authored files were not edited):
- field-context compensation/nix-workflow.md: "Every store path in Nix code is the output of evaluating a package, a flake input or an option. A `/nix/store/` literal, `builtins.storePath`, or string context added by hand is never written, in a module, a check, or data that Nix reads."
- field-context compensation/update.md: "A running endpoint survives a Home activation because the input that built its executable stays pinned. When no declared input rebuilds the running executable, stop and report that, rather than writing its store path into source."

The living's ruling itself is raw vision in flows/d68c82/vision/criomos.md. Crystallizing it into a vision skill goes through a book, not this report.

### 3e. Possible causes (not ranked; more than one may hold)

1. W: The order chain demanded generated unit text identical to the live units: "definitions invariant", "preserve exact occupied live definitions", "anchor … to your immutable live receipt". The source packages had moved past the running versions (corePackages.codex is now 0.163.0). For li, writing the receipt's paths was the only way the worker found to make the text identical.
2. W: Home Manager's activation reloads user units through sd-switch with no exclusion mode (claim by 6f51ad and d5b96b, not independently witnessed). compensation-update requires no restart but names no declarative way to achieve it.
3. W: No skill sentence forbids the literal (3d). The independent artifact and guard reviews passed (d5b96b log.md:373, C), which suggests their criteria were preservation, not resolvability (I).
4. I, unwitnessed: the living's notion, "in a hacky way, with a bunch of comments on how we're going to fix it next time", reached Mind as NOTION 36 minutes before the spawn. The comments the worker wrote match that shape. Whether the encrypted brief carried the notion is unknown. The notion is about socket naming, not executables; per spirit, a notion binds only when the need matches it exactly.
5. Unknown: whether any input at 682508d4 rebuilt wdj0sc…-codex-0.153.4 at all. If none did, cause 1 left no pinned-input path without new packaging. Settling this needs an evaluation of the old corePackages.codex at the 0.153.4 manifest on the remote builder.
6. W, for e11475: the Bird extension copied the same pattern, because Field asked for unit-byte preservation and 42265e supplied Bird's live store path as the target.

## 4. Correct resolving form and runtime effect, per live site

Live state on ouranos at 19:20-19:30 CST (W):
- `codex-remote-control` runs as MainPID 1936 (0.153.4, up since 2026-09-26 16:19, NRestarts 0), listening on ~/.codex/app-server-control/app-server-control.sock with 0 unix clients and 1 TLS connection to a Cloudflare 443 endpoint.
- `codex-remote-control-next` runs as MainPID 1960 (0.158.0-alpha.9, up since 2026-09-26) with 0 unix clients and no TCP.
- The candidate `codex-remote-control-next-8mkkxq293hk2` runs as MainPID 1965146 (0.161.0-alpha.2) with 21 client processes and about 25 TLS connections.
- The current Home generation's closure contains zbznvq… (codex-next 0.158). It does not contain wdj0sc… (0.153.4) or dxqsqx… (prepare). Those two are kept only by runtime roots (/proc of PID 1936) and /run/booted-system.

| Site | Resolving form | Runtime effect of replacing it |
|---|---|---|
| codex-remote-control.nix:24 | `"${codexCliPackage}/bin/codex"`, already the non-occupied branch (`config.criomos.corePackages.codex`, 0.163.0); or, to hold 0.153.4, a typed option whose value is a package pinned by input | W, for li: ExecStart changes, so sd-switch restarts PID 1936 (`Restart=always`). Its one remote-control TLS session drops and any thread loaded in it is interrupted; no local unix client is attached now. The server comes back on 0.163.0 over ~/.codex state; whether 0.163 migrates that state one way is unknown. For Bird on Zeus the same applies to her stable server; Zeus was not observed. |
| codex-remote-control.nix:25 | `"${config.criomosHome.codexNext.rawClientPackage}/bin/codex"` | I: if that package evaluates to zbznvq… (consistent with zbznvq… being in the current closure), the `codex` wrapper is byte-identical. Otherwise only new `codex` launches change. No server restarts; running clients keep their process. |
| codex-next.nix:16 | `"${package}/bin/codex"` (non-occupied branch) | I: identical ExecStart if `package` evaluates to zbznvq…. |
| codex-next.nix:17 | `"${prepare}"` (non-occupied branch) | W: the current `prepare` text adds two "# Bird keeps …" comment lines inside the script that the pinned dxqsqx… lacks. Its output path therefore differs, ExecStartPre changes, and sd-switch restarts PID 1960. 1960 has no clients now; Flow's routing to it was not checked. The Bird branch is dead code; removing it has no effect. |
| herdr.nix:53-54 and checks/herdr-toast-delivery:131-132 | Admit the predecessor through the typed `criomosHome.herdr.predecessorGeneration` contract or HM's `$oldGenPath` content check, or retire the admission once no host holds that file | Activation only; no service. A host whose ~/.config/herdr/config.toml still equals that predecessor would have its activation refuse adoption. On ouranos the file is a dangling link into an absent store path (…-primary-committer-restarter-deployment), so neither predecessor applies here; who wrote that link is unknown, and how activation handles it was not observed. |
| lib/primary-committer-hook-trust.nix:7 | `${pkgs.nodejs-slim}/bin/node` with the proof script packaged as a derivation instead of private-repos evidence paths; `hash` computed in Nix from the resolved command rather than written literally | The candidate config.toml hook key and `trusted_hash` change on activation (hexis mode "always"). W: the current file holds `trusted_hash` 20b644…. I: Codex would treat the changed SessionStart hook as untrusted until the new hash is merged; no server restart unless the candidate unit itself changes. |
| packages/harness-profile/default.nix:4, :12 and owned-rust-exports.json | baseline: `homeConfigurations.<user>.config.home.path` or a flake input carrying the accounted baseline; oldChatgpt: the previous chatgpt package from a pinned input; rust targets: `"${rust}/bin/<name>"` from `inputs.self.packages.${system}.rust-toolchain` | W: `harness-home-profile` is installed in li's nix profile and its closure includes k6mwx3… and kds5yv…. Replacing changes the profile output; the next profile upgrade changes which applications and Rust entrypoints sit on PATH. No service restart. Pure evaluation becomes possible (`builtins.storePath` needs impure mode, per the 2b0163 message, C). |
| CriomOS modules/nixos/userHomes.nix:17-32 | Retire after Zeus adoption, or supply from the cluster's host data repo as typed values; a general repo keeps no setup-specific host value. HM's `$oldGenPath` already covers the previous generation (herdr.nix:258-263) | Zeus only, at Home activation: it decides whether existing Herdr config and the Kvantum link are adopted. Removing it before adoption completes could make Zeus activation refuse; Zeus state was not observed. |
| lojix-test modules/immutable-converter-replay.nix:20-21 | Build the converter from a flake input pinned at its revision (as `helperSource` already does for the helpers), or a published artifact fetched by content hash | Test only. W: l04p8r… is absent from the ouranos store, so this check cannot build here. A rebuilt converter replays a rebuilt binary, not the original immutable one; whether that still serves the test's purpose is the test owner's question. |

## Open items needing a ruling or an observation

- Whether the ruling covers synthetic fixtures (1c) and profile-path literals (1e).
- History removal: 19 main-reachable commits, 13 on remote branches only, 37 in local jj keep refs. Rewriting main changes every downstream lock that pins these repos; 41fa34 records 12 lock edges (C, flow-evidence/41fa34/nix-store-literals-20261018/affected-repository-lock-edges.json). Unreachable objects already on GitHub are not removed by a force-push (I, from general GitHub behavior; not witnessed here).
- Zeus: Bird's live stable and next units and the presence of wdj0sc… there were not observed.
- Whether `pkgs.callPackage owned-agents/codex-next {}` evaluates to zbznvq…; settling it needs an evaluation on the remote builder.
