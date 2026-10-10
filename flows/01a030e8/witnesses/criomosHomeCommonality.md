# CriomOS-home common-source audit

Method: code read `/home/li/primary/SKILL_VARIABLES.md`
Method: code read `/home/li/primary/NON_MANAGEMENT_AGENTS.md`
Method: code read `/home/li/primary/.agents/skills/flows/SKILL.md`
Method: code read `/home/li/primary/flows/01a030a1/vision/commonGround.md`
Method: code read `/home/li/primary/flows/01a030a1/reports/commonGroundReacquisition.md`
Method: code read `/home/li/primary/flows/01a02b4b/vision/homeEquivalence.md`
Method: code read `/home/li/primary/flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
Method: code read `/home/li/primary/psyche-raw/Vision/setupIndependentInterfaces.md`
Method: code read `/git/github.com/LiGoldragon/CriomOS-home`
Method: code read `/git/github.com/LiGoldragon/CriomOS`
Method: code read `/git/github.com/LiGoldragon/CriomOS-lib`
Method: code read `/git/github.com/LiGoldragon/horizon-rs`

## Repository identity and status

- Home: `/git/github.com/LiGoldragon/CriomOS-home`; parent `756ce723ea7f1a58d20e2b6f153f15e30aa9b885` (`home: update Codex and Claude CLIs`); working copy `4575c086…`, clean/empty.
- OS: `/git/github.com/LiGoldragon/CriomOS`; parent `93049a6e3eb7f66a23484402c96d835caa233b99` (`checks: align composed Home pin contract`); working copy `75ea5b2c…`, dirty. Dirty paths include `flake.nix`, `modules/nixos/userHomes.nix`, and the agent-intercom command-ownership gate rename. Those paths are current-worktree evidence, not clean authority.
- Existing shared predecessor: `/git/github.com/LiGoldragon/CriomOS-lib`; parent `6e3bcb0808b722c881d9c9b19d684b56b9d65642`; working copy `7c7cad26…`, clean/empty.

The audit used authored Nix sources, manifests where present, architecture/ownership documents, and lock/input declarations. Generated `.agents/`, `.claude/`, `.codex/`, and `.pi/` trees were treated as read-only evidence and were not included as extraction sources.

## Psyche ruling relevant to extraction

`flows/01a030a1/vision/commonGround.md:1-7` says common OS/Home ground belongs in a direct source repository consumed by both. `flows/01a030a1/reports/commonGroundReacquisition.md:105-121` says only the actual intersection moves; OS and Home composition remain local, and OS reaching common material indirectly through a Home construction is wrong. `flows/01a02b4b/vision/homeEquivalence.md:1-20` places shared values in Horizon/extended-Horizon or shared Nix machinery. `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md` is the current request, but the exact core name, schema, and migration authority remain unsettled.

## Observed shared surfaces

### Existing shared library and large-AI data

Home declares `criomos-lib` as a cross-consumed helper/data input (`CriomOS-home/flake.nix:117-125`). Home reads the model catalog in `modules/home/profiles/min/pi-models.nix:17-18,29-32,68-72` and `modules/home/profiles/max/browser-use.nix:53-63`. OS reads the same catalog in `modules/nixos/llm.nix:24-28` and uses its `serverPort` for the system router at `:128-155`. The source is `CriomOS-lib/data/largeAI/llm.json:1-24`; the library describes itself as shared pure helpers/data in `CriomOS-lib/ARCHITECTURE.md:1-18` and exports constants/helpers in `lib/default.nix:17-161`.

This is an actual shared source surface, not duplicated Home/OS code. It is the strongest candidate for `core.data.largeAI`, or for a controlled evolution/rename of `CriomOS-lib`. The existing flat constants object is not uniformly shared: Home uses `constants.fileSystem.home` (`modules/home/base.nix:131-145`, `profiles/min/niri.nix:35-44`), while OS primarily uses network/system values. It should be split by observed ownership before being called core. `mkJsonMerge` is explicitly retired in favor of Hexis (`CriomOS-home/flake.nix:117-125`); other exported helper functions should not be moved without active cross-consumer call-site evidence.

### Duplicated Horizon service decoder

Home repeats the same `serviceName` decoder in:

- `modules/home/profiles/min/default.nix:34-47`
- `modules/home/profiles/min/agent-intercom.nix:11-27`
- `modules/home/profiles/min/orchestrate.nix:17-30`
- `modules/home/profiles/min/spirit.nix:20-33`

`modules/home/vscodium/vscodium/default.nix:18-24` has a related direct predicate. OS centralizes an equivalent helper in `modules/nixos/node-services.nix:13-53`, exposing `has`, `payload`, and nested PersonaDevelopment capability queries; OS consumers include `modules/nixos/agent-intercom.nix:9-13` and `modules/nixos/users.nix:8-11`.

This is the clearest duplicated source-level concept. It is not behavior-identical: Home defaults absent services to `[]` and accepts one-key attrsets; OS validates the collection as a vector and supports payload/nested capability semantics. A core adapter is plausible only after explicit compatibility/schema authority settles malformed and multi-key behavior. Horizon schema/method logic itself remains in `horizon-rs` (`lib/src/proposal.rs:113-187,319-403,591-607`).

### Endpoint and projected-user variables

Home’s Pi and browser modules independently substitute `horizon.node`, `horizon.exNodes`, router/large-AI role predicates, and catalog `serverPort` (`pi-models.nix:29-32,68-72`; `browser-use.nix:56-63`). This shares catalog data and Horizon fields with OS, but the router-first/fallback endpoint selection is currently Home policy; OS’s `llm.nix:140-155` configures the system service from its own node role. It is not yet a cross-repo helper.

Home’s module interface is `horizon`, `user`, and Home `inputs` (`modules/home/default.nix:3-16`); Home maps projected users to standalone configurations (`flake.nix:582-610`). OS supplies those arguments through Home Manager (`modules/nixos/userHomes.nix:1-50`, dirty checkout) and separately owns system-user/SSH/group policy. This is a shared projection contract, not shared implementation. Both write Home Manager state version `26.05` (`CriomOS-home/flake.nix:595-598`; `CriomOS/modules/nixos/userHomes.nix:16`), but that literal has separate authorities and should not enter core.

### Common flake axes

Common input names are independently declared/followed in Home (`flake.nix:4-21,117-125,160-184`) and OS (`CriomOS/flake.nix:4-49,109-132`): nixpkgs, Blueprint, Home Manager, rust-overlay, system, pkgs, horizon, `criomos-lib`, Orchestrate, and Spirit. This is dependency alignment, not a runtime namespace. The lock files currently have divergent nixpkgs revisions (Home `f83fc3…`; OS `b47ad6…`) while many shared inputs match. A core repo should not own consumer package sets, deployment projections, or all input declarations without separate authority.

## False positives and deliberate ownership boundaries

- Home owns desktop/profile/package policy, user Agent Intercom adapters, user Spirit state, themes, Pi/browser configuration, and Home Manager construction (`CriomOS-home/ARCHITECTURE.md:17-51,133-210`; `modules/home/default.nix:32-91`).
- OS owns NixOS users/groups/devices/networking/system services, system Spirit, system llama routing, and Agent Intercom prerequisites (`CriomOS/ARCHITECTURE.md:257-295`; `modules/nixos/agent-intercom.nix:9-14`; `modules/nixos/llm.nix:140-176`).
- Agent Intercom capability names are shared Horizon data, but system prerequisites and user broker/configuration are intentionally separate (`CriomOS/ARCHITECTURE.md:257-287`; `CriomOS-home/ARCHITECTURE.md:169-210`). Only a pure service decoder is a core candidate.
- Spirit’s upstream pin is shared, but Home’s user service and OS’s system daemon have different state/lifecycle owners; do not extract either module.
- Home explicitly has no deployment authority and no Lojix edge (`README.md:7-10,24-27`; `ARCHITECTURE.md:230-241`; `checks/system-projection-boundary/default.nix:1-24`). OS owns deployment/projection/activation (`CriomOS/flake.nix:109-132,233-272`). Core must remain deployment-neutral.
- The dirty OS package-set shortcut (`CriomOS/flake.nix:154-170`) and dirty Home Manager wiring (`modules/nixos/userHomes.nix:33-50`) are integration evidence only, not an approved core end-state.

## Initial namespace hypothesis

The smallest evidence-backed direct surface is:

```text
core.horizon.nodeServices
  serviceName
  servicesList
  has
  payload
  personaDevelopmentHas

core.data.largeAI
  llm.json / parsed catalog
```

Potential `core.json` helpers should wait for confirmed active cross-consumers. Existing `CriomOS-lib` should be evaluated as the likely predecessor before creating a parallel authority. Do not initially include Home construction, OS deployment, package-set selection, secrets, Horizon schema, Home filesystem policy, OS network constants, system/user service modules, or the Home endpoint-selection policy.

## Unknowns requiring authority

- Whether `criomos-core` replaces/renames `CriomOS-lib` or coexists with it.
- Exact namespace names/casing and compatibility policy.
- Whether shared catalog data is core-owned, Horizon-owned, or remains `CriomOS-lib`-owned.
- Whether service decoding adopts Home’s permissive behavior or OS’s strict validation.
- Which shared values originate in Horizon versus core.
- How standalone and embedded Home package-set/activation identity is to converge.
- No psyche approval was found for schema, deployment, activation, or compatibility changes.

## Sources

- Psyche records: `flows/01a030a1/vision/commonGround.md`, `flows/01a030a1/reports/commonGroundReacquisition.md`, `flows/01a02b4b/vision/homeEquivalence.md`, `flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`.
- Witnessed repositories: `/git/github.com/LiGoldragon/CriomOS-home`, `/git/github.com/LiGoldragon/CriomOS`, `/git/github.com/LiGoldragon/CriomOS-lib`, `/git/github.com/LiGoldragon/horizon-rs`.
- Parent flow: `flows/01a030e8`; related OS-side witness: `flows/cc8a92e8/witnesses/criomosCoreAudit.md`.
