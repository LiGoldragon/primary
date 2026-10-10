# Audit of items 47 and 48, Prometheus service provider (Codex cf7879) — 2026-09-16 night

Written by a Fable audit subflow of flow 840e42, read-only; placed here verbatim by the main flow. Witnessed unless marked claim.

## Verdict

1. **Works:** one disabled-by-default NixOS module (`criomos.prometheusServiceProvider`) that, when enabled, switches on stock Prosody (PEP, encryption required, no registration) and stock Forgejo (https, registration off, Actions flag), plus a flake check that reads those option values back. Nothing is merged, nothing is deployed.
2. **Missing (item 47):** Yggdrasil binding, ssh, namespaces/orgs for universal primary / persona / per-person, GitHub mirrors, any `sops.secrets` declaration, any runner, any build of the Slint app or crates, any result recording, any review step. The "pipeline" is a two-line `/etc/forgejo-review-pipeline/*.conf` text file and `actions.ENABLED = true`.
3. **Missing (item 48):** accounts for the living and a bot, a chime bot, a `Notify.{…}` CLI, a bot build check, self-signed fallback, any Cloudflare linkage. OMEMO 2 is not established: PEP alone is enabled; MAM, carbons, smacks are untouched; and, decisively, the enabled configuration **fails NixOS's own evaluation** (witnessed below).
4. **Must change before the living tests it:** the module must set `services.prosody.muc` and `httpFileShare` (or explicitly disable `xmppComplianceSuite`), or `system.build.toplevel` throws; the check must evaluate `toplevel`, not just option echoes; TLS must have the self-signed path the order required (today a null path is an assertion failure, so the module is unenableable without a pre-existing sops secret).
5. **Provenance:** Codex's reports (through commit `5289296cc`, 23:25 -0600) do not mention this branch at all; the three CriomOS commits (23:28–23:33 -0600, GPG-signed by the living's key on ouranos) postdate its last report, whose final line says "disabled Prometheus service module proof" was *next*. Codex claimed nothing about 47/48 beyond that; the module is unreported work, not a verified deliverable.

## Evidence

**Branch contents** (`/git/github.com/LiGoldragon/CriomOS`, `origin/proposal/prometheus-service-provider-poc`, 3 commits over main, 217 lines, contained by no other branch; main last moved 2026-09-12): `modules/nixos/prometheus-service-provider.nix`, `checks/prometheus-service-provider-policy/default.nix`, a `flake.nix` check registration, and an import line in `modules/nixos/criomos.nix`. That import means the module is present (disabled) in every CriomOS host that consumes `nixosModules.criomos`, prometheus included.

**Secrets.** The module takes `tls.certificatePath`/`keyPath` as plain strings and asserts both non-null when enabled. No `sops.secrets.*` is declared; the check feeds literal `/run/secrets/...` strings. No secret can reach an agent through this branch because no secret exists in it; the sops discipline is a doc-comment, not code. The self-signed-until-Cloudflare fallback is absent — a null path is a hard assertion failure.

**Evaluation witnessed** (offline, 120 s bound, temporary worktree at `7c9975a`):
- `nix eval .#checks.x86_64-linux.prometheus-service-provider-policy` throws on the `system` stub input, by repo design (AGENTS.md: needs lojix `--override-input`). Lojix inputs not materialized; the check itself therefore unevaluated by the auditor.
- Evaluating the module directly with `inputs.nixpkgs.lib.nixosSystem` and the check's own "enabled" values, then forcing `system.build.toplevel`, fails with two nixpkgs Prosody assertions: *"You need to setup at least a MUC domain to comply with XEP-0423"* and *"You need to setup http_file_share modules through config.services.prosody.httpFileShare"*. The branch's check never touches `toplevel`, so it cannot see this.
- Codex reported no `nix eval`/`nix build` of this branch anywhere in `flows/cf7879/log.md`, `reports/overnight-2026-09-15.md`, or `reports/to-840e42.md`.

**The check is self-confirming.** Every `test … = …` line compares an option value to the literal the check itself set (domain in, domain out; path in, path out). The two `hasFailedAssertion` cases are the only behavior tests, and they test the module's own assertions, not NixOS's. It is not a text change-detector, but it proves wiring, not a working service.

**OMEMO 2.** Locked nixpkgs has Prosody 13.0.6 and separate `modules.{mam,carbons,smacks,csi,bookmarks}` options; the module sets only `modules.pep`. PEP is necessary for XEP-0384; MAM/carbons are what make a bot's messages reach an offline living. No client/bot exists, so OMEMO 2 (XEP-0384 0.9, SCE) is untested end to end — Codex's own log (line 45) already said "generic OMEMO support does not prove an OMEMO 2 client/bot implementation".

**Cloudflare** (`/git/github.com/LiGoldragon/cloud`, `origin/proposal/cf7879-cloudflare-readonly-fixture-fixed`, commit `b0402e3`, +317 lines): a `FixtureCredentialSource` bound to one `CredentialHandle` and a `ReadOnlyFixtureApi` whose create/update/delete return `RequestRejected`. Codex reports `cargo test --test cloudflare_fixture --features cloudflare` 2/2 (claim; its reviewer did not rerun). No TLS/certificate provisioning exists on cloud main or this branch — only CAA/TLSA record-kind enums. There is no "Cloudflare provider object" for the Prosody module to consume; the CriomOS module does not reference cloud at all.

**Deployment / hosts.** Codex's overnight report states repeatedly "no host deployment". CriomOS main is unchanged since 2026-09-12 and the POC branch is contained only by itself. A bounded read-only SSH probe of prometheus for `prosody*`/`forgejo*` units was denied by the permission classifier, so live host state is Codex's claim plus branch containment, not a witness.

**Inference (the auditor's).** The 23:28–23:33 CriomOS commits, signed with the living's key on ouranos and unreported by Codex, were most likely produced by a Codex worker after the last report commit; alternatively by the living directly. Either way, no account of them exists in `flows/cf7879`.

Files: `/git/github.com/LiGoldragon/CriomOS` (branch above); `/git/github.com/LiGoldragon/cloud` (branch above); Codex reports at `origin/flow/cf7879:flows/cf7879/reports/{overnight-2026-09-15.md,to-840e42.md}` and `flows/cf7879/log.md`.
