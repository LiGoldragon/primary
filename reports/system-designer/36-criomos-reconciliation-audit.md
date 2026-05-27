# Audit — criomos production-to-lean reconciliation

*Designer audit of `reports/system-operator/162-production-to-lean-criomos-reconciliation-2026-05-27.md`. Per psyche 2026-05-27 (Spirit 913, High): audit and critique the report after refreshing the latest nota-next / schema-next design context. The operator-class work itself is substantively sound; this audit surfaces the substrate-direction question, the cross-arc integration with the schema-deep pilot (`/35`), and discipline observations.*

## What was audited

Report `/system-operator/162` is the operator's response to Spirit records 905 + 908 + 906 (2026-05-27):

- **905** (Decision Maximum) — audit production CriomOS changes not ported to the lean lojix+horizon stack; create a report; use findings to guide the port.
- **908** (Decision Maximum) — port high-confidence changes immediately where the correct change is clear; then test.
- **906** (Constraint Maximum) — full-OS build tests must run on remote builders with `max-jobs 0`, not as local laptop fanout.

The operator delivered: ~12 high-confidence ports into `CriomOS/horizon-leaner-shape` (commit `ptzmopzwpvky` — "criomos: port production fixes to lean stack", landed on top of the existing horizon-leaner-shape arc); a full-OS build sweep against Prometheus with `max-jobs 0` (3 nodes passed, 2 nodes failed for non-module-regression reasons); identification of three architectural consequences (repository-ledger localhost-only, aarch64 strategy, horizon projection critical path); a 7-step recommended-next sequence.

## Working model for this audit

The operator's report is **substantively the right kind of work** for the lane and the captured intent. The audit's job is not to relitigate operator decisions inside their authority — it's to surface what a designer-class reading adds: substrate-direction integration, cross-arc concerns, discipline observations that improve the next iteration. I read the report against:

- Workspace discipline (`AGENTS.md`, `ESSENCE.md`, `INTENT.md`, `protocols/active-repositories.md`).
- The current state of `nota-next` (head: `ounvxllxtntv` — "allow colon-qualified nota symbols"), `schema-next` (`pyzrvmuplowo` — "add schema package module entrypoint"), `schema-rust-next` (`qzrnlkwoukmq` — "emit schema module file paths"). All three substrate repos are actively moving.
- The schema-deep pilot in `/35` (commit `rnwxqrlzmrmm` on lojix `schema-deep`, pushed) — ships today; demonstrates the same substrate direction at scale for the lojix component.
- The parallel lean-stack arc in `/34` (the MVP+sandbox audit) and `/29` (lean cluster data shape).
- Spot-checked: production `datom.nota` vs lean `goldragon/horizon-leaner-shape/datom.nota` — the v3/v4 divergence the report names is real.

## What the operator got right

**Substantively sound port choices.** Every high-confidence port named is the right shape:

- Nix local builder caps for non-dedicated hosts (`max-jobs = 1`, `cores = 2`) — pure deploy-policy carry-forward.
- Horizon enum → Nix system name normalization (`X86_64Linux` → `x86_64-linux`) — clean projection rule.
- `includeHome` / `includeAllFirmware` consumption in lean modules — preserves the contract surface area.
- Router Wi-Fi secret policy + the `country`/`ssid` tolerance for transitional names — the operator threaded the needle correctly (tolerance now, naming-discipline question deferred to architecture).
- Desktop audio HSP/HFP role enablement — touches policy not architecture.
- Devshell ghq layout fix, NordVPN server lock/update, WireGuard projection check — all isolated and verifiable.

**Constraint-discipline.** Spirit 906 said "remote builders with `max-jobs 0`, not local laptop fanout." Every full-OS build invocation in the sweep used `--option max-jobs 0` against Prometheus. Discipline followed.

**Lane-discipline.** "Schema-deep work is a sibling future track; I did not edit it" — correct boundary observation. The operator did not cross into `/35` territory while it was in flight.

**Empirical evidence over inference.** The full-OS build sweep is the right kind of test for "port immediately where the correct change is clear, then test those builds" (Spirit 908). Three nodes passed; two failed for named non-regression reasons. That's an actual cutover-readiness signal, not a paper exercise.

**Failure-mode taxonomy is correct.** "These are not ordinary module regressions; they are build-topology/source-distribution gaps." Reading the failures correctly separates "port-stops-working" from "shipping-architecture-is-incomplete." That distinction is what makes the recommended-next sequence actionable instead of panicked.

**Architectural consequences cleanly named.** Three high-leverage issues identified:

1. `repository-ledger` flake input is `git+ssh://gitolite@localhost/...` — not compatible with distributed builds.
2. `aarch64-linux` (balboa) cannot be built by an x86-only remote builder.
3. Lean `horizon-rs` cannot parse the current production NOTA bracket-string form.

All three are real; all three deserve named follow-up. The operator surfaced viable remedies for #1 (publish/mirror; teach Lojix/Arca to stage content-addressed source; cluster-resolved Gitolite host with deploy key) and named the architectural tension without forcing a premature decision.

## Discipline observations

Three observations that improve the next iteration; none reduce the audit's positive substantive reading.

### 1. Compound commit could split into per-port commits

`ptzmopzwpvky` ("criomos: port production fixes to lean stack") bundles ~12 distinct ports into one commit. Per workspace jj discipline (`skills/jj.md`), narrow per-change commits are easier to revert/cherry-pick when a single port turns out wrong. The operator may have judged the compound commit cheaper because all ports were verified by the per-port checks before commit; that's a defensible call. But a future iteration where some ports are higher-risk would benefit from per-port commit granularity — easier to bisect, easier to drop one port without losing the others.

Not a blocker; a discipline note for the operator's next port sweep.

### 2. Bead-shape would help the next-step sequence become claimable

The "Recommended Next Sequence" is a 7-step ordered list. Each step is named but not bead-shaped: no owner-lane suggestion, no dependency graph, no estimated lift. `/34`'s pickup queue shape (rank-numbered beads with file paths + dependencies + lane) makes it dispatch-ready; this list reads more like a designer-style outline.

For an operator-authored report, this is reasonable — operators tend to surface findings and let claims emerge through the work loop. But the list spans clusters of work — substrate fixes (#3, #4), build-topology fixes (#1, #2), reconciliation continuation (#5, #6, #7) — that could be claimed independently by different lanes. Bead-shape would surface that. Optional improvement.

### 3. The cross-arc future-merge concern with `/35` is not surfaced

The operator correctly avoided touching the schema-deep work (lane discipline ✓). But the operator-ported changes land in `CriomOS/horizon-leaner-shape`, which is the integration target of `/34`'s near-term cutover arc. The schema-deep pilot `/35` runs in parallel; if/when operator amalgamates `/35` per `skills/double-implementation-strategy.md`, the changes the operator ported in `162` must be **carried forward into the amalgamation**.

The report does not flag this. It's not a defect — the operator may legitimately consider it amalgamation-step concern not their concern today — but a single forward-looking sentence ("ports below need to migrate into any future schema-deep amalgamation") would close the loop for the future-amalgamator.

## Substantive observations

### The horizon-rs / `datom.nota` shape drift is the highest-leverage blocker

The operator names this as recommended-next step #3 ("Port production NOTA/bracket-string parser support into `horizon-rs/horizon-leaner-shape`") + step #4 ("Migrate `goldragon/horizon-leaner-shape/datom.nota` to the current production-style variant/vector cluster shape"). The framing is correct but understates the leverage.

Spot-check confirms: production `datom.nota` uses **positional records without `Entry` map wrappers, bracket strings, Pascal booleans, current nota-codec shape** (per its own header comment). Lean `goldragon/horizon-leaner-shape/datom.nota` is at the **v3 shape** (`(Entry key value)` map entries, quoted strings, pre-2026-04-27 migration). The lean stack is at least one full nota-codec migration step behind. Until step #3+#4 land, no full-OS build can complete — the operator already proved that empirically.

Three suggestions on this blocker (substrate-direction reading below extends to a fourth):

- **Per-step revert.** Production has a documented history of nota-codec migration steps (the v2→v3 migration comment in the lean datom.nota is the witness). The right move is to walk that same migration forward to v4 in the lean stack, one step at a time, preserving the data shape carefully. Mechanical operator work.
- **Production datom.nota is the cleaner target.** Producing the lean `datom.nota` by **regenerating from a schema rather than hand-migrating** would dodge the migration-step problem entirely. (This is where the substrate-direction reading bites — see next section.)
- **Lean horizon-rs nota-codec pin.** The lean stack pinned a specific nota-codec rev at the time of the v3 migration. The pin can be bumped to the current main; this is a flake.lock update. The bumping may surface other API breakages that need follow-on porting work, but it's the substrate-aligned move regardless of the rest.

### The `repository-ledger` localhost issue should be solved at the substrate layer

The operator's three remedies (publish/mirror; teach Lojix/Arca content-addressed staging; deploy-key with cluster-resolved host) are all viable. The operator's call — "the third option is the fastest tactical fix, but the second is the cleaner long-term match for the Arca/Lojix direction" — is correct in priority.

Designer-class observation: the "teach Lojix/Arca to stage source inputs as content-addressed artifacts" path is exactly the kind of capability that should live in the **runtime triad's executor layer** (per `skills/component-triad.md` §"Runtime triad"). In the schema-deep pilot (`/35`), the `Builder` actor owns build execution; a `SourceStager` actor — schema-defined message protocol, methods on schema-emitted nouns — would slot in as a peer of `Builder` and resolve the gitolite-on-localhost trap by abstracting the input source. That's a longer-arc concern but worth naming so it doesn't get re-invented when the schema-deep pilot promotes.

### Aarch64 strategy — three valid paths, none picked

The operator names the constraint correctly: x86-only Prometheus can't build aarch64 derivations. Three paths exist:

- Add `binfmt`/emulation on Prometheus + advertise aarch64 as a supported system on the builder.
- Add a real aarch64 builder somewhere (cluster member or external).
- Defer balboa-in-cluster builds until one of the above lands; build balboa on its own host.

None is chosen. Reasonable for a reconciliation report — this is an architecture decision proper, not a tactical port. But it deserves a Spirit clarification capture from the psyche so the cluster-operator lane knows which path to invest in. The operator could surface this as a question.

### Router Wi-Fi fallback as "transitional debt" — needs owner

The operator names it as debt and proposes the correct end-state (Horizon derives SSID from cluster identity; router country from explicit Horizon config or standard reduction; CriomOS consumes projected value). Three sentences of "what right looks like" are clear; what's missing is an owner — designer-class to refine the projection rules, operator-class to apply them. The reconciliation report doesn't pin this; it should. Or this audit's recommendation should: name the owner.

**Audit recommendation: this is a designer-class projection-rule question.** The router Wi-Fi projection should be specified in a designer follow-on report (or as part of the `/29` lean cluster data shape work); operator implements when the spec lands. I'll suggest this as a designer pickup-queue item in `Concrete suggestions` below.

## The substrate-direction reading

This is the unique designer contribution to this audit. The operator's recommended-next sequence is incrementally correct — each step makes the lean stack work better. But three of the seven steps (#3 nota parser port, #4 datom.nota migration, #5 re-run lean Horizon projection) can be read at two levels:

- **Local-fix reading** (what the operator named): port the production nota-codec changes into the lean stack's old-nota dependency; migrate the lean datom.nota content forward step-by-step; re-run projection.
- **Substrate-direction reading**: **the lean stack's nota dependency is on the legacy `nota` library. The new `nota-next` + `schema-next` substrate is actively moving** (the heads listed in the working model). When the operator hits "lean horizon-rs cannot parse the current production NOTA bracket-string form," the failure is the legacy substrate's parser refusing the new shape. The **substrate-direction fix** is to migrate the lean stack onto `nota-next`/`schema-next` rather than keep walking the legacy parser forward.

The schema-deep pilot in `/35` is the worked precedent. It demonstrated this turn that the schema-derived stack works at the lojix-component scale: 28 schema-emitted typed nouns in one authored `schema/lojix.schema`, lowered through schema-next, emitted by schema-rust-next, methods attached by hand-written Rust. The same shape applies to cluster data: `goldragon/cluster.schema` declares the cluster proposal types; schema-next lowers it; schema-rust-next emits the Rust types `horizon-rs` consumes; `goldragon/datom.nota` becomes data that conforms to the schema and is consumed by the schema-emitted parser, not by a hand-rolled nota parser.

What that implies for the operator's recommended sequence #3–#5:

- **#3 (port nota parser support to lean horizon-rs)** could be **superseded** by migrating lean horizon-rs onto `nota-next`. The lift is comparable: in both cases, the lean horizon-rs's parsing layer changes. In the substrate-direction case, the lean horizon-rs gains the active-future substrate (which the production stack will also migrate to over time per psyche records 805–820 schema-derived stack direction). In the local-fix case, the lean horizon-rs gets one nota-codec migration step closer to production but stays on the legacy substrate that the workspace is moving away from.
- **#4 (migrate lean datom.nota to current production shape)** could be **transformed** into declaring `goldragon/cluster.schema` and regenerating `datom.nota` as conforming data. This is a bigger lift (designer-class work to author the schema), but it eliminates the migration-step problem permanently — the next nota-codec evolution doesn't break consumers because consumers use the schema-emitted parser.
- **#5 (re-run lean Horizon projection)** stays the same; it just runs against the new parser/schema substrate.

This is not a recommendation to redo the operator's work. The operator's ports stand. The recommendation is: **the recommended-next sequence's substrate-touching steps should be evaluated against the substrate-direction option before being executed**. The operator's step #3 is the local-fix path; the substrate-direction path may be a better investment given that the schema-deep pilot just proved out and the lean horizon-rs's old-nota dependency will eventually need to migrate anyway.

### Why this matters specifically right now

Three factors converge to make the substrate-direction read load-bearing today:

1. **The schema-deep pilot just shipped.** `/35` proves the schema-derived stack works at real-runtime scale. The substrate is no longer hypothetical.
2. **The substrate repos are actively moving.** `nota-next` just gained colon-qualified symbol support (head `ounvxllxtntv`); `schema-next` added a package module entrypoint (`pyzrvmuplowo`); `schema-rust-next` is emitting file paths (`qzrnlkwoukmq`). The substrate is taking on shape faster than the legacy nota is being migrated forward.
3. **The lean stack's nota debt is recurring.** This is at least the second nota-codec migration cycle hitting the lean stack (the v2→v3 noted in the lean datom.nota header, now v3→v4). Continuing the legacy migration walk has a sunk-cost shape — every new nota-codec migration imposes the same cost on the lean stack until it migrates off the legacy.

The psyche has named the schema-derived stack direction repeatedly (records 805–820, 880s for /35). The reconciliation work is exactly the right moment to ask: continue paying legacy-substrate debt, or invest the migration into the future substrate?

## Cross-arc integration with the schema-deep pilot (`/35`)

The two arcs share an integration concern. Naming it:

- `/34` (existing-lean-stack MVP+sandbox) + `/162` (operator's port-into-lean reconciliation) feed the same lean stack at `horizon-leaner-shape`. Both are operator-class ship-soon work. The B-0 lock break in `/34` and the nota parser issue in `/162` are both real blockers on the same target.
- `/35` (schema-deep pilot) is parallel longer-arc work on the schema-derived substrate. It does not block `/34`/`/162`; it does not depend on them; it does not interfere.

The **convergence question**: when the schema-deep pilot promotes (psyche authorization pending per `/35/3` §"Five open psyche questions" #5), the amalgamation step per `skills/double-implementation-strategy.md` must carry forward the changes from `/34` + `/162` into the schema-deep target. The operator's port-into-lean work increases the "what needs to be carried forward" surface area.

This is not an objection — the operator's work was directed by psyche records 905+908 and shipped per Spirit 906 constraint. It IS work that should be done. The audit's job is to make the cross-arc concern explicit so future amalgamation has the picture.

Concrete carry-forward items the schema-deep amalgamation must absorb (extracted from `/162` §"Ported In This Pass"):

- Nix local builder caps for non-dedicated hosts.
- Horizon enum → Nix system name normalization.
- `includeHome` / `includeAllFirmware` deployment shape.
- ThinkPad thermal `ignoreCpuidCheck` policy.
- Legacy Chroma NixOS module removal.
- Router Wi-Fi secret policy + transitional name tolerance.
- Desktop audio HSP/HFP roles + ALSA loopback demotion.
- Devshell ghq layout fix.
- NordVPN server lock/update files.
- WireGuard projection tolerance.
- New/ported checks wired into lean flake.

These are NixOS module-level changes; most map cleanly into the schema-deep pilot's CriomOS consumer layer. The schema-deep pilot itself doesn't touch CriomOS — it lives in lojix — so amalgamation here means **operator integrates lojix-schema-deep into the lojix that CriomOS uses, while keeping the CriomOS-side ports landed in `/162`**. The lojix-side and CriomOS-side are loosely coupled at the deploy interface; the carry-forward is straightforward.

## Concrete suggestions for the operator's next iteration

In priority order:

1. **Surface the substrate-direction question to the psyche.** Before walking the recommended-next sequence step #3, ask: continue the nota-codec migration walk, or migrate lean horizon-rs onto `nota-next` + `schema-next`? This is a designer-class question with operator-class consequences; psyche should decide. (Or, if the psyche prefers operator-authority on substrate decisions for the lean stack, name that.)
2. **Capture the aarch64 strategy as a Spirit Clarification request.** The three paths named in the report need a psyche decision before cluster-operator can claim balboa-build work.
3. **Designer-class follow-on for router Wi-Fi projection.** Name an owner for the "what right looks like" prose — likely a designer-class report extending `/29`'s cluster data shape with the projection rules.
4. **Carry-forward annotation in `/162`.** Append a short section noting that the ports listed are inputs to any future schema-deep amalgamation, with a pointer to `/35/3` §"What would land in lojix proper" for the schema-deep side's amalgamation list.
5. **For the next compound port sweep, split commits per-port.** Optional discipline improvement; not a defect today.

For the workspace (orchestrator pickup):

6. **Decide whether substrate-direction migration belongs in `/34`'s pickup queue.** The `/34` audit's `B-0` lock break is a near-term unblocker; if the substrate-direction path is taken, the lock-break's fix shape may change (because lean horizon-rs's wire types would come from `nota-next`/`schema-next` instead of legacy `nota-codec` + hand-authored `signal-lojix`). This is a designer call to make explicit.

7. **Operator should run a re-test sweep after the substrate-question is settled.** Whatever path is taken (#1 above), there's a second build sweep needed to confirm the lean stack reaches green for the three remaining nodes (ouranos, balboa, the lean horizon-rs path). Bead-shape this in the next reconciliation report.

## See also

- `/system-operator/162-production-to-lean-criomos-reconciliation-2026-05-27.md` — the report this audits.
- `/system-designer/34-mvp-and-sandbox-audit/5-overview.md` — parallel lean MVP arc; B-0 lock break + 4 structural prerequisites + sandbox witness gap.
- `/system-designer/35-schema-deep-new-logics/3-overview.md` — schema-deep pilot synthesis; promotion criteria all met, awaiting psyche authorization.
- `/system-designer/29-lean-horizon-cluster-data-shape.md` — natural home for the cluster-data schema-direction question.
- Spirit records 905 + 906 + 908 — the directives the operator was responding to.
- Spirit record 913 — the directive this audit responds to.
- `protocols/active-repositories.md` — schema-next stack repo map.
- `INTENT.md` §"The schema-driven stack" — workspace-level substrate-direction statement.
- `skills/double-implementation-strategy.md` — designer-pilot-vs-operator-port-and-amalgamate framing.
- `skills/component-triad.md` §"Runtime triad" — Signal/Executor/SEMA frame the SourceStager-as-actor sketch lives in.
