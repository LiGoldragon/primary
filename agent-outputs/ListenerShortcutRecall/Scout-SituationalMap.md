# Listener Shortcut Rebind + Transcript Recall Scout Map

## Task And Scope

Read-only scout for a planned Listener change:

- record/toggle: `Mod+Alt+M` -> `Mod+M`
- cancel: `Mod+Ctrl+Alt+M` -> `Mod+Ctrl+M`
- add a past-transcript recall UI on `Mod+Alt+M` (the key being freed by the toggle move)
- `Mod+Shift+M` stays unbound

I mapped three areas: (1) keybind source of truth and collisions, (2) Listener
transcript persistence for a recall UI, (3) the existing Whisrs recall UI and
reuse options. I did not edit, deploy, run anything with side effects, read
transcript/audio contents, or trigger transcription/API spend.

Host/date context: workspace `/home/li/primary`, date 2026-07-02.

## State Note (advance since the ListenerUsabilityFixes lane)

The premise handover is accurate and already deployed:

- Listener is live at `0.5.1` with typed cancel (`listener cancel <session>`).
- The previous lane already moved Listener off `Mod+Alt+L` onto `Mod+Alt+M`
  (record/toggle) and `Mod+Ctrl+Alt+M` (cancel). `Mod+Alt+L` is gone.
- `signal-listener` is at `0.4.0` with the typed `Cancel`/`Cancelled` operation.

So this lane operates on the current deployed binds, not the old `Mod+Alt+L`.

## Repos And Files Consulted

Compositor / home config (the source of truth):

- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/listener-dictation-bindings/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/whisrs-dictation-bindings/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/checks/whisrs-recall/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/packages/whisrs/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/flake.nix`, `flake.lock`
- Active rendered compositor config: `/home/li/.config/niri/config.kdl`

Listener + contract:

- `/git/github.com/LiGoldragon/listener/src/{runtime,delivery,capture,recording_log,transcription,configuration,command}.rs`
- `/git/github.com/LiGoldragon/signal-listener/src/lib.rs`, `src/schema/lib.rs`, `Cargo.toml`

Whisrs:

- `/git/github.com/LiGoldragon/whisrs/src/history.rs` (local checkout `af25e63`)
- `whisrs-recall` source viewed at the pinned `criomos` rev `c32c8bcf`:
  `src/recall/main.rs`, `src/recall.rs`

On-disk state (names/sizes only, no contents read):

- `~/.local/state/listener/captures/`
- `~/.local/share/whisrs/history.jsonl`

Prior evidence read: the five files named in the brief under
`agent-outputs/ListenerUsabilityFixes/*` and
`agent-outputs/ListenerCancelSemantics/GeneralCodeImplementer-Evidence.md`.

## Area 1 — Keybind Source Of Truth

### Compositor

The compositor is **niri** (not Hyprland/Sway). Binds are authored in Nix under
`programs.niri.settings.binds` and rendered to `/home/li/.config/niri/config.kdl`.
Niri has no implicit/default keybinds — every bind is explicit in this config, so
the config is the complete bind surface.

### Current dictation binds (observed facts)

All in `dictation.nix`, inside `programs.niri.settings.binds`:

- `:329` `binds."Mod+V"` -> `a.spawn "${whisrs}/bin/whisrs" "toggle-copy"` (title "Voice Typing (Copy)")
- `:335` `binds."Mod+Shift+V"` -> `a.spawn "${whisrs}/bin/whisrs" "toggle"` (title "Voice Typing")
- `:341` `binds."Mod+Alt+V"` -> `a.spawn "${whisrs}/bin/whisrs-recall"` (title "Voice Typing Recall")
- `:347` `binds."Mod+Ctrl+V"` -> `a.spawn "${whisrs}/bin/whisrs" "cancel"` (title "Voice Typing Cancel")
- `:353` `binds."Mod+Alt+M"` -> `a.spawn "${listenerToggle}/bin/listener-toggle-capture" "toggle"` (title "Listener Capture")
- `:359` `binds."Mod+Ctrl+Alt+M"` -> `a.spawn "${listenerCancel}/bin/listener-cancel-capture" "cancel"` (title "Listener Cancel")

`whisrs` and `listener` package derivations: `dictation.nix:17-18`
(`whisrs = pkgs.callPackage ../../../../packages/whisrs`, `listener =
inputs.listener.packages.<system>.default`).

### What each Listener bind actually runs

`Mod+Alt+M` -> `listener-toggle-capture toggle`, a wrapper defined at
`dictation.nix:90-121`:

- runs `listener status`; if the daemon is down it `systemctl --user start
  listener.service` and polls;
- on `(StatusReported Idle)` it `exec listener start`;
- on `(StatusReported (Capturing (...)))` it parses the numeric session and
  `exec listener stop "$session"` (stop = transcribe + clipboard-deliver);
- the wrapper's stdout therefore carries the full typed stop reply
  (`(Stopped (... transcript ...))`) — relevant to Area 2.

`Mod+Ctrl+Alt+M` -> `listener-cancel-capture cancel`, wrapper at
`dictation.nix:123-135`: reads the active session, `exec listener cancel
"$session"` (no transcribe, no clipboard, retains the audio artifact).

The active rendered config confirms the two live binds:
`/home/li/.config/niri/config.kdl:65` (`Mod+Alt+M` -> listener-toggle-capture) and
`:74` (`Mod+Ctrl+Alt+M` -> listener-cancel-capture).

### Collision scan (Mod+M / Mod+Ctrl+M / Mod+Alt+M / Mod+Shift+M)

Searched the whole CriomOS-home `modules/` tree and the active rendered
`config.kdl` for any `M`-letter binds:

- The ONLY `M`-letter binds anywhere are the two Listener binds above
  (`Mod+Alt+M`, `Mod+Ctrl+Alt+M`).
- `rg '"Mod\+M"|"Mod\+Ctrl\+M"|"Mod\+Shift\+M"'` across the whole repo: **no hits**.
- No `Mod+M`, `Mod+Ctrl+M`, or `Mod+Shift+M` in `config.kdl` either.

Verdict: **no collision** for the three target keys. `Mod+M` (bare mod+letter),
`Mod+Ctrl+M`, and `Mod+Shift+M` are all currently free. Niri has no builtin
bind to collide with. `Mod+Alt+M` is not a collision either — it is being freed
by the toggle move and reused for recall (a self-consistent reassignment).

Note: `Mod+L` is the session-lock key in `niri.nix` (prior lane evidence), which
is why Listener uses the `M` family, not `L`. `Mod+Minus`/`Mod+Shift+Minus`
exist in `niri.nix:362-364` but are unrelated to the `M` letter.

### Exact edits to make the planned change

In `dictation.nix`:

1. `:353` change the bind key string `"Mod+Alt+M"` -> `"Mod+M"` (keeps the same
   `listener-toggle-capture toggle` action; title "Listener Capture").
2. `:359` change `"Mod+Ctrl+Alt+M"` -> `"Mod+Ctrl+M"` (keeps `listener-cancel-capture
   cancel`; title "Listener Cancel").
3. Add a NEW `binds."Mod+Alt+M"` spawning a Listener recall program (title e.g.
   "Listener Recall"). That recall program does not exist yet (see Area 2/3).
4. `Mod+Shift+M`: leave absent.

Required companion edit (will otherwise fail the build check):
`checks/listener-dictation-bindings/default.nix` currently asserts
`Mod+Alt+M -> listener-toggle-capture` (`:75-77`) and
`Mod+Ctrl+Alt+M -> listener-cancel-capture` (`:79-81`), and asserts
`Mod+Alt+L` is absent (`:83-85`). These assertions must be retargeted to the new
keys, and a new assertion added for the recall bind. The whisrs-bindings check
(`checks/whisrs-dictation-bindings`) does not change — no Whisrs bind moves.

Both checks are wired in `flake.nix:382` (whisrs-dictation-bindings),
`:385` (listener-dictation-bindings), `:389` (whisrs-recall smoke).

## Area 2 — Listener Transcript Persistence

### What `.listenerlog` is

A **custom binary AUDIO recording log**, not text. `recording_log.rs`:

- file magic `LSTNLOG1` (`:12`), framed records (`LSTNREC1`/`LSTNCMT1`) of
  signed-16-bit-LE mono 16 kHz PCM with CRC32 checks and a recovery scanner;
- max record payload 8192 bytes (`:22`);
- lives in the capture store directory, file name `capture-<session>.listenerlog`
  (`capture.rs:108-116`).

Capture store directory (`configuration.rs:195-206`): `$XDG_STATE_HOME/listener/captures`
or `~/.local/state/listener/captures`, overridable by `LISTENER_CAPTURE_STORE`.
Confirmed on disk: `~/.local/state/listener/captures/` holds only
`capture-N.listenerlog` (audio) and `capture-N.raw.s16le` (raw PCM export). No
text files.

### Where finished transcripts land

On normal stop (`runtime.rs:95-150`): recover the log -> `export_raw_pcm` to
`capture-N.raw.s16le` -> `transcriber.transcribe(...)` (OpenAI) -> deliver the
resulting `TranscriptText` to the **system clipboard** via
`OutputTargetDispatcher.deliver` (`delivery.rs`). The only output target is
`OutputTarget::SystemClipboard` (`delivery.rs:69-77`), executed as `wl-copy` (or
`LISTENER_CLIPBOARD_PROGRAM`, `delivery.rs:107-118`).

The transcript is also returned inside the typed reply `Output::Stopped(
CaptureStopped { ..., transcript_text: TranscriptText(String), ... })`
(`signal-listener/src/schema/lib.rs:379-383, 498`). The CLI prints the whole
reply via `writeln!(output, "{reply}")` (`listener/src/command.rs:27-31`) using
the generated NOTA `Display` for `Output` — so `listener stop <session>` emits
the transcript text on stdout as part of the NOTA projection, and the
`listener-toggle-capture` wrapper (which `exec`s `listener stop`) inherits that
stdout.

### Is there a persisted transcript list today?

**No.** There is zero transcript-text persistence in Listener:

- No history/journal/transcript file is written anywhere (`rg` for
  history/persist/save in listener src: only the audio `CaptureStore`).
- The only `remove_file` calls are socket cleanup (`daemon.rs:140`,
  `status.rs:321`); audio artifacts accumulate but are never turned into text.
- On-disk confirmation: nothing under `~/.local/state/listener`,
  `~/.local/share/listener`, or `~/.config/listener` holds transcripts — only
  binary audio.

The retained `.listenerlog`/`.raw.s16le` files are AUDIO; deriving text from
them would require re-running OpenAI transcription (real API spend). A recall UI
must NOT read them.

### What a recall feature would read from

A recall feature needs a **new transcript-text store** that does not exist today.
The text to populate it already exists end-to-end at stop time (no
re-transcription needed):

- cleanest producer: `runtime.rs` `stop()` at the point it holds
  `transcript_text` (`:126`) — the daemon can append a history entry on
  stop-success, and it also has session id and start time (from the recording
  log header) for metadata;
- alternative producer without daemon changes: the `listener-toggle-capture`
  wrapper could parse the NOTA `Stopped` reply on stdout and append to a history
  file — feasible but fragile (shell-parsing NOTA) and lacks clean metadata.

### Contrast with Whisrs

Whisrs already has exactly the store Listener lacks. `whisrs/src/history.rs`:

- append-only JSONL at `$XDG_DATA_HOME/whisrs/history.jsonl`
  (`~/.local/share/whisrs/history.jsonl`; confirmed present, 1.9 MB, mode 600,
  actively appended);
- `HistoryEntry { timestamp: DateTime<Local>, text: String, backend: String,
  language: String, duration_secs: f64 }`;
- `append_entry` on each successful transcription (the whisrs daemon writes it;
  `dictation.nix` even chmods/creates the file in `whisrsServe`);
- `read_entries(limit)` returns newest-first, truncated to `limit`.

### Verdict

**Recall needs a NEW store — it is not "wire an existing store to a UI".**
Listener persists audio only; it has no transcript-text history. However the
store is a small, additive, self-contained addition (mirror Whisrs's JSONL
`HistoryEntry`, append on stop-success), because the transcript text is already
produced and available in the daemon and in the typed stop reply. Concretely,
the recall UI would read from a to-be-created `history.jsonl`-style file, NOT
from `.listenerlog`.

## Area 3 — Whisrs Recall UI

### Correction to the premise: it is Fuzzel, not Noctalia QML

The brief says the Whisrs recall UI lives "in Noctalia (QML)". Observed facts
contradict that:

- `whisrs-recall` is a standalone Rust CLI binary. `Mod+Alt+V` spawns
  `${whisrs}/bin/whisrs-recall` directly (`dictation.nix:341-345`); it does not
  route through Noctalia/QuickShell.
- The selection UI is **fuzzel `--dmenu`**. `packages/whisrs/default.nix:75-80`
  wraps `whisrs-recall` with `fuzzel` + `wl-clipboard` on PATH.
  `skills.md:130`: "`Mod+Alt+V` opens `whisrs-recall`, a Fuzzel-backed selector".
- Noctalia has NO recall component: `rg -i recall` across
  `noctalia-dev/noctalia-shell` and all CriomOS-home QML returns nothing. The
  active Noctalia plugins are only `listener-level` and `whisrs-level` bar
  widgets (`~/.config/noctalia/plugins/`). Noctalia's role for dictation is the
  microphone-level bar widget, not recall.

### Structure and data source (from `whisrs/src/recall.rs` + `recall/main.rs` at pinned rev `c32c8bcf`)

`whisrs-recall` CLI (`src/recall/main.rs`):

- flags: `-n/--limit` (default 20), `--history <path>`, `--selector` (default
  `fuzzel`), `--selector-arg`, `--copy-command`, `--copy-arg`, `--print`.
- default fuzzel args (`recall.rs SelectorCommand::fuzzel()`): `--dmenu --prompt
  "whisrs> " --width=120 --with-nth=2 --accept-nth=1 --match-nth=2 --only-match`.

Flow:

1. read `history.jsonl` newest-first up to `limit` (`crate::history`);
2. build rows `<index>\t<preview>` where preview is the transcript flattened to
   one line, capped `MAX_PREVIEW_CHARS = 160`;
3. pipe rows to the selector; fuzzel shows column 2 (preview) but returns column
   1 (index) via `--accept-nth=1`;
4. copy the FULL selected transcript to the clipboard (default native clipboard;
   `--copy-command` overridable), and optionally `--print` to stdout.

Its data source is exactly the Whisrs `history.jsonl` schema
(`{timestamp,text,backend,language,duration_secs}`). The `whisrs-recall` smoke
check (`checks/whisrs-recall/default.nix`) pins this exact contract: fuzzel arg
order, the tab-separated `index<TAB>flattened-text` rows, and that timestamps are
not shown to the user.

Note for implementers: the recall source is on the `criomos`-branch whisrs fork
pinned in `flake.lock` (`whisrs-src` rev `c32c8bcf`, `owner LiGoldragon`); the
local `/git/github.com/LiGoldragon/whisrs` checkout (`af25e63`, v0.1.11) does NOT
contain `src/recall*` or the `whisrs-recall` bin. Read the pinned rev, not the
local working copy.

### Three reuse options

(a) Reuse the Whisrs `whisrs-recall` binary directly. It is parametrizable:
`whisrs-recall --history <listener-history.jsonl> --selector-arg ...` would work
IF Listener writes the identical JSONL schema. Fastest path, zero new UI code.
Downsides: hard-couples Listener's UX to the Whisrs binary and its `whisrs> `
prompt branding; forces Listener to emit Whisrs's exact `HistoryEntry` shape;
couples two independently-versioned tools across a fork boundary. The prompt
string is not currently a flag (only `--selector-arg` lets you override the whole
arg vector), so branding would need the full fuzzel arg vector passed in.

(b) Extract a shared selection crate used by both. Cleanest long-term dedupe, but
neither tool has a shared crate today and `whisrs-recall` lives in the upstream
whisrs fork; extraction means cross-repo coordination and a new shared component.
Highest effort, out of proportion to a ~120-line selector.

(c) Listener-owned recall equivalent with the same UX. Add a small Listener
transcript history store (Area 2) plus a `listener-recall` selector (mirror the
~120-line `recall.rs`: read Listener's history newest-first, `index\tpreview`
rows, fuzzel `--dmenu` with the same nth flags, copy full text). Self-contained,
typed, and owned by the component that produces the data.

### Recommendation

**Option (c), a Listener-owned recall**, with option (a) as an acceptable
interim if speed is the priority.

Rationale:

- The workspace component discipline (micro-components / component-architecture:
  a component owns its own capability surface, typed storage) favors Listener
  owning both its transcript history and its recall selector rather than
  depending on the Whisrs binary and its history schema at runtime.
- The recall selector is small (fuzzel dmenu + JSONL read + clipboard copy);
  duplicating it inside Listener is cheaper than a cross-repo shared-crate
  extraction (b) and avoids the fork-coupling of (a).
- It keeps Listener and Whisrs independently versionable, matching how the two
  tools are already kept separate (separate services, separate binds, separate
  Noctalia level widgets), and lets Listener carry its own metadata (session id,
  start time) natively.
- Interim (a) is viable only if Listener first writes the identical Whisrs JSONL
  schema; that constraint alone argues for owning the format, i.e. (c).

Either way, the UI is a fuzzel dmenu spawned from a niri bind — no Noctalia/QML
work is required for recall.

## Observations vs Interpretations

Observations (backed by file:line / command output above): the niri bind lines
and their actions; the collision scan result; `.listenerlog` binary audio format;
clipboard-only delivery; absence of any transcript-text persistence on disk and
in source; the Whisrs `history.jsonl` schema and `whisrs-recall` fuzzel flow; the
binding check assertions.

Interpretations: that recall "needs a new store but is additive/small" (the text
exists at stop; only persistence is missing); that option (c) is the best reuse
choice (a judgment against workspace component discipline, not a hard constraint);
that `Mod+M` is safe because niri has no implicit binds (niri requires explicit
binds, but I did not exhaustively audit every niri version default — see unknowns).

## Unknowns And Not Checked

- I did not fully trace the generated NOTA `Display` of `Output::Stopped` to
  confirm the exact stdout text shape of the transcript (only that
  `transcript_text` is a field in the printed reply and the CLI prints the whole
  reply). If the wrapper-capture recall option (Area 2 alternative) is pursued,
  confirm the precise projection in `signal-listener/src/schema/lib.rs` before
  relying on shell parsing.
- I did not verify niri's own built-in/hardcoded shortcut table for any implicit
  `Mod+M`; I relied on niri's explicit-bind model and the empty config scan.
  Low risk but not proven by a niri-internal source read.
- I did not read transcript text, clipboard contents, or audio contents, and did
  not run transcription or any live capture. Capture files were listed by
  name/size only.
- I did not run `nix flake check` or build the checks; the required check edits
  in Area 1 are inferred from reading the assertions, not from a failing build.
- I did not claim any paths or edit anything (read-only scout). Implementers must
  claim `dictation.nix` and `checks/listener-dictation-bindings/default.nix`
  before editing, and coordinate with any active CriomOS-home worktree
  (`CriomOS-home-listener-zddv4`, `CriomOS-home-laptop-colemak-merge` exist).

## Blockers

None for scouting. The one hard dependency for the feature: the recall UI needs a
Listener transcript history store that does not exist yet — that store (Area 2)
must be built before or alongside the `Mod+Alt+M` recall bind, or the bind will
spawn a selector with no data.
