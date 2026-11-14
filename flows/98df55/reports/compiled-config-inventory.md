# Configuration the Flow Nexus and its clients take from outside Memory, the meta socket or the place file

Flow worktree `pko0-90d453` at 291b73e6; CriomOS-home `pko0-90d453` at 8c0abbcd.
Contract: meta-signal-flow cdb4e7d (`ethos/signal.ethos`). Paths below are relative to `crates/` unless they say otherwise.
Production means the daemon `flow-nexus-daemon` (crates/flow-nexus, outside `#[cfg(test)]`), the CLIs `flow-nexus`, `flow-nexus-hook` (crates/flow), `flow-nexus-meta` (crates/flow-meta), and flow-place.

Classes. A: derived from the place. B: a family the meta contract already carries, also defaulted in code. C: no meta variant sets it. D: fixed.

## How an unconfigured Nexus answers today (applies to every A/B/C row)

`RunningNexus::open` (flow-nexus/src/lib.rs:1549) makes a new memory empty and opens it with `open_configured`, which seeds no Nexus family. While no `Configure.Nexus` is committed:
- Meta `Configuration` / `ObserveConfiguration` answers `Unconfigured` (lib.rs:2139).
- Ordinary `Start`/`Launch`: `launch_session()` answers NotConfigured, and the Start is answered `StartRejected.LaunchPersistenceRefused` (launching.rs:241-254). A missing model is answered the same way (launching.rs:259-262). It is not answered `CompositionRefused.Unconfigured`.
- A root that is empty or relative is answered `StartRejected.CompositionRefused.Unconfigured` (launching.rs:213-228). A fresh wake with no configured model gets the same answer (waking.rs:3505-3517), and so does a failed successor start (sending.rs:1510-1516).
- The Curriculum composer is `CurriculumComposer::at("")`, so a composition answers `ContextRefusal::ComposerUnavailable` (context.rs:238).
- `HerdrCli.flows_root` becomes the relative path `flows` (`with_source_root("")`, herdr.rs:451). The unit's working directory is `%h`, so this resolves to `~/flows`.

## Table

| # | file:line | value | read by | class | if Memory lacks it / where it surfaces |
|---|---|---|---|---|---|
| A1 | flow-ethos/src/place.rs:37 | `flow.sock` | daemon place.rs:21 (binds it); CLIs `PlaceSockets::ordinary_in`; Claude hook configuration | A: `<Runtime>/flow.sock` | Not a Memory value. The place file has no Runtime: the daemon exits `Missing.<path>` (main.rs:96-101) and the CLIs refuse before sending. |
| A2 | flow-ethos/src/place.rs:38 | `flow-meta.sock` | daemon main.rs:121; flow-meta | A: `<Runtime>/flow-meta.sock` | as A1 |
| A3 | flow-nexus/src/place.rs:16 | `flow.sema` | `RunningNexus::open` | A: `<State>/flow.sema` | as A1 |
| A4 | flow-ethos/src/place.rs:69-70 | `flow-nexus`, `nexus` | flow-place `nexus_name()`; `ConfigurationFile::under` | A: names the place-file path `<config home>/nexus/<place>/flow-nexus.signal` and the CLI file | as A1 |
| A5 | flow-place/src/lib.rs:76-77; translator `ConfigurationHome::of_process` (via flow-place/src/lib.rs:38); flow-ethos/src/place.rs:85-95 | env `XDG_CONFIG_HOME`, else `HOME`/.config | daemon (main.rs:96) and both CLIs, to locate the place file and the CLI file | A: how the place file is found | No config home: refused `Unlocated`/`Missing` before anything binds or sends |
| A6 | flow-ethos/src/place.rs:105 (file), flow-place/src/lib.rs:96-105 | `<config home>/nexus/flow-nexus.datom`, `{ <place> }` | CLIs only, for the place name | A: the place name, which the daemon gets as argv | CLI refused `Missing.<path>`, exit 2 |
| A7 | flow-nexus/src/herdr.rs:217 | `ordinary_socket = <XDG_RUNTIME_DIR>/flow/flow.sock` (flow-defaults) | `HerdrCli::default` | A: placeholder for `<Runtime>/flow.sock` | Always replaced by `with_ordinary_socket(place)` (lib.rs:1579), so inert. The env is still read. |
| A8 | flow-defaults/src/lib.rs:80-83, 47-49, 62-64 | env `XDG_RUNTIME_DIR`, else `/run/user/<uid>` with uid from `/proc/self` | `from_environment` (called in production at herdr.rs:162 via lib.rs:1575) | A: the old runtime anchor | Feeds A7 and A9 only |
| A9 | flow-defaults/src/lib.rs:94-98 | `.local/state/flow`, `flow.sema`, `flow`, `flow.sock`, `flow-meta.sock` | `LaysOutDefaults` → `SeedsConfiguration::socket_configuration` (store.rs:364) → legacy `FlowStoreConfiguration` | A: old layout, now the place's | Only on the dead seeding path (B16). Duplicates A1-A3. |
| B1 | flow-nexus/src/herdr.rs:209-215, 247-268 | `<dir of current_exe>/flow-nexus-hook`, else bare `flow-nexus-hook` | `HookChoice::harness_hook` → Claude flag settings (herdr/launch.rs:478-487) | B: `HarnessHook.Path` | Unconfigured, or a relative path: the hook beside the daemon is written into every Claude launch. Nothing refuses. |
| B2 | flow-nexus/src/store/delivery.rs:93-101, 114-139 (also store.rs:388-392) | Claude `[/ ! #]`, `esc esc`, `enter`; Codex `[/ !]`, `esc`, `[]` | `SelectsHarnessProfile::profile` for typing into panes | B: `Nexus.ConfigureNexus` HarnessProfiles / `Harness.HarnessProfile` | A configured Nexus missing a kind gets the code profile with no notice. With no Nexus at all, `delivery_configuration()` reads the legacy record and answers `StateInvariant`. |
| B3 | flow-nexus/src/store.rs:155-156, used 1700-1716 (called from `open_configured_in_place`, store.rs:2790), 5976-5977, 6732, 6753 | draws 64, tries 3 | request-id drawing and announcements | B: `RequestIdDraws` / `AnnouncementTries` | Written into Memory at every configured open when absent, then read from Memory |
| B4 | flow-nexus/src/store.rs:210, 5972 | 30 minutes | default Minutes of a request that names none | B: `DefaultMinutes.Minutes` | Read-time fallback; Configuration reports 30 |
| B5 | flow-nexus/src/store/handover_configuration.rs:154; handover_archive.rs:208 | 60 000 ms | handover archive publication deadline | B: `PublicationDeadline.Duration` | Read-time fallback |
| B6 | flow-nexus/src/store/queue_delivery.rs:87-89 | first attempt 3, next request 2 (`{1 3 1}`) | counters on an empty store | B: `Counters.ConfigureCounters` (partly D: Codex reserves ids 1-2) | Seed values |
| B7 | flow-nexus/src/herdr.rs:175-203 | `/fixture/codex`, `~/.codex`, `~/.codex/app-server-control/...sock`, `gpt-5.6-sol`; `/fixture/codex-next`, `~/.codex-next`, `gpt-6-*`; timeout 10 s | `HerdrCli::default` | B: `Nexus.ConfigureNexus` Codex endpoints | Replaced by `with_codex_endpoints` (lib.rs:1577) with the configured endpoints, or with empty ones when unconfigured, so inert |
| B8 | flow-nexus/src/herdr.rs:170-176 | `~/primary/flows` | `HerdrCli::default` flows_root | B: `ConfigureNexus` SourceRoot | Replaced by `with_source_root`. Unconfigured, it becomes the relative `flows` (see the unconfigured section). |
| B9 | flow-defaults/src/lib.rs:75-79, 53-60 | env `HOME`, else `/etc/passwd` home of the uid, else `/` | `from_environment` (production via herdr.rs:162) | B: the anchor of B8, B10-B13 and of C5 | Its one live consumer is C5 |
| B10 | flow-defaults/src/lib.rs:99 | `primary` → `~/primary` | `source_root()` → herdr.rs:170, store.rs:377 | B: `ConfigureNexus` SourceRoot | as B8 / B16 |
| B11 | flow-defaults/src/lib.rs:100-102 | `codex-stable-flow-client`, `.codex`, `[gpt-5.6-sol gpt-5.6-luna]` | `stable_codex()` → store.rs:378 | B: `ConfigureNexus` first CodexEndpoint | Dead seeding path only (B16) |
| B12 | flow-defaults/src/lib.rs:103-105 | `codex-next-flow-client`, `.codex-next`, `[gpt-6-sol gpt-6-luna gpt-6-astra]` | `next_codex()` → store.rs:379 | B: `ConfigureNexus` second CodexEndpoint | as B11 |
| B13 | flow-defaults/src/lib.rs:106 | `app-server-control/app-server-control.sock` | `codex_endpoint()` | B: CodexEndpoint ControlSocketPath | as B11 |
| B14 | flow-defaults/src/lib.rs:107, 137-139 | `<runtime>/curriculum/curriculum.sock` | `curriculum_socket_path()`; no production caller | B: `ConfigureNexus` CurriculumNexusPath | Dead code; unconfigured gives ComposerUnavailable |
| B15 | flow-nexus/src/store.rs:393-394 | MetaAspects `[Psyche]`, Message Nexus None | `SeedsConfiguration::delivery_configuration` | B: `ConfigureNexus` MetaAspects / MessageNexusPath | Dead seeding path only |
| B16 | flow-nexus/src/store.rs:344-397 (`SeedsConfiguration`), 2071-2097 (`ConfigurationOnlyStore::configuration(&defaults)`), 2173-2194 (`OpensFlowStore::open_seeded`; `open()` = `open_seeded(path, &DefaultConfiguration::from_environment())`), 2799-3044, store/delivery.rs:320-339; Cargo.toml:14 `flow-defaults` | the whole default layout | compiled into the daemon; callers are tests only (store/reminder.rs:301, store.rs tests, tests/unit/*) | B (with A9 inside it) | Unreachable from main.rs today. Any production call of `FlowStore::open` seeds Memory from the environment. |
| C1 | flow-nexus/src/herdr.rs:173 → emission.rs:399, 424 | `herdr` (looked up on the unit's `PATH`) | every Herdr command | C (no `HerdrBinary`) | Not in Memory. Failure shows as Herdr-unavailable: `StartRejected`, `RebindRejected.HerdrUnavailable`, `MetaBindExisting` `HerdrUnreadable`. |
| C2 | flow-nexus/src/herdr.rs:174 → emission.rs:632 | `flow-id` (on `PATH`) | flow-identity claim and verification | C | Failure: no claim, so `current_route` is None (herdr.rs:283) and a Start or Send finds no route |
| C3 | flow-nexus/src/handover_archive.rs:192 | `git` (on `PATH`) | handover archive commits | C | `HandoverArchiveRefusal` |
| C4 | flow-nexus/src/emission.rs:130 (only Codex gets `--executable`) | Claude executable: Herdr's `--kind claude` default, on Herdr's or the unit's `PATH` | Claude `agent start` | C (Codex has ClientPath; Claude has nothing) | Start fails at the Herdr agent start |
| C5 | flow-nexus/src/herdr.rs:167-169, 205-207; claude.rs:38-39, 136 | env `CLAUDE_CONFIG_DIR`, else `$HOME/.claude` → `projects/`, `jobs/`, `daemon/roster.json`, `sessions/` | transcript reading, title and readiness waits, session-of-process | C (no Claude home in ConfigureNexus) | Wrong or absent: Claude binds and readiness fail. Shows as `SessionUnreported`/`SessionUnproven` on BindExisting, title-wait timeout on Start. |
| C6 | flow/src/hook.rs:293-296 | env `CLAUDE_CONFIG_DIR`, else `$HOME/.claude` | `flow-nexus-hook`, to find its harness process | C (the hook's argv carries only `HookConfiguration{ OrdinarySocketPath }`) | The hook reports without a harness |
| C7 | flow-nexus/src/herdr.rs:218-221 | title_wait 10 s, rest_wait 30 s, submission_wait 5 s, render_wait 1 s | launch, prompt and submission | C | Constant |
| C8 | flow-nexus/src/herdr/launch.rs:1971, 562 | StartAgent timeout 30 000 ms; pane-output wait 5000 ms over 50 lines | launch | C | Constant |
| C9 | flow-nexus/src/herdr/pane.rs:54-64 | 3 interrupt presses × 3000 ms, composer 12 lines, rest wait 15 000 ms | pane writer | C | Constant |
| C10 | flow-nexus/src/codex.rs:90, 187 | Codex app-server timeout 10 s | `CodexEndpoints::from` | C (CodexEndpoint has no timeout) | Constant |
| C11 | flow-nexus/src/emission.rs:568, 570 | Curriculum exchange 30 s, answer frame 64 MiB | composer | C | Constant |
| C12 | flow-nexus/src/emission.rs:718 | Herdr socket reply 30 s | Herdr socket prompts | C | Constant |
| C13 | flow-nexus/src/restarting.rs:98, 102 | automatic reopens 1; spawned-exit wait 3 s | restart (the comment there says this would need a family) | C | Constant |
| C14 | flow-nexus/src/compacting.rs:44 | 600 s compaction watch margin | compaction watch | C | Constant |
| C15 | flow-nexus/src/store/reminder.rs:26 | 4 task reminders ("Ruled 2026-10-29") | task reminders | C, or D if the ruling fixes it | Constant |
| C16 | flow-nexus/src/lib.rs:1748-1749 | socket read and write timeout 5 s | every connection | C | Constant |
| C17 | flow-nexus/src/sending.rs:1407 | direct-send settlement wait 10 s | Send | C | Constant |
| C18 | flow-nexus/src/lean.rs:19 | 15 Claude deferred-tool names | leave-outs | C (tracks the Claude Code version) | Constant |
| C19 | flow-nexus/src/context.rs:48; waking.rs:555; store/request_id_upgrade.rs:19-20 | prompt and notice texts | composed context and notices | C (strings held in code) | Constant |
| C20 | flow-nexus/src/herdr.rs:441, 452; codex.rs:824 | the flows directory `flows` under the source root | flow directories; `flow-id --flows-root` | C (or D as Flow's own layout convention) | Constant |
| C21 | flow-nexus/src/codex.rs:294-297 | Codex history page 16 × 16 pages | turn history reading | C | Constant |
| D1 | flow-nexus/src/lib.rs:2637 | env `NOTIFY_SOCKET` | readiness | D: systemd's protocol | — |
| D2 | flow/src/hook.rs:306 | env `FLOW_ID` | hook | D: the process's own flow identity, set at launch | — |
| D3 | flow-nexus/src/herdr/launch.rs:995; herdr.rs:735, 870 | `claude`, `codex` | Herdr agent kinds | D: Herdr's vocabulary | — |
| D4 | flow-nexus/src/herdr/launch.rs:442-454; emission.rs:110, 637 | `CLAUDE_CODE_CHILD_SESSION`, `CLAUDE_JOB_DIR`, …, `FLOW_LAUNCH_REQUEST_ID`, `CODEX_SESSION_ID` | environment hygiene and hand-off | D: interface names of Claude, Flow and flow-id | — |
| D5 | flow-nexus/src/codex.rs:497 | `app-server proxy --sock` | Codex client | D: Codex CLI protocol | — |
| D6 | flow-nexus/src/codex.rs:170 | `<Codex home>/sessions` | transcripts | D: Codex's layout under its configured Home | — |
| D7 | flow-nexus/src/lib.rs:2700; sending.rs:51 | frame 1 MiB; send payload 64 KiB | wire | D: the contract's limits (`Oversized`) | — |
| D8 | flow-nexus/src/store/living_upgrade.rs:464 | `default` Herdr session | 0.54.x upgrade only | D: historical fact | — |
| D9 | flow-nexus/src/store.rs:113-210, 328 etc. | table, family and schema names; engine layout 7 | storage | D: storage identity | — |
| D10 | flow-nexus/src/binding.rs, caller.rs, claude.rs:145 | `/proc/<pid>/…` | process identity | D: kernel interface | — |
| D11 | flow-nexus/src/main.rs:27, flow/src/main.rs:67, codex.rs:887 etc. | `CARGO_PKG_VERSION` | `--version`, client info | D: build identity | — |
| D12 | flow-nexus/src/main.rs:49-52 etc. | datom reader budgets 65 536 / depth 1 024 | argument parsing | D: parser bounds | — |

Counts: A 9, B 16, C 21, D 12.

## Nix

- The flake generates no Rust from Nix and no configured daemon. `packages.default` is `workspaceBinaries` (flake.nix:463-470), and flow-nexus has only the `datom` feature (crates/flow-nexus/Cargo.toml:9-11). This matches UPGRADES.md:29-37.
- One residue remains: `migration-predecessor.lib.mkFlowPackage { defaultConfiguration = … }` (flake.nix:259-285). It builds the 0.53.2 predecessor for the request-id migration test fixture only.
- CriomOS-home `flow-nexus-place.nix` builds the configuration as datom queries (`nexusQuery`, lines 151-159) and replays them through `flow-nexus-meta` (lines 219-237). The place file is compiled at activation (lines 403-409).
- The unit sets no environment (lines 433-440), but the systemd user manager still gives it `HOME`, `PATH`, maybe `CLAUDE_CONFIG_DIR`, and `NOTIFY_SOCKET`. Of these the daemon reads `HOME` and `CLAUDE_CONFIG_DIR` (C5, B9), and `PATH` decides C1-C4.
- The module header's "Nothing else reaches the unit: no environment" is therefore not quite true of the daemon.
- `stableCodex.home` is `~/.codex-next` (line 85) while the code default is `~/.codex` (B7, B11). This is unrelated to the ruling but worth a look.

## Ambiguous

- A5 and A6: finding the place file needs `XDG_CONFIG_HOME`/`HOME`, and the CLIs read the place name from `flow-nexus.datom`, a second file beside the place file. I classed both A, as the means by which the place file is reached. Strictly, the ruling's "nothing read from the environment" is broken by A5.
- B6: the counter seeds `{1 3 1}` are partly protocol, since Codex reserves request ids 1-2. Only `LogicalDelivery`/`SendOutcome` = 1 is a true default.
- B16: dead in the running daemon, yet compiled in and public. `OpensFlowStore::open` defaults to `from_environment`, so any new caller seeds Memory from `HOME`/`XDG_RUNTIME_DIR`. Removing it touches about 20 test sites that build `DefaultConfiguration { home, runtime_directory }` to get a `ConfigureNexus`.
- `HerdrCli::default` (lib.rs:1575 → herdr.rs:160): every placeholder except C1, C2, C5 and C7 is overwritten at open (lib.rs:1575-1579). So the environment read survives only to supply the Claude home and the executable names.
- C4: whether the Claude executable is Flow's to configure (a ClientPath like Codex has) or Herdr's (its kind default) is a design question.
- C15: TASK_REMINDERS cites a ruling, so it may be meant fixed (D).
- C20: `flows` under the source root could be a fixed Flow layout (D) rather than configuration.
- Not classed: bounded buffers (codex.rs:30-31, handover_archive.rs:26 1 MiB capture, claude.rs:444 4 MiB tail, codex_turns.rs:99, submission.rs:43, handover_observation.rs:12, the 64 ancestry limits). I read them as resource bounds (D-like), not configuration.
- A Start on an unconfigured Nexus answers `LaunchPersistenceRefused`, not `CompositionRefused.Unconfigured` (launching.rs:251-254). That is where a "not configured for it" answer would belong.
- Stale docs: README.md:314 and NON_IDEAL_AGENTS.md:9, 24 still describe `flow-defaults` anchors as the default layout.
