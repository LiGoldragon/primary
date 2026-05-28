# DJI Mic Profile Churn Fix

## Trigger

Li reported that the DJI Mic no longer stayed hot for speech-to-text. The
symptom was a two-to-three second wake delay when starting Whisrs, with the
Bluetooth profile visibly changing and the keepalive stream failing to keep the
mic awake.

## Findings

- `whisrs status` was respected before live changes. I did not restart the
  keepalive service or change the Bluetooth profile while Whisrs reported
  `recording` or `transcribing`.
- The live `dji-keepalive.service` was active and had a `pw-loopback` child, but
  its journal repeatedly logged that the DJI card had left
  `headset-head-unit`.
- A live profile watch showed the card really flipping from
  `headset-head-unit` to `off`.
- The old service treated any profile mismatch as fatal: it killed the loopback,
  unloaded the null sink it owned, then rebuilt the stream. That made each
  profile blip drop the hot capture path.
- Manual `ConnectProfile` plus `pactl set-card-profile` restored the MSBC
  headset profile and held it stable for a one-minute watch.

## Change

Changed `CriomOS-home` so `dji-keepalive.service` repairs profile mismatch
in-place:

- added `reassert_profile`;
- added a short settle after BlueZ `ConnectProfile`;
- expanded profile entry retries during startup;
- changed the steady-state profile mismatch path to reassert profile without
  dropping the existing `pw-loopback`;
- kept teardown only for real Bluetooth disconnects, missing source/sink, or
  child process exit;
- added a Nix check that rejects the old profile-mismatch teardown log path.

## Files

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/dji-keepalive/default.nix`

## Verification

- `nix --max-jobs 0 build .#checks.x86_64-linux.dji-keepalive --no-link -L`
  passed using Prometheus as builder.
- Commit pushed: `b76dcc65` (`home: repair dji keepalive profile in place`).
- Activated through lojix:
  `(HomeOnly goldragon ouranos li [/git/github.com/LiGoldragon/goldragon/datom.nota] [github:LiGoldragon/CriomOS-home/main] Activate (Some prometheus) None)`.
- The live service now runs
  `/nix/store/vi738p6dprjc84w2ka67sf4lpd89ml09-criomos-dji-keepalive`.
- Post-activation journal showed one initial profile blip repaired with:
  `reasserting profile without dropping keepalive`.
- After that, a one-minute profile watch stayed on `headset-head-unit`.
- `pactl list short sources` showed the DJI source and keepalive monitor
  running.
- A Whisrs `toggle-copy` then `cancel` smoke test opened the mic and returned to
  `idle` without a transcription request; the card stayed on
  `headset-head-unit`.

## Remaining Risk

One observed event was a real BlueZ connection drop. The service still has to
tear down and reconnect for a true Bluetooth disconnect. This fix addresses the
avoidable self-inflicted churn where a transient profile mismatch killed the hot
stream.
