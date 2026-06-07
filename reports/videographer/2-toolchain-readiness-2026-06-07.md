# Videographer toolchain — readiness spec

What the video work needs, how it must be configured on this machine,
and a concrete artifact + checklist so another agent (operator or
system-operator) can get the toolchain ready for the videographer lane.

All versions below were read from the live `nixpkgs#` registry on
2026-06-07, so the attribute names are accurate to act on directly.

## TL;DR for the readying agent

1. Place the devshell flake from the "Configuration approach" section
   (location is an open decision — see the last section).
2. `nix develop` it and run the verification checklist at the bottom.
3. Pre-warm the Whisper/alignment model cache once (so the videographer
   isn't blocked on a first-run download mid-task).
4. Report back which checklist items pass. Nothing is installed
   statefully — the flake is entered ephemerally and GC-clears.

That's the whole job. The rest of this report is the *why* and the
*detail* behind those four steps.

## Hard environment constraints (do not fight these)

These were established the hard way in the captions research and are
now load-bearing for how the toolchain must be shaped:

- **No stateful installs** (Spirit `j4r1`). No `pip install`, no
  persistent virtualenvs, no downloaded toolchains in `$HOME`.
  Everything is declarative/ephemeral via nix.
- **`nix-ld` is disabled** — the `/lib64` loader is the always-fail
  stub, and it ignores a correctly-set `NIX_LD`. Generic-Linux binary
  wheels and downloaded binaries (pip `torch`, Playwright's bundled
  Chromium/node, `skia-python`) **cannot execute**. Tools must come
  from nixpkgs (built for NixOS), not from pip wheels.
- **`steam-run` is unfree-blocked** — the usual FHS escape hatch
  (`steam-unwrapped`, `unfreeRedistributable`) won't evaluate, so it is
  not an option for running generic binaries.
- **CPU-only for ML** — no `nvidia-smi`, no CUDA. Whisper transcription
  runs on CPU: pick `base`/`small`/`medium` models and accept slower
  runs; do not assume a GPU.
- **Wayland session** (`XDG_SESSION_TYPE=wayland`, `wayland-1`, with
  XWayland on `:0`) — screen capture uses Wayland-native tools.
- **VAAPI present** — `/dev/dri/{card0,renderD128}` exist, so ffmpeg
  hardware-accelerated encode/decode (`h264_vaapi`, `hevc_vaapi`) is
  available in principle. This matters: it offloads encoding from the
  CPU. May need `LIBVA_DRIVER_NAME` and a VAAPI driver wired in the
  shell; verify and otherwise fall back to CPU `libx264`.

## Already on the box (baseline — no action needed)

In the nix profile today: `ffmpeg` + `ffprobe` (8.0.1, built with
`--enable-libass`, so the `ass` and `subtitles` filters work), `mpv`,
`yt-dlp`, `imagemagick` (`magick`/`convert`), and
`google-chrome-stable` (147). The devshell below pins these explicitly
anyway so the environment is reproducible rather than relying on the
ambient profile.

## Configuration approach — one ephemeral devshell flake

The NixOS-native way to make tools "ready" without stateful installs is
a flake `devShell`: one declarative entry point that puts the whole
toolchain on `PATH` for the duration of a `nix develop`, reproducible
and garbage-collectable. This is the recommended deliverable.

```nix
{
  description = "Videographer toolchain — ephemeral video-work devshell";

  # Pin to the same nixpkgs the system uses; nixos-26.05 shown as a
  # concrete default (the versions in this report came from it).
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      captionFonts = with pkgs; [
        montserrat            # bold, legible display font for captions
        inter
        dejavu_fonts
        noto-fonts-color-emoji # color emoji in captions
      ];
    in {
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          # --- edit / encode / mux (VAAPI hw-accel via /dev/dri) ---
          ffmpeg-full          # libass, vaapi, full codec set
          mediainfo
          mkvtoolnix
          # --- frames / thumbnails / image ops ---
          imagemagick
          # --- transcription: word-level timestamps for captions (CPU) ---
          whisperx
          # --- scene detection + caption-build scripting ---
          (python312.withPackages (ps: [ ps.scenedetect ]))
          # --- text-to-speech (voiceover / generated test clips) ---
          piper-tts
          espeak-ng
          # --- source download + playback/verify ---
          yt-dlp
          mpv
          # --- Wayland screen capture ---
          wf-recorder
          wl-screenrec
        ] ++ captionFonts;

        shellHook = ''
          # Make caption fonts discoverable to libass via fontconfig.
          export FONTCONFIG_FILE=${pkgs.makeFontsConf { fontDirectories = captionFonts; }}
          # Keep model weights in a project-local cache (data, not a
          # stateful package install); override by exporting HF_HOME first.
          export HF_HOME="''${HF_HOME:-$PWD/.cache/huggingface}"
          export XDG_CACHE_HOME="''${XDG_CACHE_HOME:-$PWD/.cache}"
          echo "videographer devshell ready: ffmpeg $(ffmpeg -version | head -1 | cut -d' ' -f3)"
        '';
      };
    };
}
```

## Tool inventory (verified)

| Capability | Tool (nixpkgs attr) | Version | Why it's needed |
|---|---|---|---|
| Edit / encode / mux / burn-in subtitles | `ffmpeg-full` | 8.0.1 | The workhorse: trim, concat, crop, scale, filtergraph, encode, audio, and `ass`/`subtitles` burn-in (libass). |
| Container inspect | `mediainfo` | 26.01 | Quick stream/codec/bitrate inspection beyond `ffprobe`. |
| Container mux/split | `mkvtoolnix` | 98.0 | Clean MKV muxing, track surgery, chapters. |
| Frames / thumbnails / images | `imagemagick` | 7.1.2-19 | Thumbnail composition, frame post-processing. |
| Transcription (word timestamps) | `whisperx` | 3.8.5 | Word-level timestamps via wav2vec2 alignment — the basis of synced captions. Nix-built (torch works); avoids the pip-torch wall. |
| Scene detection / scripting | `python312Packages.scenedetect` | 0.6.7.1 | Cut detection; Python host for the captions-build script. |
| TTS | `piper-tts` | 1.4.2 | Natural voiceover and generated test clips (needs a voice model). |
| TTS (lightweight) | `espeak-ng` | 1.52.0 | Robotic but instant; fine for quick test audio. |
| Source download | `yt-dlp` | 2026.03.17 | Pull source/reference clips. |
| Playback / verify | `mpv` | 0.41.0 | Sanity playback (headless: verify via extracted frames). |
| Screen capture (Wayland) | `wf-recorder` / `wl-screenrec` | 0.6.0 / 0.2.0 | Screen recording on this Wayland session. |
| Full capture/stream (optional) | `obs-studio` | 32.1.1 | Heavier; only if multi-source scenes/streaming are wanted. |
| Caption fonts | `montserrat` `inter` `dejavu_fonts` | 9.0 / 4.1 / 2.37 | Bold, legible display fonts for the caption look. |
| Emoji in captions | `noto-fonts-color-emoji` | 2.051 | Color emoji glyphs for caption accents. |
| Font discovery | `fontconfig` | 2.17.1 | So libass resolves the fonts above (`makeFontsConf` in the flake). |

## Captioning route — the decision that drives the toolchain

The fancy-captions goal has two routes, and which one we commit to
changes what must be ready:

- **ASS-native (recommended; fully covered by the flake above).**
  `whisperx` → a word-timestamps-to-styled-ASS step → `ffmpeg -vf ass`
  burn-in, with the caption fonts + color-emoji. Every piece is
  nix-native; nothing needs `nix-ld`. The one missing piece is a small
  **word-timestamps → ASS generator**, which is a script the
  videographer authors (pure Python stdlib, no extra package), *not* a
  tool the readying agent installs. This route does the core TikTok
  look (word-by-word highlight, bold outline, pop/scale/fade, emoji,
  positioning).
- **pycaps (fancier CSS effects; harder on this box; defer).** Needs a
  browser renderer. On this machine that means either packaging
  Chromium via `python312Packages.playwright` (1.58) + nix `chromium`
  (147) — a real packaging effort — or `skia-python`, which is **not in
  nixpkgs**, or enabling `nix-ld`. Do **not** ready pycaps now; it is
  only worth it if the psyche specifically wants CSS-grade effects (see
  the open decisions). Detail and the dead-ends are in
  `reports/videographer/1-role-registration-2026-06-06.md` context and
  the earlier captions research.

## Hardware acceleration & capture notes

- **Encoding**: prefer VAAPI (`-vaapi_device /dev/dri/renderD128`,
  `h264_vaapi`/`hevc_vaapi`) to spare the CPU; verify the VAAPI driver
  resolves in-shell, else fall back to `libx264 -preset` on CPU.
- **Whisper**: CPU only — `--compute_type int8` and a `small`/`medium`
  model is the sane default; `large-v3` will be slow.
- **Screen capture**: `wl-screenrec` (VAAPI-backed, lighter) or
  `wf-recorder`; both are Wayland-native for this session.

## Model weights & caches

`whisperx` downloads a faster-whisper model plus a wav2vec2 alignment
model on first use (HuggingFace), totaling a few GB. This is **runtime
data cache, not a stateful package install** — analogous to the nix
store. The flake points `HF_HOME` at a project-local `.cache/`. The
readying agent should **pre-warm** it once (run `whisperx` on a short
sample) so the videographer isn't blocked mid-task on a download, and
note the cache location + size. A fixed-output nix derivation for the
weights is possible but is over-engineering for now.

## Verification checklist (run after `nix develop`)

```sh
ffmpeg -hide_banner -encoders | grep -E 'vaapi|libx264'   # encode paths
ffmpeg -hide_banner -filters  | grep -E '\b(ass|subtitles)\b'  # burn-in
ffprobe -version >/dev/null && echo ffprobe ok
whisperx --help >/dev/null && echo whisperx ok
python -c 'import scenedetect; print("scenedetect", scenedetect.__version__)'
piper --help >/dev/null 2>&1 && echo piper ok
wl-screenrec --help >/dev/null 2>&1 && echo wl-screenrec ok
magick -version | head -1
# end-to-end smoke: 5s test clip -> transcribe -> ASS -> burn-in -> frame
espeak-ng -w /tmp/vt.wav "the quick brown fox jumps over the lazy dog"
ffmpeg -y -f lavfi -i color=c=navy:s=1080x1920:d=5 -i /tmp/vt.wav \
  -shortest -c:v libx264 -pix_fmt yuv420p /tmp/vt.mp4
whisperx /tmp/vt.wav --model small --compute_type int8 --output_dir /tmp/vtx
# (videographer's ASS generator turns /tmp/vtx/*.json into /tmp/vt.ass)
# ffmpeg -y -i /tmp/vt.mp4 -vf ass=/tmp/vt.ass /tmp/vt-captioned.mp4
# ffmpeg -y -ss 2 -i /tmp/vt-captioned.mp4 -vframes 1 /tmp/vt.jpg  # eyeball
```

The commented last three lines depend on the videographer's ASS
generator (not yet written); the readying agent can stop after
confirming `whisperx` produces a word-level JSON.

## Open decisions (psyche / operator)

- **Flake location.** A dedicated small repo (e.g. a `video-kit` under
  `/git/...`, where video projects can also live) vs. a `videographer/`
  directory in primary (precedent: `orchestrate-cli/` lives in primary).
  Recommend a dedicated repo so source media and project files have a
  home; primary stays coordination-only.
- **Captioning route.** ASS-native now (recommended), or invest in
  pycaps/Chromium for CSS-grade effects later.
- **`nix-ld`.** If the psyche wants the easy pip path for future Python
  ML tooling (pycaps included), enabling `programs.nix-ld.enable` is a
  one-time NixOS config change + rebuild (psyche's sudo). Out of scope
  for the readying agent unless the psyche asks.
- **Model-cache policy.** Project-local `.cache/` (flake default) vs. a
  shared cache vs. a pinned nix derivation.
