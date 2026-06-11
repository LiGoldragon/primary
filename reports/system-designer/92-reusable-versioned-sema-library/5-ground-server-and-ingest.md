# Ground: server, cluster hosts, content-hash precedent, and the ingest pattern

## Scope

Ground facts for the reusable server-backed Sema version-control library: which cluster host plays which role, what content-addressing primitive already exists first-party, and the only working atomic-ingest precedent in the codebase. This maps what exists; it decides nothing. All claims are cited to lines read in `goldragon/datom.nota`, `signal-criome`, `repository-ledger`, and the CriomOS hook module.

## Cluster hosts: confirmed roles

The cluster is declared in `goldragon/datom.nota` as a `horizon-rs ClusterProposal` (positional NOTA records, source-declaration order; `datom.nota:1-3`). Each host's last positional field is its **role vector** — that is the authoritative statement of what the host *does*, distinct from the host's profile name (the first head atom). The ground-truth roles in the task match the role vectors exactly:

### ouranos — control / git host + backup INGEST target

`datom.nota:28` opens the host record with profile head `EdgeTesting`, but its role vector at `datom.nota:58` is:

```
[(TailnetClient) (TailnetController) (NixBuilder None) (PersonaDevelopment [(GitoliteServer)])]
```

So ouranos is the **TailnetController** (it runs the tailnet control plane) and hosts the **GitoliteServer** (nested under `PersonaDevelopment`). Hardware: `Metal X86_64`, 12 cores, `ThinkPadT14Gen5Intel`, 32 GB (`datom.nota:31`). This is the control/git host and, by virtue of being where Gitolite lives, the natural **backup-ingest** target — log suffixes shipped from peers land here.

Do not read the `EdgeTesting` profile head as ouranos's job; the role vector is the operative declaration.

### prometheus — backup STORAGE target (not the git/control host)

`datom.nota:59` profile head `LargeAiRouter`; role vector at `datom.nota:97`:

```
[(TailnetClient) (NixBuilder (Some 6)) (NixCache)]
```

prometheus is the **NixBuilder** (priority 6) and the **NixCache**. Hardware: `Metal X86_64`, 8 cores, `GMKtec EVO-X2`, 128 GB (`datom.nota:62`). Its filesystem is **Btrfs** across `/`, `/home`, `/nix`, `/var` subvolumes (`datom.nota:66-78`) — relevant because Btrfs gives cheap CoW snapshots at the storage layer. It also exposes the **`criome-backup`** wireless SSID as a dedicated backup access point (`datom.nota:95`: `wlp199s0f0u4 criome-backup TwoG 11 Wifi4 (routerBackupWifiPassword)`). prometheus is a **storage/cache target**, NOT the git or tailnet-control host. A prior synthesis swapped ouranos/prometheus; that swap is wrong — confirmed against the file.

### tiger — edge testing

`datom.nota:98` profile head `EdgeTesting`; role vector at `datom.nota:125`: `[(NixBuilder None)]`. Hardware `ThinkPadE15Gen2Intel`, 4 cores (`datom.nota:101`). Edge/test node.

### Other declared hosts (context, not load-bearing)

- **balboa** — `Center` profile, ARM64 `rock64`, empty role vector (`datom.nota:6-27`).
- **zeus** — `Edge` profile, `ThinkPadT14Gen2Intel`, empty role vector (`datom.nota:126-155`).

### Transport: the tailnet

ouranos is `TailnetController`; prometheus, tiger, balboa, zeus are all `TailnetClient` (`datom.nota:58,97`, and the per-host `TailnetClient` entries). Each host record carries a tailnet identity triple — a node key, a tailnet IPv6 (e.g. ouranos `201:6de1:...`, prometheus `200:ca41:...`), and a tailnet ULA prefix (`datom.nota:44-47, 83-86`). **The tailnet is the existing private mesh transport** between hosts. A "ship the log suffix to the server" design rides this mesh; no new transport substrate is implied. (Whether shipping is over SSH-to-Gitolite, a tailnet socket, or an HTTP ingest endpoint is undesigned — only the mesh floor is established.)

## Content-hash precedent: criome's blake3 ObjectDigest

The **only first-party content hash anywhere** is criome's `ObjectDigest`. Schema declaration `signal-criome/schema/lib.schema:47`: `ObjectDigest { value String }` — a newtype over a String. The hashing method is hand-written in `signal-criome/src/lib.rs:55-58`:

```rust
impl ObjectDigest {
    pub fn from_bytes(bytes: &[u8]) -> Self {
        Self::new(blake3::hash(bytes).to_hex().to_string())
    }
}
```

So the established content-addressing primitive is **blake3, hex-encoded into a String-backed typed newtype**, produced by a method on the owning noun (`ObjectDigest`), not a free function — it already satisfies the method-only discipline. In criome it addresses attestation artifacts and request digests (`lib.schema:93,135,147,161,167,194,212,234`) and is **out-of-band**: attestations reference content records by digest; content records carry no embedded proof (`criome/INTENT.md:51-54`). That separation — a digest-bearing record *referencing* the thing it covers, rather than the thing carrying its own hash — is a directly transferable shape for a hash-linked log (an entry's digest, and the prev-digest link, live in the envelope, not smeared into the payload record).

Sema itself is **sequence-addressed, not content-addressed** (per the task's ground truth: `SnapshotIdentifier(u64)`, `CommitSequence` monotonic). blake3-via-`ObjectDigest` is the reuse candidate for the per-entry/prev-entry digest the log-versioning direction calls for. It is a pattern to lift, not a crate to depend on blindly — `ObjectDigest` lives in a Signal *wire* contract (`signal-criome`), so reuse means lifting the blake3-into-typed-newtype shape into the storage layer, not importing criome's wire vocabulary into the kernel.

## The atomic-ingest precedent: repository-ledger spool + the CriomOS hook

repository-ledger is the existing event-shaped server-ingest precedent, and it demonstrates **two stacked atomic mechanisms** — one at the writer (the hook) and one at the reader (the daemon spool ingester).

### Writer side — temp-write + atomic rename (CriomOS hook)

`CriomOS/modules/nixos/repository-receive.nix` is the Gitolite post-receive hook. It writes payloads to **hidden temp files** then renames to the visible name:
- temp paths are dotfiles: `.{timestamp}-{repo}-{pid}.spool.tmp`, `.{...}.commit-observations.tmp`, etc. (`repository-receive.nix:62-66`);
- the final, visible name is `{timestamp}-{repo}-{pid}.nota` (`repository-receive.nix:67`);
- spool dir is `/var/lib/repository-ledger/spool` (`repository-receive.nix:24`).

The CLI is tried **first** against the daemon socket `/run/repository-ledger/repository-ledger.sock` (`repository-receive.nix:25,76`); the spool file is a **fallback** only when CLI submission fails (`repository-ledger/INTENT.md:35-36`, `ARCHITECTURE.md:6-10`). Atomicity comes from POSIX `rename(2)` being atomic on the same filesystem: a reader scanning for `*.nota` never sees a half-written file because partial writes are under a dotfile/`.tmp` name.

### Reader side — scan, decode, store, then move-to-processed (daemon)

`repository-ledger/src/spool.rs` `SpoolDirectory::ingest_into` (`spool.rs:40-67`):
1. ensure a `processed/` subdir (`spool.rs:44-45`);
2. collect only `*.nota` files (skips temp/dotfiles) and **sort** them — deterministic ingest order (`spool.rs:48-57`);
3. per file: `SpoolNotificationFile::from_path(...).decode()` parses the NOTA into a typed `ReceiveHookNotification` (`spool.rs:61`, decoder `spool.rs:89-113`), `store.record_hook_notification(...)` commits it (`spool.rs:62`), then `move_to_processed` renames the consumed file into `processed/` (`spool.rs:63,69-75`).

The **commit-then-move ordering** is the recoverable-ingest guarantee: the store commit happens before the source file is removed from the inbox, so a crash between steps leaves the file re-ingestible (at-least-once). Move is again an atomic `fs::rename`. This is the precedent for "consume a shipped log suffix without losing it on crash."

### What this gives a server-backed-log design — and what it does NOT

- It establishes a **proven local same-host atomic spool**: temp+rename to publish, scan-sorted, commit-before-remove to consume. A backup-ingest endpoint can reuse this exact shape for landing shipped suffixes.
- The store commit itself is the sema-engine transaction; the spool only feeds it. The free-atomicity property (log written in the same redb txn as data) lives in sema-engine, not in the spool.
- **It is NOT cross-host yet.** Both the hook and the daemon run on the same host writing/reading one local directory. `SetMirror(MirrorPolicy)` is explicitly **future** vocabulary (`meta-signal-repository-ledger/INTENT.md:31`: "future mirror target policy"; `repository-ledger/ARCHITECTURE.md:47`: GitHub mirroring execution is out of the first slice; `repository-ledger/INTENT.md` anti-patterns: this component does not own mirroring execution). So **no actual ship-to-server is wired anywhere** — there is a policy noun reserved and a local atomic-ingest mechanism proven, but the network hop and the remote-durability levels (local-committed / queued / server-committed) are unbuilt. The reusable VC library is the thing that would build them.

## The library-vs-shared-infra boundary

The task's discipline is "one redb file per component; no shared sema daemon; each component owns its own engine handle." The cluster facts let the boundary be drawn precisely:

- The **library** (linked code: generic types/traits for log-versioning, digest-linking, suffix-shipping) compiles into each component and respects per-component file ownership. No daemon shared.
- The **server/mirror** is shared infra: the **ingest target is ouranos** (GitoliteServer + TailnetController — the host where shipped suffixes land), the **bulk-storage / cache target is prometheus** (Btrfs CoW + the `criome-backup` SSID), and the **transport is the tailnet** (ouranos controller, all else clients). The library ships suffixes over the mesh to a server-side ingest that reuses the repository-ledger spool shape; the server is one shared endpoint, not a shared engine handle. That split — linked library per component, one shared ingest endpoint reachable over the tailnet — is the boundary the design must hold.

