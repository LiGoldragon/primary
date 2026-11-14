# Psyche core Opus 228e2b: handover

The living is winding down for the night and travels tomorrow. Claude usage is kept for Fable until Codex returns on Wednesday night. Start nothing new on your own; act on what reaches you.

## Waiting on the living's word (through Fable)

- **The ouranos reboot.** CriomOS a09e39e, Realize 386, is frozen as the reboot generation. It carries:
  - acpi_mask_gpe=0x6D;
  - suspend-then-hibernate on battery after 2 h, with the resume declared;
  - Flow 0.54.0 and the Lojix 0.10.6 updater change.

  BIOS 1.19 is cancelled. The order is: SetBootProfile (request in flows/6670d4/deploy/), then every flow writes its handover and leaves no background job, then the reboot. After the reboot, Mind flowNexus Opus restarts one cheap flow first, then the rest by script; this has not been tried yet.
- **Step 5, after the reboot.** One manual hibernate and resume. Then a 20-minute suspend on battery, read before and after. Then the same again with Ethernet down, WoL off and the GbE LTR ignored at runtime. Everything is in flows/228e2b/suspend/. The keep-alive audio has been removed and was a likely holder of HDA; a measuring suspend would show its effect.
- **Prometheus.** Its switch to a09e39e is held for tonight. Task 6wgg with Psyche criomos Opus is still open, and so are the zeus unit fixes (codex-remote-control-next with no working directory, and mpd on port 6600).
- **Tiger.** It is deployed only when it is announced back online.

## Open with lanes, paused

- **Build-once loop** (Field protos Opus): paused, see flows/014939/handover.md. Remaining work: the lanes repin to build-base 82d3c8e, and the doctest gap.
- **l33p** (Lojix streaming): built; its proof run follows the reboot.
- **The codex-next app-server** has run for 7.5 days at about 16 percent CPU. The living was offered stopping it until Wednesday and has not answered.

## Rules learned today

- No polling, for any reason. A design that would need a poll stops and goes to Fable as a Question; it is never landed as a debt.
- The living's words garbled by dictation: hold until Fable confirms the reading.
- A refreshed successor of a lane may miss my open requests if it predates Flow 0.53.4; since 0.53.5 they are carried by id.
- Book Haiku holds at most ten watches; a new book frees the coldest and is republished to arm its auto-replies.
