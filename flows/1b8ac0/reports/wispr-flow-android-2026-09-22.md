# Wispr Flow on Android: stuck transcription research (2026-09-22)

Commissioned by the living ("put some research in on whether there are problems with Wispr Flow on Android"). Research by a subflow of PsycheHigh 1b8ac0 with web search; prevalence claims are weak where noted.

## Is it known?

Partly. Wispr's own help center treats "Taking longer than usual… audio saved in the app" and "Failed to transcribe" as an expected Android state with a Retry path, naming battery/data restrictions and VPN/proxy as causes (docs.wisprflow.ai "Fix slow or failed transcription", updated ~2026-09-21; "Retry failed transcriptions"). The status page lists an Android-specific incident "Dictation failures on Android" on 2026-08-05 and multi-region latency incidents 2026-06-27 and ~2026-06-02→06-08 (statuspage.incident.io/wispr-flow/history). The changelog shows repeated Android fixes for exactly the "works after force-close, then dies" pattern: 1.8.4 "automatic recovery when the app is foregrounded after a force-stop or system kill", 2.0.9 (2026-07-02) bubble auto-recovery, Xiaomi/OnePlus battery-optimization fixes, Android 16 compatibility. Current Android version 2.5.2 (2026-09-19, "Reliability improvements").

Thin evidence: Google Play reviews could not be fetched; no indexed Reddit/X thread describes hours-long retry loops. The mechanisms are documented by Wispr; the prevalence of hours-long stalls is not independently corroborated.

## Likely causes, ranked

1. Background service killed or frozen by the battery manager (OEM autostart, "put unused apps to sleep", Android 13+ restricted bucket). Matches "works once or twice after force-close, then stalls".
2. Network path for cloud upload. Wispr is cloud-only at every tier; no on-device mode. VPN/proxy/DNS filtering are explicitly named blockers. Tailscale on Android has a known conflict with Private DNS (DoT) that breaks DNS (tailscale issue 4252). No Wispr-specific Tailscale report was found, but the failure shape fits: upload hangs with no clean error.
3. Wispr backend incidents (see status page).
4. Accessibility or "display over other apps" silently revoked (One UI does this).
5. Old build (below 2.0.9, especially Android 16 on 1.6.1 or older).

## What to try, in order

1. Update to 2.5.2; re-verify permissions after the update.
2. Battery: Unrestricted; Samsung: Never-sleeping apps, disable "Put unused apps to sleep"; disable "Pause app activity if unused".
3. Data: allow background and unrestricted data; exclude from Data Saver.
4. When it stalls, toggle Tailscale/VPN off and Retry the same saved audio. If it succeeds at once, the tunnel or Private DNS is the cause; set Private DNS to Automatic or disable Tailscale's DNS override.
5. Check the status page before spending time; subscribe.
6. Re-grant Accessibility and display-over-apps; reboot rather than force-stop (force-stop itself puts the app in a restricted state on many OEMs).
7. Keep takes short (Android auto-submits at 5 min); short chunks fail and retry cheaper.
8. Use in-app "Report issue" while it is stuck.

## On-device alternatives

- FUTO Voice Input (+ FUTO Keyboard/HeliBoard): offline Whisper; ~30 s capture window, so long monologues become many takes.
- Transcribro: on-device whisper.cpp with VAD chunking; handles continuous speech better; weaker punctuation.
- Dictate Keyboard (Whisper AI): Whisper keyboard with a local-model option; less proven.

None do Wispr-style filler removal; all remove the network dependence that is the leading suspect.
