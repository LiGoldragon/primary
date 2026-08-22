# VSCodium runtime audit witness

Method: code read `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`, `claude-lifecycle.sh`, `codium-launch.sh`, `codium-supervisor.sh`, `modules/home/profiles/med/codium.nix`, `modules/home/default.nix`, `packages/vscodium-casual/default.nix`, `packages/claude-code/default.nix`, `checks/vscodium-claude-lifecycle/default.nix`, `checks/vscodium-casual/default.nix`, `checks/agent-intercom/default.nix`, `flake.nix`, and `modules/home/desktop-database.nix`.

Method: code read the current Home Manager activation at the path obtained by `readlink -e /home/li/.local/state/home-manager/gcroots/current-home/activate`; no activation command was run.

Method: probe `readlink -e /home/li/.nix-profile/bin/codium`; `systemctl --user list-unit-files --all`; `systemctl --user list-units --all`; `ps -eo pid=,ppid=,user=,stat=,etime=,args=`; and read-only `stat`, `readlink`, and `sed` of the current Codium state, desktop entry, settings, and generated profile links. No Codium command, process launch, signal, or runtime-state write was performed.

## Observations

- The medium profile imports both the desktop-file module and the managed VSCodium module. The managed package replaces its `bin/codium` entry with the lifecycle launcher; the lifecycle and supervisor retain absolute store-tool dependencies. The desktop file's main `Exec` is an absolute generated opener, but that opener and its `new-empty-window` action invoke bare `codium`.
- The authored activation DAG places bootstrap before `linkGeneration`, replacement after `linkGeneration`, and three nonblocking activation refresh attempts after replacement. The generated activation additionally compares the immutable extension file; on change it removes `extensions.json` and `.init-default-profile-extensions`, then runs the managed `codium --list-extensions` before replacement and refresh.
- The lifecycle validates absolute canonical directories, keeps the lock and GC-root directory as direct children of the state directory, and uses an exclusive `flock` lease for reconciliation. It creates versioned Claude links, Nix automatic roots, and a tab-separated manifest. Registry updates use temporary files and renames; manifest updates do not call `sync`.
- The launcher classifies several CLI flags as terminal/state-management modes, but every invocation first creates or opens the lifecycle state and calls `--prepare-launch`. It then downgrades the descriptor to a shared lease. GUI/file modes use a session directory and a same-cgroup foreground supervisor; terminal modes invoke the underlying Codium CLI synchronously.
- The supervisor forwards HUP/INT/TERM and cleans its session after the child exits. There is no parent-death signal or equivalent kill-on-supervisor-loss mechanism. A SIGKILL of the supervisor can therefore leave a child and session state without the shared lease.
- Current read-only process inspection found a long-running underlying Codium process in a transient `app-codium-*.scope`, not a `criomos-codium-supervisor` process. No Codium-specific systemd user service was listed. The current managed manifest, immutable registry snapshot, versioned Claude links, and user GC root agree on the declared Claude version; a retained recovery directory still contains stale Session Storage/`LOCK` state (recorded by the prior witness).
- The merged current VSCodium settings preserve user-owned keys beyond the declaration. The observed settings contain Claude permission-bypass keys while the authored declaration only supplies the declared settings map; this is an observed state, not evidence of who set those keys or whether they are authorized.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-casual/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `flows/01a02b4d/witnesses/managedExtensionState.md`
