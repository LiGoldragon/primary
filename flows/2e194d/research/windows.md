# Model refresh windows — mvjh

Field upkeep a4f252, 2026-11-18. **Status: evidence gathered; accepted changes below are NOT YET APPLIED.** Field core owns the 0.60.1 activation boundary and has required all configuration/watcher writes to wait for its explicit release once 0.60.1 is live.

## All eight models

“Before” is the actual pre-change `flow-meta Configuration` reading, not a value inferred from a source checkout. “Accepted after” is Opus120x's authorized target; it is not yet a live readback.

| Model | API identifier | Refresh before | Accepted after | Status |
|---|---|---:|---:|---|
| Fable | `claude-fable-5-2` | 330000 | 330000 | Preserve exactly |
| Opus | `claude-opus-5-5` | 280000 | 280000 | Preserve exactly |
| Sonnet | `claude-sonnet-5-5` | 280000 | 280000 | Preserve exactly |
| Haiku | `claude-haiku-5-5` | 200000 | 200000 | Preserve exactly |
| Astra | `gpt-6-astra` | 210000 | 220000 | Compaction-capped increase |
| Sol | `gpt-6.1-sol` | 210000 | 300000 | Rounded 40% increase |
| Luna | `gpt-6-luna` | 210000 | 220000 | Compaction-capped increase |
| Terra | `gpt-6.1-terra` | Unconfigured: no Flow mapping or threshold | 300000 | New mapping + threshold authorized by Opus120x; not yet configured |

The old API id `claude-fable-5-1` also has a live330000 threshold and must remain330000. Every existing Claude entry is retained, not reconstructed from defaults.

Other existing OpenAI native entries, retained even when not selected by the current role aliases:

| API identifier | Before | Accepted after |
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

## Watchers: before and accepted after

The current watcher units are eight transient user services, all previously `SIZE=300000 --margin50000`. Source `makeshift-tools/codex-context-watch.clj` uses SIZE for the first MiddleAbrupt handover order and SIZE+margin for the second HardAbrupt handover order. **The “hard stop” wording denotes this hard-priority request; the script does not forcibly stop a process.**

| Units / role | Before first + margin → hard request | Accepted after |
|---|---|---|
| Field core Sol; Mind core/flowNexus/harnessNexus/messengerNexus/subscription/versionZero Sol | 300000 +50000 →350000 | 300000 +50000 →350000 (unchanged) |
| Field heartbeat Luna | 300000 +50000 →350000 | 220000 +10000 →230000 |

Sol's hard request is100000 below its recorded450000 compaction point. Luna's planned hard request is14800 below its source-derived244800 point. No Astra or Terra watcher unit was present in the captured unit list; no nonexistent watcher is claimed updated.

## Persistence and activation ordering

Field core Result7k94: old Flow0.59.3 restored/resumed after activation658 failed before the Home script; next0.60.1 activation follows Lojix repair. Homeac9 is configuration-free; Flow Memory owns configuration. The legacy checkout `packages/flow-deployment/default.nix` contains stale150000/Claude200000 replay declarations and is **not evidence of a deployed replay**.

Opus Resultap4b clarifies that persistence means live Flow Memory, not a new Home/startup replay. Opus Notice120x then supersedes its earlier Terra-gap disposition and authorizes adding the Terra mapping. Home remains configuration-free. Required order:
1. Field completes0.60.1 activation and explicitly releases configuration custody.
2. Re-read fresh live configuration; preserve every unrelated field and all Claude entries. Apply only the accepted OpenAI mappings/thresholds through the meta socket, plus corresponding existing watcher settings. Field isgv reports accepted0.60.1 source supports Terra, but the saved next-Codex endpoint permits only gpt-6.1-sol/gpt-6-sol/gpt-6-luna/gpt-6-astra. Extend only that endpoint permitted-model vector with gpt-6.1-terra using whole-family Configure.Nexus, preserving all other fields. Mapping alone is insufficient. Configure.Models and Configure.Thresholds also replace whole families, so every existing entry must travel in each replacement. Existing Flow owner ppek supplies acceptedfe5 `model.rs:19–36` (Terra supported), meta89 be69365b `ethos/signal.ethos:467–470,568–599` (whole-family syntax), `codex.rs:107–115` and `store.rs:6894–6910` (each native model must belong to exactly one endpoint), and `lib.rs:2317–2338` (endpoint configuration applies without daemon restart). Append `{ Terra gpt-6.1-terra }` to the intact Models vector and `{ gpt-6.1-terra 300000 }` to the intact Thresholds vector. Single-native threshold syntax `Configure.Refresh.{ gpt-6.1-terra 300000 }` is also supported, but does not establish the alias or route. No provider probe is authorized or claimed.
3. Read back all model mappings and thresholds, proving the Claude entries unchanged and that Terra's configured routing is supported.
4. Field26z7/lq8b requires persistence verification at the **next independently authorized or natural Flow restart**, with exact configuration-family capture after update and before/after that later event. No restart solely for proof is authorized, no event/time is promised, and the0.60.1 start occurs before these changes so cannot prove their post-update persistence. No independent daemon restart has been initiated here.

**Actual after-values and watcher mutation receipts: pending activation release. Post-update restart persistence verification: pending a later independently authorized/natural restart.** No threshold/model/watcher write has occurred in this report's work so far.

## Evidence custody

`/tmp/mvjh-windows-a4f252.R6kCR6pU/` holds `configuration-before.datom`, filtered `model-context-records.json`, exact `sol-compaction-record.json`, `watcher-units-before.txt` and `watcher-definitions-before.txt`. Sol record SHA256be7a3591df2ed7220596cf17a8a3c7f9acd0fbcd4ba7f0848174dfe967344cc3; initial whole configuration SHA2560683baf1a242d8556c11e1774b3fa670da6645ca61e9351c3aad0d8bc09a3af1. Configuration contains mutable traffic counters, so this historical whole hash is not a future equality oracle. No auth file was read, and no evaluation/build/provider call was started to collect these records.
