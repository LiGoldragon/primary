# Refresh after new intents and reports

## Scope

I refreshed the newest Spirit records, the recent designer/operator
reports, and the current coordination state from the cluster-operator
lane.

No new Spirit record was added for this prompt. The prompt was an
execution instruction, not a durable psyche decision.

## Action Taken

I fixed the concrete coordination gap that was safe to fix from this
lane: `cluster-operator` had a report directory and Spirit intent, but
was missing from the transitional lane registry. A concurrent
third-designer refresh landed the adjacent `nota-designer` registry
case in the same window; the final transitional registry now contains
both specialized lanes and a short specialized-lane comment.

Files edited:

- `orchestrate/roles.list`
- `orchestrate/AGENTS.md`
- `AGENTS.md`

Verification:

```text
tools/orchestrate status
```

Result: `cluster-operator.lock` now appears and is idle. The same
status output also now lists `nota-designer.lock`, matching the
third-designer refresh.

I did not edit `skills/role-lanes.md`; that file is already dirty from
another lane and the durable specialized-lane skill wording should land
through designer.

## New Intent Absorbed

Spirit records through 193 are now reflected in this lane's view.

The most important newly-settled points:

- Record 163: Spirit v0.1.1 cutover uses dual-write. The old question
  "dual-write or flip?" is no longer open; implementation remains open.
- Record 165: Health and Readiness collapse onto `Magnitude` with
  `Unknown`. That question should retire from active decision lists.
- Record 176: Bird-on-Zeus updates use LiGoldragon `main` by default,
  not a Bird/Aether branch.
- Records 177-193: version migration now has a concrete main/next
  daemon protocol shape: next handles operations it can process, main
  records divergence or recovers what it can, persona-introspect is the
  natural cross-version failure-log home, and Migration trait placement
  must be decided before implementation.

## New Reports Absorbed

### `reports/designer/284-per-type-migration-trait-specification.md`

This is the concrete migration-trait design that makes the prior
main/next intent implementable. It recommends:

- a new universal crate `migration`;
- a new `signal-version-coordination` contract;
- per-type `Migration` impls with associated `Next`;
- `PeerCheck` on each component's working contract;
- persona-introspect as the cross-version failure log;
- frozen historical sibling signal repos such as
  `signal-persona-spirit-v0-1-0`.

This is ready to be turned into an operator implementation slice, but
it is not the same as the immediate Spirit dual-write wrapper. The
wrapper is the short production cutover path; the migration crate is the
durable generalization.

### `reports/third-designer/18-audit-synthesis-2026-05-22.md`

Several questions in that synthesis are now stale:

- dual-write is answered by record 163;
- Magnitude collapse is answered by record 165;
- Bird-on-Zeus branch policy is answered by record 176.

Still relevant from that report:

- `EffectEmitted` payload shape;
- sema-upgrade bootstrap shape;
- engine-manager Axis 2 timing;
- lane registry specialization discipline.

### `reports/designer/282-workspace-implementation-status.md`

The broad status remains accurate: production has Spirit,
repository-ledger, and the pre-Persona deploy stack; the Persona engine
is not production. The branch-blocker wording around Spirit is stale,
but the production blocker remains: v0.1.1 is not the default and
dual-write/cutover is still open.

### `reports/second-operator/165-current-situation-2026-05-22.md`

Second-operator's updated refresh already absorbed records 176-193. I
agree with its current priority split: Orchestrate executor migration is
valid work, but Spirit cutover stays the higher production blocker.

## Current Shortlist

### 1. Spirit cutover implementation

Decision state: settled enough to implement.

The production path is now:

1. implement the dual-write default wrapper;
2. keep v0.1.0 and v0.1.1 coherent during the migration window;
3. cut over default reads/writes to v0.1.1;
4. keep v0.1.0 read-only or compatibility-only as needed.

The old "should we use dual-write?" question is closed. The open
question is sequencing: whether to implement the short dual-write
wrapper first or start with the full `migration` crate and
`signal-version-coordination`.

Cluster-operator recommendation: do the short wrapper first, then
generalize through the migration crate.

### 2. Bird-on-Zeus update authority

Decision state: mostly settled.

Bird should be able to ask for local updates on Zeus from LiGoldragon
`main`. The first helper surface should stay narrow:

```nota
(LocalUpdate HomeProfile)
(LocalUpdate FullSwitch)
```

Still missing in code:

- Horizon grant record;
- CriomOS local helper;
- sudo rule limited to that helper;
- production `lojix-cli` local activation path;
- Nix witnesses proving Bird does not gain broad admin, wheel, root SSH,
  or trusted Nix rights.

### 3. Migration trait foundation

Decision state: designed, not implemented.

Designer /284 is the first implementation-grade shape. The one
architectural tension I want kept visible: records now say components
use `main` and `next` branches, while earlier workspace discipline says
no branches by default. This is probably a narrow version-handover
exception, but it should be said explicitly before agents generalize it.

### 4. Cluster-operator lane registration

Decision state: fixed for the transitional helper.

`tools/orchestrate status` now lists `cluster-operator.lock`. The
same pass also left `nota-designer.lock` visible through the
transitional helper. The remaining work is documentation quality:
`skills/role-lanes.md` should gain the specialized-role-vector wording
from Spirit record 174, but that should land through the designer lane.

### 5. Orchestrate executor migration

Decision state: still valid, but not the highest production blocker.

Second-operator can continue on Orchestrate if it does not interfere
with Spirit cutover. The unresolved design points are still:

- what `EffectEmitted` carries;
- whether `Watch` / `Unwatch` survive as domain streams or collapse into
  generic `Tap` / `Untap`;
- what the first high-level Mind-to-Orchestrate owner verbs are before
  Orchestrate calls Router's `Grant` / `Extend` / `Revoke` / `Deny`.

## Still-Relevant Questions

1. Should the Spirit cutover implement the short dual-write wrapper
   first, then build the general `migration` crate, or should the
   cutover wait for the full `migration` / `signal-version-coordination`
   machinery?

2. Is the record-187 `main` / `next` branch vocabulary a narrow
   exception for version-handover only, or a broader revision of the
   no-branches-by-default discipline?

3. Is `EffectEmitted` component-local typed `Effect`, universal
   `SemaObservation`, or both in two different streams?

4. Should sema-upgrade bootstrap be hand-written for the first
   production migration, with dogfooding only after the migration
   contracts stabilize?

5. Is the current Spirit release asymmetry intentional:
   `persona-spirit` and `signal-persona-spirit` at v0.1.1 while
   `owner-signal-persona-spirit` stays v0.1.0?

6. Should engine-manager Axis 2 land now as a socket/identifier rename
   pass, or be explicitly deferred so it stops showing up as a hidden
   ABI risk?

7. For Bird-on-Zeus, is the first user-visible helper surface exactly
   `HomeProfile` and `FullSwitch`, with `Test`, `BootOnce`, and other
   engineering actions deferred?

## Recommendation

The next production-critical action is still Spirit cutover. Do the
dual-write wrapper as the immediate slice, treat designer /284 as the
durable follow-up for multi-version migration, and keep Bird-on-Zeus as
a separate narrow local-authority slice rather than waiting for the new
lojix daemon.
