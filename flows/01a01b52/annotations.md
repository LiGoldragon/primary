# Annotations

## 01a020ff · flows/01a01b52/log.md

Addendum — 2026-08-20

- The psyche reported that Emacs did not switch. A read-only follow-up found that this session changed and verified Chroma, Noctalia, dconf, the Settings portal, and GTK request state, but did not change, restart, or test Emacs. “The theme fix is deployed and live” therefore did not prove end-to-end application theming.
- Current Chroma and Emacs both resolve Dark, so no current divergence is present. Chroma is explicitly unlocated, reports `SolarClockUnavailable`, and cannot resolve its sunrise/sunset waypoints; an expected automatic Light transition is therefore absent for every consumer, not only Emacs.
- Emacs has no live theme subscription. Its init still reads a stale Darkman state file once at startup; Chroma applies later changes with a one-shot `emacsclient` command that discards output, ignores nonzero exit status, and never retries or reconciles. At the original startup Chroma and Emacs began in the same second, while the Emacs server socket appeared about four seconds later. This proves a race window but not the discarded historical client result.
- Noctalia repeatedly logged `portal color-scheme unavailable: System.Error.ENXIO` even after portal services were active, although its retained external fallback leaves it Dark now. A separate Chrome SIGTRAP/core dump was observed during the earlier process-replacement window, with no evidence tying it to theming. No current visual divergence in GTK/libadwaita, Chrome, VSCodium, or Qt was proved.
- The shared fragile boundary is write-and-forget projection: Chroma mutates settings or launches application-specific commands without consumer acknowledgement, while consumers independently depend on startup ordering, portal selection, fallbacks, and legacy state. No source, runtime, service, process, or deployment mutation occurred in this follow-up.

Correction addendum — 2026-08-21

- The psyche clarified that the observed event was a successful switch to Dark everywhere except Emacs. The preceding addendum's automatic-Light explanation is wrong. `SolarClockUnavailable` and GeoClue accuracy are unrelated to this Emacs-only miss.
- The relevant Dark reapply was at 23:48:04 CEST, more than three hours after Emacs became ready. Within three seconds Chroma, dconf, the Settings portal, and Noctalia all reported Dark. The preceding startup-race hypothesis therefore cannot explain the reported event.
- Chroma's Emacs concern is an independent one-shot `emacsclient --eval` projection. It discards stdout and stderr, ignores nonzero child exit status, catches concern errors before fanout can observe them, and has no retry or postcondition check. A failed connection, Lisp evaluation, or theme load can consequently leave Emacs behind while Chroma reports success and every preceding concern remains Dark.
- No exact Emacs error survives in Emacs buffers, its service journal, Chroma's journal, or a separate log. A later Light projection reached the same still-running Emacs daemon, ruling out a permanent client, environment, executable, or theme-file failure. The exact transient rejected condition is unknowable because the adapter erased it.
- The adapter also supplies the literal Lisp path `$HOME/.config/emacs-ignis-themes`, which cannot be shell-expanded. The correct expanded path was already present from Emacs startup in every observed active generation, so this is a confirmed additional defect but not a proved immediate cause. No sibling concern was shown to miss the same Dark event; Noctalia portal errors and the separate Chrome crash do not explain it.
