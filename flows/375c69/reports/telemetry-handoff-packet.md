# Telemetry handoff — approval packet

Owner: Mind flowNexus Secondary, flow `375c69`, Codex native
`01a1adec-61db-7213-8374-830375c69de2` (observed in CODEX_THREAD_ID).
Original task deadline: 00:20:08 UTC; succession does not reset it.

## Index

- Send 8711: own identity and HOLD.
- Send 8712: demonstrated adoption boundary and smallest correction.
- Send 8713: isolated regression, owned live proof and 0.52 carry contract.
- Send 8714: separate typed read-only context observer proposal.
- Send 8900: recovery inventory and existing trim-owner inquiry.
- Send 9048: exact pins and operational/regression scope split.
- Send 9052: separate observer design scope and snapshot qualification.
- Sends 9140–9141: proposed B appointment, isolation/effects and cleanup contract.
- `B/staging.md`: sole Luna staging runner report; no test effects authorized.
- Sends 9248–9249: exact C wire source and bounded writer audit.
- Send 9313: coherent candidate client/runtime reachability and C test custody.
- Send 9371: conditioned C errors and retained-observed-identity semantics.

## Custody and effects

No implementation/test runner exists. Core subsequently appointed one sole
Luna explorer, `/root/b_capsule_staging`, for read-only B bootstrap staging.
It performed no tests/builds/capsule creation; its report leaves capsule
capability and verified main-flow native identity unknown. No source/test locks
are held. Report locks protect only owned reports and are released after writing.
No source changes, tests, store
opens, configuration changes, harness restarts, deployment or production probes
have been performed by this successor. Read-only source/process observations and
flow messages are the work so far. Peer-only ResolveCaller.None returned
CallerUnknown; that result supplies no privileged execution authority.

All runtime HOLDs remain. Core must name and authorize the source/test/deploy
custodians before effects. A separately cleared supported book refresh does not
depend on speculative source rewriting.

## Established cause and boundary

Installed 0.51 source: `/nix/store/dz5dwigzydw2khv6wpgq3556hw83j4x7-source`.
Its Cargo pins are signal-flow `ce083f2ba9cc0bd928735ba4cc09e59965982e30`
and meta-signal-flow `281f5aa1b88cd43609c127cdf6f3c12645faf58b`.
Local flow HEAD `53782fba5e1f5b761b87f09809c0b319bcc27ad0` was observed;
equivalence to the installed source and writable-baseline approval are unproved.
Paths below are relative to `crates/flow-nexus/src/`.

Predecessor observation: bookmaker b4379a Claude process had a 0.44 flow-hook and
legacy FLOW_SOCKET; its Stop reports reached the legacy Nexus, while the 0.51
event query was empty. Actual 0.51 stored context remains unknown. Transcript
token totals are measurements of native input, not observations of that row.

Independent successor source inspection:

- `lib.rs:499–572`: MetaBindExisting verifies the seat, then adopts its records.
- `sending.rs:976–1168`: ordinary Adopt/BindSeat also verifies and adopts records.
- `binding.rs:132–206`: role, model, live process, cwd, Herdr and native identity
  are checked; endpoint/origin observations are preserved only for the same
  native session. These paths establish no hook/socket handoff.
- `herdr/launch.rs:484–519`: a new Claude launch already renders the configured
  hook binary and explicit ordinary socket for five harness events.
- `reporting.rs:118–163`: only a correlated Stop settles the flow.
- `store/context.rs:23–105,145–183`: measurement is optional; equality meets the
  configured refresh mark. No comparison defect has been demonstrated.

Adoption establishes ownership, not reporting migration. The smallest immediate
correction is the supported fresh-launch/refresh path under approved custody,
followed by actual process hook/socket and correlated 0.51 Stop observations.
No same-session restart or threshold patch is proposed. A regression-only commit
does not itself fix already-running inherited processes.

## Regression and proof contract — proposed, not run

Existing `herdr/launch.rs:3421` test
`every_claude_hook_command_carries_the_typed_nexus_socket` already covers the
socket on all five events. Reuse it; the missing proposed delta is the selected
executable plus socket through the actual fresh/refresh path with legacy parent
environment, and adoption-to-successor end-to-end behavior. Regression authority
covers tests/isolated fixtures only, not production implementation edits.

1. Isolated capsule, pinned source: independently inspect fresh and supported
   refresh Claude launch settings. All five events must name the selected hook
   binary and explicit intended socket even when parent environment names 0.44.
2. Legacy adoption fixture: prove identity adoption alone leaves the old process
   hook/socket unchanged. Do not label that telemetry migration.
3. Correlated Stop records context and settles; a wrong native Stop settles
   nothing. Exercise below, equal and above the configured mark using the actual
   recording path, for Maintained and OnDemand.
4. Isolated integration: different successor native identity, predecessor
   retired, queued logical delivery reaches successor exactly once, and the
   predecessor receives no new delivery. Distinguish emission, receipt,
   correlation, stored row, decision, launch and native delivery evidence.
5. Independent test verdict gates a repository commit. Controlled deployment
   requires exact revision and named custody approval. Then one owned cheap live
   flow crosses its existing configured mark; prove actual hook/socket, recorded
   context, successor and queue delivery. Book refresh alone is not this proof.
6. Explicitly carry the regression contract, fixtures and any approved observer
   into 0.52. No unrelated production probe or threshold reconfiguration.

Source commit scope merits: demonstrated regression coverage; separately approved
missing observer; any further behavior correction only after a failing test and
design judgment identify the defect. No behavior bodies are authorized.

### B staging result: exact missing capability

The sole staged Luna subthread is `01a1adf5-cdf0-76e1-84d6-f0fe34833dd4`.
Its correction inspection child was PID2045130/UID1001/start29122596, parent2242,
executable `/nix/store/8aprjbczx0admjfd7zrjafk236zib0mv-zsh-5.9.2/bin/zsh`.
This identifies a collaboration subthread, not a verified standalone Flow seat.

Required and missing: a supported testing-capsule bootstrap invocation, its exact
pinned source/build definition, and an isolation witness proving no host
production socket/Memory/Herdr/home/credential mounts and no network access.
The immutable installed source filters out Nix/capsule definitions; its relevant
directories are empty. Available workspace build/dev-shell commands establish
neither this capability nor isolation. No capsule was created and no tests ran.
No further runner is appointed.

Honest inventory: existing `crates/flow/tests/hook_socket.rs` already proves an
explicit typed socket defeats inherited decoy FLOW_SOCKET with env_clear;
existing herdr launch test covers all five event sockets. Neither proves OS
isolation or the complete adoption/refresh lifecycle. Preserve these tests;
propose only the missing end-to-end witnesses once capsule custody is available.
This gap holds B test effects, and leaves A supported refresh independent.

## Separate read-only context projection — proposed before bodies

Core approved the direction, with conditioned shape; bodies remain unauthorized.
Add a typed meta query for one known FlowId. Return its native session identity,
optional model, optional recorded tokens and optional configured refresh tokens.
Unknown flow and store failure have typed refusals. Reuse existing public wire
names when the wire-source design is reviewed; this sketch is not final syntax:

```ethos
; Query additions
ReadContext.FlowId
; Reply additions
ContextRead.{ FlowId NativeSessionId Option<ModelName>
              Option<ContextTokens.Integer> Option<RefreshTokens.Integer> }
ReadContextRejected.[ UnknownFlow.FlowId StoreRefused.StoreRefusal ]
```

Exact authored wire source is meta-signal-flow at the pinned revision,
`ethos/signal.ethos`. Reuse existing ContextTokens/RefreshTokens declarations
and existing StoreRefusal with actual error evidence. Generated output is
`src/generated/signal.rs`; existing boundary tests are `tests/contract.rs`.

Return explicitly separate observations, not a snapshot. Retain the INITIAL
held identity and observed model if the flow changes/disappears later; never
silently replace it with a later native identity. Read threshold for that
returned observed model. Recorded context is keyed by FlowId and has no native
provenance, so make no simultaneous/native-bound measurement claim.

The writer audit found Claude Stop at waking2715/2729 and Codex token usage at
compacting343–355 converge through performing665–667 into the keyed context
writer. The Claude measurement precedes the later dispatch gate. Configure
replaces threshold families atomically but separate match_records reads do not
prove a cross-table snapshot. No new locking or storage machinery is proposed.
No new store, migration, transcript scan, backfill, settlement or refresh. Return
the stored measurement as such: absent is unmeasured, zero is zero. Existing rows
carry no timestamp/hook provenance, so return neither invented datum. Consumers
check returned native identity before acting on the observation.

Tests: missing row, actual zero, missing model/threshold, past known flow,
unknown flow, rewrite/reopen, equality and stale expected native identity at the
consumer; compare row/events/queue before and after reads. This is observability,
not a threshold repair or a prerequisite to supported book refresh.

Observer candidate scope is the pinned meta-signal-flow authored vocabulary and
round-trip tests, flow `lib.rs` dispatch/projection and isolated tests, and Cargo
manifest/lock only for the reviewed contract pin. Confirm the authored wire
filename at that pinned tree rather than assuming it. Storage schema and
`store/context.rs` are dependencies to read, not edit. Wire shape and observation
consistency require separate design judgment before bodies. A new adoption
telemetry-admission policy would be a third design decision, not bundled here.

### Core allocation, not implementation authority

Core allocated NEW meta-signal-flow **61.0.0** for this narrow 0.51 observer.
The one local scoped ref/manifest/reservation check found no 61 collision;
unpublished and remote claims remain unknown. A fresh remote/ref plus owner-claim
check is required before staging/publication. A conflict stops the work; no
overwrite or automatic renumbering. No body/build/publication/deploy grant is
implied by allocation. Exact error/consistency semantics, consumer tests and
custody still gate bodies.

Candidate meta derives from exact `281f5aa1b88cd43609c127cdf6f3c12645faf58b`,
retaining signal-flow `ce083f2ba9cc0bd928735ba4cc09e59965982e30` and flow-ethos
`b92b9689190c62db4f4c66a2b39cafe356cec1e4`. The coherent 0.51 candidate client
and runtime repin together, preserving the workspace flow-ethos patch identity.
The existing installed client is not a consumer of the new query.

0.52 has separately reserved meta **60.0.0**. It must explicitly compose the
observer later IF adopted. Version-number ordering proves neither ancestry nor
observer inclusion.

## Book trim/refresh ownership

Recovered from existing Field core Secondary flow 1d381c: it owns planning and
coordination only. It has made no runtime/source/declaration effects, received no
START, and knows no cleared runtime writer or refresh operator. Its independently
reviewed-diff gate has not yet returned to it. Existing frozen packet:
`flows/1d381c/reports/three-change-classes.{before.datom,after.PROPOSED.datom,FINAL-PROPOSED.diff,FINAL-partition.json}`.
Field is excluded by MetaAspects[Psyche]; outside-pane CLI success supplies no
Field write clearance. Core Mind Secondary owns the grant/hold release.

Latest Core message reports Core Primary has cleared trim plus supported refresh;
the actual authorized execution owner and custody path remain to be named.
Bookmaker b4379a confirms no trim/refresh request or clearance received and is the
publisher, not an assumed refresh operator. It has no pending Far-lines rebuild.
Publication v2 remains preserved. A new Far-lines rebuild follows the landed
heading fix and supported refresh with observed 0.51 hook/socket, new native ID
and modules. This flow has granted no effects and retains its runtime HOLD while
the custody gap is resolved.
