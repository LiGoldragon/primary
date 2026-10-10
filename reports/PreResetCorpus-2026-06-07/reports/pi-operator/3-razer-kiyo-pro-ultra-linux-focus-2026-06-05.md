# Razer Kiyo Pro Ultra Linux autofocus situation report

Date: 2026-06-05
Role: pi-operator
Subject: Razer 4K Ultra HD USB camera focus trouble on Linux

## Bottom line

The camera is almost certainly the Razer Kiyo Pro Ultra, model `RZ19-04420`. The focus complaint matches a known pattern: the hardware can make an excellent image, but autofocus is visibly unstable for some users, especially when moving, when showing objects/products, or when the camera is in the wrong focus mode. The most reliable fix on Linux is not firmware-first; it is to disable autofocus and set manual focus, or use a Linux camera-control app to choose the Kiyo Pro focus mode if the control is exposed.

I did not find an official Linux firmware updater. Razer’s official firmware package is a PC updater for `RZ19-04420`, firmware `v1.0.6.1_r1`, dated 2023-04-24, with release notes saying only “Added 2 new watermark locations: top center and bottom center.” That release note does not advertise an autofocus fix. Razer’s support page says to launch the downloaded firmware updater, plug the Kiyo Pro Ultra into the PC, click update, wait, then unplug/reconnect. It does not give Linux instructions.

OpenRazer is also not the answer for this webcam. OpenRazer’s device page says webcams with no lighting features are not supported and explicitly points users to `cameractrls` for HDR and related webcam functionality.

## Local machine findings

The Razer camera was not attached during the local scan. Linux currently sees:

| Device class | Local result |
|---|---|
| USB Razer/Kiyo camera | Not present during scan. |
| Physical camera | Integrated camera only. |
| Virtual cameras | Two v4l2loopback devices. |
| Installed camera tools | `v4l2-ctl` and `qv4l2` are installed. |
| Not installed, available in nixpkgs | `cameractrls` 0.6.10, `guvcview` 2.2.2, `obs-studio`. |

Because the Razer camera was not attached, I could not verify the exact UVC control names on this machine. Those names vary by camera/driver: common focus controls include `focus_auto`, `focus_automatic_continuous`, and `focus_absolute`.

## What official sources say

Razer’s Kiyo Pro Ultra support page lists:

- Auto Focus: yes.
- Focus range: 10 cm to infinity.
- Optimized focus range: 50 cm to 200 cm.
- USB 3.0 connectivity.
- 4K 30 FPS requires the original cable, direct computer connection, and no hub.
- Manual focus procedure: open camera controls in OBS/XSplit, disable the “auto” focus checkbox, and adjust the focus slider.
- Frame-rate mismatch tip: if the output frame rate does not match Synapse, turn HDR off because HDR increases data/processing load.

The official firmware page lists only `v1.0.6.1_r1` from 2023-04-24 and gives a Windows-style updater workflow. The notes only mention watermark locations, not autofocus.

## What reviewers and users are saying

There is a split consensus:

- Positive reviewers praise image quality, large sensor, low-light performance, and shallow depth-of-field.
- Negative reports consistently mention autofocus behavior as the weak point.
- The Ultra’s face-focused autofocus is better than the older Kiyo Pro, but still not reliable for all scenes.
- “Standard” autofocus is reported as poor at tracking; face mode is better for a human face.
- Product/object demonstrations are a weak case for both Kiyo Pro and Kiyo Pro Ultra autofocus.
- Users in OBS/Synapse report losing focus when moving, even after trying settings.
- WIRED specifically called out “weird autofocus behavior” and noted the autofocus dipping in/out visibly, while also noting Synapse is Windows-only.

The practical community advice lines up with Razer’s official manual-focus advice: if the scene is mostly static, turn autofocus off and lock focus manually. If you need autofocus, use face tracking rather than standard mode when available, and try the slower/passive drive mode to reduce hunting.

## Linux control options

### Already installed: `qv4l2` and `v4l2-ctl`

These are the most immediate tools.

When the camera is attached, run:

```sh
v4l2-ctl --list-devices
v4l2-ctl -d /dev/videoN --list-ctrls
```

Look for focus controls. If present, a manual-focus flow is usually:

```sh
v4l2-ctl -d /dev/videoN --set-ctrl=focus_auto=0
v4l2-ctl -d /dev/videoN --set-ctrl=focus_absolute=VALUE
```

or, on devices that expose continuous-focus naming:

```sh
v4l2-ctl -d /dev/videoN --set-ctrl=focus_automatic_continuous=0
v4l2-ctl -d /dev/videoN --set-ctrl=focus_absolute=VALUE
```

Do not guess `VALUE`; first read min/max/step from `--list-ctrls`. There is a Razer Insider Linux report where setting focus controls on a Kiyo caused trouble after changing focus values, so the safe path is to inspect the control range first, move in small increments, and be ready to unplug/replug.

`qv4l2` gives a GUI for the same V4L2 controls. It is useful for discovering the exact focus slider behavior before scripting anything.

### Best Linux GUI candidate: `cameractrls`

`cameractrls` is the strongest Linux recommendation. Its README says it is a standalone Python CLI/GTK GUI/viewer for Linux camera controls. It can set V4L2 controls and has a Kiyo Pro extension for HDR, HDR mode, field-of-view, autofocus mode, and save/restore behavior. The old `kiyoproctrls` project was merged into `cameractrls`.

OpenRazer also points webcam users toward `cameractrls` for HDR and related functionality. On this machine, `cameractrls` is not installed, but nixpkgs has version 0.6.10.

Recommended CriomOS direction: package/install `cameractrls` through Nix/Home Manager rather than using a random clone or mutable Flatpak if we want this as part of the normal profile.

### Other options

`guvcview` is also available in nixpkgs and is a traditional Linux webcam-control GUI. It may be useful, but it is less compelling than `cameractrls` for this specific Razer camera because `cameractrls` has Kiyo Pro-specific extension controls.

OBS can expose camera properties, but OBS is not currently installed locally. If it is installed later, it may be enough to disable autofocus and set the slider from the video-device properties, matching Razer’s official instructions.

## Firmware update assessment

I would not make firmware the first move, because:

1. The official latest Kiyo Pro Ultra firmware page does not advertise an autofocus fix.
2. The updater path is Windows-style and not documented for Linux.
3. Firmware updates over Wine are risky for USB devices because failed USB firmware flashing can brick hardware.
4. A Windows VM with USB passthrough may work in principle, but firmware update passthrough is still a risk. If firmware is needed, the safer path is a real Windows machine or a carefully configured VM with direct USB passthrough, direct USB port, stable power, no hub, and no other camera apps running.

If the camera is already on `v1.0.6.1_r1`, there is likely nothing useful to update. If it is older and focus remains bad after Linux control tuning, updating from Windows may be worth considering, but it should be treated as hardware-maintenance risk, not a routine Linux command.

## Recommended next actions

1. Plug the Razer camera directly into a USB 3 port with its original cable, not through a hub.
2. Run `v4l2-ctl --list-devices` and identify the Razer `/dev/videoN` node.
3. Run `v4l2-ctl -d /dev/videoN --list-ctrls` and capture only the focus/HDR/FOV control names and ranges.
4. Try `qv4l2` first: disable autofocus and find a stable manual focus value for the normal desk distance.
5. Install/package `cameractrls` through Nix/Home Manager and test whether it exposes Kiyo Pro AF mode, FOV, HDR, and save controls for this Ultra model.
6. For normal calls/streaming, prefer manual focus if your position is fixed. If movement matters, try face autofocus plus passive/slower drive mode if available.
7. Avoid HDR while troubleshooting focus/framerate; keep good front lighting and reduce high-contrast background distractions.
8. Only pursue firmware after confirming current firmware version/control behavior, because official latest firmware notes do not point to a focus fix and Linux-native firmware update support was not found.

## Sources

- Razer Kiyo Pro Ultra support and FAQ, `RZ19-04420`: https://mysupport.razer.com/app/answers/detail/a_id/6430/
- Razer Kiyo Pro Ultra firmware updater, `RZ19-04420`: https://mysupport.razer.com/app/answers/detail/a_id/9777
- OpenRazer device/support page: https://openrazer.github.io/#devices
- `cameractrls` project: https://github.com/soyersoyer/cameractrls
- legacy `kiyoproctrls` project: https://github.com/soyersoyer/kiyoproctrls
- Stream Tech Reviews, Kiyo Pro vs Kiyo Pro Ultra: https://www.streamtechreviews.com/blog/kiyo-pro-vs-ultra
- WIRED Kiyo Pro Ultra review: https://www.wired.com/review/razer-kiyo-pro-ultra/
- Razer Insider user report, Kiyo Pro Ultra losing focus: https://insider.razer.com/razer-support-45/razer-kiyo-pro-ultra-hd-losing-focus-85452
