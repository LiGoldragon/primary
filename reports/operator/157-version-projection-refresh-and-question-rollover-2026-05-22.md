# Version Projection Refresh And Question Rollover

Report kind: refresh
Topic: version projection, Spirit cutover, and current operator questions
Date: 2026-05-22
Lane: operator

## What I Refreshed

I checked the protocol and intent surfaces after the newest designer
work:

- `orchestrate/AGENTS.md`
- `orchestrate/roles.list`
- `protocols/active-repositories.md`
- Spirit records for `component-shape`, `workspace`, and `reports`
- `reports/designer/285-versionprojection-trait-and-handover-protocol-specification.md`
- `reports/third-designer/19-refresh-after-prime-session-2026-05-22.md`
- `reports/cluster-operator/4-update-authority-and-lojix-daemon-current-state-2026-05-22.md`

`protocols/active-repositories.md` has not changed since 2026-05-20.
The live protocol changes are in `orchestrate/AGENTS.md` and
`orchestrate/roles.list`: `cluster-operator` and `nota-designer`
exist as specialized bare lanes in the transitional bash-readable
registry.

## Intent Updates Absorbed

New Spirit records after the prior refresh:

- `194 component-shape` — crate name is `version-projection`, peer to
  `signal-sema`.
- `195 component-shape` — default subscription policy is
  `TerminateAtHandover`; active subscriptions terminate cleanly and
  clients reconnect to `next`.
- `196 component-shape` — `PeerCheck` is retired; `signal-version-handover`
  is the single discovery/handover mechanism.
- `197 component-shape` — psyche affirmed the split between the shared
  projection crate and the handover signal contract.

This means `designer/285` supersedes `designer/284` wherever they
differ. In particular, implementation should not create a `migration`
crate, should not propagate `PeerCheck` into every component working
contract, and should not keep the old `signal-version-coordination`
name.

## Actions Taken

I updated the active beads with comments so future implementation does
not pick up the stale `/284` shape:

- `primary-la7q` — per-type migration trait is now
  `VersionProjection<Source, Target>` in `version-projection`;
  `PeerCheck` is retired; policy decides mirror/divergence/reject.
- `primary-ib5n` — canonical sema-upgrade architecture must merge
  `/285`; use `signal-version-handover`, not `signal-version-coordination`.
- `primary-l3h5` — sema-upgrade daemon promotion must fit the
  handover protocol and private upgrade socket.
- `primary-chpq` — immediate Spirit cutover must keep the CLI thin;
  durable handover is not CLI-owned dual-write.
- `primary-x3ci` — Spirit v0.1.1 cutover should be described as
  version-handover; first cutover may still use stop/freeze/migrate/start
  until `commit_sequence` exists.

I did not edit code. The actionable work at this point was pointer
hygiene: the design target moved under our feet, and the beads needed
to stop pointing implementers at the older shape.

## Current Implementation Reading

The highest-priority production path is still Spirit cutover. The
latest durable shape is:

1. `version-projection` is the shared crate for bidirectional type
   projection.
2. `signal-version-handover` is the daemon-to-daemon protocol.
3. Per-operation policy lives in the runtime crate, not the contract
   crate.
4. The CLI remains a thin client. Version selection comes from the
   wrapper / active-version selector, not from a smart CLI that writes
   two daemons.
5. During handover, `next` becomes the public receiver. `main` stops
   accepting normal public writes and remains writable only through the
   private upgrade socket.
6. Until sema-engine has durable `commit_sequence`, the first Spirit
   cutover can use stop/freeze/migrate/start-new.

## Still-Relevant Questions

### Active Operator Questions

1. **Spirit cutover mechanism:** should the immediate production
   implementation do the stop/freeze/migrate/start-new cutover first,
   then build full `version-projection` handover, or should the cutover
   wait for `version-projection` and `signal-version-handover`?

2. **`commit_sequence` priority:** should sema-engine `commit_sequence`
   become the next foundation task before any more live cutover work?
   `/285` says zero-downtime handover depends on it.

3. **Spirit owner release asymmetry:** is it intentional that
   `persona-spirit` and `signal-persona-spirit` move at v0.1.1 while
   `owner-signal-persona-spirit` remains v0.1.0?

4. **`EffectEmitted` payload:** should observable streams carry
   component-local typed `Effect`, universal `SemaObservation`, or two
   separate streams?

5. **Sema-upgrade bootstrap:** should sema-upgrade use a hand-written
   bottom-of-stack upgrade path until contracts stabilize, then dogfood
   later?

6. **Engine-manager Axis 2:** should the internal
   `supervisor`/`supervision_socket_*`/`.supervision.sock` rename land
   now, or be explicitly deferred?

7. **Orchestrate executor migration timing:** should `primary-c620`
   continue in parallel with Spirit cutover, or pause until the
   production Spirit transition is complete?

### Architecture Questions That Still Block Later Implementation

8. **Historical signal contract versions:** should frozen historical
   contracts be sibling repos such as `signal-persona-spirit-v0-1-0`,
   as `/285` recommends?

9. **`owner-signal-version-handover`:** defer until sema-upgrade owner
   policy exists, or create now for force-flip / rollback / quarantine
   authority?

10. **Mirror payload shape:** should handover mirror payloads stay as
    bytes plus `RecordKind`, or become typed enums?

11. **Per-operation policy declaration:** keep policy literals in each
    runtime crate for now, or push annotations into contract/schema
    generation sooner?

12. **Lane identifiers:** current third-designer synthesis says
    retired identifiers are not reserved for now, while older record
    `118` said reserved forever. Should this be formally superseded in
    Spirit so implementation does not keep rediscovering the conflict?

13. **Magnitude follow-up:** `Unknown` plus Health/Readiness collapse is
    settled, but should this become v0.1.2 only after Spirit v0.1.1 is
    fully cut over?

14. **Mind channel choreography:** what high-level owner command does
    Mind send to Orchestrate before Orchestrate calls Router
    `Grant`/`Extend`/`Revoke`/`Deny`?

15. **Bird-on-Zeus helper surface:** should first production helper
    verbs be exactly `HomeProfile` and `FullSwitch`, deferring `Test`
    and `BootOnce`?

## Recommendation

Do not start the old `/284` migration implementation. The new target is
`/285`.

For immediate work, either:

- finish Spirit v0.1.1 production cutover with the stop/freeze/migrate/start
  path and document it as the last pre-`commit_sequence` migration, or
- implement the minimum `version-projection` + `signal-version-handover`
  skeleton only far enough to prove the Spirit handover path in Nix.

I would choose the first if the goal is to get agents onto v0.1.1
quickly, and the second if the goal is to avoid another one-off cutover.
