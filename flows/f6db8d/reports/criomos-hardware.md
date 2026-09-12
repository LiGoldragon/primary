# Hardware classification in CriomOS, and the metal fixtures

Subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d,
2026-09-12. Brief: implement `reports/design-decisions.md` item 5 — recompute
what `modules/nixos/metal/default.nix:37` and its neighbours need from the live
Horizon fields, in CriomOS itself, with no host-name heuristics and no defaults
that silently disable ThinkPad battery/thermal/lid behaviour; give the four
metal check fixtures the real producer's shape, generated from the pinned
`horizon-compose` where possible; make the whole `checks` output evaluate; then
drive the complete-system `BuildOnly` of `reports/lojix-criomos.md` §3 as far as
it goes. The coordinator added, mid-task, that branch `f6db8d-remote-only-builds`
lands on main first. Nothing was deployed: no activation, no switch, no
`lojix-meta` request, no running service touched.

**witnessed** — this thread ran the command or opened the file and the text
below is what came back. **relayed** — a named report or file says so; not
re-verified here. **this thread's inference** — reasoning, not a ruling.

## 0. What to read first

1. **CriomOS main moved twice.** `b84b99ba` → `79cc994a` (remote-only builds)
   → `8fcfbfec` (hardware classification). Both pushed and verified against the
   real remote URL (§5).
2. **The `modelIsThinkpad` stop is gone**, and the complete-system `BuildOnly`
   is past it (§4). The next stop is named in §4.3 and it is not in the
   hardware group.
3. **Two upstream defects were corrected on the way, not just relocated**
   (§1.3): `chipIsIntel` was derived from the architecture and so claimed Intel
   microcode and Intel GPU drivers for every AMD machine we own; and
   `ThinkPadE15Gen2Intel` and `ThinkPadX250` were never in the retired
   `KnownModel` table, so tiger has been running as a non-ThinkPad.
4. **`fixtures/horizon-node.nix` is producer output**, not a transcription
   (§2), and this run proved it against what `lojix` itself materializes.
5. **Two pieces of the item could not be landed**: registering the new check in
   `flake.nix` and dropping `typeIs.largeAiRouter` from
   `checks/lojix-ownership`. Both paths are inside Orchestrate lock 1227, still
   held by a sibling f6db8d subflow at the time of writing. §6.

## 1. The module change

### 1.1 What was read from the projection, and what is now computed

**Witnessed**, `modules/nixos/metal/default.nix` on `b84b99ba`, lines 33-41:

```nix
  inherit (horizon.node)
    behavesAs
    size
    chipIsIntel
    modelIsThinkpad
    computerIs
    handleLidSwitch
    handleLidSwitchExternalPower
    handleLidSwitchDocked
    ;
```

Six of those eight names are absent from the projection. **Witnessed** against
the pinned producer's own source, `horizon-rs/lib/src/model.rs:22-131` at
`40d04d2504fee619e9b2b2564b8a769a3a9d6049` (the revision `flake.lock` pins):
`Node` carries `machine`, `behavesAs`, `size` and thirty-odd others;
`HardwareView` carries `cores, model, motherboard, chipGeneration, ramGib,
location`; `BehavesAs` carries eleven booleans. None of `chipIsIntel`,
`modelIsThinkpad`, `computerIs`, `handleLidSwitch{,ExternalPower,Docked}`
appears anywhere in it.

The replacement, in the same file:

- `modelFactsIndex`, an attrset keyed by model name, each row giving
  `isThinkpad`, `chipIsIntel` and `isRpi3b`.
- `modelFacts`, which throws by name on a model absent from the table and
  throws on `model == null`, naming the file to add a row to.
- `lidSwitch = { onBattery; onExternalPower; docked; }`, derived from
  `behavesAs.center`, `behavesAs.lowPower` and `behavesAs.edge`.

Twelve call sites were repointed (`isThinkpad`, `chipIsIntel`, `isRpi3b`,
`lidSwitch.*`), and the dead `# !typeIs.center;` comment at line 608 was
dropped. No host name is read anywhere in the file, and there is no `or`
default on any of it.

### 1.2 The lid-switch derivation is the retired one, unchanged

**Witnessed**, `git show f1a5eca~1:lib/src/view/node.rs` in horizon-rs, the
body of `BehavesAs::lid_switch_policy`, and `proposal/node.rs:227-229` which
maps its three fields onto the three view fields CriomOS read:

```rust
        let on_battery = if self.center { Ignore } else { Suspend };
        let on_external_power = if self.center { Ignore }
            else if self.low_power { Suspend } else { Lock };
        let docked = if self.edge { Lock } else { Ignore };
…
            handle_lid_switch: lid_policy.on_battery,
            handle_lid_switch_external_power: lid_policy.on_external_power,
            handle_lid_switch_docked: lid_policy.docked,
```

`LidSwitchAction` serialises `#[serde(rename_all = "lowercase")]`, so the
strings CriomOS received were `"ignore" | "suspend" | "lock"` — exactly what
`logind.conf` accepts and exactly what the new `lidSwitch` attrset produces.
`center`, `lowPower` and `edge` are all three still in today's `BehavesAs`
(**witnessed**, `model.rs:120-131`). So this relocation changes no behaviour
for any node, and `reports/design-decisions.md` item 5(a) is right that this
group never belonged with the model flags.

### 1.3 Two upstream defects corrected rather than relocated

**This thread's findings, both witnessed in horizon-rs's own source.**

**`chipIsIntel` was not a chip fact.** `git show
f1a5eca~1:.jjconflict-base-0/lib/src/proposal/node.rs:166` reads
`let chip_is_intel = ctx.resolved_arch.is_intel();` and
`species.rs:110-112` defines `is_intel` as
`matches!(self, Arch::X86_64)`. So every x86_64 node in the estate — Prometheus,
a GMKtec EVO-X2 with an AMD Strix Halo — was told its chip was Intel. In
CriomOS that drove `hardware.cpu.intel.updateMicrocode`, `intelUtils` in
`environment.systemPackages`, and the `treatAsIntel` GPU-driver branch. Reading
it from the model table makes `chipIsIntel = false` for `GMKtec EVO-X2`,
`rock64`, `rpi3B` and the generic `all-x86-64`, and `true` only for the named
Intel ThinkPads. `reports/design-decisions.md` item 5 proposed taking
`chipIsIntel` from the architecture; this thread did not, and the reason is
this paragraph. It is also one mechanism fewer: the module now reads
`machine.hardware.model` and nothing else about the chip.

**Two ThinkPads were classified as non-ThinkPads.** `ModelName::known`
(**witnessed**, `git show f1a5eca~1:.jjconflict-base-0/lib/src/name.rs:82-90`)
matched exactly five strings: `ThinkPadX230`, `ThinkPadX240`,
`ThinkPadT14Gen2Intel`, `ThinkPadT14Gen5Intel`, `rpi3B`. `KnownModel` had
`ThinkPadE15Gen2Intel`, `GmktecEvoX2` and `Rock64` as variants that
`known()` could never return, and `modelIsThinkpad` was
`known().is_some_and(is_thinkpad)`. So `ThinkPadE15Gen2Intel` — tiger, a real
machine in `goldragon/proposal.datom` (**witnessed**) — projected
`modelIsThinkpad = false` and got no battery thresholds, no `thinkfan`, no
`acpi_call`, no `battery-ctl`, while `modelFirmwareIndex` and
`modelKernelModulesIndex` in the very same CriomOS file branched on its name.
`ThinkPadX250` was in neither table but is keyed in
`modelKernelModulesIndex` and in `gpuUsesVaapi`. Both are `isThinkpad = true`
in the new table. **This is a behaviour change on a real machine and it is
deliberate**; it is the correction the closed-enum shadow was hiding.

### 1.4 The refusal, seen

**Witnessed**, evaluating the landed module against the real projection with an
unclassified model:

```
error: CriomOS does not classify the machine model AcmeLaptop9000.
Add a row for it to modelFactsIndex in modules/nixos/metal/default.nix
saying whether it is a ThinkPad, whether its chip is Intel, and whether
it is a Raspberry Pi 3B.
```

This is what item 5 asks for in place of `KnownModel`, and it is strictly
better than what was there: `KnownModel::known()` returned `Option` and the
projection emitted all-false for an unrecognised string, so a typo meant a
silently unconfigured machine. `model == null` throws too, naming what is
missing — a bare-metal node whose Horizon definition omits its model gets an
error rather than a ThinkPad-less ThinkPad.

## 2. The fixtures

### 2.1 What the four were doing

**Witnessed**, on `b84b99ba`, all four of
`checks/{fixed-location-policy,laptop-keyboard-keyd,metal-firmware-policy,wispr-keyboard-uaccess}/default.nix`
wrote, by hand:

```nix
    chipIsIntel = false;
    computerIs.rpi3b = false;
    handleLidSwitch = "ignore";
    handleLidSwitchDocked = "ignore";
    handleLidSwitchExternalPower = "ignore";
    machine = {
      chipGen = null;
      model = "all-x86-64";
    };
    modelIsThinkpad = false;
```

Two separate falsehoods in nine lines. The five retired fields were being
supplied by the fixture, so the checks stayed green on a contract that had been
deleted. And `machine.{chipGen,model}` is flat, while the module reads
`horizon.node.machine.hardware.model` and
`horizon.node.machine.hardware.chipGeneration` — so these four were already
*red*, and because `flake.nix:174` forces every check's value through
`filterAttrs`, one throwing check made the entire `checks` attrset unevaluable.
That is `reports/landings-criomos.md` §4.1, reproduced here.

### 2.2 One shared projection, and it is producer output

`fixtures/horizon-node.nix` now reads `fixtures/horizon-projection.json`, and
that JSON is not hand-written. **Witnessed**: `horizon-cli` was built from the
pinned producer revision on Prometheus
(`nix build --max-jobs 0 github:LiGoldragon/horizon-rs/40d04d2504fee619e9b2b2564b8a769a3a9d6049#default`
→ `/nix/store/6xlkrqa8axf11xdc8x7rav5h569a8kps-horizon-0.10.1`, built on
`ssh-ng://nix-ssh@prometheus.goldragon.criome`), and

```sh
horizon-cli --node atlas < fixtures/horizon-definition.datom
```

produced the committed JSON. Both files are committed, so the regeneration is
reproducible from the repository alone.

**Witnessed independently in this thread's own `BuildOnly` run** (§4): the
`horizon.json` `lojix-bootstrap` materialized into the generated `horizon`
flake input carries the same shape — `machine.hardware.{cores,model,
motherboard,chipGeneration,ramGib,location}` nested under
`machine.{kind,architecture,host,additionalHosts,user,diskGib}`, the eleven-field
`behavesAs`, `size` as the string `"Max"`. So the fixture is the deploy-time
attribute set, confirmed against the deploy path rather than against a reading
of the producer's source.

`node overrides` applies overrides recursively, so each check now states only
what its own assertion is about: `fixed-location-policy` states
`fixedLocation` and `behavesAs.edge`; `metal-firmware-policy` states the model
and the size; `laptop-keyboard-keyd` states `keyboard = "Colemak"`.

### 2.3 Three fields that are still not the producer's

`fixtures/horizon-node.nix` keeps a `consumerPending` block, and the report owes
an account of it rather than a silence. The modules read three things the
current projection does not emit:

- **`size` as four "at least" booleans.** The projection carries a `Magnitude`
  name (**witnessed**, `model.rs:28` `pub size: String`, and this run's
  materialized `horizon.json` says `"size": "Max"`). The retired projection
  carried `AtLeast { min, medium, large, max }`, derived as
  `self >= Magnitude::X` — **witnessed**, `git show
  95593688:lib/src/magnitude.rs:20-46` in horizon-rs. So the derivation is one
  comparison and is trivially recoverable, but it is read by
  `modules/nixos/{metal,edge,normalize,nspawn}` and
  `modules/nixos/nix/retention-agent.nix` together, and moving it is its own
  change with its own gate, not a rider on this one.
- **`wantsPrinting` and `wantsHwVideoAccel`.** These are operator opt-ins that
  **no horizon-rs revision has ever emitted** — a grep of the whole history for
  `wants_printing`, `wants_hw_video` and `has_video_output` returns nothing for
  the first two and only the deleted `has_video_output` for the third
  (**witnessed**). They need either a new Horizon field or a CriomOS-side
  decision, and neither exists. This is a decision for the living, not an
  implementation gap this thread could close.

Keeping them in one named block, in the fixture, is the honest arrangement: it
says exactly which fields are not the producer's and why, instead of scattering
them through five checks as if Horizon had supplied them.

## 3. The new check, seen red then green

`checks/metal-model-classification/default.nix` asserts the three behaviours
item 5 names, and it was seen failing before it was trusted.

**Witnessed**, the new check evaluated against the *pre-change* module (the
module restored from `git show HEAD:` for the length of one command, then put
back):

```
       … while evaluating the option `services.thinkfan.enable':
       error: attribute 'modelIsThinkpad' missing
       at …/modules/nixos/metal/default.nix:37:5:
           36|     chipIsIntel
           37|     modelIsThinkpad
             |     ^
           38|     computerIs
```

That is the same stop as `reports/lojix-criomos.md` §3.1 run 2 and §5.1,
reached from the new check — so the check's subject is precisely the defect.

**Witnessed**, the same check against the changed module, built on Prometheus:

```
building '/nix/store/kvmslh78rs453dgfxhbmjjry0yxh569n-metal-model-classification.drv'
  on 'ssh-ng://nix-ssh@prometheus.goldragon.criome'...
```

exit 0. What it pins:

- a `ThinkPadT14Gen5Intel` projection keeps `services.thinkfan.enable`,
  `systemd.services.battery-charge-default`, `battery-ctl` in
  `environment.systemPackages`, the `power` group, and
  `hardware.cpu.intel.updateMicrocode` — the five things A31 warned would be
  silently lost;
- an `all-x86-64` projection keeps none of them, including not claiming Intel;
- a `center` node gets `HandleLidSwitch`, `HandleLidSwitchExternalPower` and
  `HandleLidSwitchDocked` all `"ignore"`; a low-power edge node gets
  `"suspend"`, `"suspend"`, `"lock"`;
- an `rpi3B` projection keeps `cma=32M` in `boot.kernelParams` and a non-rpi
  one does not;
- an unclassified model and a null model each make the evaluation throw, asserted
  through `builtins.tryEval (lib.deepSeq …)` so that a `false` default would
  fail the check rather than pass it.

The other four checks, built on Prometheus at the same tree, all exit 0
(**witnessed**): `fixed-location-policy`, `metal-firmware-policy`,
`laptop-keyboard-keyd` (fetched from the Prometheus cache — the derivation is
unchanged by the fixture rewrite), and `wispr-keyboard-uaccess`, whose NixOS VM
test ran to completion on Prometheus against the new fixture:

```
vm-test-run-wispr-keyboard-uaccess> test script finished in 19.58s
copying path '/nix/store/3z2rm103cn2r1jwwmhjjp5xm0gimdjdl-vm-test-run-wispr-keyboard-uaccess'
  from 'ssh-ng://nix-ssh@prometheus.goldragon.criome'
```

That one matters more than the others, because it is the only check here that
boots the configuration the fixture produces rather than reading an option out
of it: the physical-keyboard uaccess rules, the activation service and the udev
database all behave the same on the real projection as they did on the
hand-written node.

## 4. The complete-system BuildOnly

### 4.1 Getting the request accepted at all

`reports/lojix-criomos.md` §4.3 records that `lojix-bootstrap` discards the
failing command's stderr and redacts its rejections. This thread lost four
attempts to that, and the two causes are worth recording because they are not
in the `lojix` skill.

- **The installed binary is not the pinned one.** `which lojix-bootstrap` →
  `/nix/store/628yi3nrywgfl425nmdd1f8bi8hhb4kq-lojix-0.21.1/bin/lojix-bootstrap`
  (**witnessed**), while CriomOS `flake.lock` pins lojix
  `b5cddd2e16ad49d1060cf4109f44c27359195441` (5.0.0). The pinned one was built
  on Prometheus and used instead
  (`nix build --max-jobs 0 github:LiGoldragon/lojix/b5cddd2e…#lojix-bootstrap`
  → `/nix/store/w0m0ixyvmvh93l16ywz5cjjz0lnby2gi-lojix-bootstrap`).
- **The journal parent, the gc root's parent and the evidence path's parent
  must be mode `0700` and owned by the caller.** **Witnessed**,
  `src/bootstrap.rs` at the pinned revision: `private_existing_directory` →
  `private_directory_metadata`, which refuses unless
  `metadata.mode() & 0o777 == PRIVATE_DIRECTORY_MODE` where
  `PRIVATE_DIRECTORY_MODE = 0o700`. A default-umask `0755` directory is refused
  with a bare `(BootstrapRejected [InvalidRequest])` that says nothing about
  permissions. **The `lojix` skill does not mention this**, and it is the
  single most likely reason an agent's first bootstrap request fails. Creating
  the parents `chmod 700` was the whole fix; the request text was correct from
  the first attempt.

Two further skill corrections, both **witnessed** at the pinned revision:

- The skill says `BuildOnly` carries "a direct immutable build request". It
  carries a `BootstrapInput`, which is `Direct.{ flake system selector }` **or**
  `Horizon.{ proposal cluster node shape secrets flake system selector }`. The
  complete-system build is the `Horizon` arm; the skill describes only the
  first and does not say the second exists.
- `reports/lojix-criomos.md` §3.4 already filed that the proposal must be named
  `horizon-definition.datom`, not `proposal.datom`. Still true at 5.0.0.

### 4.2 The run

**Witnessed**, the accepted request (paths abbreviated):

```sh
lojix-bootstrap 'BootstrapRun.{f6db8dhw BuildOnly.{Horizon.{<dir>/horizon-definition.datom
  alpha atlas CompleteHost NoSecrets
  github:LiGoldragon/CriomOS/8fcfbfecb420952ed686dbb635d57b51125d6462
  x86_64-linux nixosConfigurations.target.config.system.build.toplevel}
  NixBuilder.«ssh-ng://nix-ssh@prometheus.goldragon.criome x86_64-linux …»
  <dir>/journal <dir>/gcroot <dir>/evidence.datom}}'
```

Reply: `(BootstrapTerminal.Failed)`. Materialization succeeded — the journal
holds all four generated input flakes (`horizon`, `system`, `deployment`,
`secrets`) and the `horizon.json` quoted in §2.2 — and the failure is in the
evaluation, whose stderr the bootstrap discards. Replaying it by hand with the
same four `--override-input` arguments the bootstrap builds:

```
… while evaluating the option `system.build.toplevel':
… while evaluating the option `assertions':
… while evaluating the option `home-manager.users':
… while evaluating definitions from `…/modules/nixos/userHomes.nix':
error: expected a set but found a list: [ ]
```

### 4.3 The stop, and it is not the hardware group

**The `modelIsThinkpad` stop is gone.** The complete-system evaluation now gets
past `modules/nixos/metal/default.nix` entirely — past `assertions`, past
`boot`, past `services.logind`, past `services.thinkfan` — and stops in a
different module on a different field group.

**The next stop is `modules/nixos/userHomes.nix:29`**:

```nix
  homeUsers = lib.filterAttrs (_name: user: user.hasPubKey) horizon.users;
```

`horizon.users` is a **vector** in the current projection — **witnessed**,
`model.rs:14` `pub users: Vec<User>`, and this run's materialized
`horizon.json` has `"users": []`, a JSON list. `lib.filterAttrs` on a list is
the `expected a set but found a list` above. It is the same class of defect as
the one this change fixes (a consumer left behind by a producer's shape change),
in the users group rather than the hardware group.

**It is another flow's declared work**: Orchestrate lock 903,
`CriomosUserHomesVectorRepair`, flow 542442, reason "Repair the current Horizon
users-vector home projection evaluation", on that exact file in 542442's own
worktree (**witnessed**, `Observe.Locks`). This thread did not take it.

So the answer to "is a complete-system `BuildOnly` possible?" is: not yet, and
for the first time the reason is not the metal module. After `userHomes.nix`,
the three fields of §2.3 are the next thing a real projection will hit, because
`size` arrives as `"Max"` and `modules/nixos/{metal,edge,normalize,nspawn}` and
`nix/retention-agent.nix` read `size.min`, `size.large`, `size.max`. Those two
items — the users vector and the `size`/`wants*` group — are what stand between
here and `BootstrapTerminal.Succeeded`, on this thread's evidence.

## 5. The gate

**Witnessed**, `nix flake check -L --max-jobs 0 --impure` with
`NIXPKGS_ALLOW_UNFREE=1` and the four real inputs this run's own materialization
produced (`--override-input horizon|system|deployment|secrets` pointing at the
bootstrap's generated flakes), on the landed tree:

```
checking flake output 'checks'...
error:
       … while checking flake output 'checks'
         at …/flake.nix:290:7
       … in the left operand of the update (//) operator
         at …/flake.nix:178:22
       error: MS2130 UVC patch must be reviewed for the selected kernel
```

That is the whole of it. The four metal fixtures no longer throw, so
`flake.nix:178`'s `filterAttrs` gets through them, and the one remaining thing
that makes the `checks` attrset unevaluable is a **deliberate refusal awaiting a
human**: `checks/ms2130-uvc-aspect-quirk/default.nix:56-58` asserts
`kernel.version == "7.0.1"` and the pinned nixpkgs now carries
`linuxPackages_latest.kernel.version = "7.1.8"` (**witnessed**). Its message says
what it wants: somebody must review the MS2130 UVC patch against the selected
kernel. It is not this change's to answer and not a hardware-classification
matter.

So `nix flake check` on CriomOS is **red, on one deliberate human-review throw,
and on nothing else in the check set**. `reports/landings-criomos.md` §4.2
relayed the same throw as one of the two failures behind the fixture stop; it is
now the only one, and it is witnessed here rather than relayed. The unfree
`platform-tools` refusal §4.2 also named is handled by
`NIXPKGS_ALLOW_UNFREE=1`, as that report says.

Each individual check this change touches was built on Prometheus and exits 0
(§3). Nothing here made a green gate red: the gate was red before this work at
the four fixtures, and the fixtures are now green.

## 6. What landed, and what could not

### 6.1 Landed

CriomOS `main`, two commits, in this order:

- **`79cc994a9931`** — "Refuse local builds on hosts with no Nix builder role".
  The coordinator's addition: branch `f6db8d-remote-only-builds`
  (`dbf2daaf`, parent `acc3feab`) rebased onto `b84b99ba` and landed.
  `modules/nixos/nix/client.nix` gives a node with no builder role
  `max-jobs = 0`; an edge builder keeps its single slot; a dedicated builder
  keeps `node.maxJobs`; `trusted-users` and `builders-use-substitutes`
  unchanged. `checks/nix-role-policy` built on Prometheus at the rebased
  revision, exit 0 — the same derivation
  (`/nix/store/v1fky8clr2bsjjb2r1k39im232sb8pfq-nix-role-policy`) the
  `reports/remote-only-builds.md` thread built, so the rebase changed nothing
  about it. The rationale and the deploy consequences are in that report and
  are not repeated here.
- **`8fcfbfecb420`** — "Classify hardware in CriomOS, from the model Horizon
  projects". §§1-3 above.

**Witnessed**, against the real remote URL rather than the checkout's `origin`:

```
$ git ls-remote https://github.com/LiGoldragon/CriomOS.git main
8fcfbfecb420952ed686dbb635d57b51125d6462	refs/heads/main
$ git ls-remote ssh://git@github.com/LiGoldragon/CriomOS main
8fcfbfecb420952ed686dbb635d57b51125d6462	refs/heads/main
```

All work was done in a fresh clone under this thread's scratchpad, never in the
shared checkout under the Repository root, because a sibling f6db8d subflow held
lock 1227 on paths inside it.

### 6.2 Not landed, and why

**`flake.nix` — registering `checks.<system>.metal-model-classification`.**
Every check in CriomOS is listed explicitly in `flake.nix`'s `projectChecks`
(**witnessed**, `flake.nix:177-240`); blueprint's own discovery does not supply
the `inputs` argument these checks take. So the new check needs one line:

```nix
          metal-model-classification = pkgs.callPackage ./checks/metal-model-classification {
            inherit inputs;
          };
```

`/git/github.com/LiGoldragon/CriomOS/flake.nix` is inside **Orchestrate lock
1227** (`F6db8dCriomosLojixLanding`, flow f6db8d), still held when this report
was written. The check is committed, builds green on Prometheus, and is one
line away from being in the gate.

**`checks/lojix-ownership/default.nix:64` — `typeIs.largeAiRouter = false;`.**
The one remaining retired-field write in the CriomOS check set
(**witnessed**, grep of `checks/` and `modules/` for `typeIs`, `computerIs`,
`modelIsThinkpad`, `chipIsIntel`, `handleLidSwitch`, `chipGen` finds nothing
else). No module reads `typeIs`, so it is a dead fixture field rather than a
false green, and dropping it is a one-line deletion. That path is also inside
lock 1227.

Both are owed as one further commit the moment 1227 releases, and neither
changes any behaviour.

**This thread's inference, offered to the main flow rather than acted on**:
lock 1227 may be stale. Its reason is "Land `f6db8d-lojix-start` on CriomOS main
with the lojix 5.0.0 repin", and that landing is **already on main** — `cf3be61`
"Repin lojix to 5.0.0 b5cddd2e" and `b84b99ba` "Point the lojix checks at the
Nexus the module now starts" are both ancestors of `8fcfbfec` (**witnessed**,
`git log --oneline`). So the work the lock names is done and the lock was still
held after more than an hour of polling. This thread did not release another
flow's lock, and will not; the main flow is the one that can decide whether its
holder has gone.

## 7. Unknowns, stated as unknowns

- **Whether `ThinkPadX250` should be `isThinkpad = true`.** It was in neither
  `KnownModel` nor `ComputerIs`, yet `modelKernelModulesIndex` and
  `gpuUsesVaapi` in CriomOS key on it. This thread judged it a ThinkPad —
  it is one, and `thinkpad_acpi` charge thresholds work on it — but no psyche
  record and no prior report says so. If it is deliberately excluded, the row is
  one boolean to change.
- **Whether a bare-metal node should be allowed no model at all.** The new code
  throws. A `Live` ISO node built as bare metal with no model would now fail
  where it previously got all-false hardware policy. No such node exists in
  `goldragon/proposal.datom` (**witnessed** — every `Metal` node there names a
  model), but the estate is not the only consumer.
- **Why `goldragon/proposal.datom` still does not parse.** **Witnessed** again
  at the pinned producer: `horizon-cli --node ouranos` refuses it with
  `Structural(… problem: Multiple)` at byte 165, inside a guillemet string that
  itself contains braces. `reports/lojix-criomos.md` §3.3 attributes this to the
  protos guillemet-escape writer defect under another flow's lock 1105. Not
  re-diagnosed here; it is the reason the fixture definition is a small authored
  one rather than the real cluster proposal.
- **Whether `wantsPrinting` and `wantsHwVideoAccel` should become Horizon
  fields or CriomOS options.** A decision, not an implementation gap. §2.3.

## Sources

- **Witnessed**, this thread, 2026-09-12, in a fresh clone of CriomOS `main`
  under this thread's scratchpad:
  `modules/nixos/metal/default.nix` and the four metal checks read and edited;
  `nixfmt-rfc-style` run over every file touched;
  `nix eval --max-jobs 0 --impure` of each of the five checks' `drvPath`
  (before and after the fixture move, byte-identical);
  `nix build --max-jobs 0 -L` of `metal-model-classification`,
  `fixed-location-policy`, `laptop-keyboard-keyd`, `metal-firmware-policy` and
  `nix-role-policy`, all exit 0, the first, second and fourth built on
  `ssh-ng://nix-ssh@prometheus.goldragon.criome`;
  the same `metal-model-classification` evaluated against the pre-change module
  restored from `git show HEAD:` and seen failing at `modelIsThinkpad`;
  the unclassified-model and null-model throws forced directly;
  `nix flake check -L --max-jobs 0 --impure` with `NIXPKGS_ALLOW_UNFREE=1` and
  the four materialized inputs;
  `nix eval` of `linuxPackages{,_latest}.kernel.version` from the pinned
  nixpkgs;
  `jj git init --colocate`, `jj commit`, `jj bookmark set main`,
  `jj git push --bookmark main`;
  `git ls-remote` against both `https://github.com/LiGoldragon/CriomOS.git` and
  `ssh://git@github.com/LiGoldragon/CriomOS`.
- **Witnessed**, the producer: `nix build --max-jobs 0
  github:LiGoldragon/horizon-rs/40d04d2504fee619e9b2b2564b8a769a3a9d6049#default`
  (built on Prometheus) →
  `/nix/store/6xlkrqa8axf11xdc8x7rav5h569a8kps-horizon-0.10.1`;
  `horizon-cli --node atlas` run on the fixture definition and its output
  diffed against `CriomOS-home`'s `f6db8d-lojix-start`
  `fixtures/horizon-projection.json` — identical;
  `horizon-cli --node ouranos` run on `/git/github.com/LiGoldragon/goldragon/proposal.datom`
  — refused.
- **Witnessed**, `/git/github.com/LiGoldragon/horizon-rs`, read only, no build:
  `lib/src/model.rs`, `lib/src/projection/{views,names,node}.rs`,
  `lib/src/generated/horizon.rs`, `lib/tests/contract.rs` at `HEAD` and at the
  pinned `40d04d2`; `git show f1a5eca~1:` of `lib/src/view/node.rs`,
  `.jjconflict-base-0/lib/src/{name,species,node,proposal/node}.rs`;
  `git show 95593688:lib/src/magnitude.rs`; `git diff --stat 40d04d2 HEAD --
  lib/src/model.rs` (empty).
- **Witnessed**, `/git/github.com/LiGoldragon/lojix`, read only:
  `src/{ingress,bootstrap,inspected_text}.rs` at the local checkout (4.0.1) and
  at the pinned `b5cddd2e` (5.0.0); `tools/src/lojix-bootstrap.rs` and
  `tools/tests/bootstrap.rs` at the pinned revision;
  `nix build --max-jobs 0 github:LiGoldragon/lojix/b5cddd2e…#lojix-bootstrap`
  → `/nix/store/w0m0ixyvmvh93l16ywz5cjjz0lnby2gi-lojix-bootstrap`, and six
  `lojix-bootstrap` invocations (four refused, one `Failed` probe, one
  `Failed` complete-host run) with the generated journal inputs read afterwards.
- **Witnessed**, `/home/li/wt/github.com/LiGoldragon/CriomOS-home/f6db8d-lojix-start/fixtures/`,
  read only: `horizon-definition.datom`, `horizon-projection.json`,
  `horizon.nix`.
- **Relayed**, named: `flows/f6db8d/reports/design-decisions.md` §5 (the
  decision implemented here, including the three-way split and the
  implementation plan); `flows/f6db8d/reports/lojix-criomos.md` §§2.2, 3.1-3.4,
  5.1-5.3 (the `modelIsThinkpad` stop, the byte-identical materialization, the
  bootstrap's discarded stderr, the `horizon-definition.datom` naming);
  `flows/f6db8d/reports/landings-criomos.md` §§4.1-4.3 (the four fixtures making
  `checks` unevaluable, the unfree and MS2130 failures behind it, the stop
  unchanged at the landing revision);
  `flows/f6db8d/reports/remote-only-builds.md` (the branch landed in §6.1, its
  rationale, its `trusted-users` decision and its deploy consequences);
  `flows/33a4d4/log.md` lines 24-26, by way of `lojix-criomos.md`.
- **Orchestrate**: `Observe.Locks` before each acquisition and repeatedly while
  waiting on 1227. Acquired lock **1336**
  (`F6db8dMetalHardwareClassification`, f6db8d) on
  `modules/nixos/metal/default.nix`, the four metal checks,
  `checks/metal-model-classification/default.nix` and this report; and lock
  **1338** (`F6db8dRemoteOnlyBuildsLanding`, f6db8d) on
  `modules/nixos/nix/{client,builder}.nix` and
  `checks/nix-role-policy/default.nix`. Lock 1227
  (`F6db8dCriomosLojixLanding`, f6db8d, a sibling) was held throughout and its
  four paths were not touched — §6.2. Locks 1335 and a `TestC` probe were
  acquired and released while diagnosing the CLI defect below.
- **A defect in the `orchestrate` CLI, witnessed.** The `orchestrate` client
  refuses a guillemeted multi-word `LockReason`:
  `orchestrate 'Lock.{ TestC f6db8d [ /tmp/a ] «Recompute hardware
  classification …» }'` → `invalid request: Corporate(Locus { path: [1],
  extent: … }, Arity(4, 17))` — seventeen fields where four were expected, i.e.
  the reason's words were parsed as positional fields. The same request with a
  single-word reason is accepted. The `orchestrate` skill documents the
  guillemeted form as copyable and it does not work with the installed client;
  every lock in this report therefore carries a single-token reason.
