# W1 and W4: making CriomOS start the Lojix it pins, and reading the Horizon it is given

Subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d,
2026-09-11/12. Work confined to the test bookmark `f6db8d-lojix-start` in
CriomOS and CriomOS-home. Nothing was deployed, no running service was touched,
no `meta-lojix` request was made, and the lojix and horizon-rs repositories were
read but never written — a sibling holds Orchestrate locks 1111 and 1112 on
them.

**witnessed** = this flow ran the command or opened the file and the output is
quoted below. **relayed** = another flow's report says so and is named.
Observations, hypotheses and unknowns are kept apart.

---

## 0. What to look at first

1. **W1 is done and witnessed red-green**, but landing it requires one more
   change this branch could not make: **the lojix revision CriomOS pins does not
   compile.** §1.4. That is a repin, and the repin rewrites `flake.lock`, which
   another f6db8d subflow holds (Orchestrate lock 1123).
2. **W4 is done and witnessed red-green**, against a projection proved
   byte-identical to what Lojix materializes at deploy time. §2.
3. **The complete-system BuildOnly did not reach `BootstrapTerminal.Succeeded`,
   and the reason is upstream of both.** §3.
4. **Two further defects were found while doing this**, neither previously
   reported: the pinned lojix cannot build (§1.4), and lojix's own VM-test
   fixture is stale against the horizon-rs revision lojix itself pins (§3.3).

---

## 1. W1 — CriomOS now starts the Nexus

### 1.1 What was wrong, restated from the evidence

`modules/nixos/lojix.nix:27` at CriomOS `main` (`acc3feab`):

```nix
daemonCommand = "${cfg.package}/bin/lojix-daemon ${cfg.startupArchivePath}";
```

Three separate things made that unable to start:

- **There is no `lojix-daemon`.** Witnessed: the pinned revision's workspace
  declares `[[bin]] lojix-nexus` (`nexus/Cargo.toml`), `lojix`, `lojix-meta`,
  and five offline tools (`tools/Cargo.toml`); no target named `lojix-daemon`
  exists.
- **The Nexus refuses the argument.** `nexus/src/main.rs:19-21` returns
  `Error::UnexpectedNexusArguments` when `args_os().nth(1).is_some()`.
- **The archive was never going to be read.** `src/daemon.rs`
  `EnvironmentConstructible for Daemon` opens `NexusConfiguration::store_path()`
  and reads `store.nexus_configuration_state()?.desired_configuration`. Nothing
  in the Nexus reads the file `lojix-write-configuration` writes.

### 1.2 The shape the Nexus actually has

Witnessed in `src/lib.rs:345-386` at both the pinned revision `23f09f28` and
lojix `main` `fab60e58` — identical in both:

| what | value | how it is chosen |
|---|---|---|
| state directory | `/var/lib/lojix` | `XDG_STATE_HOME`/lojix, else this |
| store file | `<state>/lojix.sema` | fixed basename, not configurable |
| runtime directory | `/run/lojix` | `XDG_RUNTIME_DIR`/lojix, else this |
| ordinary socket | `<runtime>/ordinary.sock` | fixed basename |
| owner socket | `<runtime>/meta.sock` | fixed basename — **not `owner.sock`** |
| socket modes | `0o660` / `0o600` | built in |

`src/daemon.rs:117-124` creates both socket parents and the state directory
itself, so nothing outside needs to.

So CriomOS's module was not merely calling the wrong binary: it was declaring
six values the Nexus does not read, including an owner socket path
(`owner.sock`) the Nexus never binds and a store (`lojix-v5.sema`) it never
opens.

### 1.3 What the branch changes

`CriomOS` `f6db8d-lojix-start` = **`c4c830c10d32e15c6afc055383ca49fef95963fd`**
(one commit on `main` `acc3feab4d99`).

- `modules/nixos/lojix.nix` — `ExecStart` is the pinned package's `lojix-nexus`
  with no argument; the service has no `ExecStartPre` at all. Socket paths,
  socket modes, the store file and the reset archive become `readOnly` options
  derived from `stateDirectoryPath`/`runtimeDirectoryPath`, restating the
  Nexus's own built-in choices so the exported `LOJIX_ORDINARY_SOCKET` /
  `LOJIX_OWNER_SOCKET` and the tmpfiles ownership name what the Nexus opens.
  `lojix-write-configuration` moves onto the manual reset unit — the only
  consumer left, because `lojix-reset-store` takes no path and reads the store
  from a `LOJIX_CONFIGURATION` archive. The unit is `lojix.service`: it is a
  Nexus, not a daemon (`Vision/nexus.md:5`).
- `modules/nixos/lojix-persona-development.nix` — sets only identity
  (`user`, `group`, `nexusHost`) and the SSH-agent endpoint. The eight path and
  mode settings are gone.
- `checks/lojix-daemon-config-roundtrip/` → `checks/lojix-nexus-service/` —
  asserts the zero-argument `ExecStart` and the empty `ExecStartPre` at
  evaluation. The old check asserted the `ExecStartPre` string and never touched
  `ExecStart`; it also grepped the writer's output for `'(ConfigurationWritten ['`,
  a form the writer replaced with `ConfigurationWritten.{ … }`
  (`tools/src/lojix-write-configuration.rs:34`) — so that gate was doubly dead.
- `checks/lojix-nexus-start/` — new NixOS VM test: boots a machine carrying this
  module, waits for both sockets, asserts the unit's `ExecStart` argv, and
  completes one ordinary `Query`.
- `flake.nix` — the two checks registered; `lojix-fresh-daemon-startup` renamed
  `lojix-fresh-nexus-startup`; and a comment recording §1.4.

### 1.4 The pinned lojix revision does not compile — decisive, and blocking

Witnessed:

```
$ nix build --builders '' github:LiGoldragon/lojix/23f09f28accc2d7e9d4e2e8853a0ceb1eb78ac66#default
error: builder failed with exit code 101
  > error: could not compile `meta-signal-lojix` (lib) due to 72 previous errors
  > error[E0599]: no method named `datomize` found for reference `&SecretsInput`
  >   --> …/meta-signal-lojix-2.3.0/src/generated/signal.rs:6:12
  > help: trait `Datomizable` which provides `datomize` is implemented but not in scope
```

Cause, witnessed in `Cargo.lock` at `23f09f28`: it carries **two**
`meta-signal-lojix 2.3.0` entries —

- `rev=6302a9128cd2` → `datom-codec 0.25.7`
- `rev=7e98d8855e74` → `datom-codec 0.25.6`

`nexus/Cargo.toml`'s dev-dependency selects the second; its generated signal
code cannot see `Datomizable` in codec 0.25.6. This is the same class as the two
incompatible `kameo` crates that W10 names, one layer down.

lojix `main` `fab60e584daf1c33a629cb8e2f3c353f9323f40e` carries a **single**
`meta-signal-lojix 3.0.1` and builds:

```
$ nix build --builders '' github:LiGoldragon/lojix/fab60e58…#default
/nix/store/4vaivp475kinb7lm07bankkvlr6bfjy4-lojix-1.0.1
$ ls …/bin
lojix  lojix-bootstrap  lojix-inspect-store  lojix-meta
lojix-migrate-configuration  lojix-nexus  lojix-reset-store  lojix-write-configuration
```

Its Nexus surface is identical to the pinned one on every point the module
depends on (verified field by field: `lojix-nexus`, zero arguments, the same
`DEFAULT_RUNTIME_DIRECTORY`/`DEFAULT_STATE_DIRECTORY`, the same `meta.sock` and
`lojix.sema` basenames, the same `0o660`/`0o600`, the same
`ConfigurationWriteRequest` and `ConfigurationWritten.{ … }` reply).

**The branch does not carry the repin.** Repinning rewrites `CriomOS/flake.lock`,
held by Orchestrate lock 1123 (`F6db8dRemovalsCriomosHome`, also f6db8d). The
branch instead records the defect and the exact remedy in `flake.nix` beside the
pin, and every witness below that needed a built binary used a transient
`--override-input`, per nix-workflow's "keep local overrides transient".

### 1.5 Evaluation witness — ExecStart is the pinned package's Nexus, no argument

Against the **pinned** (`23f09f28`) package, evaluating the branch's module:

```
$ nix eval --impure --builders '' --json --expr 'import …/w1-probe.nix { criomos = "…/f6db8d-lojix-start"; }'
{"execStart":"/nix/store/6dknkqcd2883xm1dp523rxfm143yazqz-lojix-1.0.1/bin/lojix-nexus",
 "execStartIsBarePinnedNexus":true,
 "execStartPre":[],
 "ordinarySocket":"/run/lojix/ordinary.sock",
 "ownerSocket":"/run/lojix/meta.sock",
 "pinnedPackage":"/nix/store/6dknkqcd2883xm1dp523rxfm143yazqz-lojix-1.0.1",
 "storePath":"/var/lib/lojix/lojix.sema"}
```

`execStart` is exactly `pinnedPackage + "/bin/lojix-nexus"`, `execStartPre` is
empty, and the three derived paths are the Nexus's own.

### 1.6 The gate, seen red then green

The same assertions live in `checks/lojix-nexus-service`. Green on the branch:

```
$ nix eval --impure --builders '' --raw --expr '…callPackage ./checks/lojix-nexus-service…'
/nix/store/myh5l7l3ccnhgnkzfsyypn5mfppmjmyj-lojix-nexus-service.drv
```

Red when the argument is put back — one word changed in the module, everything
else identical:

```
error: string '"/nix/store/6dknkqcd…-lojix-1.0.1/bin/lojix-nexus /var/lib/lojix-fixture/reset-configuration.rkyv"'
       is not equal to
       string '"/nix/store/6dknkqcd…-lojix-1.0.1/bin/lojix-nexus"'
```

This is the gate that did not exist: the defect that shipped is now the thing
the check fails on.

### 1.7 VM test

`checks/lojix-nexus-start` boots a NixOS machine carrying this module, waits for
`/run/lojix/ordinary.sock` and `/run/lojix/meta.sock`, asserts the unit's argv,
and completes one ordinary `Query.ByNode`. Run locally with `--builders ''` and
a transient lojix override to a buildable revision — it cannot be run against
the declared pin, because the declared pin does not build (§1.4).

Witnessed, green:

```
$ nix build --impure --builders '' --expr '…callPackage ./checks/lojix-nexus-start { inputs = flake.inputs // { lojix = fab60e58 }; }'
/nix/store/nz17w77h5hjlj7lb8ydya6jp27l94idf-vm-test-run-lojix-nexus-start
```

From the test log, with the ANSI stripped:

```
machine: (finished: waiting for unit lojix.service, in 27.79 seconds)
machine: waiting for success: test -S /run/lojix/ordinary.sock && test -S /run/lojix/meta.sock
machine: (finished: … in 1.08 seconds)
machine: must succeed: systemctl show lojix.service --property=ExecStart --value
         | grep -F 'argv[]=/nix/store/4vaivp475kinb7lm07bankkvlr6bfjy4-lojix-1.0.1/bin/lojix-nexus ;'
machine: (finished: … in 0.04 seconds)
machine: must succeed: LOJIX_ORDINARY_SOCKET=/run/lojix/ordinary.sock
         …/bin/lojix 'Query.ByNode.{ fixture-cluster fixture-node None }'
machine: Queried.{ [] [] { 2 2 } }
(finished: run the VM test script, in 29.33 seconds)
```

The unit reached `active`, the Nexus bound both sockets at the paths CriomOS
exports, systemd's own `ExecStart` argv is the bare `lojix-nexus` with nothing
after it, and one ordinary `Query` returned a typed `Queried` — an empty live
set and GC-root set with the state marker `{ 2 2 }`, which is what a fresh
store should say.

So far as this flow can find, that is the first time a Lojix configured by
CriomOS has answered a request since 2026-09-05.

---

## 2. W4 — the Horizon-projection / consumer mismatch

### 2.1 It does fail an evaluation. Witnessed.

The history report left this as Unknown 1: "Whether §4.4 actually fails an
evaluation. I read both sides but ran no `nix eval`." It does.

The producer was run, not read. `horizon-cli` from horizon-rs
`8f4240ef23024c2d3b55f803d96d3c6e7aa5b433` — the revision `lojix/Cargo.toml`
pins — projecting a composed definition:

```
"machine": { "kind": "Metal", "architecture": "x86_64", "host": null,
             "additionalHosts": [], "user": null, "diskGib": null,
             "hardware": { … } }
```

`machine` keys: `kind, architecture, host, additionalHosts, user, diskGib,
hardware`. **No `arch`.** And the value is lowercase `x86_64`, so
`== "X86_64"` would be false even if the key existed — the consumer is wrong
twice.

Evaluating CriomOS-home `main` (`caffe9a1`, the revision CriomOS pins) against
that projection:

```
error: attribute 'arch' missing
at …/modules/home/profiles/min/default.nix:240:20:
   240|     ++ (optionals (node.machine.arch == "X86_64") [ i7z ]);
      |                    ^
```

The renaming layer the history report allowed for does not exist.

### 2.2 The fixtures were hiding it, and now cannot

`checks/yt-dlp/default.nix:47` and
`checks/ai-agent-launch-orchestration/default.nix:25` each hand-wrote
`horizon.node.machine.arch = "X86_64"` into the module arguments. A fixture
authored to match its consumer can never disagree with it — which is exactly why
this survived months of green checks.

Both now read `fixtures/horizon.nix`, which is
`fromJSON (readFile ./horizon-projection.json)` over the verbatim output of the
real producer, with `fixtures/horizon-definition.datom` kept beside it so the
regeneration is reproducible.

**That fixture is provably the deploy-time shape.** `lojix-bootstrap` was run in
`BuildOnly` mode on the same definition, and its materialized horizon input was
compared with the checked-in fixture:

```
$ diff <(canonical journal/.../generated-inputs/horizon/horizon.json) \
       <(canonical CriomOS-home/fixtures/horizon-projection.json)
IDENTICAL: fixture equals the deploy-time materialized horizon
$ cat journal/.../generated-inputs/horizon/flake.nix
{ outputs = _: { horizon = builtins.fromJSON (builtins.readFile ./horizon.json); }; }
```

So a check reading this fixture sees precisely the attribute set a deploy-time
evaluation sees.

### 2.3 Red, then green, in both directions

`CriomOS-home` `f6db8d-lojix-start` =
**`0176de5f6d9a4a9111adebbff5e2480d31a6dd06`** (one commit on `main`
`caffe9a17cc5`).

- Consumer repaired to `node.machine.architecture == "x86_64"`. The same
  evaluation that said `attribute 'arch' missing` now returns `127` packages,
  and `i7z` is among them (`true`) — the branch is live, not merely
  non-erroring.
- Both checks evaluate against the real projection:
  `yt-dlp` → `/nix/store/wb0jlq8lzx007b72lhn1dazk5fripq2v-yt-dlp-current-source.drv`,
  `ai-agent-launch-orchestration` → `/nix/store/xpfawyzfb7ji9xpvq89rvi76jcnssf3f-….drv`.
- Restoring the old field turns the check red:

```
error: attribute 'arch' missing
at …/modules/home/profiles/min/default.nix:243:20:
   243|     ++ (optionals (node.machine.arch == "X86_64") [ i7z ]);
```

### 2.4 The same class, swept — two more, both unrepaired

Sweeping every `horizon.*` and `node.*` consumer in CriomOS-home against the
real projection:

| consumer | projection | effect |
|---|---|---|
| `modules/home/profiles/min/spirit.nix:32` `horizon.node.services or [ ]` | `node.services` **absent** | silently `[]` — Spirit's node-service predicate can never be true |
| `min/pi-models.nix:37`, `max/browser-use.nix:56` `node.typeIs.largeAiRouter or false` | `node.typeIs` **absent** | silently `false` — no router node is ever found |
| `flake.nix:710` `mapAttrs … horizon.users`; `min/agent-intercom.nix:11` `(horizon.users or { }).${username}` | `users` is a **list** | an attrset operation on a vector |

The first two are `or`-guarded, so they do not fail — they quietly answer wrong,
which is worse than a failure and is the same class 33a4d4 named for CPU vendor,
board class and lid-switch policy. The third is the Home-side twin of the
`userHomes.nix` users-vector repair flow 542442 left on a branch (Orchestrate
lock 903). **None of the three is repaired here**: each changes behaviour rather
than restoring it, the users contract already has an unlanded design elsewhere,
and the living has not been asked. They are named, with their sites, for a
decision.

---

## 3. The complete-system BuildOnly

### 3.1 It did not reach `BootstrapTerminal.Succeeded`

Two `BuildOnly` runs against the branch revision, both
`(BootstrapTerminal.Failed)`. `lojix-bootstrap` discards the failing command's
stderr — §4.3's defect, met directly — so each failure was rediagnosed by
replaying the bootstrap's own `nix eval` by hand against the generated inputs it
left in its journal.

**Run 1**, a `Live` node:

```
error: expected a set but found null: null
… while evaluating definitions from `…/modules/nixos/disks/preinstalled.nix'
… while evaluating the option `boot.loader.systemd-boot.enable'
```

A `Live` node projects `installation: null`, and a `CompleteHost` build wants
disks. A fixture inadequacy, not a CriomOS defect.

**Run 2**, the same node as an `Installation` with two disks:

```
error: attribute 'modelIsThinkpad' missing
at «github:LiGoldragon/CriomOS/c4c830c1…»/modules/nixos/metal/default.nix:37:5:
    36|     chipIsIntel
    37|     modelIsThinkpad
      |     ^
    38|     computerIs
… while evaluating definitions from `…/modules/nixos/metal/default.nix'
… while evaluating the option `assertions'
```

### 3.2 What that result means

This is **33a4d4's blocking finding, now witnessed by an evaluation rather than
inferred**: `modules/nixos/metal/default.nix` reads `chipIsIntel`,
`modelIsThinkpad`, `computerIs` and their neighbours from a horizon node view
the current producer does not emit. The real projection's `node.machine.hardware`
carries `cores, model, motherboard, chipGeneration, ramGib, location`, and
nothing derived.

So the answer to "is a complete-system BuildOnly possible locally?" is: **not
yet, and not because of anything in W1 or W4.** Both repairs are upstream of the
stop, and the stop is the metal-module sweep 33a4d4 named and nobody has done.
`modules/nixos/metal/default.nix` is outside this flow's Orchestrate reservation
and is a behaviour change rather than a restoration, so it was not taken
unasked. It is the next item if you want the BuildOnly.

One thing the attempt did settle, which is worth more than the failure: the
materialization path itself works end to end. `lojix-bootstrap` parsed the
definition, projected the node, wrote the four generated flakes, and drove `nix`
— §2.2's byte-identical `diff` is a by-product of that run.

### 3.3 Two things found on the way

- **The real cluster proposal does not parse.**
  `/git/github.com/LiGoldragon/goldragon/proposal.datom` is refused by the
  pinned horizon-rs at byte 165 — `Structural(… problem: Multiple })`, inside a
  guillemet string that itself contains braces
  (`«/ {/dev/disk/by-label/NIXOS_SD Ext4 []}»`). That is very likely the
  guillemet-escape writer defect another f6db8d subflow is repairing under
  Orchestrate lock 1105 (`ProtosStringRoundTrip`). Not repaired here: it is in
  `protos`, and it is theirs.
  `/git/github.com/LiGoldragon/criomos-horizon-config/horizon.dotos` is refused
  separately — it is still in the pre-Datom parenthesised form
  (`(HorizonProposal …)`), which current Datom reads as Meaning.
- **lojix's own VM-test fixture is stale against the horizon-rs it pins.** The
  proposal string embedded at `lojix/flake.nix` in the
  `same-host-test-activation` check gives a `NodeDefinition` of 10 fields;
  horizon-rs `8f4240ef` requires 11 (`fixed_location_option` was added). Refused
  with `Arity { expected: 11, found: 10 }`. Its curly-quoted string
  `“ssh-ed25519 …”` is also the superseded delimiter; guillemets parse. So that
  check cannot be green at the revision lojix itself pins. **Recorded, not
  fixed — it is a lojix change, and lojix is the sibling's.**

### 3.4 A ninth false statement in the `lojix` skill

W2 lists eight. Here is a ninth, witnessed: the skill says a deployment proposal
"must be an existing absolute regular non-symlink `proposal.datom` file". The
bootstrap validator requires the file to be named
**`horizon-definition.datom`** (`src/bootstrap.rs:2166-2169`,
`safe_existing_regular_file(&input.proposal_source.0, "horizon-definition.datom")`).
A request naming `proposal.datom` is refused with a redacted
`(BootstrapRejected [InvalidRequest])` that says nothing about the name — this
flow lost two attempts to it, which is §4.3's defect in the bootstrap ingress.

---

## 4. Landing note for the living

### 4.1 What to review

**CriomOS `f6db8d-lojix-start` = `c4c830c10d32e15c6afc055383ca49fef95963fd`**
(one commit on `main` `acc3feab4d99`)

1. `modules/nixos/lojix.nix` — the judgement call is that socket paths, socket
   modes and the store file become `readOnly` options *restating* the Nexus's
   built-in choices rather than settings the module makes. The Nexus offers no
   way to set them (only `XDG_STATE_HOME`/`XDG_RUNTIME_DIR`, which append
   `lojix`), so the alternative was to keep declaring values nothing reads.
   The agreement between CriomOS's restatement and the Nexus's real behaviour is
   witnessed at runtime by `checks/lojix-nexus-start`, not at evaluation.
2. The unit rename `lojix-daemon.service` → `lojix.service`. On Ouranos this
   means the switch stops the old unit and starts a new one — which is wanted,
   since the running 0.21.1 must stop regardless. Say if you would rather keep
   the name.
3. `checks/lojix-nexus-start` is a new VM test in CriomOS's check set; it adds a
   NixOS VM build to the gate.

**CriomOS-home `f6db8d-lojix-start` = `0176de5f6d9a4a9111adebbff5e2480d31a6dd06`**
(one commit on `main` `caffe9a17cc5`)

4. `fixtures/horizon-projection.json` is a generated artifact checked into the
   repository. It is regenerated by one command, recorded in
   `fixtures/horizon.nix`. If you would rather CriomOS-home take horizon-rs as a
   flake input and project at check time, say so — that is a larger change and
   was not made unasked.

### 4.2 How to land it

In this order. Steps 1 and 2 are not optional: without them the branch is
correct and still cannot start.

1. **Repin lojix.** `CriomOS/flake.nix` pins `23f09f28`, which does not compile
   (§1.4). Repin to `fab60e584daf1c33a629cb8e2f3c353f9323f40e` or a later
   buildable revision and update `flake.lock`. This branch could not: another
   f6db8d subflow holds `CriomOS/flake.lock` under Orchestrate lock 1123. Land
   that subflow's work first, or release 1123, then repin.
2. **Run the gate with the repin in place.** `checks/lojix-nexus-service` and
   `checks/lojix-nexus-start`. `lojix-nexus-start` is the one that matters: it
   is the first CriomOS gate that observes Lojix actually answering.
3. **Land CriomOS-home first, then CriomOS.** CriomOS pins CriomOS-home by
   revision; the Home repair must be a published revision before CriomOS's pin
   moves to it. The `min` profile repair is independent of the lojix work and
   can land on its own.
4. **On Ouranos, before or with the switch: the store.** The Nexus opens
   `/var/lib/lojix/lojix.sema`, which is the retained **schema-v4** file; it is
   refused. The live v5 data is at `lojix-v5.sema`, which the Nexus will never
   open — its basename is fixed. Two facts follow:
   - `systemctl start lojix-reset-store` once recreates the v4 file as v5. The
     reset unit now writes its own archive, so it needs no prior Nexus start.
   - **The deployment history in `lojix-v5.sema` is left behind.** You said on
     2026-08-13, "I dont care about any past lojix database. how do we get a
     clean working lojix service running?" — this note assumes that still holds.
     If it does not, the change is in lojix (make the store file selectable, or
     migrate), and it is the sibling's repository.
5. **Do not expect `Query.ByNode` to answer about Ouranos afterwards.** The new
   store is empty by design; that is W5, untouched here.

### 4.3 What is still owed, from this work

- The repin (§1.4) — blocked on lock 1123, not on judgement.
- The three unrepaired projection/consumer divergences (§2.4) — need your
  direction, not more investigation.
- lojix's stale `same-host-test-activation` fixture (§3.3) — a lojix change;
  exact repair recorded there.
- The `protos` guillemet defect that makes the real cluster proposal unparsable
  (§3.3) — already in hand under lock 1105.
- The skill's ninth false statement (§3.4) — for W2's proposal.

---

## Sources

- `flows/f6db8d/reports/lojix-history.md` — W1 and W4 as stated, §4.1, §4.4,
  §5; the living's quoted words on the past database and on redeployment.
- `/git/github.com/LiGoldragon/CriomOS` at `acc3feab4d99` and this flow's
  `f6db8d-lojix-start` `c4c830c10d32e15c6afc055383ca49fef95963fd`.
- `/git/github.com/LiGoldragon/CriomOS-home` at `caffe9a17cc5` and this flow's
  `f6db8d-lojix-start` `0176de5f6d9a4a9111adebbff5e2480d31a6dd06`.
- `/git/github.com/LiGoldragon/lojix` at `23f09f28accc2d7e9d4e2e8853a0ceb1eb78ac66`
  (the pin) and `fab60e584daf1c33a629cb8e2f3c353f9323f40e` (`main` at the time
  of writing) — read only; `nexus/src/main.rs`, `src/daemon.rs`, `src/lib.rs`,
  `src/bootstrap.rs`, `tools/Cargo.toml`, `tools/src/lojix-write-configuration.rs`,
  `Cargo.lock`, `flake.nix`.
- `/git/github.com/LiGoldragon/horizon-rs` at
  `8f4240ef23024c2d3b55f803d96d3c6e7aa5b433` — read only; `lib/src/model.rs`,
  `lib/src/projection.rs`, `lib/src/generated/horizon.rs`, `cli/src/main.rs`,
  `cli/tests/compose.rs`, `flake.nix`.
- `/git/github.com/LiGoldragon/goldragon/proposal.datom` and
  `/git/github.com/LiGoldragon/criomos-horizon-config/horizon.dotos` — read only.
- Commands run by this flow, all quoted above: `nix build` of lojix at both
  revisions and of horizon-rs `horizon-compose`/`default`; `horizon-cli`
  projections; `nix eval` of the Home consumer, of the two Home checks, and of
  the CriomOS module and check; `lojix-bootstrap` in `BuildOnly` mode; the
  `diff` of the materialized horizon against the checked-in fixture.
- Orchestrate `Observe.Locks` snapshot taken at the start of this work: locks
  1111 and 1112 (lojix, horizon-rs — the sibling), 1123
  (`CriomOS/flake.lock`, `CriomOS-home/flake.nix`, `CriomOS-home/flake.lock`),
  1105 (`protos`), 903 (`CriomOS/.../userHomes.nix`, flow 542442).

---

## 5. Continuing past the `modelIsThinkpad` stop — subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834`, 2026-09-11

Dispatched to drive §3's complete-system `BuildOnly` past the
`modelIsThinkpad` stop: find where it was supposed to come from, fix it at the
source rather than with a hiding default, and keep going. Held Orchestrate
lock 1157 (`F6db8dMetalHorizonFields`, this flow) on
`CriomOS/modules/nixos/metal/default.nix` for the duration; released on
completion. No file in CriomOS or CriomOS-home was edited — the finding below
is why.

**witnessed** = this thread ran the command or opened the file and the output
is quoted below. **relayed** = 33a4d4's report, named, says so; this thread
did not take it on faith and reproduced it independently (§5.1, §5.2).

### 5.1 The stop reproduced independently

Built a standalone `nixosSystem` evaluation of
`CriomOS/modules/nixos/metal/default.nix` against the real
`horizon.node` — the same `fixtures/horizon-projection.json` §2.2 proved
byte-identical to what Lojix materializes at deploy time, its `node` object
extracted and fed in directly, no hand-written fixture involved:

```
$ nix eval --impure --builders '' --json --expr '(lib.nixosSystem {
    specialArgs = { inputs = flake.inputs; deployment = {…}; horizon.node = realNode; };
    modules = [ .../modules/nixos/metal/default.nix { system.stateVersion = "26.05"; } ];
  }).config.assertions'
error: attribute 'modelIsThinkpad' missing
at …/modules/nixos/metal/default.nix:37:5:
    36|     chipIsIntel
    37|     modelIsThinkpad
      |     ^
    38|     computerIs
```

Identical stop to §3.1 Run 2, reached without a bootstrap run — confirming the
defect is in the module/projection contract itself, not an artifact of the
bootstrap's fixture handling.

### 5.2 Where `modelIsThinkpad` (and its neighbours) were supposed to come from

`horizon.node` is a projected `Node` view from horizon-rs. Witnessed against
the pinned revision `8f4240ef23024c2d3b55f803d96d3c6e7aa5b433` and against the
current fixture: `node.machine.hardware` carries `cores, model, motherboard,
chipGeneration, ramGib, location`; `node.behavesAs` carries the closed
`BehavesAs` boolean set. Neither carries `chipIsIntel`, `modelIsThinkpad`,
`computerIs`, `handleLidSwitch`, `handleLidSwitchExternalPower`, or
`handleLidSwitchDocked`, nor any field that renames to one — confirmed by
grepping the pinned revision's `view/node.rs` for every spelling: zero hits.

These are not a producer/consumer naming mismatch like W4's `arch` →
`architecture` (§2). They were a real, named horizon-rs feature that was
**deliberately removed**, witnessed in horizon-rs's own history
(`/git/github.com/LiGoldragon/horizon-rs`, read only):

- `8e28bca` "KnownModel: add ThinkPadE15Gen2Intel, GmktecEvoX2, Rock64 +
  ComputerIs flags for Nix consumers" — the feature existed: a closed
  `KnownModel` enum matched against `machine.model`, projected as a
  `ComputerIs` struct (`thinkpad_t14_gen2_intel`, …, `thinkpad_e15_gen2_intel`,
  `thinkpad_x230`, `thinkpad_x240`, `gmktec_evo_x2`, `rock64`, `rpi3b`) plus a
  parallel `TypeIs` struct and a `LidSwitchPolicy`.
- `f1a5eca` "horizon-lib: drop TypeIs + ComputerIs (enum-shadow structs)" —
  witnessed via `git diff f1a5eca~1 f1a5eca`: `ComputerIs`, `TypeIs`,
  `KnownModel`, and `LidSwitchPolicy` are deleted outright, and `BehavesAs` is
  rederived directly from `NodeSpecies` instead of through `TypeIs`. The
  commit message names the reason: they were "enum-shadow structs" — a design
  judgement against per-model closed-enum flags, not an oversight.

So `modelIsThinkpad` and its neighbours have no current source of truth to
repoint at. The concept they named was intentionally retired from Horizon's
typed contract, and `modules/nixos/metal/default.nix` (ThinkPad battery
thresholds, `acpi_call`, `thinkfan`, lid-switch handling, the RPi3b branch,
Intel microcode/`intelUtils` gating) was never migrated off it. Fixing this at
the source of truth is not available as a mechanical repair: there is no
projection field, machine record, or removed-but-restorable option to read
instead. The only paths forward are design choices —
whether Horizon should re-expose typed hardware classification (and in what
shape, now that `KnownModel` is gone), whether CriomOS should instead match on
the raw `machine.hardware.model` string itself, or whether these
ThinkPad/RPi3b-specific behaviours belong somewhere else entirely — and this
thread has "no host/model-name heuristics or default policies were invented"
already recorded against it once (33a4d4, log.md line 25). Inventing a
default here (e.g. `modelIsThinkpad or false`) would silently disable every
real ThinkPad's battery/thermal/lid handling, which is exactly the failure
mode `min/spirit.nix`'s `or [ ]` and `pi-models.nix`'s `or false` already
demonstrate at §2.4.

### 5.3 Where this stops

This is the "needs the living" stop named in the dispatch: a design choice
about how (or whether) hardware-model semantics re-enter the Horizon
contract, not a running-service change and not resolvable by more evaluation.
No further stop past it was reached, because none of `modelIsThinkpad`'s
uses can be given a real value without that choice. The complete-system
`BuildOnly` still does not reach `BootstrapTerminal.Succeeded`; §3's landing
note is otherwise unchanged, with one addition:

- **New, for the living's decision list (alongside §2.4's three)**: how
  `chipIsIntel`, `modelIsThinkpad`, `computerIs.{thinkpadT14Gen2Intel,
  thinkpadT14Gen5Intel, thinkpadE15Gen2Intel, thinkpadX230, thinkpadX240,
  gmktecEvoX2, rock64, rpi3b}`, and `handleLidSwitch{,ExternalPower,Docked}`
  should be reconstituted (or their CriomOS consumers rewritten), now that
  horizon-rs's `KnownModel`/`ComputerIs`/`TypeIs`/`LidSwitchPolicy` are gone
  by design. Every real-machine consequence of not deciding this
  (`modules/nixos/metal/default.nix` lines 134, 302, 336, 342, 362, 401, 441,
  509 [`chipIntel` via `intelUtils`], 536, 541, 612, 617) sits behind it, and
  five checks (`wispr-keyboard-uaccess`, `metal-firmware-policy`,
  `fixed-location-policy`, `laptop-keyboard-keyd`, plus `metal-firmware-policy`
  again for the Intel/ThinkPad-true branch) currently pass only because they
  hand-write these retired fields into their fixtures — the same shape of
  false-green W4 (§2.2) found and closed for `arch`.

### Sources

- `flows/f6db8d/reports/lojix-criomos.md` §3 (this file, unedited above this
  section) — the `BuildOnly` run and its `modelIsThinkpad` stop, as this
  thread was dispatched against.
- `flows/33a4d4/log.md` lines 24-26 — relayed: the same finding, reached by
  `remember`/`hotfix` without a `nix eval` witness at the time.
- `/git/github.com/LiGoldragon/CriomOS` `f6db8d-lojix-start`
  `c4c830c10d32e15c6afc055383ca49fef95963fd` — read only;
  `modules/nixos/metal/default.nix`, and a transient (unsaved, not committed)
  probe expression evaluated against it with `nix eval --impure`.
- `/home/li/wt/github.com/LiGoldragon/CriomOS-home/f6db8d-lojix-start`
  `fixtures/horizon-projection.json` — read only; its `node` object fed
  directly into the probe above.
- `/git/github.com/LiGoldragon/horizon-rs` — read only, git history only
  (no build, no eval): `git show` of `8f4240ef23024c2d3b55f803d96d3c6e7aa5b433:lib/src/model.rs`
  and `:lib/src/view/node.rs`; `git log -S` for `Thinkpad`/`ThinkPad`/
  `modelIsThinkpad`; `git diff f1a5eca~1 f1a5eca` on
  `lib/src/view/node.rs`. Lock 1112 (another f6db8d subflow) reserves this
  repository for writing; nothing was written to it here.
- Orchestrate: acquired lock 1157 (`F6db8dMetalHorizonFields`, this flow) on
  `CriomOS/modules/nixos/metal/default.nix` before evaluating; released after.
  `Observe.Locks` re-checked before acquiring — unchanged from the snapshot
  above plus locks opened by other subflows in the interim (1126-1156), none
  on this path.
