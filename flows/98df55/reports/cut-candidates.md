# Flow version 0 cut: removal candidates and their live callers

For the ruling (Fable ar7o): the cut of Flow version 0 is removal. A part with no vision line goes, and so does a second way to one effect, once no live flow, hook, client or Nexus calls it.

Sources:

- The audit is `flows/ddcdff/reports/flow-size.md`, §3 and §4.
- Every Flow `file:line` below is on flow origin/main `eabddc8d` (0.56.2), path `crates/flow-nexus/src/` unless another path is named.
- Contract lines are on signal-flow `4982eeb` (`sf:`) and meta-signal-flow `cdb4e7d` (`msf:`), the revisions that 0.56.2 pins, file `ethos/signal.ethos`.
- Every candidate below is still present unchanged on `pko0-90d453` `291b73e6`. Its 17 commits touch place and configuration start, not these files.

## The live world (read-only, 2026-11-14)

- **ouranos is the only host running Flow.**
  - `flow-nexus-0550.service` runs `/nix/store/nwwm7…-flow-configured-0.56.2/bin/flow-nexus-daemon` on `~/.local/state/nexus/main/flow.sema`, which is 77 MB.
  - `flow-configure-0550.service` replays ten datoms on every Nexus start. The journal shows them at 05:43:49–50.
- **zeus runs no Flow.**
  - It has no unit and no daemon, and `~/.local/state/nexus/main/` is empty.
  - It has only the 0.56.2 client and `~/.config/nexus/flow-nexus.datom` set to `{ main }`.
  - It holds one stale store, `~/.local/state/flow/flow.sema` (Oct 18), which nothing opens.
- **prometheus runs no Flow.**
- **The live configuration** is from `flow-nexus-meta 'Configuration'`, saved in the scratch copy `config.txt`:
  - MessageNexusPath and MessageNexusBinary are `None None`.
  - Heartbeat is `None`.
  - ProtectedAddresses is `[]`.
  - Counters is `{ 22309 5820 5536 }`.
  - HandoverArchive is unconfigured.
- **Caller evidence from transcripts.** This is every Bash command that executed `flow-nexus` or `flow-nexus-meta` in Claude and Codex transcripts from the last 14 days, excluding this flow's own. Search text is filtered out.
- **The hook.** Flow writes it into every Claude flow's `--settings` for SessionStart, UserPromptSubmit, PostToolUse, Stop and SessionEnd. Each one runs `~/.local/bin/flow-nexus-hook '{ /run/user/1001/nexus/main/flow.sock }'`, which sends only `Report` (`crates/flow/src/hook.rs:443,465,872-930`).
- **Other Nexuses that call Flow.**
  - energy-translator (running) calls `Observe.TurnEnds` (energy-nexus `crates/translator/src/flow.rs:197`).
  - energy-nexus calls `Send` through the client (`translator/src/lib.rs`).
  - Message's `message-nexus` calls the bridge inputs (`message/crates/message-nexus/src/flow_edge.rs:144-262`), but no Message Nexus runs on any host.
  - lojix, orchestrate, Curriculum and CriomOS call no Flow input.
- **What the skills tell flows to type.** The authored skills (psyche-, mind- and field-belief) name only `Send`, `Launch`, `Remind`, `Refresh`, `Queues`, `Answer` and, in flow-messaging, `Cancel`.

## Candidates, in proposed order (smallest risk first)

### 1. Heartbeat

- **What it is.**
  - `heartbeat.rs` (369 lines; loop at `:319-347`), started at `main.rs:201-204`.
  - It has two store families: `store.rs:162-165` (meta heartbeat configuration) and `:205-207` (heartbeat standings).
  - It adds a `Heartbeat` delivery purpose (`store/logical_delivery.rs`).
  - It is configured by `msf:497` `Heartbeat.Option<HeartbeatConfig>`.
- **Vision line.** None. The vision speaks against it:
  - `intent:design`: "Polling, in any form … is out of every design".
  - `vision/model-roles/0.md:47`: a Fable flow "takes no heartbeat".
- **Live callers.** None found.
  - The live Configuration holds Heartbeat `None`.
  - Outside the flow, meta-signal-flow and flow-nexus test repos, `Configure.Heartbeat` appears nowhere in /git (zoekt).
  - No transcript runs it.
  - The thread runs but sleeps on configuration change.
- **Risk.** Low for callers. The stored families stay registered in the running schema (`store.rs:2562,2585`), so dropping them is a stored-format change.

### 2. Meta ConsumeReset

- **What it is.** `msf:318`, handled at `lib.rs:1116-1135`.
- **Vision line.** None.
- **Live callers.** None.
  - Energy Nexus consumes Codex resets through its own emission `CodexConsumeReset` (energy-nexus `ethos/emission.ethos:4,15`; `crates/translator/src/lib.rs:274`) and never through Flow.
  - No transcript runs it.
- **Risk.** Low.

### 3. Recovery (`recovery.rs`, `bin/flow-recovery.rs`)

- **What it is.** A "Lojix Field recovery admission". Its own doc says "the installed recovery service *will* invoke" it.
- **Vision line.** None.
- **Live callers.** None.
  - `git grep` of lojix, CriomOS, CriomOS-home, orchestrate and Curriculum finds nothing.
  - The binary is shipped in the running package's `bin/` and nothing calls it.
- **Risk.** Low.

### 4. Store check (`store_check.rs`, `bin/flow-store-check.rs`)

- **What it is.** A deploy guard that opens a copy of the store.
- **Vision line.** None.
- **Live callers.** None in any deploy.
  - CriomOS-home origin/main has no `store-check`.
  - The only callers are Flow's own capsule (`capsule/flow-capsule.clj`, per `flows/4f3cb8/reports/052-final-codec-consumers.md:54`).
  - It ships in the package's `bin/`.
- **Risk.** Low. The capsule test needs a matching edit.

### 5. Meta Refresh and meta Restart (the duplicates)

- **What they are.**
  - `msf:322-323` declares them "as the ordinary Restart/Refresh, a protected Address's included".
  - Handlers are at `lib.rs:1310-1331`, and both call the same `self.nexus.restart` / `self.nexus.refresh` as the ordinary ones (`lib.rs:496-502`, `:964-970`).
  - The ordinary inputs are `sf:383` `Refresh.Address` and `sf:410` `Restart.FlowId`.
  - `sf:171` says that apart from the threshold refresh, every act on a protected Address is answered as for any other Address. The ordinary Refresh and Restart therefore already cover protected Addresses.
  - The meta forms exist only on the meta surface (contract, `lib.rs` MetaCall and `dispatch_meta_serially` at `lib.rs:2787-2799`). No client code builds them.
- **Vision line.** The ordinary ones have one. The meta duplicates have none.
- **Live callers.** No code, hook or Nexus calls them. Flows typed them by hand:
  - Session `1da0549e` (via `systemd-run`): `Refresh.{ Psyche book Haiku }` (11-09 22:07), `Refresh.{ Psyche core Sonnet }` (11-09 22:18, 22:49), `Refresh.{ Psyche core Fable }` (11-10 00:13), `Restart.9e8441` (11-10 05:11) and `Restart.c3c1a0` (11-10 13:49, 13:50).
  - Session `228e2b56`: `Refresh.{ Psyche core Opus }` (11-10 04:57).
  - Nothing after 11-10. The ordinary `Refresh` has 70 executed calls in 37 sessions, the last at 11-14 19:20.
- **Risk.** Low. Any habit of the meta form moves to the identical ordinary input.

### 6. Unconfigured or uncalled configuration families

- **What they are.** Inside `ConfigurationChange` (`msf:485-506`):
  - `Counters` (`:499`; it continues ids across a store replacement; `store/counters.rs`)
  - `RequestIdDraws`
  - `AnnouncementTries`
  - `HandoverArchive`, `HandoverCount` and `PublicationDeadline` (the handover archive, `handover_archive.rs`)
- **Vision line.** None.
- **Live callers.** None.
  - zoekt finds none of these `Configure.*` forms outside the Flow repos.
  - The Home configure unit sends none of them.
  - The handover archive is unconfigured: the journal logs `handover archive is ArchiveUnconfigured; closed generations retained` 13,611 times in 7 days.
- **Risk.** Low for callers. Each one keeps a stored family, so removing it is a format step. `Counters` stays as internal id state; only its Configure arm goes.

### 7. Meta Deliver and Vet (the inputs only)

- **What it is.** `msf:324-325`, handled at `lib.rs:1334-1350`.
- **Vision line.** None. Its own effect is "the one send path" (`vision/flow-nexus/0.md:85`), which Send already serves.
- **Live callers.**
  - No code calls them.
  - A Codex flow ran `flow-nexus-meta 'Vet.{ audit2bc724 … }'` once, on 11-12 07:58.
  - Meta `Deliver` was not executed in 14 days.
- **Risk.** Low to medium. `delivery.rs` (`DeliversMessages::deliver`) stays, because the drain uses it internally (`waking.rs:3752`, `successor_refused`). Only the two meta arms go.

### 8. Other queue, notes and observation inputs

| input | location | live callers |
|---|---|---|
| Push, Silence, Clear, ClearAll, Hot | `sf:416-421`, `lib.rs:1010-1048` | none in transcripts, repos or skills |
| Keep, Drop, Glance, Read | `sf:411-414`, `lib.rs:972-993` | none executed; a subagent's text on 11-10 calls the `Keep…`/`Drop…` lines retired |
| ObserveLegacyArchive | `msf:331` | none |
| Withdraw | `msf:339` | none |
| ResolveQueueDelivery | `msf:333` | none |
| ConsumeReset | `msf:318` | none (see item 2) |
| RegisterFlow | `msf:319` | none |
| MetaBindExisting | `msf:533` | none |
| Rebind | `msf:336` | none |
| ObserveSends, ObserveSender, ObserveDeliveries | `sf:402-404` | `message-nexus` (`flow_edge.rs:233,256`), not running; the flow CLI streams them (`crates/flow/src/client.rs:78-81`); one Codex use on 11-13 |
| Start, Replace, LaunchStatus, Observe.Launch | `sf:382,386-387`; `launching.rs:1` | `Start` 3 calls in one Codex session (11-05/06); `LaunchStatus` once (11-14 04:18, Codex) |

- **Vision line.** None for any of them. For each, the vision serves the effect through `Launch`, `DeliverAll`, `Queues`, `Cancel` or the debugging line.
- **Risk.**
  - Low for the inputs with no caller.
  - Medium for Start, Replace and LaunchStatus: `launching.rs` serves all four "from one durable account", and the refresh successor path shares it.

### 9. The Message bridge, with IdentifyThread and SendServers

- **What it is.**
  - `metaflow.rs:1-3`: "Bind, Identify, IdentifyThread, Lock, Deliver, Release, Acknowledge and ArchiveRequest, each taken from any caller".
  - The inputs are `sf:391-397,400`.
  - `ConfigureNexus` carries `Option<MessageNexusPath> Option<MessageNexusBinary>` (`msf:429`). `message_nexus_path` is read at `store.rs:1118-1121` and `store/delivery.rs:81`. `msf:38-39` itself says MessageNexusBinary is "configured and read by nothing".
  - SendServers (`store/send_server.rs`, `msf:492`) trusts the MCP send server `message-mcp-send` to name a Codex thread through IdentifyThread.
- **Vision line.** None. The vision names one send path (`vision/flow-nexus/0.md:85`).
- **Live callers.**
  - The only code that calls it is `message-nexus` (`flow_edge.rs:144` Bind, `:152` Identify, `:165` IdentifyThread, `:177` Lock, `:193` Deliver, `:206` Acknowledge, `:262` Release).
  - No Message Nexus runs on ouranos, zeus or prometheus: there is no unit and no `/run/user/1001/message`.
  - Home declares `messageNexus = null` (CriomOS-home `modules/home/profiles/min/flow-0550.nix`), and the live Configuration shows `None None`.
  - No Codex config wires `message-mcp-send` as an MCP server.
  - One manual `flow-nexus 'Identify'` was run by a Codex flow on 11-14 18:45, to debug.
  - The Codex send tool (`send_tool.rs`, 2,697 `send tool invocation Accepted` log lines this week) is Flow's own and is kept.
- **The configure unit is one caller.** It sends `Configure.SendServers` at every start (`flow-0550-send-servers.datom`, journal 05:43:50), and its `Configure.Nexus` datom carries the two `None` Message fields (`flow-nexus-place.nix:165-173`).
- **Risk.** Medium.
  - Removing SendServers and the two ConfigureNexus fields is a wire change. The Home configure unit's `nexusQuery` and `sendServersQuery` must change in the same change.
  - Message's `flow_edge` repins or is retired with it.

### 10. Store upgrade code and the frozen crates

The vision line is `vision/versioning/0.md:8`: "A change of the memory format is a new subversion, and carries the upgrade from the previous format". `vision/memory/0.md:19` says the same. That covers the upgrade from the format just before the current one. It does not cover keeping every earlier upgrade.

| part | upgrades from | taken on the live store |
|---|---|---|
| `store/request_id_upgrade.rs` (4,513 lines), `crates/{flow-ethos,signal-flow,meta-signal-flow}-before-request-ids` (3,002 generated lines; workspace `Cargo.toml:2`, `crates/flow-nexus/Cargo.toml:18-20`), `generated/send_tool_before_request_ids.rs`, `FlowMemoryEra::RequestIdPredecessor` (`store.rs:307-310`, recognised at `:5883`) | 0.53.2 Memory (frozen Flow 85bf0f1, signal-flow 3596923, meta-signal-flow b36597a) | yes: ouranos opens as `Current`; its store passed 0.53.3 and later |
| `store/event_upgrade.rs` | events-v5, written through 0.54.5 | yes |
| `store/living_upgrade.rs` (also used in the configuration-only open, `store.rs:1982`) | 0.54.2 → 0.54.3 (seven families) | yes |
| `store/reap_upgrade.rs` | launch outcome v9 (0.54.6) → v10 | yes |
| `store/leave_out_upgrade.rs` | permaflow v6 (0.54.7) → v7 (0.55.0); the upgrade from the previous format, the one the vision asks for | yes: journal `2026-11-13T23:50:31 … store upgrade: … takes its leave-outs … into its permaflow` (19 lines); no upgrade on the four starts since (01:14, 02:38, 04:39, 05:43) |
| `store/staged_open.rs` (`store.rs:2416`) | not a format: the first running open of a configuration-only store | a no-op on a running store (`begin` returns None) |

All of these run in `store.rs:2589-2668`, and on every open.

- **Live callers.** Every live store has taken them all. ouranos's is the only one.
  - Old copies do exist on ouranos: `~/.local/state/nexus/main-memory-backup-0542…0546-d99e39` and many `~/.local/state/flow-*`. Zeus also holds `~/.local/state/flow/flow.sema`.
  - Nothing opens any of these.
  - A rollback restore of `main-memory-backup-0546-d99e39`, which is in 0.54.6 format, would need `reap_upgrade` and `leave_out_upgrade`.
- **Risk.** Medium, because `request_id_upgrade` is not migration alone:
  - It registers three families in the `Current` era: `prior_deliveries`, `task_announcements` and `upgrade_assignments` (`store.rs:2594-2596`).
  - It runs `run_request_id_announcements` at every open (`store.rs:2799`) and after every meta Refresh and Restart (`lib.rs:2794`).
  - The legacy queue archive also runs at every open (`store.rs:2795` `archive_legacy_queue`; `store/queue_delivery.rs:593-732`) and feeds ObserveLegacyArchive.
  - Removing these is a stored-format step: the families are dropped by an evolution, or kept empty as `leave_out_upgrade` keeps its retired family.
  - I did not read whether `prior_deliveries` still holds open rows. That needs a store read.
  - `leave_out_upgrade` is the one carried upgrade. Removing it is in line with the ruling only once the next format step carries its own.

### 11. BindSeat, Adopt (seat binding)

- **What it is.** `sf:408-409`, `sending.rs:1-20`, `binding.rs`.
- **Vision line.** None.
- **Live callers.** Flows used them.
  - `BindSeat` was run 32 times across 11 sessions, the last on 11-12 00:33. It was used to re-register seats after a reboot: on 11-10 at 13:51–13:53 and 21:52–21:53 by sessions `b0c913d0`, `50e213f3`, `01493920`, `663f9845`, `6670d427`, `5d67fa19`, `16d726cb` and `c3c1a0db`.
  - `Adopt` was run twice by `678f2148` on 11-12 00:33.
  - Flow's own CLI tests reference both (`crates/flow-nexus/tests/unit/seat_binding.rs`).
- **Risk.** Medium to high. It is the observed recovery path for flows after a reboot or a lost binding, and nothing else replaces it until Flow re-binds its own seats.

### 12. Whole-family configuration

- **What it is.** `ConfigurationChange` whole families (`msf:485-506`) sit beside the one-at-a-time `Permaflow`, `Harness`, `Refresh`, `Amend` and `Remove` (`msf:503-510`).
  - Only three are true duplicates:
    - `Metaflows` (`:493`), beside Permaflow, Amend and Remove.Permaflow.
    - `Thresholds` (`:486`), beside Refresh and Remove.Refresh.
    - `Nexus.HarnessProfiles` inside `ConfigureNexus` (`:429`), beside Harness and Remove.Harness.
  - `Models`, `SendServers`, `HarnessFlags`, `HandoverPolicies`, `Investigation`, `DefaultMinutes`, `HarnessHook` and the rest of `Nexus` have no one-value form. Removing them removes the only way to set them, so they are not duplicates.
  - The audit also counts leave-outs as held twice, in the permaflow and in HarnessFlags.
- **Vision line.** `vision/flow-nexus/0.md:147`: "Configuration changes one value at a time". `vision/nexus/1.md:147` says the same. The whole-family forms have none.
- **Live callers.**
  - The Home configure unit `flow-configure-0550.service`, at every Nexus start. Its ExecStart datoms (journal 2026-11-14 05:43:49–50) are:
    - `Configure.Nexus.{ … }` (`flow-0550-nexus.datom`)
    - `Configure.Models.[ … ]`
    - `Configure.Thresholds.[ … ]`
    - `Configure.SendServers.[ … ]`
    - `Configure.HarnessHook.«…»`
    - `Configure.Metaflows.[ … ]` (25,790 bytes)
    - `Configure.HarnessFlags.[ … ]`
    - `Configure.Investigation.{ … }`
    - `Configure.DefaultMinutes.30`
    - `Configure.HandoverPolicies.[ … ]`
  - Its source is CriomOS-home origin/main `modules/home/profiles/min/flow-nexus-place.nix:165-214` with `flow-nexus-config/*.datom`. Its matcher is `case "$reply" in Configured.*` (`:236-238`).
  - Flows have also run them by hand:
    - `Configure.Metaflows` from a Codex session on 11-12 17:57–17:58, through `subprocess.run(['flow-nexus-meta','Configure.Metaflows.'+…])`.
    - `Configure.Amend` 8 times and `Configure.Harness` once (11-14), which are the one-value forms.
  - On pko0 a new memory starts unconfigured, and "a release replays the configuration through `flow-nexus-meta`, `Configure.Nexus` first" (pko0 `UPGRADES.md:1-37`).
- **Risk.** High. Every Nexus start depends on it.
  - Removing the three duplicate families requires rewriting the Home configure unit in the same change: one `Configure.Permaflow` per metaflows entry, one `Configure.Refresh` per threshold, and one `Configure.Harness` per profile with `HarnessProfiles` out of `ConfigureNexus`.
  - pko0's replay must change with it.

## Kept, not listed for removal

- The Codex app-server path and its send tool.
- Every input in flow-messaging.
- The Fable protection: `protecting.rs`, ProtectedAddresses.
- Kept answers, which `Answer` stands on.
- Turn ends: energy-translator subscribes to `Observe.TurnEnds`, and that service is running.
- HandoverPolicies: Home configures it, and the warnings tell flows to `Refresh`.
- `Observe.Agent`: flows used it 6 times, the last on 11-14.
- `Observe.Undecodable`: flows used it 3 times, the last on 11-11.
- The audit's other §3 items are refactors rather than removals: the Visible/private type pairs, the defaults in two homes, the fallback chains, compiled-in values and the state held twice. Each needs its own ruling.

## Unknowns

- Whether `request_id_upgrade`'s `prior_deliveries` and `task_announcements` still hold open rows on ouranos. This needs a store read.
- Whether pko0's unconfigured new memory still produces configuration-only stores. If it does not, `staged_open` and the configuration-only open also go.
- The transcript window is 14 days. A caller that runs less often than that would not show.
