# ChatGPT corrected-live witness

Method: repaired the canonical Home source and ran its focused remote Nix
syntax check; advanced the CriomOS input to the immutable repair revision and
independently evaluated the user activation package against materialized
Ouranos inputs; then used the witnessed Lojix owner/ordinary socket tuple with
the canonical proposal source. After terminal realization and activation,
inspected the active profile, launched only ChatGPT through its activated
wrapper, and observed its unit, Niri window, journal handshake, and persistent
Codex owner.

## Corrected source and consumer

- CriomOS-home `e5033f327ffca69958163eb09d1114bbab0d9e03` repairs the ASAR
  replacement boundary and exposes a `desktop-app-support` syntax witness. The
  broken fixture failed first with Node's `Unexpected token '}'`; the corrected
  remote-builder check passed.
- CriomOS `50d7d347aead7125101dc7ba3a2240d019fd9cec` advances only its
  canonical `criomos-home` input to that immutable Home revision and locks NAR
  hash `sha256-I0IcuVbXYBY/3KybeT6aD/aSdZMWKAB8Bcwjtrr7VRw=`.
- Independent consumer evaluation of
  `homeConfigurations.li.activationPackage.drvPath`, with the materialized
  Ouranos user-environment inputs, succeeded with
  `/nix/store/sb6pdziwbqh31nvvclngc6cldiryyphm-home-manager-generation.drv`.

## Correction and deployment

The earlier claim that only `.datomic` was canonical and thus deployment was
blocked was false. It overgeneralized this stale historical statement from
`flows/01a05209/log.md`: “Canonical goldragon authority has migrated to
`proposal.datomic`, but deployed Lojix accepts only legacy `.dotos`.” The
current, witnessed canonical source is the regular, non-symlink file
`/git/github.com/LiGoldragon/goldragon/proposal.datom`; flow `01a05c80`
successfully used it for Ouranos user-environment deployments 123 and 124.
The stale incompatible path is `goldragon/datom.dotos`.

Before mutation, hostname was `ouranos`; Lojix queried logical node
`goldragon/ouranos`; and the witnessed transport was
`ssh-ng://li@ouranos.goldragon.criome` to `li@ouranos.goldragon.criome`.

- Owner-socket `Deploy.UserEnvironment` with `Realize` admitted deployment
  140 at marker 3548 and ordinary-socket query recorded terminal
  `Completed`, marker 3564, `Succeeded` for revision `50d7d347…`.
- The matching `ActivateNow` admitted deployment 141 at marker 3569 and
  terminally recorded `Completed`, marker 3602, `Succeeded`.
- The active Home profile is now
  `/nix/store/nsjw787mzy5y97v20dl6kw344jz35bh2-home-manager-generation`.

## Live desktop witness

No old ChatGPT main process or Niri ChatGPT window survived activation, so no
unrelated process was terminated. The activated profile's `bin/chatgpt` wrapper
was started as the single transient user unit `cf0ed9-chatgpt-corrected`.

- Unit is `active/running`, main PID 1603053; Niri window 444 has app id
  `chatgpt` and title `ChatGPT`.
- Its journal records a successful app-server initialize handshake
  (`transportKind=websocket`) followed by the `connected` state. It has no
  `Unexpected token` parse error.
- The persistent Codex owner remained PID 4013983 with unchanged start time
  `Mon Aug 31 21:58:24 2026`; ChatGPT connected through that existing owner.

No safe GUI automation surface is available for creating or resuming user
conversations, so the ChatGPT window is intentionally left open. The one
remaining living product action is: create a harmless new chat, then open and
continue any existing conversation, and confirm both accept input.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home` commit `e5033f327ffca69958163eb09d1114bbab0d9e03`.
- `/git/github.com/LiGoldragon/CriomOS` commit `50d7d347aead7125101dc7ba3a2240d019fd9cec`.
- `/git/github.com/LiGoldragon/goldragon/proposal.datom`.
- `flows/01a05c80/log.md` and `flows/cf0ed9/witnesses/chatgpt-restart.md`.
- Lojix ordinary queries `Query.ByDeployment.(140)` and
  `Query.ByDeployment.(141)`; local user-unit journal and Niri window query.
