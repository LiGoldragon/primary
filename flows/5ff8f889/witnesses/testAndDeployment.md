# Home test and deployment conventions

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`,
`/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`,
`/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-local/default.nix`,
`/git/github.com/LiGoldragon/CriomOS-home/checks/aggregator-deployment/default.nix`,
`/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix`,
and `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-dotos-config/default.nix`.

Home registers durable checks in `outputs.checks`, mapping each system to
`pkgs.callPackage ./checks/<name>`. Existing checks combine Home Manager
evaluation assertions with `pkgs.runCommand` witnesses. The most realistic
local examples materialize generated service fields, execute generated
startup/configuration wrappers against temporary HOME/XDG directories, launch
packaged binaries, and inspect protocol replies. The Chroma config check is a
generated-output assertion; several older checks still use source greps, but a
new adapter witness should run the machinery.

The accepted e2e witness should therefore be a new check directory, likely
`checks/chroma-emacs-isolated-daemon/`, registered in `flake.nix`. It should
evaluate the relevant Home module, use the generated Ignis theme directory and
the exact Emacs package that Home configures, then run the built Chroma daemon
and an isolated Emacs daemon inside a private D-Bus/XDG environment. A concise
behavioral sequence is:

1. Create private HOME, XDG config/state/runtime, and D-Bus session paths.
2. Materialize Home's generated `ignis-dark` and `ignis-light` files into the
   isolated HOME and load the Home-generated init/early-init.
3. Start the real Chroma package with a minimal manual-theme config and the
   required fake native peers (the existing Chroma sandbox supplies gamma and
   Ghostty patterns). Start Emacs as a daemon after Chroma to exercise late
   registration.
4. Observe the Chroma consumer-status signal for `Applied` at a revision, then
   query Emacs for `custom-enabled-themes` and a representative face. Drive
   Light and Dark and assert the expected Ignis symbol and rendered foreground.
5. Load a temporary unrelated overlay theme and assert both overlay retention
   and exactly one Chroma-owned theme after each transition.
6. Restart or replace the Chroma bus owner while Emacs remains alive, wait for a
   fresh `Applied` acknowledgement, and assert reconciliation from the latest
   desired revision.

The exact D-Bus name, interface, registration method, status signal, revision
query, and typed failure form are not present in current Chroma and must come
from the Chroma slice-2 implementation. The Home check must subscribe to the
acknowledgement event rather than sleep for a guessed duration. Plugin fake-peer
ERT/isolated-daemon checks own the complete protocol edge matrix; Home owns
this real built-Chroma/generated-theme/isolated-Emacs witness.

Method: code read `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`,
`/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`,
`/git/github.com/LiGoldragon/CriomOS/flake.nix`,
`/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`, and
`/git/github.com/LiGoldragon/CriomOS/reports/0038-lojix-local-config-and-home-deploy-design.md`.

CriomOS owns deployment and embeds Home Manager through
`inputs.criomos-home.homeModules.default`. It exports an independent Home
projection only for comparison; a deployment must consume the activation
package embedded in `nixosConfigurations.target`. Deployment requests own the
exact source revision, store URI, SSH destination, input mode, output selector,
backend, and builder. The OS rules require updating and locking the Home input
before a full deployment, then obtaining the materialized Horizon/system/
deployment/secrets inputs from the deployment request. Evaluation, realized
closure, selected generation, running service state, and boot persistence are
separate witnesses.

Home-only activation is a live overlay: boot-time NixOS Home Manager can
relink files from the Home revision pinned in the system generation. Durable
deployment observations therefore require a full system generation containing
the new Home pin. No build, activation, deployment, or live observation was
performed in this reconnaissance.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-local/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/aggregator-deployment/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/spirit-deployment/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-dotos-config/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/AGENTS.md`
- `/git/github.com/LiGoldragon/CriomOS/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`
- `/git/github.com/LiGoldragon/CriomOS/reports/0038-lojix-local-config-and-home-deploy-design.md`
- Flow `5ff8f889`
