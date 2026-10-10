# Mint Pipe Ruling Findings

## Recorded Design Sources

- Flows/da88cf report: flows/da88cf/reports/tailnet-repair-slice.md §3 (sections 3.1–3.5)
- GO MINT ruling: da88cf log entries 36, 134
- Scope: ouranos and Prometheus subset (da88cf log entry 155)
- CA key and TLS key handling: producer → `gopass cat NAME >/dev/null`, then `gopass cat NAME | sops encrypt --age <recipient> --input-type binary --output-type json --filename-override … /dev/stdin`
- TLS certificate: public, encrypted from scratch file
- Preauth keys: `ssh root@ouranos headscale preauthkeys create … | sops encrypt …` (no gopass, no jq)
- Recipients (ssh-to-age from cluster-definition.datom): ouranos age15k8h8e60x9qj558xms2wnc77akupprzsy6k4sg6zvrnk5h7tmgkqz57zf0 (verified against live host), Prometheus age1wgftrgvjduazn8rrz024zj8gpn82cgmm53nmn63uhtaysyk3w3fszqrg3d (verified)
- Mirror hosts (mirror-alpha, mirror-beta, vm-testing): recipients unverified
- SKILL_VARIABLES.md: no gopass/sops/age entries present

## Root Cause

**Environment:** ouranos, gopass 1.16.1, isolated throwaway store (--crypto plain --storage fs), not the real store (which has core.autopush = true)

**Issue:** `gopass cat NAME` enters write mode whenever stdin is not a character device. Under a piped harness, stdin is inherited as a pipe, and the read step enters write mode, reads the empty pipe as input, and overwrites the entry with 0 bytes. OpenSSL then fails ("Could not find private key"), and the entry remains at 0 bytes.

**Reproduction:** 
- Write ok, bare readback 0 bytes
- "Could not find private key" error
- Entry left at 0 bytes (sha256 e3b0c442… — empty)

## Fix Validated

**Working method:** `gopass cat NAME </dev/null`

- Redirects stdin from /dev/null
- Returns exact bytes on readback
- 32 random bytes: sha256 07680278…5796 (original and readback verified)
- 241-byte P-256 PEM: openssl pkey -check confirms "Key is valid"
- Through sops encrypt→decrypt to throwaway age key: sha256 773984ee…728e preserved

**Invalid reads:**
- `gopass show -o` on binary: fails with "no password to display"
- `gopass show -n`: prints MIME/base64 wrapper (sha256 69ef3213…), not raw bytes

## Write × Read Validation Table

| Write Method | Read Method | 32 Random Bytes | 241-byte P-256 PEM | Notes |
|--------------|-------------|-----------------|-------------------|-------|
| `gopass cat NAME` (stdin) | `gopass cat NAME </dev/null` | EXACT | EXACT | openssl pkey accepts; validated method |
| `gopass insert --force NAME` (stdin) | `gopass cat NAME </dev/null` | 33 bytes (not exact) | EXACT | Not authorized for these keys |
| `gopass insert --force NAME` (stdin) | `gopass insert -n NAME` | 33 bytes | EXACT | Not authorized |
| `gopass insert --force NAME` (stdin) | `gopass show -o` | 27 bytes | 27 bytes (first line only) | Not usable |
| `gopass cat NAME` (stdin) | `gopass show -n` | MIME/base64 wrapper | MIME/base64 wrapper | Not raw bytes |
| `gopass cat NAME` (stdin) | `gopass show -o` | 0 bytes | 0 bytes | No output |
| Any write | `gopass cat NAME` (piped stdin) | 0 bytes, entry erased | 0 bytes, entry erased | Failure mode; corrupts entry |

## Authorized Pipeline

**Bash commands with `set -o pipefail`, inside `nix shell nixpkgs#openssl`:**

1. **CA key:**
   ```
   openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 | gopass cat goldragon.criome/tailnet/certificate-authority-key >/dev/null
   gopass cat goldragon.criome/tailnet/certificate-authority-key </dev/null | sops encrypt --age "$OURANOS" --input-type binary --output-type json --filename-override secrets/tailnetCertificateAuthorityKey.sops /dev/stdin > secrets/tailnetCertificateAuthorityKey.sops
   ```

2. **CA certificate and server certificate signing** (matching slice §3.2 and §3.4):
   - CA key fed by: `gopass cat goldragon.criome/tailnet/certificate-authority-key </dev/null | openssl ... -key /dev/stdin` or `-CAkey /dev/stdin`

3. **TLS key:**
   ```
   openssl genpkey -algorithm EC -pkeyopt ec_paramgen_curve:P-256 | gopass cat goldragon.criome/tailnet/headscale-tls-key >/dev/null
   gopass cat goldragon.criome/tailnet/headscale-tls-key </dev/null | sops encrypt --age "$OURANOS" --input-type binary --output-type json --filename-override secrets/headscaleTlsKey.sops /dev/stdin > secrets/headscaleTlsKey.sops
   ```

4. **CSR generation:**
   ```
   gopass cat goldragon.criome/tailnet/headscale-tls-key </dev/null | openssl req -new -key /dev/stdin -subj "/CN=$FQDN" -out "$P/headscale.csr"
   ```

5. **TLS certificate (public):**
   ```
   sops encrypt --age "$OURANOS" --input-type binary --output-type json --filename-override secrets/headscaleTlsCertificate.sops "$P/headscale.pem" > secrets/headscaleTlsCertificate.sops
   ```

6. **Preauth keys (ouranos and Prometheus only):**
   ```
   ssh root@ouranos.goldragon.criome headscale preauthkeys create --user <ID> --reusable --expiration 8760h </dev/null | sops encrypt --age <RECIPIENT> --input-type binary --output-type json --filename-override secrets/tailnetPreauthKey<NAME>.sops /dev/stdin > secrets/tailnetPreauthKey<NAME>.sops
   ```
   - Recipients: ouranos age15k8h8e60x9qj558xms2wnc77akupprzsy6k4sg6zvrnk5h7tmgkqz57zf0, Prometheus age1wgftrgvjduazn8rrz024zj8gpn82cgmm53nmn63uhtaysyk3w3fszqrg3d

## Security Constraints

- No command substitution on secrets
- No temporary files for secrets
- No tee or filters on secret-bearing output
- Secret-bearing output redirected to `/dev/null`
- Real gopass store has autosync/autopush on: each write is committed and pushed as encrypted content
- Empty entries from failed attempts must be overwritten (write step does this) or removed with `gopass rm -f`

## Self-Test Procedure

Before minting, self-test with a throwaway entry under scratch/b860be-selftest:
1. Write 32 random bytes from a scratch file with `gopass cat`
2. Read back with `gopass cat NAME </dev/null`
3. Compare sha256
4. Remove with `gopass rm -f`

## Validation Form

Set `-o pipefail` and validate with:
```
gopass cat NAME </dev/null | openssl pkey -noout
```

This form is safe in a harness (stdin redirected, not piped to gopass read operation).

## Status

- Ruling sent to b7da5d with receipt `Transported.{ b7da5d done }`
- Addendum sent to b7da5d with receipt `Transported.{ b7da5d done }` (addressing gopass insert --force alternative, confirmed not authorized)
