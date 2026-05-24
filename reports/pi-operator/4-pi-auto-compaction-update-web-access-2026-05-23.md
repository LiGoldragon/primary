# Pi auto-compaction update and web-access packaging — 2026-05-23

## Scope

Psyche reported that Pi was not auto-compacting even though the setting appeared enabled, and asked for a latest-version update plus online/source-code research into whether another threshold setting is required.

Work happened in `/git/github.com/LiGoldragon/CriomOS-home` under the `pi-operator` claim.

## Findings

- Pi's documented auto-compaction trigger is `contextTokens > contextWindow - reserveTokens`; `enabled` only turns the mechanism on. The threshold is controlled by `reserveTokens`, and the retained unsummarized tail is controlled by `keepRecentTokens`.
- The current CriomOS-home profile had `compaction.enabled = false` in `modules/home/profiles/min/pi-models.nix`. Even if the live setting was hand-toggled, the declarative profile was not enforcing the intended state.
- Pi 0.75.4/0.75.5 includes compaction-adjacent fixes after our pinned 0.75.3. The changelog calls out a fix for `AgentSession` retry, compaction, and event settlement to use the awaited agent lifecycle instead of a separate event queue.
- The 0.75.5 source clamps compaction summary `maxTokens` to `model.maxTokens`, matching the public issue about silent auto-compaction failures on high-context models.
- Online Pi docs confirm the settings shape: `compaction.enabled`, `compaction.reserveTokens`, and `compaction.keepRecentTokens`.

## Changes made

- Updated Pi source from `github:badlogic/pi-mono?ref=v0.75.3` to canonical `github:earendil-works/pi-mono?ref=v0.75.5`.
- Updated `packages/pi/default.nix` for version `0.75.5`, new package names, changed `packages/ai` script patching, and refreshed `npmDepsHash`.
- Set declarative compaction policy in `modules/home/profiles/min/pi-models.nix`:
  - `enabled = true`
  - `reserveTokens = 32768`
  - `keepRecentTokens = 20000`
  - `"/compaction" = "always"` in the managed settings modes
- Added `pi-web-access` 0.10.7 as a Nix package with a flat flake-input npm dependency closure.
- Enabled `packages/pi-web-access` alongside `pi-linkup` and `pi-subagents`.
- Extended checks to assert the web-access package layout, flake-input packaging discipline, compaction settings, and extension-load behavior.
- Updated `docs/pi-extensions.md` with the `pi-web-access` packaging pattern.

## Validation

Commands run successfully:

```sh
nix build --no-link path:$PWD#packages.x86_64-linux.pi --option warn-dirty false -L
nix build --no-link \
  path:$PWD#packages.x86_64-linux.pi-web-access \
  path:$PWD#checks.x86_64-linux.pi-harness-profile \
  path:$PWD#checks.x86_64-linux.pi-criomos-extension-load \
  --option warn-dirty false -L
```

Notes:

- The second validation emitted transient binary-cache/DNS warnings, then built locally/remotely and completed successfully.
- `pi-criomos-extension-load` now loads both the local theme-switcher extension and `pi-web-access/index.ts` far enough to list the local test model.

## User-attention items

- The effective auto-compaction trigger is now earlier than Pi default because `reserveTokens` is `32768` instead of `16384`. This is intentional headroom for long Codex turns; lower it if compaction feels too eager.
- `pi-web-access` is installed in addition to `pi-linkup`, not as a replacement. Their tool names do not conflict: `pi-web-access` provides `web_search`/`fetch_content`; Linkup provides `linkup_web_search`/`linkup_web_fetch`.
- `pi-web-access` optional video/GitHub helpers may depend on runtime tools like `ffmpeg`, `yt-dlp`, `git`, or `gh`; the package-load check covers extension import, not every optional extraction path.
