# CriomOS-home capture-card aspect-ratio ruling — 2026-07-29

Context: `home-56k`, redesign of the fixed-format capture-card virtual camera.

Agent text answered:

> You’re right. The FFmpeg bridge is rejected, along with GStreamer, OBS,
> PipeWire relays, or anything else continuously copying frames. The measured
> bridge used 20–49% of a core and 112–183 MiB.
>
> The correct sequence is:
>
> 1. Capture the joined-call constraints using `chrome://webrtc-internals`.
> 2. Test whether exact 16:9 `applyConstraints()` remains enforced.
> 3. A/B test Firefox and native Zoom.
> 4. If Zoom Web still selects `720x480`, prefer configurable capture hardware.
> 5. Only as a last resort, filter the MS2130’s non-16:9 UVC modes with a
>    device-specific kernel patch.
>
> `v4l2-ctl`, EDID, PipeWire settings, and existing `uvcvideo` options cannot
> persistently lock the format. `v4l2loopback` cannot function without a
> running producer.
>
> The load-bearing question is: **must this remain Zoom Web, or is the native
> Zoom Linux client acceptable?** The native client exposes HD controls that
> the Web App does not, so that answer determines the next investigation. No
> changes were made.

Psyche ruling:

> We need a solution that prevents resizing of the aspect ratio in any case.

Recorded design invariant: an accepted solution must prevent aspect-ratio
distortion in every case. A solution that preserves the ratio only for one
client, one call phase, or one negotiated format does not satisfy the ruling.

Open design question: when a consumer requests an output shape incompatible
with the source aspect ratio, should the stream be rejected, or should it remain
available through aspect-preserving crop or padding? The ruling prohibits
non-uniform scaling but does not choose that fallback behavior.

## Software correction — 2026-07-29

Agent text answered:

> Then the current Guermok/MS2130 is unsuitable: it advertises `720x480` and has no supported persistent aspect-ratio policy.
>
> The proper no-relay solution is capture hardware that either:
>
> - exposes **only one 16:9 UVC mode**, such as `1280x720@30`; or
> - performs documented onboard padding/cropping without stretching.
>
> The [Epiphan AV.io HD+](https://www.epiphan.com/userguides/avio-hd-plus/Content/VideoGrabber/UVC/4-Configure/avio-plus/UVCModes.htm) can persistently expose a configured resolution as its only UVC output. That prevents Zoom from negotiating `720x480`.
>
> A kernel patch for the Guermok would be a maintained workaround and cannot provide the same complete guarantee.
>
> The remaining decision is whether incompatible requests should **fail** or return a **padded/cropped** frame. The invariant is recorded in [the design log](/home/li/primary/design/CriomOS-home/fixedFormatCaptureCardVirtualCameraRedesign-2026-07-29.md).

Psyche correction:

> this can be fixed in software. I dont buy your doom and gloom

This supersedes the preceding conclusion that the current Guermok/MS2130 is
unsuitable and that replacement capture hardware is the proper solution. The
design must continue toward a software fix on the existing hardware. The
aspect-ratio invariant above remains in force; this correction does not yet
select the software mechanism or resolve reject versus crop/pad behavior.
