# Model refresh windows — mvjh

Field upkeep a4f252, 2026-11-18. **Status: live model routing/aliases/thresholds and watcher settings APPLIED AND READ BACK after Field core’s explicit write release.** Applied2026-11-18 at about22:31 CST, after0.60.1 acceptance. No Flow daemon restart was requested or performed. Persistence across a later independently authorized/natural restart remains pending that event.

## All eight models

“Before” is the actual pre-change `flow-meta Configuration` reading, not a value inferred from a source checkout. “Read back after” is the positively verified live configuration after Opus120x/h25n and Field0vjh release. All three configured families were read back and checked.

| Model | API identifier | Refresh before | Read back after | Status |
|---|---|---:|---:|---|
| Fable | `claude-fable-5-2` | 330000 | 330000 | Preserve exactly |
| Opus | `claude-opus-5-5` | 280000 | 280000 | Preserve exactly |
| Sonnet | `claude-sonnet-5-5` | 280000 | 280000 | Preserve exactly |
| Haiku | `claude-haiku-5-5` | 200000 | 200000 | Preserve exactly |
| Astra | `gpt-6-astra` | 210000 | 220000 | Compaction-capped increase |
| Sol | `gpt-6.1-sol` | 210000 | 300000 | Rounded 40% increase |
| Luna | `gpt-6-luna` | 210000 | 220000 | Compaction-capped increase |
| Terra | `gpt-6.1-terra` | Unconfigured: no Flow mapping or threshold | 300000 | New mapping + threshold + exactly one next-endpoint route verified; provider serving capability not probed |

The old API id `claude-fable-5-1` also has a live330000 threshold and must remain330000. Every existing Claude entry is retained, not reconstructed from defaults.

Other existing OpenAI native entries, retained even when not selected by the current role aliases:

| API identifier | Before | Read back after |
|---|---:|---:|
| `gpt-5.6-luna` | 210000 | 220000 |
| `gpt-5.6-sol` | 210000 | 220000 |
| `gpt-6-sol` | 210000 | 220000 |

The cache also advertises `gpt-5.6-terra`, but Flow does not currently configure it. The requested new Terra mapping is specifically `gpt-6.1-terra`, not that older API id.

## Real compaction evidence and arithmetic

Codex's own current-home database `/home/li/.codex-next-5ck97j38j3sb/logs_2.sqlite`, row **3724404**, UTC **2026-11-19 03:52:50**, thread `01a1f141-1908-7612-a225-2d4a4f252678`, target `codex_core::session::turn`, explicitly records model `gpt-6.1-sol` and:

- `auto_compact_scope_limit=Some(450000)`
- `auto_compact_limit_scope=Total`
- `full_context_window_limit=Some(475000)`
- `total_usage_tokens=130597`, `token_limit_reached=false`

Thus **450000**, not the advertised500000 window or the effective475000 inference limit, is the recorded Sol auto-compaction threshold. This row records the threshold, not an actual compaction event. The watcher measures `last_token_usage.input_tokens`; Codex's compaction limit here is on total scope tokens, so these counters differ. A reserve is necessary and is not a guarantee against a single unusually large turn.

The same home's `models_cache.json`, fetched **2026-11-19T03:52:10.953381218Z**, advertises Sol6.1/Terra6.1 context500000, effective-context95%, and null explicit auto-compact limit. Astra6/Luna6/older Sol and Luna advertise272000. Exact local official release `rust-v0.161.0-alpha.2` (tag870b79feef9d4ecdd578b9f76f621c54f744bc31, commit5ccfcfe0fe510784521a3328b93f1c2fccc5e7a1), `codex-rs/protocol/src/openai_models.rs:525–535`, computes the default auto-compact limit as90% of context, capped by an explicit lower limit. This supports **244800** for272000-context models and450000 for500000-context models. Only Sol's450000 is additionally verified from the actual runtime record here; the other figures are cache-plus-release-source derivations, not measured compaction events or reproducible-binary identity claims.

Requested210000×1.4=294000. The accepted nice20k grid rounds this up to **300000**, a42.86% increase. Sol then has150000 tokens between refresh threshold and recorded compaction point.

For the smaller models,300000 would exceed244800. With a chosen minimum20000-token compaction reserve, the ceiling is224800; the largest nice20k-grid figure fitting is **220000**. That is only **4.76%** above210000: the compaction point caps their increase well below40%, as Opus120x explicitly accepted. Their refresh-to-compaction headroom is24800.

Terra has no live baseline to raise; its new300000 target is explicitly authorized to match Sol. Its cache500000 window and source-derived450000 compaction leave the same planned150000 reserve, without a Terra runtime-threshold witness yet.

## Watchers: before and verified after

The eight existing watcher units were transient user services, all previously `SIZE=300000 --margin50000`. Source `makeshift-tools/codex-context-watch.clj` uses SIZE for the first MiddleAbrupt handover order and SIZE+margin for the second HardAbrupt handover order. **The “hard stop” wording denotes this hard-priority request; the script does not forcibly stop a process.**

| Units / role | Before first + margin → hard request | Read back after |
|---|---|---|
| Field core Sol; Mind core/flowNexus/harnessNexus/messengerNexus/subscription/versionZero Sol | 300000 +50000 →350000 | 300000 +50000 →350000 (unchanged) |
| Field heartbeat Luna | 300000 +50000 →350000 | 220000 +10000 →230000 |

Sol's hard request is100000 below its recorded450000 compaction point. Luna's planned hard request is14800 below its source-derived244800 point. No Astra or Terra watcher unit was present in the captured unit list; no nonexistent watcher is claimed updated.

## Persistence, mutation receipts and activation ordering

Field core Result7k94: old Flow0.59.3 restored/resumed after activation658 failed before the Home script; next0.60.1 activation follows Lojix repair. Homeac9 is configuration-free; Flow Memory owns configuration. The legacy checkout `packages/flow-deployment/default.nix` contains stale150000/Claude200000 replay declarations and is **not evidence of a deployed replay**.

Opus Resultap4b clarifies that persistence means live Flow Memory, not a new Home/startup replay. Opus Notice120x then supersedes its earlier Terra-gap disposition and authorizes adding the Terra mapping. Home remains configuration-free. Completed order:
1. Field0vjh explicitly released writes after0.60.1 was live, configuration preservation and Send proof complete. Opus h25n also instructed immediate application. A fresh live Configuration was captured before mutation.
2. `Configure.Nexus` extended only the next endpoint permitted-model vector with `gpt-6.1-terra`; exact readback of the entire Nexus family matches that sole intended change. Terra occurs in exactly one endpoint. The accepted source owner’s pointers are `model.rs:19–36`, meta89 `ethos/signal.ethos:467–470,568–599`, `codex.rs:107–115`, `store.rs:6894–6910`, and `lib.rs:2317–2338`; endpoint reconfiguration needs no daemon restart.
3. Whole-family `Configure.Models` retained every original alias and appended Terra. Whole-family `Configure.Thresholds` retained all Claude entries exactly, changed only the six existing OpenAI thresholds, and added Terra300000. Typed `Configured.Nexus`, `Configured.Models` and `Configured.Thresholds` acknowledgements were retained. Exact intended Nexus equality, complete Models/Thresholds map equality, unchanged Claude values and unique Terra routing all passed readback checks. No other configuration family was written.
4. The Luna watcher received a persistent user-unit drop-in at `/home/li/.config/systemd/user/codex-context-watch-Field-heartbeat-Luna.service.d/override.conf`, through `systemctl --user edit --stdin`; only that watcher was restarted. Its live argv is220000 with10000 margin. The other seven Sol watcher argv remain300000 with50000 margin. All eight services read back active with the expected values. Drop-in SHA256`1408333899fd412ea600de057fd9ffe9f821780b57a675058a2dc1be6797454b`. The original service cohort is transient; no new boot-time watcher launcher was invented. The persistent drop-in retains Luna’s policy for this unit name when recreated.

Home stays configuration-free and no startup replay was added. Existing Home-source evidence places configuration in Memory/meta and starts the daemon without replay; Flow source owner points to `store.rs:3330,3421,6926` for threshold read/persistence and `store/context.rs:200–225` for consumption. This supports the existing persistence design, **not an observed post-update restart**.

**Later restart proof is still pending:** Field26z7/lq8b requires the next independently authorized or natural Flow restart, with exact family capture before/after it. No restart solely for proof is authorized, no event/time is promised, and the completed0.60.1 start occurred before these changes. Field owns that later proof. Terra provider capability remains unprobed.

## Evidence custody

`/tmp/mvjh-windows-a4f252.R6kCR6pU/` holds `configuration-before.datom`, filtered `model-context-records.json`, exact `sol-compaction-record.json`, `watcher-units-before.txt` and `watcher-definitions-before.txt`. Mutation packets/typed acknowledgements are `configure-{nexus,models,thresholds}.datom` and `configure-receipts.json`; live readback is `configuration-after-write.datom` with `configuration-readback-checks.json`. Watcher after-properties and all-eight checks are `watcher-properties-after.txt` and `watcher-readback-checks.json`. Sol record SHA256be7a3591df2ed7220596cf17a8a3c7f9acd0fbcd4ba7f0848174dfe967344cc3; initial whole configuration SHA2560683baf1a242d8556c11e1774b3fa670da6645ca61e9351c3aad0d8bc09a3af1. Configuration contains mutable traffic counters, so this historical whole hash is not a future equality oracle. No auth file was read, and no evaluation/build/provider call was started to collect these records.
