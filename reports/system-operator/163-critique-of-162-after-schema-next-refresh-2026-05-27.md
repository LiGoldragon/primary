# Critique Of 162 After Schema-Next Refresh — 2026-05-27

## Frame

This critiques `reports/system-operator/162-production-to-lean-criomos-reconciliation-2026-05-27.md` after refreshing the freshest NOTA/schema-next design surface:

- `reports/designer/385-nota-schema-next-stack-design-via-nix-tests-2026-05-27.md`
- `reports/designer-assistant/384-emit-to-src-schema-2026-05-27.md`
- `reports/designer-assistant/383-next-version-schema-design-study-and-implement-2026-05-27.md`
- `reports/system-designer/35-schema-deep-new-logics/1-vision-schema-deep-new-logics.md`
- `reports/system-designer/35-schema-deep-new-logics/2-schema-deep-lojix-next-pilot.md`
- `reports/system-designer/35-schema-deep-new-logics/3-overview.md`
- `reports/operator/212-brace-namespace-and-schema-modules-2026-05-27.md`
- `reports/operator/211-declarative-schema-macro-implementation-2026-05-27.md`
- `reports/designer/380-bottom-up-tour-02-schema-macros-2026-05-27.md`

The report being critiqued was useful as a system-operator snapshot, but it is now too narrow to serve as the next implementation plan.

## Findings

### 1. The Report Treats `horizon-leaner-shape` As “The Next Stack”

Severity: high.

`162` correctly identified the production-to-lean drift for the `horizon-leaner-shape` track. The problem is that the fresh schema-next work changes the map. The schema-deep Lojix pilot is no longer abstract future design: it has a pushed `schema-deep` branch, a `schema/lojix.schema`, schema-emitted runtime nouns, a deeper actor topology, and a green Nix witness family in `reports/system-designer/35-schema-deep-new-logics/3-overview.md`.

The better framing is:

- `horizon-leaner-shape` is the current lean cutover track.
- `schema-deep` is the stronger next architecture candidate and likely amalgamation target.
- Production fixes from `162` must feed whichever track becomes production, but porting them to `horizon-leaner-shape` is not the same as finishing the next stack.

Consequence: `162` should not be used as the implementation order for “new Lojix”. It should be renamed mentally to a production-to-lean snapshot.

### 2. “Port Bracket NOTA Support Into `horizon-rs`” Is Probably The Wrong Long-Term Move

Severity: high.

`162` recommends “port production NOTA/bracket-string parser support into `horizon-rs/horizon-leaner-shape`.” That may be a tactical unblocker if the old lean stack must build now, but it is not the schema-next direction.

Current schema-next architecture says:

- NOTA parsing belongs to `nota-next`.
- Schema lowering belongs to `schema-next`.
- Rust emission belongs to `schema-rust-next`.
- Crates carry `schema/lib.schema`.
- Braces are key/value maps.
- Colon-qualified names are the schema namespace path.
- Generated Rust lives in a schema-shaped module tree, with the current design corrected toward `src/schema/`.

So the durable move is not “teach old `horizon-rs` the new text details.” The durable move is to make Horizon proposal/view nouns schema-authored and emitted through the nota-next/schema-next path, or at least to define exactly why old `horizon-rs` survives inside the new architecture.

Tactical patch acceptable; architectural target missing.

### 3. The Report Understates The Difference Between “Policy Checks Passed” And “Lean OS Builds”

Severity: medium-high.

`162` says the ported lean policy checks passed, and it correctly says real lean full-OS builds were blocked. But its “Ported In This Pass” wording is stronger than the evidence.

The direct checks proved several local policies:

- Nix role policy.
- Desktop audio policy.
- Router Wi-Fi secret/projection policy.
- Firmware policy.
- Legacy Chroma removal check.
- WireGuard projection tolerance check.

They did not prove:

- Lean Horizon projection works.
- Lean `goldragon/datom.nota` is current.
- Lean full `nixosConfigurations.target` evaluates.
- Lean Lojix can build every production node.
- The ported modules compose with Home, CriomOS-lib, and the actual projected view.

Better wording: the fixes were staged and locally witnessed, not port-complete.

### 4. Repository Source Distribution Should Be A Schema/Actor Noun, Not A Footnote

Severity: high.

`162` correctly finds that `repository-ledger` as `gitolite@localhost` breaks distributed builds. The critique is that the remedy list is too ad hoc for the fresh schema-deep design.

In schema-deep Lojix, source movement is not just a flake-input inconvenience. It is a deployment-plan concern that should become typed state:

- source reference;
- source availability;
- builder capability;
- cache/copy plan;
- target activation plan;
- fallback decision;
- observation trace.

The `Builder`, `ClosureCopier`, `Activator`, `GcRootPinner`, `Store`, and `ObservationFan` planes in the schema-deep pilot are exactly where this belongs. The report’s “Arca staging is cleaner long-term” is directionally right but too weak. Source distribution should be first-class in the schema-emitted Lojix plan, not only an optional remedy after a failed fetch.

### 5. The Balboa Failure Should Be Classified As Capability Planning Failure

Severity: medium.

`162` says Balboa failed because Prometheus is x86_64-only and Balboa is aarch64. That is accurate. But the schema-deep design suggests a stronger invariant: Lojix should not ask Nix to build an incompatible target and then discover the error through cascading derivation failures.

The builder plane should inspect or project builder capabilities first. The request should fail early with a typed Lojix rejection such as “no builder supports `aarch64-linux`,” or route to an aarch64 builder/emulation node if one is declared. This belongs in the schema-emitted build plan and observation stream.

### 6. Store Paths In The Report Are Low-Value And Violate The Testing-Artifact Discipline

Severity: medium.

`162` records full Nix store paths for successful builds. That gives short-term proof, but it is noisy and not durable: store hashes are opaque, token-expensive, and not useful as architecture evidence. The testing skill says not to record raw store hashes in docs; let Nix produce them.

Better report shape:

- record the exact Lojix command shape;
- record pass/fail per node;
- record the failure class and root cause;
- if a store path is needed operationally, keep it in shell output or a machine-readable build ledger, not a prose report.

### 7. The Report Misses The Schema-Deep Amalgamation Consequence

Severity: high.

`reports/system-designer/35-schema-deep-new-logics/3-overview.md` explicitly says records 905/908 feed the lean stack and must be carried forward when schema-deep is promoted. `162` was itself part of 905/908, but it did not close the loop:

- Which of the production fixes become fields/variants in `schema/lojix.schema`?
- Which remain CriomOS Nix module details?
- Which belong in Horizon projection?
- Which belong in pan-Horizon constants?
- Which become schema-deep actor messages or SEMA records?

Without this mapping, a future operator may port the same fix twice: once to lean hand-authored types, then again to schema-deep emitted nouns.

### 8. The Report Correctly Rejects Wholesale Rebase

Severity: positive finding.

The strongest part of `162` is the decision not to wholesale rebase. That remains correct after schema-next refresh. Schema files, proposal shapes, Lojix runtime types, and CriomOS projection consumers have diverged semantically. Mechanical rebase would hide architecture decisions inside conflict resolution.

The right path is still semantic porting, but now semantic porting needs a three-column matrix:

- production `main`;
- current lean `horizon-leaner-shape`;
- schema-deep / schema-next target.

### 9. The Report Correctly Finds Router Wi-Fi Fallback Debt

Severity: positive finding with stronger consequence.

`162` correctly calls router Wi-Fi projection fallback transitional. The stronger schema-next reading is that SSID derivation and Wi-Fi auth shape should be schema-visible, not buried in CriomOS Nix defaults.

Production cluster data should select feature variants and secret references. Horizon/schema reduction should derive:

- network name from cluster identity;
- auth mode such as password migration vs certificate EAP;
- country/regulatory configuration from the right non-cluster-specific source;
- runtime secret binding shape.

CriomOS should consume the projected typed view without string fallback policy beyond narrow compatibility shims.

## Revised Next Sequence

1. Treat `162` as a historical production-to-lean audit, not as the current next-stack roadmap.
2. Create a production-fix carry-forward matrix with one row per production fix and columns for `horizon-leaner-shape`, `schema-deep`, Horizon projection, CriomOS, CriomOS-home, and CriomOS-lib.
3. Decide whether the next implementation target is old lean cutover first or schema-deep amalgamation first. The two can coexist, but they should not silently compete.
4. If old lean cutover is still required, patch `horizon-rs` only enough to parse current NOTA and run lean full-OS builds. Mark it tactical.
5. For the durable path, express Horizon/Lojix proposal/view/deploy nouns through `schema/` files and schema-emitted Rust, following the nota-next/schema-next/schema-rust-next stack.
6. Promote repository source distribution, builder capability, cache/copy route, and activation target into schema-emitted Lojix nouns and actor messages.
7. Add a Lojix capability preflight witness so Balboa-style architecture mismatches fail before Nix begins a doomed build.

## Bottom Line

`162` is a useful snapshot of production drift and remote-build failures. It is not wrong in its local facts, but it is stale as architecture guidance. After the schema-next refresh, the main correction is to stop treating `horizon-leaner-shape` as the sole “next stack” and start mapping production fixes into the schema-deep future as first-class schema nouns, actor messages, and SEMA records.
