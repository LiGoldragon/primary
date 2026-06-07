# Skill — secrets

*Handling secret material so it is never seen, never logged, and never
lands anywhere but an encrypted store. Two layers: gopass in the user
session, sops-nix on cluster hosts.*

## The absolute: an agent never sees a secret value

A secret value never reaches the agent's eyes or any durable surface.
Everything else here serves this rule. A secret must never appear in:

- stdout/stderr of any command you run;
- a log line, report, chat message, or commit message;
- a command's `argv` (visible to any `ps` on the box);
- a shell trace (`set -x` while a secret variable is live);
- the nix store, a test fixture, or a checked-in plaintext file.

How to work and still satisfy the rule:

- **Pipe source to sink.** Move a secret by connecting the producer's
  stdout to the consumer's stdin. The value lives only in the pipe
  buffer and the two processes' memory, never on a terminal.
- **Verify blind.** Confirm success by exit code, by byte length
  (`... | wc -c`), by an entry name (`gopass ls | grep -F <name>`
  lists names, never values), or by ciphertext markers
  (`grep ENC\[ <file>.sops`). Never decrypt-to-check.
- **Public keys are public.** Age recipients, nix cache public keys,
  and ssh public keys are not secrets — they may appear in `argv` and
  output freely. Only the secret bytes are forbidden.

## Two layers: gopass for the session, sops-nix for the cluster

- **gopass** encrypts secrets within the user session — git-backed,
  per-user, decrypted on demand through the user's own key. It is the
  human-controlled source of truth for interactive and development use.
- **sops-nix** carries secrets to cluster hosts. The secret is
  encrypted at rest in the repository (only ciphertext is committed)
  and decrypted **only on the target host at activation**, into a
  runtime tmpfs at `/run/secrets/<name>`.

These compose: mint a secret into gopass, then bridge it into a sops
file for deployment. The *plaintext* never enters the nix store; the
sops file holds only ciphertext, and decryption happens at activation
outside the store.

## gopass: wrapping environment variables at the daemon-wrapper layer

A binary that needs a secret in an environment variable is **wrapped**
so the secret is fetched fresh at exec time, never baked into the
package or the systemd unit:

```nix
pkgs.symlinkJoin {
  name = "flarectl-wrapped";
  paths = [ pkgs.flarectl ];
  nativeBuildInputs = [ pkgs.makeWrapper ];
  postBuild = ''
    wrapProgram $out/bin/flarectl \
      --run 'export CF_API_TOKEN=$(${pkgs.gopass}/bin/gopass show -o cloudflare/api-token)'
  '';
}
```

The secret is read at each invocation (rotation needs no rebuild),
never stored in the store path, never written to the unit file.
Command substitution `$(...)` strips the trailing newline, so the
exported value is the clean secret.

**Path conventions.** Provider-scoped for an external provider's single
global credential (`cloudflare/api-token`); zone-scoped for a local
service in a cluster zone
(`goldragon.criome/local-llm-api-token`) so the path survives the
service moving between hosts.

## Minting a secret without seeing it

Generate with a CSPRNG and pipe straight into the store; never echo the
generated value:

```sh
token=$(head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n')   # 256-bit hex
printf '%s\n' "$token" | gopass insert -f <path> >/dev/null
```

Confirm by exit code and `gopass ls | grep -F <name>`. Make minting
idempotent: refuse to overwrite an existing entry unless an explicit
`--rotate` flag is given, because rotation forces every consumer to
re-read.

## sops-nix: how cluster secrets decrypt on the host

- **Host key.** Decryption uses the host's SSH ed25519 key converted to
  age (`sops.age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ]`).
  No separate per-host age key file to manage.
- **Recipient.** Encrypt to the host's age recipient, derived from its
  ssh public key: `echo 'ssh-ed25519 <body>' | ssh-to-age`. Cross-check
  the derived value against the recipient on an existing working secret
  before trusting it — encrypting to the wrong key fails silently (the
  host simply cannot decrypt).
- **File shape.** The binary store: a JSON file
  `{"data":"ENC[AES256_GCM,...]","sops":{"age":[{recipient,enc}]}}`,
  consumed with `format = "binary"`.
- **Declaration.** In a host module:

  ```nix
  sops.secrets.<name> = {
    format = "binary";
    sopsFile = <the .sops file>;
    owner = "<service-user>";
    mode = "0400";
    restartUnits = [ "<service>.service" ];
  };
  ```

  The service reads `config.sops.secrets.<name>.path`
  (`/run/secrets/<name>`). Rotation is handled by `restartUnits`.
- **Deploy wiring is per-cluster.** How the encrypted file becomes a
  flake input the host config references is the deploy tooling's job;
  consult the cluster repo's own docs.

## The blind bridge: gopass to sops-nix

Move a secret from gopass into a sops file without ever exposing it:

```sh
gopass show -o <gopass-path> \
  | sops --encrypt --age <recipient-public-key> \
      --input-type binary --output-type binary /dev/stdin \
  > <file>.sops
```

The plaintext flows gopass → pipe → sops; it never touches a terminal
or `argv`. The recipient is a public key, safe on the command line.
`gopass show` triggers decryption (the pinentry prompt is the human
unlocking their own store) — the agent still never sees the value.
Verify blind: `grep ENC\[ <file>.sops` for encryption and
`grep -oE 'age1[a-z0-9]+' <file>.sops` for the recipient set.

## See also

- `skills/system-operator.md` — deploy surface; keys come from gopass
  at the daemon-wrapper layer.
- `skills/nix-discipline.md` — services as NixOS modules; store-path and
  secret-state hygiene.
