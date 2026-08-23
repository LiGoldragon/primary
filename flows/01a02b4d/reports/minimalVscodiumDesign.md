# Minimal VSCodium design

This is a proposal for a replacement shape, not an accepted architecture and
not an implementation record. The governing direction is to discard the
managed-extension machine and start from the smallest declarative surface. A
first version may be broken in known ways; preserving the old machine is not a
reason to retain its machinery.

## Intent

Provide VSCodium in the medium Home profile with a pinned, declarative package
and extension set, and let Hexis merge the declared settings into VSCodium's
mutable settings file. The extension directory and extension registry are
Home Manager's immutable generation output. There are no manually installed or
self-updated extensions in the supported contract.

An activation may replace the package and extension generation while an older
VSCodium remains open. That older process is unsupported and may break. A
restart is the operator's remedy. No compatibility bridge, live migration,
process lease, or automatic cleanup is part of this design.

## What the current code does

The current module combines unrelated concerns in one path:

- `modules/home/vscodium/vscodium/default.nix:15-97` builds a casual package,
  launcher, supervisor, and lifecycle package, then replaces `bin/codium`.
- `modules/home/vscodium/vscodium/default.nix:119-182` independently builds
  the VisualJJ, Claude, and ChatGPT/Codex VSIX packages. These are the useful
  declarative extension-delivery pieces.
- `modules/home/vscodium/vscodium/default.nix:247-267` declares the medium
  profile and its extension list. This is the useful Home Manager boundary,
  but its package is currently the custom managed package.
- `modules/home/vscodium/vscodium/default.nix:333-350` adds bootstrap,
  replacement, and three nonblocking registry-refresh activation hooks. Those
  hooks exist only to reconcile the custom mutable lifecycle.
- `modules/home/vscodium/vscodium/default.nix:352-356` gives Hexis the declared
  settings map at `$HOME/.config/VSCodium/User/settings.json`. This remains the
  settings boundary.
- `modules/home/profiles/med/codium.nix:11-83,85-117` adds a custom opener,
  path/line/column parsing, a user desktop file, and a bare `codium` desktop
  action. Those conveniences are not part of the minimal contract.
- `modules/home/default.nix:78,90` imports both the custom desktop profile and
  the custom VSCodium module. The desktop-profile import is removable when
  upstream desktop integration is the chosen boundary.

The code audit and witnesses show why the reconciliation path is not a useful
foundation: it owns mutable links, manifests, roots, registry copies, leases,
supervisor sessions, and recovery branches, while raw Codium and existing
processes can still bypass those assumptions. See the audit's ranked findings
for the exact lifecycle and runtime paths.

## Minimal Nix sketch

The exact Home Manager option is the nested profile option
`programs.vscodium.profiles.default.extensions`; do not invent a second
extension registry or use a top-level extension list. The intended module
shape is approximately:

```nix
lib.mkIf user.size.medium {
  programs.vscodium = {
    enable = true;
    package = pkgs.vscodium;
    mutableExtensionsDir = false;

    profiles.default.extensions = [
      visualjj
      claude-code-codium
      codex-chatgpt-codium
      ovsx.cdervis.vscode-pi
      pkgs.vscode-extensions.mkhl.direnv
      pkgs.vscode-extensions.jnoortheen.nix-ide
      ovsx.zaaack.markdown-editor
      ovsx.lyuwenhan.mermaid-snap
      ovsx.onlyutkarsh.mermaid-diagram-lens
    ];
  };

  home.activation.mergeVscodiumSettings = inputs.hexis.lib.mkManagedConfig {
    inherit lib pkgs hexis;
    file = "$HOME/.config/VSCodium/User/settings.json";
    declared = nixSettings;
  };
}
```

The sketch deliberately leaves the existing `nixSettings`, VSIX derivations,
and native fixups in place. The actual patch must preserve the module's
existing arguments and medium gate and should use the pinned Home Manager
option names accepted by the current input. `mutableExtensionsDir = false`
is the ownership decision: VSCodium does not receive an extension directory
that it may mutate.

The ordinary CLI packages remain ordinary package consumers. Keep
`packages/claude-code/default.nix` and the pinned Codex CLI package/input when
they are consumed by the non-VSCodium CLI surface; the Claude package is also
the native executable embedded by the Claude VSIX fixup. Do not retain a
package merely to support the deleted launcher or lifecycle.

## Keep and delete

| Keep | Why |
|---|---|
| `pkgs.vscodium` | Stock editor package; no `symlinkJoin` replacement of `bin/codium`. |
| `programs.vscodium.enable` and the `size.medium` gate | The actual product boundary. |
| `profiles.default.extensions` list | Declarative extension delivery is a real problem. |
| Raw locked VSIX inputs and derivations | They pin versions and avoid the unfree catalogue gate where required. |
| VisualJJ `patchelf` fixup | Its bundled native `jj` needs the Nix interpreter/RPATH. |
| Claude native-binary replacement | The generic Linux binary is not runnable as shipped on NixOS. |
| Pinned ChatGPT/Codex VSIX | The sidebar is intentionally coordinated with its CLI pin. |
| `nixSettings` through Hexis | Hexis alone owns declared-settings merge into the mutable JSON file. |
| Non-VSCodium CLI packages still used elsewhere | Their independent CLI contracts are not VSCodium lifecycle machinery. |
| Existing medium profile behavior that does not add Codium-specific machinery | Keep only if it is independently consumed; no new convenience wrapper is implied. |

| Delete from the VSCodium design | Why |
|---|---|
| `packages/vscodium-casual/default.nix` | The custom package only adds disable flags around stock VSCodium. |
| `codiumManagedPackage` and its launcher replacement | It creates a second runtime authority for `codium`. |
| `claude-lifecycle.sh` | Mutable links, manifests, roots, registry reconciliation, and recovery are no longer needed. |
| `codium-launch.sh` and `codium-supervisor.sh` | No process coordination or launch protocol is required. |
| `home.activation.bootstrapMutableClaudeCodeExtension` | No mutable extension bootstrap remains. |
| `replaceMutableClaudeCodeExtension` and `refreshMutableClaudeCodeRegistry` | No post-generation reconciliation remains; remove the triple refresh. |
| Custom manifest, GC roots, registry witnesses, leases, sessions, backups, and recovery paths | They describe the deleted lifecycle and must not become a second state system. |
| `checks/vscodium-casual` and lifecycle-only tests | Their contracts disappear. Replace with one behavioral proof, not source grep. |
| `modules/home/profiles/med/codium.nix` custom opener/desktop entry | Rely on upstream desktop integration; discard path rewriting and bare-command convenience. |
| Codium-specific `EDITOR`, `VISUAL`, and MIME-default overrides | They are custom default-editor convenience, not required to provide VSCodium. |
| Manual/self-updated extension support | It conflicts with immutable declarative ownership. |
| Automatic cleanup or migration of abandoned lifecycle state | Old state may remain until separately authorized cleanup. |

Deleting a file from the Home repository, removing its import, and removing
its check are implementation work for that repository; this flow intentionally
does not perform those edits.

## Invariants

The minimal implementation should have only these durable invariants:

1. If `user.size.medium` is false, the VSCodium module contributes nothing.
2. If it is true, `programs.vscodium.package` is `pkgs.vscodium` and
   `mutableExtensionsDir` is false.
3. Every supported extension comes from the Nix extension list under
   `profiles.default.extensions`; VSCodium's own extension updater remains
   disabled by the declared settings.
4. The Claude and VisualJJ native fixups remain inside their derivations; no
   activation-time replacement is performed.
5. Hexis is the only owner of declared settings merge. Undeclared user keys
   remain subject to Hexis's existing merge semantics; this proposal does not
   silently turn that into replacement.
6. No VSCodium activation hook mutates extension links, registries, manifests,
   GC roots, or process state.
7. Desktop integration is upstream's responsibility. The design does not
   promise custom relative-path resolution, `path:line:column` rewriting, or
   a custom preferred-editor selector.

## Deliberate breakage and omissions

This design intentionally does not promise:

- operation of a VSCodium process that was started from an older generation;
- migration of the current mutable extension directory or registry;
- preservation of manually installed extensions;
- live extension updates, marketplace updates, or a custom extension updater;
- a supervisor, launcher, lock, readiness protocol, or launch recovery;
- custom file URI handling, workspace-relative paths, or line/column parsing;
- automatic deletion of the current `~/.local/state/criomos/vscodium-claude`
  tree, recovery directories, old links, or old roots.

The expected failure mode is simple: activation produces the new Home
generation; a newly started VSCodium reads it; an already-running older
VSCodium may fail or continue with stale state until restarted. There is no
attempt to make that transition transactional across processes.

## Smallest durable proof

The replacement check should be one behavioral check in the Home repository,
not a collection of source-text assertions:

1. Evaluate and activate an isolated Home configuration in a temporary home
   with a small, externally specified extension fixture containing at least
   one versioned extension and one nested Hexis setting.
2. Witness that the generated VSCodium extension directory/profile and its
   extension registry are immutable generation outputs, contain the declared
   extension IDs and versions, and do not acquire a mutable-install path.
3. Seed one unrelated settings key, run activation, and witness that Hexis
   writes the declared key while preserving the undeclared key according to
   the existing merge contract.
4. If feasible on the configured builder, run a fresh process against the
   isolated profile and witness `--list-extensions --show-versions` and
   `--version` discovery. This must use the generated profile, not the live
   user's Codium state.

The expected extension versions and settings values come from the fixture,
not from code under test. The check should fail once against the unimplemented
contract before it is accepted. It must not grep Nix source or generated
wrapper text. No real user activation, build, or Codium launch belongs in this
flow.

## Breaking deployment

This is a breaking Home change. The deployment sequence, once separately
authorized and implemented, is:

1. Land the Home change in `CriomOS-home`.
2. Repin the consuming `CriomOS` input to that pushed Home revision.
3. Deploy through the owning system/Home deployment path rather than a local
   ad-hoc activation.
4. Treat any old VSCodium process as unsupported; restart it if needed.

Do not add a compatibility pin, old-generation root, process drain, automatic
cleanup, or migration step. Existing lifecycle state can be left in place
until cleanup receives its own authority. The breaking deployment procedure
belongs in the Home repository's `UPGRADES.md` when the implementation lands;
this proposal does not edit that repository.

## Unresolved deployment-selector contradiction

The source currently presents two related but non-identical Home surfaces:

- CriomOS reads `inputs.deployment.deployment.includeHome` and uses it to gate
  `home-manager.nixosModules.home-manager` and `modules/nixos/userHomes.nix`
  (`/git/github.com/LiGoldragon/CriomOS/flake.nix:162-167,248-256`). Its
  exported `homeConfigurations` are projections of the embedded target
  (`:259-266`).
- The same flake separately exposes
  `independentHomeConfigurations = inputs.criomos-home.homeConfigurations`
  (`/git/github.com/LiGoldragon/CriomOS/flake.nix:268-272`). That standalone
  surface is evaluated by CriomOS-home and is not itself selected by
  `includeHome`.

Therefore “repin CriomOS and deploy through the owner” is necessary but does
not by itself settle which Home activation package a Home-only selector names.
Using the embedded target preserves projected-node selection; using the
standalone output preserves CriomOS-home's own surface. They can differ when
the target has a different user set or when `includeHome = false` removes the
embedded option entirely. The proposal does not choose between these
deployment authorities. The deployment owner must resolve that contradiction
before an implementation can claim that the VSCodium change reached the
intended user profile.

## Sources

- Witness: `flows/01a02b4d/witnesses/vscodiumCodeInventory.md`
- Witness: `flows/01a02b4d/witnesses/vscodiumRuntimeAudit.md`
- Witness: `flows/01a02b4d/witnesses/managedExtensionState.md`
- Report: `flows/01a02b4d/reports/vscodiumCodeAudit.md`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix:15-18,26-97,119-182,186-242,247-267,270-356`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/claude-lifecycle.sh:1-734`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-launch.sh:1-117`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/codium-supervisor.sh:1-99`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/codium.nix:11-117`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/default.nix:32-90`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/vscodium-casual/default.nix:1-46`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix:1-5`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-casual/default.nix:1-22`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/vscodium-claude-lifecycle/default.nix:1-1210`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:43-92,548-551`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix:162-167,248-272`
