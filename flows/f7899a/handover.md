# Psyche criomos Opus f7899a: handover, 2026-11-10 17:40 CST

State log: flows/f7899a/state.md. Deploy requests and await-watch.sh (opens a watch, submits, reads to the terminal; never re-query): flows/f7899a/deploy/.

## Open requests
- **fz3n (Psyche core Fable, Order; answer Fable in a few lines):**
  1. **Claude terminal fix:** declare the Claude Code theme in CriomOS-home as the ANSI theme that follows the terminal palette (light-ansi or dark-ansi; check which value the Claude Code version in Home accepts, and whether one ANSI theme serves both palettes). Today `~/.claude/settings.json` is an undeclared 0600 file holding "theme":"light" among other keys, so the declaration must merge the theme key and keep the rest. chroma switches the Ghostty palette ([Terminal Desktop Ghostty Pi], CriomOS-home modules/home/profiles/min/chroma.nix:132-146). Pin it in CriomOS, deploy li's Home on ouranos (and zeus), and say whether a running Claude session picks it up or only a new one.
  2. **chroma takes a GeoClue fix every 3 minutes:** find the cause and remove it. Repo /git/github.com/LiGoldragon/chroma: geoclue.rs (MAX_LOCATION_AGE 300 s, a FreshLocationLease), daemon.rs about 1216-1242 and 1355-1403, and a 60 s retry at schedule.rs:119-121 / daemon.rs:152-161. Those are probably polls too. Wanted: a static location changes only at a deployment, and a live one arrives as the GeoClue LocationUpdated signal that chroma subscribes to; no timer, no lease expiry. New chroma version, then a Home pin and deploy.
  3. Leave darkThemeSwitchTiming ("Early", sunset minus 30) alone; Fable is asking him.
- **l33p (Psyche core Opus, Task):** one proof run of the harness updater on the Lojix watch. Held until prometheus serves builds. Done with lojix 321682e (0.10.6), signal-lojix 0.11.0 bd5d250, meta-signal-lojix 0.12.0 1b0aaeb and the CriomOS revision.
- The Results qlcy, ilou, fhek, x9be, zar2, ryv5 (no lane busy on prometheus) answer 6670d4's switch question; prometheus was switched at 17:16 for 6fx6. Nothing owed.

## Done this flow
- k365, opch, pgyn, yrne and 4h7y answered. The live tether proof waits on his next plug-in at CriomOS 4400906.
- 3vj7: goldragon 6490c11 puts ouranos and zeus in Oaxaca. Deployed: ouranos 408/409 at CriomOS 4400906, zeus 410/411 at a09e39e. GeoClue static serves 17.0654, -96.7236.

## Live state
- ouranos: CriomOS 4400906 (gen 409). The runtime /run/systemd/logind.conf.d/90-trip.conf comes out when he is back.
- zeus: CriomOS a09e39e (gen 411). prometheus: 4400906. tiger: unreachable; deploy only when it is announced back.
- No background jobs.
