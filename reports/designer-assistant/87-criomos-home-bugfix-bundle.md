# 87 — CriomOS-home bugfix bundle on `horizon-re-engineering`

*Six discrete fixes land on the `horizon-re-engineering` branch
of CriomOS-home, one commit each.  Targets: the three
High-severity findings from designer-assistant/82
(`gap-audit-criomos-home.md`, §"Findings table" rows 1–3), the
Dead-code finding (§"Findings table" row 8 — orphan WM files),
the known-pending wasistlos comment stub (§"Findings table" row
4), and the Quickshell stale-widget note pending under bd
`primary-d5im` (§"Findings table" row 5).*

---

## TL;DR

Six fixes land cleanly.  `i7z` now gates on `node.chipIsIntel`
(the typed bool derived from `Arch::X86_64`) instead of the
always-false string comparison `arch == "x86-64"`; the dead
`services.dunst` block (`enable = !size.min` inside `mkIf
size.min`) is deleted in favour of noctalia owning
notifications; Emacs reads its dark/light mode from
`$XDG_STATE_HOME/chroma/current-mode` (verified against
`chroma/src/theme.rs:443`'s writer) instead of the retired
`darkman/` path; four orphan window-manager files plus
`med/element.nix` (a NixOS-shaped service masquerading in the
HM tree) are removed; the `wasistlos` comment stub in
`profiles/max/default.nix` is gone; an eight-line block above
`startWhisrs` in `dictation.nix` records the Quickshell
startup-only plugin-scan caveat.  Six commits, six pushes,
bookmark `horizon-re-engineering` advances from `72e31c43` to
`3826a67d`.

---

## §1 — arch typo (audit 82 finding 1, HIGH)

**File:** `modules/home/profiles/min/default.nix` (worktree
root `/home/li/wt/github.com/LiGoldragon/CriomOS-home/horizon-re-engineering/`,
same root for every file path below).

**Before** (line 133): `++ (optionals (node.machine.arch ==
"x86-64") [ i7z ]);`

**After**: `++ (optional node.chipIsIntel pkgs.i7z);`

**Why it never matched.**  The schema serialises
`Arch::X86_64` as the PascalCase string `"X86_64"` (verified by
`horizon-rs/lib/src/view/node.rs:82` + the cluster fixtures
under `CriomOS-test-cluster/fixtures/horizon/*.json`, every
node carries `"chipIsIntel": true` alongside the typed `Arch`
enum).  The hyphenated `"x86-64"` is not a value the
projection ever emits — the equality is always false, `i7z`
installs on zero nodes.

**Why `node.chipIsIntel`.**  The bool exists on `view::Node`
precisely for this kind of "is this an Intel chip" gate; it
lifts the dispatch out of the Nix layer and into the typed
projection, per `skills/abstractions.md` §"What 'find the
noun' actually looks like" — the verb "is this Intel" belongs
on the chip type, not on a free Nix string-compare.  The
CriomOS-side metal module already consumes the same field
(`/git/github.com/LiGoldragon/CriomOS/modules/nixos/metal/default.nix:21`,
used at lines 97, 232, 271, 433); this fix brings CriomOS-home
into alignment.  The list-append also flips from `optionals` +
a one-element list to `optional` + the bare package — the
idiomatic shape for a single conditional package.

**Commit:** `4f170231` (`home: i7z gates on node.chipIsIntel
(was always-false x86-64 string)`).

---

## §2 — dunst delete (audit 82 finding 2, HIGH)

**File:** `modules/home/profiles/min/default.nix`

**Before** (lines 291–303, inside the `mkIf size.min` body):

```nix
services = {
  dunst = {
    enable = !size.min;
    settings = { global = { geometry = "300x5-30+50"; transparency = 10; };
                 urgency_normal.timeout = 10; };
  };
  gpg-agent = { ... };
```

**After**: the `dunst` attribute is gone; `services.gpg-agent`
becomes the first child.

**Why it was dead.**  The whole `services` attrset sits inside
`mkIf size.min { ... }`.  `dunst.enable = !size.min` is
therefore `size.min AND !size.min`, which is always false;
dunst was never enabled.  A sibling comment three lines below
the deleted block (still present after this fix) reads `#
swaync disabled — noctalia handles notifications natively`.
Noctalia already owns the notifications path; dunst is doubly
redundant.  Clean delete, no commented stub — the git log
carries the removed config if anyone needs to revive it.

**Commit:** `4ff1c67b` (`home: delete dead services.dunst
block (noctalia owns notifications)`).

---

## §3 — Emacs theme reads chroma state path (audit 82 finding 3, HIGH)

**File:** `modules/home/profiles/med/emacs.nix`

**Before** (line 213–223, inside the `initEl` blob): a
`darkman/current-mode` path expansion feeding a `pcase` on
`"dark"` / `"light"`.

**After**: the `darkman/current-mode` literal becomes
`chroma/current-mode`; the comment expands to name the
producer + the writer site + the deferred push-style follow-up
inline:

```elisp
;; Load ignis theme from chroma state at startup.  Chroma writes
;; "$XDG_STATE_HOME/chroma/current-mode" with the literal "dark" or
;; "light" (chroma/src/theme.rs:443).  Replaces darkman, which was
;; retired; the old path "darkman/current-mode" no longer updates.
;; File-poll only at Emacs startup — push-style theme updates from
;; chroma are tracked as follow-up (see designer-assistant report 87).
```

**Why the chroma path.**  Chroma replaced darkman as the
visual-state daemon (theme + warmth + brightness, per the
comment block in `profiles/min/default.nix` lines 269–275 and
the chroma module at `profiles/min/chroma.nix`).  The chroma
daemon writes its current mode to `$XDG_STATE_HOME/chroma/current-mode`
as the literal string `"dark"\n` or `"light"\n` — verified at
`/git/github.com/LiGoldragon/chroma/src/theme.rs:443`:
`tokio::fs::write(state_dir.join("current-mode"),
format!("{mode}\n")).await?;`.  The Emacs init already
string-trims the file content and dispatches on `"dark"` /
`"light"` via `pcase`, so producer wire format matches
consumer expectation byte-for-byte.  The chroma activation
hook in `profiles/min/chroma.nix:185–187` also seeds the
default file with `"dark"`, so first-boot has a value.

**Why file-poll persists (and the deferred work).**
Push-not-pull discipline (`skills/push-not-pull.md`
§"Subscription contract") prefers a subscription contract
over file-poll-at-startup; the right long-term shape is for
chroma to expose a D-Bus or socket signal on mode change, and
Emacs to subscribe.  Today chroma's only public surface for
"current mode" is the state file; building the subscription
path is multi-step work touching both chroma (producer:
signal, schema) and the Emacs init (consumer: `dbus-monitor`
subprocess, lifecycle binding).  Out of scope for this bundle.
The expanded comment in the file names the gap inline.  See §8
below for the follow-up framing.

**Commit:** `5bf79c7d` (`home/emacs: read theme mode from
chroma state path (was retired darkman path)`).

---

## §4 — orphan WM files + element.nix delete (audit 82 finding 8 + finding 9)

**Files deleted:** `modules/home/profiles/min/waybar.nix`,
`min/hyprland.nix`, `min/sway.nix`, `min/swayConf.nix`,
`modules/home/profiles/med/element.nix`.

**Files modified:** `modules/home/default.nix` — removed the
four-line comment that explained why `element.nix` was NOT
imported (the explanation is moot once the file itself is
gone).

```mermaid
graph TD
  hm[modules/home/default.nix]
  hm -.imports.-> live[profiles/{min,med}/* live files]

  del1[profiles/min/waybar.nix]:::gone
  del2[profiles/min/hyprland.nix]:::gone
  del3[profiles/min/sway.nix]:::gone
  del4[profiles/min/swayConf.nix]:::gone
  del5[profiles/med/element.nix]:::gone

  del3 -.imports.-> del4
  hm -.X never imported.-> del1
  hm -.X never imported.-> del2
  hm -.X never imported.-> del3
  hm -.X never imported.-> del5

  classDef gone fill:#eeeeee,stroke:#9e9e9e,stroke-dasharray:5
```

**Per-file ownership check** (`grep` over the worktree for
each filename, scoped to `.nix`, `.toml`, `.md`):

| File | Imports found | Verdict |
|---|---|---|
| `waybar.nix` | 0 | orphan — delete |
| `hyprland.nix` | 0 | orphan — delete |
| `sway.nix` | 0 | orphan — delete |
| `swayConf.nix` | 1 (`min/sway.nix:47`) | orphan-chain — delete with `sway.nix` |
| `med/element.nix` | 1 (a comment in `default.nix` explaining the non-import) | orphan + wrong tree — delete; the comment in `default.nix` also goes |

**Why element.nix goes too.**  The file declares
`systemd.services.nginx-element` (system-level, not user-level
— `home-manager` evaluation would surface this as a
wrong-module-type error if it were imported).  It's a NixOS
module shape masquerading as an HM profile (audit 82
§"Per-file walk → `modules/home/default.nix`" + the in-file
comment at `default.nix:62` both named the mis-location).  The
audit's two-option framing — "move to CriomOS or delete" —
collapses to delete because the file is also **incomplete**:
the `nginx-element` service is a single hardened unit with no
reverse-proxy + matrix-server pair wired anywhere (per
recommendation 6 in audit 82's §"Recommendations").  Reviving
as a NixOS module would start from the git log; the on-disk
file isn't a working starting point.

The `fzfBase16map.nix` / `fzfDark.nix` / `fzfLight.nix` /
`zed_colemak_keybindings.json` files that audit 82 flagged as
"likely ORPHAN" (§"Orphan / dead files in `profiles/min/`"
table) are out of scope for this bundle — they need
independent consumer-existence verification, and the user
instruction named only the five files above.  Tracked as
future work (see §8).

**Commit:** `1ab36df0` (`home: delete orphan WM files (waybar,
hyprland, sway, swayConf) and element.nix`).

---

## §5 — wasistlos clean delete (audit 82 finding 4)

**File:** `modules/home/profiles/max/default.nix`

**Before** (lines 46–50, inside `mkIf size.large`):

```nix
[
  # freecad # broken
  # wasistlos # removed upstream (unmaintained); upstream hint: karere
  gitkraken
]
```

**After**: the `# wasistlos` line is gone; the `# freecad #
broken` line above survives.

**Why clean delete.**  The `wasistlos` upstream removal is
permanent (the package is unmaintained); the comment stub
doesn't earn its place.  The "upstream hint: karere" survives
in the report layer (`~/primary/reports/system-assistant/15-handover-2026-05-14.md`
§"Side notes" captured it originally), so the substance isn't
lost.  The `# freecad # broken` line above is a separate
audit-flagged item (audit 82 finding 4, second half) on a
different package whose breakage is the live reason for the
omission — that line stays for now (see §8).  The wasistlos
line is unique in being a comment about a delete-already-done.

**Commit:** `d0b2661d` (`home/max: drop wasistlos comment stub
(clean removal)`).

---

## §6 — Quickshell stale-widget note (audit 82 finding 5, bd `primary-d5im`)

**File:** `modules/home/profiles/min/dictation.nix`

**Insertion** — eight lines added immediately above
`startWhisrs`:

```nix
# Quickshell stale-widget caveat: noctalia-shell (the Quickshell host
# for the whisrs-level bar widget) scans its plugins directory only at
# process start.  After a `home-manager switch` that updates plugin
# files, the widget renders neutral until the host restarts.  Niri's
# `spawn-at-startup` fires only at session start; there is no plugin-
# rescan IPC.  Restart shape: kill the running quickshell PID and
# relaunch `noctalia-shell` detached.  A "permanently neutral" widget
# on a CriomOS-home deploy day is a stale-quickshell smell first.
```

**Why this placement.**  The user-flow that hits the caveat
is: developer changes the whisrs-level `BarWidget.qml` in
`noctalia-plugins/`, runs `home-manager switch`, expects the
bar widget to re-render.  The dictation module is where the
whisrs service + the plugin-asset drop meet; the niri
`spawn-at-startup` block immediately below the `startWhisrs`
definition also fires only at session start, doubling the
relevance of the caveat to this file.

**Substance.**  Distilled from
`~/primary/reports/system-assistant/15-handover-2026-05-15.md`
§"Operational note from former report 01" — the five-fact
shape: scan happens at startup; `home-manager switch` doesn't
trigger re-scan; restart procedure is "kill the running
quickshell PID and relaunch `noctalia-shell` detached"; Niri
spawn-at-startup is one-shot at session start; diagnostic
heuristic is to suspect a stale quickshell first.  The comment
preserves what an in-tree reader needs without sending them to
a report.

**Commit:** `3826a67d` (`home/dictation: note Quickshell scans
plugins only at startup (bd primary-d5im)`).

---

## §7 — Commits pushed

| # | Commit | Bookmark advance | Message |
|---|---|---|---|
| 1 | `4f170231` | `72e31c43 → 4f170231` | `home: i7z gates on node.chipIsIntel (was always-false x86-64 string)` |
| 2 | `4ff1c67b` | `4f170231 → 4ff1c67b` | `home: delete dead services.dunst block (noctalia owns notifications)` |
| 3 | `5bf79c7d` | `4ff1c67b → 5bf79c7d` | `home/emacs: read theme mode from chroma state path (was retired darkman path)` |
| 4 | `1ab36df0` | `5bf79c7d → 1ab36df0` | `home: delete orphan WM files (waybar, hyprland, sway, swayConf) and element.nix` |
| 5 | `d0b2661d` | `1ab36df0 → d0b2661d` | `home/max: drop wasistlos comment stub (clean removal)` |
| 6 | `3826a67d` | `d0b2661d → 3826a67d` | `home/dictation: note Quickshell scans plugins only at startup (bd primary-d5im)` |

All commits pushed individually to `origin` via `jj git push
--bookmark horizon-re-engineering`.  The final bookmark sits
at `3826a67d`.  Pre-existing merge commit `72e31c43` (the
recovery merge from earlier in the 2026-05-15 session) is now
an ancestor of `4f170231` — FIX 1's content rides on top of
the merge node, with the merge node still carrying both
parents (the wasistlos comment-out at `mnyukyqm/0` and the
pi-models step-6 at `mnyukyqm/2`).  No empty-description
commits (`jj log -r '@- & description(exact:"")'` empty).

Per-fix parse check via `nix-instantiate --parse <file> >
/dev/null` passes for every edited file before the commit; no
`nix build` or `nix flake check` runs (resource posture:
user's laptop overheating).

---

## §8 — Open follow-ups

**Chroma push-subscription for Emacs theme** (FIX 3's
deferred-to-subscription note).  Today the Emacs init
file-polls `chroma/current-mode` once at startup; mid-session
theme changes don't propagate.  The right shape per
`skills/push-not-pull.md` §"Subscription contract" is for
chroma to expose a D-Bus signal on mode change (or extend the
existing chroma IPC, if one lands) and for Emacs to subscribe
via `dbus-register-signal`.  Two-side work: producer-side
schema + signal emission in `chroma/src/theme.rs`;
consumer-side `dbus-register-signal` + `load-theme` wiring in
`med/emacs.nix`.  Not file-tracked anywhere yet; bd-worthy
under `role:designer` if the user wants it queued.

**Remaining likely-orphans in `profiles/min/`** (audit 82
§"Findings table" row 10).  `fzfBase16map.nix`, `fzfDark.nix`,
`fzfLight.nix`, `zed_colemak_keybindings.json` — flagged
"likely ORPHAN" by the audit, not in this bundle's scope.
Each needs an independent consumer-existence check (chroma
owns fzf theming via the `base.nix` init hook today; zed is
not in any package list).  A follow-up cleanup commit can
sweep these together once verification is done.

**`freecad` comment in `max/default.nix`** (audit 82 finding
4, second half).  The `# freecad # broken` comment stub above
the now-deleted `# wasistlos` line is structurally the same
shape — a comment about a package that isn't being installed.
The audit's direction is "delete-or-fix": either the upstream
freecad breakage is fixable (in which case the package goes
back in), or the comment goes the way of wasistlos.  Out of
scope here because the upstream-fix path needs investigation.

**`AIPackages` PascalCase** (audit 82 finding 19).  The
binding name on `profiles/min/default.nix:177` is PascalCase
for an instance value (a list of packages); ESSENCE
§"PascalCase = compile-time structural; camelCase = instance"
wants `aiPackages`.  One-line rename + every call-site in the
same file (only the `home.packages = ... ++ AIPackages ++ ...`
site).  Not in this bundle's scope; trivially follow-uppable.

**Profile-ladder concern split** (audit 82 finding 11 + the
recurring `primary-gfc0` operational debt item).  The largest
structural follow-up: split `profiles/min/default.nix` into a
non-graphical-base file (CLI tools, fonts, gpg-agent, gated on
`size.min`) and a desktop-session file (ghostty, wofi, lapce,
wl-gammarelay, gated on `behavesAs.edge`).  Prerequisite for
the cloud-host work tracked under designer report 78.  Tracked
in bd; out of scope here.

---

## Cross-references

- **`~/primary/reports/designer-assistant/82-gap-audit-criomos-home.md`**
  — the audit driving this bundle.  §"Findings table" rows
  1, 2, 3 are the three HIGH items (arch typo, dunst
  always-false, Emacs darkman path); row 8 is the orphan-WM-files
  finding; row 9 is `element.nix`'s wrong-tree placement; row 4
  is the wasistlos stub; row 5 is the Quickshell stale-widget
  note.
- **`~/primary/reports/system-assistant/15-handover-2026-05-15.md`**
  §"Operational note from former report 01" — the substance
  for the Quickshell caveat distilled into FIX 6's comment
  block.
- **`/git/github.com/LiGoldragon/chroma/src/theme.rs:443`** —
  the writer for `current-mode`; verified against FIX 3's
  reader (`format!("{mode}\n")` ⇄ the Emacs init's
  `string-trim` + `pcase` on `"dark"` / `"light"`).
- **`/git/github.com/LiGoldragon/horizon-rs/lib/src/view/node.rs:82`**
  + cluster fixtures under `CriomOS-test-cluster/fixtures/horizon/`
  — the typed `chipIsIntel: bool` field FIX 1 now consumes.
- **`~/primary/skills/push-not-pull.md`** §"Subscription
  contract" — names the file-poll vs subscription discipline
  that FIX 3's deferred follow-up restates (§8).
- **`~/primary/skills/abstractions.md`** §"What 'find the
  noun' actually looks like" — backs FIX 1's
  move-the-verb-onto-the-noun shape (the "is this Intel" verb
  belongs on the chip type, not on a free Nix string-compare).
- **bd `primary-d5im`** — the in-flight bead item filed for
  the Quickshell stale-widget note; FIX 6 closes the in-source
  comment side.  The bd item itself can be closed by whoever
  holds the operator lock next.

---

*End of report 87.*
