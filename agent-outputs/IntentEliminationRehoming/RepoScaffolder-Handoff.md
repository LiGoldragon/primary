# Repo Scaffolder Handoff — INTENT elimination + orphaned schema-cc rehoming

Two independent finishing tasks. Both completed and fast-forward pushed; locks
were psyche-confirmed stale and no genuinely active concurrent work was found.

## Task and scope

- TASK 1: eliminate `INTENT.md` in `signal-criome`, folding its non-redundant
  direction into `ARCHITECTURE.md`, landing on `main` as a fast-forward while
  preserving the `criome-authorization-push` feature branch.
- TASK 2: re-home the one orphaned archived Spirit record routed to the retired
  standalone `schema-cc` repo into the live successor `schema-next`.

## Edit coordination

- `orchestrate "(Observe Roles)"`: no claim existed on either target path
  (active claims were on cloud / CriomOS-test-cluster / CriomOS, unrelated).
  Nothing stale to clear on the targets; claimed each path under lane
  `repo-scaffolder`, released after each task.
- Claim grammar note: `(Claim (<lane> [(Path <abs>)] <bare-reason-atom>))` —
  the path goes inside a `[...]` block; the reason is a bare atom (no brackets,
  no spaces). `(Release <lane>)` releases ALL paths held by the lane, so
  schema-next was re-claimed after the TASK 1 release.

## TASK 1 — signal-criome (/git/github.com/LiGoldragon/signal-criome)

### Pre-flight gate

- `main` and `main@origin` both at `wtkytpqv 5976b287` (clean FF base).
- Op log: last op 11h prior was a push of `criome-authorization-push`; the
  shared `@` was an empty no-description commit on top of that feature
  bookmark. No active concurrent work.
- `jj new main` based the work directly on `main`, leaving the feature commits
  (`kvrvpyxx`, `qusxnvup 2986f8f8`) on their own parallel line off main.

### INTENT elimination

- Compared `INTENT.md` (125 lines) against `ARCHITECTURE.md` (463 lines).
  All but two facts were already 100% present in ARCHITECTURE.md.
- Folded two non-redundant facts into `ARCHITECTURE.md`:
  1. Parked-authorization-snapshot approver queue shape (a parked entry carries
     either a policy `AuthorizationEvaluation` or the original
     `SignalCallAuthorization` that becomes a signed `AuthorizationGrant` when a
     meta approver answers the slot) — added to §"Routed authorization relation".
  2. Deliberately-distinct local vs multi-node trust planes
     (`ObjectCoSignature` / `CoSignatureExpectation`; co-resident
     orchestrate/agent components return workflow receipts for criome to adopt;
     independent authority sits at the criome quorum layer) — folded into
     §"Workflow guard substrate".
- Deleted `INTENT.md`.
- Pointer retarget: the only `INTENT.md` references in the repo were inside
  `INTENT.md` itself (self-references + a pointer to `primary/INTENT.md` and
  `criome/INTENT.md`). No external file (README, Cargo.toml, AGENTS.md,
  skills.md, Rust src) referenced it, so no retargeting was needed.

### Verification

- `jj diff --stat`: `ARCHITECTURE.md` +16 net, `INTENT.md` -125 (deleted).
  Docs/structure-only change; no Rust source touched, so the contract crate's
  wire vocabulary is unaffected.
- Grep confirmed no dangling `INTENT.md` references remain in tracked files.

### Result

- Commit: `8421fd12` (change `wnsnpxro`) on `main`.
- Push: fast-forward, `main` moved `5976b2870e02 -> 8421fd126398`.
  `main == main@origin` confirmed after push.
- Feature branch preserved: `criome-authorization-push` intact at
  `qusxnvup 2986f8f8`.
- Archived records routed to this repo: 0 (per the routing manifest), so no
  record integration was required for TASK 1.

## TASK 2 — schema-next (/git/github.com/LiGoldragon/schema-next)

### Record identification

- Manifest `agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`
  §DEFERRED-TO-STRAGGLER → `intended: repos/schema-cc (1 record)`:
  record id `vpbx`.
- Full record pulled from `/tmp/spirit-archive-extract/archived-spirit-records.dump.md`
  (line 1688): `vpbx` (Decision, cert=High, imp=Minimum, priv=Zero).
  Referents: `schema-cc schema-next schema-rust-next nota-next`.
  Description: schema-cc is the schema compiler-compiler — the schema language
  and compiler definition (reference grammar, dispatch precedence, built-in
  heads, shape vocabulary, emission rules) is kept as typed data that GENERATES
  the schema compiler (schema-next and schema-rust-next) rather than being
  hand-written, bottoming out in the nota-next seed; push as much of the
  compiler definition into data as possible.

### Pre-flight gate

- `main` and `main@origin` both at `unvxmttw 357eac0e` (clean FF base).
- Op log: last op 3h prior was a push of `main`; no active work.
- `jj new main` based the work on `main`.

### Integration (by synthesis)

- schema-next is the live successor that contains the in-tree schema-cc, so the
  record was synthesized as a new bullet in `ARCHITECTURE.md`
  §Direction / "What schema is", immediately after the existing self-hosting
  bullet (which it sharpens). The bullet names the compiler-compiler
  architecture explicitly, cites `(Spirit \`vpbx\`)` in the file's existing
  citation convention, and explains the schema-next / schema-rust-next /
  nota-next-seed relationship plus the "push the compiler definition into data"
  governing rule. +9 lines.

### Verification

- `jj diff --stat`: `ARCHITECTURE.md` +9.
- Confirmed `vpbx` now cited; no `---` horizontal rules introduced.

### Result

- Record id: `vpbx`. Integrated into schema-next: yes.
- Commit: `e4f7382c` (change `wwwnxulu`) on `main`.
- Push: fast-forward, `main` moved `357eac0e4562 -> e4f7382cde7e`.
  `main == main@origin` confirmed after push.

## Blockers / unknowns / follow-up

- None blocking. Both tasks landed.
- `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` is a local,
  non-committed extract; the `vpbx` integration prose stands on its own in
  schema-next ARCHITECTURE.md and does not depend on the dump persisting.
- The routing manifest's DEFERRED-TO-STRAGGLER bucket still holds 42 other
  parked records for other straggler repos (signal-criome, CriomOS,
  spirit-guardian-config, persona, lojix-cli); those are out of scope here and
  remain for their own owner/straggler-clearing passes. (signal-criome's
  parked records, if any, were not part of this brief — TASK 1 stated 0 routed
  records for signal-criome, matching the manifest's per-target table which
  does not list signal-criome as a routed target.)
