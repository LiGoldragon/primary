# Prometheus Nix store repair report

## Current result

The ordered repair stopped at its first object. On canonical root SSH,
`hostname` was `prometheus` and boot ID was
`c3cf7dd5-c3df-44f1-a688-1d6b88de1d6c` before and after the attempt.

At low priority (`nice -n 19 ionice -c 3`):

1. `nix-store --repair-path /nix/store/vjlirf3yjj6ln6wl6xq0cpks3jnb8px5-source`
   exited 1: Nix reported that it cannot repair the path.
2. `nix-store --verify-path /nix/store/vjlirf3yjj6ln6wl6xq0cpks3jnb8px5-source`
   exited 1. The registered hash is
   `sha256:0d28gj47z4l9y7g2l9kc7fsksy7l5xps28gnq89fryh1kp7fnxsi`; the bytes
   hash as `sha256:1zp3yysmv76vr5mz3knhmcdfi0386x7a4gi6xi2f32qcz5p3va3h`.

The independent poststate still finds a zero-byte regular `flake.nix`, and
`nix hash path --type sha256 --sri` still returns
`sha256-cKg9bvkMi+FE7CY+ok43aIDoGqvQzvFryducXbX34/4=` for the object.

The initial whole-store low-priority scan was subsequently authorized despite
that failure, then interrupted for the exact-path deletion priority. Native
root/referrer queries found the corrupt source unrooted and unreferenced;
`nix-store --delete` removed it and its registration. A later unchanged build
refetched it. Independent current verification passes, with the exact expected
SRI `sha256-UXfrzp0B+uwSwvYhoW8v9Hg9tTtsJire8YmSf4h8SDQ=`.

The next corrupt path named by the unchanged build was
`/nix/store/2iclijlq0z87fick06c8klrn2ii10xyv-flow-nexus.datom.drv`.
It was an empty registered file and failed verification. It had no roots; its
referrer closure consisted of three additional rebuildable `.drv` files. All
four were natively deleted and independently found absent/unregistered.

A full-priority whole-store scan ran from `2026-11-13T18:14:08-06:00` through
`2026-11-13T18:44:55-06:00`. New build/deployment priority superseded it, so its
owned PID received SIGINT and exited 1 with `interrupted by the user`. The scan
is incomplete and was not replaced. Before interruption it named 818 unique
unrepairable paths, all retained in
`whole-store-full-priority-unrepaired-paths.txt`; 822 unique modified paths had
been observed and no repair-success line appeared. These are a prefix of the
store traversal, not a whole-store count. They were not mass-deleted because
the scan was stopped to release its GC/database lock for current targeted
build repairs. No service action, restart, switch, evaluation or build was run
by this lane.

A later handoff named `install-fonts-hook.drv` after a native closure deletion
was refused as live. The current bounded recheck found that path had already
been recreated: it is 1854 bytes and `nix-store --verify-path` passes. Its
referrer graph is held by the active naming build's temporary root. No stale
deletion was attempted; the valid live build graph was left intact. Evidence is
`install-fonts-hook-current-graph-2.txt`.

## Path disposition

- Source deleted and later refetched valid:
  `/nix/store/vjlirf3yjj6ln6wl6xq0cpks3jnb8px5-source`
- Corrupt derivation and holding derivation referrers deleted: four paths in
  `flow-nexus-drv-delete-list.txt`
- Whole-store scan prefix found unrepairable: 818 unique paths in
  `whole-store-full-priority-unrepaired-paths.txt`
- Repaired by the interrupted scans: none evidenced
- Whole-store status: incomplete by explicit priority interruption

## Private evidence

- `preflight.txt`, `preflight-ssh.stderr`
- `exact-repair.log`, `exact-repair.exit`
- `exact-postverify.log`, `exact-postverify.exit`
- `poststate.txt`, `poststate-ssh.stderr`, `poststate.exit`
- `corrupt-source-referrers.txt`, `corrupt-source-delete.log`,
  `corrupt-source-postdelete.txt`
- `targeted-current-status.txt`
- `flow-nexus-drv-referrers.txt`, `flow-nexus-drv-delete-list.txt`,
  `flow-nexus-drv-delete.log`, `flow-nexus-drv-postdelete.txt`
- `whole-store-repair.log`, `whole-store-repair-resumed.log`
- `whole-store-full-priority.log`, its timestamps, exit status, and extracted
  unrepairable path list

The evidence directory is mode 0700 and files are mode 0600. Logs contain
paths and verifier diagnostics only; no file contents were read into them.
