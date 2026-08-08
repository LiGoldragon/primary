# 6 — Adversarial review of the five finder reports

cloud-designer lane, 2026-06-05. Read-only. Lens: DOUBT, especially
completeness claims. Every load-bearing assertion in reports 1-5 was
re-checked against the actual files: `triad-port/schema/{nexus,sema}.schema`,
`triad-port/src/{schema_runtime,lib}.rs`, both wire contracts
(`signal-lojix` + `meta-signal-lojix` `triad-port/schema/lib.schema`), and
the legacy Stack A monolith (`lojix-cli/src/{deploy,build,activate,artifact,
cluster,copy,check,stage,host,request,error,lib}.rs`). Default verdict on an
unsupported claim: "incomplete."

## Verdict table — each finder's completeness

| Finder | Verdict | One-line |
|---|---|---|
| 1 sweep:intent | SOUND, with two over-claims | Intent picture verified; "schemas are FAITHFUL to all of them" is too strong — three correctness breaks below contradict it. Its 5-gap list is a strict subset of reports 2/3. |
| 2 inventory:functionality | SOUND on coverage, INCOMPLETE on the runtime | Best inventory; every cited file:symbol checks out. But it audits the SCHEMA catalog and stops — it misses that the runtime `run_*` arms are broken (wrong addressing, wrong eval attribute, literal `$CLOSURE`). Calls effects "partial" that are actually non-functional. |
| 3 audit:nexus | SOUND, strongest report | Every gap (A-G + the five §3 items + the §5 stage-machine) verified true against `schema_runtime.rs`. Gap D (materialization) correctly named the headline. Two missed runtime bugs (below) it would have caught had it read `run_nix_eval`/`run_activate_generation` line-by-line. |
| 4 audit:state | SOUND, grep-claims verified | The Rollback-never-constructed grep claim is TRUE (re-confirmed: zero `Rollback`/`Promoted`/`Demoted` constructions). Live-set append-only, in-flight non-durable, fake digest — all verified. One over-reach corrected below (the `recorded_at` claim slightly overstates; `Recent` IS produced, just untimestamped — which the report does say, so it stands). |
| 5 boundary:horizon | SOUND on the boundary, OUT-OF-SCOPE drift | The lojix-consumes-pretty finding (`is_remote_nix_builder`, `nix_url`) verified against `deploy.rs:60,232`. But the report's whole second half audits `horizon-rs`/`horizon-next`/`horizon-core` — files NOT in this session's stated scope, and several of its claims about those files are UNVERIFIED here (it asserts `horizon-core/schema/magnitude.schema` content and `horizon-next/INTENT.md` staleness without this reviewer being able to confirm — see "Unsupported claims"). |

Net: the synthesis is broadly trustworthy. The five reports converge on the
SAME headline (Nexus catalog is a 6-verb skeleton over a ~19-effect legacy
pipeline; the materialization/override-input subsystem is entirely absent;
SEMA is over-built relative to Nexus). But all five UNDER-state the severity:
they treat the rewrite as "incomplete catalog, correct shape." It is worse
than that — the runtime effect arms that DO exist are individually broken in
ways that mean the current daemon cannot deploy ANY real node even within its
6-verb skeleton. Three of those breaks NO finder caught.

## Part A — Functionality the inventory MISSED or mis-rated (the runtime is broken, not just thin)

Report 2 audits the SCHEMA against legacy and rates `NixEval`/`NixBuild`/
`CopyClosure`/`ActivateGeneration` as "covered" or "partial." Reading the
actual `run_*` arms in `schema_runtime.rs` shows three of them are not
"partial" — they are non-functional. These are MISSED items, not severity
re-rankings.

### A1 — The eval attribute is WRONG (`run_nix_eval`, schema_runtime.rs:933-942) — MISSED by all five

`nix_eval_command` (schema_runtime.rs:147-159) sets
`attribute = format!("{}.{}", cluster_name, node_name)`, and `run_nix_eval`
runs `nix eval --refresh --raw <flake>#<cluster>.<node>.drvPath`. Legacy
`build.rs:181-193 target_attr` is
`<flake>#nixosConfigurations.target.config.system.build.toplevel` for system
and `<flake>#homeConfigurations.<user>.activationPackage` for home. So the
rewrite evaluates a flake attribute that does not exist (`criome.prometheus`
instead of `nixosConfigurations.target.config.system.build.toplevel`). Every
deploy fails at the Eval stage. No finder read this arm; report 2 marked
NixEval "covered" (its row 13). This is a hard correctness break inside a
"covered" verb — exactly the kind of thing z6qu visibility is supposed to
prevent (the attribute construction is inline, not a declared feature).

### A2 — `run_activate_generation` activates a LITERAL `$CLOSURE` (schema_runtime.rs:980, 1095-1105) — MISSED by all five

`NixCommand::activate_system` hardcodes the remote command
`nix-env -p /nix/var/nix/profiles/system --set "$CLOSURE"` — the literal
shell token `$CLOSURE`, never substituted from the pipeline's
`closure_path`. The closure path the pipeline tracked
(`pipeline.closure_path`) is NEVER passed to `activate_generation_command`
(schema_runtime.rs:182-189 — the command carries no closure path at all).
So activation always sets the system profile to the empty/unset `$CLOSURE`.
Reports 2/3 noted the ActivationKind branching is collapsed (true), but ALL
five missed that the activate effect does not even carry the closure path it
is supposed to activate. `ActivateGenerationCommand` (nexus.schema:60) has no
`ClosurePath` field — a schema gap that produces the runtime break.

### A3 — copy + activate ssh to the bare `node_name`, not the criome domain (schema_runtime.rs:965, 980, 1083-1105) — MISSED by all five

`run_copy_closure` runs `nix copy --to ssh-ng://<node_name>` and
`run_activate_generation`/`collect_garbage` run `ssh <node_name> …`. Legacy
addressing (`host.rs:19-65 SshTarget`) is ALWAYS
`<user>@<criome_domain_name>` — e.g. `root@prometheus.cluster.criome`,
derived from horizon's `criome_domain_name`, "never from a literal
hostname" (host.rs:8-9). The rewrite has no horizon projection (Gap G2/D),
so it has no `criome_domain_name` to address with and falls back to the bare
node name, which will not resolve. This is the downstream consequence of the
missing projection that reports 2/3 named at the schema level, but NONE
traced it into the copy/activate/gc runtime arms. It means even if A1/A2 were
fixed, copy/activate/gc would still fail to reach the host.

These three (A1-A3) sharpen the synthesis materially: the materialization gap
(Gap D) is NOT the only thing stopping a real build — even the closure-build
attribute, the activation closure, and the host addressing are broken. The
fix list must include "make the existing 6 effect arms actually work,"
not only "add the missing verbs."

### A4 — secrets file names are a hidden hardcode the inventory under-flagged

Report 2's G7 (secrets absent) is correct and high-severity. Verified:
`artifact.rs:18-30, 155-207` hardcodes exactly three sops filenames
(`router-wifi-sae-passwords.sops`, `router-backup-wifi-password.sops`,
`local-llm-api-token.sops`) and the secrets flake template names them. Report
2 calls the hardcode "a smell"; it is more than that for z6qu/a2t4 — these
are cluster-data facts that belong in horizon, so the secrets EFFECT (when
added) must take its file set from the projected horizon, not a const. Worth
stating explicitly so the synthesis does not port the hardcode forward.

### A5 — Stack A operations the inventory's external-op table got RIGHT (no gap, recorded to close the doubt)

I re-checked `request.rs` against report 2's external-op table. The four
`LojixRequest` variants (FullOs/OsOnly/HomeOnly/CheckHostKeyMaterial) are
exactly as listed; no fifth operation hides in `request.rs`, `lib.rs`
(just module decls), or `main.rs`. Report 2's "external parity COMPLETE"
claim is SOUND. The `proposal load` step (its G1) is real
(`cluster.rs:20 ProposalSource::load` NOTA-decodes a `ClusterProposal`) and
genuinely has no Nexus verb — confirmed.

## Part B — Nexus gaps declared "covered" that are actually inline-only or absent

### B1 — `BuildTarget` is "covered" but the build does the SAME thing for Local and Remote (verified)

`run_nix_build` (schema_runtime.rs:944-962) branches Local vs Remote, but the
Remote arm just adds `--builders ssh-ng://<builder>` to a local `nix build`
(NixCommand::build_closure_remote, 1069-1081). Legacy `build.rs:374
execution_invocation` WRAPS THE WHOLE nix invocation in ssh-to-builder
(`target.remote_invocation(...)`) — the build RUNS ON the builder, it is not
a `--builders` delegation. Report 2's G9 flagged the ssh-wrap-vs-`--builders`
difference; confirmed true. The schema's `BuildTarget` variant exists, but the
remote semantics are wrong, and — combined with the absence of remote-input
staging (Gap C/G8) — a remote build cannot resolve the generated override
inputs. So "NixBuild covered/partial" overstates: remote build is
non-functional, not partial.

### B2 — `ReadEventLog` dead-and-wired-to-fail: verified exactly as reports 3/4 claim

`decide_ordinary_input` (schema_runtime.rs:254-267) routes only `Query` and
`CheckHostKeyMaterial`; `Selection::ByEventLog` falls into
`generation_matches` returning `true` for everything (schema_runtime.rs:857)
so a `ByEventLog` query runs `QueryGenerations` and returns ALL generations,
and a genuine `EventLogRead` reply hits `decide_read_completion:329` →
`MalformedSelector`. Both reports 3 (Gap B) and 4 (gap 5) are correct AND
mutually consistent. Not a contradiction — a corroboration.

### B3 — CheckKeyMaterial: reports 2/3/4 AGREE it is a stub on the wrong plane — verified, no contradiction

`check_key_material` (schema_runtime.rs:899-906) returns
`mismatches: Vec::new()` unconditionally. Legacy `check.rs:36-207` is ~200
lines of real ssh-cat-publication.nota + parse + diff producing typed
ssh/ygg/address mismatches. All three reports independently say: it is real
host IO (a Nexus effect), mis-modeled as a SEMA read, AND a no-op stub. This
is the single most-corroborated finding; the synthesis should treat
"move CheckKeyMaterial to an EffectCommand AND build the real diff" as
settled, not a proposal.

### B4 — The deploy STAGE MACHINE: a contradiction-of-emphasis between reports, and a naming bug all missed

Reports 3 (§5, gap 13) and 4 (gap on DeployStage) both say the private
`DeployStage` enum (schema_runtime.rs:56-67) hides the pipeline sequencing
from the schema. True and important. But reading the actual trampoline
(advance_after_phase, 388-421 + decide_effect_completion, 480-526) surfaces a
bug NEITHER report caught: the `DeployStage` variant NAMES are misaligned with
what they trigger.
- `Submitted` → fires `NixEval` (after Building recorded). OK-ish.
- `BuildingRecorded` → fires `ActivateGeneration` (after Copying recorded) —
  it SKIPS straight from "building recorded" to activate; the actual
  Build→Copy effect transitions happen in `decide_effect_completion`
  (ClosureEvaluated→NixBuild→ClosureBuilt→CopyClosure), NOT in
  `advance_after_phase`. So the stage enum tracks only 3 of the ~5 real
  transitions and its names (`BuildingRecorded` firing activate,
  `CopyingRecorded` firing the activation-record WRITE) describe the
  PRIOR phase, not the next action.
- Consequence: the chain happens to work for the happy path, but the
  stage-name/action mismatch is fragile and actively misleading — which is the
  STRONGEST argument for reports 3/4's "lift the stage machine into the
  schema" recommendation. The synthesis should cite this concrete
  name-vs-action mismatch as the evidence, not just "it's a private enum."

### B5 — `RecordPhaseTransition` records Building/Copying/Activated but NEVER Submitted/Built/Activating/Failed

The wire `DeploymentPhase` enum (signal-lojix lib.schema:90) has 7 phases
(Submitted Building Built Copying Activating Activated Failed). The runtime
only ever records 3: Building (498), Copying (515), Activated (521). Submitted,
Built, Activating, and Failed are never emitted into the event log. A
`WatchDeployments` subscriber (once push lands) would see a sparse, non-
conformant phase stream. NO finder enumerated which phases are actually
produced; report 2 listed the enum as "covered." This is a z6qu visibility
gap (the phase-emission policy is inline and incomplete) AND a parity gap
against the wire contract's own declared phases.

## Part C — Runtime state the model claims is sufficient but isn't

### C1 — Report 4's headline gaps all VERIFIED

Re-confirmed by direct read + grep:
- Live-set append-only never demotes: `record_generation_activated:657`
  always `push`es; no key lookup. TRUE.
- Rollback ring absent: grep for `GenerationSlot::Rollback` / `Promoted` /
  `Demoted` constructions = ZERO across `schema_runtime.rs`. TRUE. Only
  `Current`/`BootPending`/`Recent`/`Pinned` are ever written. The ring,
  promotion, and demotion are entirely unimplemented.
- In-flight deploy non-durable: `record_deploy_submitted:590-616` writes NO
  table; the pipeline lives in `active_deploy: Option<DeployPipeline>`
  (lib.rs not involved; it is a field on `SchemaRuntime`, schema_runtime.rs:27).
  Restart loses it. TRUE.
- Fake digest: `marker`/`sema_marker` set `state_digest = commit_sequence`
  (schema_runtime.rs:231-243; lib.rs:133 comment confirms). No write takes an
  expected marker. TRUE — it is write-wins, not optimistic concurrency.

### C2 — Report 4's `recorded_at` claim is correct but the SLOT itself is the deeper problem

Report 4 says `GenerationSlot::Recent` has no timestamp so the narinfo-TTL
grace is uncomputable. Verified: `GenerationSlot` (signal-lojix lib.schema:57)
is a bare enum `[Current BootPending Rollback Pinned Recent]` with no payload;
ARCHITECTURE names `rollback/<n>` and `recent/<timestamp>` as PARAMETRIZED
slots. So not only `Recent` but `Rollback` needs an ordinal payload. The slot
enum cannot express the slot tree ARCHITECTURE describes. Report 4 proposes a
`recorded_at` column on the row (workable), but the synthesis should note the
deeper choice: parametrize the slot enum (`Recent Timestamp`,
`Rollback Ordinal`) vs carry the parameters as sibling columns. The wire
contract's flat enum forces the sibling-column route unless the wire enum
changes too.

### C3 — Approval/plan state: the `PlanNotApproved` reason is dead, and there is no plan state at all

`RejectionReason` (sema.schema:66) and the runtime both carry
`PlanNotApproved`, but it is only ever produced on a poisoned-lock error
(`record_deploy_submitted:614`, `record_phase_transition:635`) — a
mis-use; lock poisoning is not "plan not approved." There is NO approval/plan
table, NO plan object, and the meta contract has no approve/plan verb. If
deploys are ever to be plan-gated (the reason name implies it), that entire
state is absent. The task brief asked specifically about "approval/plan
state" — finding: it does not exist, and the one enum variant that names it is
mis-wired to a lock error. NO finder flagged this. Carry as an open question
to the psyche: is plan-approval in scope for lojix, or is `PlanNotApproved`
vestigial and should be dropped?

### C4 — Pin-label uniqueness: report 4 says "adequate" — VERIFIED, but it is O(roots) AND has no event

`pin_generation:689-696` scans all gc_roots for a label collision →
`PinLabelInUse`. Correct behavior, O(n). Report 4 rates this "adequate for
parity"; agreed. But note `meta-signal-lojix` has a `PinSlotExhausted`
rejection reason (lib.schema:111) that is NEVER produced — there is no
pin-slot CAP enforced. If pins are meant to be bounded, that limit is
unimplemented (another declared-reason-without-feature, the inverse-z6qu
pattern reports 3/4 named).

## Part D — Claims asserted WITHOUT reading the file (unsupported / unverifiable here)

### D1 — Report 5's horizon-rs / horizon-next / horizon-core claims are OUT-OF-SCOPE and partly unverified

Report 5 is the only finder that ranges outside this session's stated key
paths. Its boundary spec for raw/pretty is reasonable, and its lojix-consumes-
pretty finding is VERIFIED (`deploy.rs:60` reads `is_remote_nix_builder`;
`deploy.rs:232-243` `CacheEndpoint` reads `nix_url`/`ygg_address`). But these
claims it makes are NOT verifiable from the files this review can stand
behind, and the report states them as fact:
- "`horizon-core/schema/magnitude.schema` is the two-position `{} { Magnitude
  (...) }` types-only document" with a specific 6-point ladder
  `Zero Min Low Medium High Max`.
- "`horizon-rs` authoritative Magnitude is 5-point `Zero Min Medium Large
  Max`."
- "horizon-next's `horizon` crate declares Input/Output and emits a full
  triad."
- "horizon-next/INTENT.md is stale."

These may well be true, but report 5 presents schema/INTENT content it read in
repos outside the lojix triad-port scope, and a synthesis that forwards them
should mark them as report-5-sourced-and-unverified-by-others, not settled.
The Magnitude-ladder-divergence claim in particular is load-bearing for any
horizon parity work and should be independently re-confirmed before action.
Recommendation: the synthesis treats report 5's §1-2 (the raw/pretty boundary
+ lojix dual consumption) as SOUND and verified, and §3-5 (horizon-rs/next/
core promotion mechanics + ladder divergence) as a SEPARATE horizon-scoped
follow-up that needs its own verification pass — not folded into the lojix
engine-completeness conclusions.

### D2 — Report 1's "the current triad-port schemas are FAITHFUL to all of them" — OVER-CLAIM

Report 1 (bottom line) says the schemas are faithful to the charter, the
Nexus-catalog principle, SEMA expectations, raw/pretty, and minimalism. The
charter/principle alignment is fine, but "faithful to the Nexus-catalog
principle (z6qu)" is precisely what reports 2/3/4 (and this review) DISPROVE:
the catalog is a 6-verb skeleton missing ~13 effects, the SEMA layer is
over-built with no producers, the stage machine is a private enum, and three
of the six declared verbs are non-functional at runtime. Report 1's own
5-gap section then contradicts its "faithful" framing. The synthesis should
take report 1's intent agglomeration (solid) but DROP its faithfulness verdict
in favor of reports 2/3/4's gap-laden one.

## Part E — Contradictions and convergences BETWEEN the five reports

### E1 — No substantive contradiction on the gaps; strong convergence

Reports 2, 3, 4 independently reach the same five-or-so headline gaps
(materialization/override-inputs absent; CheckKeyMaterial stub-on-wrong-plane;
home activation collapsed; cache-retention events never emitted; GC verb
inert). Where they overlap, they AGREE. The cross-report consistency is itself
evidence the gaps are real, not one finder's misreading.

### E2 — A framing tension (not a contradiction): "shape correct" vs "shape broken"

Report 1 says shape is faithful; report 3 says shape is correctly DECLARED but
the stage machine and several features are not schema-visible; this review adds
that the runtime arms are individually broken. These are not contradictions —
they are three altitudes. Resolution for the synthesis: the SCHEMA SHAPE of
the declared subset is sound (the SignalArrived→Command*→Continue protocol,
the EffectCommand/EffectResult 1:1 pairing); the CATALOG COMPLETENESS is poor
(z6qu fail); the RUNTIME of even the declared subset is broken (A1-A3). State
all three explicitly rather than picking one.

### E3 — Report 2 vs report 3 on counting effects (19 vs "more than six"): reconciled

Report 2 counts 19 Stack A internal effects; report 3 says "~10-step
pipeline." Not a contradiction — report 2 counts every distinct sub-step
(4 materialize dirs + nar-hash + flake-ref as separate rows), report 3 groups
materialization as one stage. Both land on "the catalog of 6 is ~3x too
small." The synthesis can use report 2's granular count and report 3's grouped
stages without conflict.

## Must-fix corrections the synthesis should incorporate

1. **Add the three runtime breaks (A1-A3) as first-class findings.** The
   synthesis must not conclude "shape correct, catalog thin." Even the
   declared 6 verbs cannot deploy a real node: eval attribute is wrong
   (`<flake>#<cluster>.<node>` not the nixos toplevel attr), activate sets a
   literal `$CLOSURE`, copy/activate/gc address the bare node name not the
   criome domain. `ActivateGenerationCommand` needs a `ClosurePath` field.

2. **Downgrade report 1's "schemas are faithful" verdict.** Keep its intent
   agglomeration; replace the faithfulness claim with reports 2/3/4's
   gap-laden verdict. The schemas are faithful to the CHARTER, not yet to
   z6qu.

3. **Re-rate report 2's "covered"/"partial" effect rows as "non-functional."**
   NixEval, ActivateGeneration, remote NixBuild, CopyClosure, CheckKeyMaterial
   are not partial — they are broken or stubbed. Only the LOCAL build skeleton
   and the local-build-never-rejected discipline are genuinely working.

4. **Add phase-emission completeness (B5):** only 3 of 7 declared
   `DeploymentPhase` values are ever recorded; Submitted/Built/Activating/
   Failed never reach the event log.

5. **Quote the DeployStage name-vs-action mismatch (B4)** as the concrete
   evidence for lifting the stage machine into the schema, rather than the
   abstract "it's a private enum."

6. **Carry C3 (plan/approval state) to the psyche as an open question:**
   `PlanNotApproved` and `PinSlotExhausted` are declared-reasons-without-
   features mis-wired to lock errors / never produced. Decide whether plan
   approval and pin-slot caps are in lojix scope, or drop the vestigial
   reasons.

7. **Fence report 5's horizon-rs/next/core claims as report-5-sourced and
   unverified.** Treat its raw/pretty boundary + lojix-dual-consumption
   (§1-2) as verified and SOUND; treat the promotion mechanics + Magnitude
   ladder divergence (§3-5) as a separate horizon-scoped pass needing its own
   verification before action.

8. **Do not port the hardcoded secrets filenames forward (A4):** the secrets
   EFFECT, when added, must take its file set from projected horizon, per
   z6qu/a2t4 (cluster-data is horizon's, not a const in the daemon).

## Bottom line

The five finders are individually sound on what they each read and converge
strongly on the catalog-completeness story — that convergence is real
evidence, not echo. But collectively they UNDER-state severity: they audited
the schema-vs-legacy gap and largely stopped at the schema boundary. Reading
the runtime `run_*` arms shows the current GREEN daemon cannot deploy any real
node even within its 6-verb skeleton (wrong eval attribute, literal
`$CLOSURE`, bare-node-name addressing) — three correctness breaks no finder
caught. The synthesis verdict should be: SCHEMA SHAPE of the declared subset
is sound; CATALOG COMPLETENESS fails z6qu (≈13 effects + the stage machine +
home activation + retention decisions unmodeled); RUNTIME of even the declared
subset is broken. And report 5's horizon-repo claims belong in a separate
verified pass, not the lojix engine conclusions.
