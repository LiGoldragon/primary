# 60 · DigitalOcean provider landed — per-second target ready for live test (2026-06-19)

The per-second-billing provider the psyche asked for (Spirit `g7zd`) is built,
e2e-tested, and on main. Spec: report 59. This is the landing + the live-test
runbook.

## 1 · Landed + verified

- **signal-cloud** `main` = `4e846bc0` — `Provider::DigitalOcean` variant.
- **meta-signal-cloud** `main` = `54d62be8` — `Provider::DigitalOcean` variant.
- **cloud** `main` = `dfcf9e37` — the `src/digitalocean.rs` droplet adapter, the
  `digitalocean` feature, the generalized provider dispatch, the gopass shim,
  and `tests/digitalocean.rs`. Independent rebuild: green; **9/9 DO tests pass**
  including `full_host_lifecycle_runs_through_the_store_handlers`.

The `schema-rust-next` landmine recurred during the cloud repin and was
navigated again (surgical `--precise` pin-back to `733b76d3`/`abae95f9`); the
landed lock holds the working tooling.

## 2 · What's now real on main

Two compute providers behind one uniform surface:

- **Hetzner** (hourly) and **DigitalOcean** (per-second) — both expose
  create / observe / destroy + the full `PrepareHostPlan` →
  `PrepareHostDestruction` owner-approved lifecycle.
- **Provider dispatch generalized:** the host-plan apply and the `Servers`
  observe now route on the request's `Provider` (Hetzner → hetzner client,
  DigitalOcean → digitalocean client), with an honest `ProviderNotConfigured`
  rejection for any unbuilt/unsupported provider.
- **The Store path stays uniform across providers:** a plan carries an
  `ssh_key_name`; each adapter does the provider-specific key handling
  (Hetzner accepts names directly; DigitalOcean resolves name→fingerprint via
  `/v2/account/keys` inside the adapter before the droplet POST).

## 3 · Live-test runbook (when the DO token lands)

The only external input is a DigitalOcean personal access token at gopass
`digitalocean/api-token` (the daemon reads it as `DIGITALOCEAN_ACCESS_TOKEN`,
by-handle only, never echoed). Then:

1. **Register a throwaway test SSH key** in the DO account via the API (I do
   this with the token — `POST /v2/account/keys`, name e.g. `criome-test`), so
   the droplet is born SSH-able. No need to touch your personal keys.
2. **Run the daemon** (`--features digitalocean`, token injected) + the thin CLI.
3. **Drive the live cycle:** `RegisterAccount(DigitalOcean)` →
   `PrepareHostPlan(Create)` with `s-1vcpu-512mb-10gb` / `nyc1` /
   `ubuntu-24-04-x64`, `ssh_key_name=criome-test` → `ApprovePlan` → `ApplyPlan`
   (creates a real droplet) → `Observe(Servers)` until `active` with a public
   IPv4 → SSH in with the throwaway key to prove reachability →
   `PrepareHostDestruction` → `ApprovePlan` → `ApplyPlan` (deletes it) →
   `Observe(Servers)` shows it gone.
4. **Cost:** billed by the second; a full cycle is a fraction of a cent.
   Teardown `DELETE`s (a powered-off droplet still bills), so the meter stops
   immediately.

This is the real-world test of the whole Phase 1 chain — the daemon, the
sockets, the gopass auth, the live provider API, and the create/observe/destroy
lifecycle — against an actual provider, for pennies.

## 4 · Housekeeping

The landed feature worktrees + branches (`hetzner-compute`,
`digitalocean-provider` across the three repos) are now `==` their mains and
can be cleaned up (`jj workspace forget` + remove `~/wt/...` + delete the
bookmarks). Deferred; not blocking.
