Subject: Authored Nix and deployment ownership.

Method: code read /git/github.com/LiGoldragon/CriomOS/AGENTS.md

CriomOS is network-neutral and exposes only `nixosConfigurations.target`; cluster and node identity enter through Lojix-projected `horizon`, `system`, and `deployment` inputs. CriomOS-home owns Home Manager modules and CriomOS consumes them.

Method: code read /git/github.com/LiGoldragon/CriomOS/flake.nix

The current main revision is `d04f6dafce19b7b4f093c35716739f36d75973ba`. It pins CriomOS-home to `1a6e22da155bb75a6362d10623301b13d0c24b34`, Lojix to `0d968da44bc0be8ed875b8546bebf52c3de53a81`, and includes the stub `horizon`, `deployment`, `system`, and `secrets` inputs that Lojix overrides per request. `deployment.includeHome = true` is the default.

Method: code read /git/github.com/LiGoldragon/Curriculum/manifests/active-outputs.dotos

The active generated skill manifest includes `lojix`, `operating-system`, `nix-workflow`, `flows`, and `subflows`; `operating-system` depends on `lojix`. These manifests select agent guidance, not Zeus host configuration.

Method: probe `stat -Lc '%F mode=%a owner=%U:%G path=%n' /git/github.com/LiGoldragon/goldragon/datom.dotos`; `test -L /git/github.com/LiGoldragon/goldragon/datom.dotos`

The proposal source is an existing regular non-symlink `.dotos` file, satisfying the current Lojix proposal-source boundary.
