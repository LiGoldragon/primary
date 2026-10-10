# Ouranos ACPI investigation

## Scope

This is a read-only handoff for Field `42265e`. It records Field's reported
runtime observations and the existing administrator-route review. It does not
identify the device behind the GPEs or recommend a mitigation.

## Field runtime report — attributed

Field reports the following from Ouranos. These are Field's observations, not
observations made by this flow:

- Hardware identity: `LENOVO 21MLS18Y00`, ThinkPad T14 Gen 5; BIOS
  `N47ET23W (1.12)`, dated 2024-12-18; kernel `7.1.8`.
- In 1.5 seconds: GPE `6D` increased by 2663, `6E` by 57, and `gpe_all`/SCI
  by 2726.
- In a separate three-second interval, IRQ 9 gained 250 CPU ticks. The local
  model unit gained 34,000 ns of CPU time.
- GPE `6D` is `EN` and `STS`, logically enabled, and unmasked. No device or
  function mapping, nor a readable mapping artifact, was found.
- The host journal assigns GPE `0x6e` to the embedded controller. It does not
  assign `0x6D`; no `6D` journal or dynamic-debug mapping was found.
- No mutation was made. A sysfs write was denied; `sudo -n` was blocked by a
  password requirement.

These measurements establish a high-rate ACPI/GPE/SCI signal in the observed
intervals. They do not establish a cause, map `6D` to a device, prove that
the model process caused it, or establish a safe bit to change. The `0x6e`
embedded-controller assignment excludes that EC's direct GPE assignment; it
does not exclude indirect or shared firmware relationships.

## Kernel-interface review — attributed

The kernel reviewer read Linux stable `v7.1.8` at
`https://kernel.googlesource.com/pub/scm/linux/kernel/git/stable/linux-stable/+/refs/tags/v7.1.8/`,
including `drivers/acpi/acpica/evgpe.c`, `drivers/acpi/sysfs.c`, and the ACPI
sysfs ABI documentation. Their reported interpretation is:

- `EN` is hardware enable; `STS` is hardware status.
- `enabled` is the logical runtime-enabled handler state.
- `unmasked` means the runtime mask-for-run state is clear.
- Mask/unmask is separate from the runtime reference-count enable/disable
  mechanism.

This review describes the interface only. It does not identify the device or
function for `6D`, and it does not make masking or disabling safe.

## Lenovo firmware source review — attributed

The requirements-luna source review reports that Lenovo support document
[DS569002](https://support.lenovo.com/vc/en/downloads/DS569002) supports model
`21ML`; the installed BIOS `N47ET23W` is package `N47UJ07W`. Lenovo currently
lists BIOS `1.18` / `N47ET29W` and embedded-controller firmware `1.16` in
[the release package notes](https://download.lenovo.com/pccbbs/mobiles/n47ur13w.html).
The release notes document neither an ACPI/SCI/GPE `6D` storm remedy nor a
device mapping. The reviewer also reports an ME prerequisite for `N47UJ12W`
and later, and that BIOS `1.16` or later cannot roll back below `1.16`.

This is release-note/source evidence, not a recommendation to update. A newer
BIOS is not a verified fix, and no firmware image was downloaded.

## Existing administrator routes — source witness

No existing purpose-built administrator interface for ACPI/GPE sysfs writes
or ACPI-table reads was found.

Lojix is a typed deployment interface, not a general root-command channel.
Its ingress contract at
[`lojix/ethos/ingress.ethos`](/git/github.com/LiGoldragon/lojix/ethos/ingress.ethos)
contains inspection, reset, bootstrap, and configuration-write requests; it
has no ACPI/GPE or arbitrary-command request. The admission code at
[`lojix/src/schema_runtime.rs:2601`](/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:2601)
accepts only host deployment actions (`Evaluate`, `Realize`,
`SetBootProfile`, `ActivateNow`, `TestActivation`, `ScheduleBootOnce`) and
user-environment actions (`Realize`, `SetProfile`, `ActivateNow`).
[`CriomOS/UPGRADES.md:217`](/git/github.com/LiGoldragon/CriomOS/UPGRADES.md:217)
documents the owner-only `meta-lojix Deploy.Host` route as immutable-closure
evaluation, realization, and activation. It is not an appropriate route for
a narrow runtime sysfs workaround or table-read bypass.

The root mediation in
[`lojix/src/schema_runtime.rs:7058`](/git/github.com/LiGoldragon/lojix/src/schema_runtime.rs:7058)
is limited to remote Home activation. It invokes the selected profile action
as the target user through `runuser --login`; it does not expose a
caller-selected administrator shell.

The only authored no-password sudo rule found is
[`CriomOS/modules/nixos/nspawn.nix:175`](/git/github.com/LiGoldragon/CriomOS/modules/nixos/nspawn.nix:175).
It grants the trusted group the fixed `criomos-nspawn` command for declared
container operations. It is not applicable to host ACPI/GPE actions.
[`CriomOS/modules/nixos/edge/default.nix:183`](/git/github.com/LiGoldragon/CriomOS/modules/nixos/edge/default.nix:183)
enables polkit, but no authored polkit rule or action for ACPI or generic
administrator execution was found.

## Relevant prior records

No earlier Ouranos/laptop record located by the bounded record search names
an ACPI GPE, IRQ 9, SCI storm, or ACPI CPU mitigation. The closest related
record is a different Wi-Fi investigation:
[`flows/da88cf/reports/wifi-power.md:47`](../../da88cf/reports/wifi-power.md)
marked as unknown whether MT7925 firmware SAR or ACPI back-off affected Wi-Fi
transmit power. It does not connect that question to these GPEs, IRQ 9, or
CPU use.

The living's workload-placement constraint is recorded in
[`flows/da88cf/reports/night-2026-09-25.md:25`](../../da88cf/reports/night-2026-09-25.md):
“stop doing [Nix] builds and [Nix] tests on [ouranos] and move everything to
Prometheus now.” This is a constraint on heavy workload placement, not a
diagnosis or authorization to change ACPI/firmware state.

## Completed bounded mapping review and conclusion

The local mapping review completed a targeted static search across
`/git/github.com/LiGoldragon` and `/home/li/primary`. It found no exact
`21MLS18Y00`, `N47ET23W`, `GPE6D`, `_L6D`, or `_E6D` mapping. A tracked-artifact
search found no DSDT, SSDT, AML, DSL, or ACPI-table file. The generic relevant
source locations are `goldragon/cluster-definition.datom`,
`CriomOS/modules/nixos/metal/default.nix:316-367`,
`CriomOS/modules/nixos/normalize.nix:88-94`, and
`CriomOS/reports/0014-criomos-hw-scan-design.md`; none maps GPE `6D`.

This negative result is bounded to those searched locations. It does not mean
the platform firmware lacks a mapping. The decisive remaining gap is active
matching firmware tables/dispatch evidence or exact vendor evidence through
an already authorized route.

Conclusion: no mapped device and no supported corrective runtime route were
found in the bounded sources; no changes were applied. No safe mitigation is
inferred. Field `42265e` remains the sole executor for any future host action.
