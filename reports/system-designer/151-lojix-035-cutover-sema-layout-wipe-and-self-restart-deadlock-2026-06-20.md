# lojix 0.3.5 cutover: the SEMA-layout wipe decision and the daemon self-restart deadlock

System-designer, ouranos, 2026-06-20. Continues 145–150. Read-only investigation
backing the cutover is in workflow `wgpnbwzra`; this report is the synthesis plus
the live-recovery narrative that produced it.

## Where the cutover stands

The cluster Rust→nightly migration is **complete** and ouranos's 0.3.5 build is
**green** (gen 125, `826j427r…`, confirmed `lojix-0.3.5`). The blocker is no longer
Rust — it is that upgrading every daemon to current code bumped contracts the
**persisted state and the hand-written config cannot satisfy**. A `Switch` attempt
to activate 0.3.5 took the daemon down; ouranos was rolled back to the working
0.3.4 generation and is stable.

## Two things broke at activation

### 1 · The daemon self-restart deadlock (now understood, recovery known)

`Switch` where target == daemon-host runs `switch-to-configuration switch` over a
**foreground ssh the daemon awaits**. Activation restarts changed units — including,
on the same host, `lojix-daemon` itself — killing the awaiting ssh and the in-flight
switch together. Activation aborted right after stopping the daemon; nothing
restarted it (down ~25 min until recovery).

Recovery that works: a **detached transient systemd unit via `ssh root`**
(`systemd-run --unit … --service-type=oneshot --wait`), which is PID-1-owned and
survives both the daemon restart and the ssh session. That is the deadlock-free
mechanism. In lojix's own code the only *implemented* deadlock-free system cutover
is `BootOnce` (it wraps activation in exactly this `systemd-run` shape and defers to
reboot). `Switch` has only the foreground `ssh_invocation` path.

ouranos was restored by switching the system profile 125→124 and activating the old
generation through a detached unit: `lojix-daemon` active (NRestarts=0), `mirror`
and `repository-ledger` active, zero failed units, boot default safe.

### 2 · SEMA engine storage-layout bump (the real cutover blocker)

The shared `sema-engine` (rev `73eea24`, 0.6.2) pins `STORAGE_LAYOUT = 5`
(`engine.rs:57`). On open it compares against the layout persisted in the store and
**hard-refuses** an older one. The deployed stores are older:

| Store | Path | Stored layout | Why it can't auto-upgrade |
|---|---|---|---|
| lojix | `/var/lib/lojix/lojix.sema` | 4 | lojix opens **without** versioning (`lib.rs:306`), so its versioned log is empty and the in-place refold (`rebuild_derived_slots`, gated on a non-empty versioned log) is unreachable → hard-fail |
| mirror | `/var/lib/mirror/mirror.sema` | 3 | opens **with** versioning, but 3→4 was the non-additive `RecordKey(String)` → `RecordKey{kind,value}` change (commit `909eaa0`), so the layout-3 versioned-log rkyv bytes can't be refolded by a layout-5 build → correctly refused |

**No migration tool exists.** `begin_import`/`replay_versioned` are tests-only,
require a *fresh* store, and `Engine::open` hard-fails before they're reachable. No
`migrate`/`wipe`/`import` subcommand ships in lojix or mirror. The error message's
"checkpoint import or versioned replay" clause is aspirational for the in-place case.

Plus two config-contract skews surfaced by the same upgrade:

- **repository-ledger** now rejects a `.nota` path (`daemon argument error: expected
  a signal-encoded file path`) — it accepts only a binary rkyv. Its CriomOS module
  (`repository-receive.nix:229`) hands it a raw `.nota` with no encoder step, and the
  repo ships **no** `repository-ledger-write-configuration` binary (only the library
  method exists).
- **clavifaber** config has 6 root objects; the nota-next-derived `ClaviFaberRequest`
  enum decodes exactly 2 (tag + one nested payload block). The hand-written string at
  `complex.nix:34-36` flattens the 5 struct fields as siblings of the tag = 6.

## The cutover plan

### Store disposition — wipe both (the decision that needs you)

Recommendation: **wipe + re-bootstrap** both `.sema` stores. They are pre-production
**projections**, not sources of truth — live NixOS generations + GC roots live on the
target hosts; the mirror is a re-syncable, idempotently-re-shipped copy. On next
start each takes the `StampFresh` path and creates a clean layout-5 store.

```
systemctl stop lojix-daemon ; rm -f /var/lib/lojix/lojix.sema          # keep bootstrap-datom.nota + generated-inputs/
systemctl stop mirror       ; rm -f /var/lib/mirror/mirror.sema*       # incl. any redb sidecar/lock
```

What is lost: the lojix-side operational ledger (event log, deploy-jobs, test-runs,
container lifecycle) and mirror retention-settings. **This is the one step that
contradicts a recorded principle** — Spirit `29pb` ("state loss is unacceptable") is
cited *in the engine* as the reason it refuses rather than rebuilds. The wipe is
defensible under no-backward-compat-pre-production, but it needs explicit psyche
confirmation because "export first" is effectively unavailable (open hard-fails
before any export API, and no layout-aware reader exists).

### Config fixes (needed regardless of the wipe answer)

- **clavifaber** — single-line `complex.nix:34-36` fix, wrap the payload in one nested
  block (2 roots) and drop the double-quotes (bare-atom paths). No Rust change.
- **repository-ledger** — add a 4th binary `repository-ledger-write-configuration`
  (mirrors `lojix-write-configuration`: reads one NOTA arg, builds the 6-field
  `DaemonConfiguration`, writes rkyv via the existing library method) + `Cargo.toml`
  `[[bin]]`; then rework `repository-receive.nix` to the lojix/mirror two-part shape
  (ExecStartPre encoder → ExecStart on the `.rkyv`).

### Activation

- **ouranos** — the *first* 0.3.5 bring-up is an out-of-band CriomOS switch by a
  deploying operator (lojix's store is just wiped; it isn't yet trusted to deploy
  itself). The first lojix-*driven* ouranos-from-ouranos deploy must be `BootOnce`
  + reboot (the only implemented deadlock-free self-cutover).
- **prometheus** — a different node, so a lojix deploy builds in prometheus's store
  and activates over ssh: **plain `Switch`**, no self-restart risk. `BootOnce` only
  for bootloader-touching changes.

### Ordered sequence

1. Land the config fixes (clavifaber + repository-ledger encoder + module) + repin.
2. Wipe both `.sema` stores on ouranos (pending the decision below).
3. Out-of-band CriomOS switch to 0.3.5 on ouranos.
4. Verify all four units active, no crash-loop, clean engine open, sockets bound,
   publication written.
5. First lojix-driven `BootOnce` self-deploy of ouranos → reboot → confirm.
6. Prometheus rollout via `Switch` (the durable-VM-host goal).

## Open questions for the psyche

1. **Wipe vs preserve (Spirit `29pb`).** Confirm wiping both `.sema` stores is right
   for pre-production, overriding `29pb` — or direct preservation (which requires new
   layout-aware-reader code that doesn't exist).
2. **repository-ledger redb store** (`/var/lib/repository-ledger/…redb`) — assumed
   untouched (no layout error reported); confirm.
3. **Encoder request shape** — default to lojix's `ConfigurationWriteRequest` pattern
   for repository-ledger; the designer sets the encoder type + `.nota` body together.
4. **First-deploy authority** — an operator/system-operator owns the first
   out-of-band ouranos switch; the `BootOnce` self-deploy test precedes prometheus.
5. **mirror re-ship completeness** — wiping mirror relies on every source shipper
   re-shipping; confirm all source components are live, and whether any
   mirror-only checkpoint artifact must be re-published from source first.

## Deferred captures (Spirit is down — store schema v10 vs deployed binary)

To record once Spirit recovers: the **nightly toolchain Correction** (cluster Rust is
newest nightly via fenix, not stable); the **Switch-self-deadlock Constraint** (a
daemon cannot Switch-activate a generation that restarts itself — use detached
activation / BootOnce+reboot); the **ssh-not-sudo** access model (root access on hosts
is via ssh key, not sudo); and, if approved, the **pre-production store-wipe**
disposition as it relates to `29pb`.
