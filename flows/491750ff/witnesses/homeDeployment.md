# Ouranos Home deployment

Method: probe `nix eval "github:LiGoldragon/CriomOS-home/0836e4b7e367efe6a81a4fa657e2a2f741f0d801#homeConfigurations" --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/system --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/user-environment/horizon --apply builtins.attrNames --json`.

The projected evaluation returned `["bird","li"]`. Independent activation-package evaluation returned a derivation path. A remote-only Nix build of `homeConfigurations.li.activationPackage` from the same immutable revision completed successfully; Nix reported the configured Prometheus builder for the uncached derivation.

Method: probe `LOJIX_OWNER_SOCKET=/run/lojix/owner.sock meta-lojix 'Deploy.UserEnvironment.(goldragon ouranos li /git/github.com/LiGoldragon/goldragon/datom.dotos github:LiGoldragon/CriomOS-home?rev=0836e4b7e367efe6a81a4fa657e2a2f741f0d801 (ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome) Horizon (homeConfigurations.li.activationPackage) HomeManagerNixProfileV1 ActivateNow RequireImmutable Some.@/etc/nix/machines [])'`.

The corrected request was accepted as deployment 60 at marker `1375`. The first slash-form flake reference was rejected as `FlakeReferenceMalformed` before admission; it produced no deployment mutation. The ordinary query `LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock lojix 'Query.ByNode.(goldragon ouranos None)'` later reported deployment 60 `Current`, source revision `0836e4b7e367efe6a81a4fa657e2a2f741f0d801`, terminal `Completed`, `Some.Succeeded`, and terminal marker `1408`.

Method: probe `ssh -o BatchMode=yes li@ouranos.goldragon.criome 'zsh -lic '\''codex --version; claude --version; readlink -f ~/.nix-profile/bin/codex; readlink -f ~/.nix-profile/bin/claude'\'''`.

The target login shell returned `codex-cli 0.149.1` and `2.1.241 (Claude Code)`, with both executables resolving through the activated Nix profile.
