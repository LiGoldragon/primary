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
