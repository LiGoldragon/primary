# Provider startup review witness

## Method

This witness records the independent read-only review by
`review_provider_startup` in `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux-control-repair-4a8046`.
The findings below are that reviewer's observations, not this subflow's own
verification.

## Findings

In `scripts/patches/linux-status-bridge.sh:27`, the old already-patched
predicate still expects
`globalThis.__wisprStatusBridge?.setToggleHandsFree(async()=>`, but the new
patch emits `globalThis.__wisprStatusToggleHandsFree=async()=>` and registers
during bootstrap. The existing `signed-payload-patches.bats:10-22` applies the
patch twice, so the predicate must change.

In `nix/wispr-status-bootstrap-check.nix:89-106`, the control socket lacks a
connect/read deadline. The catch at line 301 merely sets `process.exitCode`
and keeps bridge servers and the heartbeat alive after an assertion failure;
the check needs a bounded deadline and unconditional cleanup.

The reviewer accepted the production parked handler ordering: the lexical
closure is established before readiness and attached after bridge
construction. The bounded local bridge start-action plus socket-close smoke
passed. `bash -n` and Node syntax passed.

The reviewer did not run a remote derivation test. The packaged artifact was
unavailable to the reviewer at the time, and there is no original-source
semantic red baseline.

## Sources

* `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux-control-repair-4a8046/scripts/patches/linux-status-bridge.sh:27`
* `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux-control-repair-4a8046/signed-payload-patches.bats:10-22`
* `/home/li/wt/github.com/LiGoldragon/wispr-flow-linux-control-repair-4a8046/nix/wispr-status-bootstrap-check.nix:89-106,301`

## Current pending status

Main instructed integration to fix both findings. The fixes have not yet been
reviewed. This witness records pending work and does not establish acceptance.
