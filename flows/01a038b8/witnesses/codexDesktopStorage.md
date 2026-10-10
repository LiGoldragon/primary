# Codex Desktop Linux storage witness

Observed 2026-08-25 on the local Linux host. This is a point-in-time witness,
not a long-duration endurance test.

Method: probe `ps -eo pid,ppid,etimes,lstart,comm,args`, `codex --version`,
`stat`/`du`/`find` over the three known stores, `readlink` over the relevant
`/proc/<pid>/fd` entries, and read `/proc/<pid>/io` before and after a 5-second
interval. All commands were read-only; no Codex action, config edit, database
write, cache deletion, logout, or process restart was performed.

## Observations

- The host is NixOS 26.11 on Linux 7.1.8, with `/` on `/dev/nvme0n1p2`
  (`ext4`, `rw,relatime`).
- The unofficial desktop wrapper is running from the immutable package
  `codex-desktop-computer-use-ui-remote-mobile-control-26.721.41059`.
  Electron PID 905798 has been running since 2026-08-22 13:14:07 +0200.
- Its child app-server is PID 906558 and executes the bundled
  `/nix/store/...-codex-0.148.0/libexec/codex ... app-server`; the process
  command line includes `--remote-control --analytics-default-enabled`.
- The local CLI lookup is `/home/li/.nix-profile/bin/codex` and
  `codex --version` returned `codex-cli 0.149.1`.
- The desktop Electron process has open descriptors for
  `~/.config/Codex` LevelDB/session stores, `~/.local/state/codex` desktop log
  files, and `~/.codex/sqlite/codex-dev.db` plus
  `~/.codex/sqlite/codex-history-snapshots-dev.db`. The 0.148.0 app-server has
  open descriptors for `~/.codex/logs_2.sqlite`/its WAL and rollout/session
  files, as well as the desktop LevelDB files.
- Read-only size snapshots were approximately:

  | Store | Bytes | Regular files |
  | --- | ---: | ---: |
  | `~/.config/Codex` | 13,380,163 | 204 |
  | `~/.local/state/codex` | 1,548,133 | 7 |
  | `~/.codex` | 5,611,385,473 | 10,479 |

  `~/.codex` is a mixed CLI/agent store and must not be attributed wholly to
  Desktop. At the same snapshot, `~/.codex/logs_2.sqlite` was 779,255,808
  bytes and its WAL was 81,155,792 bytes.
- During the 5-second interval, process `write_bytes` did not change for the
  Electron main process (5,692,399,616), the bundled 0.148.0 app-server
  (1,734,823,936), or the sampled Electron renderer processes. A few write
  syscalls/page-cache characters occurred: Electron main `wchar` increased by
  30 bytes, app-server `wchar` by 352 bytes, and one renderer by 10,384 bytes.
  The observed store file sizes and newest-file mtimes did not change during
  the interval.

## Interpretation boundary

The unchanged `write_bytes` counters are evidence that no measurable process-
attributed block-device write occurred in this five-second idle sample. The
cumulative counters prove that these long-lived processes have performed
substantial writes since startup, but do not identify which file, workload, or
other client caused them and do not equal NAND wear. The open descriptors make
shared Desktop/backend use of both Electron stores and `~/.codex` observable;
the exact per-file attribution and a Linux endurance rate remain unknown.

