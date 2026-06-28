# Handover — Spirit intent boundary & removal rework

## Intent

- Spirit holds the psyche's durable intent and direction only. Technical detail is not intent. Content explaining what Spirit is, what it is for, or how to use and interpret it is not intent either — that is manual material; the boundary rule itself is likewise manual material, not a record.
- Concrete matter — code, an architecture, a specification or mechanism, a manual entry, or a tracked task — belongs written in the repository, not stored in the intent database. Spirit is for intent; the repository is for matter. Each piece of matter goes to its proper home: architecture, manual, beads, or code.
- Far more misplaced (non-intent) content sits in the store than has been found so far; all of it must be found and moved to its proper home.
- Disposition is aggressive: a record mixing a directive with matter goes out whole, and the genuine directive kernel is then re-added as fresh, clean intent.
- Misplaced records are physically deleted (rows gone), not merely hidden.
- The guardian enforces this boundary at admission and must be aware of the intent to keep these kinds of data out of Spirit. Its operational rule lives in the guardian prompt; the manual states it for humans; the two stay in sync.
- The guardian must not gate garbage collection. There is exactly one physical-deletion path: `CollectRemovalCandidates`, on the meta socket, with no guardian. The working-socket `Remove` is removed. `Retire` remains as the guardian-gated act that nominates a record for removal.
- The boundary's guardian rejection reason is named `Matter` — deliberately general, not tied to any single destination.

## Useful context

- The daemon rework implementing the above is built and reviewed across three repos on `spirit-removal-rework` branches. signal-spirit 0.9.0 and meta-signal-spirit 0.2.0 are landed on their mains and pass full `nix flake check`. spirit 0.18.0 is not landed — its branch tip sits on the origin bookmark `spirit-removal-rework`; spirit origin `main` is still `c75da6aa`. spirit's changes: `CollectRemovalCandidates` moved to a meta-socket-only, guardian-free op; the working-socket `Remove` deleted; the guardian admission boundary plus the `Matter` reason added (admission-only — it does not touch the retirement path or existing records); the guardian-journal schema bumped v4 to v5 so an upgrading daemon cleanly orphans the old audit journal (intent records untouched; only the guardian audit history resets); and a CollectRemovalCandidates meta-socket boundary test added.
- The live daemon is untouched: version 0.16.0, 1383 records, durable marker (4477 12948372490860446260). Nothing is deployed and no record data has been mutated.
- Deletion is recoverable: `CollectRemovalCandidates` archives each record to a live `.archive.sema` sibling store before removing it.
- Deploy path once spirit lands on main: in CriomOS-home, bump the spirit flake input, remove the hand-written `guardian-alignment.conf` drop-in (or it pins the old build), rebuild and activate the home generation, then restart `spirit-daemon.service` — a full, workspace-wide Spirit outage for the restart. Verify afterward that it reports 0.18.0 with 1383 records intact.
- Later phases, each a separate step: physically delete the displaced records (mark them Zero certainty, then run `CollectRemovalCandidates`, which also clears about 739 already-Zero records); re-add the genuine directive kernels as clean intent; then the broad sweep to find and migrate all remaining misplaced content.
- Design and scope detail: `reports/legacy-disposition/1-Design-spirit-removal-rework-scope.md`.

## Open decisions

- Before spirit can build or deploy, the flake's offline-vendoring must be reconciled with its `Cargo.toml`. Several direct LiGoldragon git deps are not wired into the offline vendoring, so a fresh build fails in the no-network nix sandbox. `signal-persona` is fixed (committed). The `mentci` family — `mentci`, `meta-signal-mentci`, `signal-mentci`, and transitive `mentci-lib` — is still un-vendored and is non-optional, so it blocks the daemon build itself. This is pre-existing rot (base main has it too; cached builds masked it). Decision: run a complete vendoring sweep (find every un-vendored LiGoldragon git dep; check for a vendoring generator before hand-adding), or drop `mentci` if it is being retired.
