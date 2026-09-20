# Lojix schema compatibility addendum

Status: provisional. No deployment, Home activation, or Realize acceptance is
claimed. No source edits, screenshots, or secrets are included here.

## Reproducing request and failure

The affected request is the complete 14-field `Deploy.UserEnvironment`:

```text
Deploy.UserEnvironment.{
  goldragon ouranos li
  $HORIZON_DEFINITION
  SecretsDirectory.$GOLDRAGON_SECRETS
  github:LiGoldragon/CriomOS/aa5c151f87c0283bf63a622bf78224cb1410a188
  { ssh-ng://li@ouranos.goldragon.criome li@ouranos.goldragon.criome }
  Horizon
  { homeConfigurations.li.activationPackage }
  HomeManagerNixProfileV1
  Realize
  RequireImmutable
  Some.@/etc/nix/machines
  []
}
```

With the Goldragon `8c4d03de76907f590072c0998b00037330ebcd82` Horizon child,
the installed `lojix-meta` rejects the request before socket exchange with
`proposal source is not a Horizon definition`. The first surfaced decode field
is therefore the proposal source/Horizon definition value; that diagnostic
masks the later field comparison. The mismatch inference is grounded by the
consumer pin: Lojix horizon-lib is `40d04d25`, while Goldragon's Horizon is
`ee8d6f8d27eb6e200504807971ffdd26aaca7ed1`. The newer schema adds
`OpenCodeTesting` and changes the `Decimal` location. Horizon CLI parsing of
the child passed, so this is a producer/consumer schema skew inference, not a
finding that the child is invalid.

## Audited smallest coherent source scope

The smallest coherent repair crosses every socket-contract producer and the
Lojix consumer:

1. `signal-lojix`: update `Cargo.toml`, `Cargo.lock`, and `version`/`UPGRADES`
   metadata; regenerate and update the `generated_contract` fixture first.
   The current final provisional source proposal is
   `3f550fc278b8e14c37158036d420e7e3ed1d7c7b`.
2. `meta-signal-lojix`: make the same contract and fixture updates and pin the
   exact published `signal-lojix` revision. Its current final provisional
   source proposal is `a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85`.
3. Lojix: update root `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`,
   `UPGRADES`, and the four member `Cargo.toml` files for `nexus`,
   `clients/ordinary`, `clients/meta`, and `tools`, plus the exact signal/meta
   contract revisions. The root-only pin was insufficient. The current
   consumer proposal is branch `proposal/horizon-contract-repin-8565e8` at
   `34115703fad1df0bcf11814fc82456abc2f42b58`: all five workspace crates are
   `7.0.0`, the exact diff is nine files, and the old dependency graph is
   absent; Luna reported source PASS.

   The producer fixtures must cover `OpenCodeTesting` and `FixedLocation` with
   all four Goldragon Decimal fields, including peer-byte restore/round-trip
   checks. The separate Lojix fallback branch is
   `proposal/remote-builder-fallback-false` at `476bc56`; Luna PASS covers its
   one-file diff and focused test. Neither proposal is integrated or deployed.

No generated runtime kinds or store migration is indicated by this audit.
Remote codec and round-trip tests are required before acceptance. Deployment
is not part of this scope.

## Separate proposals and current locks

| Component | Current provisional proposal | Audit state |
| --- | --- | --- |
| `signal-lojix` | `3f550fc278b8e14c37158036d420e7e3ed1d7c7b` | Source PASS; remote contract test pending |
| `meta-signal-lojix` | `a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85` | Source proposal; remote contract test pending |
| Lojix consumer | `proposal/horizon-contract-repin-8565e8` at `34115703fad1df0bcf11814fc82456abc2f42b58` | Luna source PASS; nine-file diff, old graph absent; five crates `7.0.0` |
| Lojix fallback | `proposal/remote-builder-fallback-false` at `476bc56` | Separate one-file proposal; Luna PASS; unintegrated |

The final provisional source proposals are `signal-lojix`
`3f550fc278b8e14c37158036d420e7e3ed1d7c7b`, `meta-signal-lojix`
`a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85`, and the Lojix consumer
`34115703fad1df0bcf11814fc82456abc2f42b58` above. All five workspace crates
are `7.0.0` in the consumer proposal. Luna's source result is PASS; this is
not contract or deployment acceptance. The fallback branch remains separate
and unintegrated. The former producer locks `3002` and `3003` are not evidence
of acceptance; fallback Lock `2995` was released.

## Remote test status

The expanded signal Datom foreground test was interrupted and reaped with
exit 1, with no codec result. A detached rerun (PID `1240203`, bounded to
7200 seconds) is recorded at
`flows/8565e8/witnesses/signal-lojix-test-datom-contract.log`; it was still
pending after a two-minute sample. Its child PID `1240223` was state `S`,
`/proc` I/O was denied, and `ss` showed no attributable socket. The 100-byte
log sample contained a `cache.nixos.org` copy line; the store path remained a
4096-byte directory. This measures no visible progress. It does not establish
zero network bytes or daemon health. Raw logs are not copied into this report.

The ordinary-user network split probe succeeded: a 30-second-capped `curl` to
`cache.nixos.org/nix-cache-info` returned HTTP 200 in 406 ms;
`api.github.com` returned HTTP 200 in 299 ms; and ordinary-user
`nix path-info --store https://cache.nixos.org` for
`/nix/store/0gzsbyn4jijg9iw0zfnp1p2rai24g9cz-source` exited 0 in 535 ms and
returned that exact path. General host outbound access therefore worked during
the probe. The daemon/client fetch environment being narrower remains a
suspect, unproved explanation. The detached signal runner PID `1240203`,
bounded to 7200 seconds with the durable log path above, remains pending and
has no test pass.

## Later living deployment boundary

Morning action is to wait for the bounded runner to exit or time out, then
assess the Ouranos Nix substituter/daemon path with privileged correlated
counters if available. Rerun producer checks sequentially; only after they
pass run the remote Lojix `7.0.0` check and the full pre-socket Home request.
There is no next check, Realize, activation, or deployment claimed here.

## Morning root-check plan

No new build is authorized in this report. Root should first compare the
daemon's first substituter, `http://nix.prometheus.goldragon.criome`, using
`/etc/nix/nix.conf` with the ordinary user's effective connect timeout of 60 s
against the daemon timeout of 5 s. The user has a configured `netrc-file`,
while the daemon's explicit environment does not show one; compare the
daemon's actual netrc, proxy, DNS, and CA settings without exposing secret
contents. Correlate the daemon child socket owner and remote destination, and
record `/proc/<child>/io` byte deltas across a bounded sample.

The ordinary-user remote-store bypass was also attempted: `nix-ssh`
authentication was denied, so no build occurred. There was no daemon action.

After the daemon path is fixed, run the four producer checks sequentially and
stop on the first nonzero. Use immutable `git+file` revisions, the verified
Prometheus builder from `/etc/nix/machines`, `max-jobs 0`, `fallback false`,
`timeout 7200`, and one durable log and PID per check. The following is the
concrete detached runner; its syntax is checked with `bash -n` only and it is
not run here:

```bash
#!/usr/bin/env bash
set -euo pipefail
root=/var/tmp/lojix-contract-rerun-8565e8
mkdir -p "$root"

run_check() {
  local name=$1 ref=$2 check=$3
  local log="$root/$name.log"
  printf '%s\n' "$$" > "$root/$name.pid"
  timeout 7200 nix --option max-jobs 0 --option fallback false \
    flake check "$ref#checks.x86_64-linux.$check" >"$log" 2>&1
}

run_check signal-datom \
  'git+file:///git/github.com/LiGoldragon/signal-lojix?rev=3f550fc278b8e14c37158036d420e7e3ed1d7c7b' \
  test-datom-contract
run_check signal-generated \
  'git+file:///git/github.com/LiGoldragon/signal-lojix?rev=3f550fc278b8e14c37158036d420e7e3ed1d7c7b' \
  test-generated-contract
run_check meta-datom \
  'git+file:///git/github.com/LiGoldragon/meta-signal-lojix?rev=a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85' \
  test-datom-contract
run_check meta-generated \
  'git+file:///git/github.com/LiGoldragon/meta-signal-lojix?rev=a2a42e9d0c66d586aff7e0bb349a3c2c1d455a85' \
  test-generated-contract
```

Launch the already syntax-checked runner with `nohup setsid`, retaining its
PID and four logs. Only after all four pass may the remote Lojix `7.0.0`
check at provisional `34115703fad1df0bcf11814fc82456abc2f42b58` and the full
disconnected 14-field pre-socket Home request be attempted. Deployment,
Realize, and activation remain separate later decisions.

The current detached daemon-bound runner PID `1240203`, bounded to 7200 s,
remains pending at
`flows/8565e8/witnesses/signal-lojix-test-datom-contract.log`; its final exit
is to be appended later. No raw log was copied here, and no secret was read.

## Sources

- `flows/8565e8/reports/morning-2026-09-20.md` — request shape, Goldragon
  child, parser and preflight observations.
- `flows/f38926/log.md` — revision comparison, producer scope, fixture gap,
  proposal revisions, lock status, and deployment boundary.
