# 449 — Designer PoC port-gap audit

## Scope

The psyche asked whether any designer proof-of-concept work from the recent
wave was not ported, whether the ideas were already incorporated under another
shape, and what insights/questions fall out of the comparison.

I compared:

- designer reports 686, 687, 694, 696, 699, 704, 705, 706, and 707;
- preserved PoC code under `/tmp/mentci-poc` and
  `reports/designer/694-cluster-propagation-poc/harness`;
- current main implementations in Mentci, criome, signal-criome, router,
  spirit, orchestrate, and schema-next;
- live branch state for `signal-criome-peers`, `criome-peer-transport`,
  `criome-client-approval-witness`, `criome-auto-approve`,
  `next/impl-reference-syntax`, and the preserved schema capability branches.

## Executive result

Most designer PoCs were not lost. The main landed lines are real:

- Mentci's typed component shape, daemon state, contract vocabulary, edited
  answers as proposals, and shared `mentci-lib` model were incorporated.
- The criome ClientApproval park substrate and witness binaries were
  incorporated on criome main.
- The schema `{| |}` impl-reference prototype is effectively incorporated on
  `schema-next` main; the branch diff is now zero.
- The criome-gated propagation PoC was incorporated and improved in the
  spirit/router/criome mainline stack.
- The orchestrate worktree-registry daemon core was incorporated.

The important unported ideas are narrower and sharper:

- Mentci still lacks the PoC's real long-lived subscription push; current daemon
  connections are one request, one reply, then close.
- Mentci egui still cannot decide/answer parked questions; the approval-card
  surface is not built.
- The orchestrate daemon has the worktree registry, but primary's
  `orchestrate-cli` has no `worktree` argv adapter yet.
- E1 peer transport increments 1-3 are still on designer branches, not main:
  `signal-criome-peers` and `criome-peer-transport`.
- The criome VM proof/de-branch is still not on test-cluster main.
- The preserved schema capability-resolution branch is not ported; its idea is
  adjacent to the now-landed impl catalog but not the same feature.

## Mentci PoC

Designer PoC source: `/tmp/mentci-poc`, reports 686 and 687.

### Incorporated

The durable conceptual spine is present in the mainline Mentci stack:

- `signal-mentci` has the working contract verbs: `PresentQuestion`,
  `PushUpdate`, `ObserveInterfaceState`, `AnswerQuestion`,
  `ProposeEditedAnswer`, and `RetractInterfaceObservation`.
- `mentci` has a real daemon, one-argument binary startup, Unix socket frame
  codec, in-memory canonical interface state, daemon-minted question and
  subscription identifiers, projection by `InterfaceInterest`, and edited
  answers as typed `AnswerProposal` records.
- `mentci-lib` now owns the shared MVU-ish `ObservationModel`,
  `ApprovalModel`, NOTA fallback rendering, and the `CriomeVerdict` mapping.
- `mentci-egui` consumes that shared model instead of carrying duplicate
  approval logic.
- `meta-signal-mentci` now carries typed component socket endpoints:
  `Mentci`, `MetaMentci`, `Criome`, and `MetaCriome`.
- `mentci` now picks up criome parked ClientApproval requests on
  `ObserveInterfaceState`: the daemon polls criome's meta socket for parked
  authorizations, absorbs unseen slots into pending questions, and projects
  them to clients.

That is a substantial port. The old PoC's "daemon owns canonical UI state;
clients are thin renderers" model did land.

### Not incorporated

The PoC's most interesting runtime behavior is not yet ported: a long-lived
subscriber stays connected and receives pushed state updates when canonical
state changes. Current `mentci` reads one `MentciFrame`, applies the request,
writes one reply, and returns. `signal-mentci` defines stream/event types, and
the frame type supports `SubscriptionEvent`, but the daemon does not maintain
open client streams or fan out `MentciEvent::InterfaceStateChanged`.

So the current daemon is "observe as snapshot/poll" plus "query criome parked
queue on observe," not the PoC's full push-subscription daemon.

The egui approval card is also not incorporated. The shell displays
`ObservationView` and reply NOTA, but it cannot submit an `AnswerQuestion` or
`ProposeEditedAnswer` interaction. The CLI has direct criome meta atoms
(`criome:parked`, `criome:approve:<slot>`, `criome:reject:<slot>`,
`criome:defer:<slot>`), but the GUI remains observe-oriented.

### Insight

The current implementation made a pragmatic shortcut: it gets a real GUI client
connected to a real daemon and pulls criome parked questions into daemon state
without implementing the full resident event stream. That was the right first
proof, but it should not be confused with the 7x5z programmable-UI daemon in
full. The missing feature is not another widget; it is the daemon's persistent
subscription transport.

## Criome ClientApproval and witness branches

Designer sources: reports 704 and 705; branches `criome-auto-approve` and
`criome-client-approval-witness`.

### Incorporated

The runtime ideas are on main:

- `signal-criome` main has `AuthorizationMode` including ClientApproval and the
  parked authorization surface.
- `meta-signal-criome` main has the answer-by-slot approval surface.
- `criome` main has AutoApprove/ClientApproval runtime behavior, boundary
  hardening, and the witness binaries:
  `criome-auto-approve-witness-test` and
  `criome-client-approval-witness-test`.

The witness bins exist on criome main and exercise the same process-level proof
the designer branch described: configure mode over the meta socket, park over
the working socket, list parked authorizations over meta, decide over meta, and
observe Granted/Denied over the working socket.

### Not incorporated

The branches still exist and show diffs against main because they are stale
parallel history, not because the idea is absent. They should be treated as
retirable only after one final functional comparison, not as work to merge.

The real unported item is outside criome itself: the NixOS/test-cluster
de-branch. The VM checks are still not on test-cluster main, and the
ClientApproval park VM proof is still not a mainline check.

### Insight

The process witness is good enough to build Mentci against; the VM witness is
what prevents drift. Without the test-cluster merge, the strongest proof stays
out of the normal check path.

## E1 peer transport

Designer source: report 706; branches `signal-criome-peers` and
`criome-peer-transport`.

### Incorporated

Only conceptually. Main criome has dormant in-process signature-solicitation
verbs (`RouteSignatureRequest` / `SubmitSignature`) from earlier work, and
later design reports use that fact correctly.

### Not incorporated

The actual E1 increments 1-3 are not on main:

- `signal-criome-peers` is two commits ahead of main, adding `PeerAddress`,
  `PeerNode`, `PeerEnvelope`, and `Peers` on `CriomeDaemonConfiguration`.
- `criome-peer-transport` is two commits ahead of main, adding the TCP peer
  codec/client, BLS peer-frame DST, verify-before-decode, length-prefixed
  envelope+frame wire format, timeout hardening, and negative tests.

Current `signal-criome` main has no peer types, and current `criome` main has
no TCP peer transport hits. This is the clearest "designer made a good PoC and
operator did not port it" item.

### Insight

This is not optional polish. It is the bridge from local proof to real
networked criome quorum. The code is branch-contained and has strong
adversarial review notes; the remaining risk is integration shape, not whether
the primitive is worth keeping.

## Criome-gated propagation PoC

Designer source: report 694 harness and report 700 operator brief.

### Incorporated

This was ported more deeply than the original harness:

- `router` main has `AuthorizedObjectFanout`, typed
  `PublishAuthorizedObjectReference`, and a `StandardReference` projection from
  `signal_criome::AuthorizedObjectReference`.
- `router` preserves `AuthorizedObjectKind::Head`; the harness-era glue mapped
  only the older operation-style shape.
- `spirit` main has the offline full-chain test with criome authorizing the
  shipped D1 head, router carrying typed `{ Spirit, Head }`, and a D1/D2
  falsifier proving restore-latest is rejected when it is not the delivered
  digest.
- `spirit/src/criome_gate.rs` has the production local-gate noun over a real
  criome socket, using `spawn_blocking` for the synchronous criome client.

### Still not incorporated

The final semantic target is still not real: fetch/adopt exactly the delivered
digest D. The current mainline proof rejects a latest restore when D2 has
overtaken D1, which is the correct interim falsifier. But mirror still lacks a
fetch-by-digest restore API, so the live acquire path cannot yet retrieve D1
after D2 becomes latest.

### Insight

The port improved the PoC by correcting its weak glue and making the D1/D2 seam
explicit. The next missing piece is not in spirit or router; it is a mirror
capability.

## Schema impl-reference and capability-resolution prototypes

Designer sources: reports 696 and 699; branch `next/impl-reference-syntax`;
preserved branch `operator/preserve-schema-next-capability-resolution`.

### Incorporated

`next/impl-reference-syntax` has a zero-file diff against `schema-next` main.
The important pieces are present on main:

- `ImplCatalog`, `ImplReference`, `MethodSignature`, `ReferencedImpl`;
- `Schema::referenced_impls`;
- `RustSurface` and `ImplFact`;
- typed errors including `UnverifiedImplReference`,
  `UnresolvedImplTarget`, and `DuplicateImplEntry`;
- parity tests and impl-catalog tests.

### Not incorporated

The preserved capability-resolution branch is not ported. It contains an older
shape-derived capability resolver and reaction/composition work. That is not the
same as the landed impl catalog: the impl catalog names and verifies required
surface facts; the capability branch was moving toward resolving shape-derived
capabilities and standard impls. It should be mined only as a fresh port over
current main, not merged.

### Insight

The impl catalog gives the right boundary for a future real Rust-surface
builder. The capability-resolution branch may still answer "how do we populate
or consume that surface from actual code?", but it predates the current lowering
engine and would be a re-design input, not a merge candidate.

## Orchestrate worktree registry

Designer source: report 707 worktree registry design and wave-2 branches.

### Incorporated

The daemon-owned registry is on main:

- `signal-orchestrate` has the worktree observation contract.
- `meta-signal-orchestrate` has register/refresh meta orders.
- `orchestrate` has `WorktreeRegistry`, `StoredWorktree`, table storage,
  scanning, pushed-state derivation, and `worktrees.nota` projection.

### Not incorporated

Primary's `orchestrate-cli` has no `worktree` subcommands yet. The design
explicitly specified `tools/orchestrate worktree register/list/update/archive/
recycle/unregister/scan`; the daemon can do the typed work, but the familiar
agent argv surface is still missing.

### Insight

This is a usability gap, not a substrate gap. Because agents actually touch
`tools/orchestrate`, the registry will not become lived protocol until the CLI
adapter lands.

## Greatest insights

1. **We repeatedly ported state but deferred liveness.** Mentci has canonical
   state but not long-lived push. Criome has parked authorization and process
   witnesses but not VM mainline checks. Propagation has typed references and
   D1/D2 rejection but not fetch-by-D. Orchestrate has the table and projection
   but not the argv adapter. The pattern is consistent: the data model landed
   before the live loop.
2. **The best PoC ideas were not UI decorations; they were ownership rules.**
   The durable ideas are "daemon owns UI state," "router fans references not
   payloads," "criome owns keys and decides," "worktree registry is daemon
   state," and "impl references verify against a real surface." Those mostly
   did land.
3. **The biggest unported code is E1, not Mentci.** Mentci's missing pieces are
   interaction/liveness. E1's missing piece is actual branch code: peer contract
   and transport primitive are still off-main.
4. **The current Mentci sandbox proof is honest but easy to overread.** It proves
   connected observe and criome parked pickup. It does not yet prove the daemon
   can call back the GUI asynchronously after the initial request, which was a
   central reason the psyche wanted a full client rather than only CLI.
5. **Some stale branches are now hazardous as signals.** `criome-auto-approve`
   and `criome-client-approval-witness` look like unmerged work, but their
   substance is on main. `signal-criome-peers` and `criome-peer-transport` look
   similar but are genuinely unported. We need a cleanup pass that marks
   subsumed branches separately from live handoff branches.

## Questions for the psyche

1. Should the next Mentci slice prioritize **real streaming subscriptions** or
   the **egui approval card**? The approval card is more visible; streaming is
   closer to the original full-client concept.
2. Should I port E1 increments 1-3 to main now, before increment 4, so the
   branch-reviewed peer transport becomes a stable substrate?
3. Should the test-cluster de-branch/VM proof be treated as a release gate for
   further criome/Mentci work, or can it trail while UI liveness advances?
4. Do you want the primary `tools/orchestrate worktree ...` adapter now, since
   the daemon registry is already landed?
5. Should the preserved schema capability-resolution idea be revived soon as a
   fresh design over the landed impl catalog, or left archived until a concrete
   method-call/resolver need appears?
