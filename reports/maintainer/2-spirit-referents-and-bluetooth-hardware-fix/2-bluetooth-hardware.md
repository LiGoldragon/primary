# ouranos Bluetooth firmware persistence

## Summary

The live Bluetooth failure was an Intel AX211 firmware-loading failure on ouranos. The immediate runtime repair kept Bluetooth working by pointing the kernel firmware loader at the booted generation's firmware and reloading `btusb`. The persistent fix landed in CriomOS by tying the required firmware to the ThinkPad T14 Gen 5 Intel model predicate.

## Hardware fact

Observed ouranos hardware:

- Bluetooth USB device: Intel AX211 Bluetooth, USB ID `8087:0033`.
- WiFi/CNVi context: Meteor Lake PCH CNVi WiFi, PCI ID `8086:7e40`.
- DMI product/version: ThinkPad T14 Gen 5, product version `21MLS18Y00`.
- CriomOS model predicate used by the fix: `ThinkPadT14Gen5Intel`.

The chosen predicate is the narrow model predicate already present in the CriomOS metal firmware index. It is more stable than a one-off host name and less speculative than a broad chip-generation rule.

## Failure chain

- The live failing generation was an `OsOnly` shape: no Home Manager user units and no broad firmware set.
- Its firmware activation path pointed at a small closure containing wireless regulatory data, not the Intel Bluetooth firmware files.
- Kernel Bluetooth logs showed reset/firmware loading needed Intel `ibt-0180-0041` firmware data.
- The booted generation's firmware set did contain the needed Intel firmware, so setting the runtime firmware path to the booted generation and reloading `btusb` restored `hci0`.

## Persistent code change

Commit:

- `9d5f9e031db4` — `CriomOS: keep T14 Gen5 Intel firmware in lean deployments`

File:

- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix`

Change:

- Added `ThinkPadT14Gen5Intel` to `modelFirmwareIndex` with `linux-firmware` and `sof-firmware`.
- This keeps the Intel AX211 Bluetooth firmware in model-specific firmware even when a lean/OsOnly deployment does not enable all firmware.

## Verification

Remote-source evaluation/build:

- Built the `hardware.firmware` derivation from `github:LiGoldragon/CriomOS/main` for an OsOnly-style synthetic node whose model is `ThinkPadT14Gen5Intel`.
- Verified the resulting firmware out-link contains both Intel Bluetooth files:
  - `intel/ibt-0180-0041.sfi.zst`
  - `intel/ibt-0180-0041.ddc.zst`

Live runtime check after the temporary repair:

- Kernel firmware loader path remains `/run/booted-system/firmware`.
- `bluetooth.service` is active.
- `hci0` is `UP RUNNING PSCAN` with the same controller address observed after repair.

## What is still not done

- The system generation was not switched in this pass. The bootloader default had been the bad generation before this work; this report does not claim that the bootloader default has changed.
- The current runtime workaround remains tied to the booted generation until a safe system deploy installs a fixed generation.
- A system-designer lane currently owns broader CriomOS work, so this maintainer pass stopped at a pushed model-firmware fix plus reproducible build/eval proof rather than doing an overlapping system activation.

## Residual risks

- `ThinkPadT14Gen5Intel` is a model-level predicate. If another T14 Gen 5 Intel variant ships a different Bluetooth device, the broad `linux-firmware` inclusion is still safe but less minimal than a future USB-ID-specific hardware fact.
- OsOnly as a boot default on a desktop remains operationally risky when it drops Home Manager units and broad firmware. The model fix addresses this Bluetooth device, not the larger policy question of whether lean desktop system generations should become boot defaults.
