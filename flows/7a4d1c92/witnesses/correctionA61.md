# Correction audit: Home a61b02d0

Method: read the exact revision with `jj file show -r a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`; evaluate and build the exact `git+file` revision with the materialized system, horizon, and CriomOS-pkgs inputs; inspect the resulting derivations and store artifacts; and run the configured remote-builder check with `nix build --rebuild --no-link --print-build-logs`.

The Home worktree was clean at the corrected parent `a61b02d0cf69de757bdf8b5fa0f336f78f5054ee`, titled `home: prove resident Chroma projection closure`. Exact source and lock inspection confirms:

- Chroma source and lock: `6a8e4c6a9bb0be0a76baa43b975df91edf6752f9`.
- chroma-emacs source and lock: `119a231358cf69c16161812caf69fff4b726be5c`.

The `yt-dlp` fix is now shape-aware without assuming one module form. `checks/yt-dlp/default.nix:62-70` defines `moduleContent` that unwraps `module.config.content`, then `module.content`, then the direct module. Exact canonical evaluation of `checks.x86_64-linux.yt-dlp.drvPath` exited 0. A forced remote `nix build --rebuild` of the exact yt-dlp check also exited 0.

The corrected resident check imports the shared Home generator/materializer `modules/home/emacs/ignis-themes.nix` (`default.nix:19`, generator lines 1-83), copies the resulting `ignis-dark-theme.el` and `ignis-light-theme.el` into the isolated HOME (`run.sh:24-25`), and no longer writes lookalike Light/Dark files. It still writes only an unrelated overlay fixture and a minimal Chroma config. The common generator is also imported by Home `base.nix`, so the witness consumes the actual shared generator/materializer rather than a test-only implementation.

The corrected check evaluates Home's medium Emacs module and extracts the actual `programs.emacs.package` and `services.emacs.package` (`default.nix:23-39`), asserts those package values are equal (`:63`), and passes the same `emacsWithPackages` closure to the resident witness. The generated Home init derivation records the package closure (`emacs.nix:684-716`); the runtime witness requires `init.elc`, at least one `.eln`, and exact equality between the recorded closure and the package used by the check (`run.sh:26-28`). Read-only store inspection after the remote build confirmed `.elc` present, one `.eln` present, and closure equality. This native-init proof is artifact-level: the resident daemon uses `--quick --load test-init.el`, so the gate does not claim that daemon startup loaded Home's early-init through the normal activation path.

The remote forced rebuild executed the real check and exited 0. Its log reported:

```text
projection status: ('Applied', uint64 0)
projection status: ('Applied', uint64 1)
projection status: ('Applied', uint64 1)
projection status: ('Applied', uint64 2)
projection status: ('Applied', uint64 2)
```

The script's `assert_emacs_state` now queries five runtime facts: target theme enabled, opposite Chroma theme absent, unrelated overlay enabled/absent as expected, rendered default face background, and rendered overlay mode-line background (`run.sh:109-126`). The sequence proves Light revision 0, Dark revision 1, Chroma restart/reconciliation at revision 1, Light revision 2 with overlay retained, and a fresh Emacs daemon reconciling revision 2 with the overlay absent (`:128-160`). It uses inotify/D-Bus/Emacs barriers and contains no `sleep` command.

Canonical gate result: exact `nix flake check --no-build` with materialized system/horizon/pkgs overrides completed with `all checks passed!`; it explicitly evaluated both `checks.x86_64-linux.yt-dlp` and `checks.x86_64-linux.chroma-emacs-resident`. The configured Nix builder is `prometheus.goldragon.criome` (`/etc/nix/machines`), with builder substitutes enabled. The forced resident remote rebuild passed and emitted the runtime status sequence above.

Host-only note: manually invoking the built witness outside the Nix sandbox with the supplied `dbus` `session.conf` failed before Chroma socket creation because this host's included `/etc/dbus-1/session.conf` causes two session-bus addresses with different GUIDs; Chroma reported `Dbus(Handshake("Server GUID mismatch ..."))`. This did not reproduce under the canonical remote Nix build, which passed the full witness. It is a portability caveat for ad-hoc host invocation, not a canonical Home pin blocker.

Disposition: the previous blocker and proof gaps are closed for the corrected commit. Home is safe to pin at `a61b02d0…` on the stated canonical/remote-builder gate, subject to the ordinary deployment authority and the non-blocking host-direct D-Bus caveat. No product, deployment, or runtime state was changed by this audit.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix:143-152`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.lock:418-460`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/yt-dlp/default.nix:62-88`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/default.nix:1-76`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/chroma-emacs-resident/run.sh:1-160`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/emacs/ignis-themes.nix:1-83`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/base.nix:18-106,138-194`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/emacs.nix:14-20,316-317,684-741,792-825`
- `/etc/nix/machines`
- `nix show-config` (`builders`, `builders-use-substitutes`, `max-jobs`)
- Exact canonical evaluation and remote-build commands recorded in this witness's method.
