# Lojix Source Staging Prototype And Full-Component Critique

Kind: Implementation audit
Role: system-operator
Date: 2026-05-27

## Source Intent Mined

This report follows the current psyche constraint recorded as Spirit
record 974: prototypes for the CriomOS/Lojix/Horizon rewrite must use
the designed components fully; if a component is too incomplete to use,
the prototype should develop that component instead of bypassing it.

Recent report inputs:

- `reports/system-operator/164-criomos-lojix-rewrite-audit-and-production-vision-2026-05-27.md`
- `reports/system-operator/163-critique-of-162-after-schema-next-refresh-2026-05-27.md`
- `reports/system-designer/36-criomos-reconciliation-audit.md`
- the `lojix/schema-deep` repo architecture and local tests

The practical gap chosen for this prototype was source staging. Earlier
audits said the new deploy stack needs a real source-distribution plane
instead of pretending a raw Horizon string can be the build input.

## Implemented Prototype

Worktree:

- `/home/li/wt/github.com/LiGoldragon/lojix/schema-deep`

Main changes:

- Added schema nouns in `schema/lojix.schema`: `SourceDigest`,
  `SourceRecord`, `SemaCommand::RecordSource`,
  `ActorRequest::StageSources`, `ActorReply::SourcesReady`, and
  `Phase::StagingSources`.
- Changed `BuildRecord` to carry the `SourceDigest` it built.
- Added `src/runtime/source_stager.rs` as a real Kameo actor with
  state: the source artifact directory plus the most recent staged
  source.
- Changed the submit pipeline to run
  `PlanRecord -> SourceStager -> Store::RecordSource -> Builder`.
- Changed `Builder` and `ProcessToolchain` so builds consume
  `SourceRecord`, not `PlanRecord`.
- Added Store source ledger state and `SourcesSnapshot` for tests.
- Added trace and observation witnesses for source staging.
- Changed the staged source artifact to canonical NOTA by writing the
  schema-generated `SourceRecord::to_nota()` text, not a new key/value
  format.
- Updated repo docs so `AGENTS.md` no longer claims this repo is only a
  skeleton and `ARCHITECTURE.md` includes the source-staging plane.

## Evidence

Local inner-loop evidence:

- `cargo fmt`
- `cargo check`
- `cargo test`

Canonical Nix evidence:

- `nix --max-jobs 0 flake check -L`
- The Nix build dispatched to `ssh-ng://nix-ssh@prometheus.goldragon.criome`.
- The check passed build, test, fmt, clippy,
  `schema-deep-build-script`, `schema-deep-actor-mailboxes`, and
  `binary-boundary-test`.

The new architecture witness is:

- `tests/source_staging.rs::lojix_next_submit_stages_sources_before_build`

It proves a submit request stages a source, commits a `SourceRecord`
through Store, writes a NOTA source artifact, and only then lets the
build plane consume that staged source.

## Full-Component Critique

The prototype uses these designed components correctly enough for the
next step:

- Schema is the source of the new nouns and mailbox variants.
- Kameo owns the source-staging plane as an actor, not a helper.
- Store records the staged source through a schema-emitted
  `SemaCommand`, not an ad hoc side channel.
- The trace plane and observation plane can see the new phase.
- Nix exposes the tests as flake checks and the build ran remotely.
- NOTA remains the artifact text format.

The prototype is still not using every designed component fully:

- ARCA is not yet the backing content-addressed propagation store.
  `SourceStager` writes a local NOTA file under daemon state. That is
  better than an opaque string, but not the final store.
- SEMA is still in-memory. The generated `DatabaseMarker` is filled by
  a placeholder `DatabaseMarker::memory()` method instead of a real
  redb/sema-engine transaction marker.
- Criome authorization is still a local policy enum path. The request
  is not routed through `criome-daemon`, and no signed authorization
  object is verified.
- Owner signal is still absent. Policy actions such as preparing plans
  or deploy approvals are not separated into `owner-signal-lojix`.
- Horizon is still represented as `HorizonView(Text)`. The prototype
  does not yet project the redesigned pan-horizon + cluster proposal
  into a typed view inside the daemon.
- The nspawn witness is still a sandbox command marker. It proves actor
  ordering, not real `systemd-nspawn` execution.
- Source staging does not yet consume Git refs, ARCA objects, or
  content-addressed proposal artifacts. Its digest is derived from
  deployment identifier, Horizon text, and target node.

## Next Prototype Slice

The next slice should replace one placeholder with the designed
component rather than adding another shortcut. Best candidates:

1. Develop Store from in-memory vectors to a redb/sema-engine-backed
   database so `DatabaseMarker` stops being a placeholder.
2. Develop source staging into an ARCA-backed content-addressed import
   path while preserving the existing `SourceRecord` and
   `StageSources` actor contract.
3. Develop Horizon projection so `HorizonView` is not a text wrapper
   but a generated view object consumed by source staging and build
   planning.

My recommendation is to do SEMA persistence next. It is the narrowest
place where the current prototype is explicitly lying: reply markers
claim a database marker, but runtime still supplies a synthetic
`memory` marker. Fixing that gives every later prototype a durable
truth surface.
