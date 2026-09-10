# Post-audit port preparation

This is an executable next-step brief, not authorization to port or deploy
Orchestrate yet. The user’s order remains: finish the stack audit and final
Ethos-pinned producer gates first, then port Orchestrate with
signal-orchestrate and meta-signal-orchestrate. The live lock service remains
in place until its tested replacement deployment.

## Current coordination

Lock 1020 reserves the complete Protos and datom-codec repositories for final
producer integration. The Orchestrate service, sockets, and state observations
are recorded in `cutover-preparation.md`; no live activation or state write has
occurred here. Original receipt-981 protected CriomOS-home paths remain
prohibited. The potentially relevant `flake.lock` was not in that original
path set, but a lock-only rollout still waits for a completed stack and a
separate authorization-compatible deployment path.

## Port sequence

1. Land Ethos6, pin both producers to it, and run their generated-contract and
   dependency-ethos gates. Retain the resulting public producer revisions.
2. Regenerate the ordinary and meta signal contracts through Ethos Zero; do not
   hand-edit generated Rust. Update their runtime consumers to the generated
   named Query/Response types. Signal-only Nexus builds must not carry the
   `datom` feature; clients explicitly enable it where textual Datom input is
   used.
3. Port Orchestrate runtime callers to those generated contracts and the
   current Datom traits without compatibility adapters or parallel old chains.
4. Obtain a consistent snapshot of the live state through its database
   snapshot or transaction facility, rather than an ordinary file copy while
   writes may occur, then use that snapshot in isolated `XDG_RUNTIME_DIR` and
   `XDG_STATE_HOME`. Demonstrate either compatible archive loading or a
   one-shot migration of configuration, all locks, and allocator state. The
   obsolete state location is not an input.
5. Run the replacement Nexus in that isolated environment, exercising ordinary
   and meta sockets and the archive migration. Only a passing isolated
   replacement can become a candidate for declarative deployment.
6. For the authorized final declarative rollout, use the generated
   CriomOS-home unit owner. A `flake.lock`-only pin may be considered only when
   it does not modify any original receipt-981 protected path and when it
   resolves the tested replacement revision. Do not patch a generated unit.
   The final cutover migrates a latest state snapshot after controlled
   quiescence, never the earlier test snapshot.

## Sources

- `reports/cutover-preparation.md`
- `reports/substrate-audit.md`
- The user-inlined Vision and Intent, including Nexus and Signal requirements.
- Original protection receipts cited in `cutover-preparation.md`.

## Declarative deployment constraint

A subsequent read-only review found that the deployment source
`CriomOS-home/flake.nix:138-139` fixes the Orchestrate input commit. A
`flake.lock`-only change cannot durably repin a replacement. The original
receipt-981 prohibition still excludes edits to that protected file and its
other listed paths, even though the associated live lock was released. The
port may therefore complete its runtime, migration, isolated-Nexus, and
consumer work while preparing the exact reviewed deployment patch outside the
protected checkout. It must not edit the protected path or activate the live
replacement. Once the complete port is reviewable, root can request an
explicit amendment for that exact protected-file patch as the final
deployment step.
