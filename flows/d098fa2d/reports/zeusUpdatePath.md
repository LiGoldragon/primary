# Zeus update path

## Observations

Zeus is the `goldragon/zeus` production node declared in `goldragon/datom.dotos`: an Edge/Max x86_64 ThinkPad T14 Gen2 Intel with no node services. The proposal maps both `bird` and `li` to Zeus home presence. The authored OS source is network-neutral: CriomOS owns `nixosConfigurations.target`, while CriomOS-home owns the Home Manager modules consumed by that target. Lojix projects the proposal into the `horizon`, `system`, `deployment`, and `secrets` inputs.

The current checked-in CriomOS source is `d04f6dafce19b7b4f093c35716739f36d75973ba`; it pins CriomOS-home `1a6e22da155bb75a6362d10623301b13d0c24b34` and Lojix `0d968da44bc0be8ed875b8546bebf52c3de53a81`. The current active daemon on Ouranos is Lojix 0.17.5. Its ordinary query for `goldragon/zeus` returned no generation or deployment record. Zeus generated-input trees exist locally, but their complete-host/full-os projections are dated July and are historical managed output.

## Inference

The current update boundary is a typed owner request, not a host-specific NixOS configuration or setup script. The canonical full-host request shape is:

```text
LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.Host.(goldragon zeus CompleteHost <absolute-datom.dotos> <immutable-CriomOS-flake> (<explicit-nix-store-uri> <explicit-ssh-destination>) Horizon (nixosConfigurations.target.config.system.build.toplevel) NixosSystemdBootV1 <approved-host-action> RequireImmutable <optional-builder> [])'
```

The daemon then validates and records admission, resolves the immutable source, projects Horizon and writes generated flake inputs, evaluates the exact selector, realizes the closure, copies it to the request-owned Nix store URI, performs the requested host activation, and records a terminal deployment/generation result. `ActivateNow` is a live switch; `SetBootProfile` changes the persistent boot profile; `ScheduleBootOnce` installs a target-owned one-shot boot path. A successful admission alone is not completion.

If the intended source is the currently checked-in CriomOS main, its observed immutable candidate is `github:LiGoldragon/CriomOS/d04f6dafce19b7b4f093c35716739f36d75973ba`; selecting it for production remains a caller decision.

## Unknowns and authority gates

The exact Zeus transport pair, optional builder specification, immutable CriomOS revision to deploy, extra substituters, and activation action are not established by the current skill variables or by any Zeus live deployment record. Lojix explicitly forbids deriving transport from cluster/node names. The caller must supply or approve these values. A live switch, boot-profile change, or boot-once scheduling is an activation mutation and remains outside this explanation-only request.

## Sources

- [declaredSources witness](../witnesses/declaredSources.md)
- [zeusSource witness](../witnesses/zeusSource.md)
- [liveState witness](../witnesses/liveState.md)
- [pipeline witness](../witnesses/pipeline.md)
- Current flow: `d098fa2d`
