# Tailnet repair: operator slice for Field (b7da5d)

Subflow of da88cf, 2026-09-25/26 (ouranos clock). This covers the source for the declarative Headscale CA and tailscale enrollment, the secrets Field mints, and the deploy and witness steps. Nothing was activated, deployed, restarted or minted. No secret was created; the only keys made were snakeoil test fixtures committed inside the CriomOS VM test.

Grades: **W** = witnessed by this subflow; **I** = inferred; **U** = unknown.

## 1. What landed, on which bookmarks

| Repo | Bookmark | Revision | Base | Version |
|---|---|---|---|---|
| horizon-rs | `tailnet-repair-da88cf` (and `main`, on the main flow's ruling) | @@HORIZON_REV@@ | `ee8d6f8d` (0.12.0) | 0.13.0 |
| goldragon | `tailnet-repair-da88cf` | @@GOLDRAGON_REV@@ | main `8c4d03de` | data plus Horizon pin |
| CriomOS | `tailnet-repair-da88cf` | @@CRIOMOS_REV@@ | main `d193bafc` | no version surface |

**horizon-rs 0.13.0** is the one schema change for tonight. It is based on the `ee8d6f8d` lineage, the one goldragon and the running `lojix-7.0.0` use. It is not based on the abandoned 0.5.1 `b45d6ad`.

- `TailnetClient.SecretReference` names that node's preauth-key secret.
- `TailnetController.{ Option<CertificateAuthority> TlsCertificateReference TlsKeyReference }` carries the public cluster CA as base64 DER, which stays `None` until it is minted. It also names the server certificate and key secrets.
- `RouterInterfaces` gains an 8th field, `CountryCode`.
- New capability `UsbDownlink.{ Ipv4Cidr }`.

Projections:

```
{ kind = "tailnetClient"; preauthKeyReference; }
{ kind = "tailnetController"; certificateAuthority; tlsCertificateReference; tlsKeyReference; }
routerInterfaces.country
{ kind = "usbDownlink"; ipv4Network; }
```

**goldragon** repins horizon to 0.13.0. It declares the tailnet references below and `country MX` on Prometheus's router. It gives ouranos `UsbDownlink.{ 10.44.0.0/24 }`. Prometheus gets **no** UsbDownlink, because `10.18.0.0/24` is its Router LAN (`CriomOS-lib` `network.lan.subnet`), and a second network with the same CIDR would collide. The controller's CA is `None` on the branch until step 3.6.

**CriomOS**:

- `network/tailnet-roles.nix` (new): one reading of the roles. The controller is found in node ∪ exNodes. The login URL is `https://<controller criomeDomainName>:<constants.network.headscale.port>`. The CA is rewrapped to PEM. It asserts exactly one controller and a declared CA.
- `network/tailnet-trust.nix` (new): `security.pki.certificateFiles` on every tailnet node.
- `network/headscale.nix`:
  - TLS certificate and key come from sops secrets owned by `headscale`, with `restartUnits = headscale`.
  - The self-signed oneshot is **deleted**.
  - `ExecStartPre` refuses to start unless the certificate verifies against the cluster CA for `sslserver` and `-checkhost` matches the node's current `criomeDomainName`. This would have caught the `maisiliym` certificate.
- `network/tailscale.nix`: the "Phase 1 / manual" shape is gone. `tailnet-enroll.service` is a oneshot that reads `BackendState` (it waits up to 30 s while it stays `NoState`). It exits 0 unless the state is `NeedsLogin` or `NoState`. Otherwise it runs:

  ```
  tailscale up --reset --force-reauth --login-server=<URL> --auth-key=file:/run/secrets/<key> --hostname=<node> --accept-dns=false --timeout=90s
  ```

  It has `Restart=on-failure`, 30 s apart. `--accept-dns=false` keeps today's hand-set DNS choice, since dnsmasq forwards the tailnet domain.
- Checks:
  - `checks/headscale-selfsigned-cert` is removed.
  - New `checks/tailnet-declaration` (evaluation contract).
  - New `checks/tailnet-enrollment` (NixOS VM test).
  - `checks/resolver-role-policy` fixture migrated.

## 2. Preconditions and merge order

1. **Repin train first (not done here).** `signal-lojix` and `meta-signal-lojix` embed `HorizonDefinition`, and `lojix` pins `horizon-lib`. All three pin `ee8d6f8d` today. They must repin to horizon @@HORIZON_REV@@ and be published. Then the ouranos Lojix Nexus must run that lojix. Until then, the running Nexus cannot decode the new goldragon definition (**I**, same skew as the 09-20 `proposal source is not a Horizon definition` failure).
2. **Mint the secrets** (§3) into the goldragon checkout on the `tailnet-repair-da88cf` bookmark. Commit and push that bookmark.
3. Merge horizon-rs (already main on the ruling), then goldragon, then CriomOS. CriomOS must also pin the repinned lojix before the ouranos deploy. Otherwise activation restores the old Nexus.
4. The main checkout `/git/github.com/LiGoldragon/goldragon` (the `SecretsDirectory`) must be at the merged goldragon revision when Lojix runs.

Until step 3.6 records the CA, CriomOS evaluation of every tailnet node fails with `tailnet: the TailnetController on ouranos carries no cluster CA certificate`. This is deliberate.

## 3. Secrets: names, recipients, minting

Recipients are each host's age key, derived from its ssh host key in `cluster-definition.datom` with `ssh-to-age` (public data, **W**; ouranos's matches `/etc/ssh/ssh_host_ed25519_key.pub`).

| Secret file (`goldragon/secrets/`) | Consumer | Recipient host | Age recipient |
|---|---|---|---|
| `headscaleTlsCertificate.sops` | headscale on ouranos | ouranos | `age15k8h8e60x9qj558xms2wnc77akupprzsy6k4sg6zvrnk5h7tmgkqz57zf0` |
| `headscaleTlsKey.sops` | headscale on ouranos | ouranos | same |
| `tailnetCertificateAuthorityKey.sops` | none at runtime (kept for reissue) | ouranos | same |
| `tailnetPreauthKeyOuranos.sops` | tailnet-enroll | ouranos | same |
| `tailnetPreauthKeyPrometheus.sops` | tailnet-enroll | prometheus | `age1wgftrgvjduazn8rrz024zj8gpn82cgmm53nmn63uhtaysyk3w3fszqrg3d` |
| `tailnetPreauthKeyMirrorAlpha.sops` | tailnet-enroll | mirror-alpha | `age17xk8r543z4drj2maxz255saq5ma9tpm4xjrq24eh6jx8mffvnvqsk5lf7v` |
| `tailnetPreauthKeyMirrorBeta.sops` | tailnet-enroll | mirror-beta | `age1dhcrc3q3y83k0gv6zezvykdc8yzuyrkpns6u8cdl4uypn6v0pc0qhnwhy0` |
| `tailnetPreauthKeyVmTesting.sops` | tailnet-enroll | vm-testing | `age1hpw6pxxr2ycvahy598cjutmj98wla5tc3w6jeczq8et2vpfjgdrqzhw8pe` |

**Key type: ECDSA P-256** for both the CA and the server.

- Go `crypto/tls` and `crypto/x509` (tailscaled, headscale) verify it natively.
- Unlike Ed25519 certificates, it is also accepted by browsers, Android and every stock TLS stack. That matters for the Unity tailnet app the living described.

The CA carries a critical name constraint `permitted;DNS:.goldragon.criome`, so the cluster-wide trust anchor cannot vouch for any outside name. Go and OpenSSL enforce it (**W** in the VM test with `.criome`).

All steps run as `li` on ouranos. Only `headscale` needs `sudo`. Plaintext keys live only in gopass (the cluster's plaintext store, precedent `localLlmApiToken`) and in pipes. Nothing secret is printed, placed in argv or environment, or written to a temporary file. Public artifacts (CA certificate, CSR, server certificate) go to a scratch directory.

The verified interfaces:
- `sops encrypt … /dev/stdin` with `--filename-override` round-trips on sops 3.13.3 (**W**).
- `gopass cat <name>` reads stdin to store and writes stdout (**W**, help text).
- `headscale preauthkeys create`'s default output is the key alone: the VM test asserts one token on one line (**W** in the test at the nixpkgs pin).

```sh
set -o pipefail
cd /git/github.com/LiGoldragon/goldragon            # jj new tailnet-repair-da88cf first
nix shell nixpkgs#openssl nixpkgs#jq                # openssl is not installed on ouranos
P=$(mktemp -d)                                      # public artifacts only
OURANOS=age15k8h8e60x9qj558xms2wnc77akupprzsy6k4sg6zvrnk5h7tmgkqz57zf0
FQDN=$(nix run .#horizon-cli -- --node ouranos < "$(nix build --no-link --print-out-paths --max-jobs 0 --option fallback false .#horizon-definition)/horizon-definition.datom" | jq -r .node.criomeDomainName)
test "$FQDN" = ouranos.goldragon.criome             # derived from cluster data, checked
```

3.1 CA private key, into gopass then sops:

```sh
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
  | gopass cat goldragon.criome/tailnet/certificate-authority-key >/dev/null
gopass cat goldragon.criome/tailnet/certificate-authority-key \
  | sops encrypt --age "$OURANOS" --input-type binary --output-type json \
      --filename-override secrets/tailnetCertificateAuthorityKey.sops /dev/stdin \
      > secrets/tailnetCertificateAuthorityKey.sops
```

3.2 CA certificate (public), valid 10 years:

```sh
gopass cat goldragon.criome/tailnet/certificate-authority-key \
  | openssl req -x509 -new -key /dev/stdin -sha256 -days 3650 \
      -subj "/CN=goldragon tailnet CA" \
      -addext "basicConstraints=critical,CA:TRUE,pathlen:0" \
      -addext "keyUsage=critical,keyCertSign,cRLSign" \
      -addext "nameConstraints=critical,permitted;DNS:.goldragon.criome" \
      -out "$P/tailnet-ca.pem"
```

3.3 Server key, into gopass then sops; CSR (public):

```sh
openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 \
  | gopass cat goldragon.criome/tailnet/headscale-tls-key >/dev/null
gopass cat goldragon.criome/tailnet/headscale-tls-key \
  | sops encrypt --age "$OURANOS" --input-type binary --output-type json \
      --filename-override secrets/headscaleTlsKey.sops /dev/stdin > secrets/headscaleTlsKey.sops
gopass cat goldragon.criome/tailnet/headscale-tls-key \
  | openssl req -new -key /dev/stdin -subj "/CN=$FQDN" -out "$P/headscale.csr"
```

3.4 Server certificate, SAN = the controller's current name, 825 days:

```sh
printf 'basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature\nextendedKeyUsage=serverAuth\nsubjectAltName=DNS:%s\n' "$FQDN" > "$P/server.ext"
gopass cat goldragon.criome/tailnet/certificate-authority-key \
  | openssl x509 -req -in "$P/headscale.csr" -CA "$P/tailnet-ca.pem" -CAkey /dev/stdin \
      -CAserial "$P/tailnet-ca.srl" -CAcreateserial -sha256 -days 825 \
      -extfile "$P/server.ext" -out "$P/headscale.pem"
openssl verify -CAfile "$P/tailnet-ca.pem" -purpose sslserver "$P/headscale.pem"   # expect: OK
openssl x509 -noout -in "$P/headscale.pem" -checkhost "$FQDN"                      # expect: does match
sops encrypt --age "$OURANOS" --input-type binary --output-type json \
  --filename-override secrets/headscaleTlsCertificate.sops "$P/headscale.pem" > secrets/headscaleTlsCertificate.sops
```

3.5 Preauth keys, one reusable key per host, one year. Find the user ID once (`sudo headscale users list`; the persisted ouranos profile suggests ID 1 `li`, **U**). If there is none, run `sudo headscale users create li`. Then, for each row `NAME RECIPIENT` of the table above (Ouranos, Prometheus, MirrorAlpha, MirrorBeta, VmTesting):

```sh
sudo headscale preauthkeys create --user <ID> --reusable --expiration 8760h \
  | sops encrypt --age <RECIPIENT> --input-type binary --output-type json \
      --filename-override secrets/tailnetPreauthKey<NAME>.sops /dev/stdin \
      > secrets/tailnetPreauthKey<NAME>.sops
```

3.6 Record the public CA in cluster data (not secret):

```sh
CA=$(openssl x509 -in "$P/tailnet-ca.pem" -outform DER | base64 -w0)
sed -i "s|TailnetController.{ None {|TailnetController.{ Some.$CA {|" cluster-definition.datom
grep -c 'TailnetController.{ Some.MII' cluster-definition.datom                   # expect: 1
```

3.7 Check ciphertext only, one recipient each, then commit and push the bookmark:

```sh
for f in secrets/headscaleTls*.sops secrets/tailnet*.sops; do jq -e '.data and (.sops.age|length==1)' "$f" >/dev/null && echo "$f ok"; done
nix flake check --max-jobs 0 --option fallback false
jj commit -m '(("Secret", "tailnet"), ("Add", "cluster CA, Headscale TLS and per-host preauth ciphertext"), ("Verdict", "tailnet trust and enrollment are declared by cluster data"))'
jj bookmark set tailnet-repair-da88cf -r @- && jj git push --bookmark tailnet-repair-da88cf
rm -r "$P"
```

## 4. Deploy (after §2)

`<P>` is the store path of `nix build --max-jobs 0 --option fallback false github:LiGoldragon/goldragon/<merged rev>#horizon-definition`, and `<C>` is the merged CriomOS revision (40 hex). Each form follows `flows/00f95a/materialization-ouranos-flow-0.10.7/lojix-evaluate.request` (current Lojix 7 grammar) and the succeeded Zeus family in `flows/0384e0/witnesses/zeus-deployment.md` (Evaluate, then Realize, then activate). Submit each one only after the previous one reaches terminal `Succeeded` (`lojix 'Query.ByDeployment.<id>'`).

**Ouranos first** (controller, so the SAN-matching certificate is served before clients enroll):

```text
LOJIX_OWNER_SOCKET=/run/lojix/meta.sock lojix-meta 'Deploy.Host.{ goldragon ouranos CompleteHost <P>/horizon-definition.datom SecretsDirectory./git/github.com/LiGoldragon/goldragon/secrets github:LiGoldragon/CriomOS?rev=<C> { ssh-ng://root@ouranos.goldragon.criome root@ouranos.goldragon.criome } Horizon { nixosConfigurations.target.config.system.build.toplevel } NixosSystemdBootV1 Evaluate RequireImmutable Some.@/etc/nix/machines [] }'
```

Then the same request with `Realize`, then with `ActivateNow`.

**Prometheus second.** Use the same shape with `prometheus` and `{ ssh-ng://root@prometheus.goldragon.criome root@prometheus.goldragon.criome }`: `Evaluate`, `Realize`, then `ScheduleBootOnce` and an attended reboot. CriomOS ARCHITECTURE requires BootOnce on large-AI nodes unless the living waives it. `ActivateNow` applies only under such a waiver.

On ouranos the enroll unit passes `--force-reauth --reset`. This drops the hand-set `https://127.0.0.1:8443` login, and Headscale registers ouranos as a new node. The stale node (ID 2) can then be removed with `sudo headscale nodes delete -i 2` once `nodes list` shows the new one.

## 5. Post-activation witness

On ouranos:

```sh
systemctl status headscale.service tailnet-enroll.service --no-pager
journalctl -u headscale.service -b --no-pager | grep -E 'does match|OK|error'
tailscale status
tailscale debug prefs | jq -r .ControlURL          # https://ouranos.goldragon.criome:8443
sudo headscale nodes list                          # ouranos and prometheus, online
openssl s_client -connect ouranos.goldragon.criome:8443 -servername ouranos.goldragon.criome \
  -CAfile /etc/ssl/certs/ca-certificates.crt -verify_return_error -verify_hostname ouranos.goldragon.criome </dev/null \
  | openssl x509 -noout -subject -issuer -ext subjectAltName   # SAN DNS:ouranos.goldragon.criome, issuer goldragon tailnet CA
```

On prometheus:

```sh
tailscale status                                   # ouranos listed as a peer
tailscale ping ouranos
journalctl -u tailnet-enroll.service -b --no-pager
```

If the enroll unit is re-run on a healthy node, it logs `already enrolled, not re-registering` and `nodes list` stays unchanged.

## 6. Test and check results

@@RESULTS@@

## 7. Side findings

- `goldragon/secrets/opencodeServerPassword.sops` has one recipient, `age1wgft…` = **prometheus**. Its consumer is ouranos's `OpenCodeTesting`, so ouranos cannot decrypt it (**W** recipients, **I** failure).
- CriomOS main's flake `checks` attribute does not evaluate. A pin assertion compares CriomOS-home `478b4ea0…` with `f652ba9a…` and fails inside `blueprintChecks`. The checks here were run by `callPackage` on each check directory with the flake's own inputs (**W**).
- Flow 542442 holds lock 907 on a CriomOS worktree that edits `checks/headscale-selfsigned-cert`, which this branch deletes. Expect a merge conflict there. Take the deletion.
- With the client module, a client's activation reports `tailnet-enroll` failed while the controller is unreachable. The unit retries every 30 s (**I**).

## Sources

- `flows/da88cf/reports/headscale-repair.md`; `flows/f5a74e/reports/cluster-topology-roles.md` (tailnet section); `flows/da88cf/reports/prometheus-pending.md` §4; `flows/da88cf/reports/daisy-chain-plan.md` §3; `flows/f38926/log.md` (09-20 repin train); `flows/00f95a/materialization-ouranos-flow-0.10.7/`; `flows/0384e0/witnesses/zeus-deployment.md`.
- horizon-rs `ee8d6f8d`, goldragon `8c4d03de`, CriomOS `d193bafc`, lojix `a67f5773` (`lojix-horizon-datom31-00f95a`), signal-lojix `f7866bf0`, meta-signal-lojix `b500561f`; the running Nexus `lojix-7.0.0`.
- Subflow transcript `da88cf8d-06f7-4a70-9c7a-e7c8cdb78908`; build logs in its scratchpad `tailnet-impl/`.
