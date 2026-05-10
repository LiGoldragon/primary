# 103 — Kameo wave landed

*Designer report. Closing record for the Kameo runtime switch.
Operator/103 (drift correction) settled what NOT to build; this
report names what DID land in the wave that followed.*

---

## 0 · TL;DR

The workspace runtime default switched from direct `ractor` to
**Kameo 0.20**. Six designer beads (primary-jfr, primary-5lm,
primary-585, primary-95c, primary-s5j, primary-m9u) closed in
sequence; one stale ractor adoption bead (primary-186) closed as
superseded. Two follow-up beads filed (primary-gyg, primary-jsi).

What landed:

| Where | What |
|---|---|
| `/git/github.com/LiGoldragon/kameo-testing` | New repo. crane+fenix Nix flake. 26 tests across 9 files (lifecycle/messages/spawn/mailbox/registry/supervision/streams/links/topology). All green under `nix flake check`. |
| `~/primary/skills/kameo.md` | New workspace skill — Kameo 0.20 usage in this workspace. Covers core shape, module map, lifecycle hooks, messages/replies (with the `tell`-of-fallible-handler trap), spawn variants, supervision, mailbox, registry, streams, links, anti-patterns. Every claim cited against kameo-testing. |
| `~/primary/skills/autonomous-agent.md` | New top-level section *"Active beads — check first, work them through"*. Names the `bd ready --label role:<role>` session-start check, the `role:<role>` label convention, the 7-step bead flow, and how user-prompt vs active-bead conflicts resolve. |
| `~/primary/skills/actor-systems.md` | §"What this skill is for" + §"Rust shape" rewritten — Kameo as runtime default; `Self IS the actor` shape replaces the ractor `behavior marker + State` split; per-kind `Message<T>` rule; `tell`-of-fallible-handler trap surfaced. |
| `~/primary/skills/rust-discipline.md` | §"Actors: logical units with kameo" — renamed and rewritten. Declarative supervision via `RestartPolicy`/`SupervisionStrategy`/`restart_limit`. ZST-actor anti-pattern row updated. *Handle pairing requirement retired (Kameo's `ActorRef<A>` is statically typed). |
| `kameo-testing/notes/findings.md` | Source-grounded research notes — defaults, module paths, spawn shapes, lifecycle traps, doc/source drift. Kept as the canonical reference behind the skill's claims. |

In flight (parallel, not designer's lane):

- **operator** holds `/git/github.com/LiGoldragon/persona` for *"migrate persona meta crate to kameo actor path"*.
- **operator-assistant** holds the seven persona-* runtime repos for *"kameo actor migration across persona runtime repositories"* (persona-mind, persona-router, persona-message, persona-system, persona-harness, persona-wezterm, persona-sema).
- **designer-assistant** holds `kameo-testing-assistant` for state-bearing-pattern + failure-supervision tests in a parallel repo (primary-7ph, primary-54f, primary-qjb, primary-eeg).

The architectural decision is the user's call from the prior turn:
*"if we should switch, we should switch as soon as possible"* —
applied. Persona-mind is small enough that the migration is
bounded; every additional ractor actor would have reinforced an
awkward shape that disagrees with `skills/actor-systems.md`'s
discipline.

---

## 1 · The new active-beads protocol

Embedded at the top of `skills/autonomous-agent.md`. Every agent
runs `bd ready --label role:<their-role>` at session start; if
results, that work outranks session-default behavior. The
user's direct prompt always wins, but in the absence of contrary
instruction the bead IS the workspace's continuing intent.

Corollary: when filing a bead for another role, tag with
`role:<that-role>` so it surfaces under their lane. Filing without
a role label hides the work from every role's session-start check
— it becomes background that no one is actively scanning for.

This is the workspace's primary mechanism for cross-session work
continuity. The Kameo wave used it end-to-end: six beads filed,
six closed, two new ones filed for follow-ups (primary-gyg,
primary-jsi), one stale bead retired (primary-186).

---

## 2 · Why Kameo, captured for future readers

The framework's shape agrees with the workspace's discipline.
Concretely:

| Workspace rule | Kameo native shape |
|---|---|
| Public actor nouns must carry data (`skills/actor-systems.md` §"Rust shape") | `Self` IS the actor; `Args = Self` is the documented common case |
| Verbs live on the data-bearing noun | All lifecycle hooks take `&mut self`; methods on the actor type directly |
| Typed mailbox per actor | `mailbox::bounded(64)` default; per-message `Message<T>` impls |
| Supervision is part of the design | Declarative `RestartPolicy` + `SupervisionStrategy` + `restart_limit(n, window)` |
| No shared locks | Message passing model; same as ractor — discipline-enforced |
| Push-only / no polling | Mailbox is the push channel; no scheduled wakeups by default |

Under direct ractor, the same rules required carve-outs ("framework
markers OK if private", "give State a domain name", "behavior on
State or reducers, not on the marker"). Under Kameo, no carve-outs
— the framework agrees with the discipline.

Migration cost was bounded: persona-mind has 9 real ractor actors
per designer-assistant/3; every additional ractor actor would have
been written in the awkward shape that needs unwinding later. The
cost grows nonlinearly with actor count. Switching now beat
switching at 90 actors.

---

## 3 · Open follow-ups

Filed:

- **primary-gyg** (P2, designer-assistant) — Investigate the
  on_panic-Continue semantics under `flavor = "multi_thread"`
  Tokio runtime. The `on_panic_continue_keeps_actor_alive` test
  was deliberately omitted from kameo-testing because under
  current_thread (the `#[tokio::test]` default) the surviving-actor
  path returns `ActorStopped` to subsequent asks — contrary to the
  documented behavior. The Kameo source shows the lifecycle loop
  continues on `Continue`, so multi_thread should fix it; verify
  and add the test back.
- **primary-jsi** (P3, system-specialist) — Create
  `lore/rust/kameo.md` as the tool reference, mirroring the lore↔primary
  split that existed for ractor (`primary/skills/actor-systems.md`
  is the architectural rule, `lore/rust/ractor.md` was the tool
  reference). With the kameo switch, the workspace skill is at
  `primary/skills/kameo.md`; the tool reference at
  `lore/rust/kameo.md` is still pending.

Not filed (left to the agents currently in flight):

- The persona-* runtime crates' actual migration to Kameo —
  operator-assistant's lane via `[primary-186]` superseded; the
  work continues without a new bead.
- designer-assistant's complementary kameo-testing-assistant repo
  + state-bearing-pattern test wave (primary-7ph and dependents) —
  designer-assistant's lane.

---

## See also

- `~/primary/skills/kameo.md` — workspace usage skill (the
  framework reference for this workspace).
- `~/primary/skills/actor-systems.md` — architectural discipline
  (what counts as actor-shape, no-blocking-handler, no-public-ZST).
  Updated this wave.
- `~/primary/skills/rust-discipline.md` §"Actors: logical units
  with kameo" — Rust style for actor code. Updated this wave.
- `~/primary/skills/autonomous-agent.md` §"Active beads — check
  first, work them through" — the new session-start protocol that
  surfaced this wave's beads to the next agent every time.
- `/git/github.com/LiGoldragon/kameo-testing` — falsifiable source
  for every Kameo behavior claimed in the skill.
- `~/primary/reports/designer/102-kameo-deep-dive.md` — the
  upstream research that motivated the switch.
- `~/primary/reports/operator/103-actor-abstraction-drift-correction.md`
  — the corrective report that retired `persona-actor` /
  `workspace-actor` and set the ractor-or-kameo decision back to
  the user; this wave is what "kameo, soon" looked like.
