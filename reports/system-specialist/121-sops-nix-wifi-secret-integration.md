# sops-nix Wi-Fi Secret Integration

Role: system-specialist
Date: 2026-05-14

## Summary

The router Wi-Fi SAE password can be moved out of CriomOS now without
waiting for the full EAP-TLS migration, if the move is shaped as a
`SecretReference` path rather than as "the same password in another Nix
file."

The clean production target is:

- `goldragon` owns the encrypted secret payload.
- `lojix-cli` materializes a `secrets` flake input beside the existing
  generated `horizon`, `system`, and `deployment` inputs.
- `CriomOS` imports `sops-nix`, declares the expected secret by logical
  name, and passes the decrypted runtime path to hostapd through
  `services.hostapd.radios.<radio>.networks.<network>.authentication.saePasswordsFile`.
- Horizon's new schema later names this as
  `WifiAuthentication::Wpa3Sae { password: SecretReference }`; the
  current production bridge can use the same logical name before the new
  Horizon/lojix infrastructure lands.

This keeps the plaintext out of the Nix store and out of process
arguments. The encrypted payload may enter the store; sops-nix is built
for that.

## Primary Sources Checked

- `sops-nix` README: flake import uses `inputs.sops-nix.url =
  "github:Mic92/sops-nix"` and imports `sops-nix.nixosModules.sops`.
- `sops-nix` README: age can decrypt through SSH Ed25519 host keys with
  `sops.age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ]`.
- `sops-nix` README: decrypted system secrets live under `/run/secrets`,
  default to `root:root`, support per-secret mode/owner/group, and can
  restart units on change.
- `sops-nix` README: binary format is supported; for binary secrets one
  encrypted file corresponds to one decrypted secret file.
- NixOS hostapd module in local nixpkgs: inline
  `authentication.saePasswords.*.password` is warned as store-leaking;
  `passwordFile` and `saePasswordsFile` are the intended runtime-file
  paths.

Relevant source URLs:

- <https://github.com/Mic92/sops-nix>
- <https://raw.githubusercontent.com/Mic92/sops-nix/master/README.md>

## Current Production Facts

Pre-implementation leak, now superseded by the implementation status
below:

- `CriomOS/modules/nixos/router/default.nix` hardcodes the WPA3-SAE
  password inline under `services.hostapd`.

Current deploy shape:

- `CriomOS/flake.nix` accepts generated `horizon`, `system`, and
  `deployment` inputs.
- `lojix-cli` materializes those inputs under `~/.cache/lojix/...`,
  computes NAR hashes, and passes them with `--override-input`.
- Remote builds already stage the generated input directories with
  `rsync`, so encrypted secret inputs can use the same path.

Current Horizon shape:

- `horizon-rs` has `RouterInterfaces` but no Wi-Fi policy object and no
  `SecretReference`.
- Existing reports 117, 119, and 120 correctly say not to move the
  plaintext into Horizon. The missing piece is a typed reference to a
  secret payload.

## Recommended First Implementation

### 1. Add a `secrets` flake input to CriomOS

`CriomOS/flake.nix` should grow:

```nix
secrets.url = "path:./stubs/no-secrets";
```

The stub output should expose an empty set:

```nix
{ outputs = _: { sopsFiles = { }; }; }
```

This mirrors the current `system`, `horizon`, and `deployment` input
shape: CriomOS stays network-neutral and receives deploy-specific data
only through flake inputs projected by the deploy tool.

### 2. Import sops-nix in the CriomOS module graph

Add:

```nix
inputs.sops-nix.url = "github:Mic92/sops-nix";
inputs.sops-nix.inputs.nixpkgs.follows = "nixpkgs";
```

Then import `inputs.sops-nix.nixosModules.sops` from a small CriomOS
module, not from router-specific code. That module should set:

```nix
sops.age.sshKeyPaths = [ "/etc/ssh/ssh_host_ed25519_key" ];
```

This uses the existing host SSH Ed25519 private key as the target
decryption key, matching sops-nix's documented age/SSH path. Later,
ClaviFaber can own a dedicated age key if we decide SSH host key reuse
is not the right trust boundary.

### 3. Declare the router Wi-Fi SAE password as a binary secret

For the first production target:

```nix
sops.secrets.router-wifi-sae-passwords = {
  format = "binary";
  sopsFile = inputs.secrets.sopsFiles.routerWifiSaePasswords;
  mode = "0400";
  restartUnits = [ "hostapd.service" ];
};
```

Binary format avoids YAML/JSON secret documents. The decrypted file is
exactly the hostapd SAE password list format: one accepted SAE entry per
line.

### 4. Change hostapd to consume the runtime path

Replace inline `saePasswords = [ { password = ...; } ];` with:

```nix
authentication = {
  mode = "wpa3-sae";
  saePasswordsFile = config.sops.secrets.router-wifi-sae-passwords.path;
};
```

Add explicit service ordering:

```nix
systemd.services.hostapd.after = [ "sops-nix.service" ];
systemd.services.hostapd.requires = [ "sops-nix.service" ];
```

hostapd builds its runtime config in `preStart`, and that preStart reads
the file. The service must not race secret activation.

### 5. Let lojix-cli generate and stage the `secrets` input

Add a `SecretsDir` artifact parallel to `HorizonDir`, `SystemDir`, and
`DeploymentDir`.

For the production bridge, it can discover:

```text
<proposal-repo>/secrets/router-wifi-sae-passwords.sops
```

and write:

```nix
{
  outputs = _: {
    sopsFiles = {
      routerWifiSaePasswords = ./router-wifi-sae-passwords.sops;
    };
  };
}
```

If no known secrets exist, lojix does not pass a `secrets` override and
CriomOS uses `stubs/no-secrets`.

For router nodes, CriomOS should fail closed when the router Wi-Fi
secret is missing. A router configuration that silently starts without
the SAE secret is worse than a failed deploy.

## Encrypted Secret Placement

First file:

```text
goldragon/secrets/router-wifi-sae-passwords.sops
```

Recipients:

- the Prometheus host SSH Ed25519 key converted to age;
- Li's admin/user age recipient, so the operator can rotate the secret;
- later, any replacement router during the dual-radio migration.

No `.sops.yaml` is required for this first step. Use explicit age
recipients when encrypting/updating the file. That keeps the production
data surface free of YAML configuration while we decide how the new
Horizon/lojix infrastructure should model recipient policy.

## Future Horizon Shape

Horizon should eventually carry public, nonsecret metadata only:

```rust
pub struct SecretReference {
    pub source: SecretSource,
    pub name: SecretName,
}

pub enum SecretSource {
    Cluster,
}

pub enum WifiAuthentication {
    Wpa3Sae { password: SecretReference },
    EapTls { /* public certificate policy */ },
}
```

CriomOS should not know `goldragon`, `prometheus`, or any secret file
layout. It should receive a resolved `inputs.secrets.sopsFiles.<name>`
path from lojix and render the service.

The new lojix daemon can replace the production bridge by resolving
`SecretReference` through typed cluster state, but the Nix-side contract
can stay the same: CriomOS gets a `secrets` input with encrypted files.

## Tests To Land With Implementation

Pure CriomOS checks:

- `router_wifi_secret_cannot_be_inline`: source scan rejecting inline
  hostapd SAE password definitions in CriomOS router modules.
- `router_requires_wifi_secret`: synthetic router horizon with no
  `routerWifiSaePasswords` secret must fail evaluation.
- `router_uses_sops_secret_path`: synthetic router horizon plus a fake
  encrypted-file path must evaluate hostapd authentication to
  `saePasswordsFile = config.sops.secrets.router-wifi-sae-passwords.path`.

lojix-cli checks:

- `secrets_input_is_materialized_when_cluster_secret_exists`: artifact
  writer creates a `secrets` flake with `sopsFiles.routerWifiSaePasswords`.
- `nix_invocation_passes_secrets_override`: system builds include
  `--override-input secrets ...` when a secrets artifact exists.
- `remote_stage_copies_secrets_input`: remote build staging includes the
  generated secrets directory beside horizon/system/deployment.

Stateful test:

- A CriomOS-test-cluster nspawn/VM test with a generated age key and a
  dummy sops binary secret should prove `sops-nix.service` decrypts the
  file and hostapd's generated runtime config includes a `sae_password=`
  line from the decrypted path. This can use test-only secret material;
  no production secret should be copied into a test fixture.

## Risks

- If CriomOS consumes the secret before lojix passes the new `secrets`
  input, router deploys fail. That is acceptable only once the lojix side
  lands in the same change wave.
- If hostapd starts before sops-nix, it fails or starts without the
  expected password. Add explicit systemd ordering.
- If the encrypted file is readable only by the router host key and not
  by an operator/admin key, rotation becomes painful. Include an operator
  recipient.
- The encrypted binary file will still be copied to remote builders as
  part of the Nix input. That is acceptable because it is encrypted; the
  plaintext appears only on the target under `/run/secrets`.

## Decision

Use sops-nix for the transitional WPA3-SAE password, but make the
integration a first `SecretReference` implementation rather than a local
Nix cleanup. The durable contract is the `secrets` flake input and the
runtime path consumed by hostapd. Horizon/lojix can evolve behind that
contract without putting secret values into CriomOS or Horizon.

## Implementation Status, 2026-05-14

This report has been forwarded from design into implementation state.
The production sops-nix slice has landed and been pushed in the
production stack:

- `horizon-rs` commit `f4af8b7c`: adds `SecretName` and
  `SecretReference`, and lets `RouterInterfaces` refer to the router
  WPA3-SAE password by logical secret name.
- `goldragon` commit `f0355d50`: stores the transitional router
  password as `secrets/router-wifi-sae-passwords.sops` and points the
  Prometheus router interface at `routerWifiSaePasswords`.
- `lojix-cli` commit `42529ebd`: materializes and stages a generated
  `secrets` flake input beside the existing generated `horizon`,
  `system`, and `deployment` inputs.
- `CriomOS-home` commit `f59ec859`: adds the operator tools needed for
  this flow (`sops`, `age`, `ssh-to-age`) and updates `lojix-cli`.
- `CriomOS` commit `b7b7d504`: imports `sops-nix`, declares the router
  secret from `inputs.secrets.sopsFiles.routerWifiSaePasswords`, passes
  the decrypted runtime path to hostapd via `saePasswordsFile`, and adds
  a pure Nix check rejecting inline `saePasswords`.

Verification completed before the deployment incident:

- `horizon-rs` tests passed.
- `lojix-cli` tests passed.
- Local and remote evaluation for Prometheus showed hostapd now uses
  `saePasswordsFile = "/run/secrets/routerWifiSaePasswords"` and no
  inline `saePasswords`.
- Prometheus's SSH host key could decrypt the staged sops secret through
  the age recipient path, without printing the plaintext.
- Remote Nix evaluation on Prometheus succeeded and returned a system
  derivation path.

## Deployment Incident

The attempted Prometheus `Switch` activation built remotely and reached:

```text
Checking switch inhibitors... done
stopping the following units: hostapd.service
```

After that point the activation produced no useful output for several
minutes. Prometheus became unreachable over the Yggdrasil SSH path; the
local hung `ssh` / `lojix-cli` processes were killed. From the local
machine, the Yggdrasil route still existed, but Prometheus no longer
answered over that path. A local IPv4 scan of the upstream LAN showed
only `ouranos` with SSH open, so Prometheus was not reachable by the
obvious fallback route either.

Treat Prometheus as needing direct recovery or direct local verification.
Do not assume the switch completed. The most likely recovery surface is
the host console, physical access, or a reboot/power path.

Recovery checklist once Prometheus is reachable:

- Check whether the new generation activated:
  `readlink /run/current-system` and
  `readlink /nix/var/nix/profiles/system`.
- Check the units involved in the network cut:
  `systemctl status sops-nix hostapd yggdrasil systemd-networkd`.
- Inspect logs without printing the secret:
  `journalctl -u sops-nix -u hostapd -b --no-pager`.
- Confirm the decrypted secret file exists with restrictive permissions:
  `ls -l /run/secrets/routerWifiSaePasswords`.
- Confirm hostapd generated a runtime config using a file-backed SAE
  path rather than inline Nix material.
- If hostapd failed because the secret was unavailable, start with
  `systemctl restart sops-nix` and then `systemctl restart hostapd`.
- If the system is half-switched and the network cannot be restored,
  roll back to the previous generation from the console, then revisit
  the ordering and activation behavior before another remote switch.

## Still Open

`primary-a61` remains open. This implementation removes the password
plaintext from CriomOS, but the original acceptance criteria are not yet
fully satisfied:

- The SSID and regulatory country policy still need to move out of
  CriomOS and into Horizon-projected Wi-Fi policy.
- The dual-radio migration remains the intended path: keep the current
  password-based WPA3-SAE network while adding the certificate/EAP-TLS
  network on the USB Wi-Fi dongle, migrate clients, then delete the old
  password network.
- CriomOS-test-cluster still needs the broader Wi-Fi constraints for
  synthetic policy, missing secrets, and absence of hard-coded Wi-Fi
  data.
- Prometheus recovery must happen before this can be treated as
  production-proven. The current code has passed evaluation and local
  decryption checks, but the live switch left the router unreachable.

Context-maintenance decision: this report stays as the load-bearing
working artifact for the sops-nix Wi-Fi secret work. No separate
catchall handover report is needed for this topic.
