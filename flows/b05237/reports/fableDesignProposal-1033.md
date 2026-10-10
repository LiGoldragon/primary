# Fable's Design Proposal, 09-18 10:33am

Carried verbatim from flow c7128c (Fable), session
`c7128cb2-3ac6-424e-8db3-d5f3313ffea0`, response at
2026-09-18T16:33:38Z (10:33:38am local). Five forks for the living
to rule on, each with a proposed shape.

## 1. Hardware type

Today one string names the model and a table turns it into three
booleans. Booleans do not scale to a phone.

Proposed shape — one classification call, gating everywhere:

- model string, turned into a hardware record, read by every module
- record fields: kind (laptop, desktop, board, phone), arch
  (x86-64, aarch64), touch, battery, modem (yes/no), desktop
  (niri, phosh, none)

The record is computed once, beside the table that exists now.
Modules ask "kind is phone" or "desktop is phosh", never "is this
a ThinkPad". An unknown model stays an evaluation error, as today.
Horizon behaviour roles stay what they are; `mobile` is added as a
role for the phone.

Fork: richer record as above, or more booleans. Booleans mean every
new device adds a column to every row.

## 2. Stock harnesses

Keep one stable version of each harness as a plain upstream fetch
with the ordinary executable name. Codex stops being built from
source. If a patch is still needed, it lives in a wrapper around
the stock binary, never in the source, named as a separate variant.

Flow: upstream release, to fetched binary, to stock `codex` and
`claude` — with an optional wrapper variant under its own name.

Unknown to Fable: what the current source patches do. If one is
load-bearing, it must be listed before the switch.

## 3. Stable and next Codex remote

Two user services, both logged in, both running, distinct names,
distinct sockets and state directories: `codex-remote-stable`
pinned to pin A, `codex-remote-next` pinned to pin B. On handover,
pin B becomes stable, a new pin becomes next, and it rebuilds.

Two Nix profiles would not do this — a profile switches the whole
environment and cannot run both at once. Two services do exactly
the alpha/beta alternation described. The plain `codex-remote` name
always points at stable.

## 4. Herder window management

Full screen by default, and a layout template per layer rather than
a single split cap:

- primary: one full pane, subflows as tabs
- secondary: two splits
- worker: up to four splits, then a new tab

A cap alone still leaves the confusing state described. Templates
make the layout say what the pane is. The Herder user guide and the
Vim/Emacs research asked for are a separate report, not yet done.
Whether Herder 0.8.2 supports layout templates natively is unknown
to Fable.

## 5. Mobile compositor for the Libre M5

Three-way fork:

- **Phosh** — the GNOME phone shell. Mature on Linux phones,
  touch-first, conservative.
- **Niri** — what runs now. Scrollable tiling, touch support young.
- **Sway with touch** — works, but nobody designs for it on a phone.

Proposal, from the living's own earlier suggestion: two profiles.
Conservative profile is Phosh, testing profile is Niri, both
selected by the hardware record's desktop field. Unknown to Fable:
whether the Libre M5's chip has NixOS kernel support at all — must
be verified upstream before anything else on this device.

## The three repos and Primary Next

Primary Next is a template, bare, rebased-history repo. It expects
`psyche/`, `mind/`, and `field/` mounted. A persona sets them up at
a chosen level: stable or testing.

The field Nexus is the system monitor; agents ask it, it signals
with a trace back to the caller. Energy levels name models: Luna is
ultra-low, Terra is low, Sol is medium, Astra is high. Model effort
stays medium throughout.

After the living rules on the five forks, this goes to Astra for
implementation.

## Sources

- Flow c7128c (Fable), session
  `c7128cb2-3ac6-424e-8db3-d5f3313ffea0`, transcript line 732,
  timestamp 2026-09-18T16:33:38.502Z, read via
  `/git/github.com/LiGoldragon/transcript/transcript.py`.
