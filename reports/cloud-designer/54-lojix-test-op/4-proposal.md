# 54 — Proposal: the lojix test operation + multi-host node model

Status: **PROPOSAL for psyche confirmation before building.** This touches
two production-track contracts (`horizon-rs` and the `lojix` triad), so
nothing is built until confirmed. Frame and method: `0-frame.md`.

The convergence in one line: a test-VM node declares one-or-more FIXED
vmhosts (the declared host-set is the image-exchange trust boundary);
lojix gains a typed meta `Test` operation plus a `Check` shorthand, the
daemon config carries a default vmhost, and a `Test` either fires a
hermetic nix check or drives the report-51 host-untouched live cycle,
recording a durable queryable result.

## 1. HORIZON multi-host node model

### 1.1 Representation — primary `super_node` + additive `super_nodes`

Keep `Machine.super_node: Option<NodeName>` as the **primary/canonical
host** (arch resolution, the guest-fold discovery predicate, and the
single-host majority all keep reading it unchanged). Add one new field at
the positional tail of `Machine` (after `disk_gb`/`location`, the
positional-NOTA tail rule):

```rust
/// Additional hosts permitted to hold and exchange this Pod's image.
/// Empty (the default) = the single-host majority, host-set =
/// {super_node}. Non-empty extends the image-distribution trust
/// boundary to {super_node} ∪ super_nodes. Pod-only; cluster-authored;
/// FIXED in the declaration. MUST stay near the end so positional nota
/// records keep parsing with implicit empty defaults.
#[serde(default)]
pub super_nodes: Vec<NodeName>,
```

The node's full **declared host-set** is `{super_node} ∪ super_nodes`,
deduped, primary first. One accessor (methods-only rule), the single
reader every consumer goes through:

```rust
impl Machine {
    /// The declared host-set: primary super_node first, then the
    /// additional super_nodes, deduped. Empty only for a non-Pod.
    pub fn host_set(&self) -> Vec<&NodeName> { /* … */ }
}
```

Why primary-plus-additive over widening `super_node` to `Vec<NodeName>`:
the additive shape leaves every existing single-host node
(`super_nodes` defaults `[]`) projecting byte-identically, keeps
`super_node` as the unambiguous primary that arch/user resolution already
read, and confines the change to one new field plus the host-set fold —
not every consumer, fixture, and resolution site. This is the smaller
correct shape, not a compatibility concession. (Decision A below offers
the `Vec` alternative if the psyche prefers it.)

### 1.2 Image-exchange permission wiring — a scoped projection field

"Permission to send each other the image" decomposes, in the existing
mechanism, into: the **receiving** host trusts the **sending** host's Nix
signing key (`trusted-public-keys` / `extra-trusted-public-keys`), and the
sender is reachable as a substituter (`is_nix_cache` + `nix_url`). There
is no per-node "allowed peers" set today; image trust today is the
cluster-wide roll-up `Cluster.trusted_build_pub_keys` (every node's
`nix_pub_key_line`, flat-collected at projection) fed into
`nix.settings.trusted-public-keys`.

Proposed: make the host-set→key relation **explicit and typed in the
projection** rather than leaning on the cluster-wide pool. Add a
projection-derived field on the output `Node` (a guest node):

```
image_exchange_pub_keys: Vec<NixPubKeyLine>
```

derived exactly the way `cache_urls` / `dispatchers_ssh_pub_keys` are
derived in `Node::fill_viewpoint` — filter the node map by the node's
host-set, map each host to its `nix_pub_key_line`. Symmetrically, each
host node collects the signing keys of its peer hosts across every guest
it co-hosts. CriomOS then emits those as `extra-trusted-public-keys`
scoped to the test-VM substrate (mirroring how lojix already injects
`extra-trusted-public-keys` per deploy), the host-set being the trust
scope.

This records the host-set→key relation explicitly (queryable, testable)
in the typed projection and leaves the choice of how narrowly CriomOS
scopes the actual `nix.settings` sink as a CriomOS-side decision —
without re-deriving trust from node names. Phase 1 may feed
`image_exchange_pub_keys` into the same `trusted-public-keys` sink as
today (no behavior change, the relation is now explicit); narrowing the
emitted scope is a follow-on. (Decision B asks whether the boundary
should in fact be tighter than cluster-wide, which is the only thing that
makes the scoping load-bearing.)

### 1.3 Invariant updates

- **C1 (Pod-super_node-exists)** extends to the whole host-set: every
  name in `{super_node} ∪ super_nodes` must exist in the cluster (loop the
  host-set; emit `Error::MissingSuperNode(node, missing_host)` per missing
  entry). Today it checks only `super_node`.
- **Single-arch invariant (new):** all hosts in the set must resolve to
  the same `Arch` — a guest image is one closure; every host that may run
  it must share its architecture. New `Error::HostSetArchMismatch`. Arch
  resolution itself stays the single hop on `super_node` (the primary).
- **Image-exchange readiness (new, gated on §1.2 narrowing):** every host
  in a node's host-set expected to serve/receive the image must have a
  `nix_pub_key_line`, and to pull must be `is_nix_cache` with a
  `nix_url` — mirroring the three `DeploymentRejected` checks lojix
  already enforces, so a host-set naming an unsigned host fails
  projection rather than silently failing to copy.
- **`super_user` follow-up:** `super_user` is single-valued (the runner on
  the primary host). A multi-host guest implicitly needs that user present
  on each host; today nothing validates the runner user exists on any
  host. Flagged as a follow-up gap, not blocking.

Single-host nodes (`super_nodes = []`) are entirely unaffected by every
one of these — each new check is a no-op on a one-element host-set.

## 2. The lojix test OPERATION — meta, not ordinary

The op lives on the **owner-only meta contract** (`meta-signal-lojix`),
alongside `Deploy/Pin/Unpin/Retire`. Reasoning:

- A test run starts a VM and deploys into it — strictly more privileged
  than `Deploy`, which is already meta-only. It cannot sit on the
  unauthenticated ordinary read/observe socket.
- A LIVE test reuses the meta deploy machinery directly (the
  `submit_deploy` / `decide_meta_input` path), spawned via the same
  `DeployJobs` decoupled executor so it survives client disconnect.
- The ordinary contract is explicitly the read/observe/subscribe surface;
  its header already states "Owner-only mutations live in
  meta-signal-lojix."

The **result** is read back on the ordinary contract (§5.3) — write on
meta, observe on ordinary, exactly as deploys already work.

### 2.1 Schema additions to `meta-signal-lojix/schema/lib.schema`

Extend the operation root and reply root:

```schema
[Deploy Pin Unpin Retire Test]
[Deployed DeployRejected Pinned PinRejected Unpinned UnpinRejected
 Retired RetireRejected Tested TestRejected]
```

In the `{...}` body, the request (reusing the already-imported
`ClusterName`/`NodeName`/`DatabaseMarker`):

```schema
Test TestRequest

;; full form vs shorthand verb — a real shorter variant, not a
;; defaulted field (nota forbids tail-omission)
TestRequest    [(Run TestRun) (Check QuickCheck)]
TestRun        { ClusterName * NodeSelection HostSelection TestMode }
QuickCheck     { ClusterName * NodeName * }
NodeSelection  [(Nodes [NodeName]) All]
HostSelection  [DefaultHost (OnHost NodeName)]
TestMode       [Hermetic Live]
```

- `NodeSelection` — `(Nodes [<name> …])` for an explicit guest list, or
  bare `All` to sweep every Pod the resolved host runs.
- `HostSelection` — the multi-host picker: `DefaultHost` reads the daemon
  config default (§4); `(OnHost <h>)` overrides **among the node's
  declared host-set**. The daemon rejects a host not in the declared set.
- `TestMode` is two variants, not three. Report 53 had `[Hermetic Live
  Both]`; `Both` was a client-side convenience. Inside the daemon, one
  request is one effect — a caller wanting both issues two ops. (Decision
  C revisits this.)

Replies (mirroring the existing meta receipt pairs, each carrying the
imported `DatabaseMarker`):

```schema
Tested AcceptedTest
TestRejected RejectedTest

;; the daemon mints a run id and returns an immediate accepted handle,
;; exactly like AcceptedDeploy — the result lands durably and is read
;; over the ordinary socket (§5.3), not returned inline.
AcceptedTest { TestRunIdentifier * DatabaseMarker * }

TestRejectionReason [ClusterUnknown NodeUnknown
  VmHostNotDeclaredForNode HostDeclaresNoVmHost
  NodeNotHostedOnVmHost SubstrateUnavailable InternalError]
RejectedTest { TestRejectionReason * DatabaseMarker * }
```

`TestRunIdentifier` is a new `Integer` shared type, defined in
`signal-lojix:lib` (so the ordinary query path can name it too) and
cross-imported into meta, exactly as `DeploymentIdentifier` is.

## 3. The SHORTHAND verb — `(Check <node>)` lowering to the full op

The shorthand follows the spirit `State`→`Record` precedent precisely:
**a distinct typed NOTA operation that fills defaults and lowers to the
full record** — never an under-filled struct or a flag. spirit's `State`
carries raw text the daemon classifies and fills; lojix's `Check` carries
only the node and the daemon expands the rest from config defaults.

```
;; routine "test this node" — cluster, host, mode all from config
meta-lojix '(Test (Check goldragon mercury))'

;; full form — explicit selection, host, mode
meta-lojix '(Test (Run goldragon (Nodes [mercury]) (OnHost prometheus) Hermetic))'
```

`QuickCheck { ClusterName NodeName }` *structurally means* "this node, the
config-default host, the config-default mode" — the decoder expands it to
a full `TestRun`. The lowering happens in the daemon's `decide_meta_input`
path, reading `RuntimeConfiguration` defaults — the same architectural
spot where spirit's daemon classifies `State`. It is a real shorter
variant whose meaning the decoder expands, not a positional record with
omitted fields (NOTA forbids tail-omission).

The schema file is where the shorthand vocabulary is "maintained": adding
a routine verb is a schema edit regenerated into the typed codec; the
daemon never hand-parses NOTA, the CLI decodes via the generated decoder.

## 4. The CONFIG-DEFAULT vmhost — a new `DaemonConfiguration` field

Today `DaemonConfiguration` is exactly five fields (two socket paths +
two modes + state dir) with no test surface. Add a `test_defaults` field:

```rust
pub struct DaemonConfiguration {
    pub ordinary_socket_path: String,
    pub ordinary_socket_mode: u32,
    pub owner_socket_path: String,
    pub owner_socket_mode: u32,
    pub state_directory_path: String,
    pub test_defaults: TestDefaults,   // NEW
}

pub struct TestDefaults {
    pub cluster: String,
    pub default_vm_host: String,   // the config-default vmhost
    pub default_mode: TestMode,    // Hermetic as the everyday default
}
```

- **Binary-only config.** This is decoded from the single rkyv startup
  file (`DaemonConfiguration::from_rkyv_file`); the daemon rejects inline
  NOTA and `.nota`. The default vmhost is authored as typed NOTA in
  `lojix-write-configuration` and encoded to rkyv before exec — never a
  flag, never a runtime `Configure` op. (lojix's INTENT.md aspirationally
  lists a `Configure` meta op; the test defaults deliberately ride the
  binary-startup path instead, consistent with the
  daemons-take-binary-config-only override.)
- `RuntimeConfiguration::from_daemon_configuration` projects it into the
  runtime so `decide_meta_input` can read it when lowering `(Check …)`.
- This is exactly "config gives it a default": `(Check goldragon mercury)`
  lowers `HostSelection` to `DefaultHost` →
  `test_defaults.default_vm_host`; an explicit `(OnHost prometheus)`
  overrides it, but only to a host the node declares.

`TestMode` is defined once in `meta-signal-lojix` and imported into the
config schema (the same cross-import the meta contract already does for
`signal-lojix` types), since it is shared between the wire op and the
config default.

## 5. DISPATCH + LIFECYCLE + DURABLE RESULT

The key finding: almost all dispatch/lifecycle machinery already exists —
the new work is one meta op arm, two effects, one durable table driver,
and the config field. The op spawns through the existing `DeployJobs`
decoupled executor (submit returns an accepted handle; the run outlives
the client), reuses the `EffectCommand` pipeline and `SshTarget` (which
already targets the guest by its horizon domain, zero VM special-casing),
and writes through the existing event-log commit pattern.

### 5.1 Vmhost resolution (config-default + override within the declared set)

1. `DefaultHost` → `test_defaults.default_vm_host`. `(OnHost h)` → `h`.
2. The daemon validates the resolved host is in the node's **declared
   host-set** (`{super_node} ∪ super_nodes` from the projection) and that
   the host declares a `VmHost` service. Not-in-set →
   `(TestRejected VmHostNotDeclaredForNode)`; host with no VmHost service
   → `(TestRejected HostDeclaresNoVmHost)`. This preserves the invariant
   that "test X on host Y" is a cluster-data pairing, never a per-run
   mutation — the request *selects within* the declared set, never invents
   a host.

### 5.2 Hermetic vs Live dispatch

- **Hermetic** (everyday default, zero host effect): the daemon issues one
  `NixBuild` effect per node of the pre-declared auto-pickup check
  `.#checks.<system>.vm-<cluster>-<node>` (the §1 auto-pickup
  `runNixOSTest` engine). `runNixOSTest` owns its own sandboxed VM — no
  SSH, no tap, no live host. Pass/fail is the build exit status. The
  daemon stays a pure dispatcher selecting checks by name; no nix
  authoring at runtime.
- **Live** (report-47 v2 — the daemon-driven host-untouched cycle): the
  full report-51 §3 cycle, now driven from inside the daemon via two new
  daemon-owned effects bracketing the existing deploy chain:
  `BringUpTestVm → [ResolveFlakeAuth → MaterializeHorizon → NixEval →
  NixBuild → CopyClosure → ActivateGeneration] → assert →
  TearDownTestVm`. `BringUpTestVm` shells `ssh <host-fqdn>` +
  `systemd-run --user` + `unshare -rn` + `nsenter` to bring up the
  generated microVM and additive tap **inside a user network namespace**
  (the one host-touching step, user-level only — no sudo, no
  switch-to-configuration). The deploy in the middle is the same internal
  effect chain `Deploy` runs, sequenced after bring-up. `TearDownTestVm`
  stops the user units; the tap and route vanish with the namespace —
  host netns byte-identical. The whole cycle runs in one `DeployJobs`-style
  spawned pipeline, surviving client disconnect.

A hard safety refusal carried from report 51: on a `VmHost` that is also a
live router, LIVE runs only the host-untouched user-namespace path — never
`switch-to-configuration` on the router itself.

### 5.3 The durable queryable result (closing the observability gap)

The daemon emits no logs — a failed deploy is silent today. The deploy
path already closes this via durable `Generation`/`DeployJob` records read
over `(Query (ByNode …))`. The test op closes the same gap with a new SEMA
table mirroring `DeployJobTable` exactly (one row per submitted test,
written on submit, rewritten at every phase transition so a restarted
daemon reconciles an in-flight test):

```schema
TestRunTable   { runs (Vec TestRunRecord) }
TestRunRecord  { TestRunIdentifier * ClusterName * NodeName *
                 host NodeName mode TestMode phase TestRunPhase
                 outcome TestOutcome closure_path (Optional ClosurePath)
                 detail (Optional TestDetail) }
TestRunPhase   [Submitted BringingUp Deploying Asserting TearingDown Completed Failed]
TestOutcome    [Pending Passed (Failed FailureStage)]
FailureStage   [BringUp Deploy Assert TearDown HermeticCheck]
```

Each transition lands a `LoggedEvent` in the append-only event log so the
test's phase timeline is durably auditable. The bring-up/teardown
`Starting/Started/Stopping/Stopped` transitions of the live VM record
through the existing **`ContainerLifecycleRecord`** table — finally giving
that built-but-undriven scaffolding its driver (named in report 47 §2:
"only the driver is missing"). The Live test op is that driver.

Queryable via the ordinary CLI by extending the ordinary `Selection`:

```schema
Selection [(ByNode NodeSelector) (ByGeneration GenerationLookup)
           (ByEventLog EventLogRange) (ByTestRun TestRunLookup)]
TestRunLookup { ClusterName * NodeName * run (Optional TestRunIdentifier) }
```

`lojix '(Query (ByTestRun (goldragon mercury None)))'` returns the durable
`TestRunRecord` — pass/fail, phase reached, the deployed closure, and the
exact failure stage (`(Failed Deploy)` vs `(Failed Assert)`). A failed
LIVE test is no longer silent.

## 6. Implementation order + gates

Designer lanes ship `next`/feature branches under `~/wt/...`; operators
own main + rebase. The lojix triad (component + signal + meta-signal)
pushes to main per its triad discipline. Order chosen so each step is
independently green:

1. **horizon-rs (`horizon-test-vm` branch, designer).** Add
   `Machine.super_nodes` + `Machine::host_set`, the projected
   `image_exchange_pub_keys` fold, the extended C1 host-set existence
   invariant + single-arch invariant. Single-host fixtures stay
   byte-identical; add a multi-host fixture and tests. No lojix dependency
   yet.
2. **signal-lojix + meta-signal-lojix schema (designer → operator
   integrates to triad main).** Add `TestRunIdentifier` to signal-lojix;
   add `Test`/`TestRequest`/`Run`/`Check`/replies to meta-signal-lojix;
   add `(ByTestRun …)` to the ordinary `Selection`. Regenerate codecs.
3. **lojix daemon (operator owns main).** `TestDefaults` on
   `DaemonConfiguration` + `RuntimeConfiguration` projection;
   `TestRunTable`/`TestRunRecord` in sema; the `Test` arm in
   `decide_meta_input` with the `(Check …)` lowering and host-set
   validation; the Hermetic dispatch (`NixBuild` of `vm-<node>`); the two
   new `BringUpTestVm`/`TearDownTestVm` effects + the Live pipeline; the
   `(ByTestRun …)` query path; wire bring-up/teardown into
   `ContainerLifecycleRecord`.
4. **CriomOS (designer branch).** Emit `image_exchange_pub_keys` into the
   test-VM substrate's `extra-trusted-public-keys` (phase 1 may target the
   existing `trusted-public-keys` sink).
5. **`lojix-write-configuration`.** Author the `test_defaults` typed NOTA,
   encode to rkyv.

Gates:

- **The first LIVE run on Prometheus stays behind explicit psyche
  authorization** (report 51 §5). Hermetic is freely runnable; LIVE is
  not, until the psyche authorizes the first Prometheus cycle.
- Everything before step 3's Live path (the horizon model, the schema,
  Hermetic dispatch, the durable table, the query) is independently
  green and unblocked by the gate.

## Open decisions needing psyche confirmation

- **Decision A — host-set representation.** Recommended: additive
  `super_nodes: Vec<NodeName>` beside the primary `super_node` (single-host
  byte-identical, primary stays unambiguous). Alternative: widen
  `super_node` to `Vec<NodeName>` (conceptually cleaner, touches every
  consumer + a "which is primary?" choice for arch/user). Confirm A or
  request the widening.
- **Decision B — image-exchange trust boundary scope.** Is the host-set
  meant to be *tighter* than the existing cluster-wide signing-key pool?
  If yes, the §1.2 scoped `extra-trusted-public-keys` emission and the
  image-exchange-readiness invariant are load-bearing. If cluster-wide is
  acceptable, the host-set is purely a placement/permission fact and
  `image_exchange_pub_keys` is recorded for queryability but the actual
  trust needs no narrowing.
- **Decision C — `TestMode` arity.** Recommended `[Hermetic Live]` (one
  op = one effect; a caller wanting both issues two). Confirm, or add
  `Both` as a third privileged variant (hermetic gate then live).
- **Decision D — `Check` shorthand surface.** `(Check <cluster> <node>)`
  carries cluster + node, lowering host + mode from config. Confirm
  cluster stays explicit, or make cluster itself a config default so the
  routine verb is `(Check <node>)`.
- **Decision E — result inline vs query-only.** Recommended: `Test`
  returns an immediate `AcceptedTest { TestRunIdentifier }` handle (like
  `AcceptedDeploy`) and the result is read over the ordinary
  `(ByTestRun …)` query. Confirm, or request a blocking variant that
  returns the terminal verdict inline (weaker disconnect survival).
