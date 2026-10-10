# Goldragon check, tailnet-repair-da88cf @ e8ce1e42, 2026-09-26

Subflow of b860be. Authority: read-only. No commits, pushes, deploys, or messages made to the goldragon repository or the cluster.

## Target and workspace

- Repository: `/git/github.com/LiGoldragon/goldragon` (origin `ssh://git@github.com/LiGoldragon/goldragon`).
- Bookmark: `tailnet-repair-da88cf`.
- Remote verification: `git ls-remote origin refs/heads/tailnet-repair-da88cf` → `e8ce1e42be4644b4e96cac1bcba6a8b1b4232563` (**W**, matches the assigned revision exactly).
- Checkout: a fresh `jj workspace add /home/li/wt/github.com/LiGoldragon/goldragon-b860be-check`, then `jj edit e8ce1e42` inside it. `jj log -r @` in that workspace confirms `sszkzyuu e8ce1e42be4644b4e96cac1bcba6a8b1b4232563`. The shared `tailnet-repair-da88cf` workspace checkout (used by other flows, e.g. da88cf) was never touched.

## `nix flake check`, built on Prometheus only

Command (first pass, default eval cache):

```
nix flake check --max-jobs 0 --option builders 'ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 6 10 big-parallel,kvm,nixos-test' -L
```

Result: `all checks passed!`, exit 0. This pass evaluated all three checks (`synchronizer`, `horizon-definition`, `synchronizer-configuration`) but reported "running 0 flake checks" — Nix's local `eval-cache` (`~/.cache/nix/eval-cache-v6`, shared across the machine) had already recorded a successful check for this exact flake-lock/derivation state from earlier work on this same revision, so it produced no fresh `building '…' on 'ssh-ng://…'` lines this pass.

To capture direct build-offload evidence rather than rely on the cached verdict, the check was re-run with the eval cache disabled for this invocation only (`--option eval-cache false`; the shared cache directory itself was left untouched):

```
nix flake check --max-jobs 0 --option eval-cache false \
  --option builders 'ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux /etc/ssh/ssh_host_ed25519_key 6 10 big-parallel,kvm,nixos-test' -L
```

Full captured output:

```
evaluating flake...
checking flake output 'packages'...
checking derivation packages.x86_64-linux.default...
copying path '/nix/store/6im92ly6cg18mjx8r2kj3pzhghnfymgf-source' from 'http://nix.prometheus.goldragon.criome'...
warning: file 'nar/6im92ly6cg18mjx8r2kj3pzhghnfymgf-05gkj63qrfym7rb93fc5sd74sf8vz20pr0rkhz10czyr7nnqjhrq.nar' does not exist in binary cache 'http://nix.prometheus.goldragon.criome'
evaluation warning: stdenv.isLinux is deprecated, use stdenv.hostPlatform.isLinux instead
evaluation warning: stdenv.isDarwin is deprecated, use stdenv.hostPlatform.isDarwin instead
derivation evaluated to /nix/store/pmb2jqgnnyihb557qsbv68rbikd3vk59-horizon-definition.drv
checking derivation packages.x86_64-linux.horizon-definition...
derivation evaluated to /nix/store/pmb2jqgnnyihb557qsbv68rbikd3vk59-horizon-definition.drv
checking derivation packages.x86_64-linux.horizon-cli...
derivation evaluated to /nix/store/bk47b9f55pd2gkcpj2dr48rf4hrn3p46-horizon-0.13.0.drv
checking derivation packages.x86_64-linux.synchronizer-configuration...
derivation evaluated to /nix/store/hia0mahvrf7y7s5jrydpjc66n23fkd9b-goldragon-synchronizer.datom.drv
checking flake output 'checks'...
checking derivation checks.x86_64-linux.synchronizer...
copying path '/nix/store/s1vjmwkiffxix669fnsb8blwzqib1qc7-source' from 'http://nix.prometheus.goldragon.criome'...
warning: file 'nar/s1vjmwkiffxix669fnsb8blwzqib1qc7-1acw9xb1cxdj9c7h5dajcqjz7wmlvwfhiqy4069b71j8hk0clmaa.nar' does not exist in binary cache 'http://nix.prometheus.goldragon.criome'
derivation evaluated to /nix/store/mqswhyvhdjxr3q7hijlkphynsxxw06i9-synchronizer-0.4.0.drv
checking derivation checks.x86_64-linux.horizon-definition...
derivation evaluated to /nix/store/pmb2jqgnnyihb557qsbv68rbikd3vk59-horizon-definition.drv
checking derivation checks.x86_64-linux.synchronizer-configuration...
derivation evaluated to /nix/store/l0321dwfyff4n7vmnhgy9m9gmkk6dskm-goldragon-synchronizer-configuration-check.drv
running 2 flake checks...
building '/nix/store/hia0mahvrf7y7s5jrydpjc66n23fkd9b-goldragon-synchronizer.datom.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
copying 1 paths...
copying path '/nix/store/b5pman22ipn9wc1gb2c0xc591jrxivm2-goldragon-synchronizer.datom' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
building '/nix/store/l0321dwfyff4n7vmnhgy9m9gmkk6dskm-goldragon-synchronizer-configuration-check.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
copying 1 paths...
copying path '/nix/store/4y05wrvpw0rw8amlpzm10gmrcbd543x1-goldragon-synchronizer-configuration-check' from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
all checks passed!
warning: The check omitted these incompatible systems: aarch64-linux
Use '--all-systems' to check all.
```

Result: **pass**, exit 0. Offload evidence (the required lines), verbatim:

```
building '/nix/store/hia0mahvrf7y7s5jrydpjc66n23fkd9b-goldragon-synchronizer.datom.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
building '/nix/store/l0321dwfyff4n7vmnhgy9m9gmkk6dskm-goldragon-synchronizer-configuration-check.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
```

No local build was ever attempted or permitted: `--max-jobs 0` throughout, and the third check output (`checks.x86_64-linux.synchronizer`, `synchronizer-0.4.0.drv`) was already realized on the remote builder from an in-progress, separately-observed remote build during this same session (see note below) and required no further local or remote work this pass.

Note on the `synchronizer-0.4.0.drv` build: before the eval-cache-disabled run, a direct `nix build .#checks.x86_64-linux.synchronizer` was issued (also `--max-jobs 0`, same declared builder) to probe why the output was locally absent. It ran to a 300 s timeout mid-build with dozens of `building '…-cargo-package-gix-*.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...` lines (gitoxide crate dependencies of the synchronizer binary) — further, independent offload evidence for that same derivation, on the same declared builder, though not to completion in that one invocation. The subsequent full `nix flake check` (above) found that output already present and did not need to re-drive it.

## Cluster-data assertions (read-only grep of `cluster-definition.datom` at e8ce1e42)

The datom file is single-line; matches are exact substrings from that line.

| Assertion | Found / Missing | Exact text |
|---|---|---|
| ouranos `UsbDownlink.{ 10.44.0.0/24 }` | **Found** | `UsbDownlink.{ 10.44.0.0/24 }` (inside the `ouranos` node's persona/capability list) |
| `TailnetController` with non-`None` CA | **Found** | `TailnetController.{ Some.MIIBzDCCAXOgAwIBAgIUQbqvH0+pYw+hLs93fu1uJKVIgY8wCgYIKoZIzj0EAwIwHzEdMBsGA1UEAwwUZ29sZHJhZ29uIHRhaWxuZXQgQ0EwHhcNMjYwOTI2MDY0OTI3WhcNMzYwOTIzMDY0OTI3WjAfMR0wGwYDVQQDDBRnb2xkcmFnb24gdGFpbG5ldCBDQTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABHVjMZwyWQ9g5jxxi/eV8sQY2uUg0YsbmBuAFnjbfKLUwEBE/UJtDNYUUkYb21r4ynqhGh9DjAl9UyBHvDueC8KjgYwwgYkwHQYDVR0OBBYEFFgEkXZNNg1SuK2NcAikuFcOaKkqMB8GA1UdIwQYMBaAFFgEkXZNNg1SuK2NcAikuFcOaKkqMBIGA1UdEwEB/wQIMAYBAf8CAQAwDgYDVR0PAQH/BAQDAgEGMCMGA1UdHgEB/wQZMBegFTATghEuZ29sZHJhZ29uLmNyaW9tZTAKBggqhkjOPQQDAgNHADBEAiAC/P5/GILXkUTNatmnAoMrspxcttNxTjn3qj//EzXMHwIgKvVV9c1cI1zmWCqvSy+lkBXVdlTLxPqGm8ieN35Rbag= { headscaleTlsCertificate } { headscaleTlsKey } }` (on `ouranos`; CA is `Some.MIIB…` DER-base64, not `None`) |
| Five preauth secret names | **Found, all 5** | `TailnetClient.{ tailnetPreauthKeyMirrorAlpha }` (mirror-alpha), `TailnetClient.{ tailnetPreauthKeyMirrorBeta }` (mirror-beta), `TailnetClient.{ tailnetPreauthKeyOuranos }` (ouranos), `TailnetClient.{ tailnetPreauthKeyPrometheus }` (prometheus), `TailnetClient.{ tailnetPreauthKeyVmTesting }` (vm-testing) |
| Prometheus `NixBuilder Some.8` | **Found** | `NixBuilder.Some.8` (in the `prometheus` node's capability list) |
| Prometheus Metal cores `16` | **Found** | `Metal.{ X86_64 { 16 Some.«GMKtec EVO-X2» None None Some.128 None } }` (on `prometheus`; first field `16` is the core count) |

All six declared assertions are present at this revision; none missing.

Side note (not part of the acceptance contract, observed in passing): the workspace's `secrets/` directory at this revision holds only `localLlmApiToken.sops`, `opencodeServerPassword.sops`, `routerBackupWifiPassword.sops`, `routerWifiSaePasswords.sops` — no `tailnetPreauthKey*.sops` or `headscaleTls*.sops` files exist yet as physical ciphertext in this checkout. The cluster-data assertion above concerns only the *names declared in cluster data*, which are present; whether the ciphertext has been minted for each name is a separate, unverified question this contract did not ask.

## Elapsed time

Approximately 13 minutes, from workspace creation (~2026-09-26 06:58 UTC) through the final passing `nix flake check` (2026-09-26 07:08:51 UTC / 01:08:51 local).

## Scope

Read-only throughout: one new personal jj workspace was added and later left in place (not deleted, not committed to, not pushed); no commits, pushes, deploys, or messages were made against goldragon or any cluster host.
