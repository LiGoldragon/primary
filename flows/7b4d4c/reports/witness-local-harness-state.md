# Witness: local harness state

**Method.** Direct filesystem inspection executed 2026-09-04 via Bash commands:
`find`, `git remote get-url origin`, `git log -1`, directory listings,
`readlink -f`, `file`, `cat` of Nix package files and Curriculum skill sources.
No simulated or inferred state. Each finding is stated with its command or path.

---

## 1. Repositories carrying harness or persona work

**Single clone root found:** `/git`. No other clone roots exist under `~`, `~/Projects`, `~/src`, `~/code`, or `~/repos`.

**Method:** `find /git -maxdepth 3 -name ".git" -type d` then `find /git -maxdepth 4 -type d -name "*hijack*" -o -name "*harness*" -o -name "*persona*" -o -name "*nexus*"`.

### Named harness/persona/hijack repositories

All nine repositories below exist as initialized git directories under
`/git/github.com/LiGoldragon/`. Every one has no remote URL, no commits,
and no tracked files. The `git remote get-url origin` and `git log -1` commands
returned empty for each.

| Repository | Path | Remote | Last commit | Content |
|---|---|---|---|---|
| `claude-hijack` | `/git/github.com/LiGoldragon/claude-hijack` | none | none | empty |
| `codex-hijack` | `/git/github.com/LiGoldragon/codex-hijack` | none | none | empty |
| `harness` | `/git/github.com/LiGoldragon/harness` | none | none | empty |
| `signal-harness` | `/git/github.com/LiGoldragon/signal-harness` | none | none | empty |
| `meta-signal-harness` | `/git/github.com/LiGoldragon/meta-signal-harness` | none | none | empty |
| `persona` | `/git/github.com/LiGoldragon/persona` | none | none | empty |
| `signal-persona` | `/git/github.com/LiGoldragon/signal-persona` | none | none | empty |
| `meta-signal-persona` | `/git/github.com/LiGoldragon/meta-signal-persona` | none | none | empty |
| `persona-spirit` | `/git/github.com/LiGoldragon/persona-spirit` | none | none | empty |

Five-line account, same for all nine: each directory registers as a git
repository (`git log` exits with "does not have any commits" rather than "not a
git repo"), carries no tracked files, has no configured remote, has no commits,
and has no README. They are initialized placeholder shells with no content on
this machine.

### Other clone roots

`/git/depp.brause.cc/shackle` — the only other cloned repository found.
Its name does not match any harness, hijack, persona, or nexus pattern; not
further inspected.

---

## 2. Harness packaging and installation

**Method:** `readlink -f` on the `~/.nix-profile/bin/` symlinks; `file` and
string inspection of the resulting store paths; `cat` of
`/git/github.com/LiGoldragon/CriomOS-home/owned-agents/*/default.nix` and
`/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix`.

### Resolved executables

```
which claude  → /home/li/.nix-profile/bin/claude
              → /nix/store/84z2f0da7dnwpvnfny0k5k3cvcqzbjy4-claude-code-2.1.258/bin/claude

which codex   → /home/li/.nix-profile/bin/codex
              → /nix/store/9j5wqyh61gv4ywylqz0bblmss0ahrw62-codex/bin/codex

which pi      → /home/li/.nix-profile/bin/pi
              → /nix/store/ihhmcnadz9wz56appgjp38z2a4xmcwd9-pi-0.84.1/bin/pi
```

The `claude` store path is a makeWrapper-generated shell script calling
`.claude-wrapped` with `--argv0 claude` and injecting `bubblewrap` and `socat`
into PATH. It is not a renamed or persona-variant wrapper; it is the standard
Nix `wrapProgram` fixup.

### Claude Code

- **Nix source:** `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/claude-code/default.nix`
- **Package name:** `claude-code`; **executable:** `claude`
- **Version pinned:** `2.1.258` (read from `hashes.json` beside the derivation)
- **Source:** upstream binary fetched from `storage.googleapis.com/claude-code-dist-*`
- **Wrapper additions:** `DISABLE_AUTOUPDATER=1`, `DISABLE_INSTALLATION_CHECKS=1`,
  `DISABLE_NON_ESSENTIAL_MODEL_CALLS=1` (default); telemetry flags optional via
  `disableTelemetry` argument; `bubblewrap` and `socat` prepended to PATH

### Codex

- **Nix source:** `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/default.nix`
- **Package name:** `codex`; **executable:** `codex`
- **Version pinned:** `0.153.2` (from `hashes.json`)
- **Source:** built from source via `rustPlatform.buildRustPackage` from
  `github.com/openai/codex` tag `rust-v0.153.2`; `codex-cli` and
  `codex-code-mode-host` packages built
- **Wrapper additions:** `bubblewrap` bwrap binary linked into
  `$out/codex-resources/bwrap`; PATH prefixed with bubblewrap on Linux

### Pi

- **Nix source:** `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix`
- **Package name:** `pi`; **executable:** `pi`
- **Version pinned:** `0.84.1` (hardcoded in derivation)
- **Source:** built from `earendil-works/pi` monorepo via `buildNpmPackage`;
  multiple patches applied (skill-block completion, action-space, theme
  persistence)
- **Wrapper additions:** makeWrapper script sets `PI_PACKAGE_DIR` if unset;
  resolves `LINKUP_API_KEY` from gopass at runtime
- **Status:** the pi-models module (`modules/home/profiles/min/pi-models.nix`)
  carries the comment `# DEPRECATED — Pi is being phased out. Do not add new models or configuration here.`

### Local LLM (llama.cpp router)

- **Nix source:** `/git/github.com/LiGoldragon/CriomOS/modules/nixos/llm.nix`
- Node role: hosts designated `behavesAs.largeAi`
- Serves models via `llama-server` with a router on a configurable port;
  model inventory read from `criomos-lib/data/largeAI/llm.json`
- No harness executable; accessed as an OpenAI-compatible endpoint by Pi's
  provider config

### Named persona variants

No wrapper scripts or renamed executables for "Claude Light", "Claude
Unopinionated", "Codex Bare", or "Codex Unsafe" were found anywhere in
`/git/github.com/LiGoldragon/CriomOS-home`. The search covered all `.sh`
files and paths matching `*wrapper*`, `*light*`, `*unopinionated*`, `*unsafe*`,
`*bare*`, `*system-prompt*`, and `*persona*`.

---

## 3. agent-harness-packaging skill in Curriculum

**Path:** `/git/github.com/LiGoldragon/Curriculum/skills/agent-harness-packaging.md`

**Full text as found:**

```
---
description: An external manager for coding harnesses must be selected, packaged, installed, configured, or integrated.
dependencies: [nix-workflow]
---

Treat an external harness manager as distinct from the Claude or Codex harnesses it coordinates.

Obtain current release, packaging, installation, and integration facts from authoritative upstream sources before choosing or changing an integration.

Put durable packages and configuration in the declarative source that owns that environment.

Put a distinct reusable package in its own public package repository; a home-environment source consumes a pinned package output.

Give an agent manager a package and executable name that cannot collide with an unrelated existing package; StablyAI Orca is `orca-ide`, not GNOME `orca`.

Do not run an upstream integration installer that mutates a configuration Nix owns; express the intended configuration in its declarative owner.

Evaluation is not package proof: build the artifact and behavior-smoke every claimed CLI, GUI, and headless surface.
```

### Curriculum skills mentioning Claude Code, Codex, Pi, DeepSeek, or a harness by name

| Path | Line | Text |
|---|---|---|
| `skills/context-strata.md` | 20 | `interface is promoted from bottom to middle. Harness seizure:` |
| `skills/context-strata.md` | 23 | `What a given harness puts in each stratum is verified information,` |
| `skills/context-strata.md` | 26 | `Verified placements: Codex CLI 0.149.1 injects a $-mentioned skill's` |
| `skills/context-strata.md` | 29 | `is bottom. Claude Code lists the catalog in the base context and` |
| `skills/context-strata.md` | 34 | `Channels. A harness may tag the flow's own output with named channels` |
| `skills/context-strata.md` | 37 | `stratum. What a harness retains per channel is verified information:` |
| `skills/context-strata.md` | 38 | `for Codex CLI 0.149.1, commentary and final are both assistant-role` |
| `skills/vocabulary.md` | 12 | `Thread: one running model session and its context. A \`THREAD_ID\` identifies one thread in a harness.` |
| `skills/vocabulary.md` | 14 | `Transcript: the file the harness writes holding one thread from beginning to end.` |
| `skills/vocabulary.md` | 27 | `Base context: the harness-built portion of the top stratum — the instructions the harness itself composes ahead of everything authored here. Vendor parlance: system prompt.` |
| `skills/skill-designing.md` | 48 | `Target-specific text in a flat source uses \`{% if claude %}\`, \`{% if codex %}\`, or \`{% if pi %}\`, ...` |
| `skills/skill-designing.md` | 55 | `` `disable-model-invocation: true` in Claude Code and as`` |
| `skills/skill-designing.md` | 56 | `$-name-only injection in Codex.` |
| `skills/main-flow.md` | 22 | `{% if codex %}` |
| `skills/main-flow.md` | 23 | `Before the first flow artifact, run \`flow-id codex --flows-root\` with the explicit absolute flows root.` |
| `skills/agent-harness-packaging.md` | 2 | `description: An external manager for coding harnesses must be selected, packaged, installed, configured, or integrated.` |
| `skills/agent-harness-packaging.md` | 6 | `Treat an external harness manager as distinct from the Claude or Codex harnesses it coordinates.` |
| `skills/nix-input-upgrade.md` | 23 | `Patch interface changes silently across minor versions. A patch that applied cleanly at v0.80 may require rebase at v0.84 because the surrounding function signature changed (Pi v0.83 grew a new argument).` |
| `skills/subflow.md` | 7 | `Obtain the current \`THREAD_ID\` from the harness after launch.` |
| `skills/prompt-crafting.md` | 9 | `A prompt explains nothing the harness does automatically and nothing everybody knows; it carries only what the receiving flow would not otherwise have.` |

No Curriculum skill mentions DeepSeek by name.

---

## 4. context-strata skill

**Path:** `/git/github.com/LiGoldragon/Curriculum/skills/context-strata.md`

**Full text as found:**

```
---
description: Designing or implementing something that depends on where text enters an LLM's context. Almost never arises in ordinary task work.
dependencies: []
---

An LLM's context has three strata; a higher stratum outranks a lower
one. Text meant to bind must enter at the middle stratum or above.

Top stratum: the base context, and any text authored into its seat.
Universal invariants go here.

Middle stratum: the typed prompt, the entry files and other
system-reminder injections, skills loaded through the skill interface,
a subflow's brief from the main flow.

Bottom stratum: what the flow fetches or says itself — tool results, files it
opens, subflow reports, its own output. No authority.

Promotion: moving text up a stratum; a skill loaded through the
interface is promoted from bottom to middle. Harness seizure:
authoring the top stratum ourselves.

What a given harness puts in each stratum is verified information,
not read from docs.

Verified placements: Codex CLI 0.149.1 injects a $-mentioned skill's
body as a user-role message (middle) and lists the catalog, bodies
excluded, in a developer-role message; a skill the model reads by tool
is bottom. Claude Code lists the catalog in the base context and
injects a skill's body at the middle stratum by both paths — the typed
/command and the flow's own Skill-tool load; only a file read outside
the interface is bottom.

Channels. A harness may tag the flow's own output with named channels
(e.g. commentary, final). Channels are not strata; they are visibility
and retention tags on items in one position — the flow's output, bottom
stratum. What a harness retains per channel is verified information:
for Codex CLI 0.149.1, commentary and final are both assistant-role
messages distinguished only by a phase field, both replayed to the
model until compaction, both dropped after.
```

**Manifest or dependency declaration governing harness-tree generation:**
Curriculum's `ARCHITECTURE.md` (read in full) states the skill is pure data
consumed by the external `curriculum-deploy` runtime. No manifest exists within
Curriculum itself that names which harness trees receive `context-strata`. That
mapping lives in the `curriculum-deploy` repository, which is not cloned under
`/git` on this machine. The `dependencies: []` frontmatter field records
in-Curriculum skill-loading dependencies, not harness deployment scope.

---

## 5. Curriculum generation mechanism

**Method:** `cat /git/github.com/LiGoldragon/Curriculum/UPGRADES.md`,
`cat /git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md`,
`cat /git/github.com/LiGoldragon/Curriculum/README.md`.

Five-line summary:

1. Curriculum is a pure data repository: `skills/*.md` (38 sources) and
   `roles.datom`.
2. An external runtime — the public `curriculum-deploy` repository at validated
   revision `c64223acb7d38b53968b55701f2ded93e82587c1` — reads those sources
   and produces the `.agents/`, `.claude/`, `.codex/`, `.pi/` trees in
   consuming workspaces.
3. `curriculum-deploy` is not cloned on this machine; the generation command is
   not documented within Curriculum.
4. Per-harness differences in skill text are expressed in the flat skill sources
   using `{% if claude %}`, `{% if codex %}`, `{% if pi %}` conditional blocks
   (specified in `skills/skill-designing.md`); the runtime expands them
   per-target at deploy time.
5. UPGRADES.md explicitly prohibits using the retired Cargo, Nix, CLI, DOTOS,
   manifest, and generated-inventory surfaces that were formerly part of this
   repository.

---

## Contradictions with the 38dec9 remember

The 38dec9 remember (as relayed in the task brief) holds that no harness skill
or system-prompt repository exists.

Two contradictions are observed:

**Contradiction A — the skill exists.** The `agent-harness-packaging` skill is
present in the Curriculum source at
`/git/github.com/LiGoldragon/Curriculum/skills/agent-harness-packaging.md`.
Its description is "An external manager for coding harnesses must be selected,
packaged, installed, configured, or integrated." It is deployed into the working
`.claude/skills/` tree (confirmed by `ls /home/li/primary/.claude/skills/`
listing `agent-harness-packaging` among installed skills).

**Contradiction B — the named repositories exist as initialized shells.** Nine
repositories (`claude-hijack`, `codex-hijack`, `harness`, `signal-harness`,
`meta-signal-harness`, `persona`, `signal-persona`, `meta-signal-persona`,
`persona-spirit`) exist as git-initialized directories under
`/git/github.com/LiGoldragon/`. They are empty — no commits, no remote, no
content — so they carry no system-prompt, wrapper, or harness work at this
time. The 38dec9 remember's claim that no such repository exists does not match
the directory state on this machine; the directories are present, just
unpopulated.

**No contradiction** on named wrapper variants: no "Claude Light", "Claude
Unopinionated", "Codex Bare", or "Codex Unsafe" wrapper scripts or packages
exist anywhere in the inspected trees.

---

## Sources

- `find /git -maxdepth 3 -name ".git" -type d` — clone root survey
- `find /git -maxdepth 4 -type d -name "*hijack*" -o ...` — named-repo discovery
- `git remote get-url origin` and `git log -1` run inside each named repo path
- `which claude codex pi` and `readlink -f` on each result
- `file /nix/store/84z2f0da7dnwpvnfny0k5k3cvcqzbjy4-claude-code-2.1.258/bin/claude` and string inspection — wrapper type
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/claude-code/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/claude-code/hashes.json` (version via python3)
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/owned-agents/codex/hashes.json` (version via python3)
- `/git/github.com/LiGoldragon/CriomOS-home/packages/pi/default.nix`
- `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/pi-models.nix`
- `/git/github.com/LiGoldragon/CriomOS/modules/nixos/llm.nix`
- `grep -rn "claude\|codex\|\bpi\b" /git/github.com/LiGoldragon/CriomOS{,-home} --include="*.nix" -l` — Nix file survey
- `find /git/github.com/LiGoldragon/CriomOS-home -name "*.sh" -o -name "*wrapper*" -o -name "*light*" ...` — wrapper/persona search
- `/git/github.com/LiGoldragon/Curriculum/skills/agent-harness-packaging.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/context-strata.md`
- `/git/github.com/LiGoldragon/Curriculum/skills/skill-designing.md`
- `grep -rn -i "claude code\|codex\|\bpi\b\|deepseek\|harness" /git/github.com/LiGoldragon/Curriculum/skills/`
- `/git/github.com/LiGoldragon/Curriculum/ARCHITECTURE.md`
- `/git/github.com/LiGoldragon/Curriculum/UPGRADES.md`
- `/git/github.com/LiGoldragon/Curriculum/README.md`
- `ls /home/li/primary/.claude/skills/` — installed skill list
