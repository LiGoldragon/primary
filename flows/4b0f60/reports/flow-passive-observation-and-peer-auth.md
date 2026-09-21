# Flow passive observation and peer-auth contract

**Date:** 2026-09-21  
**Owner:** Mind4b0f60 architecture; implementation remains with the explicitly reserved writers.  
**Status:** living architecture and implementation contract. It makes no claim that the whole Flow/Message pair, deployment, source parity, or peer-auth feature probe has passed.

## Passive observation surface

`ObserveSessions` is authorized as a bounded snapshot query with explicit selection, cursor, and limit. Each row carries exact `FlowRef`, native identity, harness, runtime binding generation, Flow lifecycle generation, and declared profile. `observedBusy | observedIdle | observedUnknown` is an observation separate from duty, availability, and admission busy: an idle row neither creates work nor proves it may receive a wake.

Each metric carries quality and freshness state, including `VerifierUnavailable`; missing/null is never zero. Context reports separate occupancy proxy from emitted totals, cache breakdown, and account quota. A proxy is not resident occupancy; cumulative total is not current context; account quota has its own scope and timestamp. Event Watch exists only for a real source feed and supplies initial state plus deltas. No polling loop is introduced. Requests never select a verifier by filesystem path or PID.

```text
ObserveSessions{selection, cursor?, limit} -> SessionSnapshot{rows, cursor, completeness}
SessionRow{flow, native, harness, binding_generation, lifecycle_generation,
           profile, activity, availability, metrics}
Metric<T> = Observed{value, source, observed_at, freshness, quality}
          | Unknown{reason} | Unavailable{cause} | VerifierUnavailable{cause}
          | Stale{last_value, last_observed_at, cause} | Conflict{references}
WatchSessions{selection, resume_cursor?} -> initial Snapshot + ordered Delta*
```

Flow resolves the exact logical/native binding. Observation returns `IdentityConflict` or an explicit unknown when proof is absent; it does not infer lifecycle or binding generation from title, terminal, process ID, or a caller claim. A statusline/context adapter is a verifier edge only after the actual feed is proved; its inability to run is a typed quality state rather than reason to fabricate data.

## Sender authentication boundary

Unix-domain socket `SO_PEERCRED`, read at connection time, identifies the connecting process/user as peer PID, UID, and GID. It does **not** identify a Flow. `SO_PEERPIDFD` is the preferred feature-probed route for a stable peer incarnation. The root rejects treating numeric `pidfd_open` plus start time as automatically race-free; without a supported peer-pidfd route, use explicit unsupported/degraded/`VerifierUnavailable`. The local kernel version 7.1.8 is an environment observation, not a feature probe.

Multiple appserver sessions can share a peer, parent, TTY, or environment. None maps authority to a Flow. Sender authority instead requires an explicit registered caller binding/delegation scoped to `(FlowRef, binding_generation, operation)`, plus a kernel-identity join. A caller-supplied Flow field is an assertion only. The delivery-permit bearer binding nonce is not sender authentication. Request IDs and deduplication prevent replay/duplication effects; they do not authenticate a sender.

For an operation requiring authenticated authority, missing or incompatible proof produces a typed refusal. A passive snapshot can be permitted by explicit UID read policy, but its rows are labelled `SenderUnattributed`; it never invents a Flow. Shared UID is not adversarial tenant isolation without a stronger OS boundary. Connection FD passing or a proxy authenticates the original connector only: it cannot establish the author of each later write without per-message credentials or delegation. The logical envelope is server-stamped with `AuthenticatedPrincipal`, attributed Flow when proven, and correlation; arbitrary payload PID never supplies authority.

For the Message→Flow caller, an ordinary `VerifySender{pid,...}` must not treat Message payload peer records as kernel proof. Original-peer evidence can cross that boundary only through an explicit registered trusted-component attester/delegation path with its own kernel identity, capability, and generation, or a verifier operating inside the authority boundary and returning an opaque scoped receipt. Until that is proved, `BoundFlowSender = VerifierUnavailable` and identity-required mutations refuse. Sender-envelope claims and source-event ID deduplication are not authentication. Fieldef8b's disposable UDS research found spoofing payload PID cannot change `SO_PEERCRED` and a pidfd exit can be signalled; this establishes attribution limits, not BoundFlow proof.

```text
AuthenticatedPrincipal{uid, gid, peer_incarnation?, connection_ref}
CallerBinding{principal, flow, binding_generation, allowed_operations, evidence}
Envelope{principal, attributed_flow?, correlation, payload}
```

The system retains compiled binary domain contracts and root versioning. It does not tunnel a private JSON/string protocol around them.

## Process and implementation boundary

Medium owns the reserved wire/handler/auth work; Low3847 owns verifiers; f72 retains signal lock 2862, Flow CLI 2836, and Message 2864; 9dd3776 owns deployment work; Field Terra owns runtime audit. These scopes do not transfer paths or authorize work outside their actual reservations. Existing Message provenance and triad `ConnectionContext` are reusable inputs, not completed Flow sender binding. Current tested Low832b08ba evidence is a standalone remote gate, not proof of the whole pair. Keep pending test/release states as pending.

The prior running Flow binary `98f68df` SHA has no source map, and Message 0.12.0 source parity is unverified. Restored census source `f26ac801e` reported an 11/12 mapping, which is not duty proof. Those observations may inform a bounded report, never an implementation/deployment success claim.

Implementation first establishes the compiled-domain request/response types, exact identity resolver, verifier capability boundary, and peer-auth registration path; consumer output then exposes quality/freshness rather than hiding it. Watch is enabled only after source ordering, cursor/replay, initial-snapshot/delta, and reconnect behavior are witnessed. No observer starts model work, changes a lifecycle state, resumes a Flow, or assumes a delivery permit establishes sender identity.

## Required evidence and tests

Use behavioral tests with real domain machinery and deterministic time where a deadline/freshness transition is involved. Required cases cover: valid peer; wrong EUID; forged payload PID; a shared parent with multiple Flows; stale binding generation; exited peer and PID reuse; proxy/FD passing; unsupported verifier producing `VerifierUnavailable`; independently changing busy status; stale feed; and partial metric result. Add source ordering/replay/late delta, Watch reconnect, explicit UID read policy, and per-message delegation cases before enabling an authority-changing operation.

No test or report may promote individual Low gate evidence, kernel version, binary SHA, local tracking state, or 11/12 census mapping into whole-pair release, deployment parity, duty, or authenticated-Flow proof. A verifier failure remains visible and bounded; no fallback polling or filesystem/PID selector bypasses it.

## Concrete source audit

Flow source is clean local main `61d765e4814035c2c0a1424e670a1b62da3d10b6`: [`README.md`](/git/github.com/LiGoldragon/flow/README.md), [`flow-nexus/lib.rs`](/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/lib.rs), [`store.rs`](/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/store.rs), [`herdr.rs`](/git/github.com/LiGoldragon/flow/crates/flow-nexus/src/herdr.rs), and the [Flow CLI](/git/github.com/LiGoldragon/flow/crates/flow/src/main.rs) show Store plus ordinary/meta UDS, claim-marker admin registration, exact Herdr route recheck, and caller-origin stamps. They do not show a UDS sender credential binding. Flow's idle/working and `interactive_ready` eligibility reinforces activity≠availability.

Message source is clean local main `933064073b156dc1bf59458e18bc52619acce71d`; Signal Message is `7f2fc2d44b7b1a5e59c32b8071c56a4822310ed8`. [`daemon.rs`](/git/github.com/LiGoldragon/message/src/daemon.rs:52) accepts ordinary/owner UDS via triad runtime and passes accept-time `ConnectionContext`; [`provenance.rs`](/git/github.com/LiGoldragon/message/src/provenance.rs:46) classifies `SO_PEERCRED` and resolves a pinned `/proc` ancestor while documenting sender identity as separate. The generic UDS implementation at [`triad-runtime process.rs`](/git/github.com/LiGoldragon/triad-runtime/src/process.rs:22) reads rustix `SO_PEERCRED` into UID/GID/PID only; no pidfd/`SO_PEERPIDFD` implementation is witnessed. [`relay.rs`](/git/github.com/LiGoldragon/message/src/bin/relay.rs:228) supports an explicit Nexus Busy route only: PTY failure is not Busy.

The passive Field overview at [`tools/field-census.mjs`](/home/li/primary/tools/field-census.mjs) read-only joins HM and Herdr exact five-tuples; [`codex-context.mjs`](/home/li/primary/tools/field-census/codex-context.mjs:198) validates native UUID against metadata/transcript path and [`claude-context.mjs`](/home/li/primary/tools/field-census/claude-context.mjs:100) validates session IDs. These are observation checks, never sender auth or availability authority. No socket query, fetch, or build was run for this audit.

## Sources

- **Current living decisions:** ObserveSessions/Watch boundaries; identity/profile/activity/metric requirements; reserved implementation roles; peer-auth model and tests; and pending-release limitations. These are architecture authority, not implementation receipts.
- **Official protocol references supplied by root:** [Linux unix(7)](https://www.man7.org/linux/man-pages/man7/unix.7.html) for Unix-domain socket peer credentials and [Varlink specification](https://uapi-group.org/specifications/specs/varlink/) for primary API usage. They do not establish local feature support or Flow authority mapping.
- **Reported local evidence:** Low832b08ba standalone remote-gate test; Flow `98f68df` binary SHA without source map; Message 0.12.0 parity unverified; restored census `f26ac801e` 11/12 mapping without duty proof; local kernel 7.1.8 without feature probe.
- **Concrete-path audit returned by `/root/checkup_architecture`:** Flow/Message/Signal Message revisions and paths cited in “Concrete source audit,” including the current UDS/provenance boundary, and no pidfd implementation. It is source inspection only.
- **Finalized living auth addendum:** Fieldef8b disposable UDS spoof/pidfd evidence; Message→Flow attester/opaque-receipt requirement; and activity/admission separation. It specifies the required implementation boundary, not a completed feature.
