# Exact Home yt-dlp check blocker

Method: evaluate the canonical check from the exact Home revision and materialized deployment inputs:

```text
nix eval --impure --show-trace --raw \
  --override-input system /var/lib/lojix/generated-inputs/goldragon/ouranos/home/system \
  --override-input horizon /var/lib/lojix/generated-inputs/goldragon/ouranos/home/horizon \
  --override-input pkgs /git/github.com/LiGoldragon/CriomOS-pkgs \
  'git+file:///git/github.com/LiGoldragon/CriomOS-home?rev=002e521a625cd8a8fa3c4fd7de2a533084e48634#checks.x86_64-linux.yt-dlp.drvPath'
```

The exact-revision evaluation fails while Blueprint imports the canonical check:

```text
error: attribute 'home' missing
at checks/yt-dlp/default.nix:62:17:
  minPackages = (minModule.content or minModule).home.packages;
```

The source cause is deterministic. `checks/yt-dlp/default.nix:25-62` directly imports `modules/home/profiles/min` and assumes either a top-level `content` attr or a top-level `home` attr. At the audited revision, `modules/home/profiles/min/default.nix:445-449` returns an attrset with `imports` and `config = mkIf size.min { ... home = ...; }`; its direct shape has neither top-level `content` nor top-level `home`. The medium profile returns a different `lib.mkIf` shape with `content`, which is why the analogous `mediumPackages` expression does not fail.

The smallest owning correction is in `checks/yt-dlp/default.nix`, not in the Chroma integration: unwrap the min module's `config.content` before reading `home.packages`, or use one helper that handles both `config.content`, `content`, and direct module shapes. No correction was applied by this flow.

Method: probe `jj log --root:checks/yt-dlp/default.nix` and the exact parent diff. The check's file history is:

- `062561b4e29f2b08729f86bf33ca3f2c2e1f7417` — central yt-dlp overlay;
- `20b53335be4243555a9568062487454a96e202ee` — Home package-set verification;
- `51063e6a55ac94f64613f623c5c6601f8a965c99` — unrelated graphical-agent TUI closure.

The latest of those is `2026-08-19`, before audited Home revision `002e…` (`2026-08-23`). The `002e…` diff from its predecessor does not touch `checks/yt-dlp/default.nix`. The blocker therefore predates and is independent of the Chroma–Emacs integration.

Control observation: evaluating the same path through the concurrently modified Home working copy returned a derivation after an outside implementation flow changed `checks/yt-dlp/default.nix`; that is not a result for the audited exact commit. The exact `git+file?...rev=002e…` evaluation above is the authoritative blocker witness.

The separate resident-check derivation evaluates successfully when imported from the exact revision (witness `residentCheckConstruction.md`), so the yt-dlp failure blocks canonical aggregate evaluation but does not invalidate the isolated check's construction evidence.

No product edit, deployment, build, or runtime-state mutation was performed by this witness.

## Sources

- `/git/github.com/LiGoldragon/CriomOS-home/checks/yt-dlp/default.nix:16-73` at revision `002e521a625cd8a8fa3c4fd7de2a533084e48634`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/default.nix:445-449`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/med/default.nix:87-112`
- `/git/github.com/LiGoldragon/CriomOS-home` Jujutsu history for `checks/yt-dlp/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home` exact parent diff `1a6e22da155bb75a6362d10623301b13d0c24b34..002e521a625cd8a8fa3c4fd7de2a533084e48634`
