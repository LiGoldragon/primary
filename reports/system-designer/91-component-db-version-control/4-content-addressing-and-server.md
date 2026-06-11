> **Correction (applied in the synthesis, file 6 §Corrections):** §3 below attributes the `GitoliteServer` + `TailnetController` role to **prometheus**. That is wrong — `goldragon/datom.nota` assigns those roles to **ouranos** (lines 28–58); prometheus (lines 59–97) is `[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]`, the `criome-backup`-SSID Btrfs node, a backup *target* not the Gitolite/control host. Read every "prometheus = Gitolite/controller" claim below as **ouranos**. The rest of this finding holds.

## 1. Content-addressing / hashing primitives across the stack

The headline finding: **the Sema storage plane is sequence-addressed, not content-addressed.** Every durable identity in `sema`, `sema-engine`, and `signal-sema` is a persisted monotonic `u64` counter. The only real content hashing in the LiGoldragon stack is criome's blake3 `ObjectDigest`, plus Nix's narHash on the four CriomOS flake axes, plus git's opaque SHA-1s carried through as strings.

| Primitive | What it hashes/identifies | Type | Content-addressed? | Source |
|---|---|---|---|---|
| `SnapshotIdentifier(u64)` | a sema-engine snapshot/version generation | `u64` monotonic counter | **No** — sequence | `sema-engine/src/snapshot.rs:19`, advanced via stored `LATEST_SNAPSHOT_KEY` counter `sema-engine/src/engine.rs:970` |
| `CommitSequence(u64)` | one durable commit (atomic write batch) | `u64` monotonic counter | **No** — sequence | `sema-engine/src/sequence.rs:17`, stored at `LATEST_COMMIT_SEQUENCE_KEY` `engine.rs:874` |
| `DatabaseMarker` | `(CommitSequence, SnapshotIdentifier)` pair = whole-DB version cursor | struct of two `u64`s | **No** — sequence | `sema-engine/src/snapshot.rs:35`; read by `current_database_marker` `engine.rs:883` |
| `RecordIdentifier(u64)` / `RecordKey(String)` | a row in an identified table | `u64` counter / opaque string | **No** | `sema-engine/src/record.rs:26,56`; counter at `IDENTIFIED_COUNTERS` `engine.rs:35` |
| `Slot<Payload>(u64)` + `Revision(u64)` | wire identity of a mutable record + its generation for compare-and-set | phantom-typed `u64` + `u64` | **No** — sequence | `signal-sema/src/identity.rs:36,77` (explicitly "on the wire the slot is just its numeric identifier") |
| `CommitLogEntry` / `COMMIT_LOG` table | replayable operation log (the WAL) keyed by sequence | rkyv struct, redb table keyed by `u64` | **No** — supports `replay_from_sequence` / `commit_log_range` but by sequence, not hash chain | `sema-engine/src/log.rs:15`; `engine.rs:900-918` |
| rkyv archived bytes | the on-disk value encoding under each redb key | `AlignedVec` of rkyv bytes (no digest taken) | **No** — values are stored raw, never hashed | `sema/src/lib.rs` Table encode/decode; `DatabaseHeader` `lib.rs:111` is a format guard (format_version/endian/pointer-width/unaligned/bytecheck), not a content hash |
| criome `ObjectDigest(String)` | **blake3 hex** of arbitrary bytes — the one true content hash | blake3-256 → hex `String` | **YES** | `signal-criome/src/lib.rs:55-57` `Self::new(blake3::hash(bytes).to_hex().to_string())`; type at `signal-criome/src/schema/lib.rs:49`; `blake3 = "1"` in both `criome/Cargo.toml:28` and `signal-criome/Cargo.toml:22` |
| criome `BlsPublicKey` / `BlsSignature` / `PublicKeyFingerprint` | BLS12-381 attestation material | opaque `String`s | n/a (crypto identity, not content addressing) | `signal-criome/src/schema/lib.rs` |
| CriomOS four flake input axes: `system`, `pkgs`, `horizon`, `deployment` | per-deploy projected inputs, each cached independently in nix's flake-eval cache | Nix flake `narHash` = **sha256** | **YES** (Nix store / narHash) | `CriomOS/flake.nix:2` (description names all four as "content-addressed flake inputs from lojix"), inputs at `flake.nix:46-72` |
| git / Gitolite object ids (`ObjectIdentifier`, `old/new_object_id`) | commit/tree/blob identity carried into the ledger | git **SHA-1** hex, stored as opaque `String` | YES (git's own CAS) but **not computed by us** — passed through | `repository-ledger/src/spool.rs:181` wraps them as `ObjectIdentifier::new(...)`; produced by `git rev-list` in `CriomOS/modules/nixos/repository-receive.nix:122-124` |
| Nix store paths generally | derivation inputs/outputs | sha256-based store-path hash | YES (Nix CAS) | platform-level |

**Implication for a backup remote:** if the design wants content-addressing of Sema snapshots, it must add it — blake3 over rkyv archived bytes is the natural fit and there is already a `blake3 = "1"` precedent in criome to copy. Today the only stable cross-machine identity a Sema store exposes is the `(CommitSequence, SnapshotIdentifier)` `DatabaseMarker` plus the replayable `COMMIT_LOG`.

## 2. repository-ledger — the server-side ingest precedent

`repository-ledger` (`/git/github.com/LiGoldragon/repository-ledger`) is the closest existing pattern for "ship versioned change events into a Sema store, server-side." It is a full triad component: thin `repository-ledger` CLI + long-lived `repository-ledger-daemon`, paired with `signal-repository-ledger` (ordinary) and `meta-signal-repository-ledger` (meta).

How it works (the dual-path atomic-receive pattern):
- **Fast path:** the CriomOS Gitolite `post-receive` hook builds a `(PushObservation (ReceiveHookNotification ...) [(CommitObservation ...)])` NOTA request and invokes the `repository-ledger` CLI, which connects to `repository-ledger-daemon` over its Unix socket and submits a typed Signal frame (`repository-receive.nix:177`).
- **Fallback spool (the atomicity guarantee):** if the daemon is down or CLI submission fails, the hook writes the notification to a dot-prefixed temp file then atomically `mv`s it into the spool as a `<timestamp>-<repo>-<pid>.nota` file (`repository-receive.nix:182-184`). A `SpoolIngestActor` driven by a 2-second ticker (`daemon.rs:46`) drains `*.nota` files, decodes them with `nota-next`, records them, and moves each to `processed/` only after the store commit (`spool.rs:60-66`). Atomic rename + commit-then-move = no lost or double-counted events.
- **Storage:** one `sema-engine` database (`repository-ledger.redb`). Every stored item is a typed Rust record (events, commit observations, file-change observations, registrations, spool policy, mirror policy) — "no line-oriented log is the source of truth" (INTENT.md).
- **Actor shape:** `RepositoryLedgerStoreActor` serialises all reads/writes through its kameo mailbox (no `Arc<Mutex>`); the daemon engine holds it in a `OnceCell` and lazy-starts on first connection (`daemon.rs:143-154`).
- **Two authority tiers, two sockets:** ordinary working traffic vs meta (registration/spool/mirror policy) on separate listener tasks via `triad_runtime::AsyncMultiListenerDaemon`.
- **Execution plane:** Signal in → Nexus work → Sema read/write → Signal reply, via `triad-runtime::Runner`. NOTA only at CLI/spool/debug edges; inter-component traffic is rkyv Signal frames.
- **Queries:** agent-facing discovery (`RecentRepositories`, `ChangedFiles`, `CommitMessages`) as first-class `Query` operations; the six Sema words never appear on the public wire.

This is a directly reusable template for a Sema backup remote: a triad daemon that accepts versioned change events (here, git pushes) over a socket with a durable spool fallback, lands them as typed records in a sema-engine DB, and is provisioned as a NixOS systemd service tied to a node role.

## 3. Server infrastructure available as a backup target

**Gitolite server — runs on `prometheus`.** The `goldragon/datom.nota` cluster proposal assigns the `GitoliteServer` role exclusively to the node whose services vector is `[(TailnetClient) (TailnetController) (NixBuilder None) (PersonaDevelopment [(GitoliteServer)])]` (`goldragon/datom.nota:58`). The CriomOS module `modules/nixos/repository-receive.nix` enables it only on `personaDevelopmentHas ... "GitoliteServer"` hosts (`repository-receive.nix:14-15`), with `services.gitolite.enable = true`, `dataDir = /var/lib/gitolite` (`:190-195`).

**Cluster nodes** (from `goldragon/datom.nota`): `zeus` (Edge, ThinkPad T14), `prometheus` (LargeAiRouter, GMKtec EVO-X2, 128GB, the Gitolite + NixCache + NixBuilder host), `tiger` (EdgeTesting, ThinkPad E15, NixBuilder). prometheus is the natural backup host — it already runs the Gitolite server and a Nix binary cache, and notably exposes a `criome-backup` WiFi SSID (`datom.nota:95`), suggesting backup is already an intended prometheus concern.

**Already-running server-side daemon:** `repository-ledger-daemon` runs as systemd service `repository-ledger` on the Gitolite host (`repository-receive.nix:216-242`), `User=repository-ledger`, binding two Unix sockets:
- `/run/repository-ledger/repository-ledger.sock` (mode 432 = 0660, ordinary/working tier)
- `/run/repository-ledger/repository-ledger-owner.sock` (mode 384 = 0600, meta/owner tier)
- store at `/var/lib/repository-ledger/repository-ledger.redb`, spool at `/var/lib/repository-ledger/spool` (config encoded at `repository-receive.nix:34-36`).

**Atomic-receive primitives that exist today:**
- git `receive-pack` via Gitolite (the SHA-addressed object transfer + ref update), with the `post-receive` hook as the event tap.
- The repository-ledger **spool**: atomic temp-write-then-rename of NOTA files + commit-then-move-to-processed — a filesystem-level at-least-once delivery primitive (`repository-receive.nix:182-184`, `spool.rs`).
- The sema-engine **commit log** (`COMMIT_LOG` table) with `replay_from_sequence(CommitSequence)` (`engine.rs:900`) — a replayable WAL that a backup/mirror could tail by sequence cursor.
- Signal-frame length-prefixed rkyv transport over Unix sockets (`triad_runtime::LengthPrefixedCodec`, `daemon.rs:280`) with a protocol-version handshake.

There is **no** existing network/TCP receive endpoint or cross-host sema-engine ingest socket — all current sockets are local Unix sockets; cross-host reach would be over the tailnet (all nodes are `TailnetClient`s; prometheus is `TailnetController`).

## 4. Precedent for remote sync (push state to a server)

- **beads → git remote (the one live remote-sync precedent).** `.beads/push-state.json` records `last_push: 2026-06-09T19:28:17Z` and `last_commit: tdiv2v3impeagiisivj4cc57jfvuls75` (a jj change/commit id) — beads tracks a high-water mark against the workspace git remote. `.beads/config.yaml:39-45` documents a JSONL backup that is "Auto-enabled when a git remote exists" with `git-push` to either the project repo or a separate `git-repo`. Backend is **embedded Dolt** (`.beads/metadata.json`: `dolt_mode: embedded`, `dolt_database: primary`), with `embeddeddolt/primary/` on disk. Note: the Dolt DB, `interactions.jsonl`, `push-state.json`, and `backup/` are all gitignored (`.beads/.gitignore`); only `config.yaml`/`metadata.json`/`README.md` are tracked. So beads' "remote" is the existing git remote + a periodic JSONL export, not a bespoke server.
- **Spirit Sema store hard-migration backups (local, not remote).** `~/.local/state/spirit/` shows the two-submodule From-chain migration backups landing as siblings: `spirit.sema` (live), `spirit.schema-1-backup-0.sema`, `spirit.schema-old-backup-{0,1,2,3}.sema`. This is local rotation, not remote sync — but it is the existing convention for "snapshot the durable Sema file at a schema boundary."
- **No sema-engine remote/mirror today.** repository-ledger's INTENT/ARCHITECTURE name a *future* "mirror policy" (`MirrorPolicy`, `MirrorPolicySet` in `meta-signal-repository-ledger`, surfaced in `lib.rs:28`) and explicitly defer "GitHub mirroring execution in the first slice" — so a mirror/backup verb is anticipated in the contract but unimplemented.

**Candidates for the version-control remote of a Sema backup:** (a) the existing Gitolite server on prometheus (git transport, already trusted, already has a hook tap); (b) the existing `repository-ledger-daemon` socket pattern cloned for a `sema-backup`/mirror daemon on prometheus; (c) the existing git remote that beads already pushes to. The cleanest reuse is the repository-ledger triad shape (daemon + spool fallback + sema-engine DB + NixOS role gating) pointed at prometheus, with content-addressing added via blake3 over rkyv bytes (criome precedent) since the Sema plane provides only sequence identities today.
