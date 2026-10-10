# criomos-core proposal

## Conclusion

`criomos-core` should be the dependency-free successor to `CriomOS-lib`, not a second shared library beside it. CriomOS and CriomOS-home should each depend on it directly. It should own only source whose semantic contract is genuinely shared by both consumers.

The audited intersection is smaller than the visual similarity of the repositories:

1. The one strong duplicated implementation is the pure Nix interpretation of Horizon service variants.
2. The large-AI model catalog is genuine shared source, but is already shared through `CriomOS-lib`.
3. The existing flat `CriomOS-lib.constants` namespace mixes OS-only and Home-only values. Those values are not common merely because they currently sit in a common repository.
4. Package construction, Home embedding, activation, deployment, Horizon schema, consumer modules, shared pins, formatting, and development shells have other owners or distinct semantics.

The terminal shape is therefore a small leaf repository with conceptual namespaces, while all consumers are migrated and `CriomOS-lib` is retired. A parallel `CriomOS-lib` and `criomos-core` would create two authorities for the same responsibility.

## Ground

The living ruled in `01a030a1` that common OS/Home ground belongs in a separate repository used directly by both, because obtaining common machinery through Home is indirection. This flow asks for all such commonality to be sourced from `criomos-core` and exported as namespaces.

The current repositories inspected were:

- CriomOS at `93049a6e3eb7f66a23484402c96d835caa233b99`, with working-copy changes present during audit in its flake, Home embedding, and one gate move;
- CriomOS-home clean at `756ce723ea7f1a58d20e2b6f153f15e30aa9b885`;
- CriomOS-lib clean at `6e3bcb0808b722c881d9c9b19d684b56b9d65642`.

Claims involving the dirty CriomOS paths describe the inspected working copy, not settled architecture. Generated agent trees were excluded. Neither consumer contained an authored DOTOS manifest.

## Commonality map

| Surface | What is shared | Disposition |
|---|---|---|
| Horizon service variants | CriomOS has the full `serviceName` / list / membership / payload implementation; Home repeats reduced name and membership implementations in four profiles. | Move the pure interpretation into `criomos-core.lib.horizon.services`; delete all consumer copies. |
| Large-AI catalog | OS and two Home profiles read the same `CriomOS-lib/data/largeAI/llm.json`. | Move its authored source to Core and export the parsed value as `criomos-core.data.largeAI`. |
| Existing Lib constants | Both depend on Lib, but OS consumes network/security constants while Home consumes `fileSystem.home`. There is no demonstrated cross-consumer value in that flat namespace. `CriomOS-lib/lib/default.nix:88-92` also duplicates the subnet and gateway authored by `criomos-horizon-config/horizon.dotos:7-10`. The audit did not establish that Horizon currently emits those facts. | Split by ownership: OS values to CriomOS, Home values to CriomOS-home. The observed pan-LAN duplicate has an existing configuration owner; moving it into projected Horizon output is a separate unresolved design, not Core work. |
| JSON helpers | `importJSON` has no active shared consumer; `mkJsonMerge` was retired for Hexis; `fetchHfModel` is nixpkgs-dependent and has no active shared consumer. | Do not carry them into Core. Delete or relocate only if a concrete owner still consumes them. |
| Horizon user/node fields | Both consume the emitted Horizon projection. | Shared contract, not shared implementation. Horizon-rs and Horizon configuration retain schema and fact authority. Core may interpret an emitted value but may not redefine it. |
| Agent Intercom capabilities | Both recognize the same Horizon service names. OS owns host prerequisites; Home owns user package, broker, adapters, and desktop setup. | Share only the generic service query. Keep consequences in each consumer; a universal invariant belongs in Horizon validation if later ruled schema-level. |
| Spirit | Both use the upstream component, but OS runs system lifecycle/state and Home runs user lifecycle/state. | Keep both integrations consumer-owned. |
| Home construction and embedding | Both paths must produce equivalent Home, but standalone construction belongs to Home and OS embeds it for selected local users. | Do not move a Home evaluator into Core. That would make Core depend on Home and create a cycle. Core remains a leaf. |
| Package set | Both need aligned packages and overlays. | CriomOS-pkgs owns package instantiation/cache semantics. Core must not depend on nixpkgs or become another package authority. |
| Shared flake inputs and lock revisions | Several pins/follows presently align. | Integration and release policy, not reusable source. Keep in consumer flakes/locks. |
| Large-AI endpoint selection | Router-first/fallback selection is repeated in two Home modules but not in OS. | Home-local refactor, not OS/Home common ground. |
| Home Manager state version | Both currently contain `26.05`, under different Home/NixOS construction sites. | Release policy coincidence; keep consumer-owned. |
| `formatter.nix` | The only exact code-identical authored file found by the cross-repository content hash. | Keep per repository or source from general tooling; formatting is not CriomOS domain source. |
| Development shells | Similar tools, different toolchain and side effects. | Keep per repository. |
| No-Horizon/no-system stubs | Same filenames but deliberately different failure contracts. | Keep per consumer. |
| Documentation, license, generated shims | Similar shape or identical administrative text. | Not Core runtime/source namespaces. Generated trees remain generated evidence. |
| Secrets, deployment, activation, networking, users, desktop | They sometimes consume the same facts but enact different authorities. | Secrets/deployment/network/system users remain OS-owned; desktop/user state remain Home-owned. |

This map separates literal duplication, equivalent behavior, shared data, shared contracts, and coincidental syntax. Only the first three can yield Core source, and only when ownership is neutral.

## Proposed anatomy

### Purpose

`criomos-core` is the setup-independent, dependency-free Nix meaning layer shared by CriomOS and CriomOS-home. It provides pure interpretation and static data. Both consumers call it directly.

### Inputs

- Pure Nix values supplied by a consumer, especially already-emitted Horizon values.
- Authored static data stored in Core itself.

Core has no flake inputs. In particular it has no dependency on nixpkgs, Blueprint, Home Manager, CriomOS-pkgs, horizon-rs, CriomOS, or CriomOS-home.

### Outputs

```nix
inputs.criomos-core.lib.horizon.services = {
  normalize = /* service list -> canonical service records */;
  has = /* service name -> service list -> bool */;
  payload = /* service name -> service list -> payload or null */;
  hasCapability = /* service name -> capability -> service list -> bool */;
};

inputs.criomos-core.data.largeAI = {
  serverPort = /* authored port */;
  models = /* authored model catalog */;
};
```

The public contract is the namespace value, not the internal file layout. The JSON catalog may remain the authored representation, but consumers should stop parsing a repository-relative path independently.

`normalize` should accept only the Horizon-emitted list shape, require every element to be either a string or an exactly-one-key attribute set, and return canonical `{ name; payload; }` records. Invalid or ambiguous values should fail explicitly. The consumers are migrated together; no permissive compatibility branch is proposed.

The existing OS-specific `personaDevelopmentHas` becomes a use of generic `hasCapability` in CriomOS. Core owns the algebra, not the meaning or policy of `PersonaDevelopment`.

### What Core does not do

- It does not materialize or author Horizon.
- It does not select nodes, users, deployments, secrets, or package sets.
- It does not export NixOS modules, Home Manager modules, activation packages, or deployment applications.
- It does not know CriomOS or CriomOS-home as dependencies.
- It does not preserve unused Lib APIs.
- It does not become a bucket for same-looking source.

## Dependency shape

Consumers point toward their authorities; Core points toward none:

```text
CriomOS ────────> criomos-core
       ├────────> CriomOS-pkgs
       ├────────> emitted Horizon
       └────────> CriomOS-home       (embedding only)

CriomOS-home ───> criomos-core
             ├──> CriomOS-pkgs
             └──> emitted Horizon

criomos-core ───> no repository input
```

CriomOS consumes Core's API directly; it never obtains shared values through Home. Embedding still gives CriomOS a transitive dependency through Home to Core, but that path is not the source interface. There is no reverse Core -> Home edge and therefore no Core/Home cycle.

## Migration

1. Create `criomos-core` as the replacement authority for `CriomOS-lib`, carrying forward only the valid shared history/source.
2. Establish the dependency-free flake outputs `lib.horizon.services` and `data.largeAI` with their behavioral checks.
3. Move the large-AI catalog into Core and make all three current consumers use the exported parsed namespace.
4. Move the service normalization/query implementation into Core. Replace the CriomOS helper and all four Home copies in the same migration; express PersonaDevelopment capability lookup through the generic query.
5. Move OS-only constants out of Lib into CriomOS and Home-only filesystem constants into CriomOS-home. Move pan-Horizon facts only after Horizon output ownership is designed and approved.
6. Delete unused `importJSON`, `mkJsonMerge`, and `fetchHfModel` rather than transporting a historical API.
7. Replace the `criomos-lib` input with `criomos-core` in both consumers, update every call site and lock, and remove the old input in the same change series.
8. Retire `CriomOS-lib` once no consumer remains. Do not leave forwarding outputs or a compatibility namespace.
9. Leave the current standalone/embedded Home package-equivalence repair separate. It composes Home and package authorities; it is not Core source.

## Proof required for realization

The implementation round should first witness each new test failing, then expose every durable test as a Nix check.

- Core service checks: strings, one-key payload variants, empty list, membership, payload, nested capability, malformed list, zero/multiple-key variants, and duplicate service-name behavior.
- Core data checks: the authored catalog evaluates to the declared namespace and required model/port fields are valid.
- Consumer checks: CriomOS and Home service-gated modules produce the same results through Core as their intended current behavior on valid Horizon output.
- Repository gates: `nix flake check` for Core, CriomOS, and CriomOS-home.
- Integration gate: the existing standalone-versus-embedded Home activation-equivalence witness remains green after the dependency replacement.
- Absence check through evaluation, not source-text matching: neither consumer evaluation requires `criomos-lib`, and both evaluate with Core as their direct shared dependency.

No product implementation, deployment, or activation is part of this proposal round.

## Rulings before implementation

The evidence supports the proposal but does not supply living-psyche authority for two design choices:

1. Whether `criomos-core` supersedes `CriomOS-lib` completely. This proposal recommends replacement because coexistence creates duplicate authority.
2. Whether the service interpreter is strict at the Nix boundary as proposed, or whether malformed service values must instead be rejected entirely by Horizon-rs before projection.

The repository name and broad direct-dependency shape were requested in this flow. The two choices above define the boundary and failure contract and should be ruled before realization.

## Sources

- `flows/01a030a1/vision/commonGround.md`
- `flows/01a02b4b/vision/homeEquivalence.md`
- `flows/01a030a1/reports/commonGroundReacquisition.md`
- `flows/01a030a1/reports/extendedHorizonReacquisition.md`
- `flows/01a02f74/reports/currentVsVisionMap.md`
- `flows/cc8a92e8/witnesses/criomosCoreAudit.md`
- `flows/01a030eb/witnesses/criomosHomeCommonality.md`
- Remembered flows: `01a030a1`; supporting remembered records from `01a02b4b`, `012fbf07`, and `01a02f74`
