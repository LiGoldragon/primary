# 54 — lojix test operation: frame and method

## Why this session

The psyche has steered the VM-testing surface that report 53 placed in an
external `vmtest` CLI **into the LOJIX component itself**, and refined the
node host model. Two psyche statements anchor the convergence:

> "config gives it a default, and it has a shorthand verb for quick
> routine operations, which we can start maintaining in a schema file.
> maybe this all actually belongs in the lojix component."

> "keeping each node's vmhost fixed in its declaration ... even if it's
> more than one host, which would give them permission to send each other
> the image for it".

So the test orchestration becomes a first-class **meta-signal-lojix**
operation with a config-default vmhost and a shorthand verb, and a test-VM
node may declare **one or more** fixed vmhosts whose declared host-set is
the image-distribution trust boundary.

This is a real contract change to two production-track components
(`horizon-rs` and the `lojix` triad), so the deliverable is a **proposal
for psyche confirmation before building**, not a build.

## Scope

1. HORIZON multi-host node model — representation + image-exchange
   permission wiring + invariant updates; single-host nodes unaffected.
2. The lojix test OPERATION — ordinary vs meta placement, fields, schema
   file, modern syntax.
3. The SHORTHAND verb — lowering to the full op via config defaults
   (spirit `State` precedent).
4. The config-default vmhost — new `DaemonConfiguration` field(s).
5. DISPATCH + LIFECYCLE + DURABLE RESULT — hermetic vs live (report-47
   v2, daemon-driven), the queryable test-result record, vmhost
   resolution (config-default + per-request override within the declared
   set).
6. Implementation order + gates (Prometheus live run stays psyche-gated).

## Method

Three grounding sub-reports (multihost model, lojix-op placement,
dispatch-lifecycle) were produced read-only against the live source, then
synthesized here. Before writing, the synthesizer re-verified every
load-bearing surface against the actual files:

- `Machine` field order and the `super_node`/`super_user` host edge —
  `horizon-rs … lib/src/machine.rs` (worktree `horizon-test-vm` carries
  the C1 `disk_gb`/`location` tail; field order confirmed).
- `VmHostCapability`/`guest_subnet`/`NodeService::VmHost` —
  `horizon-rs … lib/src/proposal.rs:128-246` (worktree).
- meta contract root `[Deploy Pin Unpin Retire]` + reply root + the
  `{...}` body and shared-type imports —
  `meta-signal-lojix/schema/lib.schema`.
- ordinary `Selection [(ByNode …) (ByGeneration …) (ByEventLog …)]` and
  the `SystemAction`'s pre-existing `Test` activation variant (a distinct
  concern from this op) — `signal-lojix/schema/lib.schema`.
- `DaemonConfiguration` (exactly five fields, rkyv-only) —
  `lojix/src/lib.rs:163-170`.
- `DeployJobTable`/`DeployJob` (the durable pattern to mirror) and
  `ContainerLifecycleRecord` (built-but-undriven) —
  `lojix/schema/sema.schema:81-93`.
- report 53 §4 converged `[(Run …) (Standard …)]` two-variant shorthand
  shape — `reports/cloud-designer/53-vmtest-autopickup-and-client/4-proposal.md`.

## Hard constraints honored

- NOTA positional records, full-English identifiers, no `(key value)`,
  no tail-omission (the shorthand is a real shorter variant, never a
  defaulted field).
- Daemons take only binary rkyv startup config — the default vmhost is a
  `DaemonConfiguration` field, NOT a `Configure` wire op or a flag.
- Methods-only Rust (`Machine::host_set`, the projection folds as
  methods on the data-bearing types).
- No backward-compat constraint pre-production; additive where it keeps
  the single-host majority byte-identical only because that is the
  smaller correct shape, not as a compat goal.
- The first Prometheus LIVE run stays behind explicit psyche
  authorization.

## Output

The proposal is `4-proposal.md`. Chat carries the executive summary plus
the open decisions needing psyche confirmation.
