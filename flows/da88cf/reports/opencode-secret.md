# OpenCode secret assertion — where it lives, why evals differ, minimal fix

1) Assertion site: CriomOS@3e2cc8be `modules/nixos/testing/opencode.nix:40`
   `message = "OpenCode testing requires inputs.secrets.sopsFiles.${secretName}"`
   (secretName = "opencodeServerPassword", line 14). Gate: line 13
   `enabled = nodeServices.has horizon.node.capabilities "openCodeTesting"` —
   a CriomOS module reading cluster/**horizon** data, not a Home module. Ouranos's
   generated `horizon/horizon.json` (both evals share this input) lists capability
   `"kind": "openCodeTesting"` at line 122, so the module is enabled for ouranos
   either way; only `secretAvailable` differs. CriomOS-home@4a9d85d7 only consumes
   the same secret path (`modules/home/profiles/min/opencode.nix:12`) and asserts
   nothing itself.

2) `/var/lib/lojix/generated-inputs/goldragon/ouranos/complete-host/`:
   horizon/ (flake.nix, horizon.json) — 2026-07-10 07:10:52
   system/  — 2026-07-10 07:10:52
   deployment/ — 2026-07-10 07:10:52
   secrets/ (flake.nix only) — 2026-09-25 22:43:21 (tonight's, newer than the other three)
   secrets/flake.nix: `sopsFiles = {}` — empty; no `opencodeServerPassword` key.
   Integrator's earlier "current Horizon inputs" eval evidently used an older
   secrets input (or none) that didn't yet assert this, or bypassed the check.
   goldragon/secrets **main** (`wt/348e7b-goldragon-secrets`, `origin/main`) DOES
   hold `secrets/opencodeServerPassword.sops` — the file exists upstream but
   hasn't propagated into tonight's generated `secrets/flake.nix` sopsFiles map.

3) Minimal declared fix to unblock deployment 32: not a repo-file toggle — the
   generated `secrets/flake.nix` sopsFiles map must include `opencodeServerPassword`
   pointing at goldragon/secrets' `secrets/opencodeServerPassword.sops` (a Lojix
   generated-input regeneration, not a hand edit). Alternative to disable instead:
   drop the `openCodeTesting` capability entry from ouranos's horizon capabilities
   (cluster data, not this repo) — but flows/5f38bc/messages/…e71dab.md ("Coordinate
   b7da5d OpenCode Home work") shows the living wants OpenCode live, so the correct
   fix is declaring the secret (regenerating the secrets input from goldragon/secrets
   main), not disabling the capability.
