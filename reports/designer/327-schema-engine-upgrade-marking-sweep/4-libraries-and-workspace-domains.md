*Kind: Triage · Topic: schema-engine-upgrade-marking-sweep · Slice: D · Date: 2026-05-24*

# 327 · Slice D — substrate libraries + workspace-domain components

Subagent D triage report for the schema-engine upgrade marking sweep
per `0-frame-and-method.md`. Two marking formats applied: substrate
libraries use frame §3.2 (macro-pattern integration); workspace-domain
components use frame §3.1 (component triad upgrade).

## §1 Scope as dispatched

**Substrate libraries (§3.2 marking):**

- `signal-frame` (wire kernel; sibling `signal-frame-macros` subcrate covered inline)
- `signal-sema` (universal vocabulary)
- `sema-engine` (typed database engine)
- `sema` (storage kernel)
- `semac` (sema compiler — stale per CLAUDE.md)
- `nota` (NOTA notation library; also has INTENT.md)
- `nota-codec` (codec implementation)
- `nota-derive` (derives)
- `nota-config` (config helpers)
- `version-projection` (projection trait + types)
- `signal-executor` (generic command executor)
- `signal-derive` (orphan candidate per /317-2)

**Workspace-domain components (§3.1 marking):**

- `forge` + `signal-forge`
- `cloud` + `signal-cloud`
- `domain-criome` + `signal-domain-criome`
- `lojix` + `signal-lojix` + `lojix-cli`
- `horizon-rs`
- `signal-criome`
- `signal-repository-ledger`

## §2 Inventory check before edits

Pre-sweep ARCHITECTURE.md presence + line count:

| Repo | Pre-sweep state | INTENT.md? |
|---|---|---|
| signal-frame | 599 lines | no |
| signal-sema | 404 lines | no |
| sema-engine | 228 lines | no |
| sema | 217 lines | no |
| semac | MISSING — created minimal | no |
| nota | 110 lines | YES (77 lines) |
| nota-codec | 177 lines | no |
| nota-derive | 98 lines | no |
| nota-config | 147 lines | no |
| version-projection | 182 lines | no |
| signal-executor | 247 lines | no |
| signal-derive | 58 lines | no |
| forge | 132 lines | no |
| signal-forge | 277 lines | no |
| cloud | 60 lines | no |
| signal-cloud | 71 lines | no |
| domain-criome | 90 lines | no |
| signal-domain-criome | 39 lines | no |
| lojix | 379 lines | no |
| signal-lojix | 270 lines | no |
| lojix-cli | 84 lines | no |
| horizon-rs | 116 lines | no |
| signal-criome | 425 lines | no |
| signal-repository-ledger | 145 lines | no |

VCS check: all repos jj-tracked EXCEPT `signal-derive`, which is a
plain git repo. Sweep used the appropriate tool per repo (`jj
commit -m '…'` for jj repos; `git add … && git commit -m '…'` for
signal-derive).

## §3 Edits applied

### §3.1 Substrate libraries (§3.2 marking format)

All twelve substrate libraries received a `## Macro-pattern integration`
section. Per-library integration target was tailored per the dispatch
brief.

| Repo | Section placement | Integration target |
|---|---|---|
| signal-frame | After existing "See Also" — replaced ending; ALSO added `### Sibling subcrate signal-frame-macros` subsection inside the new section to cover the proc-macro subcrate per dispatch | "wire kernel emitted Frame + ShortHeader + Caller; macro emits signal_channel! invocations against this crate's types" |
| signal-sema | After examples/canonical.nota code block | "universal SemaOperation/SemaOutcome vocabulary; cross-schema imports pull these types into per-component schemas" |
| sema-engine | After Non-Goals section | "typed database engine; macro emits redb table descriptors from storage type declarations in component schemas" |
| sema | After "future work" prose | "storage kernel; consumed by sema-engine" — plus a note that the reducer-based migration model in the existing future-work section becomes more natural under the schema-engine upgrade |
| semac | ENTIRE ARCH file CREATED — minimal description + role + pipeline + stale-status note + cross-cutting context + the new marking section | "sema-binary backend of the aski/sema pipeline; potential future provider of .schema ↔ sema-binary relation; today's MVP uses Rust proc-macro reading .schema files instead" |
| nota | After Status section | "NOTA notation suite; .schema file format is itself NOTA" |
| nota | INTENT.md — after existing footer | Same role-focused integration note tailored for the intent layer |
| nota-codec | After existing test/exercise summary | "NOTA notation suite; nota-codec gains the .schema reader for schema files per /326-v13" |
| nota-derive | After Status section | "NOTA notation suite; macro-emitted types continue to derive NotaRecord / NotaEnum via this crate" |
| nota-config | After Status section | "NOTA notation suite; orthogonal to schema-engine — sits at binary's argv boundary, not inside wire protocol" |
| version-projection | BEFORE existing "See also" section | "VersionProjection trait the macro emits impls of, derived from schema-diff per /326-v12 §5" |
| signal-executor | BEFORE existing "See Also" section | "generic command executor; component daemons compose with macro-emitted Command/Effect/dispatcher" |
| signal-derive | After Status section | "Schema derive — orphan per /317-2; may retire when macro pattern fully lands" — explicit orphan-candidate marking |

**signal-frame-macros handling:** the dispatch listed
`signal-frame-macros` as a separate library, but in the actual repo
layout it lives as a sibling proc-macro subcrate inside the
`signal-frame` repo at `signal-frame/macros/`. There is no
separate repo. Marking was placed as a `### Sibling subcrate
signal-frame-macros` subsection inside `signal-frame`'s
`## Macro-pattern integration` section, with the dispatch-specified
integration target text: gains the schema reader + AssembledSchema
lowering per /326-v13 + primary-ezqx.1.

### §3.2 Workspace-domain components (§3.1 marking format)

All twelve workspace-domain repos received a `## Pending schema-engine
upgrade` section. Per-component sequencing and concerns reflect the
dispatch-specified notes.

| Repo | Section placement | Sequencing note |
|---|---|---|
| forge | After Status section | Per /316 forge family direction; schema cutover follows persona triad. Skeleton state means the schema-engine-shaped form IS the natural first implementation — no `signal_channel!` body to migrate |
| signal-forge | BEFORE existing "See also" section | Per /316 forge family direction; bundles with first-real-implementation |
| cloud | After Hard Constraints | Per primary-kbmi.1; schema cutover coordinates with cloud daemon implementation. Owner-vs-ordinary split appears in shared schema |
| signal-cloud | After Constraints | Per primary-kbmi.1; coordinates with cloud daemon implementation |
| domain-criome | After Hard Constraints | Per primary-kbmi.2; schema cutover after cloud — domain-criome's projection-to-cloud path means cloud's schema needs to land first |
| signal-domain-criome | After Constraints | Per primary-kbmi.2; after cloud |
| lojix | After section 7 (cross-cutting context) | Per primary-9up1 migration to current foundation; coordinates with that migration. ARCH still references deprecated signal-core (mid-migration); schema cutover lands after that completes. Cluster-operator deploy-window coordination called out |
| signal-lojix | After section 7 (cross-cutting context) | Per primary-9up1 migration |
| lojix-cli | After cross-cutting context | Transitional CLI; schema cutover may coincide with retirement rather than mid-life refactor. CLI is daemon's first client; daemon owns the schema per triad rule |
| horizon-rs | After cross-cutting context | Per spirit 303 + primary-54ti; after horizon migrates to current foundation. Future absorption into forge in-process actors gets a clean handoff form via schema-emitted types |
| signal-criome | BEFORE existing "See also" section | After pilot succeeds and schema-language stream-block syntax stabilises; criome's Path A subscription FSM is the most schema-mechanically-complex feature in scope |
| signal-repository-ledger | After existing canonical-examples code block | Query-heavy contract; the schema-language must encode optional positional fields (`(Some …)` / `None`) without losing typed-variant discipline. Straightforward cutover after pilot. Owner-vs-ordinary split appears in shared schema |

## §4 Creations

One ARCHITECTURE.md created from scratch:

- `/git/github.com/LiGoldragon/semac/ARCHITECTURE.md` — semac's repo
  had only `CLAUDE.md` describing the component plus a deleted
  `v015_archive/` (per latest jj log). The created ARCH file
  captures the role (only tool that produces true sema), the
  pipeline position (downstream of veric / domainc; upstream of
  rsc), the STALE status against v0.20, the disconnect from the
  workspace's current `signal-frame` / `sema-engine` substrate,
  and the §3.2 marking. Total ~60 lines.

The created ARCH explicitly flags that the schema-engine upgrade
does NOT block on semac — semac is on a separate aski/sema
toolchain whose v0.20 implementation hasn't landed yet — and that
the §3.2 marking is forward-looking rather than near-term
sequencing.

## §5 Commits + push

Per-repo commits made with the dispatch-specified message form.
All commits use inline `-m` per `skills/jj.md`. No remotes were
pushed (dispatch instruction: do NOT push).

| Repo | VCS | Commit message |
|---|---|---|
| signal-frame | jj | `signal-frame: mark macro-pattern integration per /326-v13 + /324` |
| signal-sema | jj | `signal-sema: mark macro-pattern integration per /326-v13 + /324` |
| sema-engine | jj | `sema-engine: mark macro-pattern integration per /326-v13 + /324` |
| sema | jj | `sema: mark macro-pattern integration per /326-v13 + /324` |
| semac | jj | `semac: add minimal ARCHITECTURE.md + mark macro-pattern integration per /326-v13 + /324` |
| nota | jj | `nota: mark macro-pattern integration per /326-v13 + /324` (covers both ARCHITECTURE.md and INTENT.md edits) |
| nota-codec | jj | `nota-codec: mark macro-pattern integration per /326-v13 + /324` |
| nota-derive | jj | `nota-derive: mark macro-pattern integration per /326-v13 + /324` |
| nota-config | jj | `nota-config: mark macro-pattern integration per /326-v13 + /324` |
| version-projection | jj | `version-projection: mark macro-pattern integration per /326-v13 + /324` |
| signal-executor | jj | `signal-executor: mark macro-pattern integration per /326-v13 + /324` |
| signal-derive | git | `signal-derive: mark macro-pattern integration per /326-v13 + /324 (orphan candidate)` |
| forge | jj | `forge: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-forge | jj | `signal-forge: mark pending schema-engine upgrade per /326-v13 + /324` |
| cloud | jj | `cloud: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-cloud | jj | `signal-cloud: mark pending schema-engine upgrade per /326-v13 + /324` |
| domain-criome | jj | `domain-criome: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-domain-criome | jj | `signal-domain-criome: mark pending schema-engine upgrade per /326-v13 + /324` |
| lojix | jj | `lojix: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-lojix | jj | `signal-lojix: mark pending schema-engine upgrade per /326-v13 + /324` |
| lojix-cli | jj | `lojix-cli: mark pending schema-engine upgrade per /326-v13 + /324` |
| horizon-rs | jj | `horizon-rs: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-criome | jj | `signal-criome: mark pending schema-engine upgrade per /326-v13 + /324` |
| signal-repository-ledger | jj | `signal-repository-ledger: mark pending schema-engine upgrade per /326-v13 + /324` |

24 commits total. No pushes per instruction.

## §6 Cross-cutting observations

**Observation 1 — ARCH coverage is nearly universal in this slice.**
Out of 24 repos in scope, 23 already had ARCHITECTURE.md present.
Only `semac` lacked one, and its absence reflects the component's
stale state (waiting on aski/sema v0.20 toolchain) rather than
neglect.

**Observation 2 — INTENT.md presence is sparse.** Of the 24 repos,
only `nota` has an INTENT.md. The intent-layer discipline (per
workspace AGENTS.md) is currently concentrated in the workspace
prose INTENT.md and component ARCH files; per-repo INTENT.md is
the exception, not the rule, across the substrate libraries and
workspace-domain components.

**Observation 3 — `signal-frame-macros` is internal, not a separate
repo.** The dispatch brief listed it as a candidate separate repo;
in fact it lives as `signal-frame/macros/` proc-macro subcrate.
Marking was placed inline in `signal-frame`'s ARCH as a sibling-
subcrate subsection. Future architecture sweeps should not treat
`signal-frame-macros` as a separate inventory entry.

**Observation 4 — VCS-tool inconsistency.** `signal-derive` is the
only jj-uninitialised repo in this slice. Used git for its commit.
This is itself a small workspace-discipline observation worth
flagging to the orchestrator: every other in-scope repo uses jj.
Likely either a workspace-onboarding gap or a deliberate exception
because signal-derive is orphan and may retire soon — checking
either way isn't part of this sweep.

**Observation 5 — signal-criome's Path A subscription FSM is the
trickiest schema-language target in scope.** The contract owns the
canonical subscribe/event/retract/ack lifecycle that several other
contracts (system, harness, terminal personas) imitate. Whatever
the schema-language stream-block syntax decides for Path A becomes
the precedent. Flagged as a per-component sequencing concern in
the marking; orchestrator may want to call out that schema-
language stream-block grammar must support full Path A round-trip
before signal-criome can cut over.

**Observation 6 — owner-signal-\* contracts coexist with their
ordinary signal-\* siblings but the schema-language assumes the
two legs share ONE `.schema` file.** Per the dispatch + `/326-v13`,
each component owns a single `.schema` file holding both
ordinary-operations and owner-only-operations declarations.
Several in-scope contracts (cloud, domain-criome, repository-
ledger) have paired owner-signal contracts; the per-component
markings call this out so the policy-vs-working separation
discipline survives the cutover. The owner-signal-\* repos
themselves were NOT in slice D's scope — orchestrator may want to
confirm those are covered elsewhere or schedule a follow-up sweep
for them. (Spotted in `/git/github.com/LiGoldragon/`:
`owner-signal-cloud`, `owner-signal-domain-criome`,
`owner-signal-repository-ledger`, `owner-signal-sema-upgrade` —
none appeared in any slice's brief based on the frame's §6
inventory.)

**Observation 7 — `signal-criome` carries the criome daemon
contract but the criome daemon repo itself is not in this slice.**
The dispatch put `signal-criome` in slice D as a contract; the
daemon repo (`criome` or equivalent) does not appear in any of
the four slices' briefs as documented in §6. If the criome daemon
exists as a separate repo, it likely needs its own marking
(triad §3.1) — flagging for orchestrator synthesis.

**Observation 8 — Several substrate libraries' marking sections
are very similar in shape.** The §3.2 template is reusable, and
the per-library integration target lines were carefully tailored
per the dispatch's per-library notes. If the macro pattern
stabilises and additional substrate libraries onboard, the
template can be copy-paste-able with the integration-target line
swapped in.

## §7 Deferrals + blockers

No deferrals. No hard blockers.

Soft items that flowed into Observations rather than blockers:

- `signal-frame-macros` was inventory-bookkeeping (not a separate
  repo) — handled inline.
- `semac` ARCH had to be created — handled per dispatch instruction
  "If a repo doesn't have ARCHITECTURE.md, CREATE a minimal one".
- `signal-derive` VCS mismatch — handled via git instead of jj per
  the actual repo state.
- owner-signal-\* contracts visible in the workspace but not in
  any slice's brief — flagged for orchestrator follow-up but not
  handled.
- `criome` daemon repo (if it exists separately) not in any slice's
  brief — flagged for orchestrator follow-up.

## §8 Cross-references the orchestrator may want to thread

The overview (file 5) integrates across all four slices. From
this slice, items the orchestrator may want to surface in
`5-overview.md`:

- Total marking commits: 24 (12 substrate + 12 workspace-domain)
- One ARCH creation (semac)
- One VCS exception (signal-derive uses git)
- Two follow-up sweep candidates (owner-signal-\* family; criome
  daemon if separate repo)
- One contract flagged as the schema-language stream-block grammar
  precedent (signal-criome)

## Slice D summary

Slice D summary: 24 edits + 1 creation + 0 blockers (substrate
libraries: 12; workspace-domain: 12).

(The 24 edits include the per-repo marking commits. The 1 creation
is `semac/ARCHITECTURE.md`. The 0 blockers reflects that every
in-scope repo had a working ARCH or accepted a minimal one. Two
soft follow-ups — owner-signal-\* family + criome daemon — are
flagged as observations for orchestrator synthesis, not blockers.)

## See also

- `reports/designer/327-schema-engine-upgrade-marking-sweep/0-frame-and-method.md` — dispatch frame
- `reports/designer/326-v13-spirit-complete-schema-vision.md` — schema-language design
- `reports/designer/324-migration-mvp-spirit-handover-re-specification.md` — migration MVP
- `reports/designer/322-spirit-mvp-positional-schema-worked-example.md` — Spirit MVP worked example
- `reports/operator/174-schema-import-header-design-critique-2026-05-24.md` — lowering + AssembledSchema form
