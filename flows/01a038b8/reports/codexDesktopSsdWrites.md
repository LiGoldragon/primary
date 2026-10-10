# Codex Desktop SSD writes

As of 2026-08-25, the notorious high-write defect is substantially fixed, but the broader claim that current Codex Desktop is harmless to SSDs is not established. The original defect involved the shared Codex app-server/CLI persistence layer, so it was not confined to one desktop operating system. Current Linux evidence shows a quiet backend in one short idle sample and separate bursty Electron LevelDB compaction in another; neither is a sustained endurance measurement.

## What was real

Issue `openai/codex#28224`, opened 2026-06-14, reported about 37 TB of writes over 21 days on one system. The reporter traced the churn to `~/.codex/logs_2.sqlite` and its WAL/SHM files: a persistent TRACE sink stored full transport events, Responses WebSocket/SSE payloads, noisy dependency records, and duplicated telemetry while continuously pruning retained rows. The reported annual figure was an extrapolation from one system, not a controlled population result.

Official changes materially removed that path:

- PRs `#29432` and `#29457`, released in 0.142.0 on 2026-06-22, stopped full WebSocket-event persistence, duplicate telemetry, and several noisy targets.
- 0.142.5 stopped writing full Responses WebSocket request payloads to trace logs.
- PR `#29599`, released in 0.143.0, stopped persisting bridged log events.
- PRs `#31789`–`#31792`, released in 0.145.0, filtered large MCP, Hyper, tool-list, and streamed-response TRACE records.

These fixes support “the original amplification mechanism was substantially reduced.” They do not provide a before/after NAND-write benchmark.

## Linux now

OpenAI now documents an official Linux preview. The application inspected locally is not that official package: it is the third-party `ilysenko/codex-desktop-linux` Nix build `26.721.41059`, with Electron 42.3.0 and bundled Codex backend 0.148.0. The independently installed shell CLI is 0.149.1.

Read-only local observations returned by the investigation:

- The bundled 0.148.0 app-server performed no writes during one 10-second idle sample, and the historically noisy logging targets were absent.
- Electron wrote 4,943,872 bytes during a different 10-second sample while `~/.config/Codex/Local Storage/leveldb` compacted a roughly 4.67 MiB log into a roughly 1.85 MiB table. This witnesses bursty application-state churn, not a long-term write rate.
- Desktop-owned configuration, cache, and daily logs were small: about 7.9 MiB, 1.4 MiB, and 1.6 MiB respectively.
- Shared Codex state was much larger: `~/.codex` about 5.3 GiB, including roughly 3.4 GiB of sessions, a 779 MiB `logs_2.sqlite`, and a 782 MiB `thread_history_1.sqlite`. Several TUI/agent processes also use these stores, so their size or writes cannot be assigned to Desktop alone.

The shared backend makes Linux relevant to the earlier SQLite defect, but there is no evidence that Linux has a uniquely worse write path. The Electron LevelDB activity is a different mechanism from the fixed persistent TRACE defect.

## Residual reports and unknowns

Later public reports describe two unresolved mechanisms:

- Issue `#35401` reported a plugin-catalog cache rewritten wholesale about every 8.6 seconds on macOS with CLI 0.145.0 and resident app-server 0.144.5, estimating about 65 GB/day for that file. It was not a clean Desktop-only test, and no confirmed fix was found.
- Issue `#35823` reported SQLite freelist/space-reclamation amplification on Windows Desktop `1.2026.190.0`. This establishes file-growth inefficiency, not equivalent physical NAND writes.

No public controlled study was found for current stable 0.149.1, no local active-workload Linux measurement was made, and no SMART/media-health evidence attributes endurance loss to Codex. Consequently, “Codex Desktop still destroys SSDs” is unsupported, while “all excessive-write paths are gone” is also unsupported.

## Sources

- [Original high-write report, openai/codex#28224](https://github.com/openai/codex/issues/28224)
- [Persistent-log fix #29432](https://github.com/openai/codex/pull/29432)
- [Persistent-log fix #29457](https://github.com/openai/codex/pull/29457)
- [Codex 0.142.0 release](https://github.com/openai/codex/releases/tag/rust-v0.142.0)
- [Codex 0.142.5 release](https://github.com/openai/codex/releases/tag/rust-v0.142.5)
- [Bridged-log fix #29599](https://github.com/openai/codex/pull/29599)
- [Codex 0.143.0 release](https://github.com/openai/codex/releases/tag/rust-v0.143.0)
- [Codex 0.145.0 release](https://github.com/openai/codex/releases/tag/rust-v0.145.0)
- [MCP logging fix #31789](https://github.com/openai/codex/pull/31789)
- [MCP tool-list fix #31790](https://github.com/openai/codex/pull/31790)
- [Hyper logging fix #31791](https://github.com/openai/codex/pull/31791)
- [Streamed-response logging fix #31792](https://github.com/openai/codex/pull/31792)
- [Plugin-cache rewrite report #35401](https://github.com/openai/codex/issues/35401)
- [SQLite reclamation report #35823](https://github.com/openai/codex/issues/35823)
- [Official Linux app documentation](https://learn.chatgpt.com/docs/linux/linux-app)
- [Prior local Linux packaging report](../../01a0338f/reports/linuxDesktopApplications.md)
- [Prior local installation witness](../../01a0338f/witnesses/ouranosChatgpt.md)
- Flow `01a038b8`
