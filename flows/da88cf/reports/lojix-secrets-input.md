# Lojix secrets input: why sopsFiles is empty (deployment 32)

Verdict: the empty map is expected output for the request as submitted. It is a caller error, not a Lojix defect. Deployment 32 passed `NoSecrets`. It used current cluster data (goldragon main 8c4d03d), not a July materialization. It FAILED at Eval; it did not build.

## Source (lojix a67f5773, src/schema_runtime.rs)
- `ClusterSecretsDirectory::from_input`: `NoSecrets => Ok(Self { path: None })`.
- `secret_files`: `let Some(directory) = &self.path else { return Ok(Vec::new()); };` When a directory is given, it reads that directory without recursing and keeps entries with extension `sops`. There is no manifest. The expected level is `.../goldragon/secrets`, which holds 4 `*.sops` files, including opencodeServerPassword.sops.
- `write_secrets` resets the directory and always writes `{ outputs = _: { sopsFiles = {\n  }; }; }`. With no files, the map is empty.
- `materialization_root` = `generated-inputs/<cluster>/<node>/<shape>`. The path is shared and is rewritten on every deploy. There is no per-deployment temporary directory.

## Deployment 32
- `lojix 'Query.ByDeployment.{ 32 }'` → `Failed ... Some.Failed.{ Eval EvaluationFailed ... Failed assertions:» True }`. The record holds the override hashes `horizon ...narHash=sha256-pq5BCnL7...` and `secrets ...narHash=sha256-wzsoy6o9...`.
- `nix hash path` of the on-disk horizon/ and secrets/ gives exactly those two hashes. The 22:43 tree is deployment 32's own materialization.
- The file mtimes are all 22:43:20–21, horizon.json included. The July times belong only to the directories, which keep their mtime because the files are rewritten in place.
- The Lojix store bytes (read from a copy) show `p61bn3w1...-horizon-definition/horizon-definition.datom` followed immediately by `github:LiGoldragon/CriomOS?rev=3e2cc8be...` (7 records). No secrets path sits between them, which means `NoSecrets`. The prometheus records do show `SecretsDirectory` paths there, for example `/home/li/wt/348e7b-goldragon-secrets/secrets`.
- The proposal p61bn3w1 is goldragon main 8c4d03d (00f95a report). It carries `OpenCodeTesting.{}` for ouranos, and horizon.json contains `"openCodeTesting"`. With that capability present and the map empty, the assertion fires, as expected.

## Earlier ouranos host deploys
Deploys 3 (477beac) and 4 (36653a12) succeeded. Their stored requests have the same `...datom` + `github:` adjacency, which also means `NoSecrets`. Presumably no capability required a secret at the time. The 00f95a packet, which deployment 32 reused, records `Secrets | NoSecrets`.

## Fix
Resubmit with `SecretsDirectory./git/github.com/LiGoldragon/goldragon/secrets` (the form in tailnet-repair-slice.md:211).
