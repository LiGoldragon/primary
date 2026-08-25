# Desktop packaging anatomy

The ruled destination is to project Codex and Claude desktop applications onto medium graphical nodes, admit any third-party packaging only through a repeatable per-update audit, and keep terminal and desktop engine versions aligned. This round establishes the boundaries; it does not implement or deploy them.

## Projection boundary

`Medium` currently names several unrelated things. Horizon node size, user trust, model effort, and Home's `profiles/med` are not interchangeable. `AgentIntercomGraphical` is the explicit local graphical-session capability.

Current node declarations are:

```text
Ouranos  Large  Local + Graphical
Tiger    Max  Local + Graphical
Zeus     Max  no AgentIntercom service
```

There is presently no exact Medium node. Home's `profiles/med` means projected size at least Medium and therefore also matches Large and Max. The flow initially interpreted “just medium size” as exact Medium, but the living has not yet reviewed this raw-value-versus-threshold distinction. Current Ouranos and Tiger carry the separate `AgentIntercomGraphical` capability. Package projection remains in `CriomOS-home`; node capability selection remains in `goldragon/datom.dotos`; system prerequisites remain in CriomOS.

## Package ownership boundary

Both vendors now publish official Linux payloads. A third-party flake is no longer needed as the binary origin. The smallest third-party trust shape is an owned public package repository that:

- fetches only vendor release metadata and signed/fixed-output payloads;
- pins every architecture's URL, version, hash, and extracted engine identity;
- packages without running vendor maintainer scripts or mutable installers;
- keeps update and check implementations out of consumer `flake.nix` files;
- exposes packages and Nix checks consumed by immutable Home revisions.

A reputable external flake can instead remain a pinned direct input. Consuming it directly adds its repository, update code, wrapper patches, cache, and revision to the trusted closure. That changes control and trust, but does not inherently increase audit labor: both an owned derivation and an external one require auditing vendor payload plus packaging code on each accepted update. An external flake can reduce maintenance through shared upstream work; an owned repository makes every packaging change deliberate and locally controlled. The choice must therefore rest on trust, control, reuse, and responsiveness—not a claimed audit-work advantage.

## Per-update audit contract

Inputs:

- immutable vendor metadata, payload URL/signature/hash, architecture, license and release identity;
- exact package provider and every flake lock/consumer pin;
- desktop launcher, wrapper, runtime flags, embedded engines and mutable download/cache behavior;
- separately packaged TUI/CLI source revision and artifact checksum;
- node capabilities, projected size, architecture, current profile and resident process versions.

Durable checks:

1. Prove the final provider and immutable source; never infer it from a package name or store residue.
2. Verify the required upstream commit/contract, not merely a tag or version string.
3. Extract and assert desktop build, embedded engine, platform checksum, launcher, sandbox/runtime flags, and maintainer-script exclusion.
4. Build each GUI and CLI through configured remote builders; keep evaluation and build evidence separate.
5. Smoke the actual launcher and headless engine surface. For Codex, assert the selected CLI and app-server report the same pinned version.
6. Evaluate every Home/CriomOS consumer and assert the expected per-node capability matrix.
7. After activation, witness profile paths, desktop entry, launched executable, resident process and engine version separately.
8. Report PWA, URL handler, unreferenced store path, profile package, and running application as distinct states.

Outputs are a machine-readable package tuple, a provider/provenance matrix, a per-node expected/observed matrix, and explicit `current`, `stale`, `missing`, `skewed`, `unsupported`, or `unknown` status. Package-specific facts belong in package checks and workspace documentation; the reusable operating rule belongs in Curriculum.

The closest authored procedure was `nix-input-upgrade`. It already covered provider mapping, immutable revisions, contract pins, patch classification, upstream commit proof, and consumer evaluation. The living approved this additional owning-skill line:

> Before advancing an external package input, verify its final provider, immutable upstream payload and hash, embedded runtimes, contract-pinned consumers, built launchers, and resident versions.

That exact line is now deployed from authored Curriculum commit `ccd1e9f0` through Primary consumer commit `d1056645`; generated copies match the authored source and the durable flake gate passed.

## Alignment contract

Codex can have strong identity. Desktop is a separate Electron frontend, but its CLI, TUI, app-server and protocol share the public Rust workspace. Because Desktop supports `CODEX_CLI_PATH`, Nix can expose one Codex derivation to both terminal and Desktop, assert the app-server's reported version, and activate them atomically. Desktop `26.x` and Codex `0.x` remain separate version fields.

Claude has observable rather than enforceable identity. Desktop and Code share Anthropic's engine/configuration semantics, but Desktop owns a separately downloaded/embedded Code runtime and has no supported external-CLI override. Strict parity would require either holding the standalone CLI back to the embedded version or holding Desktop until it embeds the selected CLI version; otherwise the correct contract is to expose the exact skew. Unsupported internal overrides are outside the proposed design.

## Rulings needed

1. Should the package repository be owned and fetch vendor payloads directly, using third-party flakes only as audited prior art, or may a third-party flake remain a direct pinned input?
2. For Claude, should strict equality block/hold releases, or should independently current Desktop and CLI be allowed with their embedded/standalone skew made explicit and checked?
3. Should the reusable per-update audit rule be elevated to Intent because it governs external package upgrades broadly?
4. Does “medium size” mean raw exact Medium or the existing cumulative Medium threshold, and should the package predicate also require the preserved `behavesAs.edge` general-desktop role?

## Sources

- [Codex alignment witness](../witnesses/codexDesktopAlignment.md)
- [Claude alignment witness](../witnesses/claudeDesktopAlignment.md)
- [Installed application report](linuxDesktopApplications.md)
- [Audit-skill deployment witness](../witnesses/auditSkillDeployment.md)
- Authored `nix-input-upgrade`, `nix-workflow`, `testing`, `agent-harness-packaging`, and `documentation-placement` skills
- `CriomOS-home/modules/home/profiles/min/agent-intercom.nix`
- `CriomOS/modules/nixos/agent-intercom.nix`
- `goldragon/datom.dotos`
- Flow `01a0338f`
