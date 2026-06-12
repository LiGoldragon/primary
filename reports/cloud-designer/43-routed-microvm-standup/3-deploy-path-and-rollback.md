# 43 · Deploy path + rollback — how a CriomOS config safely reaches a live host, and how to undo it

cloud-designer, READ-ONLY reconnaissance, 2026-06-12. Dimension 3 of the
routed-microVM standup (frame: `0-frame-and-method.md`). Every claim is
grounded in a file read or a Spirit lookup; no live host was mutated.

## Bottom line

Stand the `vm-testing` microVM up with **production `lojix-cli`**, action
**`BootOnce`**, run **on the target node itself**. The new lojix daemon
**cannot** do this yet — it rejects every activating action by contract. Roll
back by **rebooting** (BootOnce self-heals to the prior generation on reboot 2;
or pick the prior entry in the systemd-boot menu).

## The production tool is `lojix-cli` (flagless NOTA), not the daemon

The deploy *orchestrator* is `lojix-cli`: a flagless, NOTA-only one-shot CLI.
The request **is** one positional NOTA record, tag-dispatched — `FullOs` /
`OsOnly` / `HomeOnly` / `CheckHostKeyMaterial`
(`lojix-cli/src/request.rs:16-89`). For a microVM-host system deploy the record
is `FullOs` (system + home) or `OsOnly` (system only):

```
(FullOs <cluster> <node> <source.nota> <criomos-flake-ref> <action> <builder?> <substituters?>)
```

`<action>` is a `SystemAction` = `Eval | Build | Boot | Switch | Test |
BootOnce` (`lojix-cli/src/build.rs:9-23`). These enums gate which pipeline
tails run; only `Boot | Switch | Test | BootOnce` copy + activate
(`build.rs:30-36`, `deploy.rs:165-180`).

Note: `lojix-cli/docs/basic-usage.md` documents an older `--flag` /
`--action boot` shape; that is stale. The live request grammar is the positional
NOTA record above (`request.rs`), confirmed by report 39. The doc's *concepts*
(pin the CriomOS rev, prefer `boot`/`BootOnce` on first touch, run on the
target, recover via the systemd-boot menu) remain correct.

### Run on the target node

Addressing derives from `horizon.node.criome_domain_name`; there is **no
`--target` flag** (network-neutrality rule, `deploy.rs:102-106`,
`host.rs`). Cross-node addressing is the known gap (`docs/basic-usage.md:99-105`
— ssh host historically `localhost`). So: **invoke `lojix-cli` while logged into
the host that will run the microVM** (the chosen target from dimension 2), not
from a remote dispatcher.

## The deploy pipeline (what actually mutates the host)

`deploy()` runs a fixed sequential pipeline (`deploy.rs:82-208`): load proposal
→ project horizon → materialize the four override inputs → `nix build` the
toplevel → **copy → activate**, the last two gated on `action.activates()`
(`deploy.rs:165-180`). Only the copy+activate tail touches the live host:

- **Copy** (`copy.rs:26-68`): `nix copy --substitute-on-destination --to
  ssh-ng://<target>`. The target pulls *signed* paths from the cluster cache
  (`require-sigs`); copy is a no-op when builder == target. This is pure store
  population — it changes **no** running state, breaks **no** networking.
- **Activate** (`activate.rs`): this is the only step that can change boot
  config or restart services. Its safety depends entirely on the `SystemAction`.

## Why `BootOnce` is the safe action for a router-class host

`Switch` is forbidden here. `Boot` is acceptable; `BootOnce` is strictly safer
and is the right default for this standup.

- **`Switch`** (`activate.rs:39-69`): `nix-env --set` + `switch-to-configuration
  switch` — activates the new generation **live**, restarting changed services.
  On a router that **restarts `hostapd` + `kea`/dnsmasq + nftables and drops the
  connection you reach the host through** — exactly what broke the gemma deploy
  (Spirit `kx32`, Constraint High). Forbidden on Prometheus / any router node.
- **`Boot`** (`activate.rs:39-69` + EFI reconcile `requires_efi_reconcile` →
  `reconcile_efi`, `activate.rs:160-230`): `nix-env --set` +
  `switch-to-configuration boot` — writes the bootloader entry and **moves the
  persistent default to the new generation**, but does *not* activate live. Safe
  for live networking, but if the new generation is broken you boot **into** it
  by default; recovery needs the systemd-boot menu (console/out-of-band access).
- **`BootOnce`** (`activate.rs:75-147`, semantics `build.rs:16-22`): the
  headless-safe path. It installs the new generation's bootloader entry but
  **keeps the persistent default pointing at the currently-running generation**
  and stages the new one as a systemd-boot **one-shot**. The script reads `OLD`
  from `bootctl status`'s *Current Entry* (the running generation, the EFI
  `LoaderEntrySelected` var — not the stale `loader.conf` default), sets the new
  closure, derives `NEW` from `/nix/var/nix/profiles/system`, then
  `bootctl set-default $OLD` + `bootctl set-oneshot $NEW` (`activate.rs:92-126`).
  Net effect: **reboot 1 lands NEW; reboot 2+ auto-returns to OLD**. A
  networking break in the new generation **self-heals on the next reboot** with
  zero operator action — the property that makes it safe for a router with **no
  out-of-band/console access** (Spirit `xv9v`, Constraint High: "Prometheus
  deploys should use the safe BootOnce path rather than Switch").

### Disconnect-survival (also a hard constraint)

`BootOnce` dispatches the activation as a **transient `systemd-run --unit=…
--collect --wait --service-type=oneshot`** unit owned by PID 1
(`activate.rs:128-147`). An ssh drop does **not** kill it — the unit runs to
completion on the target; the deployer re-attaches with `ssh <target> journalctl
-u <unit>.service` (`activate.rs:232-255`). This satisfies Spirit `1lex`
(Constraint High: disruptive Prometheus ops must run as durable transient units
so they survive an SSH drop) and the `se72` decision's "survive SSH disconnect"
clause. (`Boot`/`Switch` run synchronously over a single ssh and do **not**
have this protection — another reason to prefer `BootOnce`.)

## Rollback procedure

1. **BootOnce, new gen is broken (incl. networking):** just **reboot the host**.
   The one-shot is consumed on reboot 1; reboot 2 falls back to the persistent
   default = OLD = the generation that was running pre-deploy. No menu
   interaction, no console needed — this is the self-heal. (If reboot 1 lands a
   *working* gen you want to keep, promote it with a subsequent `Boot`/`Switch`
   from a safe context.)
2. **Boot, new gen is broken:** reboot, and at the **systemd-boot menu** select
   the prior `nixos-generation-NN.conf`; the previous generation is always
   retained (`docs/basic-usage.md:86-97`). Requires console/menu access.
3. **There is no `nix-env --rollback` subsystem.** "Rollback" *is* the BootOnce
   one-shot design + EFI reconcile; GC-rooting is implicit (setting the system
   profile makes the closure a profile generation = a GC root) — report 39.
4. **Always pin `--criomos github:LiGoldragon/CriomOS/<rev>`** (here: the
   `next` branch rev carrying `vm-testing`) so nix's eval cache fetches fresh
   code rather than a stale prior eval (`docs/basic-usage.md:55-65`).

## Tool choice: production `lojix-cli`, NOT the lojix daemon

The lojix daemon (report 38, `lojix/src/schema_runtime.rs`) reimplements only
the *front* of the pipeline. It **cannot stand this up**:

- Its reject-guard `unsupported_deploy_reason` only accepts `Eval | Build` for
  System and `Build` for Home; **every activating action is rejected**
  (`lojix/src/schema_runtime.rs:530-550`): "Activating actions remain rejected
  because copy/activate is not yet target-safe; accepting them would write false
  live-set state." There is no `BootOnce` activation path at all.
- Its `activate_system` stub is broken — `ssh <node> nix-env … --set
  "$CLOSURE"` with **`$CLOSURE` unset**, **no `switch-to-configuration`**, **no
  systemd-run transient unit**, **no EFI reconcile**, and a **bare node name**
  as the ssh host (`lojix/src/schema_runtime.rs:1863-1873`). It would neither
  activate nor protect a router.

So the microVM standup deploy runs through **production `lojix-cli`**. The
daemon proving it can do the same full-OS deploy is the *downstream* cutover
validation (report 42 S5 / `se72`), gated on the daemon's copy/activate +
BootOnce being made target-safe — it is not a prerequisite this standup can use.

## Concrete safe invocation (illustrative — confirm node/source with synthesis)

Run **on the chosen target host** (per dimension 2), as the user (not sudo;
lojix-cli escalates internally):

```bash
rev=<CriomOS next rev carrying vm-testing>   # pin it
lojix-cli "(FullOs goldragon <target-node> <source.nota> github:LiGoldragon/CriomOS/$rev BootOnce None None)"
# reboot to land NEW; if networking breaks, reboot again → auto-returns to OLD
```

`source.nota` is the cluster proposal (`goldragon/datom.nota`-style). For a
system-only first touch use `OsOnly … BootOnce`. Validate the build first with
`(OsOnly … Build None None)` (no activation, no host mutation) before any
`BootOnce`.
