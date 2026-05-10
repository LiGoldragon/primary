# Skill — speech-to-text interpreter

*Decoding STT-transcribed prompts that contain workspace-specific
words.*

---

## What this skill is for

Li often dictates prompts through a speech-to-text tool. The
tool sometimes transcribes workspace-specific words
(repository names, library names, programming-language tokens)
incorrectly, because they're not in its dictionary or because
they collide with common English. When you read a prompt that
contains a phonetic-near-miss for a known workspace word,
**guess the intended word**, act on the guess, and only ask if
the guess turns out to be wrong.

The tool itself lives in the **CriomOS-home** repo (one of this
workspace's repos). Read CriomOS-home's `skills.md` /
`ARCHITECTURE.md` for the specific tool, model, and any
configuration. Don't name the vendor or model in this skill —
that drifts; the repo is canonical.

---

## How to read STT output

1. **Read for intent first.** STT errors are almost always at the
   word level, not the structural level. The grammar usually
   survives even when individual nouns get mangled.
2. **When a word looks suspicious**, check it against the table
   below before treating it as English.
3. **When the user pronounces a name** that *sounds* like a
   word in the table but the transcript shows the word itself
   (e.g. "ASCII" appearing where you'd expect a project name),
   default to the project. The STT often "corrects" a real
   project name into a familiar English word.
4. **Don't ask the user to spell things out** — when they
   dictate a spelling, the STT will sometimes auto-correct it
   anyway. Instead, look up the canonical spelling on the
   filesystem (workspace `repos/` symlink index, or
   `RECENT-REPOSITORIES.md`).

---

## Canonical spellings live on the filesystem

When the user mentions a repository, the canonical spelling
**is the directory name** under
`/git/github.com/<org>/<repo>/`. The workspace's
`repos/` index (`<workspace>/repos/`) is symlinks to those
canonical paths. Read the directory name; don't reconstruct
spelling from the spoken form.

This rule applies recursively: any time you're unsure how a
project name is spelled, look at the directory.

---

## Table of common words and what they may have been

The **transcribed form** is what STT might emit; the **canonical
form** is the workspace's name for that thing. When you see the
transcribed form in a prompt and it doesn't make sense as
English, try the canonical form.

### Repositories (sema-ecosystem)

| Heard / transcribed as | Canonical |
|---|---|
| "Creom" / "Cree-ome" / "Krio" / "Criom" / "Cry-om" | **Criome** — the universal validator/coordinator daemon at the center of the sema-ecosystem; long-term replaces Git, code editor, SSH, web server, etc. Canonical written name is `Criome` (capital C, trailing `e`); filesystem path is lowercase `criome` per GitHub convention. |
| "Sema" / "Seema" | the canonical-store repo |
| "Nota" / "Nodda" | the text-format repo |
| "Nexus" | the request-language repo |
| "Signal" | the binary-IR repo (overlaps with the English word — context decides) |
| "Arca" / "Ar-ka" | the content-addressed-store repo |
| "Forge" | the executor repo (overlaps with the English word — context decides) |
| "Prism" | the projector repo (overlaps with the English word — context decides) |
| "Hexis" / "Hex-is" | the host-config-reconciler repo |
| "Lore" | the docs repo (overlaps with the English word — context decides) |
| "Workspace" | the workspace meta-repo |
| "ASCII" / "asci" / "askii" | the retired language-design repo (`aski`); the user pronounces the project name like the encoding |

### Repositories (system / tooling layer)

| Heard / transcribed as | Canonical |
|---|---|
| "Crio-OS" / "Creom OS" / "Krio-O-S" | the host-OS repo |
| "Crio home" / "Krio-home" | the home-manager repo |
| "Crio Emacs" | the Emacs config repo |
| "Lojix" / "Logix" / "Logics" / "Logic CLI" | the deploy CLI repo |
| "Horizon RS" / "Horizon Rust" | the horizon Rust crate repo |
| "Goldragon" / "Gold dragon" | the cluster-proposal repo |
| "Gascity" / "Gas city" / "Gas-city" | the orchestration repo (LiGoldragon fork) |
| "Mentci" / "Men-chee" / "Menchi" | the older-generation repo family |
| "The Book of Sol" / "Sol" / "Sole" | the writing-project repo |
| "Persona" | the operator's current scaffolding repo |

### Programming-language terms

| Heard / transcribed as | Canonical |
|---|---|
| "Rust" / "rust" | the Rust language |
| "Nix" / "Nicks" / "Nyx" | the Nix language / build system |
| "Cargo" | Rust's build tool / dependency manager |
| "Rkyv" / "ar-keev" / "Archive" (in a Rust context) | rkyv (binary serialization crate) |
| "Ractor" / "Reactor" (in a Rust+actor context) | ractor (the actor framework) |
| "Tokio" / "Toki-yo" | tokio (the async runtime) |
| "Serde" / "Sir-day" | serde (serialization) |
| "Thiserror" / "This error" | thiserror (error-derive crate) |
| "Anyhow" / "Eyre" | anyhow / eyre (forbidden in this workspace's Rust crates) |
| "Crane" / "Crain" | crane (Nix Rust packaging) |
| "Fenix" / "Phoenix" (in a Nix-toolchain context) | fenix (Rust toolchain in Nix) |
| "Blueprint" | numtide/blueprint (Nix flake layout helper) |
| "Flake" / "Flakes" | Nix flakes |
| "Nixpkgs" / "Nix packages" / "Nix peekages" | nixpkgs |
| "Home-manager" / "Home manager" | home-manager (Nix HM) |

### VCS and tooling

| Heard / transcribed as | Canonical |
|---|---|
| "Jujutsu" / "Jujitsu" / "JJ" / "Jay-jay" | jj (the version-control system) |
| "Dolt" / "Dolt SQL" | Dolt (git-for-data) |
| "Beads" / "BD" / "Bee-dee" | bd / beads (issue tracker) |
| "Anna's archive" / "Annas" | annas (Anna's Archive CLI) |
| "Linkup" | linkup (search CLI) |
| "Substack" | substack (publishing CLI) |

### Other workspace terms

| Heard / transcribed as | Canonical |
|---|---|
| "Ouranos" / "Uranus" | the user's primary node name |
| "Prom" / "Prometheus" | the binary cache server |
| "Polecat" / "Mayor" / "Refinery" / "Witness" | gas-city role names from the gastown pack |
| "Operator" / "Designer" | this workspace's lock-coordinated agent roles (Codex / Claude) |
| "ESSENCE" / "Intention" | the workspace's intent doc; see `~/primary/ESSENCE.md` |
| "Lock" / "Lockfile" | when adjacent to "operator" or "designer," means the coordination protocol; otherwise normal English |

---

## Caveats on specific entries

- **ASCII / aski lineage.** `aski/CLAUDE.md` formally disclaims
  aski as an ancestor of nota/nexus ("shared surface features
  are coincidence, not lineage" — Li, 2026-04-25). Li's lived
  sense is that aski's design instincts (delimiter-first, no
  keywords, position defines meaning, names are meaningful, no
  opaque strings) inspired the current work. Honor the lived
  sense in conversation; flag the formal disclaimer only when
  load-bearing.

---

## When the table doesn't help

If a transcribed word still doesn't fit any candidate after
checking the table:

1. List the workspace's repos: `ls ~/primary/repos/` or
   `<workspace>/RECENT-REPOSITORIES.md`. Many workspace-specific
   words are repo names; the directory listing is exhaustive.
2. List CLI tools on PATH: `compgen -c | sort -u`. Some
   workspace tools have phonetic-misheard names (`bd`, `jj`,
   `gh`).
3. If a candidate emerges, act on it and note the match in your
   reply so the user can correct if you guessed wrong.
4. Only if no candidate emerges, ask. Frame the question by
   listing the closest matches you considered, so the user
   doesn't have to think from scratch.

---

## How to keep this skill current

This table is workspace-state — it grows as new repos and
libraries land. When you encounter a new STT mishearing in
practice that isn't in the table, add the row before continuing.
Per the workspace's autonomous-agent skill, that is a routine
edit; commit and push.

---

## See also

- `autonomous-agent.md` — when to act on a guess vs ask.
- `skill-editor.md` — how to edit this and other skills.
- CriomOS-home's `skills.md` — the specific STT tool's setup
  (model, configuration, where it runs).
- the workspace's `RECENT-REPOSITORIES.md` — the authoritative
  list of repo names with canonical spelling.
