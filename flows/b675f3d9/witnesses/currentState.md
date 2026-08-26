# Current state witness — b675f3d9

Scope: topics touched by f426777b (2026-08-25/26).
Date probed: 2026-08-26.

---

## 1. ethos-monolith

Method: probe `git -C /git/github.com/LiGoldragon/ethos-monolith log -5 --oneline`
Method: probe `git -C /git/github.com/LiGoldragon/ethos-monolith status --short`
Method: probe `grep -rn "sema.ethos|nexus.ethos|triplet|sema|nexus" /git/github.com/LiGoldragon/ethos-monolith/src/`

Head (top 5):
  b273030 Generate signal wire consumers only
  cc3ee32 format and lint generated Rust
  41cc747 flatten one-field named carrier bodies
  d4eae92 keep emitted contract warnings clean
  101ae25 document embedded Ethos values

Dirty: clean (no modified or untracked files).

Top-level layout: AGENTS.md, ARCHITECTURE.md, Cargo.lock, Cargo.toml, checks,
CLAUDE.md, fixtures, flake.lock, flake.nix, README.md, result, src, target,
tests, UPGRADES.md.

Triplet contract: no matches for "sema.ethos", "nexus.ethos", or "triplet" in src/.
One incidental hit on "semantic" in fixture/mod.rs (doc comment). The generator
now takes signal-only input; sema and nexus sources are gone.

---

## 2. signal-orchestrate and meta-signal-orchestrate

Method: probe `git -C /git/github.com/LiGoldragon/signal-orchestrate log -3 --oneline`
Method: probe `find /git/github.com/LiGoldragon/signal-orchestrate -name "*.ethos"`
Method: probe `git -C /git/github.com/LiGoldragon/meta-signal-orchestrate log -3 --oneline`
Method: probe `find /git/github.com/LiGoldragon/meta-signal-orchestrate -name "*.ethos"`

signal-orchestrate head:
  88cc01e Generate Orchestrate wire from signal Ethos only
  d23fb64 Verify Ethos output from Cargo OUT_DIR
  3de1c5d Generate Orchestrate PathLock wire contract from Ethos
.ethos files: ethos/signal.ethos only.

meta-signal-orchestrate head:
  d4dd208 Own Orchestrate Nexus storage configuration
  2b3ec7c Generate MetaOrchestrate wire from signal Ethos only
  ebefb65 Verify Ethos output from Cargo OUT_DIR
.ethos files: ethos/signal.ethos only.

Both wire repos carry exactly one .ethos file (signal.ethos); nexus.ethos and
sema.ethos were removed as part of the repair done in 01a03952.

---

## 3. Orchestrate Nexus

Method: probe `git -C /git/github.com/LiGoldragon/orchestrate log -3 --oneline`
Method: code read /home/li/primary/flows/01a03952/log.md
Method: code read /home/li/primary/flows/01a03d6e/log.md

Head:
  a4d8f7d Record live Curriculum progress
  5b49542 Start Orchestrate Nexus from XDG defaults
  6dea26f Release Orchestrate Nexus

01a03952 summary (5 lines):
  Repaired ethos-monolith to signal-only generation (0.4.0); removed nexus/sema
  sources from both wire repos (signal-orchestrate 0.16.2, meta-signal-orchestrate
  0.10.2). Proved Orchestrate 0.22.0 `live_nexus` against both wire releases in a
  disposable consumer. Wire releases pushed; authoritative Orchestrate not changed.
  Edit-coordination skill proposal drafted (spartan PathLock/PathLockRelease).

01a03d6e summary (5 lines):
  Orchestrate 0.23.0 pushed at commit 6dea26f; seven remote CI checks green.
  Home remains unedited and unpinned: deployment revealed a missing startup Signal
  frame producer (no bootstrap binary wanted; Nexus carries a default config constant).
  Meta Configure must accept new values; ordinary-socket Configure deferred.
  Nexus skill may now change; downstream chain IDs and authorization remain open.

---

## 4. Authored skill roster

Method: probe `ls /git/github.com/LiGoldragon/Curriculum/skills/`

Full roster (alphabetical):
  agent-harness-packaging, beads, behavior, breaking-upgrades, context-strata,
  design, disk-hygiene, documentation-placement, edit-coordination,
  feature-development, file-editing, flows, lojix, main-feature-integration,
  nexus, nexus-rationale, nix-input-upgrade, nix-workflow, operating-system,
  prompt-crafting, psyche, psyche-acquisition, psyche-distillation, psyche-grasp,
  psyche-interraction, realization, repository-lifecycle, secrets, skill-designing,
  spirit, subflows, testing, transcript-search, versioning, vocabulary.

protos, ethos, datom, protos-rationale: NOT present. The skill family proposed
in f426777b has not been created yet.

---

## 5. Flows after f426777b touching ethos / orchestrate / protos / datom

Method: code read /home/li/primary/flows/index.md (lines after f426777b entry)

Relevant entries (short id + description):
  01a038b5 — Migrate the curriculum stack from Dotos to Datom (datom)
  01a03952 — Remember 01a03603; propose edit-coordination skill for orchestrate
              Nexus; repair Ethos source misplacement in ethos-monolith and wire
              repos (ethos, orchestrate)
  01a03d6e — Remember recent orchestrate work; situation summary; plan and execute
              deployment; Nexus skill changes (orchestrate)
  b675f3d9 — Remember f426777b; assemble vision on ethos and ontology/anatomy-based
              design; show psyche high-level view (current flow, ethos)

---

## 6. Primary repo git state

Method: probe `git -C /home/li/primary log -3 --oneline`
Method: probe `git -C /home/li/primary status --short`

Log:
  d505f7786 flow: preserve X11 direction
  9c9a1b350 flow: record ChatGPT freeze diagnosis
  c1dd903a2 Record Nexus configuration boundary

Status:
   M flows/index.md
  ?? flows/b675f3d9/
