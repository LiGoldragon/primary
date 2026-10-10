# Audit: the Lojix deployment plane

## 1. What Lojix IS today

Lojix is a Rust Nexus (21,277 lines across 17 modules) shipping a long-lived
deploy-orchestrator daemon (`lojix-daemon`), two authority-tiered CLI clients
(`lojix` on the ordinary socket, `meta-lojix` on the owner socket), a
bootstrap ingress (`lojix-bootstrap`), a startup-configuration writer
(`lojix-write-configuration`), a store inspector (`lojix-inspect-store`), and a
store reset primitive (`lojix-reset-store`). Its wire vocabulary lives in two
separate repositories: `signal-lojix` (1,444 lines) and `meta-signal-lojix`
(1,481 lines). CriomOS packages the daemon as a systemd service with an
ExecStartPre configuration writer, systemPackages, and environment variable
export. CriomOS-home does not carry Lojix at all.

```
                          authored source
                          ──────────────
                  goldragon/datom.dotos
                  criomos-horizon-config/horizon.dotos
                  manifests/*.dotos  (EMPTY -- nothing authored)

                          runtime
                          ───────
 ┌──────────────────────────────────────────────────────────────┐
 │                     lojix-daemon                             │
 │                                                              │
 │  ordinary socket (/run/lojix/ordinary.sock, 0660)            │
 │    Query, WatchDeployments, WatchCacheRetention,             │
 │    Unwatch, CheckHostKeyMaterial                             │
 │                                                              │
 │  owner socket (/run/lojix/owner.sock, 0600)                  │
 │    Deploy, Pin, Unpin, Retire, Test                          │
 │                                                              │
 │  ┌──────────── sema store (.sema, redb v4) ───────────────┐  │
 │  │ 10 tables: live-set, gc-roots, event-log,              │  │
 │  │ container-lifecycle, deploy-job, test-run,              │  │
 │  │ deployment-record, identifier-allocation,               │  │
 │  │ deployment-outbox, pending-transition-intent            │  │
 │  └────────────────────────────────────────────────────────┘  │
 │                                                              │
 │  deploy pipeline:                                            │
 │    ResolveFlakeAuth -> MaterializeHorizon -> NixEval         │
 │    -> NixBuild -> CopyClosure -> ActivateGeneration          │
 │                                                              │
 │  MaterializeHorizon writes content-addressed flakes:          │
 │    state-dir/generated-inputs/{horizon,system,deployment,    │
 │    secrets}/flake.nix                                        │
 │  then nix eval --override-input for each                     │
 └──────────────────────────────────────────────────────────────┘
 │                                                              │
 │  CriomOS stubs (replaced by lojix at eval time):             │
 │    stubs/no-horizon, stubs/no-system,                        │
 │    stubs/default-deployment, stubs/no-secrets                │
 └──────────────────────────────────────────────────────────────┘

 CLI layer (text-to-Signal boundary):
   lojix    'Query.ByNode.(alpha node-1 None)'
   meta-lojix 'Deploy.Host.(...13 positional fields...)'
```

## 2. Findings

### 2.1 Duplicated types between runtime_flow.rs and runtime_model.rs

**Severity: duplicates a source.**

Eleven types are defined twice with identical shapes but different derive sets:
`DeploymentTransport`, `DeploymentInputMode`, `ActivationBackend`,
`ExtraSubstituter`, `TestExecutionProfile`, `NixStoreUri`, `SshDestination`,
`FlakeAttribute`, `DeploymentOutputSelector`, `NixBuilderSpec`, `NixSystem`.

runtime_model.rs types derive `rkyv::{Archive, Serialize, Deserialize}` for
durable persistence. runtime_flow.rs types derive only `Clone, Debug,
PartialEq, Eq` for in-memory pipeline use. The adapters.rs `WireShape` impls
convert between them field by field.

Evidence:
- `runtime_flow.rs:74` / `runtime_model.rs:66` (DeploymentTransport)
- `runtime_flow.rs:79` / `runtime_model.rs:71` (DeploymentInputMode)
- `runtime_flow.rs:86` / `runtime_model.rs:78` (ActivationBackend)
- `runtime_flow.rs:98` / `runtime_model.rs:473` (ExtraSubstituter)
- `runtime_flow.rs:188` / `runtime_model.rs:85` (TestExecutionProfile)
- Six more newtype wrappers: NixStoreUri, SshDestination, FlakeAttribute,
  DeploymentOutputSelector, NixBuilderSpec, NixSystem.

The split has a reason: runtime_flow values carry no rkyv overhead and exist
only during a pipeline run; runtime_model values persist. The adapters layer
converts at the boundary. Whether this justifies the duplication depends on
whether the two representations ever diverge (they have not yet) and whether
the conversion cost is worth the isolation.

**Disconfirming evidence:** The separation insulates the pipeline from
serialization concerns and makes rkyv a private dependency of the model layer.
If a pipeline field changes shape without changing the persisted form, only one
side changes. This survives as a defensible architecture if divergence is
expected. It does not survive as minimal machinery for types that have been
identical since creation and show no pressure to diverge.

### 2.2 Query.ByDeployment returns empty results

**Severity: blocks a stated design.**

`schema_runtime.rs:4187` hard-codes `ByDeployment(_) => false` in the
live-generation filter, meaning a `Query.ByDeployment` always returns an empty
generation vector. The deployment-record filter at line 4213 does match
correctly, but the combined result has no generations -- making the query
functionally broken.

Evidence: `schema_runtime.rs:4187`:
```rust
ordinary::Selection::ByDeployment(_) => false,
```

Psyche statement it departs from: The lojix skill documents `Query.ByDeployment`
as a supported query carrying one deployment identifier. The psyche said "the
interface is lojix and meta-lojix CLI only" and "CLIs cannot accept any other
type of argument than the typed input object" -- the interface contract promises
this query works.

**Disconfirming evidence:** None found. The `false` is not guarded by any
comment explaining intentional omission. This appears to be a bug or an
incomplete implementation.

### 2.3 CheckHostKeyMaterial returns empty material

**Severity: blocks a stated design (stub, not implementation).**

`schema_runtime.rs:4276-4283`:
```rust
fn check_key_material(&self, query: ordinary::KeyMaterialQuery) -> sema::SemaReadOutput {
    let commit_sequence = self.current_commit_sequence();
    sema::SemaReadOutput::KeyMaterialChecked(ordinary::KeyMaterialReport {
        node_name: query.node_name,
        string_vector: Vec::new(),
        state_marker: Self::marker(commit_sequence),
    })
}
```

Always returns `string_vector: Vec::new()`. The interface advertises host key
material checking, but the implementation is a stub returning no data.

**Disconfirming evidence:** This may be intentional deferral -- key material
verification requires reaching the target host, which may not have been
needed for the MVP deployment path. But the operation is exposed on the
ordinary socket and agents are told they can use it. Stub status should be
documented or the operation removed from the contract.

### 2.4 Empty manifests/ -- no deployment selection exists

**Severity: blocks a stated design.**

`/home/li/primary/manifests/` is empty. AGENTS.md (`NON_MANAGEMENT_AGENTS.md:12`)
says "Identity and deployment selection are only `manifests/*.dotos`." The flow
log at `flows/01a048a6/log.md` records: "No authoritative `manifests/*.dotos`
selection supplies the required explicit store/SSH transport, builder, selector,
and input mode for Ouranos and Zeus."

A correct deployment manifest must contain:
1. The cluster name and node name (which node to build for)
2. The proposal source (path to the cluster `.dotos` file)
3. The flake reference (CriomOS flake)
4. The deployment transport (Nix store URI + SSH destination)
5. The deployment input mode (Horizon or Direct)
6. The deployment output selector (flake attribute)
7. The activation backend
8. The host deploy action
9. The source revision policy
10. Optionally: builder, extra substituters

These manifests are authored by the psyche (or at the psyche's direction), not
by agents. No psyche quote was found specifically approving or defining the
manifest shape -- the `manifests/*.dotos` convention appears in AGENTS.md
instructions but lacks a surviving psyche founding ask.

**Disconfirming evidence:** The manifests may be intentionally empty because
the correct shape has not yet been decided by the psyche.

### 2.5 Deploy request fields: psyche-asked or agent-invented?

**Severity: adds unasked machinery (partially).**

The `Deploy.Host` request carries 13 positional fields: cluster_name,
node_name, host_composition, proposal_source, flake_reference,
deployment_transport, deployment_input_mode, deployment_output_selector,
activation_backend, host_deploy_action, source_revision_policy,
optional_nix_builder_spec, extra_substituter_vector.

Evidence for psyche origin:
- **Transport (store URI + SSH destination):** The psyche explicitly chose split
  transports ("prefer the direct ethernet route" for heavy transfers,
  "zeus.goldragon.criome is fine" for activation). Transport must be explicit.
- **Activation backend:** The psyche distinguished OS redeploy from Home Manager
  activation ("use the nix user env only, or OS redeploy").
- **Source revision policy:** The psyche values immutable source pinning ("make
  sure KareemOS and KareemOS Home are in sync").
- **Deploy action:** The psyche referenced evaluate/activate stages.

Evidence against:
- **Input mode (Horizon vs Direct):** No psyche quote survives asking for two
  input modes. The Horizon path is the designed one; Direct appears to be an
  agent-added alternative for bypassing Horizon materialization.
- **Builder specification:** No psyche quote asks for per-request builder
  selection.
- **Extra substituters:** No psyche quote requests this.
- **Output selector:** A flake attribute selector is infrastructure plumbing,
  not a psyche design decision.

The psyche's general stance: "way too complex. start with ultra minimal" (said
of a skill-training text proposal, but reflecting a general pattern the psyche
applies consistently -- see "your skill is too complicated", "youre
overcomplicating this to the extreme").

**Disconfirming evidence:** The fields not traceable to the psyche (builder,
substituters, input mode, output selector) are all things a Nix deploy tool
genuinely needs to be correct. A builder is needed when the deploying host
cannot build for the target. Substituters are needed for binary cache access.
The output selector names the NixOS configuration to build. These are not
comfort features -- they are correctness requirements for a multi-host Nix
deployment tool. The question is whether each request should carry them or
whether the manifest should default them.

### 2.6 Sema store: 10 tables for 8 nodes

**Severity: adds unasked machinery.**

The redb-backed sema store carries 10 durable table families:
1. `live-set` -- the current generation per (cluster, node)
2. `gc-roots` -- Nix GC root tracking
3. `event-log` -- append-only deployment and lifecycle events
4. `container-lifecycle` -- container state mirror
5. `deployment-record` -- per-deployment history
6. `deploy-job` -- in-flight deployment resumption
7. `test-run` -- test execution records
8. `identifier-allocation` -- monotonic ID counters
9. `deployment-outbox` -- phase-transition notification delivery
10. `pending-transition-intent` -- pre-commit transition staging

The store supports: schema versioning (v4, with v2/v3 migration refusal),
commit sequences, state digests, event-log retention compaction, outbox
delivery states (Pending/Dispatched/Acknowledged), transition intent staging
(Pending/Bound/Appended/Acknowledged), deploy-job resumption on daemon restart.

The psyche said: "I dont care about any past lojix database. how do we get a
clean working lojix service running?"

The psyche's vision from psycheStackOrigins.md: "Everything is in the daemon"
-- the daemon owns its durable state. A sema store is the psyche's own
architecture for durable Nexus state (sema-engine is a shared library). The
question is not whether state should be durable but whether this much state is
needed.

For an 8-node cluster: the outbox, transition-intent staging, and event-log
retention compaction are infrastructure for a system under high deployment
throughput. An 8-node cluster does not have that throughput. The deploy-job
resumption table is valuable (daemon restart should not lose an in-flight
deploy), but the outbox and transition-intent machinery adds complexity without
a current consumer.

**Disconfirming evidence:** The daemon is designed for correctness, not for
current scale. The outbox ensures that subscription watchers receive every
phase transition even if the daemon restarts between phases. This is the kind
of correctness the spirit says "more than makes up for the added machinery."
The transition-intent staging is the mechanism for exactly-once phase recording.
Whether these survive depends on whether Lojix has subscription consumers (it
does: `WatchDeployments` and `WatchCacheRetention`). The machinery exists to
serve contracts already on the wire; removing it breaks those contracts.

### 2.7 Signal/meta-signal contract stack

**Severity: cosmetic (aligned with psyche).**

The three-repo shape (lojix + signal-lojix + meta-signal-lojix) matches the
psyche's own architecture: "3 repos per component" and "they will each have a
signal-XXX and meta-signal-XXX repo." The generated signal code uses opaque
type names (`z2VTvQ`, `z2VcR1`, `z2VW7Q`, `z2VeCY`) from the schema-rust
code generator. The contracts compile, round-trip test, and enforce interface
boundaries.

No finding -- this matches the psyche's stated design.

### 2.8 Content-addressed flake emission

**Severity: cosmetic (justifiable engineering).**

Lojix materializes four content-addressed flake directories (horizon, system,
deployment, secrets) from the cluster proposal, then passes them to `nix eval`
via `--override-input`. Each generated directory contains a tiny `flake.nix`
(e.g., `{ outputs = _: { system = "x86_64-linux"; }; }`).

A simpler alternative: pass horizon data as a JSON file directly to CriomOS
evaluation via `--impure` or an environment variable. But this would break
Nix's pure evaluation model, lose flake-eval caching (same system = same
narHash = cached pkgs evaluation), and require CriomOS to accept impure inputs.
The content-addressed approach is consistent with CriomOS's stub architecture
and Nix's flake design.

**Disconfirming evidence for the alternative:** CriomOS's `flake.nix:2` says
it is designed to consume "content-addressed flake inputs from lojix." The stub
architecture (no-horizon, no-system, no-secrets, default-deployment) exists
precisely to be overridden by content-addressed flakes. This is the designed
interface, not machinery added around it.

No finding against current shape.

### 2.9 TestDefaults and development scaffolding

**Severity: cosmetic.**

`TestDefaults` (`schema_runtime.rs:311`, `lib.rs:290`) provides shortened test
request forms. Production configuration uses `NoTestDefaults` (verified in the
CriomOS module's `startupRequest` and in the lojix-ownership check). The test
infrastructure is cleanly separated: `TestDefaults` fills in cluster/host/mode
only when the daemon was configured with them; production rejects shortened
forms.

No finding -- test scaffolding is correctly gated.

### 2.10 Nix module/packaging: OS-only placement

**Severity: no finding (aligned with psyche).**

The psyche ruled "it should only be in OS." Evidence:
- CriomOS imports `modules/nixos/lojix.nix` (the NixOS module).
- CriomOS-home has zero references to lojix.
- The `lojix-ownership` check (`CriomOS/checks/lojix-ownership/default.nix`)
  asserts `!(builtins.hasAttr "lojix" homePackages)`,
  `!(builtins.hasAttr "lojix-client" homePackages)`,
  `!(builtins.hasAttr "lojix" (rootLock.nodes."criomos-home".inputs or {}))`,
  and `!(builtins.hasAttr "lojix" homeLock.nodes)`.

Lojix is OS-only. The check enforces it.

### 2.11 CLI invariant: no flags

**Severity: no finding (aligned with psyche).**

The psyche ruled "CLIs cannot accept any other type of argument than the typed
input object." Evidence:
- `lib.rs:226-243`: `single_inline_dotos_argument` rejects flag-style arguments
  (`argument.starts_with('-') => Err(Error::FlagArgument)`), multiple arguments,
  and non-UTF-8 arguments.
- `client.rs:95-101`: `from_argument` rejects `DotosFile` and `SignalFile`
  forms with `Error::InlineDotosRequired`.
- The daemon binary accepts a signal file (its startup archive), not a Dotos
  argument -- this is the correct shape (the daemon is not a CLI client).

No flags exist. The invariant holds.

### 2.12 DeploymentPhase / DeploymentLifecycle duplication

**Severity: duplicates a source.**

`runtime_model.rs` defines both `DeploymentLifecycle` (line 222, 9 variants)
and `DeploymentPhase` (line 315, 9 variants) with identical variant names:
Submitted, Building, Built, Copying, Activating, Activated, Completed,
Rejected, Failed. `DeploymentLifecycle` is used in `DeploymentRecord`;
`DeploymentPhase` is used in `DeploymentPhaseEvent`. Both are persisted.

**Disconfirming evidence:** These may serve different roles in the type system
(record-level lifecycle vs event-level phase). But they are identical enums.

### 2.13 No hardwired host values

**Severity: no finding (aligned with psyche).**

The psyche ruled "nothing in this should hardwire bird or zeus anywhere" and
"remove those hard wired deployment variables." Lojix source contains no
hardwired node names, IP addresses, or host-specific values. All per-host
information comes from the deploy request (which comes from the manifest or
the agent's typed request). The `lojix.nix` CriomOS module uses only
configuration options, not hardwired values.

## 3. Disconfirming evidence summary

See inline per finding. The strongest case for the current shape:

1. **Type duplication (2.1, 2.12):** The flow/model split isolates the pipeline
   from serialization. This is a defensible architecture **if** the types are
   expected to diverge. They have not diverged yet.

2. **Store complexity (2.6):** The outbox and transition-intent staging serve
   contracts already on the wire (WatchDeployments, WatchCacheRetention). The
   machinery is proportional to the contract it serves. This survives.

3. **Request fields (2.5):** Builder, substituters, input mode, and output
   selector are correctness requirements for multi-host Nix deployment. The
   question is where they should default (manifest vs hard-coded), not whether
   they should exist.

4. **Content-addressed flakes (2.8):** This is the designed interface, not
   added machinery. It survives.

## 4. End-shape

The deploy tool than which none better is possible for this psyche:

```
           authored by psyche               authored by psyche
           ──────────────────               ──────────────────
    goldragon/datom.dotos              manifests/ouranos.dotos
    (cluster proposal)                 manifests/zeus.dotos
                                       (per-node deploy selection:
                                        cluster, node, proposal_source,
                                        flake, transport, action,
                                        activation_backend,
                                        source_revision_policy)

                 │                              │
                 ▼                              ▼
  ┌──────────────────────────────────────────────────────┐
  │                    lojix-daemon                       │
  │                                                       │
  │  meta-lojix 'Deploy.Host.(... from manifest ...)'     │
  │                                                       │
  │  1. Read proposal .dotos, project horizon             │
  │  2. Write content-addressed {horizon,system,           │
  │     deployment,secrets}/flake.nix                     │
  │  3. nix eval --override-input ... CriomOS#target      │
  │  4. nix build                                         │
  │  5. nix copy --to <store-uri>                         │
  │  6. Activate on target                                 │
  │                                                       │
  │  sema store: live-set, deploy-job, deployment-record, │
  │              gc-roots, event-log, identifier-alloc     │
  │  (drop: outbox, transition-intent, container-lifecycle,│
  │   test-run -- when no consumer uses them)              │
  │                                                       │
  │  ordinary socket: Query, Watch                         │
  │  owner socket: Deploy, Pin, Unpin, Retire, Test        │
  └──────────────────────────────────────────────────────┘
                         │
            CriomOS stubs overridden at eval time
                         │
                         ▼
              NixOS generation on target
```

### Changes from current state

1. **Fix Query.ByDeployment** -- one line: change `false` to the correct
   deployment-identifier match at `schema_runtime.rs:4187`.

2. **Implement or remove CheckHostKeyMaterial** -- either connect it to the
   target node's SSH host key, or remove it from the ordinary-socket contract
   until it is implemented.

3. **Author manifests** -- the psyche (or an agent at the psyche's direction)
   writes `manifests/ouranos.dotos` and `manifests/zeus.dotos` with the
   deploy-selection fields. The fields that are not per-request choices
   (builder, substituters, input mode, output selector) default from the
   manifest. Per-request overrides remain possible through the CLI.

4. **Consolidate duplicated types** -- the runtime_flow.rs types that are
   identical to runtime_model.rs types should either be newtype wrappers around
   the model types (if the rkyv derives are not wanted in the pipeline) or
   unified. DeploymentPhase/DeploymentLifecycle should be one enum.

5. **Evaluate store tables** -- if WatchDeployments and WatchCacheRetention
   have no current consumers (agents do not use them), the outbox and
   transition-intent tables can be removed. Container-lifecycle is a mirror
   with no current producer. Test-run is used by the Test contract and should
   stay if testing is used.

### Vertical-slice migration (cluster deployable at every step)

Step 1: Fix ByDeployment (one-line change, no migration).
Step 2: Consolidate duplicated types (internal refactor, no wire change).
Step 3: Author manifests for Ouranos and Zeus.
Step 4: Deploy Ouranos using the authored manifest (proves the vertical slice).
Step 5: Deploy Zeus using its manifest.
Step 6: Evaluate and remove unused store tables.

No compatibility path needed -- each step is a forward change that does not
break the existing contract.

## 5. Unknowns

1. Whether the runtime_flow/runtime_model type split was an intentional
   architecture decision or an accidental duplication. No comment or commit
   message explains the split.

2. Whether the Deploy request's `DeploymentInputMode::Direct` has ever been
   used in production. If not, it may be dead code.

3. Whether any subscription consumer (WatchDeployments, WatchCacheRetention)
   has ever been connected by an agent or tooling. If not, the outbox and
   transition-intent tables have no justification.

4. What the correct shape of a deployment manifest `.dotos` is -- no psyche
   ruling defines the manifest format.

5. Whether the container-lifecycle mirror has a producer. The daemon writes
   container transitions, but what generates them is unclear.

6. Whether `lojix-bootstrap` is still needed now that the daemon is deployed
   via the CriomOS module. Bootstrap was the pre-daemon ingress.

7. The provenance of `DeploymentPhase` vs `DeploymentLifecycle` -- whether
   the duplication was intentional.

## Sources

### Lojix source (read directly)
- `/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs` (8,135 lines)
- `/git/github.com/LiGoldragon/lojix/src/runtime_flow.rs` (544 lines)
- `/git/github.com/LiGoldragon/lojix/src/runtime_model.rs` (940 lines)
- `/git/github.com/LiGoldragon/lojix/src/lib.rs` (3,017 lines)
- `/git/github.com/LiGoldragon/lojix/src/daemon.rs` (1,103 lines)
- `/git/github.com/LiGoldragon/lojix/src/client.rs` (231 lines)
- `/git/github.com/LiGoldragon/lojix/src/adapters.rs` (629 lines)
- `/git/github.com/LiGoldragon/lojix/src/bin/lojix.rs` (22 lines)
- `/git/github.com/LiGoldragon/lojix/src/bin/meta-lojix.rs` (24 lines)
- `/git/github.com/LiGoldragon/lojix/src/bin/lojix-daemon.rs` (24 lines)
- `/git/github.com/LiGoldragon/lojix/flake.nix`

### Signal contracts (read directly)
- `/git/github.com/LiGoldragon/signal-lojix/src/` (1,444 lines total)
- `/git/github.com/LiGoldragon/meta-signal-lojix/src/` (1,481 lines total)

### CriomOS integration (read directly)
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/lojix.nix`
- `/git/github.com/LiGoldragon/CriomOS/checks/lojix-ownership/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix` (lojix input, stubs)
- `/git/github.com/LiGoldragon/CriomOS/stubs/{no-horizon,no-system,default-deployment,no-secrets}/flake.nix`

### Primary workspace (read directly)
- `/home/li/primary/manifests/` (empty)
- `/home/li/primary/NON_MANAGEMENT_AGENTS.md`

### Psyche reports (read in full)
- `flows/674a4dab/reports/psycheLojix.md`
- `flows/674a4dab/reports/psycheStackOrigins.md` (sections: Lojix, three stacks)

### Witness maps (read in full, relevant sections)
- `flows/674a4dab/witnesses/rustSideMap.md` (section 3: Lojix, section 5: Dead/Duplicated)
- `flows/674a4dab/witnesses/nixSideMap.md` (sections 1-3: Flake graph, Where defined, Build path)

### Lojix tests (counted, not read in full)
- `/git/github.com/LiGoldragon/lojix/tests/` (17 test files, 2,869 lines)
