# 66 · Cloud-operator handoff — land DigitalOcean Phase-1 live + harden (2026-06-19)

For **cloud-operator**. Tier-1 live is proven; the work below is the
integration + hardening that belongs on `cloud` main (your lane) plus the
Tier-2 live run. Incorporates the review you fed back through the psyche —
your adapter-scope, delete-before-assert, write-scope-probe, missing-sweep,
flake-path, and lock points are all reflected here.

## 1 · Context — what's proven, and where it lives

- **Tier-1 live PASSED** against real DigitalOcean (report 64 §1 update):
  SSH key registered → droplet `578840636` (`Initializing` → `Running`,
  public IPv4 `157.230.0.136`) → destroyed `Ok(())` → post-run sweep showed
  zero leftover droplets. Cold build 1m17s, lifecycle 29.6s, sub-cent.
- **The verified artifacts are NOT on main.** They live in a disposable
  clone at `/tmp/cloud-livetest` (at committed `0768326`) and in report 64:
  the compiling test (§2.1) and the corrected rkyv encoder (§3.1). Landing
  them on `cloud` main is this handoff.
- **Token reality:** stored at gopass `digitalocean.com/api-token` (the
  `.com` domain form, like `dolthub.com/api-token`). It is a scoped token
  with `droplet` + `ssh_key` (read+write confirmed by the live create) but
  no `account` scope — irrelevant, the adapter only hits `/v2/account/keys`
  and `/v2/droplets`. Your point stands: a 403 on `/v2/account` proves
  nothing about adapter usability.
- **Image home decided:** Spirit `ad53` (Decision, Medium) — *[cloud-node
  OS images live in CriomOS as a CloudNode-species profile … the cloud
  daemon references the image by id through the existing HostPlan
  image_name field]* — report 65. Your "keep it design until psyche
  confirmation + Spirit capture" caution is now satisfied (psyche confirmed
  the placement; `ad53` recorded). No wire change is needed — `image_name`
  is already plumbed end to end.

## 2 · Actions (prioritized)

### P0 — Commit the flake.nix gopass `.com` fix

`/git/github.com/LiGoldragon/cloud/flake.nix` carries an **uncommitted**
change (` M flake.nix`) moving the DO gopass path from `digitalocean/api-token`
to `digitalocean.com/api-token` at lines 71 and 91 — which matches where the
token actually lives. Verify authorship, then commit to main. Until it's
committed, any fresh checkout / the `/tmp` clone still wraps the daemon with
the wrong secret path (Tier-1 is unaffected only because the token is
exported manually; the nix `doctl`/daemon wrappers are not).

### P1 — Land the Tier-1 live smoke test, hardened

Add `tests/digitalocean_live.rs` (verified, compiling content in report 64
§2.1) — `#[ignore]`-gated. Two hardenings your review correctly demands
before it can be called panic-proof:

- **RAII teardown guard.** Wrap the created `HostIdentifier` in a `Drop`
  guard whose `drop` issues `delete_server`, so a panic / ctrl-c / process
  kill *between create and the delete call* still destroys the droplet. The
  current test deletes before asserting (covers the assert-failure path) but
  a kill in the create→delete window still leaks. The external bash sweep I
  ran is a one-off, not in the repo — a `Drop` guard is the durable fix.
- **True free write-scope probe.** `ensure_ssh_key` only writes if no key
  matches by name/public-key; if `criome-test` already exists it's a bare
  `GET`, making droplet-create the first write. Use a unique per-run key
  name (nonce-suffixed) and delete it in teardown, or assert the key is
  absent first — so "free write-scope check before any cost" actually holds.

### P1 — Add the rkyv config encoder (unblocks Tier 2 + deploy)

Add `examples/write_config.rs` (corrected in report 64 §3.1: plain struct
literal, `u32` socket modes, `CloudDaemonConfigurationFile::new(&out).write_configuration`).
Today the rkyv `DaemonConfiguration` writer is library-only / `#[cfg(test)]`,
so there is no command-line way to emit the daemon's single startup
argument. This is the one missing piece for booting `cloud-daemon` by hand
and for the deploy/bootstrap config-encode path.

### P2 — Add a DO-enabled daemon package variant

`packages.default` builds default features (`["cloudflare"]`) and passes no
override, so `nix run .#daemon` yields a daemon **without** the DO provider
(capabilities answer `NotBuilt`). Add a package variant with
`buildFeatures = [ "digitalocean" "cloudflare" ]`. The `cloud-daemon` gopass
wrapper (flake.nix:91) already injects `DIGITALOCEAN_ACCESS_TOKEN`, so a
feature-enabled `nix run` boots a DO-capable daemon with the token wiring
done.

### P2 — Run the Tier-2 full-daemon live chain

Once the encoder (P1) + package variant (P2) land, drive report 64 §3:
boot `cloud-daemon` over its sockets, then `RegisterAccount` →
`PrepareHostPlan(Create)` → `ApprovePlan` → `ApplyPlan` → `Observe(Servers)`
→ `PrepareHostDestruction` → `ApprovePlan` → `ApplyPlan` →
`Observe(Servers)`-gone, against live DO. **Watch:** report 64 flags the
Tier-2 NOTA strings as schema-inferred — field order was verified against
the `meta-signal-cloud`/`signal-cloud` source by the report's verify pass,
but not yet round-tripped through the actual `meta-cloud`/`cloud` parser, so
expect to debug a parse rejection or two on the first run. I can drive this
in the disposable clone first if you'd rather I de-risk the NOTA before it
touches your integration flow — say the word.

## 3 · Coordination

- **Lock:** I am not holding `cloud-designer.lock` because my work is in
  claim-exempt surfaces (`reports/cloud-designer/`), a disposable `/tmp`
  clone, and Spirit — none are shared locked resources, and I deliberately
  leave the canonical `cloud` repo unlocked so you can integrate. Claim
  `cloud-operator` on `/git/github.com/LiGoldragon/cloud` when you start the
  P0–P2 work.
- **Branch flow:** P0–P2 are code-repo `cloud` changes — yours to land on
  main (designers stage on `~/wt` feature branches; you own main + rebase).
  The verified sources to lift from are in report 64 (§2.1 test, §3.1
  encoder) and this brief.
