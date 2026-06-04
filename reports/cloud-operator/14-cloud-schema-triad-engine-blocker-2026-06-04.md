---
title: Cloud schema triad engine blocker
role: cloud-operator
date: 2026-06-04
status: current
---

# Cloud schema triad engine blocker

The actual generated schema-based triad engine for `cloud` is not done.
The completed work so far is narrower: `cloud/schema/sema.schema` and
`cloud/schema/nexus.schema` are real runtime schema files, and the SEMA
schema lowers with current local generator code.

The current blocker is in `schema-next`, not in the cloud runtime file
names. `cloud/schema/nexus.schema` imports `cloud:sema:*` roots. The
`cloud:sema` module itself imports `signal-cloud` and `meta-signal-cloud`
contract types. Current `schema-next` resolves a directly imported module by
lowering that module without carrying the caller's resolver through nested
imports. A direct `signal-cloud:lib:Input` root import lowers in isolation;
`cloud:nexus` fails when resolving `cloud:sema` because nested imports lose
the resolver and report `UnresolvedImportCrate { crate_name: "signal-cloud" }`.

The `schema-next` repository is currently claimed by the operator lane for
`primary-1tsw` (`schema-next: read multiple plane-schemas per crate`). Its
working tree already contains uncommitted multi-module/root-import edits, so
this cloud-operator pass should not overwrite it.

Implementation conclusion: a hand-written cloud engine could be made
triad-shaped today, but that would not be the intended generated
schema-based triad engine. The no-regret next step is to finish and commit the
claimed `schema-next` multi-plane recursive import work, then generate and
compile the cloud Nexus and SEMA runtime modules with `schema-rust-next`'s
`NexusRuntime` and `SemaRuntime` targets.
