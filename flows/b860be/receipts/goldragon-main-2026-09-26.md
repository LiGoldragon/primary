# goldragon main move — 2026-09-26

Task: move goldragon `main` to carry the tailnet bookmark. Workspace:
`/home/li/wt/github.com/LiGoldragon/goldragon-b860be-check` (pre-existing, reused).

## 1. Fetch and ancestry check

```
$ jj git fetch
Nothing changed.
```

Expected starting `main` (mint commit): `3e6ecfa92944c0113b192314f9c4a66cb33f1cb7` — confirmed present:

```
$ jj log -r 'main' --no-graph -T 'commit_id ++ "\n"'
3e6ecfa92944c0113b192314f9c4a66cb33f1cb7
```

`tailnet-repair-da88cf` confirmed at `e8ce1e42be4644b4e96cac1bcba6a8b1b4232563`:

```
$ jj log -r 'tailnet-repair-da88cf' --no-graph -T 'commit_id ++ "\n"'
e8ce1e42be4644b4e96cac1bcba6a8b1b4232563
```

Ancestry, both directions:

```
$ jj log -r '3e6ecfa92944c0113b192314f9c4a66cb33f1cb7::e8ce1e42be4644b4e96cac1bcba6a8b1b4232563' --no-graph -T 'commit_id ++ "\n"'
(empty)
$ jj log -r 'e8ce1e42be4644b4e96cac1bcba6a8b1b4232563::3e6ecfa92944c0113b192314f9c4a66cb33f1cb7' --no-graph -T 'commit_id ++ "\n"'
(empty)
$ jj log -r 'fork_point(3e6ecfa92944c0113b192314f9c4a66cb33f1cb7|e8ce1e42be4644b4e96cac1bcba6a8b1b4232563)' --no-graph -T 'commit_id ++ "\n"'
0d462a339e06fc9a90c10affbde0e08d6829744d
```

**Answer: no** — `main` (3e6ecfa9) is not an ancestor of `tailnet-repair-da88cf`
(e8ce1e42), and neither is `tailnet-repair-da88cf` an ancestor of `main`. The
two diverged at merge base `0d462a339e06fc9a90c10affbde0e08d6829744d`
("secrets: add Ouranos OpenCode password recipient"). `main`'s branch minted
tailnet secret ciphertexts (CA key, Headscale TLS, verified-host preauth);
`tailnet-repair-da88cf`'s branch declared the tailnet cluster data / CA
trust anchor (a merge commit itself, built on `a3fdb232d4fd` etc.).

## 2. Merge commit (since answer was "no")

```
$ jj new main tailnet-repair-da88cf -m 'Merge tailnet-repair-da88cf into main'
Working copy  (@) now at: ovuwnxus ddf27e0c (empty) Merge tailnet-repair-da88cf into main
Parent commit (@-)      : tzsyzolw 3e6ecfa9 main
Parent commit (@-)      : sszkzyuu e8ce1e42 tailnet-repair-da88cf
Added 5 files, modified 0 files, removed 0 files
```

No conflicts arose — jj auto-merged cleanly (`jj resolve --list` → "No
conflicts found at this revision"). What was resolved:

- `cluster-definition.datom`: only `tailnet-repair-da88cf` touched this file
  (CA-certificate declaration); the merge result is byte-identical to the
  tailnet side, confirmed by diff. No manual resolution needed — this
  satisfies "resolve on the side of the tailnet bookmark for cluster data"
  by construction.
- `secrets/`: both sets are present together — main's 5 newly-minted files
  (`headscaleTlsCertificate.sops`, `headscaleTlsKey.sops`,
  `tailnetCertificateAuthorityKey.sops`, `tailnetPreauthKeyOuranos.sops`,
  `tailnetPreauthKeyPrometheus.sops`) plus the 4 files already common to
  both branches (`localLlmApiToken.sops`, `opencodeServerPassword.sops`,
  `routerBackupWifiPassword.sops`, `routerWifiSaePasswords.sops`). No
  secrets file was dropped from either side.

## 3. `nix flake check`, Prometheus-only

```
$ nix flake check --option max-jobs 0 --option eval-cache false
...
copying path '/nix/store/6im92ly6cg18mjx8r2kj3pzhghnfymgf-source' from 'http://nix.prometheus.goldragon.criome'...
...
checking derivation checks.x86_64-linux.synchronizer...
checking derivation checks.x86_64-linux.horizon-definition...
checking derivation checks.x86_64-linux.synchronizer-configuration...
running 0 flake checks...
all checks passed!
warning: The check omitted these incompatible systems: aarch64-linux
EXIT: 0
```

Remote builder in effect (`/etc/nix/machines`):
`ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux ...`. `--option
max-jobs 0` barred any local build; the run only queried/copied from the
Prometheus binary cache (`http://nix.prometheus.goldragon.criome`) and
succeeded with exit 0 — no local build fallback occurred. Result: **check
passed**.

## 4. Bookmark move and push

```
$ jj bookmark set main -r ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b
Moved 1 bookmarks to ovuwnxus ddf27e0c main*
$ jj git push --bookmark main
Changes to push to origin:
  bookmark: main [move forward from 3e6ecfa92944 to ddf27e0c28bf]
```

## 5. Verification against the real remote

```
$ jj git remote list
origin ssh://git@github.com/LiGoldragon/goldragon
$ git ls-remote ssh://git@github.com/LiGoldragon/goldragon refs/heads/main
(actually queried as git@github.com:LiGoldragon/goldragon.git)
ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b	refs/heads/main
```

Local revision `ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b` matches the real
remote's `refs/heads/main`. Push landed.

## Result

- Ancestry answer: **no**, main and tailnet-repair-da88cf had diverged.
- New goldragon `main` on the real remote: **ddf27e0c28bfdd98bf36dcb580ab51abc2c6c40b**
  (merge of `3e6ecfa92944c0113b192314f9c4a66cb33f1cb7` and
  `e8ce1e42be4644b4e96cac1bcba6a8b1b4232563`).
- `nix flake check` (Prometheus-only): passed, exit 0.
- Unresolved: none. Merge required no manual conflict resolution.
