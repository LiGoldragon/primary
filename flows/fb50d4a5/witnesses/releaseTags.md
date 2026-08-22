# Release tags

Method: probe `jj -R /git/github.com/LiGoldragon/kameo tag list`; `gh api repos/tqwewe/kameo/releases?per_page=100`; `gh api repos/tqwewe/kameo/tags?per_page=100`; `gh api repos/LiGoldragon/kameo/releases?per_page=100`; `gh api repos/LiGoldragon/kameo/tags?per_page=100`; code read `/git/github.com/LiGoldragon/kameo/Cargo.toml`

Observed on 2026-08-22:

- Upstream latest root release is `v0.22.2`, published 2026-07-18, at `90138758779d2260798c41cfaa47598db84f05b8`.
- Upstream root releases after the fork base include `v0.21.0` (2026-06-21), `v0.21.1` (2026-07-01), `v0.22.0` (2026-07-05), `v0.22.1` (2026-07-08), and `v0.22.2` (2026-07-18). Component tags at the latest release include `actors-v0.8.1` and `console-v0.1.4`; `macros-v0.21.1` is at the v0.22.0 release point.
- The local checkout has those upstream tags, including `v0.22.2`, `actors-v0.8.1`, `console-v0.1.4`, `v0.22.1`, `v0.22.0`, `v0.21.1`, and `v0.21.0`. They are refs to upstream history, not releases of the LiGoldragon fork.
- `LiGoldragon/kameo` has zero GitHub releases. Its latest root tag is `v0.20.0` at `2c075ec7e1eca7165bb836eaeef70a144902920f`; its origin tag list has no root tag newer than v0.20.0.
- The fork checkout's `Cargo.toml` still declares package version `0.20.0` and repository metadata `https://github.com/tqwewe/kameo`; its `main` head is not tagged.

## Sources

- https://github.com/tqwewe/kameo/releases
- https://github.com/tqwewe/kameo/tags
- https://github.com/LiGoldragon/kameo/releases
- https://github.com/LiGoldragon/kameo/tags
- `/git/github.com/LiGoldragon/kameo/Cargo.toml`
