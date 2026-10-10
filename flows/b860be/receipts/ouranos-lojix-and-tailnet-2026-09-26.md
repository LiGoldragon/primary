# Ouranos Lojix state and tailnet secret minting — live-state witness

Subflow of b860be, 2026-09-26 00:43 CST. Passive observation only; nothing was
mutated, no lock was taken, no message was sent. Grades: **W** = witnessed
here, live, this run.

## A. Lojix state for ouranos (goldragon cluster)

Client: `lojix` (ordinary socket). Environment already carried
`LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock` (confirmed present:
`/run/lojix/ordinary.sock` exists, srw-rw----, owned by `li:users`); this
value was used as-is, not guessed. Cluster name `goldragon` taken from the
goldragon checkout's own cluster data (`cluster-definition.datom`, top-level
name field) and matches every da88cf report's usage.

### `Query.ByNode.{ goldragon ouranos None }` — exact command and reply (W)

```
$ lojix 'Query.ByNode.{ goldragon ouranos None }'
```

Generation list (`Queried.{ [generations] [deployments] {cursor} }`, first
vector) — deployment-relevant generations for ouranos:

| Generation id | Kind | Activation | Status | Drv/output | Commit |
|---|---|---|---|---|---|
| 3 | CompleteHost | LiveActivation | Recent | `.../bbmk2cxk...-nixos-system-ouranos-26.11.20260813.0e251e2` | `477beac0...` |
| **4** | CompleteHost | LiveActivation | **Current** | `.../41cvi7l9...-nixos-system-ouranos-26.11.20260813.0e251e2` | `36653a12...` |
| 13 | UserEnvironment | LiveActivation | Recent | `.../xb15yxds...-home-manager-generation` | `eb614bf9...` |
| 15 | UserEnvironment | LiveActivation | Recent | `.../rl7ghdjp...-home-manager-generation` | `7f9f7be2...` |
| 21 | UserEnvironment | ProfileOnly | Recent | `.../d0ny8fwv...-home-manager-generation` | `63edfc9f...` |
| **27** | UserEnvironment | LiveActivation | **Current** | `.../y2mh6aji...-home-manager-generation` | `cef11110...` |

**Current generation: host generation 4 (CompleteHost, commit `36653a125de8f14518af2dddf89333610891d140`); user-environment generation 27 (commit `cef111108623617987b6e366ccbe4176c093d6b5`).** Both witnessed directly in the `Queried` reply's generation vector, each explicitly tagged `Current`.

Deployment ledger (second vector) includes deployment **32**:

```
{ 32 32 { HostEnvironment goldragon ouranos CompleteHost Host.Realize LiveActivation RequireImmutable Some.3e2cc8be83f03859dc4fafe6ddba17280c488e22 } Some.{ 766 766 } Failed Some.{ 780 780 } Some.Failed.{ Eval EvaluationFailed Some.{ Some.{ nix eval ... github:LiGoldragon/CriomOS?rev=3e2cc8be83f03859dc4fafe6ddba17280c488e22#nixosConfigurations.target.config.system.build.toplevel.drvPath } ... } True } }
```

Terminal reason for 32: `Failed.{ Eval EvaluationFailed }` — the nix evaluation
at CriomOS rev `3e2cc8be83f03859dc4fafe6ddba17280c488e22` failed with `Failed
assertions:` (stack trace truncated in the reply) after also hitting the
prometheus binary-cache timeout noise; underlying nix error text is
"Failed assertions:" at `nixos/modules/system/activation/top-level.nix`. This
is a real terminal record (Failed), not absence of one.

The reply's cursor is `{ 784 784 }` (event-log position), confirming 32 is the
highest deployment recorded as of this witness.

### `Query.ByDeployment.{ <n> }` for 32 and above — exact commands and replies (W)

```
$ lojix 'Query.ByDeployment.{ 32 }'
→ Queried.{ [] [ { 32 32 ... Failed Some.{ 780 780 } Some.Failed.{ Eval EvaluationFailed ... } } ] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 33 }'
→ Queried.{ [] [] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 34 }'
→ Queried.{ [] [] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 35 }'
→ Queried.{ [] [] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 36 }'
→ Queried.{ [] [] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 37 }'
→ Queried.{ [] [] { 784 784 } }

$ lojix 'Query.ByDeployment.{ 38 }'
→ Queried.{ [] [] { 784 784 } }
```

**Deployment 32 is the only deployment id newer than 31 that exists** in the
store as of this witness. Deployment ids 33–38 all return an empty deployment
vector (`[]`), meaning no such deployment record exists — not "still
running", genuinely absent. The cursor stays `{ 784 784 }` throughout, so no
new deployment landed between queries in this run.

**Terminal state of deployment 32 (only deployment > 31):** `Failed.{ Eval EvaluationFailed }` — terminal, present.

**Non-terminal deployments now: none witnessed.** Deployment 32 is terminal
(Failed); deployments 33+ do not exist. No deployment above 31 is in flight.

**A: witnessed.**

## B. Tailnet secret minting (goldragon repository)

Repository path from `flows/da88cf/reports/tailnet-repair-slice.md`:
`/git/github.com/LiGoldragon/goldragon` (the checkout also serves as the
`SecretsDirectory`; `goldragon/secrets` is a subdirectory of this same
repository, not a separate checkout — confirmed by `jj file list`, no
separate `goldragon/secrets` repo exists at that path).

All checks below are `jj log`, `jj bookmark list`, `jj file list -r <rev>` —
read-only, no mutation.

### Bookmark existence and revision (W)

```
$ jj bookmark list | grep -i tailnet
tailnet-repair-da88cf: suqttyoq a3fdb232 (("Cluster", "tailnet"), ("Add", "Horizon 0.13.0 tailnet secret references, router country MX, ouranos USB downlink, Prometheus-only builder at eight jobs"), ("Verdict", "tailnet trust and enrollment are named by cluster data; CA awaits minting"))
```

**Bookmark `tailnet-repair-da88cf` exists**, at revision
`a3fdb232d4fd3d6ef752f64e85546749a1f87b28` (change id `suqttyoq`). This
matches the revision already reported by `flows/da88cf/reports/integration-2.md`.

### Descent from goldragon main (W)

```
$ jj log -r 'main' --no-graph -T 'commit_id'
0d462a339e06fc9a90c10affbde0e08d6829744d

$ jj log -r 'ancestors(tailnet-repair-da88cf) & main' --no-graph -T 'commit_id'
(empty)

$ jj log -r '(ancestors(tailnet-repair-da88cf) & ancestors(main))' --no-graph -T 'commit_id ++ "\n"'
8c4d03de76907f590072c0998b00037330ebcd8
2820bd436cb1b49ff4a435c36004744f4459be3
199f5eb107d91b9a468cafd09d1b6dc7119df70e
1f49f8dea50932cacc781d531c48b6d20805b439
89b07e20825a2c4707af0cec4fb86d03b9b0b299
...
```

Current goldragon `main` is `0d462a339e06fc9a90c10affbde0e08d6829744d`. The
merge base of the bookmark and current main is `8c4d03de76907f590072c0998b00037330ebcd8`,
**not** current main. **The bookmark does NOT descend from current goldragon
main** — it branched from an older point (`8c4d03de`, matching the base
already named in `tailnet-repair-slice.md`) and main has since advanced past
it (to `0d462a33`, "secrets: add Ouranos OpenCode password recipient",
per `flows/da88cf/reports/integration-2.md`). This is a live, current-state
fact, independent of what any flow claims about it.

### Secret files for CA, TLS, and the five preauth keys (file names only — W)

Expected file names, per `flows/da88cf/reports/tailnet-repair-slice.md` §3:
`tailnetCertificateAuthorityKey.sops`, `headscaleTlsCertificate.sops`,
`headscaleTlsKey.sops`, `tailnetPreauthKeyOuranos.sops`,
`tailnetPreauthKeyPrometheus.sops`, `tailnetPreauthKeyMirrorAlpha.sops`,
`tailnetPreauthKeyMirrorBeta.sops`, `tailnetPreauthKeyVmTesting.sops`.

```
$ jj file list -r 'tailnet-repair-da88cf' | grep -i secrets/
secrets/localLlmApiToken.sops
secrets/opencodeServerPassword.sops
secrets/routerBackupWifiPassword.sops
secrets/routerWifiSaePasswords.sops

$ jj file list -r 'main' | grep -i secrets/
secrets/localLlmApiToken.sops
secrets/opencodeServerPassword.sops
secrets/routerBackupWifiPassword.sops
secrets/routerWifiSaePasswords.sops
```

**None of the eight expected tailnet secret file names exist**, on either the
bookmark or main. Only four pre-existing, unrelated secrets are present
(`localLlmApiToken.sops`, `opencodeServerPassword.sops`,
`routerBackupWifiPassword.sops`, `routerWifiSaePasswords.sops`) — none of
these is a CA, TLS, or preauth-key secret. File names only were inspected;
no file content was read.

There is no separate `goldragon/secrets` repository or directory distinct
from `<repo>/secrets/` — the same `jj file list` covers it.

### CA recorded on the bookmark (W)

`cluster-definition.datom` on the bookmark carries, for `ouranos`:

```
TailnetController.{ None { headscaleTlsCertificate } { headscaleTlsKey } }
```

The first field (`Option<CertificateAuthority>`) is `None`. **The CA is not
recorded on the bookmark.** This matches the bookmark's own commit message
verdict ("CA awaits minting"). Cluster data does name the TLS certificate and
key secret references (`headscaleTlsCertificate`, `headscaleTlsKey`) and each
node's preauth-key secret reference (e.g. `TailnetClient.{
tailnetPreauthKeyOuranos }` on ouranos, `tailnetPreauthKeyPrometheus` on
prometheus, `tailnetPreauthKeyMirrorAlpha`/`MirrorBeta` on the two mirrors,
`tailnetPreauthKeyVmTesting` on vm-testing) — the references exist in cluster
data, but the secret files themselves do not exist in the repository.

**B: witnessed. Not minted (0 of 8 expected secret files present, on
bookmark or main). CA not recorded on the bookmark (`None`). Bookmark exists
but does not descend from current goldragon main** (forked at `8c4d03de`;
main has since moved to `0d462a33`).

## C. `date`

```
$ date
Sat Sep 26 12:43:30 AM CST 2026
```

**C: witnessed.**
