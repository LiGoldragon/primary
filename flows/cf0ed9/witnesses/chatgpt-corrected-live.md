# ChatGPT corrected-live witness

Method: read the corrected Home source and focused remote Nix check result;
updated and pushed CriomOS's immutable Home input; independently evaluated the
consumer against the materialized Ouranos user-environment inputs; queried the
ordinary Lojix node record; and inspected the declared proposal-source boundary.
No Lojix deployment, Home activation, ChatGPT replacement, or persistent Codex
owner mutation was performed after the deployment boundary proved unavailable.

## Corrected source and consumer

- CriomOS-home `e5033f327ffca69958163eb09d1114bbab0d9e03` repairs the ASAR
  replacement boundary and exposes a `desktop-app-support` syntax witness. The
  broken fixture first failed with Node's `Unexpected token '}'`; the corrected
  focused remote-builder check passed.
- CriomOS `50d7d347aead` advances only its canonical `criomos-home` input to
  that immutable Home revision and records NAR hash
  `sha256-I0IcuVbXYBY/3KybeT6aD/aSdZMWKAB8Bcwjtrr7VRw=`.
- Independent consumer evaluation used the materialized Ouranos user-environment
  `system`, `horizon`, `secrets`, and deployment inputs for
  `homeConfigurations.li.activationPackage.drvPath`. It remained active at the
  close of this witness; its observed output contained only input-override and
  existing deprecation warnings, not an evaluation error.

## Declared deployment boundary

`Query.ByNode.(goldragon ouranos None)` reports the current user-environment
generation as deployment 139, source revision `8dc7c010...`; logical node is
`goldragon/ouranos`. The declared user transport is
`ssh-ng://li@ouranos.goldragon.criome` to `li@ouranos.goldragon.criome`, which
identifies the same Ouranos node.

No deployment was admitted. The active Lojix deployment service accepts a
regular legacy `.dotos` cluster proposal, while Goldragon's canonical proposal
has migrated to `.datomic`; the former `goldragon/datom.dotos` is absent. Flow
`01a05209` records the same active-Lojix incompatibility and absence of a valid
Ouranos proposal source. Creating a legacy duplicate or changing Lojix's
proposal format would be a compatibility/deployment change outside this repair.

Consequently no corrected Home generation was activated and no ChatGPT process
was restarted. The persistent Codex owner and the existing parse-error Desktop
process were deliberately left untouched.

## Remaining action

The single required next authorization is a supported Lojix/Goldragon proposal
format path for the active service. After that exists, submit the immutable
CriomOS `50d7d347...` user-environment deployment, observe its terminal state,
then gracefully replace only ChatGPT and perform one new chat plus one existing
conversation resume.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home` commit `e5033f327ffca69958163eb09d1114bbab0d9e03`.
- `/git/github.com/LiGoldragon/CriomOS` commit `50d7d347aead`.
- `flows/cf0ed9/witnesses/chatgpt-restart.md`.
- `flows/01a05209/log.md`.
- ordinary Lojix `Query.ByNode.(goldragon ouranos None)` observation.
