# Curriculum stack migration to Datom

Migrating the surviving curriculum stack from Dotos to Datom, continuing from the earlier runtime/data separation rather than repeating it.

Remembered: 01a035d3 — depth 1

The remembered flow moved the generator runtime into public `curriculum-deploy`, made Curriculum external data, gave the runtime one typed Datom input, and cut the witnessed Primary consumer over without a compatibility path. The present workspace still exposes a broader legacy Dotos stack and an old manifest-driven Curriculum checkout, so the remaining migration boundary must be distinguished from that completed runtime cutover.

The living's opening Datom migration ruling is recorded verbatim. Current inspection established that canonical Vision already rules that everything migrates to Datom and that skill presence replaces activation manifests. It also exposed two conflicting present views: the earlier public data-only cutover and old Dotos/manifest-driven checkouts still visible in the workspace.

Dispatched the breaking cutover through an implementation subflow, with parallel read-only subflows resolving repository/ref authority and independently classifying the remaining Dotos surface. The implementation is to preserve the already-ruled external-runtime/data-only anatomy, remove rather than translate dead manifest machinery, migrate every real local consumer together, document the breaking deployment, and prove the behavioral and Nix boundaries before landing.

Repository archaeology resolved the apparent regression: the old manifest/Dotos tree is only Curriculum's stale physical Jujutsu workspace at `e7520542`. Authoritative `main@origin` is `ccd1e9f`, a data-only tree of `roles.datom` plus present skill files, and Primary already pins it with `curriculum-deploy` `ef35a6dc` and Datom `d47419ef`. The remaining audit is limited to active generated consumer artifacts and any genuinely curriculum-owned Dotos surface; Primary's unused top-level legacy Dotos inputs are outside this migration unless evidence shows the curriculum consumes them.
