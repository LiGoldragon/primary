# Wispr physical keyboard capture on Ouranos

Remembered: 01a052bb and 01a05209 — depth 1. Canonical Lojix 0.20.0 and the Wispr window repair are live. This flow owns only keyboard shortcut capture without reading Wispr session contents, changing autostart, or touching Codium.

Live diagnosis: `input_id` classifies event0 (AT keyboard), event1 (MiniDox), and event20 (keyd virtual keyboard) as keyboards. Stored udev state lacks `uaccess` for all three, but a udev add simulation applies the deployed rule to all three. The missing physical-keyboard ACL is stale udev state, while the current keyboard-only predicate is too broad because it includes keyd's virtual node. Determine and realize the smallest physical-origin declarative restriction, then deploy and reprocess only its intended keyboard nodes.

Correction: the runtime exposed the parent `CODEX_SESSION_ID` as 01a052bb. The distinct `CODEX_THREAD_ID` identifies this subflow as 01a05396; an accidental parent-log append was immediately restored, and the parent lock was released using deployed scalar `Release.385` syntax.
