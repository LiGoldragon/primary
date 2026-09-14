# OpenCode release package

`release-package.nix` packages the immutable upstream OpenCode 1.17.13 Linux x64 release with its published fixed SHA-256 and `fetchurl`. The release archive digest identifies the downloaded asset; it is separate evidence from the expected source-tag commit `10c894bdeef3618f5666fb506ef7f9491bb964d8`. This file does not install or build the package locally; evaluation and remote build are owned by the calling flow.
