# 1 · sops-nix infrastructure (scout synthesis)

## How it works in this cluster

- **No `.sops.yaml`.** There is no creation-rules file. Secrets are
  encrypted ad-hoc with explicit `--age <recipient>` on the `sops`
  command line. Recipients are named per-encryption, not by path regex.
- **Host decryption key = SSH host key via ssh-to-age.**
  `CriomOS/modules/nixos/secrets.nix:7` sets
  `sops.age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ]`. No
  dedicated age key files; the host's ed25519 key decrypts.
- **prometheus is already a valid recipient.** Its ssh host pubkey
  (`goldragon/datom.nota:80`) converts via `ssh-to-age` to
  `age1wgftrgvjduazn8rrz024zj8gpn82cgmm53nmn63uhtaysyk3w3fszqrg3d`,
  which is the sole recipient on the one existing encrypted secret.
  Verified independently in this cycle (derivation matched the
  recipient on the working file). prometheus also carries the router
  interface, which is why that secret targets it.
- **Existing secret + format.** Exactly one:
  `goldragon/secrets/router-wifi-sae-passwords.sops`. sops-JSON binary
  store: `{"data":"ENC[AES256_GCM,...,type:str]","sops":{"age":[{recipient,enc}]}}`.
  Consumed with `format = "binary"`.
- **Declaration shape** (`CriomOS/modules/nixos/router/default.nix:57`):
  `sops.secrets.<name> = { format = "binary"; sopsFile = inputs.secrets.sopsFiles.<name>; mode = "0400"; restartUnits = [ ... ]; };`
  The service reads `config.sops.secrets.<name>.path` (= `/run/secrets/<name>`).
  sops-install-secrets runs at activation before services start.

## The structural blocker

`lojix-cli` **hardcodes** the secret set. `lojix-cli/src/artifact.rs`
(`SECRETS_FLAKE_TEMPLATE`, ~lines 18–26 + copy at 151–184) generates a
secrets flake exposing ONLY `routerWifiSaePasswords = ./router-wifi-sae-passwords.sops`.
It does not enumerate the `secrets/` directory. There is no generic
"add a secret" path, no `.sops.yaml` + `sops updatekeys` workflow, and
no helper script.

**Consequence:** deploying a new sops secret (the llm api token)
through lojix requires a **Rust change to lojix-cli** — either adding
the file to the hardcoded template, or (better) generalizing it to
enumerate the directory. lojix-cli is the cluster deploy tooling, on
the system-operator surface.

## Recipe to add a prometheus-readable secret

1. Encrypt into the data repo (this cycle did this, blind):
   `gopass show -o <path> | sops --encrypt --age <prometheus-recipient> --input-type binary --output-type binary /dev/stdin > goldragon/secrets/<name>.sops`
2. Expose it through `lojix-cli/src/artifact.rs` (Rust change).
3. Declare `sops.secrets.<name>` in a prometheus-gated module and point
   the consumer at `config.sops.secrets.<name>.path`.
4. Deploy via lojix (file 3).
