# Field clearance packet — live tools, stage 1

Requested by Field hopi, 2026-11-16. Proposal only. This packet deliberately separates read-only inventory from executable provisioning: exact store paths and compiler policy cannot truthfully be claimed before the assigned runtime actor reads them. No command below has run remotely and no slot is assumed.

## Scope and custody

Field assigns one runtime actor and one slot, confirms whether cold refresh/replacement is required before wake, then clears this read-only stage. Actor returns its identity and evidence paths to researchTools. No existing session, remote scratch root, source checkout, mount or analyzer is reused. Field does not need to reserve twelve concurrent endpoints; benchmark sessions stage one pair at a time after tool validation. Ordinary reads/searches/edits remain native on Ouranos; only semantic requests/builds are remote once separately cleared.

Source-only local roots already exist: `/tmp/research-tools-09fa53.RK73td/flow` at a044e39 and sibling `lojix` at 5d75a403, exact full revisions in `flows/72fb9a/research/live-code-tools.md`. Both are read-only trial sources, not runtime allocations. Oracle is sibling `oracle/` and is excluded from all answerer roots. No source-edit fixture is presently authorized.

## Stage 1 — exact read-only inventory

Assigned actor runs the following on each host in its normal user context and retains stdout/stderr with host identity. On Prometheus this is inventory of the proposed LSP/build runtime, not ordinary source work wrapped in SSH. No version probe executes rust-analyzer, rustc or Cargo in this stage; package wrapper text and store references are read instead. Credentials are not inspected.

```sh
hostname
for name in lspmux rust-analyzer cargo rustc nix python3 ast-grep sshfs fusermount3; do
  command -v "$name" || true
done
test -r /etc/nix/machines && cat /etc/nix/machines
test -c /dev/fuse && ls -l /dev/fuse
```

For each returned tool path, actor records `readlink -f PATH`; if it is a text wrapper, reads the wrapper without invoking it. Read the existing compiler/analyzer guard's declared policy and report whether a temporary Nix build, a manual remote analyzer and observational compiler probes require a separate exception. Preserve the guard; do not bypass it with a guessed absolute binary. Also return presence of already-retained compatible offline vendor/toolchain artifacts, with exact store identities only. No store-wide or filesystem-wide search.

Source/tool gap requiring a decision: lspmux is absent from Ouranos PATH, and remote availability is unknown. Existing SCIP package is proposal-only CriomOS ab62d218610f35af6279ed3590224dee83645011, `packages/repository-analysis/default.nix`; it pins old Flow379, so it is not a current-corpus dependency closure. It provides an example guard, not authority or an artifact covering the new corpora. Ranked Aider map also still needs an approved Nix artifact. Stage 1 ends on command exit; no polling.

## Stage 2 — approval fields to fill from inventory

Return these fields to Field before any provisioning/start: exact lspmux/analyzer/toolchain/map store paths and versions; immutable source/dependency identities for each corpus; exact Field-allocated remote mktemp root and local mount root; private socket and configuration paths; actor/session identities; explicit memory/thread/time limits; cleanup process IDs and mount ownership; concrete start/query/stop command lines. These are values to approve, not guessed defaults. A missing field blocks that operation rather than silently choosing a value.

Provision a missing executable only through the owner's reviewed Nix build on Prometheus, with no profile install or host declaration. Reuse existing closure/artifact first. Reading `rust-nix-example` whole and packaging-owner review precede any build-file edit. No new application stack or Node.

## Proposed guarded semantic coverage

One manually started lspmux on a private Unix socket and at most one rust-analyzer per corpus on Prometheus. All clients use identical workspace roots, initialization and environment so instance sharing is verified, not presumed. Keep a shared connection alive only during the bounded trial if needed; terminate explicitly rather than rely on idle GC. Query through one command carrying protocol input and returning compact source-bearing results. Reuse the harness LSP client if available; otherwise a thin framing/URI-map client only, no authored server or multiplexer.

Initialization to verify against the selected analyzer: `checkOnSave=false`, Cargo `allTargets=true`, extra args `--locked --offline`, build scripts disabled, proc macros disabled. The previous batch package additionally supplied a no-op build-script override because its loader bypassed the enable switch; a live server's behavior must be tested, not assumed identical. Override command, if needed, is an explicit approved executable path in the runtime configuration. Supply the pinned Rust library sources explicitly.

Propose compiler observation only: log every configured compiler invocation; allow only version/print probes; refuse code generation, output paths and invocations lacking a permitted probe. Put the approved guard on configured RUSTC/PATH and record effective values. Disable check/build-script/proc-macro launch paths. Existing guard remains authoritative, including if it refuses this policy. A wrapper is not universal containment against arbitrary absolute compiler paths; coverage must say that. Record absence of target artifacts and unchanged lock/source hashes. Missing build-script cfg/env/OUT_DIR and procedural expansions limit answer coverage and must be visible in tool responses and final report.

## Mount, freshness and failure boundary

After exact paths and session are approved, actor manually mounts ONLY the allocated Prometheus disposable root using existing sshfs at the allocated Ouranos root. No fstab, profile, service, shared SSH settings or credentials change. Initial corpus tree is read-only. Read-only and semantic checks come first; a tiny fixture scratch tree or exact file whitelist requires a separate source-write grant before any freshness edit. Do not edit canonical source or assume Core's read-only archive grant permits it.

Text-search continuation test may terminate only a trial-owned LSP transport or lspmux/analyzer process. The mounted source transport stays up for that test so native local text search remains usable. A source-transport failure is a separate optional bounded diagnostic, not the dropped filesystem experiment. No host/network restart or interruption of another flow. No real power-cut claim.

## Cleanup receipt

Actor records every trial-owned PID/session/socket/mount/root as created. At the end or first stop event: stop answerer sessions through their owner, terminate registered semantic clients and servers, verify owned children exited, unmount the exact allocated mount, verify its entry is gone, preserve requested logs/hashes, then remove only registered disposable runtime roots after retention is agreed. Do not stop unrelated processes or delete the source-only oracle/evidence before reporting. Return exit states and any residue explicitly. No cleanup command runs against an unallocated path or guessed PID.

Stage 1 read-only inventory is the only clearance currently requested. Stage 2 provisioning/runtime remains a separate approval after the returned facts make its commands exact.
