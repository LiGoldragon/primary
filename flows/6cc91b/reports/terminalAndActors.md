# Terminal, actors, and Slint

## 1. Herder

No such thing exists anywhere searched: `/git` (all owners), `/home/li/primary`,
`/home/li/.nix-profile`, `/home/li/.config`. Every hit for "herder" outside
primary's own flow records is coincidental (test fixtures in rust-lang/rust,
a nixpkgs maintainer name, oxeylyzer text corpus) — none is a project.

Within primary, "Herder" appears only as spoken words, never as a built
thing:
- `flows/6cc91b/vision/nexus.md:7` — "should we just use Herder, because that
  was glitchy?"
- `flows/34d94e/log.md:60` — same utterance, fuller context (STT capture).
- `flows/564f55/reports/postOutage.md:110` — "not Herder or Agent Intercom"
  (named as something to avoid, in a different sense).
- `flows/6cc91b/reports/today.html:106` — a prior audit already flagged this
  exact gap: *"Who is 'Herder'? Named tonight as a possible alternative to
  the Python injector. Nothing in the record carries that name."*

So: say so plainly. Herder is not a repo, package, crate, or binary on this
machine. It is a name spoken twice (once by STT) with no referent built.
Nearest real candidates for "efficient abduco-style attach with message
injection," in order of how close they already sit to the living's ask:

- **abduco** (`/home/li/.nix-profile/bin/abduco`; upstream source mirrored at
  `/git/github.com/martanne/abduco`) — the actual program the living named.
  Raw byte-stream client/server around a PTY: `MSG_CONTENT` packets over a
  Unix socket, attach/detach/resize/exit only, no escape-sequence parsing.
  terminal-cell's own ARCHITECTURE.md (§1.2) cites it as "the concrete
  reference" for its data plane.
- **dtach** — not installed, not present in `/git`; older, narrower
  abduco ancestor, not worth chasing given terminal-cell supersedes it.
- **tmux control mode** (`/home/li/.nix-profile/bin/tmux`) — present and
  installed, but heavier (full terminal multiplexer, screen model) than what
  the living asked for ("super efficient kind of abduco").
- **The Claude daemon attach route**, `flows/024bc7/tools/claude_inject.py` —
  closest thing to "inject messages" running today. Speaks the Claude Code
  daemon's own control-socket protocol (`~/.claude/daemon/control.key`,
  `cc-daemon-<uid>/*/control.sock`), attaches, types keystrokes (bracketed
  paste + CR) into a live session. Python, PTY-attach-then-type, not an
  actor, not a message-passing API — the "asynchronicity ... made it
  impossible" ancestor `vision/nexus.md` refers to; the living already said
  "I don't want to use Python."

Conclusion: **terminal-cell is already the "Herder backend for now"-shaped
thing** — the real, built, tested equivalent of what "Herder" gestured at,
minus the name. There is no separate Herder to adopt or reject.

## 2. terminal-cell

Source: `/git/github.com/LiGoldragon/terminal-cell/ARCHITECTURE.md`,
`src/`, `tests/`, `git log`.

**What it does today.** A `terminal-cell-daemon` owns one child process group
and one PTY for the session's lifetime, behind two separate Unix sockets:
`control.sock` (Signal control-plane + byte-tag CLI: `terminal-cell-send`,
`-capture`, `-wait`, `-exit`, `-resize`) and `data.sock` (raw bidirectional
byte plane for `terminal-cell-view`, the visible viewer). Plane isolation is
enforced and tested: an attach on `control.sock` is rejected before any
bytes move, and vice versa. It is marked "the active terminal primitive for
V1 harness work, including Claude/Codex tests" (ARCHITECTURE.md §0); the
sibling `terminal` repo is explicitly archived/inactive in its favor.
Version 3.0.1 as of the latest commit (`9cab87c`), actively developed
(commits through 2026-09-12).

**Its own process actor.** Yes — `TerminalCell`, a Kameo actor
(ARCHITECTURE.md §1.4, §"Actors"), owns state that lives across time:
transcript truth, worker-lifecycle, prompt-pattern registration, wait
conditions. Load-bearing design point: the actor mailbox is kept *off* the
hot viewer path on purpose — "Live viewer bytes (`data.sock`) never traverse
a Kameo actor mailbox" — precisely so actor overhead doesn't cost latency.

**Message injection.** Yes, explicitly designed for it. `TerminalInputPort` +
`TerminalInputWriter` is "the writer plane that owns the input gate."
Keyboard bytes from an attached viewer arrive there tagged `Viewer`;
programmatic input enters the *same* port tagged `Programmatic` — one PTY
writer, one gate, two byte sources, arbitrated, not raced. That is a strict
superset of what `claude_inject.py` does by typing into a raw pty: injection
here is a first-class, gated, source-tracked control-plane operation, not a
keystroke simulation.

**vs. abduco, on the living's stated criterion (efficient attach + message
injection).** terminal-cell is abduco's model (single PTY, single owning
daemon, attach/detach, raw byte plane, no escape parsing on the hot path —
ARCHITECTURE.md names abduco as "the concrete reference") *plus* the two
things abduco cannot do: (1) a typed control plane (`signal-terminal`) for
resize/prompt-pattern/wait/injection as structured requests rather than
socket-fd tricks, and (2) an arbitrated programmatic-injection path that
coexists with a live human viewer without the human's bytes and the program's
bytes stepping on each other. Plain abduco has no such gate — two writers to
its socket just interleave. So: terminal-cell is not "should we build our own
abduco," it already is one, extended exactly where the living's ask points
(injection, its own actor). No reason surfaced in the sources to prefer raw
abduco over it for this project.

## 3. The forked actor library

**Which library.** Kameo (`kameo = { git =
"https://github.com/LiGoldragon/kameo.git", rev = "f491b45d..." }`), forked
at `github.com/LiGoldragon/kameo` from upstream `github.com/tqwewe/kameo`.
Confirmed by grep across every `Cargo.toml` under `/git/github.com/LiGoldragon/*`
(terminal-cell, criome, chroma, clavifaber, ethos-engine, harness, introspect,
lojix, logos-engine, mentci, mind, persona, repository-ledger, router,
sema-storage, system, terminal, triad-runtime, upgrade, kameo-testing — 19
consumer repos). "Cameo" in the living's speech is confirmed STT drift for
Kameo (`terminal-cell` commit `599a6fe use Kameo lifecycle fork` and
`bd1defd Pin kameo at the rev triad-runtime already carries` are the two
commits that put the fork into terminal-cell).

**The fork's divergence.** Merge-base with upstream `main`:
`4d2e2d0` (upstream, version 0.20.0 at that point). Six of our own commits
sit on top:
- `1325f6a` actor: publish terminal lifecycle outcomes
- `da0f64a` actor: split lifecycle control mailbox
- `1980e34` actor: cover lifecycle control edge cases
- `8ea1e3f` actor: gate weak shutdown result helpers
- `f491b45` fix lifecycle fork after upstream rebase (mechanical repair only)
- `3486e4f` docs: mark Protos estate status (unrelated housekeeping)

Net effect (git show --stat across the four substantive commits): new types
`ActorTerminalOutcome`, `ActorTerminalReason`, `ActorStateAbsence` on
`WeakActorRef`/`ActorRef`; a split lifecycle-control mailbox distinct from
the message mailbox in `mailbox.rs` (the single biggest diff, +838/-261 in
one commit); ~1000 lines of new coverage in `tests/lifecycle_phases.rs`. No
commit body explains "why" beyond the one-line subject; the shape (publish a
terminal outcome, gate a weak-ref shutdown result, split the control
mailbox) reads as: give callers a reliable, queryable answer to "did this
actor actually stop, and how" without racing the regular mailbox — exactly
the property a PTY-owning daemon actor (terminal-cell's `TerminalCell`) or a
persona-lifecycle actor would want. One branch name corroborates this intent
directly — `persona-spirit`'s `Cargo.toml` points at fork branch
`persona-lifecycle-terminal-outcome` — but that branch is not present in the
local git mirror to inspect further.

**Currently unconsumed.** Grepping every `LiGoldragon/*/src` tree for the
fork's new symbols (`ActorTerminalOutcome`, `ActorTerminalReason`,
`ActorStateAbsence`) finds them nowhere outside `kameo` itself: 19 repos pin
the fork revision, but none yet calls the lifecycle-outcome API it added —
pure surface area with no realized caller.

**Upstream since the fork point.** 51 commits on `upstream/main` past the
merge-base, taking upstream from 0.20.0 to released 0.22.2 (2026-07-17) with
further unreleased commits through `1b6bffb` (2026-09-13, "fix: serialize
supervised restarts"). Of those, several land in the *same* territory our
fork extended by hand:
- `#360` **BREAKING**: `ctx.pipe`/`ctx.pipe_with` for pipe-to-self
- `#362` reject new messages after `stop_gracefully` instead of silently dropping
- `#363` `on_undelivered` hook for messages left in the mailbox at terminal stop
- `#364` deliver leftover tells to `on_undelivered` when the restart budget is exhausted
- `#359` **BREAKING**: return pending ask's message as `ActorRestarting`/`ActorNotRunning` during drain
- `#365` **BREAKING**: make `ActorRef` cloning a single `Arc` clone
- `#387` (unreleased) fix: serialize supervised restarts
(Source: `CHANGELOG.md` at `upstream/main`, primary page —
github.com/tqwewe/kameo, and local `git log` on the fetched `upstream`
remote.)

**Which of our changes upstream may have made unnecessary.** Upstream's
`on_undelivered`/`stop_gracefully` rejection (#362/#363/#364) and drain
signaling (#359) now give a stock, supported way to know what happened to
messages an actor never processed before dying — conceptually adjacent to
our `1325f6a`/`da0f64a` "publish terminal lifecycle outcomes" / "split
lifecycle control mailbox" hand-built work. Whether upstream actually covers
the specific "did this actor's OS-level resource (PTY, socket) finish
tearing down" question our fork answers isn't determinable from the
changelog alone — needs a real diff/API read. Recommendation: diff
`ActorTerminalOutcome`/`ActorStateAbsence` against `on_undelivered` +
`ActorRestarting`/`ActorNotRunning` before further fork maintenance, since
the fork is unconsumed and every unreleased upstream commit is growing
rebase cost for zero realized benefit.

**"A new prodigy"?** No. `LukaOber/kameo` turned up in search but is a
0-star personal fork of `tqwewe/kameo` with no documented divergence, not a
new project. `tqwewe/kameo` remains the live upstream already being tracked.

**Rust actor-library landscape, September 2026** (grading: primary page /
snippet / inference; source for all bullets below: search summary of
tqwewe.com/blog/comparing-rust-actor-libraries and
github.com/tqwewe/actor-benchmarks — **snippet**, none independently opened):
- Kameo, Actix, Coerce, Ractor, Xtra remain the field's named contenders.
- Actix: fastest messaging/spawn, but async support "an afterthought."
- Kameo/Coerce/Ractor: similar message-passing performance, Tokio-based;
  Coerce and Ractor emphasize distribution.
- Xtra: runtime-agnostic (async-std/smol/Tokio/wasm-bindgen).
No primary page (docs.rs/crates.io/README) was opened to confirm current
version numbers for Actix/Coerce/Ractor/Xtra — only Kameo's own repo was
read directly; treat the above as **inference-adjacent** pending that read.

## 4. Slint

**Used anywhere under `/git`?** No. `grep -rn slint` across every
`LiGoldragon/*/Cargo.toml` returns nothing. Unity/Criome's Slint client does
not exist as code yet — it is vision only (`flows/6cc91b/vision/criome.md`).

**Current state**, from slint.dev / github.com/slint-ui/slint (primary
pages):
- Latest release **1.17.1**, 2026-07-07 — a bugfix patch
  (github.com/slint-ui/slint/releases, primary page).
- License: dual model — "a royalty-free permissive license for desktop,
  mobile, and web development, and a support-inclusive perpetual-fallback
  license for long-term maintenance," by SixtyFPS GmbH — **snippet** of
  slint.dev, not re-read line-by-line this pass.
- Platforms: Linux, Windows, macOS desktop; STM32-class microcontrollers
  embedded; Android/iOS supported today **for Rust specifically** (not yet
  scheduled for C++/JS/Python) — **snippet**, slint.dev/mobile + GitHub
  discussion #10425. iOS had an NLnet-funded push targeting 2026-08-01
  completion (nlnet.nl/project/SlintiOS) — **snippet**. WebAssembly/browser
  exists but is experimental — **snippet**.
- Sandbox / process model / host-runtime question: **not answered by sources
  found this pass** — a gap, not a "no." Nothing in slint.dev's public pages
  or release notes describes a Linux sandbox or host-runtime expectation;
  needs a targeted read of Slint's platform/backend docs
  (github.com/slint-ui/slint `docs/`, or "Backends & Renderers").

Sources: github.com/slint-ui/slint/releases (primary), CHANGELOG.md at
slint-ui/slint master (primary), slint.dev/mobile (snippet),
github.com/slint-ui/slint/discussions/10425 (snippet),
nlnet.nl/project/SlintiOS (snippet), github.com/tqwewe/kameo (primary,
cloned + fetched locally), github.com/LukaOber/kameo (fetched directly),
tqwewe.com/blog/comparing-rust-actor-libraries (snippet, search summary).
