# 145 — Component vs binary naming correction

*Mini designer report. Surface a naming inconsistency I
introduced across /143, /144, and a handful of ARCH docs:
calling the message component `persona-message-daemon` in
diagrams and prose where the bare component name
`persona-message` belongs. States the rule positively and
names every fix site.*

---

## 0 · The rule

Per `lore/AGENTS.md` §"Binary naming — `-daemon` suffix,
full English", the `-daemon` suffix is **binary-file-level
only**. It exists so daemon executables don't collide with
CLI executables at PATH level. It does **not** retag the
component anywhere else.

Symmetric across all six first-stack components:

| Layer | Mind | Router | System | Harness | Terminal | Message |
|---|---|---|---|---|---|---|
| **Repo / component** (diagrams + prose) | `persona-mind` | `persona-router` | `persona-system` | `persona-harness` | `persona-terminal` | `persona-message` |
| **`ComponentKind` variant** | `Mind` | `Router` | `System` | `Harness` | `Terminal` | `Message` |
| **Daemon binary file** | `persona-mind-daemon` | `persona-router-daemon` | `persona-system-daemon` | `persona-harness-daemon` | `persona-terminal-daemon` | `persona-message-daemon` |
| **CLI binary file** (where one exists) | `mind` | `persona-router` (daemon-client CLI) | `system` | — | `persona-terminal-view`, `-send`, `-signal`, … | `message` |
| **Socket file** | `mind.sock` | `router.sock` | `system.sock` | `harness.sock` | `terminal.sock` | `message.sock` |

**Where `-daemon` belongs**: `Cargo.toml`'s `[[bin]] name =
"<crate>-daemon"`, nix flake `apps.<crate>-daemon`, systemd
unit names, the `SpawnEnvelope.executable_path` field, the
`PERSONA_<CRATE>_DAEMON_EXECUTABLE` env var when one exists.
File-paths only.

**Where the bare repo name belongs**: every architecture
diagram, every prose reference to "the message component," the
flowchart node labels, the ARCH-document section headings, the
report TL;DRs.

The asymmetry I introduced — naming five components by their
repo name and one by its daemon binary — is the inconsistency
this report retires.

---

## 1 · Why the rule

Two reasons:

1. **Symmetry teaches.** A reader looking at a flowchart
   sees `persona-router → persona-harness → persona-terminal`
   and learns the component grammar from those three labels.
   Inserting `persona-message-daemon` in the same diagram
   forces the reader to learn a second grammar (daemon-tagged
   names) for no payoff.
2. **`-daemon` is doing real work elsewhere.** The suffix
   disambiguates the daemon **executable** from the CLI
   **executable** at PATH level (e.g., `mind` CLI vs.
   `persona-mind-daemon`). When the same suffix is sprayed
   across architectural prose, it loses that signal — readers
   start to think `-daemon` is part of the component name,
   and the disambiguation it earns at the binary layer
   evaporates.

---

## 2 · Fix sites

### 2.1 `/143` (prototype-readiness gap audit)

| Section | Current | Corrected |
|---|---|---|
| §1 flowchart node | `mday["persona-message-daemon<br/>(binds message.sock 0660)"]` | `mday["persona-message<br/>(binds message.sock 0660)"]` |
| §4.7 flowchart node | `daemon["persona-message-daemon"]` | `daemon["persona-message"]` |
| §4.8 actor topology — the actor `MessageDaemonRoot` stays (that's an actor name, not a component name) | — | (no change) |
| Prose mentions of "persona-message-daemon binary" | — | keep (those refer to the binary file specifically) |

### 2.2 `/144` (final cleanup after DA/36)

| Section | Current | Corrected |
|---|---|---|
| §0 TL;DR table referring to `persona-message-daemon` as the spawn-envelope-reading process | `persona-message-daemon` | `persona-message` (the daemon binary is `persona-message-daemon` — file-level only) |
| §2.1 Relation B endpoint label | `persona-message-daemon (sender)` | `persona-message (sender)` |
| §3.5 timestamp authority table | "`persona-message-daemon` mints..." | "`persona-message` mints..." |
| §4 Witness 2 narration | "persona-message-daemon receives, stamps..." | "persona-message receives, stamps..." |
| Prose mentions of "persona-message-daemon binary" | — | keep (those refer to the binary file specifically) |

### 2.3 `signal-persona-message/ARCH`

| Section | Current | Corrected |
|---|---|---|
| §"Channel" Relation A endpoint | `persona-message-daemon (receiver)` | `persona-message (receiver)` |
| §"Channel" Relation B endpoint | `persona-message-daemon (sender)` | `persona-message (sender)` |
| §"Channel" prose | "`persona-message-daemon` decodes the frame..." | "`persona-message` decodes the frame..." |
| §"Origin bridging" prose mentioning the daemon binary specifically | — | keep |
| §"Timestamp authority" row labeled `persona-message-daemon` | `persona-message-daemon` | `persona-message` |

### 2.4 `persona-message/ARCH`

| Section | Current | Corrected |
|---|---|---|
| §0 TL;DR mermaid node | `"persona-message-daemon"` | `"persona-message"` (in the flowchart) |
| §1 Component Surface bullet: "a `persona-message-daemon` supervised first-stack binary" | rename to: "a supervised first-stack daemon entry point (binary: `persona-message-daemon`)" | clarify the binary distinction |
| §1.5 daemon actor topology — the actor names (`MessageDaemonRoot`, `UserSocketListener`, `OriginStamper`, `RouterClient`, `SupervisionPhase`) are actor names, not component names; keep | — | (no change) |
| §4 Invariants: "The daemon reads its `signal-persona::SpawnEnvelope`..." | keep "the daemon" wording; this prose talks about the binary's behavior at startup | (no change; "daemon" as a noun is fine — it's the role) |
| Code Map entries `src/bin/persona-message-daemon.rs` | — | keep (file path) |

### 2.5 `persona-message/README.md`

| Section | Current | Corrected |
|---|---|---|
| Header paragraph "`persona-message-daemon` is the engine's user-writable ingress boundary..." | Either rewrite to "`persona-message` runs a long-lived daemon that binds the engine's user-writable ingress socket..." or keep with explicit "(binary: `persona-message-daemon`)" qualifier | clarify the binary distinction |

### 2.6 Operator bead `primary-devn`

References to "persona-message-daemon" in track descriptions
are about the binary being added; those are accurate and stay.
The component name in cross-cutting prose (e.g., "all six
first-stack daemons answer the supervision relation") should
use the bare component names.

---

## 3 · Witness / audit

A simple constraint witness for the workspace:

```text
component_name_in_diagrams_matches_repo_name
  — source-scan every `reports/designer/*.md` for the
    pattern `persona-<X>-daemon` in mermaid node labels and
    in component-reference prose. Allowed: file paths
    (Cargo.toml [[bin]], nix apps, executable_path,
    src/bin/), env-var names, systemd unit names, and
    explicit "(binary: ...)" qualifiers. Disallowed:
    diagram nodes and prose that refer to the supervised
    component itself.
```

Not blocking; designer-assistant can sweep when the report
backlog allows.

---

## 4 · What this report is not

- Not a scope change. The component is the same component.
- Not a rename. `persona-message-daemon` is still the right
  daemon binary file name; the rule just confines that name
  to file-level contexts.
- Not a workspace convention change. The convention in
  `lore/AGENTS.md` §"Binary naming — `-daemon` suffix"
  already says binary file names get the suffix; this
  report just names that I drifted past that rule in /143 +
  /144 and walks the drift back.

---

## See also

- `lore/AGENTS.md` §"Binary naming — `-daemon` suffix,
  full English" — the canonical rule this report applies.
- `~/primary/reports/designer/143-prototype-readiness-gap-audit.md`
  — diagrams + prose absorbed the inconsistency.
- `~/primary/reports/designer/144-prototype-architecture-final-cleanup-after-da36.md`
  — same.
- `/git/github.com/LiGoldragon/persona-message/ARCHITECTURE.md`
  — same.
- `/git/github.com/LiGoldragon/signal-persona-message/ARCHITECTURE.md`
  — same.
- bead `primary-devn` — track descriptions reviewed for the
  rule.
