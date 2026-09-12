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
**`2985c813cae8f077845873149252f7dbc0575e8d`**, confirmed after each push
with `git ls-remote https://github.com/LiGoldragon/CriomOS.git
refs/heads/main`. This thread landed four commits, and a sibling f6db8d
subflow landed two in between:

| commit | whose | what |
|---|---|---|
| `c4c830c10d32e15c6afc055383ca49fef95963fd` | the branch | `f6db8d-lojix-start` unchanged. Its parent was already `acc3feab`, so the prescribed rebase onto current main was a fast-forward and rewrote nothing — witnessed by `git merge-base main origin/f6db8d-lojix-start` returning `acc3feab`. |
| `cf3be614df5a2aec2a7ed9a8a9719fc954696668` | this thread | the repin the branch could not carry: lojix 5.0.0. |
| `b84b99ba5483b5e7c31687e18df4b92cf86406e0` | this thread | two check repairs the branch left behind, found only by building its checks. §1.3. |
| `79cc994…` | a sibling | "Refuse local builds on hosts with no Nix builder role". |
| `8fcfbfecb420952ed686dbb635d57b51125d6462` | a sibling | "Classify hardware in CriomOS, from the model Horizon projects" — which **resolves the `modelIsThinkpad` stop** this thread was told to record and not fix. §4.3. |
| `2985c813cae8f077845873149252f7dbc0575e8d` | this thread | lojix **6.0.0**, the new check registered, one retired fixture field dropped. §1.5. |

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

### 1.5 The second repin: lojix 6.0.0, and why it matters more than a version number

While this landing was in flight, lojix released **6.0.0**
`c4bba4fa12408c39ff745b0773468cd32a74403f`, and the main flow directed
pinning it. It carries the same contract pins as 5.0.0 — verified the same
way, one revision of each:

```
signal-lojix      5.0.0   rev=4271b5ce…   count=1
meta-signal-lojix 6.0.0   rev=35deec4e…   count=1
horizon-lib       0.10.1  rev=40d04d25…   count=1
```

and the same Nexus surface on every point CriomOS's module depends on —
`[[bin]] lojix-nexus`, `DEFAULT_RUNTIME_DIRECTORY = "/run/lojix"`,
`DEFAULT_STATE_DIRECTORY = "/var/lib/lojix"`, `ordinary.sock`, `meta.sock`,
`lojix.sema`, `0o660`/`0o600`. So the module needed no edit; only
`checks/lojix-ownership`'s two hardcoded values moved, to
`c4bba4fa…` and `lojix-6.0.0`.

**It also fixes §3.** 6.0.0 replaced the five-second poll with a wait on
an announced event. Witnessed, `nexus/tests/daemon_configuration.rs`:

```rust
/// Wait for the event the Nexus announces when both listeners are bound …
/// The wait ends on the announcement, or on the child's standard output
/// closing — which is what happens when the Nexus exits before becoming
/// ready, so a failed startup is reported at once rather than after a
/// deadline.
fn announced_readiness(daemon: &mut Child, occasion: &str) -> Vec<String> {
```

with `READINESS_BACKSTOP` at 300 seconds — a backstop, not the mechanism.
The consequence is the one that matters: **lojix now builds on
Prometheus.** CriomOS's own resolution of it, with CriomOS's nixpkgs,
built remotely:

```
$ nix build --max-jobs 0 … .lojix-package
building '/nix/store/xn706di9mhl9mnv099clcm47ivw9inij-lojix-6.0.0.drv' on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
/nix/store/x24nswlz2dcm3zmq2c1vsanx8yiwdns8-lojix-6.0.0
```

Every lojix gate is therefore green **on the remote builder**, not merely
locally. §1.4's table is superseded by §1.6.

### 1.6 The gate at the landed head, all on Prometheus

Every one of these ran with `--max-jobs 0`, so every build happened on
Prometheus and none on this machine.

| check | result |
|---|---|
| `lojix-ownership` | `/nix/store/nw6r30d7wpij4rcid4qfn6nyjwd4ac0c-lojix-ownership` |
| `lojix-nexus-service` | `/nix/store/pk3wmlk1b1nf8b4wzwn2qfz1fcifi216-lojix-nexus-service` |
| `lojix-nexus-start` (NixOS VM) | `/nix/store/bzq6487v6mvx1fvcna8349nncflnv3ci-vm-test-run-lojix-nexus-start` |
| `lojix-fresh-nexus-startup` (lojix's own) | `/nix/store/3qg8kk713ajbgs07mcz2bzq28g479wym-lojix-test-6.0.0` |
| `metal-model-classification` (newly registered) | `/nix/store/zv3qxza9wmapf2jr266jl2wpphdalbnb-metal-model-classification` |

The VM test again, now against 6.0.0, ANSI stripped:

```
machine: (finished: waiting for unit lojix.service, in 24.87 seconds)
machine: must succeed: systemctl show lojix.service --property=ExecStart --value
         | grep -F 'argv[]=/nix/store/x24nswlz…-lojix-6.0.0/bin/lojix-nexus ;'
machine: Queried.{ [] [] { 2 2 } }
```

### 1.7 Two lines the main flow named, and what each was

**`checks/metal-model-classification` was not registered in
`projectChecks`.** The sibling's commit added the check directory and its
`flake.nix` entry was missing, so nothing ran it — a check that exists and
is never evaluated is not a gate. It is registered beside
`metal-firmware-policy` and is green (§1.6).

**`checks/lojix-ownership` set `typeIs.largeAiRouter = false` on its
fixture.** `typeIs` is one of the structs horizon-rs deleted in `f1a5eca`
("drop TypeIs + ComputerIs (enum-shadow structs)"), so the projection
never emits it. A fixture that writes a field the producer does not emit
is precisely the false-green that let `machine.arch` survive for months.
The line is deleted, and `grep -c typeIs checks/lojix-ownership/default.nix`
is now `0`.

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

## 4. What the gates cannot reach, and why — all pre-existing

Every claim in this section was verified on an **unmodified clone of the
repository's own `main`** before any of this work was applied, so that
none of it could be attributed to the landing.

### 4.1 CriomOS's `checks` output cannot be evaluated at all

`nix flake check` on CriomOS `main` `acc3feab`, with a real `system` and a
real `horizon` supplied, stops here:

```
error: attribute 'hardware' missing
at …/modules/nixos/metal/default.nix:21:12:
    21|   inherit (horizon.node.machine.hardware) model;
```

and it stops there identically with the branch applied, with the
current-producer projection, and with the live Ouranos projection —
because the failure is not in the `horizon` input. `flake.nix:174`
computes

```nix
blueprintChecks = lib.mapAttrs (_: checks: lib.filterAttrs (_: lib.isDerivation) checks) …
```

and `filterAttrs` forces **every** check's value. One throwing check
therefore makes the entire `checks` attrset unevaluable — even
`builtins.attrNames` on it fails. CriomOS's check set is all-or-nothing.

The throwing checks are four, found by grep and confirmed one at a time:
`checks/fixed-location-policy`, `checks/laptop-keyboard-keyd`,
`checks/metal-firmware-policy` (twice) and `checks/wispr-keyboard-uaccess`
each hand-write

```nix
machine = {
  chipGen = null;
  model = "all-x86-64";
};
```

while `modules/nixos/metal/default.nix` reads
`horizon.node.machine.hardware.model` (line 21) and
`horizon.node.machine.hardware.chipGeneration` (line 322). The module was
migrated to the current projection's `machine.hardware.*` shape; these
four fixtures were not. This is the same class of false-green that
`reports/lojix-criomos.md` §2.2 found and closed for `machine.arch`,
except that this one has already gone red.

**Not repaired here.** Applying the four-fixture repair transiently (to
learn whether anything else was red) does get past it — that is how §4.2
and §4.3 were reached — but the repair was reverted and not landed, for
two reasons. It is inseparable from the `modelIsThinkpad` design item the
brief reserves (§4.3): the same four fixtures hand-write
`modelIsThinkpad`, `chipIsIntel` and `computerIs`, so repairing the
`machine` shape makes them green again *by continuing to hand-write
retired fields* — it restores the false green rather than removing it.
And three of the four are the declared subject of Orchestrate locks 907
and 908 held by flow 542442.

### 4.2 Two further pre-existing failures behind that one

With the four fixtures transiently repaired, CriomOS's gate reaches and
fails at:

- `platform-tools_r37.0.1-linux.zip` refusing the unfree licence. Every
  run in this report therefore carries `NIXPKGS_ALLOW_UNFREE=1 --impure`;
  `reports/removals.md` §1 relayed the same necessity independently.
- `error: MS2130 UVC patch must be reviewed for the selected kernel`
  (`checks/ms2130-uvc-aspect-quirk`), a deliberate throw awaiting a human
  review of the kernel.

Neither is touched by this landing.

### 4.3 The `modelIsThinkpad` stop is unchanged — witnessed at the landing revision

The brief reserves this and asks only whether the complete-system
evaluation still stops there. It does. Evaluating
`modules/nixos/metal/default.nix` at the landed tree against the real
current-producer projection:

```
error: attribute 'modelIsThinkpad' missing
at …/modules/nixos/metal/default.nix:37:5:
    36|     chipIsIntel
    37|     modelIsThinkpad
      |     ^
    38|     computerIs
```

Identical to `reports/lojix-criomos.md` §3.1 run 2 and §5.1. Nothing in
this landing moves it, and nothing here was expected to.

### 4.4 CriomOS-home's gate stops at `orchestrate-wrapper-fallback`

On an unmodified clone of CriomOS-home `main` `caffe9a17cc5`:

```
error: attribute 'config' missing
at …/checks/orchestrate-wrapper-fallback/default.nix:35:8:
    35|     if moduleResult.config ? content then moduleResult.config.content else moduleResult.config;
```

`modules/home/profiles/min/orchestrate.nix` returns a plain attribute set
with no `config` key. Its sibling `checks/orchestrate-service-path`
already carries the three-way fallback for exactly this
(`if moduleResult ? config && moduleResult.config ? content … else moduleResult`);
`orchestrate-wrapper-fallback` was never given it. Identical error on the
landing stack, at the same line — this landing neither caused it nor is
blocked by it. It is repaired in §5, because §5 has to edit that file
anyway and a renamed binary inside a check nobody can evaluate is not a
gate.

## 2. CriomOS-home

### 2.1 The three branches, stacked

All three were already children of `main` `caffe9a17cc5`, so the
prescribed rebase onto current main rewrote nothing; the work was to
**stack** them in the ordered sequence the brief names, which is what
turns three parallel one-commit branches into a landable line:

```
caffe9a17cc5  main (before)
  └─ 0176de5f  f6db8d-lojix-start   (unchanged, already on main)
       └─ a6aa639d  f6db8d-removals     (rebased from 4cb132ec)
            └─ 1d82a32b  f6db8d-rust-relock  (rebased from 37db5a8b)
```

Both rebases applied cleanly. `f6db8d-removals` and `f6db8d-rust-relock`
both edit `flake.lock` — the first removing the `primary-generated-src`
node, the second moving `rust-overlay` — and the two regions do not
overlap.

### 2.2 One thing verified that the branches could not verify

`fixtures/horizon.nix` documents its projection as generated by
horizon-rs `8f4240ef23024c2d3b55f803d96d3c6e7aa5b433`, "the revision lojix
pins". After §1.2 that is no longer true: lojix 5.0.0 pins
`40d04d2504fee619e9b2b2564b8a769a3a9d6049` (horizon-lib 0.10.1). So the
fixture was re-derived from the checked-in definition with the **newly
pinned** producer:

```
$ horizon-cli --node atlas < fixtures/horizon-definition.datom
IDENTICAL to fixtures/horizon-projection.json
```

(`horizon-cli` from `/nix/store/6xlkrqa8axf11xdc8x7rav5h569a8kps-horizon-0.10.1`,
built on Prometheus; comparison by parsed equality in Python, not by text.)
The projection did not move between the two horizon-rs revisions, so the
fixture is still exactly the deploy-time shape. Only its comment moved, to
name both revisions.

### 2.2b The branch's own two check derivations reproduce exactly

`reports/lojix-criomos.md` §2.3 recorded the two repaired checks as
evaluating to specific derivations. On the stacked tree, against the real
projection, the gate reports the same two paths character for character:

```
checking derivation checks.x86_64-linux.yt-dlp...
derivation evaluated to /nix/store/wb0jlq8lzx007b72lhn1dazk5fripq2v-yt-dlp-current-source.drv
checking derivation checks.x86_64-linux.ai-agent-launch-orchestration...
derivation evaluated to /nix/store/xpfawyzfb7ji9xpvq89rvi76jcnssf3f-ai-agent-launch-orchestration.drv
```

Independent corroboration of that report, reached by a different route
(the repository's own gate rather than a hand-written probe) and with the
stack's two later commits on top.

### 2.2c A third defect the branch shipped: it breaks Home's OS-boundary check

`checks/system-projection-boundary` is a policy gate, not a test of
behaviour: it greps every Home `.nix` source and `flake.lock` for the
string `lojix` or `LOJIX` and fails if any is found, with the message
*"Home Nix sources must not retain an OS deployment edge"*. Two
exemptions are listed by path; `fixtures/` is not one of them.

`f6db8d-lojix-start` as pushed adds `fixtures/horizon.nix`, whose comment
says it twice. Witnessed, at the pushed branch revision:

```
$ git show f6db8d-lojix-start:fixtures/horizon.nix | grep -niE lojix
9:# revision lojix pins and materializes into the `horizon` flake input at deploy
10:# time. Lojix's materialized flake is literally
```

So the branch was red on that check before this landing touched it, and
the first comment edit §2.2 made added two more occurrences. Caught by
building the check:

```
/nix/store/…-source/fixtures/horizon.nix:10:# (horizon-lib 0.10.1) — …
Home Nix sources must not retain an OS deployment edge
```

The comment is reworded to carry the same provenance without naming the
deployment tool, and says at the end why it does not name it, so the next
person does not reintroduce the name. Verified over the whole tree with
the check's own find/grep:

```
$ find . -type f -name '*.nix' ! -path ./checks/system-projection-boundary/default.nix \
    ! -path ./modules/home/profiles/min/dictation.nix -print0 \
    | xargs -0 grep -nE '[l]ojix|LOJIX'
(no output)
```

Whether a source-text grep is the right shape for this boundary is a
separate question — by the `testing` skill it is a change-detector, and it
fails on a comment while a real deployment edge could be spelled any
number of other ways. It is the repository's declared policy, so it is
obeyed rather than argued with here, and named in §7 as a thing to decide.

### 2.3 What the branches remove that should be remarked on

`f6db8d-removals` deletes two assertions from
`checks/keyboard-layout-policy` that did

```nix
swayConfiguration = builtins.readFile ../../modules/home/profiles/min/swayConf.nix;
… !(lib.hasInfix "xkb_variant colemak" swayConfiguration) …
```

— tests that read source text and compare strings. Those are
change-detectors of the kind the `testing` skill names outright: they fail
on any edit and catch no behaviour. They existed only to prove two files
were stale, and they leave with the files. The three niri assertions,
which test a computed configuration value, stay.

## 7. Unknowns, stated as unknowns

- **Whether lojix's `zero_argument_daemon_persists_…` test fails on
  Prometheus for load alone.** The five-second clock wait is sufficient to
  explain it and the same derivation is green on a quieter machine, but no
  instrumented run was made on Prometheus to show the bind completing at,
  say, six seconds. The remedy is the same either way: wait on the socket.
- **Whether any consumer outside CriomOS and CriomOS-home pins the
  superseded orchestrate `5f016531` or lojix `23f09f28`.** Not surveyed.
  `reports/lojix-honesty.md` §8 left the same question open for the lojix
  producers.
- **What the four metal fixtures should say.** §4.1 states what they say
  now and why repairing the `machine` shape alone is not the answer. What
  the right fixture is depends on the `modelIsThinkpad` decision, which is
  not this thread's.
- **Whether `checks/system-projection-boundary` should be a source grep at
  all.** It fails on the word `lojix` in a comment (§2.2c) and would pass a
  real deployment edge written any other way. The boundary it defends is
  real; the instrument is a change-detector. Not decided here.
- **Whether `horizon.users` should be a vector at the Home boundary.**
  §2.4 of `reports/lojix-criomos.md` named this; §4.5 now witnesses it as a
  hard failure of `homeConfigurations` against the current producer. The
  contract has an unlanded design elsewhere (Orchestrate lock 903, flow
  542442), so it is not decided here — but it is the single thing standing
  between the estate and a buildable home generation at deploy time.
- **Whether `checks/ms2130-uvc-aspect-quirk`'s throw is still wanted.** It
  is a deliberate `throw` awaiting a kernel review; nobody was asked
  whether that review has happened.

## 6. Deploy note for the living

Nothing here was deployed. This is what a deploy would now do, and what
must happen before one is possible.

### 6.1 The meta `Configure` the deploy needs, and why it is not the one anybody wrote down

The brief asks for "the first meta Configure that
`reports/orchestrate-review.md` says must be the deploy's first act".
**That requirement has been obsolete since orchestrate 0.33.0, and a
different one has taken its place.** Both halves are witnessed below, in
the code of the revision §5 pins, not relayed.

**What orchestrate-review asked for, and why it no longer applies.**
§3.3 and D-4 were written against 0.32.0, which seeded a carried 0.30/0.31
store with the privileged Configure recorded as *not* done — leaving
`Configure` open on the ordinary socket, so any ordinary peer could
repoint both sockets. 0.33.0 closed it. Witnessed in
`crates/orchestrate-nexus/src/store/cutover.rs`, in the assertion the
store's own test makes when opening a previous-generation store:

```rust
assert!(
    store.state().meta_configure_occurred(),
    "a configuration carried out of a generation with no ordinary Configure was set by the privileged path, so the ordinary bootstrap window stays shut"
);
```

So on the deployed host, ordinary `Configure` answers
`ConfigurationRefused.MetaConfigureOccurred` from the first start. The
stranding hazard D-4 named is gone, and a meta `Configure` is no longer
needed to close it.

**What the deploy does need instead.** 0.34.0 changed the meta socket's
default basename, following the same `<component>-meta` ruling this
landing obeys. Witnessed, `crates/orchestrate-nexus/src/defaults.rs:14`:

```rust
const META_SOCKET_FILE: &str = "orchestrate-meta.sock";
```

But a carried store does not take the defaults. The same `cutover.rs`
test asserts, of a store opened with defaults deliberately set to
different paths:

```
"the metadata tree is seeded from the previous generation's row, not from the defaults"
```

Therefore, on the deployed host after the switch:

- the Nexus binds **`meta-orchestrate.sock`**, the path its carried store
  remembers;
- the Home wrapper §5 lands exports
  **`ORCHESTRATE_META_SOCKET=…/orchestrate-meta.sock`**, the new default,
  which is correct for every fresh store and for the gate;
- so `orchestrate-meta` cannot reach the running Nexus, and because
  ordinary `Configure` is shut, nothing else can move the path either.

The deploy's one-time bootstrap step is therefore:

> After the switch, send the meta `Configure` **to the old path**, once:
>
> ```sh
> ORCHESTRATE_META_SOCKET="$XDG_RUNTIME_DIR/orchestrate-nexus/meta-orchestrate.sock" \
>   orchestrate-meta 'Configure.{ /run/user/<uid>/orchestrate-nexus/orchestrate.sock /run/user/<uid>/orchestrate-nexus/orchestrate-meta.sock }'
> ```
>
> then `systemctl --user restart orchestrate-nexus`. After the restart the
> Nexus binds `orchestrate-meta.sock` and the wrapper's exported path is
> the right one. Expect
> `Configured.{ { <ordinary> <meta> } True }` — the receipt shape, not the
> bare configuration.

The alternative, if the living would rather not hand-run anything, is to
delete the carried store and let the Nexus seed from the defaults — which
discards every held Lock, and is a choice, not a step.

**The `orchestrate` skill's release request will also change.** The
release request documented in `SKILL_VARIABLES.md` is unaffected, but two
new files appear beside the sockets at 0.34.0 —
`orchestrate.sock.claim` and `orchestrate-meta.sock.claim`, `0600`,
empty, advisory-locked for the life of the process (relayed from the
repository's own `UPGRADES.md`). Any cleanup or `tmpfiles` rule sweeping
the runtime directory must leave them alone while the service runs. There
is no such rule in CriomOS-home's module today — witnessed, the unit
declares only `RuntimeDirectory=orchestrate-nexus`.

### 6.2 A deploy would not carry any of §2's CriomOS-home work

`CriomOS/flake.nix` pins `criomos-home` at `caffe9a17cc5` — the revision
*before* §2. A deploy of CriomOS today evaluates that revision, so the
`machine.architecture` repair, the removals, the Rust relock and the
Orchestrate repin are all invisible to it. Moving that pin is a one-line
change, and it is deliberately **not** made here, for the reason
`reports/removals.md` §2 gives: re-pinning CriomOS's `criomos-home` input
is a deploy decision. Two things break the moment it is made, and both are
in `CriomOS/checks/lojix-ownership/default.nix`:

- `expectedHomeRevision = "caffe9a17cc5…"` — must become the new head.
- `expectedOrchestrateRevision = "5f016531…"` — asserted against **both**
  lockfiles. CriomOS's own `flake.nix:32` still pins `5f016531`, and §5
  moves CriomOS-home's. The assertion then compares two different
  revisions and fails. `reports/runtime-audit.md` §8 predicted this for
  the prepared patch; it is still true, and it is now the next thing in
  the way.

So the deploy sequence is: move CriomOS's `orchestrate` pin and its
`criomos-home` pin together, and update both hardcoded revisions in
`checks/lojix-ownership` in the same commit. Three values, one commit, or
the gate is red.

### 6.3 On the target, before or with the switch

- **The unit is renamed.** `lojix-daemon.service` → `lojix.service`. The
  switch stops the old unit and starts a new one. That is wanted: the
  running 0.21.1 must stop regardless.
- **The store must be reset once.** The Nexus opens
  `/var/lib/lojix/lojix.sema`, which on Ouranos is the retained schema-v4
  file and is refused; the live v5 data is at `lojix-v5.sema`, a basename
  the Nexus never opens. `systemctl start lojix-reset-store` once
  recreates it. The reset unit writes its own archive and needs no prior
  Nexus start — witnessed by `checks/lojix-nexus-service`, which asserts
  the reset unit's `ExecStartPre` writer command and its
  `LOJIX_CONFIGURATION` environment.
- **The deployment history is left behind.** This assumes the living's
  2026-08-13 words still hold: *"i dont care about any past lojix
  database. how do we get a clean working lojix service running?"*
  (relayed from `reports/lojix-criomos.md` §4.2). If they no longer hold,
  the change is in lojix — the store basename is not selectable.
- **`Query.ByNode` will not answer about Ouranos afterwards.** The new
  store is empty by design.

### 6.4 Two things that would stop a deploy today

1. **A `CompleteHost` evaluation still stops at `modelIsThinkpad`** (§4.3).
   That is upstream of everything in this landing and is the reserved
   design item.
2. **lojix 5.0.0 cannot be built on Prometheus** (§3). If the deploy
   builds on the remote builder — and under the standing cold-machine
   order it must — it fails on a five-second clock wait in lojix's own
   test, with the Nexus alive and simply not yet bound. The fix is one
   line in `nexus/tests/daemon_configuration.rs`: wait on the socket, not
   on `Instant::now()`. It is a lojix change.

### 6.5 One deploy-day hazard for every agent in the estate

Relayed from `reports/orchestrate-review.md` §3.2.5, witnessed there and
**not re-verified at 0.34.0 by this thread**: the 0.32.0-and-later
Orchestrate client refuses Datom curly quotes and requires guillemets,
while the live 0.30.0 client accepts curly quotes — and the `orchestrate`
skill documents curly quotes, with a copyable multi-word-reason example
that will fail. Every agent taking a Lock with a multi-word reason breaks
at cutover, with an error naming neither quotes nor the reason field. The
authored fix is in `Curriculum/skills/orchestrate.md` plus a
regeneration; it is not a CriomOS-home change and is not made here.

## 8. Locks

Acquired and released in the course of this work, all under `FLOW_ID`
f6db8d. `Observe.Locks` was read before each acquisition.

| id | name | why |
|---|---|---|
| 1227 | `F6db8dCriomosLojixLanding` | CriomOS `flake.nix`, `flake.lock`, `modules/nixos/lojix.nix`, `checks/lojix-ownership` |
| 1316 | `F6db8dCriomosNexusServiceCheck` | the two Nexus check files, taken when §1.3's second defect was found; released on landing |
| 1322 | `F6db8dCriomosHomeLanding` | the fifteen CriomOS-home paths the three branches touch |
| 1331 | `F6db8dCriomosHomeOrchestrateRepin` | the Orchestrate module and its two checks |

Receipts 981 and 982, which the brief names as having once protected
CriomOS-home paths, are **not held by anything**: they are absent from the
`Observe.Locks` snapshot taken at the start of this work. The live locks on
CriomOS-home paths are 1019 (`CodexArtifactBrowserFlow`, flow f7941a), which
reserves the `codex-artifact-gateway` files and
`modules/home/profiles/min/codex-artifact-gateway.nix`. A first lock request
naming `modules/home/profiles/min` as a directory was correctly refused —
`LockRejected.PathOverlap` against 1019 — and was re-made naming the eight
files under that directory that the branches actually touch. Nothing in this landing touches an f7941a path.

Also live and relevant: **1260 `OrchestrateNexusActor` (f6db8d) reserves
`/git/github.com/LiGoldragon/orchestrate`**, and that sibling was pushing
while this work ran. Orchestrate `main` moved twice under observation —
`7b965a00` → `2266b06e` → `a73ccec3` — inside about an hour. §5 records the
head at the moment of the repin and the hazard that follows from pinning a
moving branch.

### 4.5 `homeConfigurations` cannot be evaluated against the current producer

This is the most consequential thing the gate found, and it is
pre-existing.

`CriomOS-home/flake.nix:704`:

```nix
homeConfigurations = builtins.mapAttrs mkHomeConfiguration horizon.users;
```

`mapAttrs` over `horizon.users`. The current Horizon producer projects
`users` as a **vector**. Witnessed, against the real projection:

```
… while calling the 'mapAttrs' builtin
  at …/flake.nix:704:28:
   704|       homeConfigurations = builtins.mapAttrs mkHomeConfiguration horizon.users;
error: expected a set but found a list: [ ]
```

`reports/lojix-criomos.md` §2.4 named this as the third of three
unrepaired projection divergences and called it "an attrset operation on a
vector". It is no longer a reading of the source: it is a failure.

**What follows for a deploy.** A `UserEnvironment` deployment builds an
attribute under `homeConfigurations`, and the `horizon` input it is given
is materialized by the deployment tool from the current producer — the
same producer, at the same revision, whose output §2.2 proved equals the
checked-in fixture byte for byte. So **no home generation can be built at
deploy time today.** Not because of anything in this landing, and not
because of the fixture: because Home's flake reads a vector as an
attribute set.

The home-generation build the brief asks for is therefore reported in two
parts, and the split is the finding:

| horizon input | `homeConfigurations.li.activationPackage` |
|---|---|
| the live Ouranos projection, pre-migration shape, `users` an attribute set | evaluates; this is the shape `reports/removals-2.md` §2 and §3.2 gated against |
| the current producer's projection, `users` a vector | **cannot be evaluated** — the error above |

The first is the only one that can be built, and it is built against a
projection shape the producer no longer emits. That is not a gate anyone
should rely on, and saying so is more use than a green line.

This is not repaired here. It changes behaviour rather than restoring it,
the users contract has an unlanded design elsewhere (Orchestrate lock 903,
flow 542442, on CriomOS's `modules/nixos/userHomes.nix` — the OS-side twin
of exactly this), and the living has not been asked which shape wins.

## 5. The Orchestrate repin on CriomOS-home main

### 5.1 What the prepared patch got wrong

`flows/857335/reports/orchestrate-deployment.patch` was read, and applied
by hand rather than with `git apply`, because three of its hunks are
wrong at the current head:

- It pins **`1bc55af1…`**. `main` is now `a73ccec3…` (0.34.0), four
  releases later.
- It adds `test -x "${orchestratePackage}/bin/orchestrate-store-migrate"`
  to `checks/orchestrate-service-path`. That binary **does not exist**:
  `crates/*/Cargo.toml` at `a73ccec3` declares exactly four —
  `orchestrate`, `orchestrate-meta`, `orchestrate-nexus`,
  `orchestrate-upgrade-preflight`. `reports/orchestrate-review.md` §3.2.8
  says the migrator was deleted; the patch re-asserts it. That hunk would
  turn the check red on its own.
- It wraps the `Configure` call's socket paths in guillemets while leaving
  the adjacent `Lock` call's paths bare. `reports/runtime-audit.md` §8
  recorded this asymmetry as an Unknown. It is unnecessary: an absolute
  path with no space is a bare Datom atom, which is why every `Lock`
  request in this report — including the four this thread took — carries
  bare paths and is accepted. The guillemet hunk was dropped.

The patch's one correct and load-bearing hunk is the binary rename, and
that is the ruling.

### 5.2 The ruled name, and the socket name that follows it

`flows/f6db8d/vision/metaCli.md`, the living, typed: *"meta cli names is
`<component>-meta`."* So `meta-orchestrate` → `orchestrate-meta` in the
module wrapper and in both checks.

The socket file is a separate question and the answer is not the same as
the one the patch assumed. Orchestrate 0.34.0 **also** moved the meta
socket's default basename, under the same ruling — witnessed,
`crates/orchestrate-nexus/src/defaults.rs:14`:

```rust
const META_SOCKET_FILE: &str = "orchestrate-meta.sock";
```

The module's exported `ORCHESTRATE_META_SOCKET` and the check's
`metaSocketPath` therefore move to `orchestrate-meta.sock` as well. Doing
only the binary rename, as the patch does, leaves the wrapper exporting a
path the new Nexus does not bind — and the check, which runs a real Nexus
over a fresh store in the sandbox, is what catches that. §6.1 is the
deployed-host consequence, and it is the single most consequential thing
in this report.

### 5.3 The `Configured` reply shape

`reports/orchestrate-review.md` D-3 relayed that the check's expected
reply is stale. Confirmed from the contract source rather than taken on
trust — `signal-orchestrate`'s `ethos/signal.ethos` at the revision
0.34.0 pins:

```
OrchestrateNexusConfiguration.{ OrdinarySocketPath MetaSocketPath }
MetaConfigureDone.Boolean
ConfigurationReceipt.{ OrchestrateNexusConfiguration MetaConfigureDone }
```

and `meta-signal-orchestrate`'s declares `Configured.ConfigurationReceipt`.
`crates/orchestrate-meta/src/main.rs:88` prints
`response.datom_text()`, which is
`datomize().protosize().textualize()` — the generic Datom rendering. A
nested product inside a product, then a boolean, is therefore

```
Configured.{ { <ordinary> <meta> } True }
```

not `Configured.{ <ordinary> <meta> }`. The check now asserts that.

### 5.4 A check that could not be evaluated at all

`checks/orchestrate-wrapper-fallback` is repaired for the reason §4.4
gives: it reads `moduleResult.config` from a module that returns a plain
attribute set, so it has been unevaluable on `main` independently of
anything here. It is given the same three-way fallback its sibling
`checks/orchestrate-service-path` already carried. Renaming a binary
inside a check that cannot be evaluated would have been a change with no
gate behind it.

## Sources

- `flows/f6db8d/vision/metaCli.md` — the living's typed ruling, quoted in
  §5.2, which is the authority for every rename here.
- `flows/f6db8d/reports/lojix-criomos.md` — §1.2's Nexus surface table,
  §1.4's uncompilable pin, §2.2's byte-identical fixture, §3.1 and §5's
  `modelIsThinkpad` stop, §4.2's landing order and the living's quoted
  words on the past Lojix database. Every claim of its own that this
  report repeats was re-witnessed here and is marked as such; §4.2's
  quotation of the living is relayed.
- `flows/f6db8d/reports/lojix-settle.md` §7 — the superseded landing note
  naming lojix 4.0.1 `0bb3d66c`.
- `flows/f6db8d/reports/lojix-honesty.md` §1, §8 — the three released
  producer revisions the brief names, and the note that §7's landing
  recommendation is superseded by 5.0.0.
- `flows/f6db8d/reports/removals.md` §1, §2, §7 and
  `flows/f6db8d/reports/removals-2.md` §2, §3 — the two CriomOS-home
  branches' own gates and their landing notes, including the unfree
  `platform-tools` necessity and the observation that CriomOS's separate
  `rust-overlay` pin is unmoved.
- `flows/f6db8d/reports/orchestrate-review.md` §3.2, §3.3, §7, D-1 to D-4
  — the deployment requirements, the `Configured` shape, the Datom
  delimiter, and the ordinary-Configure hazard. §3.3/D-4 is relayed **and
  contradicted**: §6.1 shows from `store/cutover.rs` that 0.33.0 closed
  it.
- `flows/f6db8d/reports/orchestrate-followup.md` §5, §6 — the open-defect
  table and the unsettled CLI name, now settled by the ruling.
- `flows/f6db8d/reports/runtime-audit.md` §8 — the prepared patch's
  breakage of `checks/lojix-ownership` and the quoting asymmetry it left
  as an Unknown; both resolved here, §1.2 and §5.1.
- `flows/857335/reports/orchestrate-deployment.patch` — read in full; §5.1
  says which hunks were taken and which were not.
- `/git/github.com/LiGoldragon/CriomOS` at `acc3feab4d99`, `c4c830c1`,
  and this thread's `cf3be614` and `b84b99ba` — `flake.nix`, `flake.lock`,
  `modules/nixos/lojix.nix`, `modules/nixos/metal/default.nix`,
  `checks/lojix-ownership`, `checks/lojix-nexus-service`,
  `checks/lojix-nexus-start`, `checks/fixed-location-policy`,
  `checks/laptop-keyboard-keyd`, `checks/metal-firmware-policy`,
  `checks/wispr-keyboard-uaccess`, `stubs/no-system`, `stubs/no-horizon`.
- `/git/github.com/LiGoldragon/CriomOS-home` at `caffe9a17cc5` and the
  three f6db8d branches — read and written as §2 and §5 describe.
- `/git/github.com/LiGoldragon/lojix` at
  `b5cddd2e16ad49d1060cf4109f44c27359195441` — read only: `Cargo.toml`,
  `Cargo.lock`, `flake.nix`, `nexus/tests/daemon_configuration.rs`.
- `/git/github.com/LiGoldragon/orchestrate` at `a73ccec358d2…` (and
  `2266b06e` and `7b965a00` as `main` passed through them) — read only:
  `Cargo.toml`, `crates/*/Cargo.toml`,
  `crates/orchestrate-nexus/src/defaults.rs`,
  `crates/orchestrate-nexus/src/store/cutover.rs`,
  `crates/orchestrate-meta/src/main.rs`, `UPGRADES.md`.
- `/git/github.com/LiGoldragon/signal-orchestrate` at `e7221190…` and
  `/git/github.com/LiGoldragon/meta-signal-orchestrate` at `4279ad05…` —
  read only: `ethos/signal.ethos` in each. These are the contract
  revisions 0.34.0 pins.
- `/git/github.com/LiGoldragon/horizon-rs` at `40d04d2504fe…` — built on
  Prometheus and **run**, not read: `horizon-cli --node atlas` over
  CriomOS-home's checked-in definition, for §2.2.
- `/tmp/horizon-ouranos.json` — the live Ouranos projection in the
  pre-migration shape, used to show that §4.1's failure is independent of
  the `horizon` input and to supply the attrset-shaped `users` the home
  generation needs.
- Commands run by this thread, all quoted above: `nix flake check`,
  `nix build`, `nix eval`, `nix flake lock`, `nix derivation show`,
  `nix log`, `git ls-remote`, `jj`, `orchestrate`, and one run of
  `horizon-cli`.
- The `nix-workflow` skill — "Run Nix builds only through configured
  remote builders", which §3 could not obey and says so; "Keep local
  overrides transient", which is why every `system`/`horizon` override and
  every fixture repair used for probing was reverted; and "Keep
  evaluation and activation evidence separate", which is why §1.3
  distinguishes a drv path from a built check.
- The `testing` skill — "A new test is seen failing once before it is
  trusted" (§1.3's red-then-green), "A test waits on the tested event,
  never on the clock" (§3's diagnosis), and the prohibition on
  change-detectors (§2.3).
- The `nexus` skill and `Vision/nexus.md` — the meta CLI convention the
  ruling confirms, and "call it a Nexus, never a daemon", which is why
  §1.3 renames the check's bindings rather than only its attribute path.
- The `spirit` skill — "Backward compatibility is never a design
  variable", which is why §5.2 moves the socket basename to the new
  default and puts the one-time cost in the deploy note rather than
  keeping the old name forever.
