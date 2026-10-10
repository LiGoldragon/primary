# Scout Situational Map — Spirit content-addressed object for mirror fan-out

## Task and scope

Map exact facts in `/home/li/primary/repos/spirit` (Rust) about how Spirit
produces the content-addressed object behind mirror fan-out, so a sender can
obtain the REAL record body that re-hashes to the versioned-log head
(witness head `326640ace3...b85a`). Read-only scouting. Five questions plus a
conclusion on whether new read machinery is needed.

## Rev / branch reconciliation (IMPORTANT — observed)

- The brief names branch `criome-auth-witness` (rev `7d1b0697`). That bookmark
  resolves: `git rev-parse criome-auth-witness` = `7d1b069718a0ddede6e3928ecef272f25caaee6b`.
- The working tree is NOT on that rev. `git rev-parse HEAD` =
  `f64bc8ad74cf859d6335a43c1f11b67f974b3c8f` ("spirit: 0.18.1 …"), and
  `git branch` shows `* (HEAD detached from 61eaf14)`.
- HEAD and `criome-auth-witness` have DIVERGED:
  `merge-base --is-ancestor` is false in both directions.
- `git diff --stat HEAD 7d1b0697` over the four key files: only `src/engine.rs`
  (+37) and `src/store/mod.rs` (+14) differ; `src/shipper.rs` and
  `src/criome_gate.rs` are byte-identical between the two revs.
- `observe_head` exists ONLY on `criome-auth-witness`, NOT on the detached HEAD
  (`git grep observe_head HEAD -- src/engine.rs` → no match;
  `… 7d1b0697 …` → `src/engine.rs:722`).

Consequence: all `engine.rs` / `store/mod.rs` line numbers below are quoted at
`7d1b0697` (via `git show 7d1b0697:<path>`). `shipper.rs` / `criome_gate.rs`
line numbers are from the working tree (identical to the branch). The working
tree as checked out does NOT contain `observe_head`; a worker must check out
`criome-auth-witness` to build/edit against it.

Dependency sources quoted from the cargo git cache at the revs `criome-auth-witness`'s
`Cargo.lock` pins (verified against `git show 7d1b0697:Cargo.lock`):

- `mirror` @ `~/.cargo/git/checkouts/mirror-c6db31b88119a19c/027a991`
- `signal-mirror` @ `~/.cargo/git/checkouts/signal-mirror-49ef36ad3396768b/24ee194`
- `sema-engine` @ `~/.cargo/git/checkouts/sema-engine-ff01b9246db31ae9/1afcd01`
- `meta-signal-spirit` @ `~/.cargo/git/checkouts/meta-signal-spirit-218ef8a834c9b65d/783cd50`
  (`Cargo.lock` pins `…?branch=criome-auth-witness#783cd5024507bbf339bd92dad3bba38cd64cb40d`, v0.3.0).
  Note: the working-tree `Cargo.lock` (HEAD) pins meta-signal-spirit v0.2.0
  `#83415f2…` which has NO `ObserveHead` type; only the branch's `783cd50` rev does.

All deps are `git = "https://github.com/LiGoldragon/…"` (see `Cargo.toml:118-181`),
NOT local path deps — the envelope/entry construction lives in those crates, not
in the spirit repo itself.

## OBSERVED FACTS

### 1. Mirror-shipper machinery + the EntryEnvelope / PayloadBytes

Spirit side (`src/shipper.rs`, identical on both revs) holds the gate but does
NOT build envelopes itself. It owns a `mirror::ComponentShipper` and delegates:

- `src/shipper.rs:100` `pub async fn ship_unshipped(&self) -> Result<Option<ShipOutcome>, MirrorShipperError>`
  → `shipper.ship_unshipped().await` (line 102).
- `src/shipper.rs:72-76` arms it via
  `ComponentShipper::from_shared_engine(engine, socket_address, VersionedStoreName::new(RecordFamily::STORE_NAME))`
  — store and shipper share ONE `Arc<sema_engine::Engine>`.
- Engine wrapper: `src/engine.rs:595` (@7d1b0697)
  `pub async fn ship_unshipped_to_mirror(&self) -> Result<Option<mirror::ShipOutcome>, MirrorShipperError>`
  → `self.mirror_shipper.ship_unshipped().await`.

The actual envelope construction is in the `mirror` crate:
`mirror-…/027a991/src/shipper.rs:150-166`, verbatim:

```rust
pub fn envelope_for_entry(&self, entry: &VersionedCommitLogEntry) -> Result<EntryEnvelope> {
    Ok(EntryEnvelope::new(
        CommitSequence::new(entry.commit_sequence().value()),
        entry
            .previous_entry_digest()
            .map(|digest| EntryDigest::new(FixedBytes::new(*digest.bytes()))),
        EntryDigest::new(FixedBytes::new(*entry.entry_digest().bytes())),
        PayloadBytes::new(Bytes::new(
            rkyv::to_bytes::<rkyv::rancor::Error>(entry)
                .map_err(|source| Error::PayloadEncode {
                    surface: "versioned entry",
                    message: source.to_string(),
                })?
                .to_vec(),
        )),
    ))
}
```

So per the four fields the brief asked about:
- PayloadBytes = `rkyv::to_bytes(entry)` of the WHOLE `VersionedCommitLogEntry` —
  i.e. the REAL serialized entry body, not a digest or a re-hash.
- sequence = `entry.commit_sequence()`.
- previous_digest = `entry.previous_entry_digest()` (`Option<EntryDigest>`).
- digest = `entry.entry_digest()` (the content-addressed head of that entry).

`ship_unshipped` drains the outbox (`mirror-…/027a991/src/shipper.rs:175-202`):
maps `engine.versioned_replay_from_sequence(first)` through `envelope_for_entry`,
wraps as `EntrySuffix::from_entries(store_name, expected_head, entries)`, sends
`Input::Append(...)`.

EntryEnvelope schema (`signal-mirror-…/24ee194/src/schema/lib.rs:116-130`),
verbatim:

```rust
pub struct EntryEnvelope {
    pub sequence: CommitSequence,
    pub previous_digest: Option<EntryDigest>,
    pub digest: EntryDigest,
    pub payload: PayloadBytes,
}
pub struct EntrySuffix {
    pub store: StoreName,
    pub expected_head: Option<HeadMark>,
    pub entries: Vec<EntryEnvelope>,
}
```
`pub struct PayloadBytes(Bytes);` (`…/lib.rs:98`).

Reverse confirmation inside Spirit itself: `src/store/mod.rs:108-128` (@7d1b0697)
`MirrorRestoreImport::from_bundle` decodes the wire `envelope.payload` back into
the body — `rkyv::from_bytes::<VersionedCommitLogEntry, _>(envelope.payload.as_slice())`
(lines 120-123) and reads the head as `EntryDigest::new(*envelope.digest.as_bytes())`
(line 115). This proves the PayloadBytes IS the rkyv `VersionedCommitLogEntry`
body and `envelope.digest` is its entry digest.

### 2. CriomeGate content-object machinery (LocalHeadCapture / EntryDigest)

`src/criome_gate.rs` (identical both revs):

- `src/criome_gate.rs:52-56`:
  ```rust
  pub struct LocalHeadCapture {
      component: ComponentKind,
      head_digest: EntryDigest,
  }
  ```
- `src/criome_gate.rs:63-68` `pub fn spirit_head(head_digest: EntryDigest) -> Self`
  — captures ONLY the `EntryDigest` (and `ComponentKind::Spirit`). No body, no bytes.
- `src/criome_gate.rs:85-93` projection to the authorized object:
  ```rust
  impl From<&LocalHeadCapture> for AuthorizedObjectReference {
      fn from(capture: &LocalHeadCapture) -> Self {
          AuthorizedObjectReference {
              component: capture.component,
              digest: ObjectDigest::from_bytes(capture.head_digest.bytes()),
              kind: AuthorizedObjectKind::Head,
          }
      }
  }
  ```
- `SpiritAttestor::evaluation` (`:140-149`) builds `AuthorizationEvaluation { contract, object, evidence }`;
  `signal_call_authorization` (`:151-162`) builds a `SignalCallAuthorization` whose
  `ObjectDigest::from_bytes(capture.head_digest.bytes())` and replay nonce are all
  derived from the head digest bytes.

So CriomeGate authorizes a reference to the head DIGEST (`ObjectDigest`, blake3-hex
of the 32 head bytes), kind `Head`. It carries the digest, NOT the entry body.

The gate/ship driver `src/engine.rs:634-657` (@7d1b0697)
`pub async fn gate_and_ship_head(&self)`:
```rust
let Some(head_digest) = self.versioned_log_head()? else { return Ok(None); };
let capture = crate::criome_gate::LocalHeadCapture::spirit_head(head_digest);
```
— it captures only the digest from `versioned_log_head()`, never the body.

### 3. `versioned_log_head()` and siblings in `src/store/mod.rs` (@7d1b0697)

- `:405-407`
  `pub fn versioned_log(&self) -> Result<Vec<VersionedCommitLogEntry>, StoreError>`
  → `self.database.versioned_commit_log()` — returns the FULL entry objects (the body).
- `:420-425`
  `pub fn versioned_log_head(&self) -> Result<Option<EntryDigest>, StoreError>`
  → `self.versioned_log()?.last().map(VersionedCommitLogEntry::entry_digest)` —
  returns ONLY the digest of the last entry.
- `:429-434`
  `pub fn versioned_log_from(&self, sequence: CommitSequence) -> Result<Vec<VersionedCommitLogEntry>, StoreError>`
  → `self.database.versioned_replay_from_sequence(sequence)` — full entries after a sequence.
- `:474-480` (`#[cfg(feature = "mirror-shipper")]`)
  `pub fn import_mirror_restore_bundle(path, bundle: signal_mirror::RestoreBundle, expected_head: EntryDigest) -> Result<Self, StoreError>`.

Engine-level exposure: `src/engine.rs:476-478` `pub fn store(&self) -> &Store`
(so `versioned_log()` / `versioned_log_from()` are reachable through `engine.store()`),
and `src/engine.rs:487-489` (`#[cfg(feature="mirror-shipper")]`)
`pub fn versioned_log_head(&self) -> Result<Option<sema_engine::EntryDigest>, StoreError>`.

So a method that returns the FULL content-addressed object (the entry body)
EXISTS at the store layer: `Store::versioned_log()` and `Store::versioned_log_from()`,
each returning `Vec<VersionedCommitLogEntry>`. There is no single
`fetch entry by head/sequence` returning one entry; you take `.last()` or filter
the vec.

### 4. `observe_head` / `observe_head_async` and the meta op (@7d1b0697)

`src/engine.rs:722-739`, verbatim:
```rust
pub fn observe_head(&self) -> MetaOutput {
    match self.nexus.store().versioned_log_head() {
        Ok(head) => MetaOutput::head_observed(VersionedLogHead {
            database_marker: self.nexus.database_marker(),
            selected_head_digest: SelectedHeadDigest::new(
                head.map(|digest| HeadDigestHex::new(digest.to_string())),
            ),
        }),
        Err(_) => MetaOutput::rejected(ConfigureRejection {
            configure_rejection_reason: ConfigureRejectionReason::InternalError,
            database_marker: self.nexus.database_marker(),
        }),
    }
}

pub async fn observe_head_async(&self) -> MetaOutput {
    self.observe_head()
}
```

The meta op surface (`meta-signal-spirit-…/783cd50/src/schema/meta_signal.rs`):
- `Input` enum (`:336-341`): `Configure(Configure)`, `Import(Import)`,
  `CollectRemovalCandidates(CollectRemovalCandidates)`, `ObserveHead`.
- `Output` enum (`:349-355`): `Configured`, `Imported`,
  `RemovalCandidatesCollected`, `Rejected`, `HeadObserved(HeadObserved)`.
- `:325-328`:
  ```rust
  pub struct VersionedLogHead {
      pub database_marker: DatabaseMarker,
      pub selected_head_digest: SelectedHeadDigest,
  }
  ```
- `:309` `pub struct HeadDigestHex(String);`
- `:317` `pub struct SelectedHeadDigest(Option<HeadDigestHex>);`

Therefore: NO meta op returns the entry BODY. `ObserveHead` → `HeadObserved` →
`VersionedLogHead` carries only `selected_head_digest`, an
`Option<HeadDigestHex>` (a 64-char lowercase hex string from
`EntryDigest::Display`, per the doc comment at `src/engine.rs:709-721`). It is
the hex of the head digest, not the rehashable body. (Stated explicitly per the
brief: there is NO existing op that returns the full entry body.)

### 5. Store layer reading entries by sequence/head from sema-engine

`VersionedCommitLogEntry` (`sema-engine-…/1afcd01/src/versioning.rs:402-411`):
```rust
pub struct VersionedCommitLogEntry {
    store_name: VersionedStoreName,
    schema_hash: StoreSchemaHash,
    commit_sequence: CommitSequence,
    snapshot: SnapshotIdentifier,
    previous_entry_digest: Option<EntryDigest>,
    entry_digest: EntryDigest,
    operations: NonEmpty<VersionedLogOperation>,
}
```
Accessors: `commit_sequence()` (`:451`), `previous_entry_digest()` (`:459`),
`entry_digest()` (`:463`), `operations()` (`:467`).

The digest is computed over exactly those fields —
`EntryDigest::from_entry_fields` (`versioning.rs:257-285`) blake3-hashes a
domain tag `b"sema-engine-versioned-commit-log-entry-v2"`, store_name,
schema_hash, commit_sequence, snapshot, previous_entry_digest, and each
operation. So the rkyv-serialized `VersionedCommitLogEntry` carries every field
the digest hashes — the body re-hashes to `entry_digest`.

sema-engine read methods (`sema-engine-…/1afcd01/src/engine.rs`):
- `:1099` `pub fn versioned_commit_log(&self) -> Result<Vec<VersionedCommitLogEntry>>`.
- `:1117` `pub fn versioned_replay_from_sequence(&self, start: CommitSequence) -> Result<Vec<VersionedCommitLogEntry>>`.
- `:1585` `pub fn unshipped_outbox(&self) -> Result<Vec<OutboxEntry>>`.
- `:1591` `pub fn mirror_head(&self) -> Result<Option<MirrorHead>>`.

Spirit's `Store` wraps the first two (`store/mod.rs:405`, `:429`). `OutboxEntry`
(`sema-engine/src/outbox.rs:32,36`) exposes only `commit_sequence()` and
`entry_digest()` — no body.

## INTERPRETATION / CONCLUSION

Spirit ALREADY has the machinery to surface the real content-addressed object
(the entry body that re-hashes to the head) — but ONLY at the Rust store/engine
API layer, NOT through any wire/meta op:

- `Store::versioned_log()` and `Store::versioned_log_from(seq)` both return
  `Vec<VersionedCommitLogEntry>`. The last entry's `entry_digest()` equals the
  head; `rkyv::to_bytes(entry)` is the exact PayloadBytes the mirror ships and
  the exact bytes that re-hash (via `EntryDigest::from_entry_fields`) to the
  head. This is the SAME body construction used at `mirror` `envelope_for_entry`.
- So the "real record body" a sender needs already lives behind
  `engine.store().versioned_log()` / `.versioned_log_from()` — no new STORE
  read primitive is required to OBTAIN the body in-process.

What does NOT exist:

- No meta/wire op returns the body. `ObserveHead`/`HeadObserved`/`VersionedLogHead`
  return only the head hex (`HeadDigestHex(String)`). `LocalHeadCapture` /
  CriomeGate carry only the digest. The shipper's envelope (which DOES carry the
  body as PayloadBytes) goes to the mirror ingress, not back to a local caller.
- There is no single "get entry by head/by sequence → one `VersionedCommitLogEntry`
  (or its rkyv bytes)" accessor; callers take `.last()` / filter the vec.

So: if the requirement is for a SENDER (out-of-process, over the meta socket /
wire) to obtain the rehashable body, a NEW read op is needed — the existing
`ObserveHead` only yields the hex head. The body-producing code already exists
in-process (`Store::versioned_log*` + the mirror `envelope_for_entry` rkyv path)
and a new op would reuse `Store::versioned_log()`’s last entry rkyv-serialized,
mirroring `envelope_for_entry`'s `PayloadBytes::new(rkyv::to_bytes(entry))`.

## CHECKS RUN

- `git log/branch/rev-parse/merge-base/diff --stat/grep` in
  `/home/li/primary/repos/spirit` — pass; rev divergence as recorded above.
- `git show 7d1b0697:src/engine.rs` and `…:src/store/mod.rs` materialized and
  read for branch-accurate line numbers — pass.
- `rg`/`grep`/`Read` over spirit src and the four cargo git checkouts at the
  pinned revs — pass.
- Did NOT build or run tests (read-only scout; not requested as inspection).
- Did NOT verify the specific witness head `326640ace3…b85a` against a live
  store (no runtime inspection performed); the digest format claim is from
  source (`EntryDigest::Display`/`from_entry_fields`), not from a running daemon.

## UNKNOWNS / FOLLOW-UP

- The working tree is on a detached HEAD that lacks `observe_head`; an
  implementer must `git checkout criome-auth-witness` (or work at `7d1b0697`)
  before building against these facts.
- Whether downstream wants the body delivered over the meta socket (new op) vs.
  consumed in-process is a design choice not settled here; evidence supports
  either, with the in-process body path already present.
- `signal_mirror::RestoreBundle` shape (the full restore surface) was only
  partially read via `from_bundle`; not exhaustively mapped.
