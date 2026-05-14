# Chroma Solar Theme Schedule

## Context

The reported behavior was that Chroma's dark theme switch felt too late.
The important question was whether the schedule was hardwired inside the
engine, whether it actually used local solar time, and how to make the
light/dark transition policy configurable without making users pick fixed
clock times.

## Findings

Chroma already had a schedule model and it was not purely hardwired, but
the shipped CriomOS-home default was effectively:

- light theme at civil dawn
- dark theme at civil dusk

That explains the late evening switch: civil dusk is after sunset, so the
dark theme was waiting until the sky was already well into twilight.

The engine does use geolocation. The daemon asks GeoClue for latitude and
longitude, keeps a last-known location, and the scheduler projects solar
events for that location. The old theme schedule only exposed civil dawn
and civil dusk triggers, though, so it could not express the more natural
"dark a bit before sunset" policy directly.

## Implemented

Chroma now supports both civil twilight and sunrise/sunset triggers:

- `Sunrise`
- `Sunset`
- `CivilDawn`
- `CivilDusk`

Solar trigger offsets can still be exact signed minutes, and now can also
use readable timing labels:

- `ExtremelyEarly` = 120 minutes before
- `VeryEarly` = 60 minutes before
- `Early` = 30 minutes before
- `OnTime` = no offset
- `Late` = 30 minutes after
- `VeryLate` = 60 minutes after
- `ExtremelyLate` = 120 minutes after

CriomOS-home now exposes this as `criomosHome.visualTheme` options:

- `lightThemeSwitchTiming`
- `darkThemeSwitchTiming`

The current defaults are:

- light: `Sunrise OnTime`
- dark: `Sunset Early`

That means dark theme now starts 30 minutes before local sunset, while
light theme starts at local sunrise.

## Verification

Chroma tests now cover:

- parsing readable solar offsets
- mapping readable labels to minute offsets
- `Sunrise` and `Sunset` requiring geolocation
- Sarande, Albania schedule projection from latitude/longitude rather
  than fixed clock times

Local verification:

- Chroma: `cargo test` passed
- Chroma: `nix flake check` passed
- CriomOS-home: `nix flake check` passed
- CriomOS-home: targeted Nix formatting passed
- CriomOS: lock update was verified; direct `nix flake check` still stops
  at the expected stub boundary when no projected lojix inputs are
  provided

Runtime verification on `ouranos`:

- Home activation completed through lojix `HomeOnly ... Activate`
- `chroma-daemon` restarted successfully
- live config contains `(Waypoint (Sunrise OnTime) Light)`
- live config contains `(Waypoint (Sunset Early) Dark)`
- `chroma '(GetState)'` returned a live state from the restarted daemon

The old daemon briefly logged `unknown trigger Sunrise` when Home Manager
wrote the new config before systemd restarted the service. The restarted
daemon is the new build and accepts the new config.

## Commits

- `chroma`: `66ed03bf44efdb97e4576f2e3191084e0059fbfe`
  - `chroma: add solar schedule timing labels`
- `CriomOS-home`: `ed77c7ec03e502cd3d2bd7a81c066803677a8677`
  - `home: configure chroma solar theme timing`
- `CriomOS`: `ac4a82e5`
  - `criomos: bump home for chroma solar timing`

## Remaining Work

The exact default policy is now easy to change in CriomOS-home. If the
current default still feels too late, set `darkThemeSwitchTiming` to
`VeryEarly`. If light comes too early, set `lightThemeSwitchTiming` to
`Late` or `VeryLate`.

Warmth scheduling still uses civil dawn/dusk. That is separate from the
theme schedule and can be tuned the same way in a later pass if the
screen temperature transition feels mismatched.
