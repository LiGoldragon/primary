# Codex Desktop SSD assessment

## Answer

The historical “hard on SSDs” report was real, but the catastrophic 0.142-era
mechanism is not established as current behavior. Upstream issue #28224 records
one system writing about 37 TB in 21 days through `~/.codex/logs_2.sqlite` and
its WAL (the issue's extrapolation was about 640 TB/year); its author closed the
issue after reporting roughly 85% less logging from three merged fixes. The
0.142.0 release records the WebSocket-payload and duplicate-telemetry filters,
0.143.0 carries the bridged-log follow-up, and 0.145.0 carries four additional
persistent-log reductions (#31789–#31792).

That does not justify “all SSD risk is fixed.” Two later upstream issues remain
open: #35401 claims a plugin-catalog cache is rewritten in full every polling
interval (about 65 GB/day in its idle reproduction), and #35823 claims
`logs_2.sqlite` does not reclaim freed pages. The latter is explicitly a
Windows Desktop report, so it is not Linux evidence. The current upstream
stable release page is 0.149.1, while this host's unofficial Linux wrapper
bundles backend 0.148.0; the host's separate CLI resolves to 0.149.1.

For this Linux host, the fresh witness found no measurable process-attributed
block-device write in a five-second idle sample. It did find the Desktop and
its backend holding both Electron stores and `~/.codex` SQLite/session files,
and their cumulative process counters are nonzero. Therefore the strongest
answer is: current Linux Desktop is not witnessed as continuously hard on the
SSD at this moment, the old severe defect was addressed upstream, and the
long-running/plugin-heavy workload question remains unresolved rather than
proved safe.

## Evidence classes

### Direct observations

- The local Linux wrapper/version/process/store facts and the five-second I/O
  interval are in `../witnesses/codexDesktopStorage.md`.
- No local probe established a sustained rate, NAND wear, or a before/after
  comparison against an unfixed build.

### Upstream claims and release evidence

- #28224 is a user report with measurements, not a controlled independent
  endurance study. Its own text says the first three merged fixes were expected
  to avoid about 85% of the logs.
- PRs #29432 and #29457 are merged and listed in 0.142.0; #29599 is merged and
  listed in 0.143.0; #31789–#31792 are merged and listed in 0.145.0. These
  establish that the logging mechanisms were changed and released, not that a
  particular Linux workload now has a safe endurance rate.
- #35401 and #35823 are open reports. Their measurements and platform scopes
  remain claims until independently reproduced; neither was reproduced here.

### Hypotheses

- The local cumulative counters probably include SQLite/session persistence
  used by Desktop/backend because the relevant processes hold those files open.
  This is an attribution hypothesis, not a per-file write witness.
- Residual write amplification may depend on plugin polling, active sessions,
  platform, and the exact bundled backend; this report does not choose among
  those possible causes.

### Unknowns returned to the caller

- Linux long-duration write rate under active Desktop sessions and enabled
  remote plugins.
- Whether 0.149.1 (or the wrapper's 0.148.0 backend) contains fixes for the
  open plugin-catalog and SQLite-reclamation reports.
- Whether Desktop, CLI, or a shared app-server owns each byte in the cumulative
  counters, and whether filesystem writes reach NAND at the same volume.

## Sources

- Witness: `flows/01a038b8/witnesses/codexDesktopStorage.md`
- Flow context: `flows/01a038b8/log.md`
- [Issue #28224: Codex SQLite feedback logs can write ~640 TB/year](https://github.com/openai/codex/issues/28224)
- [PR #29432: Stop logging every Responses WebSocket event](https://github.com/openai/codex/pull/29432)
- [PR #29457: Filter noisy targets from persistent logs](https://github.com/openai/codex/pull/29457)
- [PR #29599: Stop persisting bridged log events](https://github.com/openai/codex/pull/29599)
- [PR #31789: Stop persisting RMCP service traces](https://github.com/openai/codex/pull/31789)
- [PR #31790: Reduce MCP tool-list trace volume](https://github.com/openai/codex/pull/31790)
- [PR #31791: Filter routine Hyper logs from SQLite](https://github.com/openai/codex/pull/31791)
- [PR #31792: Summarize streamed response item logs](https://github.com/openai/codex/pull/31792)
- [Release 0.142.0](https://github.com/openai/codex/releases/tag/rust-v0.142.0)
- [Release 0.143.0](https://github.com/openai/codex/releases/tag/rust-v0.143.0)
- [Release 0.145.0](https://github.com/openai/codex/releases/tag/rust-v0.145.0)
- [Issue #35401: plugin catalog cache full rewrites](https://github.com/openai/codex/issues/35401)
- [Issue #35823: logs_2.sqlite page reclamation](https://github.com/openai/codex/issues/35823)
- [Release 0.149.1](https://github.com/openai/codex/releases/tag/rust-v0.149.1)
