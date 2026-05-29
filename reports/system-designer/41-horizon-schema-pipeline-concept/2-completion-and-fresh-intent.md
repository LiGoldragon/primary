# Horizon-next — completion + fresh intent (the Plane surface, the running chain, the durable witness)

*Sub-agent completion report (system-designer lane, per record 920). The prior
build agent crashed on an API connection drop after committing collections +
building `horizon-next` locally (commit `f64a52a`, no remote, verified only by
`cargo test`). This pass FINISHED it (remote + hermetic `nix flake check`),
CLOSED the three carried-forward `/42` divergences (D2/D3/D4), and reached
further into the freshest design intent than the prior pass — the record-1054
data-carrying `Plane` enum wired into a running three-engine chain. Per record
1059 the session hit no blocking connection issues; per record 1049 every
result below is verified and honestly bounded — what works AND what is still
open is stated plainly.*

## The headline: the hermetic witness passes, reproducibly, from the pushed commit

`nix flake check` on the **committed clean tree** of `horizon-next`
(`/git/github.com/LiGoldragon/horizon-next`, branch
`collections-horizon-2026-05-28`, pushed commit `1b64d1b`) ends with:

```
running 0 flake checks...
all checks passed!
```

(`running 0 flake checks` = every derivation was cached-valid from the committed
source — i.e. the green is reproducible from the pushed tree, not from a dirty
working copy.) All twelve checks pass:

```
  - build
  - test                                   # 7 projection + 3 three-engine-chain tests
  - fmt
  - clippy                                 # -D warnings, clean
  - collections-emitted                    # D1 (collections) witness
  - cross-crate-import-emitted             # /39 import witness
  - projection-on-schema-noun
  - plane-surface-data-carrying            # NEW — record 1054
  - running-three-engine-chain             # NEW — D4 + records 1028/1030
  - types-only-core-has-no-runtime-floor   # NEW — D3
  - no-production-free-functions
  - local-schema-source-patches
```

The `test` derivation's own log (extracted from the Nix build) confirms the
chain tests genuinely RAN in the sandbox, not just locally:

```
     Running tests/projection.rs (...)
test result: ok. 7 passed; 0 failed; ...
     Running tests/three_engine_chain.rs (...)
test each_plane_crossing_is_visible_and_typed ... ok
test signal_engine_rejects_an_empty_cluster_before_projection ... ok
test request_drives_signal_then_nexus_then_sema_and_echoes_origin_route ... ok
test result: ok. 3 passed; 0 failed; ...
```

## Part A — FINISH (durable + proven)

### A1. The GitHub remote exists + is pushed

`gh repo create LiGoldragon/horizon-next --public` (matching the PUBLIC
visibility of the sibling `schema-next` / `schema-rust-next` / `schema-core`
repos, modelled on how `/39` created `schema-core`). Branch
`collections-horizon-2026-05-28` is pushed; the concept is no longer a local-only
artifact. Final pushed commit: `1b64d1b`.

### A2. The hermetic `nix flake check` witness (Spirit 1006's stronger bar)

The prior verification was `cargo test` only. This pass lands the hermetic Nix
witness (output above). Two cross-repo problems were solved to get there:

- **The nota-next pin divergence (record 1057), confirmed concretely.** The
  three repos pinned three different nota-next commits. I verified the hazard is
  real, not theoretical: building schema-next against nota-next `83720738` ("mark
  structure header overflow") FAILS schema-next's
  `design_example_schema_lowering_records_source_structure_header` test —
  `83720738` emits a `(Unknown, 15)` overflow marker where `5e063042` emits
  `(Parenthesis, 1)`. **Fix:** aligned ALL THREE repos to nota-next `5e063042`
  (the commit schema-next builds against, which has `StructureHeader`):
  schema-rust-next's Cargo.lock pinned down to it, horizon-next's Cargo.lock
  pinned to it, and the flake's `nota-next-source` input pinned to the exact
  rev `5e063042…`. All three repos' test suites pass at this pin.
- **The flake patches the schema deps to the FEATURE BRANCHES (git, not local
  path).** The committed flake (already authored by the prior agent and
  preserved) vendors `schema-next` / `schema-rust-next` from their pushed
  `collections-horizon-2026-05-28` branches and patches Cargo's git source to
  the vendored copies — Nix source-filtering can't reach a local path, exactly
  as record 1057 warns. Modelled on spirit-next's crane setup.

**One honest landmine caught and fixed.** The chain test file was initially
UNTRACKED in the git repo. `nix flake check` uses the `git+file://` tree, which
excludes untracked files — so the first "passing" `test` derivation ran ONLY
`projection.rs` and silently skipped my chain tests, and the
`running-three-engine-chain` witness failed on a missing file. I `git add`ed the
test, re-ran, and confirmed (from the sandbox log above) the chain tests now
actually execute. This is the kind of fake-green record 1049 forbids; it is
closed.

## Part B — the three `/42` divergences, closed

### D4 (+ record 1054) — a running three-engine chain that ACTUALLY DRIVES

This is the centre of the pass and converges with the fresh intent (below). The
prior state emitted `InputNexus`/`OutputNexus` dispatch traits but no running
chain (the dead-scaffolding shape record 1030 forbids). Now:

- The schema emits the **record-1054 data-carrying `Plane` enum** (full emitted
  Rust in §"Fresh intent" below) and the three trait-ordered engines
  `SignalEngine` / `NexusEngine` / `SemaEngine` (each `Plane -> Plane`), plus
  `Plane::drive` — the running chain.
- `horizon/src/lib.rs` implements the three engines on real data-bearing nouns:
  `SignalGate` (admission policy), `ProjectionNexus` (runs the existing
  `ClusterProposal::project`), `ProjectionSema` (owns the durable
  last-projection `BTreeMap` + an applied-count).
- `horizon/tests/three_engine_chain.rs` drives a real Horizon projection request
  end to end through all three engines via `Plane::drive`, asserts the reply
  carries the projected output with the distrusted node dropped, and asserts the
  origin route minted at ingress is echoed on the reply. A second test drives the
  engines one crossing at a time so each plane boundary is visible (the
  `skills/testing.md` per-plane-chain-typing rule). A third proves the Signal
  gate rejects an empty cluster before Nexus/Sema run.

Evidence: the `running-three-engine-chain` witness + the 3 passing chain tests in
the hermetic `test` derivation (above).

### D3 — the types-only-module shape (no vestigial signal plane)

The 4-position document forced a signal plane onto every module. Now
**Input/Output are OPTIONAL at the document** (a schema-next change):

- `SchemaEngine::lower_document_with_resolver` accepts two shapes, told apart
  structurally: a COMPONENT module is `{imports} (Input) (Output) {namespace}`
  (4 root objects); a TYPES-ONLY module is `{imports} {namespace}` (2 root
  objects). `Asschema` models this as `signal_plane: Option<SignalPlane>`;
  `input()`/`output()` return `Option<&EnumDeclaration>`.
- The Rust emitter reads the option: a types-only module emits ONLY its types +
  the NOTA codec — no root enums, signal frames, mail floor, or Plane surface.
- `horizon-core` is the first real types-only module: `magnitude.schema` is now
  `{} { Magnitude (...) }`, and the emitted `magnitude.rs` dropped from ~520 to
  ~150 lines, carrying zero floor symbols.

Evidence: schema-next's two new `lowering.rs` witnesses
(`types_only_module_lowers_to_imports_and_namespace_with_no_signal_plane`,
`component_module_still_carries_its_signal_plane`); horizon-next's
`types-only-core-has-no-runtime-floor` flake witness.

### D2 — the shared runtime floor (closed for the type-library case; honestly bounded)

D2's complaint was the generic floor duplicated into EVERY emitted module. D3's
fix resolves the concrete instance here: a types-only module emits NO floor, so
the floor is no longer duplicated into the imported type library
(`horizon-core`). It now lives ONCE, in the `horizon` component. The
cross-crate-import mechanism (`/39`, `pub use horizon_core::…` + the
`NotaDecodeError` bridge) already shares the imported TYPES.

**Honestly open:** the mandate's fuller D2 — extracting the generic
`OriginRoute`/`Plane`/engine-trait machinery into a dedicated shared-floor crate
that MULTIPLE components import via `pub use` — is NOT done. With one component
(`horizon`) there is exactly one copy of the floor, so there is no duplication to
eliminate yet; a second component would re-emit it. The dedicated floor crate is
the next step when a second component lands. What's closed: the floor is gone
from the type library; what's deferred: a workspace-wide single floor crate
across many components.

## Part C — MORE fresh intent than the last pass (the deepening, per record 1060)

The prior agent's emitter had no `Plane` enum at all (the collections-branch
emitter emitted only `NexusMail` + `InputNexus`/`OutputNexus`, no origin route).
This pass implements the freshest records:

### Record 1054 (Maximum) — the data-carrying `Plane` enum

The emitted Rust (verbatim from `horizon/src/schema/horizon.rs`):

```rust
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Clone, Debug, PartialEq, Eq)]
pub enum Plane {
    Signal(OriginRoute, Input),
    Nexus(OriginRoute, Input),
    Sema(OriginRoute, Output),
}

impl Plane {
    pub fn at_ingress(origin_route: OriginRoute, request: Input) -> Self {
        Self::Signal(origin_route, request)
    }

    pub fn origin_route(&self) -> OriginRoute {
        match self {
            Self::Signal(origin_route, _) => *origin_route,
            Self::Nexus(origin_route, _) => *origin_route,
            Self::Sema(origin_route, _) => *origin_route,
        }
    }
}
```

The variants CARRY the actual plane messages (`Input` / `Output`), so runtime
code matches DIRECTLY on the plane — this is NOT a thin kind tag beside a
separate envelope (record 1052 names that shape wrong; the prior crashed agent's
separate `Signal<Root>`/`Nexus<Root>`/`Sema<Root>` envelopes + `Kind` tag are
exactly what 1054 supersedes, and they are gone).

### Records 1038/1039 — origin route auto-created on the root, threaded + echoed

`OriginRoute` is the leading tuple element of every `Plane` variant — the
auto-created field on the root plane object. Minted at ingress
(`Plane::at_ingress` / `OriginRoute::at_ingress`), threaded through every hop,
and echoed on the reply. It also rides on `NexusMail` / `MessageSent` /
`MessageProcessed` and the nexus-dispatch method. **New clarification captured:**
record 1062 (Medium) records the design decision that the route is the variant's
leading tuple element (vs a named struct field) — pending psyche confirmation.

### Records 1028/1030 — the three engines as a chain that drives

The emitted chain driver (verbatim):

```rust
#[allow(clippy::type_complexity)]
pub fn drive<Signal, Nexus, Sema>(
    self,
    signal: &Signal,
    nexus: &Nexus,
    sema: &mut Sema,
) -> Result<Plane, PlaneChainError<Signal::Error, Nexus::Error, Sema::Error>>
where
    Signal: SignalEngine,
    Nexus: NexusEngine,
    Sema: SemaEngine,
{
    let ingress_route = self.origin_route();
    let admitted = signal.admit(self).map_err(PlaneChainError::Signal)?;
    let Self::Nexus(_, _) = &admitted else {
        return Err(PlaneChainError::UnexpectedPlane);
    };
    let executed = nexus.execute(admitted).map_err(PlaneChainError::Nexus)?;
    let Self::Sema(_, _) = &executed else {
        return Err(PlaneChainError::UnexpectedPlane);
    };
    let reply = sema.apply(executed).map_err(PlaneChainError::Sema)?;
    debug_assert_eq!(reply.origin_route(), ingress_route);
    Ok(reply)
}
```

The chain-driving test (the heart of the D4 witness, verbatim from
`horizon/tests/three_engine_chain.rs`):

```rust
#[test]
fn request_drives_signal_then_nexus_then_sema_and_echoes_origin_route() {
    let ingress_route = OriginRoute::at_ingress(42);
    let ingress = Plane::at_ingress(ingress_route, Input::Project(sample_cluster()));
    assert!(matches!(ingress, Plane::Signal(_, _)));
    assert_eq!(ingress.origin_route(), ingress_route);

    let signal = SignalGate::new();
    let nexus = ProjectionNexus::new();
    let mut sema = ProjectionSema::new();

    let reply = ingress
        .drive(&signal, &nexus, &mut sema)
        .expect("the request drives cleanly through the three-engine chain");

    let Plane::Sema(reply_route, Output::Projected(configs)) = reply else {
        panic!("the chain should reply with a Sema-plane projected output");
    };
    assert_eq!(reply_route, ingress_route);          // origin route echoed
    assert_eq!(configs.len(), 2);                    // distrusted "ghost" dropped
    assert!(!configs.contains_key(&NodeName(String::from("ghost"))));
    assert_eq!(sema.applied_count(), 1);             // Sema applied the reply
    assert_eq!(sema.last_projection(), &configs);
}
```

This drives a real Horizon `ClusterProposal` projection through Signal → Nexus →
Sema, exercising each engine's trait surface with the right `Plane`-carried
message, and proves the origin route threads end to end.

## What is honestly still open

- **D2's dedicated shared-floor crate** (across MULTIPLE components) — not done;
  see D2 above. The floor is gone from the type library and lives once in the
  one component; a second component would re-emit it.
- **`Plane` payload for distinct Nexus/Sema languages.** For Horizon (Signal-
  only schema) the `Plane` Nexus/Sema variants carry the Signal roots
  (`Input`/`Output`), which is correct for Horizon. A schema like Spirit that
  declares distinct `NexusInput`/`SemaInput` execution-language types would,
  under the deepest reading of 1054, carry those in the Nexus/Sema variants; the
  current emitter carries the Signal roots uniformly. This is a defensible
  scope line (the `Plane` is the dispatch surface; the distinct languages are
  still emitted as data types) but is worth a psyche confirmation. Record 1062
  flags the related placement question.
- **The superseded per-plane-language engine traits** (`fn execute(&self, input:
  NexusInput) -> NexusOutput`) were REMOVED from the emitter as the
  dead-scaffolding shape D4 named; the Spirit emission test was updated to the
  new Plane-based shape. If any downstream relied on the old traits, that's an
  integration touch for the operator on main reconciliation.
- **Operator reconciliation of the nota-next pin to main** (record 1057): the
  three repos are aligned to `5e063042` on the feature branches; the operator
  reconciles both pins to main on integration.

## Pushed artifacts

| Repo | Branch | Pushed commit | What |
|---|---|---|---|
| `schema-next` | `collections-horizon-2026-05-28` | `f73274f6` | collections + types-only modules (`signal_plane: Option`) |
| `schema-rust-next` | `collections-horizon-2026-05-28` | `419db039` | collections + `Plane` surface + three-engine chain + types-only emission |
| `horizon-next` | `collections-horizon-2026-05-28` | `1b64d1b` | the concept: types-only core, Plane, running chain, hermetic witness |

Per-repo `INTENT.md` + `ARCHITECTURE.md` updated in all three (record 944).

## See also

- `1-build-and-step-by-step-walkthrough.md` — the verified collections baseline
  this pass builds on (D1).
- `/system-designer/42-horizon-167-intent-divergence-and-fixes.md` — the D1-D4
  divergences; this pass closes D3/D4 and the type-library instance of D2.
- Spirit records: 1054 (Plane enum — implemented), 1052 (kind-tag-beside-envelope
  is wrong — superseded), 1038/1039 (origin route on the root — implemented),
  1028 (three engines), 1030 (components must drive — the running chain), 1057
  (nota-next pin alignment — done across all three repos), 1060 (iterative
  deepening — this pass reached past the prior), 1062 (NEW — the Plane origin-
  route placement clarification captured this session).
