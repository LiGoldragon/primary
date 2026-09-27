# Bounded deletion audit — 2026-09-27

Scope: read-only JJ/Git metadata for `/home/li/primary` and the three retained CriomOS-home workspaces. No source, index, checkout, reset, restore, or remote mutation occurred.

Primary working copy was `57b8bd3b69b6ca6b9602e385db0bba01f34376cc`, with parent `a8e9ae3b59c357f630bb2dbdc06b89c4237ddd49`; its status reported additions and modifications only, with no deleted path. Real `origin/main` read back as `18baad590b13ff5dfb4e9855dcd492580f9b4b5a`, matching the local `main` bookmark.

The alleged commit `b8bebfa418ca3178e196fa3d8d9480b8b2a456ad` has parent `9cf9fbdf4d6c686384b197ae0139c60142e266ac` and its immutable JJ diff summary contains exactly one modification: `flows/56ae53/log.md`. It contains no deletion.

From the known primary parent `a8e9ae3b59c357f630bb2dbdc06b89c4237ddd49` through current main, the bounded JJ diff summary counted A=132, M=5, D=0. The retained summary is `/var/tmp/flow-home-stage-main-diff-summary-6fe957.txt`, SHA-256 `220110779f0c0fa9984a2f5153d30361a10b2a78763ffbe4e5f69667e4e8e2cb`.

CriomOS-home widget workspace is clean on f368ed70. The Spirit fixture workspace is clean on its separate review branch. The older guarded-override workspace has two pre-existing modifications (`lib/flow-stable-override-adoption.sh`, `modules/home/profiles/min/flow.nix`), not deletions; this audit did not modify them.

Conclusion: this bounded evidence finds no committed or current-working-copy deletion in the audited ranges. The UI's approximately 16,000 deleted-line display is not explained by a destructive commit here; a materialization/generated-diff presentation remains possible, but the responsible UI layer and any wider deletion outside this bounded scope are unknown.
