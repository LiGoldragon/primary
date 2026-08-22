# VSCodium code audit

This is the complete read-only code audit requested for the CriomOS-home VSCodium surface. It reads `/git/github.com/LiGoldragon/CriomOS-home` and its external CriomOS consumer pin; it does not change that repository, build it, activate it, launch Codium, or mutate runtime state. The current runtime observations and the prior repair claim are carried separately from source-confirmed properties below.

## Architecture and import map

```text
CriomOS consumer
  └─ pins CriomOS-home as a separate flake revision
       └─ flake.nix inputs and outputs
            ├─ pkgs.vscodium + pkgs.open-vsx + raw locked VSIX inputs
            ├─ packages/vscodium-casual
            ├─ modules/home/default.nix
            │    ├─ profiles/med/codium.nix (desktop entry/opener)
            │    └─ vscodium/vscodium (package, extensions, settings, activation)
            ├─ packages/claude-code and optional Agent Intercom packages
            └─ checks/vscodium-casual, vscodium-claude-lifecycle, agent-intercom

modules/home/vscodium/vscodium/default.nix
  ├─ casual Codium package → managed package → bin/codium launcher
  ├─ Claude/VisualJJ/ChatGPT VSIX derivations
  ├─ lifecycle reconciler → mutable links, Nix roots, manifest, registry
  └─ launcher → supervisor → direct Codium child
```

`modules/home/default.nix:32-90` is the Home aggregate. It imports the medium profile and explicitly imports both `./profiles/med/codium.nix` and `./vscodium/vscodium`. Its comment at lines 14-16 names `vscodium-ext`, but no such current input or argument is declared there; this is documentation drift, not a live dependency.

The VSCodium module is conditional on `user.size.medium` (`modules/home/vscodium/vscodium/default.nix:244-245`). It receives `pkgs`, `inputs`, `user`, `horizon`, `hexis`, and `textScale`; the Horizon projection only selects whether the direct Claude/Codex CLI packages are added beside the optional Agent Intercom runtime (`:15-24`, `:322-331`). The medium desktop module and VSCodium module are independent imports, so the desktop opener reaches the managed command through the profile PATH rather than through a direct Nix package reference.

## Complete owned source inventory

### Configuration and profile composition

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix:32-90` imports the medium Codium desktop profile and the managed VSCodium module.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:186-242` declares Codium settings: VisualJJ SCM placement, no automatic extension updates, telemetry/update suppression, language-server disabling, terminal/editor behavior, and `textScale.codiumZoom`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:247-267` enables `programs.vscodium`, supplies the managed package, and declares VisualJJ, Claude, ChatGPT/Codex, Pi, direnv, Nix IDE, Markdown, and Mermaid extensions.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:270-314` makes `EDITOR`, `VISUAL`, and text/source MIME defaults conditional on `user.preferredEditor == "Codium"`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:352-356` delegates settings merging to Hexis at `$HOME/.config/VSCodium/User/settings.json`; this is an ensure/deep-merge boundary, so undeclared user keys survive.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix:182-198` disables Stylix's generic `vscodium` target while the module owns Codium settings.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/text-scale.nix:15-28` is the shared text-size source for Codium zoom.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix:749-818,874-881` is the symmetric preferred-editor owner: Emacs may own editor variables and MIME defaults when selected, leaving Codium installed as an auxiliary editor.

### Packages and extension construction

- `/git/github.com/LiGoldragon/CriomOS-home/packages/vscodium-casual/default.nix:6-46` wraps `pkgs.vscodium` with six `--disable-extension` flags for language/helper services while retaining Markdown preview.
- `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix:1-5` delegates the Claude CLI to `inputs.llm-agents.packages.<system>.claude-code`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:15-97` forms the runtime closure and replaces the casual package's `bin/codium` with `criomos-codium-launch`.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:99-117` turns file inputs into `.vsix`-named derivations and consumes `pkgs.open-vsx` from the CriomOS-pkgs overlay context.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:119-142` builds VisualJJ `0.28.1` from the raw locked input and patches its native `jj` ELF interpreter/RPATH.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:144-168` builds Claude `2.1.235` from the raw locked VSIX and replaces its generic Linux native binary with the pinned Nix Claude executable.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:170-182` builds ChatGPT/Codex sidebar `26.5814.41407` from its own raw locked VSIX rather than the Open VSX catalogue.
- `/git/github.com/LiGoldragon/CriomOS-home/packages/agent-intercom/default.nix:91-182` and `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix:23-95` provide optional local Agent Intercom bridges and direct raw CLIs. They are adjacent authority, not the VSCodium extension's command path: the VSCodium module explicitly embeds `claudeCodePackage` (`:161-166`) and the Agent Intercom check asserts no Intercom Claude path (`checks/agent-intercom/default.nix:189-190`).

### Activation

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:333-350` declares bootstrap before `linkGeneration`, mutable-link replacement after it, then three nonblocking `--activation-refresh` calls after replacement.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/desktop-database.nix:19-24` refreshes the user MIME database after `linkGeneration`; it is not Codium-specific, but it determines when the generated desktop entry becomes discoverable.
- The generated activation was read in `flows/01a02b4d/witnesses/vscodiumRuntimeAudit.md`: when the immutable extension declaration changes, it removes mutable `extensions.json`, calls managed `codium --list-extensions`, and then runs the lifecycle replacement/refresh path. That generated behavior is a witness claim, not a second authored source owner.

### Lifecycle reconciler

`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh` owns the user mutable state:

- `:5-25` validates absolute canonical paths and direct-child boundaries.
- `:26-78` selects extension, state, GC-root, and lock paths, then validates the substituted `nix-store` and Codium executables.
- `:79-126` defines dry-run mutation, Nix root registration, and store-target checks.
- `:99-108` accepts SemVer-like versions and exact Claude link-name shape, but does not itself inspect package identity.
- `:133-183` identifies and replaces stale managed roots.
- `:185-221` validates the tab-separated manifest and allows a narrowly recognized legacy indirection.
- `:224-265` provides package identity checks for Claude targets and strict immutable-declaration symlink/store checks.
- `:267-325` authenticates and repairs the captured contradictory three-version state.
- `:327-386` scans a complete manifest into a repair plan before performing root/link repairs.
- `:388-408` removes only prior manifest entries that still pass its ownership checks.
- `:410-418` derives the current managed target from the stable Claude link and its package version.
- `:420-592` validates, seeds, refreshes, backs up, transforms, and atomically replaces the mutable extension registry; registry and owner-state files use temporary files plus `sync`/rename.
- `:595-613` defines launch readiness and bounded preparation.
- `:615-632` performs nonblocking activation refresh under an exclusive lease.
- `:634-727` acquires the exclusive lease, handles bootstrap/migration/repair, writes the manifest, and cleans prior owned entries.
- `:729-734` dispatches activation refresh, launch preparation, registry refresh, and default reconciliation.

The managed state tuple is the stable link `anthropic.claude-code`, the versioned extension link, a matching automatic Nix GC root under the state directory, a tab-separated `manifest`, Home Manager's immutable extension declaration, Codium's mutable `extensions.json`, and the copied immutable registry witness. The lifecycle lock is an advisory `flock` on the state directory's direct child.

### Launch runtime

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:1-49` validates state/lock paths and notification dependencies.
- `:51-84` classifies terminal/state-management flags, acquires EX or SH, prepares lifecycle state, and runs terminal Codium modes synchronously with their output/status.
- `:86-117` creates a session, starts the supervisor, waits for authenticated `ready`, writes `consumed`, releases the launcher's descriptor, and returns without waiting for the GUI.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh:1-48` validates the session and direct runtime executable.
- `:49-99` writes `started`/`ready`/`status`, runs the direct Codium child in the inherited process/cgroup/cwd/environment, forwards HUP/INT/TERM, and cleans the session.
- There is no authored Codium-specific systemd service. The prior runtime witness found the GUI in a transient user-manager app scope rather than a `criomos-codium-supervisor` service.

### Desktop integration

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix:11-83` normalizes file URLs, whitespace, relative paths, and line/column suffixes, then invokes bare `codium`, adding `--goto` when a position is present. Relative paths are resolved against `$HOME/primary` (`:51-56`).
- `:85-117` writes a user-local `codium.desktop` entry with MIME declarations, an absolute generated opener for ordinary file opens, and a bare `codium --new-window` desktop action.
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:280-314` selects the same desktop ID as the preferred MIME application when Codium is selected.

### Tests and checks

- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-casual/default.nix:1-22` checks wrapper text and selected source settings with `grep`. It is a change detector, not a behavior witness.
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:1-276` evaluates the Home Manager module, package identity, locked VSIX manifest versions, and activation ordering.
- Its runtime derivation `:277-1210` uses a fake Codium and fake Nix-store root, then exercises path rejection, unprivileged roots, bootstrap, missing roots, legacy indirection, registry migration, stale-root replacement, contradictory recovery, collision preservation, leases, same-cgroup launch, CLI status/exit forwarding, registry rollback, malformed manifests, and ordinary signal cleanup.
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:859-919` is the exact home-22f three-version fixture. It creates a current immutable/stable declaration, an obsolete direct link, an obsolete root targeting a third output, and a one-row manifest; it then expects the current link/root and manifest while preserving unmanaged extension data and settings and avoiding a GUI launch.
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom/default.nix:84-116,117-225` checks the optional Agent Intercom package/profile and explicitly verifies the VSCodium Claude binary is the direct pinned package rather than an Intercom wrapper.
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:541-544,554-565` exposes these checks. No check runs a real VSCodium GUI, real extension host, or real Home Manager activation.

### Pins and external dependencies

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:43-92` pins the raw VisualJJ `0.28.1`, Claude `2.1.235`, and ChatGPT/Codex `26.5814.41407` VSIX files. Its comments define the update authorities: VisualJJ/Claude use raw file inputs to avoid the unfree catalogue gate; Codex's sidebar advances with `codex-cli`, not Open VSX catalogue refresh.
- `:120-136` pins Hexis, `llm-agents`, and `codex-cli`; `:149-153` pins Spirit, which is not a VSCodium runtime owner.
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:463-505` records the raw VSIX hashes and the locked Codex CLI revision; the root input map at `:2289-2350` includes these inputs and `visualjj-vsix`.
- The VSCodium derivations rely on `pkgs.vscodium`, the `pkgs.open-vsx` overlay from CriomOS-pkgs, `vscode-utils.buildVscodeMarketplaceExtension`, Home Manager's VSCodium module, Hexis, the pinned Claude package, `nix-store`, `flock`, `pgrep`, and absolute shell utilities.
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49` pins the consumed CriomOS-home to revision `1a6e22da155bb75a6362d10623301b13d0c24b34`; `/git/github.com/LiGoldragon/CriomOS/flake.lock:882-994` records that same lock. This is an external deployment boundary, not a path owned by CriomOS-home.

## End-to-end activation sequence

1. Flake evaluation builds the medium-only managed VSCodium package, extensions, runtime scripts, direct Claude/Codex packages, and checks. `programs.vscodium.package` is the managed symlink-join, whose generated `bin/codium` executes the launcher (`default.nix:82-97`).
2. Home Manager imports the aggregate and materializes its immutable extension profile and stable extension links during `linkGeneration` (`modules/home/default.nix:76-90`, `vscodium/default.nix:247-267`).
3. The `bootstrapMutableClaudeCodeExtension` hook runs before `linkGeneration` and only bootstraps conservative legacy state (`vscodium/default.nix:333-335`, lifecycle `:654-683`). If no manifest exists while Codium is running, it exits without discovery mutation (`lifecycle:654-663`).
4. The post-link `replaceMutableClaudeCodeExtension` hook runs `--activate` (`default.nix:337-339`). The lifecycle takes a nonblocking EX lease, authenticates the stable Claude target/version, repairs a manifest/root/link or the recognized contradictory state, writes the current versioned link/root and manifest, and cleans only authenticated prior entries (`lifecycle:634-727`).
5. Three identical post-replacement `--activation-refresh` calls run (`default.nix:344-350`). Each tries a nonblocking EX lease; if a GUI SH lease is held it returns success without waiting. If it obtains EX, it rechecks readiness and refreshes Codium's mutable registry (`lifecycle:615-632`). The source gives no reason for the count of three.
6. Hexis merges declared settings after its own activation ordering (`default.nix:352-356`). The generated activation witness records an immutable-change path that removes/rebuilds Codium's registry before lifecycle refresh; this is generated behavior, not a separate authored module.
7. `updateUserDesktopDatabase` refreshes the user's MIME cache after `linkGeneration` (`desktop-database.nix:19-24`). The deployed system consequently exposes a local desktop entry whose ordinary opener points at bare `codium`.

## End-to-end launch sequence

1. A shell, desktop opener, or MIME action resolves bare `codium` through the user's profile. The managed package's replacement `bin/codium` invokes `criomos-codium-launch` (`vscodium/default.nix:82-97`). The desktop action itself is bare and therefore depends on the desktop environment's PATH (`profiles/med/codium.nix:97-117`).
2. The launcher validates `HOME`/XDG state, state and lock canonicality, and its substituted Codium/notification executables (`codium-launch.sh:1-49`).
3. It marks terminal/state-management flags. Every invocation still creates/opens the state and runs `--prepare-launch` under EX when possible (`:51-84`), so `--help`, `--version`, `--status`, and registry-management CLI calls are not purely read-only.
4. A live supervisor can instead lend the launcher SH; any other lock holder causes a zero-exit “launch deferred” path (`:65-78`).
5. Terminal modes synchronously execute the underlying Codium and return its exact status (`:79-84`). GUI/file modes create a validated session directory, start the supervisor, wait for `token ready`, publish `consumed`, close their own descriptor, and return (`:86-117`).
6. The supervisor retains the SH lease inherited from its launch context, writes handshake/status files, starts the direct Codium child without a manager or `setsid`, forwards HUP/INT/TERM, waits for the child, and removes the session (`codium-supervisor.sh:49-99`).
7. File openings from the desktop wrapper are decoded and normalized first; paths with line/column use `--goto`, while URLs/unresolved arguments are passed through (`profiles/med/codium.nix:17-83`).

## Acceptance assessment for home-22f

The focused acceptance is substantially covered but not complete.

The source contains the intended three-version regression fixture at `checks/vscodium-claude-lifecycle/default.nix:859-919`: current declared Claude `2.1.226`, obsolete versioned link `2.1.223`, and root retaining a separate `2.1.220` output. The fixture authenticates the current immutable/stable tuple, creates the current link/root, writes a sole current manifest, removes only the obsolete authenticated link/root, preserves an unmanaged extension record and settings, refreshes the registry, and starts no GUI. The preceding flow report says the lifecycle check exited 0 with a three-version fixture, repeat/idempotence, and unmanaged-state preservation (`flows/01a02356/reports/managedExtensionContradiction.md`); this code audit did not rerun that check.

The acceptance does not establish broad lifecycle safety. The fail-closed lookalike tests at `:752-814` cover wrong roots, foreign package identity, non-store immutable declarations, foreign immutable symlinks, and malformed later manifest rows, but the normal path still has identity gaps below. The fixture uses fake Codium and fake Nix-root boundaries (`:31-129`) and ordinary signals only; it cannot prove real VSCodium registry behavior, extension-host safety, supervisor-SIGKILL handling, process provenance, or consumer deployment of this repository revision.

The external deployment pin is also separate: CriomOS consumes Home revision `1a6e22da`, while the inspected source's local parent is `9d2896c7`. Therefore “accepted in this source” and “present in the deployed Home closure” are different propositions until the consumer pin is advanced and witnessed.

## Ranked findings

### P1 — A semver-valid foreign GC root can be deleted during stale-root replacement

`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:133-154` authenticates a stale root by canonical `/nix/store` output and a semver-valid `.version` that differs from the current version. It does not require `publisher == Anthropic`, `name == claude-code`, or correspondence to the manifest target before `replace_stale_managed_root` moves the root aside and later removes the backup (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:156-183`). A foreign semver-valid package at the managed root filename can therefore be treated as lifecycle-owned and deleted. The check's adversarial identity case covers contradictory recovery (`/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:764-774`), not this normal stale-root predicate.

### P1 — Normal managed-target and manifest validation do not universally authenticate Claude identity

`managed_extension` only reads a valid semver and canonical store target from the stable link (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:410-418`). `manifest_is_valid` checks grammar, link names, target paths, and root retention (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:196-221`), but `valid_manifest_entry` itself does not inspect package publisher/name (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:99-108`). Identity checks exist in selected recovery paths (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:224-265,294-303`) rather than as a universal invariant. The normal lifecycle can therefore accept a lookalike store target when no stricter branch is reached, weakening the stated Anthropic/Claude ownership boundary.

### P1 — Existing/raw Codium processes can coexist with lifecycle mutation

The EX/SH lease is held by the managed launcher/supervisor (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:65-78`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh:78-85`). The process guard is only in the missing-manifest legacy branch (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:654-663`), so an existing-manifest activation does not inspect raw/pre-existing Codium. The desktop opener/action invoke bare `codium` (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix:75-81,113-116`), and the prior runtime witness observed an underlying Codium process in a transient app scope rather than the supervisor. Links, roots, manifest, or `extensions.json` can consequently change while an extension host has loaded the old paths. Exact extension-host activity and process provenance remain unproven.

### P1 — Supervisor loss is not bound to the Codium child

The supervisor cleans up on ordinary signals and normal child exit (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh:55-73,83-99`). It does not install a parent-death mechanism, process-group ownership, or watchdog. Killing the supervisor can leave the Codium child and session without the SH lease; a subsequent activation can mutate state while that child remains. The check covers TERM forwarding and ordinary reaping (`/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:1113-1123`), not supervisor or launcher SIGKILL.

### P2 — Contradictory recovery and multi-operation repair are not one durable transaction

`recover_contradictory_managed_state` creates the current link/root, writes and validates the new manifest, then removes the old link/root (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:307-325`). `repair_missing_manifest_roots` similarly scans a plan and executes several root/link mutations sequentially (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:327-386`). A crash between those operations can leave links, roots, and manifest at different generations. Registry files use `sync` plus rename, but manifest writes at `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:320-323,679-681,694-696,722-726` do not sync the file and containing directory.

### P2 — Obsolete-path deletion has a TOCTOU window

The contradictory-state validation authenticates `old_link` and `old_root` at `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:288-305`, then deletes those pathnames at `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:318-325` without revalidating their identity immediately before `rm -f`. A same-user writer can replace either symlink between validation and deletion. `cleanup_prior_manifest_entries` performs a similar check/delete sequence (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:388-407`). This is not a privilege boundary for a compromised user, but it violates the desired fail-closed ownership guarantee.

### P2 — Cooperative locks do not cover older/raw processes or every state path

The lifecycle and managed launcher use one advisory lock (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:634-651`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:65-78`); raw Codium and older processes do not acquire it. Alternate Codium data/extension directory flags are not tied to a corresponding state lease (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:51-61`), so a command can reconcile default state and then operate on another data tree. This is a concurrency/authority gap, not merely stale-lock handling.

### P2 — Predictable temporary names can collide with stale files

Several mutation paths use `$path.tmp.$$` and force moves (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:320-322,474-480,486-535,544-555,589-591,673-681,694-695,722-726`; `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:113-114`; `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh:49-54`). Only registry backups use `mktemp` (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:579-583`). PID reuse or stale temporary entries can make these operations overwrite or consume an unexpected same-name file; a crash can strand the temporary path.

### P2 — Normal registry refresh accepts mutable immutable bytes without universal symlink/store authentication

`registry_matches_immutable` validates JSON content and the two owner records but does not require `.extensions-immutable.json` to remain a Home Manager symlink to a store object (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:420-470`). The stricter symlink/store test exists in contradictory recovery (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:234-255`). A regular user file with matching bytes can therefore authorize normal registry convergence.

### P2 — Activation and read-only-looking CLI paths can report success while state remains unresolved

Activation refresh takes nonblocking EX and returns zero when a GUI holds SH (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:615-632`). The launcher likewise returns zero when reconciliation is in progress (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:72-76`). The module repeats the same refresh command three times (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:344-350`) without explaining the count or surfacing unresolved readiness. `--version`, `--status`, and `--help` also first call `--prepare-launch` (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:51-84`), so callers cannot rely on them being read-only.

### P3 — Raw VSIX/catalogue update authority is split and partly implicit

VisualJJ and Claude use raw file inputs while ChatGPT/Codex uses a separate raw input coordinated with `codex-cli` (`/git/github.com/LiGoldragon/CriomOS-home/flake.nix:50-92`, `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:119-182`). Open VSX remains the source for other profile extensions (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:252-266`). The policy is documented in comments, but no single lifecycle check asserts VisualJJ's `0.28.1` version or that the catalogue/raw authorities remain coordinated. The existing lifecycle check asserts Claude and ChatGPT versions (`/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:264-269`), not VisualJJ.

### P3 — Desktop path resolution hardcodes `$HOME/primary`

`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix:51-56` resolves non-absolute arguments against `$HOME/primary`. This may be intentional for the current workspace but is not a general Home profile invariant and is not represented in a contract check. The desktop action also relies on bare `codium` PATH resolution (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix:113-116`), so desktop authority differs by environment.

### P3 — Preserved user settings include an unresolved Claude permission boundary

Hexis deliberately preserves undeclared settings (`/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:316-356`). The current runtime witness reports Claude permission-bypass keys beyond the declared map. That is observed state, not evidence of who authored it or whether it is authorized; no code change is proposed by this audit.

### P3 — The deployment consumer may lag the audited source

CriomOS pins CriomOS-home separately at `/git/github.com/LiGoldragon/CriomOS/flake.nix:35-49`, and its lock repeats that revision (`/git/github.com/LiGoldragon/CriomOS/flake.lock:882-994`). The inspected Home source is later than that pin. Acceptance claims must state which revision was evaluated and which revision is deployed.

## Confirmed properties, claims, and unknowns

### Confirmed by source read

- Medium profiles import and enable the managed VSCodium module; small/large profiles do not receive it through this module's `lib.mkIf size.medium`.
- The managed `bin/codium` wrapper invokes the launcher, which invokes the lifecycle and then either the direct Codium CLI or supervisor.
- The lifecycle owns stable/versioned Claude links, user-state roots, manifest, and mutable registry refresh under an advisory lock.
- Registry file replacement uses temporary files plus `sync`/rename; manifest and multi-path repairs are sequential.
- Claude and Codex VSIX versions are pinned in source and lock metadata; VisualJJ is pinned in source/lock metadata but lacks an explicit lifecycle-version assertion.
- The home-22f three-version fixture exists at the cited lines and preserves unmanaged extension/settings records in its expected result.
- Agent Intercom's ordinary Claude/Codex commands remain separate from the VSCodium extension's direct pinned CLI.

### Claims carried from prior flow witnesses/reports

- `flows/01a02356/reports/managedExtensionContradiction.md` reports that the focused lifecycle check exited 0, the Home closure was built/activated, and live state converged to Claude 2.1.235; it also reports a normal GUI and Codium CLI observations.
- `flows/01a02b4d/witnesses/managedExtensionState.md` reports that current stable/versioned links, manifest, root, package metadata, and registry converge on Claude 2.1.235; it reports a running normal GUI and no recovery Codium process.
- `flows/01a02b4d/reports/vscodiumRuntimeAudit.md` carries the broader runtime lease, process, settings, and generated-activation observations.

Those are witnesses of prior activity, not results of this source audit.

### Unknown or unresolved

- The historical event that created the earlier contradictory activation state remains unknown.
- Whether the currently deployed Home closure contains this inspected source revision remains unresolved because CriomOS pins a separate older Home revision.
- Real VSCodium extension-host behavior, the exact upstream filesystem effects of every supported CLI flag, and raw/pre-existing process provenance were not proven here.
- Supervisor/launcher SIGKILL survivor behavior and real power-loss crash consistency remain untested.
- Whether preserved Claude permission-bypass settings are authorized user state remains a psyche/owner decision.
- Whether activation should wait, retry, or visibly fail when a GUI holds SH is not settled by this brief.
- Whether VisualJJ should receive an explicit lifecycle/version acceptance assertion is unresolved design authority.
- The deployed coordination client failed registration/claim with `transport IO error: No such file or directory`; this documentation lane proceeded unregistered, as already recorded in the flow log.

## Sources

- Witness: `flows/01a02b4d/witnesses/vscodiumCodeInventory.md`
- Witness: `flows/01a02b4d/witnesses/vscodiumRuntimeAudit.md`
- Witness: `flows/01a02b4d/witnesses/managedExtensionState.md`
- Report: `flows/01a02b4d/reports/vscodiumRuntimeAudit.md`
- Prior report: `flows/01a02356/reports/managedExtensionContradiction.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/text-scale.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/desktop-database.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/vscodium-casual/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/agent-intercom/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-casual/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock`
- Flow `01a02356`
- Flow `01a02b4d`
