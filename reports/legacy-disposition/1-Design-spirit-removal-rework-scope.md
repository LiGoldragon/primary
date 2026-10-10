---
variant: Design
topic: spirit
title: spirit removal-rework scope
date: 2026-06-27
component: spirit 0.16.0
status: scoped, not implemented
---

# Spirit removal-rework — implementation scope

Cross-agent design pickup point. The design is DECIDED (do not re-litigate);
this report nails the exact change surface, deploy mechanism, and safety
preconditions so an implementation team can execute. A clean-context agent can
start from here.

## The decided design (restated for context)

1. **`CollectRemovalCandidates` (CRC) becomes a single META-socket op with NO
   guardian.** It archives + physically removes the matching exact-Zero-certainty
   records. Today it is a working-socket op routed through Nexus as a guarded
   effect; it must become a clean meta-plane op mirroring the existing
   `Import`/`Configure` meta ops, guardian fully out of its path.
2. **Delete the working-socket `Remove` op entirely** (the hard-delete-no-archive
   path) and every guardian reference to it. After this, CRC on meta is the ONLY
   physical-deletion path.
3. **Reprogram the guardian ADMISSION prompt** to add a subject-matter boundary:
   content describing what Spirit IS / how to use or interpret it / its technical
   mechanism is MANUAL material, not durable intent — rejected at admission with
   an aggressive lean (borderline → out).

## Repos and live facts

- Daemon: `/git/github.com/LiGoldragon/spirit` — version **0.16.0**, on `main`
  (`mvwqknmr 8480eeb3`). Working contract `Input`/`Output` (with `Remove` and
  `CollectRemovalCandidates`) is **imported from `signal-spirit`**, re-exported
  via `src/lib.rs`. Meta contract (`Configure`/`Import`) is **imported from
  `meta-signal-spirit`**, re-exported via `src/lib.rs:70`. Both contracts are
  pinned `git ... branch = "main"` (Cargo.toml:167-168) — not a tag.
- Working contract: `/git/github.com/LiGoldragon/signal-spirit` — version **0.8.0**.
- Meta contract: `/git/github.com/LiGoldragon/meta-signal-spirit` — version **0.1.0**
  (Input heads `[Configure Import]` only).
- Storage schema version: **10** (`src/store/mod.rs:75`
  `SPIRIT_SCHEMA_VERSION = SchemaVersion::new(10)`). This rework does NOT change
  the storage layout — no migration needed.
- Live daemon: systemd USER service `spirit-daemon.service`, running a
  hand-deployed side build of 0.16.0 via a drop-in override (see C).
- Guardian prompt markdown is `include_str!`-compiled (`src/guardian_prompt.rs:390-407`)
  — every prompt edit needs a **rebuild**, not just a redeploy.

## A. Exact code surface

The wire enums are schema-generated from `.schema` files. `signal-spirit/schema/signal.schema`
owns the working `Input`/`Output`; `meta-signal-spirit/schema/meta-signal.schema` owns the
meta `Input`/`Output`; the daemon's own `schema/nexus.schema` + `schema/sema.schema` (with their
hand-maintained mirror modules `src/schema/nexus.rs` + `src/schema/sema.rs`) own the internal
NexusEffectCommand / SemaWriteInput surfaces. All three layers ripple.

### Change 1 — CRC → meta op, no guardian

CRC currently routes through the WORKING plane as a guarded Nexus effect. The
**store primitive is already correct and is reused unchanged**:
`Store::collect_removal_candidates` (`src/store/mod.rs:607-649`) archives each
matching record into the SEPARATE archive DB, THEN retracts from the live log,
per-record skip on archive failure. C1 only changes how that primitive is reached.

Edit sites:
- **`meta-signal-spirit/schema/meta-signal.schema`** — add a `CollectRemovalCandidates`
  input verb (line-7 `[Configure Import]` list), a `RemovalCandidatesCollected` output verb
  (line-8 list), and the request/receipt type wiring, mirroring `Import`/`ImportReceipt`.
  The payload types `RemovalCandidateCollection` / `RemovalCandidatesCollection` already
  live in `signal-spirit` and are importable. Regenerate `src/schema/meta_signal.rs`.
  **Wire-contract change → version bump (see D).**
- **`src/meta_transport.rs`** — add a `collect_removal_candidates(...)` convenience method
  mirroring `configure` (lines 68-73). The `MetaInput` enum itself comes from the contract
  re-export (line 22) — nothing hand-written here besides the method.
- **`src/daemon.rs:193-196`** — add a third arm to the two-arm meta `match input`:
  `MetaInput::CollectRemovalCandidates(request) => engine.collect_removal_candidates_async(...).await,`.
- **`src/engine.rs`** — add `pub fn collect_removal_candidates(&mut self, request) -> MetaOutput`
  + an `_async` wrapper, mirroring `Import` (`import`/`import_async` at 672-697) and `Configure`
  (`configure`/`configure_async` at 522-569 / 661-663). It calls
  `self.nexus.store().collect_removal_candidates(...)` directly — no guardian, no
  Signal→Nexus→SEMA pipeline. `&mut self` gives the EngineActor-serialized exclusivity
  Configure/Import already rely on.
- **Delete the guardian block on the CRC path:** `src/nexus.rs:926-934` — the
  `#[cfg(feature="agent-guardian")] { let operation = GuardianOperation::collect_removal_candidates(...); match self.guard_model(operation) {...} }`. (Lines 935-943, the store call + result build, move into the engine meta op.)
- **Remove CRC from the working routing:** `src/nexus.rs:1239-1241`
  (`Input::CollectRemovalCandidates => command_effect(...)`) and `src/daemon.rs:233`
  (subscription_filter arm).
- **Remove CRC from the working effect set:** `src/schema/nexus.rs:247` (NexusEffectCommand
  variant), the impl/From sites (1125-1137, 2056-2058), the `collect_removal_candidates`
  constructor (1708-1709), and `schema/nexus.schema:65,82,85,105`. CRC also leaves the
  working `signal-spirit/schema/signal.schema` Input/Output lists (44-45, 73).
- **Delete CRC's guardian user-message render:** `src/guardian_prompt.rs:382-385`. Also the
  `guardian_records_for_operation` CRC arm `src/store/mod.rs:925-928` (harmless if left — only
  builds a bundle — but should be removed for cleanliness). The `GuardianOperation::CollectRemovalCandidates`
  variant in `guardian_journal.rs` (43, 106-108, 124, 153) can stay if CRC is still journaled, or be
  dropped if the meta op is not journaled — **implementer decision** (see E).

### Change 2 — delete working `Remove`

This is broad and mechanical. `Remove` is a working `Input` variant whose effect runs the
**hard-delete-no-archive** path: guarded `guard_remove` → `Store::remove_record` →
SEMA `remove`. Delete the whole chain.

Wire/schema:
- **`signal-spirit/schema/signal.schema`** — drop `Remove` from the `Input` list (44),
  `RecordRemoved` from `Output` (45), `Remove` from `OperationKind` (217), and the type defs
  `Remove Removal` (67) + `RecordRemoved RemoveReceipt` (90). **Breaking wire-contract change → bump.**
- **`schema/sema.schema`** — drop `(Remove)` from `WriteInput` (27), `(Removed)` from `WriteOutput`
  (41), and defs at 29/43.
- **`schema/nexus.schema`** — drop `(Remove)` from `CommandSemaWrite` (54), `(GuardRemove)` from
  `NexusEffectCommand` (65), `(Removed)` from `NexusEffectResult` (85), defs at 56/77/98.
- **`src/schema/sema.rs`** — ~16 sites: WriteInput `Remove` variant (67) + struct (88) + impl
  (385-397), WriteOutput `Removed` (175) + struct (197) + impl (575-588), constructors (827, 864-865),
  From impls (931-933, 1001-1003), route enums + arms + names (1307/1319/1379/1392/1470/1488).
- **`src/schema/nexus.rs`** — ~14 sites: CommandSemaWrite `Remove` (142) + struct (163) + impl
  (726-739) + From (1846-1848) + constructor (1605); NexusEffectCommand `GuardRemove` (242) + struct
  (346) + impl (1030-1043) + From (2021-2023) + constructor (1692); NexusEffectResult `Removed` (423)
  + struct (537) + impl (1410-1423) + From (2161-2163) + constructor (1757-1758).

Runtime:
- **`src/nexus.rs`** — `CommandSemaWrite::Remove` lowering (246), `GuardRemove` apply arm (494-505),
  both `guard_remove` cfg variants (724-742), `Input::Remove` routing (1205-1216),
  `SemaWriteOutput::Removed → record_removed` (1265-1267), `NexusEffectResult::Removed → record_removed` (1370-1372).
- **`src/store/mod.rs`** — SEMA `SemaWriteInput::Remove` apply arm (194-204, the hard delete),
  `remove_record` (1038-1043), `guardian_records_for_operation` Remove arm (911-917). The low-level
  `remove(...)` helper (1024) is still used by `collect_removal_candidates`, so it STAYS.
- **`src/guardian_journal.rs`** — `GuardianOperation::Remove` variant (41), constructor (98-100),
  testimony arm (122), candidate_entries (drop from 138-139), name arm (151).
- **`src/daemon.rs:227`** — `Input::Remove(_)` subscription_filter arm.

Guardian prompt + docs:
- **`src/guardian_prompt.rs:371-376`** — `GuardianOperation::Remove` user-message render.
- **`checklist.md`** — drop `Remove` from Gate 1's op list (line 3), Gate 2's remand list (line 4),
  Gate 10's remand list (line 10). `few-shot.md` has NO Remove example — untouched by C2.
- **`src/guardian_prompt.rs:489`** + the `assembled_system_prompt_names...` test (480-497) — update the
  expected remand-list marker string once the checklist drops `Remove`.
- **Documentation ripple (not wire):** the daemon's own `INTENT.md` (lines ~123, 135) and
  `ARCHITECTURE.md` restate the `Remove` remand catalogue and the SEMA-apply `Remove` surface —
  update alongside. The workspace `skills/spirit-cli.md` and `skills/intent-maintenance.md` also
  describe `Remove`; coordinate those edits per `versioning` (skill prose is the runtime help surface here).

### Change 3 — guardian admission subject-matter boundary

Prompt-only edits (plus the gloss in Rust), all behind `include_str!` → rebuild required. No wire change
IF the implementer routes the new boundary through the existing `NonIntent` / `InsufficientWarrant`
reasons (recommended). A NEW rejection reason variant (e.g. `ManualMaterial`) would instead be a
wire-contract change (the `GuardianRejectionReason` enum, `MODEL_REASONS` array at
`guardian_prompt.rs:62-79`, the exhaustive `admission_gloss` match, reply parsing) — **flag this as the
one open design choice in C3** (see E).

Edit sites (lead-identified, verified):
- **`src/guardian-prompts/record-shape.md`** — add the manual-vs-intent framing (line 3 carries the
  metadata/Zero-sentinel gloss; line 4 the Domain/Referent distinction — natural anchor).
- **`src/guardian-prompts/checklist.md`** — Gate 6 `SHAPE OF THE ARROW` / `NonIntent` (line 8) is the
  primary site for the subject-matter boundary with the aggressive lean; Gate 4 `DESTRUCTIVE-OP` (line 6)
  per the lead's note.
- **`src/guardian_prompt.rs:100-106`** — the `InsufficientWarrant` gloss; extend so mechanism/usage
  description reads as unwarranted-for-intent. (The `NonIntent` gloss at 117-120 is the alternative home
  if the boundary is framed as "manual material is not durable intent" — pick one and be consistent with
  the checklist gate chosen.)
- **`src/guardian-prompts/few-shot.md`** — counter the Accept examples that describe Spirit's own
  mechanism: **AA** (line 10, "guardian-policy record is High importance"), **AB** (line 11, "the guardian
  should keep testimony and reasoning separate"), and **C** (line 8, "whether the guardian should be one
  model or two"). Add a new Accept example for RETIRING manual-bound content. Keep all section markers
  intact — `assembled_system_prompt_includes_every_file_section` (guardian_prompt.rs:415+) asserts them.

## B. The archive — SAFETY GATE VERDICT: GREEN (archiving is live)

**Physical deletion is safe to enable on this daemon. Not a blocker.**

Evidence:
- The archive target is owner-configured via the meta `Configure` op
  (`ConfigureRequest { ArchiveDatabaseTarget, SelectedMirrorTarget, SelectedCriomeGateTarget }`),
  stored on the Store (`Store::set_archive_target`, `src/store/mod.rs:368`). The type is
  `ArchiveDatabaseTarget = [Default | Path(ArchivePath)]`.
- **`Default` requires NO explicit config**: it resolves to a `<live-stem>.archive.sema` sibling next
  to the live store (`src/store/mod.rs:534-542`), and `Default` is the field's initial value
  (mod.rs:331, 473). The daemon's startup config rkyv carries ONLY socket/db/guardian/auth — archive
  target is NOT in startup; it defaults to the sibling.
- **The sibling archive DB exists and is actively capturing on the live daemon.** Live state dir has
  `~/.local/state/spirit/spirit.archive.sema`, a real redb store **populated with archived intent
  records** (verified: it contains full archived Entry text). Its mtime is **byte-identical to the
  live store's** (both `2026-06-26 16:16:51`, same commit) — proving the archive path is live and
  being written in lock-step with the live log.
- **`Store::collect_removal_candidates` (mod.rs:607-649) archives BEFORE it retracts**, per record:
  `archive.archive_record(...)` → on `Ok` then `self.remove(...)`; on `Err` → `ArchiveFailed` skip,
  record stays in the live log. The same archive-then-retract pattern is also used by `retire`,
  `clarify`, and other ops (mod.rs:1051/1132/1176/1236), so the archive substrate is shared and
  well-exercised. The archive DB opens at the same `SPIRIT_SCHEMA_VERSION` (10) as the live store.

Caveat the implementer should keep in mind: `Default` archiving writes to a LOCAL sibling file, not a
mirror repo or the criome target. `SelectedMirrorTarget` / `SelectedCriomeGateTarget` are separate
meta-config knobs; whether off-host durability (mirror/criome) is also wanted before bulk deletion is a
policy question for the psyche, but it is NOT required for the archive-before-retract safety property —
that property holds with the live local sibling, which is verified active.

## C. Build + deploy/restart procedure + downtime

- The spirit flake (`/git/github.com/LiGoldragon/spirit/flake.nix`) exposes packages only
  (`default`/`cli`/`daemon`/`configuration-writer`/`render`/`store-migration`/`trace`/...), no
  nixosModule/homeManagerModule (its `nix/` dir is empty). `daemonPackage` = `--features
  agent-guardian --bin spirit-daemon`. The startup config rkyv is written by the
  `spirit-write-configuration` binary, NOT by a derivation in this flake.
- **The systemd unit + the config derivation live in CriomOS-home:**
  `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/spirit.nix`. It takes
  `spiritPackage = inputs.spirit.packages.${system}.default`, builds a `runCommand
  "spirit-daemon-configuration"` (`daemonConfiguration`) that runs `spirit-write-configuration`
  with an inline NOTA request (socket `~/.local/state/spirit/spirit.sock`, meta socket
  `meta-spirit.sock`, db `spirit.sema`, DeepSeek-Pro guardian agent, 180 s timeout), and defines
  `systemd.user.services.spirit-daemon` with `ExecStartPre = spirit-startup-state` (mkdir + stale-sock
  cleanup + `spirit-migrate-store`), `ExecStart = ${spiritPackage}/bin/spirit-daemon
  ${daemonConfiguration}/spirit.config.rkyv`, `Restart=on-failure`, `RestartSec=2s`, and the 12
  `Conflicts=` legacy-unit retirement guards. Wired into the home-manager generation for user `li`.
- **The live process is a HAND-DEPLOYED side build, not the home-manager-generated ExecStart.** The base
  unit (`~/.config/systemd/user/spirit-daemon.service`) points at the CriomOS-home-locked spirit (input
  rev `0dec3710`); a hand-written drop-in `…/spirit-daemon.service.d/guardian-alignment.conf` resets
  ExecStart to a DIFFERENT 0.16.0 store path (a separate code build; config bytes byte-identical). Both
  are 0.16.0 — the store hash is the only discriminator. The currently-running build is also NOT the
  latest `main` tip. **A plain `home-manager switch` regenerates the base fragment but does NOT touch the
  drop-in, so the drop-in keeps winning until removed.**
- **Canonical rebuild + redeploy (push-first, per `nix-usage`; keep store paths in a variable):**
  1. In `spirit` (after landing the three contract bumps too): `jj commit -m '<msg>'`;
     `jj bookmark set main -r @-`; `jj git push --bookmark main`.
  2. In `signal-spirit` and `meta-signal-spirit`: land + push the bumped contracts to their `main` first
     (spirit pins them `branch=main`), so spirit rebuilds against the new wire.
  3. In `CriomOS-home`: `nix flake update spirit` (and the two contract inputs if pinned there),
     commit, push `main`. This re-evaluates `daemonConfiguration` (regenerating `spirit.config.rkyv`) and
     the unit's ExecStart store path.
  4. Build/activate the home generation from the pushed ref:
     `result=$(nix build --refresh --no-link --print-out-paths
     github:LiGoldragon/CriomOS-home/main#homeConfigurations.li.activationPackage)`, then activate
     (rewrites the base `spirit-daemon.service`).
  5. **Remove the manual drop-in** `guardian-alignment.conf` (or it overrides the fresh ExecStart);
     `systemctl --user daemon-reload`.
  6. `systemctl --user restart spirit-daemon.service` (ExecStartPre runs `spirit-migrate-store` against
     `spirit.sema` first; schema stays at 10, so it reports `Current` and does nothing).
- **Downtime: full, in-place, single-instance.** The daemon holds the redb/sema store AND all sockets
  (working `spirit.sock`, meta `meta-spirit.sock`, optional trace). A restart drops every connection —
  **every lane loses Spirit for the restart window** (socket teardown → migrate-store probe → engine
  reopen → socket rebind). There is NO blue-green / slot rotation in effect: the `Conflicts=` lines are
  retirement guards against the old `persona-spirit-daemon-vX.Y.Z` family, not an active slot mechanism.
  The single-writer engine forbids a second instance holding the store concurrently, so zero-downtime
  swap is not available as currently wired. (Do NOT restart during scoping — this report does not.)

## D. Versioning + repo workflow

Per `versioning`, four version surfaces; this rework moves three of them:

| Surface | Crate / artifact | Move | Why |
|---|---|---|---|
| Wire — working contract | `signal-spirit` 0.8.0 | **→ 0.9.0** (minor; breaking pre-1.0) | C2 removes `Remove`/`RecordRemoved`; C1 removes working CRC variants — breaking the wire vocabulary. |
| Wire — meta contract | `meta-signal-spirit` 0.1.0 | **→ 0.2.0** (minor) | C1 adds the `CollectRemovalCandidates` input + `RemovalCandidatesCollected` output verbs. |
| Component | `spirit` 0.16.0 | **→ 0.17.0** (minor) | New meta operation root + removed public working op + admission behavior change; it consumes both changed contracts (versioning: bump the daemon when it consumes a changed contract). |
| Storage schema | `SPIRIT_SCHEMA_VERSION = 10` | **unchanged** | No table layout change — CRC and Remove only route differently; the archive sibling and live store keep schema 10. No migration step. |

Guardian journal schema (`GUARDIAN_JOURNAL_SCHEMA_VERSION = 4`) is unaffected unless C1 changes how/whether
CRC is journaled (E).

Branch shape (per `feature-development` + `main-next` — these are CODE repos under `/git`, NOT primary):
- This is a multi-repo arc across three repos with breaking inter-crate wire changes, so it wants a
  **feature branch in worktrees**, same branch name across all three repos (e.g.
  `spirit-removal-rework`), cut under `~/wt/github.com/LiGoldragon/<repo>/spirit-removal-rework/`. Do NOT
  check the feature branch out in the canonical `/git` checkout.
- Land order (producers before consumers): `signal-spirit` + `meta-signal-spirit` first (the contracts),
  then `spirit` (the consumer), then the `CriomOS-home` flake-lock bump. Within each repo, the designer
  line is `next` and the operator integrates to `main`; spirit pins `branch=main`, so the contract bumps
  must reach each contract's `main` before spirit rebuilds green.

## E. Risks / unknowns / sequencing notes

1. **`branch=main` contract pinning is fragile.** spirit pins `signal-spirit` and `meta-signal-spirit`
   by `git branch=main` (not a tag) — `contract-repo`'s named anti-pattern. During the arc, spirit's
   build floats on whatever is on each contract's `main`. Sequence the landings so spirit only rebuilds
   after both contracts are green on their `main`, or the build breaks mid-arc. Consider pinning a rev
   for the deploy lock.
2. **C3 open design choice: reuse a reason vs add `ManualMaterial`.** Routing the manual-vs-intent
   boundary through existing `NonIntent`/`InsufficientWarrant` is prompt-only (no wire change, just a
   rebuild). Adding a dedicated `ManualMaterial` rejection reason is cleaner semantically but is a
   wire-contract change (the `GuardianRejectionReason` enum + `MODEL_REASONS` + exhaustive
   `admission_gloss` + reply parsing) and another contract bump. **Decide before implementing C3** — the
   prompt says "add a subject-matter boundary," not "add a reason," so reuse is the lighter reading.
3. **CRC journaling fate (C1).** When CRC leaves the guarded working path, does it stay in the guardian
   journal as a `GuardianOperation` (audit-only), or drop out entirely? If it drops, remove the
   `GuardianOperation::CollectRemovalCandidates` variant + arms in `guardian_journal.rs` (43, 106-108,
   124, 153). If audit is still wanted, keep them but feed the journal from the meta op. Minor, but pick
   one.
4. **Deploy gotcha — the drop-in must be removed.** The live daemon runs a hand-deployed side build via
   `guardian-alignment.conf`. A clean redeploy of the rework MUST delete that drop-in, or it will keep
   pinning the running process to the old build regardless of the new home-manager generation. Easy to
   miss; it is the single most likely deploy failure.
5. **Restart is workspace-wide downtime.** Every lane loses Spirit during the restart. Schedule the
   restart deliberately; there is no zero-downtime path with the current single-instance wiring.
6. **Archive durability is local-sibling by default.** The verified-live archive is a local
   `spirit.archive.sema` sibling. If the psyche wants off-host durability (mirror repo / criome) before
   enabling bulk deletion, that is a separate meta `Configure` of `SelectedMirrorTarget` /
   `SelectedCriomeGateTarget` — not required for the archive-before-retract safety property, but worth a
   one-line confirmation with the psyche.
7. **Witness tests will move.** `architectural-truth-tests` and the prompt-assembly tests
   (`guardian_prompt.rs` 415-497) assert section markers and the remand-list strings; C2/C3 break those
   expectations and must update them in the same change. The triad witness for meta-vs-working socket
   rejection should gain a case that CRC is now meta-only and rejected on the working socket.
8. **Skill/doc surfaces are part of the change, not a cleanup.** `skills/spirit-cli.md`,
   `skills/intent-maintenance.md`, spirit's `INTENT.md` and `ARCHITECTURE.md` all describe `Remove` and
   the working CRC; per `versioning` these are the runtime-help/intent surfaces and update in the same
   arc.
