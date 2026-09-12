# Landing the f6db8d branches on CriomOS and CriomOS-home main

Subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d,
2026-09-12, under the living's order "land the branches" and the ruling
"meta cli names is `<component>-meta`"
(`flows/f6db8d/vision/metaCli.md`). Nothing was deployed: no activation,
no switch, no `meta-lojix` request, no running service touched. All work
was done in fresh clones under this thread's scratchpad, never in the
shared checkouts under the Repository root, because flow f7941a holds
Orchestrate lock 1019 on paths inside
`/git/github.com/LiGoldragon/CriomOS-home`.

**witnessed** = this thread ran the command or opened the file and the
result is quoted below. **relayed** = another flow's report says so and
is named. Observations, hypotheses and unknowns are kept apart.

## 0. What to read first

1. **CriomOS main moved and CriomOS-home main moved.** The revisions are
   in §1 and §2. Both landings needed repairs the branches did not carry,
   and those repairs are the substance of this report, not a footnote.
2. **Neither repository's `nix flake check` was green before this work,
   and neither is green after.** Both were red on untouched `main` at
   sites this landing does not touch (§4.1, §4.4). This was verified by
   running the same gate on an unmodified clone of each `main` first.
   Nothing here made a green gate red.
3. **The lojix revision CriomOS now pins cannot be built on Prometheus.**
   The identical derivation is green locally and red on the remote
   builder, twice each. The cause is a five-second clock wait in lojix's
   own test, not anything in CriomOS. §3. This bears directly on a
   deploy.
4. **The `modelIsThinkpad` stop is unchanged**, witnessed at the landing
   revision against the real projection. §4.3.
5. **A deploy is still not possible**, and §6 says exactly what a deploy
   would now do and what must happen first.

## 1. CriomOS

### 1.1 The revisions

`main` was **`acc3feab4d99492276a353a80bbccffac9d6fb58`** and is now
**`b84b99ba5483b5e7c31687e18df4b92cf86406e0`**, confirmed after the push
with `git ls-remote https://github.com/LiGoldragon/CriomOS.git
refs/heads/main`. Three commits, in order:

| commit | what |
|---|---|
| `c4c830c10d32e15c6afc055383ca49fef95963fd` | `f6db8d-lojix-start` unchanged. Its parent was already `acc3feab`, so the prescribed rebase onto current main was a fast-forward and rewrote nothing — witnessed by `git merge-base main origin/f6db8d-lojix-start` returning `acc3feab`. |
| `cf3be614df5a2aec2a7ed9a8a9719fc954696668` | the repin the branch could not carry. |
| `b84b99ba5483b5e7c31687e18df4b92cf86406e0` | two check repairs the branch left behind, found only by building its checks. |

### 1.2 The repin, and what was verified rather than assumed

`flake.nix` moves `lojix` from `23f09f28…` to
**`b5cddd2e16ad49d1060cf4109f44c27359195441`** (5.0.0) and `flake.lock`
follows. `signal-lojix`, `meta-signal-lojix` and `horizon-rs` are **not**
CriomOS flake inputs — they are Cargo dependencies inside lojix, so the
brief's three producer revisions are properties of the pinned lojix, not
separate pins. Witnessed in that revision's own `Cargo.lock`:

```
signal-lojix      5.0.0   rev=4271b5ced31ea02f11f29b602301832e83cfe6c2
meta-signal-lojix 6.0.0   rev=35deec4ef0a6d023f2f49464515075779cbb4973
horizon-lib       0.10.1  rev=40d04d2504fee619e9b2b2564b8a769a3a9d6049
```

and each of `signal-lojix`, `meta-signal-lojix`, `horizon-lib`,
`datom-codec`, `protos`, `ethos-zero`, `signal` appears **exactly once**
(`grep -c '^name = "<crate>"$' Cargo.lock` = 1 for all seven). That is the
decisive property: the duplicate `meta-signal-lojix` that made `23f09f28`
uncompilable cannot recur at this revision. The old `KNOWN UNBUILDABLE`
comment beside the pin is replaced by that fact.

`checks/lojix-ownership` hardcoded `expectedRevision = "23f09f28…"` and
`expectedPackageName = "lojix-1.0.1"`; `reports/runtime-audit.md` §8
relayed that the first would bite, and it does — both assertions move with
the pin. The package name at the new revision is `lojix-5.0.0`, witnessed
by evaluating `inputs.lojix.packages.x86_64-linux.default.name`.

**`expectedOrchestrateRevision` was left at `5f016531…` deliberately.**
That check reads CriomOS-home's lockfile through `inputs.criomos-home`,
which is pinned at `caffe9a17cc5` — the revision *before* §2's landings —
so it still sees the old Orchestrate pin and the assertion still holds.
It becomes false the moment anyone moves CriomOS's `criomos-home` pin,
which a deploy requires. §6.

### 1.3 Two defects the branch shipped, found only by building its checks

`reports/lojix-criomos.md` §1.6 recorded the new check green as
`/nix/store/myh5l7…-lojix-nexus-service.drv` — a **drv path**, from
`nix eval`. Evaluating a `runCommand` to a derivation proves the Nix
expression is well-formed and runs none of its shell body. Both defects
below sit in that body or in an unevaluated sibling, and both were
invisible until the checks were actually built.

**`checks/lojix-ownership` still read a unit the branch had deleted.**
Building it failed at evaluation:

```
error: attribute 'lojix-daemon' missing
at …/checks/lojix-ownership/default.nix:119:12:
   119|   daemon = fixture.config.systemd.services.lojix-daemon;
```

The branch renamed the unit `lojix-daemon.service` → `lojix.service` and
replaced `checks/lojix-daemon-config-roundtrip` with
`checks/lojix-nexus-service`, but `checks/lojix-ownership` carried its own
copy of the same dead assertions: a `lojix-daemon` unit, an
`ExecStartPre` writer command, and an `explicitSocketFixture` setting
`ordinarySocketPath`, `ownerSocketPath`, `storePath`, `startupArchivePath`
and `daemonHost` — five options that are now `readOnly` derivations or
gone. It now reads the `lojix` unit, sets only `stateDirectoryPath`,
`runtimeDirectoryPath` and `nexusHost`, and asserts the values the Nexus
actually opens: `ownerSocketPath == /run/lojix/meta.sock` (not
`owner.sock`) and `storePath == /var/lib/lojix/lojix.sema` (not
`lojix-v5.sema`). The service-shape assertions were dropped rather than
duplicated: `checks/lojix-nexus-service` owns them.

**`checks/lojix-nexus-service` asserted a count that is off by
twenty-one.** Its shell body contains

```
test ${toString (builtins.length configuration.config.systemd.tmpfiles.rules)} = 2
```

which, rendered, is `test 23 = 2`. A NixOS system carries tmpfiles rules
from every module; the lojix module contributes two of twenty-three. The
check now names its own two rules instead of counting everything:

```nix
assert lib.all (
  rule: builtins.elem rule configuration.config.systemd.tmpfiles.rules
) expectedTmpfilesRules;
```

That new assertion was seen failing before it was trusted — changing the
declared mode from `0750` to `0751` produces

```
error: assertion '((lib).all (rule: ((builtins).elem rule (configuration).config.systemd.tmpfiles.rules)) expectedTmpfilesRules)' failed
at …/checks/lojix-nexus-service/default.nix:58:1
```

and restoring `0750` returns `/nix/store/n30ylmipaj41qwlxyag6319zgqf8kymd-lojix-nexus-service.drv`.

### 1.4 The gate, and where each build ran

All four lojix checks pass. Each was built through a probe expression
rather than `nix flake check`, because CriomOS's whole `checks` output is
unevaluable for a reason unrelated to this landing (§4.1).

| check | result | built on |
|---|---|---|
| `lojix-ownership` | `/nix/store/q8gr2z9a4zybqybg855z44w2ll44m3b5-lojix-ownership` | local |
| `lojix-nexus-service` | `/nix/store/1d6rbm46mpflpyg3h8hky35jpi3ksbq6-lojix-nexus-service` | local |
| `lojix-nexus-start` (NixOS VM) | `/nix/store/04c0yfjs2k2nmbwnsbbqal798rpxiky2-vm-test-run-lojix-nexus-start` | local |
| `lojix-fresh-nexus-startup` (lojix's own) | `/nix/store/3bhlpkwfpvs6xgfgc4yf9ic07ikn6zny-lojix-test-5.0.0` | local |

"local" is stated plainly because §3 is why: the lojix package these all
depend on cannot be built on Prometheus. The remote builder was reachable
and used by default throughout — `nix build` of an unrelated probe
derivation reported `building … on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'`
— and horizon-rs 0.10.1 was built there
(`/nix/store/6xlkrqa8axf11xdc8x7rav5h569a8kps-horizon-0.10.1`, copied from
Prometheus). These four fell back to local, and this is the record of it.

The VM test is the one that matters, because it is the only gate in the
estate that observes a CriomOS-configured Lojix answering. From its log,
ANSI stripped:

```
machine: (finished: waiting for unit lojix.service, in 16.49 seconds)
machine: waiting for success: test -S /run/lojix/ordinary.sock && test -S /run/lojix/meta.sock
machine: must succeed: systemctl show lojix.service --property=ExecStart --value
         | grep -F 'argv[]=/nix/store/b72s3cm5…-lojix-5.0.0/bin/lojix-nexus ;'
machine: must succeed: LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock
         …/bin/lojix 'Query.ByNode.{ fixture-cluster fixture-node None }'
machine: Queried.{ [] [] { 2 2 } }
```

Lojix **5.0.0** — not the revision the branch was written against —
started from CriomOS's unit with the bare zero-argument `lojix-nexus`
argv, bound both sockets at the paths CriomOS exports, and answered one
ordinary `Query` with a typed `Queried`: empty live set, empty GC-root
set, state marker `{ 2 2 }`, which is what a fresh store should say.

## 3. The lojix CriomOS pins cannot be built on Prometheus

This is new and nobody has reported it.

Building `inputs.lojix.packages.x86_64-linux.default` as CriomOS resolves
it fails, reproducibly, on the remote builder:

```
error: test failed, to rerun pass `-p lojix-nexus --test daemon_configuration`
running 3 tests
test legacy_configuration_archive_remains_available_to_the_offline_migrator ... ok
test daemon_rejects_startup_arguments_before_discovering_state ... ok
test zero_argument_daemon_persists_lifecycle_and_uses_desired_sockets_on_restart ... FAILED
thread '…' panicked at nexus/tests/daemon_configuration.rs:191:9:
ordinary was not reachable
```

Twice, on `/nix/store/17zgydcb3jiwr8g1sq32gv66bngh0hmq-lojix-5.0.0.drv`.

**Three hypotheses were separated, and two were disproved.**

*Not nixpkgs.* CriomOS forces `lojix.inputs.nixpkgs.follows = "nixpkgs"`,
pinning `f83fc3c307e7…` where lojix's own lock has `9f11f828c213…`.
Building lojix's own flake with `--override-input nixpkgs` set to
CriomOS's exact revision **succeeded**
(`/nix/store/g9dishxjqx2vnq8xshbb02gswhnk6ngz-lojix-5.0.0`). The nixpkgs
difference is not the cause.

*Not a defect in what CriomOS consumes.* The **identical derivation** —
same store path `17zgydcb…`, same inputs — built green with
`--builders ''`:

```
$ nix build -L --builders '' /nix/store/17zgydcb…-lojix-5.0.0.drv^*
/nix/store/d0s1wskw0y2l9ybnffvicw67w50yg1a8-lojix-5.0.0
```

Same derivation, green here, red there. That leaves the machine, not the
code.

*The cause, from the test.* `nexus/tests/daemon_configuration.rs` has
`const STARTUP_TIMEOUT: Duration = Duration::from_secs(5)` and
`wait_for_socket` polls until that deadline, panicking with the listener's
name. The daemon had **not exited** — `try_wait` would have panicked with a
different message — so the Nexus was alive and simply had not bound its
socket within five seconds on a loaded builder. This is a test that waits
on the clock rather than on the tested event, which is exactly what the
`testing` skill forbids, and it is load-sensitive by construction.

**This is a lojix defect, in a repository this thread does not own.** It
is not a CriomOS defect and it is not a reason to hold the pin: every
CriomOS assertion about lojix's behaviour passes. But under the standing
order that this machine stays cold and every gate runs on Prometheus, the
consequence is concrete: **the CriomOS lojix gate cannot be re-run green
on the remote builder until lojix's test waits on the socket instead of
the clock.** The green evidence in §1.4 is the local build of the exact
derivations the remote builder refuses.

