# Orchestrate's zeus store: what it is, and the upgrade that opens it

zeus's store was written by orchestrate 0.37.0 under sema-engine. It holds no Locks.

- **The upgrade lives in memory-engine.** `Engine::open` now recognises a store sema-engine wrote by its content, converts it in place, and opens it.
- **The proofs pass.** The branch Nexus opens a copy of the zeus store and serves exactly what the 0.37.0 Nexus that wrote it serves. It does the same for ouranos's older store of this kind, which holds 148 Locks. A second open upgrades nothing. The ouranos store already in the memory format behaves as it did before.
- **Gates and pushes:** every touched repository is gated green on prometheus and pushed to `ethos27-2e404d`.
- **Nothing merged or deployed.** On zeus, nothing beyond the read-only copy, with one side effect: my ssh logins restarted zeus's failing unit (see "zeus side effect" below).

Evidence is in `/home/li/primary/flows/2e404d/orchestrate/zeus-store/`. The zeus provenance is in `provenance.txt` there.

## What the store is

- **The file:** `~/.local/state/orchestrate-nexus/orchestrate-nexus.memory` on zeus, 303104 bytes, inode 28879478.
  - The copy is `zeus-orchestrate-nexus.memory`, with sha256 46a99052…ea67.
  - The checksum is the same at the source before and after the read, and for the copy.
- **The writer:** orchestrate 0.37.0, source `c7c44cb3`, built with sema-engine 0.17.0.
  - Home generation 37 ran it, from `/nix/store/kjs1zikz…-orchestrate-0.37.0`. Its binary names `orchestrate-nexus.sema` and `sema-engine-0.17.0`.
  - CriomOS-home pinned `c7c44cb3` from 2026-10-18. The store's last successful start was 2026-11-10 18:09.
- **How it got its name:** 0.38.0 renamed it itself.
  - At its first start, 2026-11-11 03:02:12, 0.38.0's own startup path upgrade (`defaults.rs`) hard-linked `.sema` to `.memory` and removed `.sema`.
  - The memory engine then refused the content. Only the name was upgraded, never the bytes.
- **The format:**
  - It is the sema kernel and engine format: `__sema_meta` with schema_version 1, `__sema_headers`, and `__sema_engine_{catalog,commit_log,counters}`.
  - The storage layout is 7, with 127 commits. There is no versioned log and no checkpoint.
- **What it holds:**
  - **No Locks:** the catalog names `locks` and `locks_v2`, but neither table was ever created, so no Lock was ever written.
  - **One row each in five tables:** `lock_id_allocator_v2` (the next id is 1), the metadata tree, the situation, the pre-0.32 `orchestrate_configuration`, and the v1 `lock_id_allocator`.
  - **The situation record** names `orchestrate-nexus.sema` and carries inode 28879478, the inode of today's `.memory` file. So on zeus the store's bearing is Moved, and it serves without a relocation. I did not check the device number.
- **ouranos has a second store of the same kind.** `~/.local/state/orchestrate-nexus/orchestrate-nexus.memory.pre-memory` was set aside on 2026-11-11. It was also written by 0.37.0, holds 148 Locks in `locks_v2` and 52296 commits. It is used below as the populated case.

## The upgrade

**memory-engine `f6ba771`** (0.20.0, branched from main `27f256c`) holds the upgrade.

- **Where it builds from:** main already had `LegacySemaStore::convert` (0.19.0), which converts a sema-engine store in one write transaction. Orchestrate pinned `abf9d85` (0.18.0), which does not have it.
- **What `Engine::open` does now:**
  1. It opens the kernel as before.
  2. Only when the kernel refuses the file with `LegacyFileLacksSchema` does it ask `SemaFile` whether the file is a sema store.
  3. A sema store is converted in place in one transaction and then opened.
- **Recognition is by content.** The file must have `__sema_meta` and `__sema_headers` under this build's rkyv header. It must be at layout 7; I added this layout check. Its log and checkpoints must verify under the sema labels.
- **Nothing is stamped.** The schema version is the one 0.37.0 wrote, carried over by renaming `__sema_meta`, so the kernel's version guard judges the store as written.
- **Any other unversioned file** keeps the kernel's refusal. A sema store that fails a check is refused and stays a sema store.
- **`Engine::sema_conversion()`** returns the receipt of a conversion on the open that made it, and `None` afterwards.
- **Why the kernel is opened first,** rather than classifying the file read-only: a store copied from a running Nexus needs redb repair. A read-only open refuses such a file with `RepairAborted`; the line 3 table listing below hit exactly that. The writable kernel open repairs it.
- **Tests:** four new tests in `tests/sema_conversion.rs` cover:
  - an in-place upgrade, with the second open a no-op;
  - a compacted store, which keeps its cut-off origin;
  - an unversioned file that is no sema store, which keeps the refusal;
  - a layout-6 sema store, which is refused and stays sema.

**orchestrate `a6c84bc`, then `32e0e2c`** (UPGRADES only) repins memory-engine 0.20.0 and memory 0.2.0.

- The Nexus prints `orchestrate-nexus upgraded <path> from the sema format to the memory format` before `ready`.
- `orchestrate-relocate` and `orchestrate-upgrade-preflight` upgrade through the same open.
- No record or label changed.

**orchestrate-test `cf5d763`, then `a5e0a43`** pins the new orchestrate head and adds a fourth input, `orchestrate-sema` (0.37.0, `c7c44cb3`), with the scenario `orchestrate-sema-orchestrate`:

1. 0.37.0 writes `orchestrate-nexus.sema`: a meta Configure and one Lock.
2. The branch Nexus moves the file, prints the upgrade line, and serves the Lock. It refuses the Lock's path, numbers the next Lock 2, and keeps ordinary Configure shut.
3. A second start prints nothing extra and holds both Locks.

## Proofs

Each run uses a fresh copy in a bwrap mount namespace, with the copy at the live path and a scratch socket directory. The scripts are `proof/prove.sh` and `proof/inner.sh`, the transcripts are in `proof/runs/`, and the table listings come from `proof/inspect.rs`.

**Line 0: zeus's failure, reproduced.** Live 0.38.0 on the zeus copy at `.sema` refuses it with the same retro-stamp error the zeus journal shows.

**Line 1: the bytes as zeus holds them now, at `.memory`.**
- The first branch open converts them: every table becomes `__memory_*`, with the same row counts.
- That open then refuses with `CarriedStore`. This is correct for a copy: its inode is not the recorded one, and the guard keeps working after the upgrade.
- `orchestrate-relocate` declares the move. The Nexus then serves `Observed.Locks.[]`, takes Lock 1 and releases it.
- The reopen does no upgrade and serves `Observed.Locks.[]` again.
- The ouranos sema store behaves the same with its 148 Locks. Its next Lock is numbered 26134.

**Line 2: what the store's writer reads, compared with the branch.** A copy at `.sema`, opened by the store's writer, 0.37.0, then by the branch Nexus:

| store | Observe.Locks md5 (0.37.0 / branch first open / branch reopen / 0.38.0 after) | Locks |
|---|---|---|
| zeus | c0432094… in all four | 0 |
| ouranos sema | 6b2bfed1… in all four | 148 |

- The branch's first open prints the upgrade line and is Moved: the hard link keeps the inode, exactly zeus's path.
- The reopen prints nothing extra.
- After the upgrade, live 0.38.0 also opens the store and sees the same Locks, so rollback to 0.38.0 stays open.

**Line 3: the ouranos store already in the memory format.** A copy of the live store (sha256 60be4a00…, 11 Locks), with the same five inputs through live 0.38.0 and through the branch:
- The two transcripts are identical except for the copy's inode line.
- The branch prints no upgrade line, and its tables after the run are still `__memory_*`.

## Heads and gates

Every gate ran `nix-fast-build --remote prometheus` against the committed revision; the logs are in `zeus-store/gates/`.

| repository | branch head (pushed) | builds on | gate |
|---|---|---|---|
| memory-engine (new branch `ethos27-2e404d`) | `f6ba771` (0.20.0) | main `27f256c` | exit 0, 10 checks |
| orchestrate | `32e0e2c` | `e78534f` | exit 0, 18 checks; `a6c84bc` also exit 0 (181 tests) |
| orchestrate-test | `a5e0a43` | `6a6c812` | exit 0, 10 checks; `cf5d763` also exit 0 |

signal-orchestrate, meta-signal-orchestrate and nexus are untouched.

## zeus side effect

zeus does not keep li's user manager running without a login (no lingering). Every ssh login therefore starts `orchestrate-nexus.service`, which fails five times and hits its start limit. My sessions at 02:35, 02:41 and 02:54 each did this.

- **What it changes:** each failed open rewrites redb-level bytes. The file's sha256 was 524a5a1a… at 02:35:45, 46a99052… at 02:35:49 (the copy), and d240d2d4… at 02:54:46.
- **What it does not change:** the rows. The refused write transaction is never committed. I infer this from the kernel's code path; I did not read the file again.
- **After deploy:** the first login will run the upgrade.

## Questions

1. **The upgrade happens on every memory-engine consumer's open, not only Orchestrate's.** Once a consumer repins to 0.20.0, a sema store it finds is upgraded on its first open. I took that from "Memory is upgraded, never accommodated". Is it wanted for every consumer, or should consumers opt in?
2. **No copy of the sema file is kept.** The conversion is one atomic redb transaction, and every refusal comes before it writes, so the upgrade keeps no pre-upgrade copy. memory-engine 0.19.0's guidance was to convert a copy. Should the zeus deploy set the file aside first, or is in-place the rule?
3. **The upgrade line is not printed when the open then refuses.** A store that is upgraded and then refused, such as a carried copy, says so only through its tables. Should the Nexus print the line on that path too?
