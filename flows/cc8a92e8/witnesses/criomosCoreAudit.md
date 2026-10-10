# CriomOS/CriomOS-home common-source audit

Method: code read `/home/li/primary/SKILL_VARIABLES.md`
Method: code read `/home/li/primary/NON_MANAGEMENT_AGENTS.md`
Method: code read `/home/li/primary/.agents/skills/flows/SKILL.md`
Method: code read `/home/li/primary/flows/01a030e8/vision/commonalityBetweenTheOsAndHomeRepos.md`
Method: code read `/home/li/primary/flows/01a030a1/vision/commonGround.md`
Method: code read `/home/li/primary/flows/012fbf07/vision/threeStacks.md`
Method: code read `/home/li/primary/psyche-raw/Vision/everyConceptShouldHaveItsRepo.md`
Method: code read `/home/li/primary/psyche-raw/Vision/domainKnowledgePlacement.md`
Method: code read `/git/github.com/LiGoldragon/CriomOS`
Method: code read `/git/github.com/LiGoldragon/CriomOS-home`
Method: code read `/git/github.com/LiGoldragon/CriomOS-lib`

## Repository identity and status

- OS path: `/git/github.com/LiGoldragon/CriomOS`. Parent revision `93049a6e` (`main`, `checks: align composed Home pin contract`); working copy revision `75ea5b2c` is undescribed and dirty: `flake.nix` modified, `modules/nixos/userHomes.nix` modified, and `checks/agent-intercom-command-ownership/default.nix` renamed to `gates/agent-intercom-command-ownership.nix`.
- Home path: `/git/github.com/LiGoldragon/CriomOS-home`. Parent revision `756ce723` (`main`, `home: update Codex and Claude CLIs`); working copy `4575c086` is empty/undescribed and clean.
- Existing shared predecessor: `/git/github.com/LiGoldragon/CriomOS-lib`. Parent revision `6e3bcb08` (`main`, `docs: mark Protos estate status`); working copy `7c7cad26` is empty/undescribed and clean.
- Authored-source scope was used. No `.dotos` manifests were found in OS or Home. Generated `.agents/`, `.claude/`, `.codex/`, and `.pi/` trees were treated as read-only evidence and excluded from the inventory.

## Psyche context

The latest relevant written psyche ruling is `flows/01a030a1/vision/commonGround.md:1-7`: shared OS/Home ground belongs in a separate source repository consumed directly by both; indirection through one consumer is bad design. The older `flows/012fbf07/vision/threeStacks.md:36-49` encourages reusable shared libraries but cautions against arbitrary `core-*` splitting. `psyche-raw/Vision/everyConceptShouldHaveItsRepo.md:1-16` and `domainKnowledgePlacement.md:3-22` support a concept-owned repository and retaining domain knowledge with its domain.

## Observed shared surfaces

### Existing shared library and data

`CriomOS-lib/AGENTS.md:3-29` defines a tiny dependency-free shared helper/data repo, with `lib/default.nix` and `data/largeAI/llm.json`; `ARCHITECTURE.md:3-18` excludes nixpkgs, cluster, node, user, network, and secret truth. Its flake exports `lib` (`flake.nix:1-6`).

Both consumers read the same model catalog:

- OS: `CriomOS/modules/nixos/llm.nix:20-25` reads `inputs.criomos-lib + "/data/largeAI/llm.json"`.
- Home Pi profile: `CriomOS-home/modules/home/profiles/min/pi-models.nix:11-18,59-86` parses and maps the same file.
- Home browser profile: `CriomOS-home/modules/home/profiles/max/browser-use.nix:53-64` parses the same file and derives its endpoint port.
- Catalog contents include the shared server port and models (`CriomOS-lib/data/largeAI/llm.json:1-24`).

The existing `constants` surface (`CriomOS-lib/lib/default.nix:25-111`) is not uniformly shared. OS consumes network/security paths and ports (`CriomOS/modules/nixos/network/headscale.nix:13-17`, `network/dnsmasq.nix:22`, `network/yggdrasil.nix:11,18`, `router/wifi-pki.nix:10`); Home consumes only `fileSystem.home` (`CriomOS-home/modules/home/base.nix:131-135`, `profiles/min/niri.nix:35-44`). This is one flat object containing separate ownership domains.

`importJSON` (`CriomOS-lib/lib/default.nix:129-132`) has no active OS/Home use found. `mkJsonMerge` (`:133-161`) is retired in favor of Hexis, as recorded by `CriomOS-home/flake.nix:117-124`. `fetchHfModel` (`:113-127`) requires nixpkgs and has no active shared consumer.

### Duplicated Horizon service-variant decoder

OS centralizes `serviceName`, `servicePayload`, `servicesList`, `has`, `payload`, and `personaDevelopmentHas` in `CriomOS/modules/nixos/node-services.nix:13-53`; the helper is used by system modules including `agent-intercom.nix:9-13`, `network/headscale.nix:14-16`, `persona-router.nix:25-28`, and `users.nix:8-24`.

Home repeats the `serviceName` implementation in:

- `CriomOS-home/modules/home/profiles/min/default.nix:34-47`
- `profiles/min/orchestrate.nix:17-30`
- `profiles/min/spirit.nix:20-33`
- `profiles/min/agent-intercom.nix:11-27`

Home VSCodium has a related but looser capability predicate (`modules/home/vscodium/vscodium/default.nix:18-24`). OS requires exactly one attrset key; the VSCodium predicate accepts an attrset containing a key. A core helper is plausible, but the Horizon schema authority must settle malformed/multi-key semantics before extraction.

### Common flake axes, not core source

OS declares common inputs and follows (`CriomOS/flake.nix:4-50`); Home declares the common axes independently (`CriomOS-home/flake.nix:4-23,117-125`). Common names include nixpkgs, Blueprint, rust-overlay, Home Manager, system, pkgs, horizon, criomos-lib, Spirit, and Orchestrate. Matching lock revisions are dependency alignment, not source-level commonality. A core repo should remain dependency-free and should not own nixpkgs, Blueprint, package sets, deployment, or Horizon projection.

## False positives and deliberate divergence

- OS → Home integration remains consumer-owned: `CriomOS/flake.nix:35-50,233-272` and `modules/nixos/userHomes.nix:35-49` consume Home modules/package outputs. Home must not become the indirect source of core material.
- OS filters node-local homes by `user.hasPubKey` (`CriomOS/modules/nixos/userHomes.nix:19-29`); Home standalone maps all projected users (`CriomOS-home/flake.nix:582-609`).
- System users, groups, SSH keys, linger, and device prerequisites are OS-owned (`CriomOS/modules/nixos/users.nix:22-50`); profile selection and user packages are Home-owned (`CriomOS-home/AGENTS.md:5-20`, `ARCHITECTURE.md:17-51`).
- Deployment and activation authority is OS-owned (`CriomOS/AGENTS.md:13-16,27-41`, `ARCHITECTURE.md:189-219`); Home explicitly has no deployment authority (`CriomOS-home/README.md:7-10,24-27`).
- OS missing-Horizon stub fails closed (`CriomOS/stubs/no-horizon/flake.nix:1-18`); Home’s standalone stub returns empty users (`CriomOS-home/stubs/no-horizon/flake.nix:1-6`). Their system stubs also intentionally differ (`CriomOS/stubs/no-system/flake.nix:1-21`, `CriomOS-home/stubs/no-system/flake.nix:1-9`).
- Both set Home Manager state version `26.05` (`CriomOS/modules/nixos/userHomes.nix:12-17`, `CriomOS-home/flake.nix:582-598`), but this is release policy, not presently a core API.
- Identical `formatter.nix`, similar `devshell.nix`, shared documentation filenames, LICENSE, and roadmap shape are repository surfaces, not neutral runtime namespaces. Their contents encode distinct ownership.
- Horizon fields (`node.name`, `node.behavesAs`, `node.services`, `horizon.users`, `user.size`) are externally projected schema. Core may provide a pure adapter, but must not duplicate Horizon schema or method computation.
- OS/Home Agent Intercom modules share capability names but own different prerequisites and user/system behavior (`CriomOS/modules/nixos/agent-intercom.nix:9-40`; `CriomOS-home/modules/home/profiles/min/agent-intercom.nix:11-35`). Only the representation decoder is a core candidate.
- OS system LLM service (`CriomOS/modules/nixos/llm.nix:20-40`) and Home Pi/browser configuration are different consumers of the shared catalog, not one shared service implementation. Secrets and authentication remain local.

## Initial core namespace hypothesis

The smallest justified direct surface is:

```text
core.horizon.nodeServices
  serviceName
  servicesList
  has
  payload
  personaDevelopmentHas

core.data.largeAI
  llm.json (or a narrowly documented parsed catalog)
```

`core.json.importJSON` should be added only if a second real consumer appears. `mkJsonMerge`, `fetchHfModel`, OS network constants, Home filesystem constants, deployment/package-set logic, user-selection logic, secrets, and Horizon schema should remain out of the initial core.

Whether `criomos-core` is a rename/evolution of `CriomOS-lib` or a replacement is unresolved. Creating both without a coordinated migration would create competing shared authorities. The current dirty OS package-set change (`CriomOS/flake.nix:155-160`) is activation-identity integration evidence, not a core extraction decision.

## Handoff status

This witness is read-only evidence for parent flow `01a030e8`. No OS/Home/lib product file, authored manifest, generated tree, commit, push, deployment, or activation was changed.
