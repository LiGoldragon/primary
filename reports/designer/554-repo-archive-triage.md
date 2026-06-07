# 554 — repo archive triage

designer, 2026-06-07. Verified read-only classification of all 150 repos under
`/git/github.com/LiGoldragon` (workflow `wiynk57oi`, 6 readers, each grounded in
the repo's README / INTENT / Cargo / last-commit against `active-repositories.md`).
Result: **96 keep, 26 archive candidates, 28 the psyche's call.**

**Status 2026-06-08:** archived on GitHub (reversible via `gh repo unarchive`) —
the 26 clear candidates (the `spirit-next` entry was only a local symlink, dropped)
plus `workspace` and `mentci-tools`, for **27 repos archived**. Verified live and
KEPT: `orchestrator` (Gas City cascade dispatcher, a production flake input),
`signal-executor` (shared request-execution library four daemons use),
`mentci-lib` and `mentci-egui` (the real upcoming-GUI repos). Follow-up:
`CriomOS-emacs` still references `aski-core` and `vscode-aski` (dead aski editor
inputs) — they still resolve read-only, but are cleanup candidates.

## Archive candidates (26) — clear

### Dead aski-language cluster (11)
The aski language is dead by the psyche's own word ("aski is dead," "aski was the
wrong way"), superseded by NOTA / nexus. The whole compiler pipeline goes with it:

| Repo | What it is |
|---|---|
| `aski` | the language spec; its last commit quotes "aski is dead" |
| `askic`, `askicc`, `aski-cc` | aski compilers (frontend / bootstrap / macro) |
| `aski-core`, `corec`, `veri-core`, `synth-core` | rkyv contract-type crates for the pipeline |
| `veric` | aski verifier; own status: "STALE — Triply Broken" |
| `semac` | old `.sema` generator backend of the aski pipeline |
| `vscode-aski` | VSCode extension for the dead language |

### Named `-archive` repos (3)
`criomos-archive`, `lojix-archive`, `nexus-spec-archive` — literally named
`-archive`; superseded content.

### Superseded renames / `-next` concepts (6)
| Repo | Superseded by |
|---|---|
| `spirit-next` | a symlink to the live `spirit` checkout (same HEAD) — just drop the alias |
| `horizon-next` | the live `schema-next` / `schema-rust-next` stack (2-commit concept) |
| `schema-core` | the live `schema-next` (2-commit cross-import witness) |
| `sema-upgrade`, `signal-sema-upgrade`, `owner-signal-sema-upgrade` | the live upgrade triad (`upgrade` / `signal-upgrade` / `meta-signal-upgrade`) |

### Dead stubs / superseded experiments (6)
| Repo | Note |
|---|---|
| `ndi` | single 2023 commit, an NDI-SDK installer script |
| `arbor` | 3-commit content-addressed tree, superseded by `arca` |
| `noesis`, `noesis-schema` | capnp-v1 era, "will be rewritten in aski" (dead) |
| `domainc` | stale proc-macro in the veric/semac pipeline (not `domain-criome`) |
| `kameo-testing-assistant` | retired `-assistant` lane duplicating `kameo-testing` |

## Your call (28) — not obviously dead; archival is yours

Personal / creative projects, third-party tools, or ambiguous — not archived on
my judgment.

- **Personal / creative (15):** `AnaSeahawk-website`, `ArtificialIntelligence`,
  `awesome`, `BookMaker`, `BookOfLuna`, `TheBookOfGoldragon`, `webpage`, `wiki`,
  `library`, `kibord`, `qmkBinaries`, `Armbian-RockPi4B-NixOS`, `maisiliym`,
  `astro-aski`, `pi-delegate`.
- **Third-party / external tools (7):** `annas-mcp`, `atom`, `kameo` (the vendored
  actor framework), `whisrs`, `hexis`, `persona-pi`, `mentci-tools`.
- **Workspace tooling, possibly superseded (6):**

| Repo | Note |
|---|---|
| `workspace` | older meta-repo overlapping `primary`'s role heavily — likely superseded by `primary` |
| `brightness-ctl` | `chroma` says it "replaces the brightness shell wrappers" — confirm chroma fully covers it |
| `substack-cli`, `WebPublish`, `test-city`, `signal-forge` | working tools / scaffolds not in the active map |

## Three the names lied about — verified to KEEP

Verifying instead of guessing caught three that name-matching alone would have
wrongly archived:

- **`orchestrator`** — not a stale dupe of `orchestrate`; it's the Criopolis
  cascade dispatcher, a live flake input in production `CriomOS-home`.
- **`signal-executor`** — not superseded by `nexus`; it's a live shared
  triad-daemon executor library (`upgrade`, `persona-spirit`, `repository-ledger`,
  `orchestrate` depend on it), refreshed today.
- **`signal-persona`** — `active-repositories.md` calls it a "retired shim," but
  its README was corrected today confirming it's canonical. The active map is
  stale here.

## Keep (96)

The live Persona / Sema / Signal / Nexus / NOTA / schema stack, production Stack A
(`CriomOS*`, `horizon-rs`, `lojix-cli`, `goldragon`), and the `signal-*` /
`meta-signal-*` / `owner-signal-*` contract triads.

## Open question — the archive mechanism

"Archive" needs a defined action: GitHub archive-flag the remotes, move them to an
archive location/org, or rename to `<name>-archive` (the existing pattern). These
are code repos with GitHub remotes, so the actual archiving is an outward,
operator-lane action — designer identifies, you and operator execute.
