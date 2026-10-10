# TUI and desktop update mechanics witness

This is a read-only investigation witness. It records current source mechanics and
does not authorize a package edit, lock update, build, or deployment.

## Authority and selectors

The primary workspace has no live authored application/version manifests under
`manifests/`; that directory is empty. `protocols/repos-manifest.dotos` is a
repository inventory, not package-version authority. The effective package
authority is therefore the Home flake inputs/lock plus the package and overlay
functions below. The host flake pins Home as a flake input and consumes its
embedded Home configuration.

Relevant selectors:

- Home package outputs: `packages.x86_64-linux.codex` and
  `packages.x86_64-linux.claude-code`.
- Complete host output: `nixosConfigurations.target.config.system.build.toplevel`.
- Embedded Home activation output: `homeConfigurations.<user>.activationPackage`.
- Standalone Home output (for a Home-only activation):
  `inputs.criomos-home.homeConfigurations.<user>.activationPackage`.

## Exact update/re-evaluation path

1. Update the Home producer's `llm-agents` input (and any separately pinned VSIX
   inputs) in the Home checkout, then evaluate/build its package and checks.
2. Publish an immutable Home revision.
3. In the CriomOS consumer, update the `criomos-home` input. Because Home's
   package inputs are flattened into the consumer lock, compare and, when needed,
   synchronize the `llm-agents`, `claude-code-vsix`, and `codex-chatgpt-vsix` lock
   nodes as well. The Home workflow explicitly requires this downstream lock
   synchronization; changing only the source URL does not change what the lock
   evaluates.
4. Re-evaluate the consumer's complete-host selector. A Home-only selector
   re-evaluates only standalone Home; it does not prove the embedded Home in the
   host output. A complete-host re-evaluation is required for desktop derivations
   included in the OS.
5. Build remotely with the repository's required builder settings, then activate
   through the typed Lojix deployment route selected by the caller. Admission is
   not completion; query the deployment until its terminal result and collect
   activation evidence separately.

For this investigation I only performed read-only metadata/evaluation queries;
no lock, package source, configuration, or deployment was changed.

## Codex current shape

`packages/codex/default.nix` selects the one `inputs.llm-agents` Codex package.
`modules/home/profiles/min/agent-intercom.nix` binds that package once as
`codexCliPackage` and passes it to the terminal wrapper, the app-server service,
Agent Intercom's raw command, and the ChatGPT Desktop wrapper's
`CODEX_CLI_PATH`. `packages/codex/tui.nix` is a launcher around that same package,
not a second Codex runtime. The graphical check compares the terminal/raw
versions and checks the ChatGPT wrapper path against the same derivation.

This is already the strongest end-shape for Codex's supported integration: one
declared package, injected into every controllable consumer. The ChatGPT Desktop
payload can still contain a vendor-bundled copy; the wrapper selects the Nix
binary, so “same TUI” means the selected execution path, not payload byte
identity. The current check does not execute a signed-in GUI session to prove
every GUI code path honors that environment variable.

The Codex editor sidebar is a separate VSIX UI (`codex-chatgpt-vsix`) and is not
the terminal binary. Its version must therefore be treated as a separately
audited UI release, not silently equated with the CLI version.

## Claude current shape

`packages/claude-code/default.nix` selects the one `inputs.llm-agents` Claude
Code package. The Claude Desktop overlay constructs the official Desktop payload,
patches its dormant local-binary branch to the Nix Claude executable, and makes
the local path fail closed when unavailable. The launcher-linkage repair makes
the final launcher execute the copied patched resource tree rather than an
upstream nested wrapper. The Claude checks exercise declared-path resolution,
fail-closed behavior, final-launcher resource linkage, and EGL linkage.

This is the strongest feasible parity shape while upstream Desktop provides no
supported external-CLI override. It guarantees the selected local Claude Code
runtime is the same package used by the terminal/extension, but it is a
package-local compatibility patch: each Desktop upstream update must re-audit
the patch markers and retain a fail-closed test. The Desktop's own release and
other cloud/vendor paths remain independently versioned; exact byte/runtime
identity for every Desktop feature is not established by the current checks.
If the upstream structure removes the dormant branch, the safe alternatives are
to hold the Desktop update until the bridge is repaired or explicitly report
unsupported local parity. A mutable second Claude installation is not a parity
solution.

## Concrete drift and double-stack conditions

- The current CriomOS source URL names a newer Home revision than the
  `criomos-home` node actually locked in `CriomOS/flake.lock`; Nix evaluates the
  locked revision. Direct Home evaluation and complete-host evaluation can thus
  describe different Home package/config generations until the downstream lock
  is synchronized.
- Home's Codex ChatGPT VSIX input is `26.5818.61809`, while the llm-agents
  ChatGPT Desktop package currently reports `26.820.60940`. These are distinct
  release streams, so the editor UI and desktop UI can drift even when the
  selected Codex CLI is shared.
- Claude Desktop's upstream payload still contains vendor manager/download and
  mutable-state machinery, although the patched local path bypasses it and
  fails closed. Stale mutable files may remain inert on disk; their presence is
  not proof of a selected second runtime. The launcher-linkage check is the
  protection against accidentally launching the unpatched nested tree.
- A running GUI process can retain an older executable after a profile update;
  package/profile equality requires restart and a fresh process witness.
- `codexTui` can occur in more than one conditional Home package list, but both
  references resolve to the same derivation. This is list duplication, not a
  version double-stack.
- Agent Intercom's adapter family has its own pinned release and is not itself
  the Codex CLI. Its raw command is nevertheless pointed at the shared Codex
  package.

## Open proof gaps

- No live GUI smoke check proves every ChatGPT Desktop feature uses
  `CODEX_CLI_PATH`.
- No signed-in Claude Desktop session proves every local-thread path remains on
  the patched executable after future upstream updates; current checks cover the
  package launcher and injected test entrypoints.
- The complete-host lock must be synchronized and then independently re-evaluated
  before claiming that a newly updated Home package is present in the deployed
  OS.

## Source witnesses

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/codex/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/codex/tui.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/claude-code/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/claude-desktop.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/overlays/patch-claude-desktop-runtime.mjs`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/vscodium/vscodium/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/agent-intercom-graphical-tui/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/claude-desktop-declared-cli/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/claude-desktop-launcher-linkage/default.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/userHomes.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/skills.md`
- `/home/li/primary/flows/01a0338f/vision/tuiAndDesktopVersions.md`
- `/home/li/primary/flows/01a038be/vision/codexDerivation.md`
- `/home/li/primary/flows/01a03e02/vision/claudeDesktopUsesOurClaudeCode.md`
- `/home/li/primary/flows/01a03e02/reports/claudeDesktopDeclaredCliRealization.md`
- `/home/li/primary/flows/01a03f47/reports/claudeDesktopRuntimeDiagnosis.md`
