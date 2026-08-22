# CriomOS-home Chroma–Emacs slice audit

This is a read-only audit of exact Home revision `002e521a625cd8a8fa3c4fd7de2a533084e48634` against the accepted Chroma–Emacs contract, Chroma `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`, and chroma-emacs `d432f95db5837e685e32afbf5790060fb15a3703`. Product repositories, deployment, and runtime state were not changed by this flow.

## Result

Pin identity and Home ownership are correct. The isolated resident check is structurally real and independently evaluable. Home is not yet a clean canonical pin candidate: exact-revision aggregate evaluation is blocked by the pre-existing yt-dlp check, and the resident check has important evidence gaps around generated Home artifacts and native-compiled initialization. A pin may be technically staged for follow-up, but should not be accepted as a green, fully proven Home revision.

## Confirmed Home contract

The lock and source declarations point exactly to the requested Chroma and chroma-emacs revisions. Home derives one PGTK Emacs package set, passes that set to `mkChromaTheme`, builds one `emacsWithPackages`, and uses it for both Emacs configuration and service. The native-compilation derivation invokes that same runtime package synchronously for byte and native compilation, with its generated `.eln` cache added to early-init.

Home owns the concrete Ignis themes. `base.nix` generates `ignis-light` and `ignis-dark` from Home palettes, installs their files under `.config/emacs-ignis-themes`, and disables Stylix's Emacs target. The Home-owned init adds that directory to `custom-theme-load-path`, supplies the two symbols, loads `chroma-theme`, and enables global `chroma-theme-mode` in the resident Emacs init.

The Chroma DOTOS config has no Emacs concern or one-shot Emacsclient adapter. The old Darkman/current-mode projection is absent as functional behavior. Generic Emacsclient remains for Home's ordinary preferred-editor, MIME, desktop-entry, and test-control surfaces; deleting that utility would exceed the settled brief. One stale VSCodium comment still mentions Darkman, but it is not a live adapter.

## Resident check

The exact check derivation evaluates independently from the dirty working copy. Its generated witness PATH includes the built PGTK Emacs-with-packages, built Chroma daemon, fake Gamma peer, and private-bus tools. The shell enters a private `dbus-run-session`, isolates HOME/XDG state, starts real Chroma and a real Emacs daemon, and queries the D-Bus projection status and Emacs face/theme state.

The sequence proves, if executed, late Emacs startup at revision 0, Light-to-Dark revision 1, Chroma owner restart and reconciliation at revision 1, Dark-to-Light revision 2, and a fresh Emacs daemon reconciling revision 2. It checks `Applied` status, expected Ignis theme/background, and preservation of an unrelated mode-line overlay. Its barriers use inotify and bounded reads; there are no sleeps or source-text assertions masquerading as behavior checks. Runtime output is queried through D-Bus and `emacsclient`.

The check is not a complete proof of the Home contract:

- It writes simplified Ignis theme files into the test HOME instead of materializing the generated `base.nix` files.
- It uses `emacs --quick` and a manually loaded test init rather than Home's generated early-init and native-compiled `.eln` path.
- It checks only `Applied`; the other protocol statuses belong to Chroma/chroma-emacs tests.
- It does not explicitly assert that the opposite Chroma theme is disabled, or query runtime source revisions.

No build or execution of this check was performed in this audit. Therefore the derivation wiring is witnessed, while execution remains a separate claim requiring an execution witness.

## Canonical blocker

Evaluating the canonical `checks.x86_64-linux.yt-dlp` output from the exact Home commit with materialized system/horizon/pkgs inputs fails at `checks/yt-dlp/default.nix:62` because the check reads `.home.packages` from a direct min-profile import. The min profile returns `config = mkIf ...`, not top-level `content` or `home`; the medium profile's shape differs. The smallest fix belongs to the check and unwraps `minModule.config.content` or normalizes both module forms.

History places this check defect before the audited integration: the file was last touched by the 2026-08-19 yt-dlp commits, and `002e…` does not modify it. The failure is therefore independent of Chroma–Emacs. A direct exact-revision import of `checks/chroma-emacs-resident` still evaluates to a derivation, cleanly separating isolated construction evidence from the aggregate blocker.

## Acceptance disposition

1. Exact pins: confirmed.
2. Same package set/native compilation: source-confirmed; resident-check execution of compiled/native init remains unproven.
3. Home Ignis ownership, path, symbols, and mode enablement: source-confirmed.
4. Darkman and Chroma-specific Emacs concern/adapter removal: confirmed, with generic Emacsclient retained intentionally and one stale documentation comment.
5. Private-bus built Chroma + PGTK Emacs resident witness: derivation construction confirmed; execution not performed here.
6. Runtime revisions/status/faces/overlay/restarts: behavior is encoded in the check, but execution must be separately witnessed; all-status coverage is intentionally delegated to upstream protocol tests.
7. Canonical Home evaluation: blocked by pre-existing yt-dlp shape defect at exact revision.

The appropriate handoff is “integration shape sound, canonical gate blocked, behavior execution and generated-artifact/native-init proof still outstanding,” not “Home fully safe to pin.”

## Correction audit — 2026-08-23

The corrected Home commit is `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee` (`home: prove resident Chroma projection closure`). It updates the plugin pin to `119a231358cf69c16161812caf69fff4b726be5c`, retains Chroma `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`, and is clean at the audited parent.

The yt-dlp check now uses a `moduleContent` helper that unwraps `config.content`, then `content`, then a direct module. Exact canonical evaluation and a forced remote rebuild of `checks.x86_64-linux.yt-dlp` both pass. The earlier shape blocker is closed without a brittle one-profile assumption.

The resident check now imports Home's shared `ignis-themes.nix` generator/materializer, copies its generated Ignis files into the isolated test HOME, evaluates Home's actual medium Emacs module, asserts program/service package identity, records and checks the exact Emacs closure, and requires real `.elc` and `.eln` artifacts. Its runtime assertions explicitly require the target theme enabled, the opposite Chroma theme absent, overlay state, rendered default and overlay face backgrounds, and all Light/Dark plus Chroma/Emacs restart transitions.

The native-init claim is artifact-level rather than an activation-path claim: `homeInitCompiled` is produced by Home's medium Emacs module and the witness checks its `init.elc`, `.eln`, and exact package-closure match. The resident daemon uses `--quick --load test-init.el`, so the check does not additionally prove that daemon startup loaded Home's early-init through the normal activation path. This bounded distinction is not a pin blocker for the requested compiled/native artifact and package-identity contract.

Exact `nix flake check --no-build` with materialized inputs reports `all checks passed!`, including yt-dlp and the resident check. A forced remote `nix build --rebuild` of the resident check passed and emitted Applied revisions `0`, `1`, `1`, `2`, `2`; a forced remote yt-dlp rebuild also passed. This is execution evidence, not merely source construction.

Direct host invocation of the built witness failed before Chroma startup because the host's included `/etc/dbus-1/session.conf` creates a duplicate/mismatched-GUID bus when passed through the Nix `session.conf`; the canonical remote Nix sandbox executed the same witness successfully. This remains a non-blocking ad-hoc-host portability caveat, not a canonical gate failure.

Updated disposition: Home `a61b02d0…` is safe to pin under the stated canonical and configured remote-builder gates. Deployment authority remains separate and was not exercised here.

## Sources

- Witness: `flows/7a4d1c92/witnesses/homeChromaContract.md`
- Witness: `flows/7a4d1c92/witnesses/residentCheckConstruction.md`
- Witness: `flows/7a4d1c92/witnesses/ytDlpBlocker.md`
- Correction witness: `flows/7a4d1c92/witnesses/correctionA61.md`
- Prior accepted contract: `flows/01a02b4c/reports/chromaEmacsReacquisition.md`
- Prior Home reconnaissance: `flows/5ff8f889/reports/chromaEmacsHomeSlices.md`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/emacs/chroma-theme-init.el`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/chroma.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/run.sh`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/yt-dlp/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/default.nix`
- `/git/github.com/LiGoldragon/chroma/src/theme_dbus.rs`
- `/git/github.com/LiGoldragon/chroma/src/daemon.rs`
- `/git/github.com/LiGoldragon/chroma-emacs/lisp/chroma-theme.el`
