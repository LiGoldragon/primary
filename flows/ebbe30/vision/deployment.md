## Next, stable, last: a test deployment branch everywhere

Context: 2026-10-09; how a version is tested and how the upgrade stays smooth.

> Let's use a test deployment if we want to test a certain version. We could have a test deployment branch everywhere, and that's how we can test-deploy something on the next branch. Let's just call it that, right? The next branch is that, so the next-suffixed package or server is from the next branch. That way, you can have a smooth upgrade, and we can have the last, which is a fallback in case somehow current becomes unstable or something, or it might actually make the atomic move more smooth.
>
> When we upgrade the NixOS layer, we're going to change these: next, stable, and last, but not necessarily, probably not all at a time. Eventually, we're going to have [Lojix] take care of the operation.

-- psyche, STT, 2026-10-09. Transcription corrected: "logics" → "Lojix".
