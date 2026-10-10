# Videographer role — registration

Created 2026-06-06 by psyche instruction, assigned to the Claude
session that handled the video-captions research earlier the same day
("add your role ... videographer"). This is the first artifact in the
videographer report lane.

## What the role is

Video as craft — the seventh main workspace role, parallel to `poet`
(prose as craft). Scope: filming and screen capture, editing,
captioning, encoding, and preparation for publishing — short-form
vertical (TikTok / Reels / Shorts) and long-form alike.

## What this registration changed

- `orchestrate/roles.list` — added the bare `videographer` main-role
  line. This is the data source the `orchestrate-cli` registry loads,
  so `tools/orchestrate claim videographer ...` works immediately; no
  Rust change is needed (the binary reads the list at runtime).
- `orchestrate/AGENTS.md` — added the `videographer` row to the roles
  table, the `claim <role>` enumeration, and the reports-convention
  list; bumped the role count six → seven.
- `AGENTS.md` (root contract) — role count six → seven; added the
  `videographer` bullet.
- `reports/videographer/` — this directory; this report.
- Lock file `orchestrate/videographer.lock` — runtime, gitignored;
  created on first claim.
- Spirit `4r1d` (Decision) records the role's creation.

## Tooling note

Per the no-stateful-install constraint (Spirit `j4r1`) and the role
decision (`4r1d`), videographer tooling runs ephemerally: `ffmpeg` /
`ffprobe` (already in the nix profile) for editing and encoding, and
transcription / caption tooling via `nix run` — never stateful pip
installs or persistent virtualenvs. The video-captions research that
prompted this role (pycaps vs. whisperx → ASS → ffmpeg, and the NixOS
binary-wheel constraints) is the craft's starting technical context.

## Open — to shape with the psyche

- `skills/videographer.md` and the `skills/skills.nota` `Role` entry
  are deliberately not written yet. The `auditor` precedent in
  `AGENTS.md` shows a role can be named before its skill file lands.
  The craft discipline — owned repos/tools, conventions, required
  reading — needs the psyche's direction before it is authored. That
  is the natural next step.
