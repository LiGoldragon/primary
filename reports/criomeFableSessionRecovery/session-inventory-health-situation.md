# Session inventory health situation

Task: diagnose current `aggregator` session inventory health without reading transcript text and propose fixes before using inventory for garbage-collection deletion decisions.

## Scope and privacy boundary

No transcript or subagent output contents were read directly. Evidence came from `aggregator`/`meta-aggregator` metadata operations, service/config metadata, source code for health semantics, and filesystem metadata: existence, counts, sizes, permissions, timestamps, symlink status, and source paths.

Spirit query: `spirit "(PublicRecords ((Full [(Technology (Software (Intelligence AgentSystems)))]) None))"` returned records including `lta7` (avoid special-case design) and `jys2` (aim for best end-shape). No archive-specific public record was found for `(Information Archives)`/operations.

## Current operation evidence

- `printf '(Version (None))' | aggregator` reports `signal-aggregator 0.5.0`.
- `systemctl --user is-active aggregator-daemon.service` reports `active`.
- `systemctl --user show ...` shows the daemon loaded/running with `ExecStart=/nix/store/...-aggregator-0.1.0-profile/bin/aggregator-daemon`; the wrapper exports `AGGREGATOR_CONFIGURATION=/home/li/.local/state/aggregator/configuration.nota` and executes the package binary.
- `meta-aggregator` `ObserveConfiguration` and `/home/li/.local/state/aggregator/configuration.nota` show exactly two transcript sources:
  - `Claude (/home/li/.claude/projects/-home-li-primary)`
  - `ClaudeSubagentOutput (/tmp/claude-1001)`
  - no `/tmp/pi-subagents-1001` source.
- `aggregator` `ObserveHealth` currently reports:
  - Claude root `/home/li/.claude/projects/-home-li-primary`: `DiscoveryTruncated`, `discovered_files=1024`, `indexed_records=105878`, `malformed_records=128`, `unreadable_records=0`.
  - Claude subagent root `/tmp/claude-1001`: `UnreadableRoot`, `discovered_files=982`, `indexed_records=18`, `malformed_records=0`, `unreadable_records=128`.
  - index: `ReadableIndexed`, `session_count=985`, `subagent_count=0`, `output_count=105896`, `transcript_block_count=105936`.
- `InventorySessions (AllConfigured None)` produced 985 session cards and scan report summaries:
  - Claude: `Truncated`, `discovered_files=1024`, `indexed_sessions=983`, `byte_count=359669925`.
  - ClaudeSubagentOutput: `Failed`, `discovered_files=982`, `indexed_sessions=2`, `byte_count=145453`.
  - aggregate completeness: failed by source failure.

## Cause analysis

### Claude project root truncation

Proximate cause: hard-coded scan discovery cap, specifically maximum discovered files. Source code `src/adapter.rs` has `TranscriptScanLimits::default_runtime()` with `maximum_discovered_files=1024`, `maximum_scan_entries=4096`, `maximum_file_bytes=8 MiB`, `maximum_line_bytes=256 KiB`, and `maximum_read_failures=128`. `TranscriptDiscoveryState::observe_transcript_file` stops once file count reaches that cap.

Filesystem metadata under `/home/li/.claude/projects/-home-li-primary`:

- `4675` `*.jsonl` files.
- `10491` total entries, `555` directories.
- `0` symlinks, `0` unreadable dirs/files.
- JSONL total byte size about `2,013,710,374` bytes.
- `5` JSONL files exceed the 8 MiB per-file cap.

Because health reports exactly `discovered_files=1024`, and actual JSONL count is `4675`, the current `DiscoveryTruncated` status is primarily the discovered-file cap, not missing directory, permissions, timeout, stale config, or symlink rejection. There are also 128 malformed failures in aggregate; `Collect` over Claude counted `Malformed=128`, matching the read-failure cap, but status is `DiscoveryTruncated` because truncation is detected first.

### `/tmp/claude-1001` subagent root failure

Proximate cause: symlink-boundary rejection inside a broad legacy/native Claude temp root, not missing directory or POSIX unreadability.

Filesystem metadata:

- `/tmp/claude-1001` exists, mode `drwx------`, owner uid `1001`, group `100`.
- It contains `2135` `.output` paths, `32926` total files, about `21,032,138,424` bytes.
- `0` unreadable dirs/files by filesystem permissions.
- `3084` symlinks total; `757` `.output` symlinks, all resolving outside `/tmp/claude-1001`; `2287` broken symlinks overall.

Aggregator evidence:

- `Collect` over `ClaudeSubagentOutput` counted `PermissionDenied=128` read failures.
- Parsing those failure paths showed all 128 sampled/capped failure paths are symlinks resolving outside the configured root.
- Source code `TranscriptFileDiscovery::collect_files` canonicalizes each path and records `ReadFailureReason::PermissionDenied` if the canonical path does not start with the canonical root. The failure accumulator caps at 128; `SourceHealthObserver` maps any non-malformed failure count to `UnreadableRoot`.

So `/tmp/claude-1001` exists and is readable, but aggregator treats out-of-root `.output` symlink targets as permission-denied failures and marks the whole source failed.

### Pi subagent root expectation

Current Pi subagent output source evidence points to `/tmp/pi-subagents-1001`:

- Deployed package source `/home/li/.pi/agent/packages/pi-subagents-tintinweb/src/output-file.ts` creates output paths at `join(tmpdir(), \`pi-subagents-${process.getuid?.() ?? 0}\`, encoded cwd, sessionId, "tasks", `${agentId}.output`)`.
- `/tmp/pi-subagents-1001` exists, mode `drwx------`, uid `1001`, with `749` regular `.output` files, no symlinks, about `344,660,035` bytes.
- The aggregator local-default generator source `src/local_default_configuration.rs` currently derives only the Claude project root and `ClaudeNativeSubagentOutputRoot::from_temporary_directory_and_user`, which yields `/tmp/claude-1001` for uid 1001.
- The systemd pre-start script regenerates local default configuration for workspace `/home/li/primary` and `temporary_directory=${TMPDIR:-/tmp}` on each daemon start; it does not add Pi’s root.

Conclusion: `/tmp/claude-1001` may be expected for Claude Code/native task-output compatibility and historical recovery, but it is not sufficient for current Pi subagent outputs. Aggregator should configure `/tmp/pi-subagents-1001` as an additional/alternative subagent-output source, likely with a producer-specific source kind or root policy.

## Proposals

### Quick config/limit changes

- Add `/tmp/pi-subagents-1001` to configured transcript sources for current Pi subagent outputs. Because pre-start rewrites local default configuration, do this in the Nix/default generator, not by hand-editing the generated config.
- Raise or expose scan limits for Claude project roots: discovered files must exceed current 4675 JSONL files, and scan entries must exceed current 10491 entries if full recursive discovery is desired. A safe immediate target is at least 8192 discovered files and 20000 scan entries for this root, with measured latency.
- Treat `/tmp/claude-1001` as optional legacy/recovery input or narrow it to the workspace/session subtrees needed, rather than scanning the entire polluted temp root.

### Product/API improvements

- Make transcript scan limits part of `AggregatorConfiguration` and report the cap that fired (`file_count`, `scan_entry`, `file_bytes`, `line_bytes`, `failure_count`) in health/inventory.
- Add separate health statuses for `SymlinkEscapedRoot`, `FailureLimitReached`, `MalformedLimitReached`, and `UnreadableRootMissing`; the current `UnreadableRoot` masks an existing root with rejected symlinks.
- Use `TruncationReason::SourceLimit` for source scan/file/line caps; current `TranscriptLimitTruncation::into_truncation` always emits `RequestLimit`, even for source caps.
- Add a first-class Pi subagent output adapter/source kind, or teach the subagent-output source to accept explicit producer/root policies.
- Add inventory deletion-gate API: return `DeletionUnsafe` when any selected source is `Failed`, `Truncated`, or `Resumable`, rather than leaving deletion policy to callers.

### Safety/privacy considerations

- Keep metadata-first health as the normal diagnostic surface; do not require transcript text reads to diagnose source completeness.
- Do not follow symlinks outside a configured root unless the configuration explicitly authorizes target boundaries. If following is allowed, report it as a policy decision.
- Garbage collection must treat source failure/truncation as a stop condition, not as evidence that absent sessions are deletable.

## Recommended next action before trusting `InventorySessions` for deletion

Do not use current `InventorySessions` for garbage-collection deletion decisions. First land a configuration/product fix that makes all selected live sources complete or intentionally excluded; then rerun `ObserveHealth` and `InventorySessions` and require zero `Failed`, `Truncated`, or capped-failure statuses. Separately cross-check inventory counts against filesystem metadata for the selected roots, and only then allow GC to delete items absent from a complete selected source set.

## Unknowns and not checked

- I did not read transcript/subagent output contents.
- I did not run deployment, edit code/config, or restart services.
- I did not benchmark larger scan limits.
- Exact semantic ownership of old `/tmp/claude-1001` vs current Pi roots should be confirmed by the feature owner before deleting or deprecating that source.
