# Repo-Operator Closeout — criome-auth witness full-chain landing

Authorized landing (psyche chose "land it + housekeeping") of the
independently-audited criome-auth witness full-body chain onto production main
lines, producers before consumers, derived from the witness `flake.lock` at
CriomOS-test-cluster `b0b30951`.

## Headline

WITNESS GREEN on prometheus at the landed chain, full-body `LANDED_BODY_REHASH …
MATCH`, native KVM boot. All target repos are on `main` at landed revs. Both
comment-only fixes applied. One pre-existing follow-up (spirit `--locked`
clippy/doc) and one major surprise (a concurrent operator + Spirit intent system
co-landed/recorded the same work) — both detailed below.

## (1) Land order executed + each repo's final MAIN rev

Dependency order, producers before consumers. "by me" = landed by this operator;
"by peer" = landed by a concurrent operator (see Surprises).

| # | repo | final `main` rev | notes |
|---|------|------------------|-------|
| — | signal-frame | `b78c80775c7f` (0.3.0) | already on main; unchanged |
| — | signal-mirror | `34ed3fdd429b` (0.1.1) | already on main; unchanged |
| 1 | meta-signal-spirit | `98704a3573cd` (0.4.0) | FF; by me; check green |
| 2 | signal-criome | `5976b2870e02` (0.6.0) | FF; by me; check green |
| 3 | meta-signal-criome | `1fc655bc6eaa` (0.3.0) | by me: repoint signal-criome→main + canonical fixture fix; check green |
| 4 | signal-router | `289c7de47d58` (0.2.0) | by me: rustfmt fix; check green |
| 5 | criome | `4c820a057c3c`* (0.4.3) | by me: repoint signal-criome+meta-signal-criome→main; check green. *Spirit INTENT record `3a13a3d3` later appended on top (non-code). |
| 6 | mirror | `5102f5ed87d1` (0.1.2) | FF; by me; raw check green |
| 7 | router | `14ed682b47bf` (0.4.1) | by me: rebased onto current main + repointed all wire/daemon deps→main; check green |
| 8 | spirit | `9e413baa9a9a` (0.19.0) | by peer; witness-green daemon; comment-fix(a) present. Full `nix flake check` RED on `--locked` clippy/doc (see §3, §7) |
| 9 | CriomOS | `0aae6cf22fee` | by peer: relock criome+router→landed mains. My equivalent driver build was green (exit 0). |
| 10 | CriomOS-test-cluster (witness) | `debd5dce68aa`* | by peer: relock criome/router/mirror/spirit→landed mains + comment-fix(b). *Spirit INTENT record on top (non-code); pins criome `4c820a05`, router `14ed682b`, mirror `5102f5ed`, spirit `9e413baa`. |

Wire generation consistent across the stack: signal-frame 0.3.0, signal-criome
0.6.0, signal-mirror 0.1.1, signal-router 0.2.0, meta-signal-criome 0.3.0,
meta-signal-spirit 0.4.0.

## (2) Rebases (main moved since branch fork)

- **router**: main had advanced 2 commits (Cargo.lock-only "align harness/signal
  lockfile"). Landed the witness family onto current main and fully repointed
  Cargo.toml deps (signal-router, signal-criome, criome, mirror) from their
  feature branches to `main`; regenerated Cargo.lock to landed mains
  (sema-engine `98ba507b`, signal-mind `eb2e0025` — exactly the verified router
  revs). Single clean landing commit; audited branch history retained on the
  origin feature ref.
- **spirit**: main had advanced 1 commit (`f64bc8a` 0.18.1 schema-10 legacy
  migration). The witness work was rebased onto it preserving
  `src/production_migration.rs`; meta-signal-spirit repointed to main; version
  0.18.1→0.19.0 (new ObserveHead/ObserveHeadObject operation roots). NOTE: this
  rebase was ultimately landed by the peer (`9e413baa`), not by me — my parallel
  rebase was discarded to preserve the peer's main (see Surprises).

## (3) Wire-bump dependents checked (HARD RULE) — no blocker

A read-only scout verified both bumps are strictly additive:
- **signal-criome 0.6.0**: trailing `node_identity.(Optional Identity)` on
  `CriomeDaemonConfiguration`. Other main consumers (orchestrate, mentci-egui,
  signal-mentci, signal-mentci-client, signal-orchestrate) only use the
  builder/unchanged types — none construct/exhaustively-destructure the record.
  COMPATIBLE.
- **signal-router**: trailing `AttestationIssuedAt`. Other main consumers
  (harness, introspect, persona) unaffected. COMPATIBLE.
- meta-signal-criome (only criome) and meta-signal-spirit (only spirit) have no
  external consumers.

**No stop-and-report blocker** — no existing main consumer breaks.

Out-of-scope observation (not introduced by this landing): `persona` carries a
pre-existing `RouterDaemonConfiguration` drift unrelated to these bumps.

## (4) Comment-only fixes applied

- (a) spirit `src/engine.rs` `observe_head` doc — `` `(Bytes 32)`/`FixedBytes<32>` ``
  corrected to `` `HeadDigestHex` String ``. Present in landed spirit `9e413baa`
  (the peer's landing carried the same fix).
- (b) witness `lib/mkCriomeAuthWitnessTest.nix` — reworded to "the store's
  content-addressed head over the imported record." Present in landed witness
  (`31f66748`→`debd5dce`). L5 framing kept as head-digest landing.

## (5) FINAL witness re-run on prometheus — WITNESS GREEN + full-body MATCH

Ran `nix run github:LiGoldragon/CriomOS-test-cluster/31f667481b1b#test-criome-auth-witness`
ON prometheus (the re-pinned-to-landed-mains witness). Native boot, exit 0.

```
RUN_HOST=prometheus  DATE=2026-06-29T11:55:25Z
system-features = nixos-test benchmark big-parallel kvm
node-b: QEMU running (pid 161526)   node-a: QEMU running (pid 161525)
node-a/node-b: connected to guest root shell
L2 OK: criome+router+spirit (node-a) and criome+router+mirror (node-b) active; distinct identities
L3 OK: meta Import receipt = (Imported (1 (1 11590050586725752087)))
L3 OK: ordinary working-socket Record refused fail-closed (guardian HarnessUnavailable)
L3 OK: real spirit versioned-log head (ObserveHead) = 326640ace33a02dac238e313cd91bcbd9a5a3dc75759fef49a3476e7fe35b85a
L3 OK: real head ENTRY BODY sourced (ObserveHeadObject); body octets = 320
L6a OK: unregistered signer refused (ForwardRefused AttestationInvalid); mirror head still empty
L6b OK: registered identity + foreign signature refused (ForwardRefused AttestationInvalid); mirror head still empty
L4: (ForwardAccepted 0)
L5 OK: real spirit head durably landed in the mirror; mirror head == 326640ace3…b85a
L5-body re-hash: LANDED_BODY_REHASH store=spirit octets=320 rederived=326640ace3…b85a carried=326640ace3…b85a expected=326640ace3…b85a MATCH
WITNESS GREEN (full chain): … the carried Append durably LANDED with head == the real spirit head; the landed BODY was read back over Restore and RE-HASHED IN THE VM through sema-engine to reproduce the real head — full-body replication, not just a digest. The registered matching key is the sole gate.
test script finished in 12.78s ; cleanup clean ; WITNESS_RUN_DONE exit=0
```

The witness pinned the LANDED daemon mains: criome `4c820a057c3c`, router
`14ed682b47bf`, mirror `5102f5ed87d1`, spirit `9e413baa9a9a` (CriomOS lib input
left at main `6646275d`, as in the verified lock — the witness does not exercise
CriomOS's modules). spirit `9e413baa` is digest-equivalent to any sema-0.6.3
relock (sema 0.6.2↔0.6.3 have an empty `versioning.rs` diff), so the result is
invariant to the open spirit `--locked` lockfile question in §7.

## (6) Per-repo checks on new main

`nix flake check` (on the prometheus remote builder) GREEN for: meta-signal-spirit,
signal-criome, meta-signal-criome (after canonical fixture fix), signal-router
(after rustfmt fix), criome candidate, mirror, router candidate. CriomOS:
`nix flake check` is pre-existing-broken at the eval stage (blueprint `//`
operator at flake.nix:136 — reproduces identically at the pristine `bf30751f`);
verified instead by building the `criome-auth-integrated-test` driver (exit 0)
with the landed criome+router. **spirit: full `nix flake check` RED** — see §7.

## (7) Open / dangling

- **Nothing of mine left dangling that should be published.** All 8 repos I
  landed are pushed with described commits; my superseded local candidates
  (spirit relock fragments, CriomOS `ebed2fca`) are orphaned (un-bookmarked) and
  correctly NOT pushed — the peer's `0aae6cf2`/`9e413baa` are authoritative.
- **spirit `--locked` clippy/doc check is RED (follow-up, NOT witness-blocking).**
  `spirit-clippy` and `spirit-doc` fail `cannot update the lock file … --locked`.
  Root cause is spirit's vendored-`[patch]` + `--locked --all-targets`
  resolution: the committed Cargo.lock must exactly match cargo's resolution
  after the flake redirects every git dep to a vendored path, and it does not.
  The peer's landing (`9e413baa`) left flake.lock sema-engine at `73eea24b`
  (0.6.2) while Cargo.lock pinned `98ba507b` (0.6.3); a delegated implementer
  reconciled that (and all daemon/contract locks to landed mains) in a candidate
  commit, but clippy/doc `--locked` STILL fail on a further vendored-resolution
  mismatch. This is a pre-existing structural fragility (the audit ran only the
  named `spirit-observe-head-object` cargoTest, not full clippy/doc `--locked`)
  — the spirit **daemon builds** and the **witness is GREEN**. Recommend routing
  to the spirit maintainer: either regenerate the patched-workspace lock inside
  the build, or drop `--locked` on the clippy/doc check derivations. I did NOT
  land a partial fix (it does not achieve green).

## (8) Surprises

1. **Concurrent operator (major).** A second operator ran this same brief in
   parallel. Work split unintentionally: I landed the wire crates + criome +
   router + mirror; the peer landed spirit (`9e413baa`), CriomOS (`0aae6cf2`),
   and the witness re-pin (`31f66748`), and committed a primary closeout
   (`efcffa1d` "record criome-auth chain landing to production mains"). Because
   the wire/daemon landings are deterministic fast-forwards, both operators
   converged on identical revs for the overlap. Per the jj discipline
   (remote-advanced → don't force) and the repo-operator contract (preserve peer
   edits), I accepted the peer's spirit/CriomOS/witness landings, discarded my
   parallel candidates, and did not overwrite shared mains. Recommend the psyche
   confirm whether two operators should be running this brief.
2. **Spirit intent records appended post-landing.** The Spirit intent system
   committed INTENT records on top of criome (`3a13a3d3`) and the witness
   (`debd5dce`) — non-code, do not change the landed behavior.
3. **Audited contract revs were not fully `nix flake check`-clean.** signal-router
   `d212ea8a` failed rustfmt; meta-signal-criome `4e5f1af3` had a stale 5-field
   canonical `Configure` fixture (signal-criome 0.6.0 made it 6-field); spirit
   has the `--locked` clippy/doc fragility. The audit validated witness behavior
   + the named checks, not every repo's full `nix flake check`. I fixed the
   first two deterministically as housekeeping (rustfmt; fixture sync) and
   reported spirit.

## Status

Landing COMPLETE; witness GREEN on prometheus with full-body MATCH at the landed
mains. One follow-up (spirit `--locked` clippy/doc) and a coordination question
(concurrent operator) for the psyche.
