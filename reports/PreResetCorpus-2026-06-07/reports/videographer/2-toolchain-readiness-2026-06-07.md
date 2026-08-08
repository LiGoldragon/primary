# Video toolchain — what I need

What I need available to do video work (edit, encode, caption,
capture), and how each has to be set up. Providing them is the
operator / system-operator's job — this is the "what," not the "how."

## Need

- **ffmpeg + ffprobe** — the core: trim, crop, scale, concat, encode,
  mux, and burn captions into the picture. Must be built **with libass**
  (so it can render captions) and **with VAAPI** (hardware encode — this
  box has no ML GPU but has an iGPU at `/dev/dri`, so encoding shouldn't
  hammer the CPU).
- **whisperx** — turns speech into **word-level timestamps**, which is
  what makes captions land on the right word. Runs **CPU-only** here, so
  its speech + word-alignment **models need to be downloaded ahead of
  time** (a few GB, cached) so I'm not stalled mid-task.
- **Caption fonts** — a couple of bold display fonts (Montserrat, Inter,
  or similar) plus a **color emoji font** (Noto Color Emoji), installed
  so the caption renderer can use them by name.
- **A Wayland screen recorder** (wf-recorder or wl-screenrec) — for
  screen capture; this is a Wayland session.
- **Text-to-speech** — Piper (natural voice) and/or espeak-ng (quick,
  robotic) — for voiceovers and for generating test clips.

## Already here (just keep them available)

yt-dlp (download source clips), mpv (playback checks), and ImageMagick
(thumbnails/frames). MediaInfo, MKVToolNix, and PySceneDetect would also
help (inspect containers, detect scene cuts) but are secondary.

## Not a tool to install — that part is mine

Captions get styled by a small script I write myself (it turns
whisperx's word timestamps into the caption file ffmpeg burns in). The
fancy browser-based caption tool I looked at earlier doesn't run on this
machine, so that's why captions go through ffmpeg + whisperx instead.
