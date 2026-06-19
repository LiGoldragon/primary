# cloud-audit 68 — completeness critic

Lane: completeness critic (modeled on report 702's completeness lane).
Scope: name what fell OUTSIDE the five lanes' frames — cloud surfaces and
claims no lane owned, and test-only-dressed-as-production claims the lanes
asserted but did not close.

Repo HEADs at audit time: cloud `3b38cdd` (one commit AHEAD of the digest's
`7f190c3` — see §6), signal-cloud `4e846bc`, meta-signal-cloud `54d62be`.

The five lanes did deep, correct work on the daemon spine, the provider
adapters, the wire contracts, the runtime/nix witness, and image-home/docs.
What follows is the negative space: the surfaces none of them put under their
lens, and the places where "live/proven/deployed" was asserted on a witness
that does not actually exist.

## The headline: no provider's "live" claim has a built-artifact witness

Three lanes lean on "DigitalOcean Tier-1 lifecycle is live-proven"
(reports 2, 4, and `active-repositories.md:91`). Pulled apart against the
actual artifacts, every provider fails the live-witness bar — each in a
different way, and no lane stated this as one unifying gap:

- **DigitalOcean** — the one "live-proven" provider. Its proof is
  `tests/digitalocean_live.rs`, which is `#[ignore]` by default
  (line 28: "live: spends real DigitalOcean money; needs
  DIGITALOCEAN_ACCESS_TOKEN + ssh-keygen"). The hermetic Nix check that
  references it, `checks.digitalocean-live-test-compiles`, runs
  `--ignored --list` (flake.nix:159) — it LISTS the test and runs nothing.
  So the only CI/Nix witness proves the live test *compiles*, never that it
  provisions. "Live-proven" is true only if a human ran
  `apps.digitalocean-live-test` with a real gopass token and watched stdout.
  No lane noted that the green-tier claim rests on an unrecorded, manual,
  money-spending run with zero durable witness. (Report 4's F4 came closest —
  "no nixosTest witnesses that the daemon serves or provisions" — but framed
  it as a daemon-lifecycle gap, not as "the Tier-1 claim itself has no
  reproducible artifact.")
- **Cloudflare** — the ONLY provider in `packages.default` (so the only one
  `nix run .#daemon` actually ships) — has NO live test at all. Its entire
  proof is `MockApi` in `tests/runtime.rs`. The provider that ships by default
  is the provider with zero live proof. No lane said this plainly; report 2
  noted Cloudflare's *error-fidelity* divergence but not that it has never
  touched a real Cloudflare account in any test.
- **Hetzner** — neither shipped nor live-tested (reports 2/4 covered the
  unshipped half well; the live-test absence is the same gap, completing it).

So the correct fleet-level statement is: **no cloud provider has a
reproducible artifact witnessing a live mutation.** That is a single P1 the
five frames collectively skirted.

## Unowned surface 1 — the CLI clients (the daemon's first client)

`src/client.rs` and the three bins (`src/bin/cloud.rs`,
`src/bin/cloud-daemon.rs`, `src/bin/meta-cloud.rs`) are a production-facing
surface no lane audited. This is the daemon's first client (the override's
"the CLI is the daemon's first client"), the thing an operator actually types.
Findings the five frames missed:

- `client.rs` is the real wire client: `send_working`/`send_meta` open the
  Unix socket, frame with `LengthPrefixedCodec`, and decode the generated
  `schema::lib` output (lines 49-113). It takes its domain *input* from the
  hand-written `signal_cloud::Operation` and bridges through
  `SchemaCloudInput` — so the CLI sits on the SAME two-tree straddle report 3
  flagged for the daemon, but report 3 only traced the daemon side. The CLI is
  a second consumer of the un-gated hand-written tree, doubling the drift blast
  radius report 3 measured.
- `CommandLineInput::from_arguments` (client.rs:122-145) enforces the
  one-argument override and rejects `--flags` — but the inline-vs-file
  discrimination is a `starts_with('(') || starts_with('[')` heuristic
  (line 139). A NOTA file whose path happens to begin with `(` would be read
  as inline text; a bare-atom operation that doesn't start with a bracket
  (none exist today, but the grammar permits top-level bare atoms per the
  workspace override) would be treated as a file path. Latent, unowned.
- **There IS a CLI→socket→daemon end-to-end test** — `tests/runtime.rs`
  imports `cloud::client::{Client, CommandLineInput, SchemaConnection}` and
  spawns the real `cloud-daemon` binary. The CLI surface is exercised; it just
  has no owning lane to say so or to assess it.

## Test-only-dressed-as-production claim 1 — report 1 P1-b and report 4 F1 overstate the daemon-lifecycle gap

Report 1 P1-b: "No live end-to-end test over the daemon socket lifecycle...
proving the provider edge but not register→prepare→approve→apply→observe
through the real kameo daemon, Store, and meta socket." Report 4 F1: "the only
live test drives HttpApi directly and never starts the daemon."

Both are **partly wrong against the source**. `tests/runtime.rs:292`,
`daemon_process_starts_from_binary_configuration_and_answers_working_request`:

- writes a real rkyv config via `CloudDaemonConfigurationFile`,
- spawns the real `CARGO_BIN_EXE_cloud-daemon` with the rkyv file as its
  single argument,
- waits for the real Unix socket, connects, and exchanges a real working
  `Observe Capabilities` request through the real kameo daemon spine,
  asserting `CapabilityState::Compiled` (cloudflare) / `NotBuilt`.

This test is in the hermetic `checks.test`, so the Nix gate DOES witness the
daemon booting from an rkyv file and answering a working request over its
socket. What is genuinely missing — and what the two lanes should have said —
is narrower: (a) no test drives the **meta socket** over the spawned daemon,
and (b) no test drives **provider apply** (register→prepare→approve→apply)
over the spawned daemon; those paths are proven only in-process against
`Store`, not through the kameo daemon binary. The lanes asserted "no daemon
lifecycle test exists" when in fact one exists and is CI-gated — they
overstated the gap by missing the working-tier daemon-spawn test entirely.

## Test-only-dressed-as-production claim 2 — report 1 P1-a contradicts report 4 F5 (the rkyv encoder)

Report 1 P1-a: "No built rkyv config encoder: the daemon's single argument can
only be produced by `#[cfg(test)]` code." Report 4 F5: "The config rkyv encoder
exists (`examples/write_config.rs`)." Both lanes audited the same HEAD; they
contradict. `examples/write_config.rs` exists and is a non-test target that
calls the public `CloudDaemonConfigurationFile::write_configuration`. Report 1
P1-a is **stale/wrong**; report 4 F5 is right (encoder exists) and its real
point stands (it's an `examples/` target with no `[[bin]]`/`apps.*` home and no
NOTA authoring file). A reader trusting both lanes gets a false "no encoder
exists" signal. The completeness verdict: the encoder exists but has no
deploy-stack home and hardcodes the `DaemonConfiguration` shape in Rust rather
than encoding typed NOTA — so the override's "encode typed NOTA into binary"
pipeline is still absent.

## Unowned surface 2 — meta-signal-cloud credential-handle custody is a wire-driven getenv

The prompt flagged this and no lane closed it. The custody chain:

- `meta_signal_cloud::CredentialHandle` (meta-signal-cloud/src/lib.rs:30) is a
  bare `String` newtype with no validation — any text is a valid handle.
- The daemon resolves a handle to a real token by treating the handle string
  **as an environment-variable name**: `std::env::var(handle.as_str())`
  (digitalocean.rs:84, cloudflare.rs:53, hetzner.rs analogue). The
  wire-supplied handle literally selects which process env var the daemon
  reads (`DIGITALOCEAN_ACCESS_TOKEN`, `cloudflare-dns-token`, etc.).
- The secret only enters the daemon's env via the flake's
  `wrapProgram ... --run 'export DIGITALOCEAN_ACCESS_TOKEN=$(gopass ...)'`
  (flake.nix:97-98). So custody = "whatever gopass secret was exported at wrap
  time," and the wire handle must coincidentally name that exact env var.

The seam — **wire handle string must equal a deploy-time env var name, with no
validation, no sealing, and no documented coupling** — is real production
surface no lane owned. The meta socket's `0o600` mode is the only thing gating
who can pick the env var the daemon reads; the handle is not a sealed reference
to a gopass path, it is a `getenv` key chosen over the wire. If the meta
socket's authority story ever weakens, this becomes arbitrary env-var
exfiltration of the daemon's process environment.

## Unowned surface 3 — schema_bridge.rs is the biggest file in the repo and is hand-written, un-gated

`src/schema_bridge.rs` is **107 KB — the largest source file, ~1.6x lib.rs**.
It is the hand-written translation between the hand-written public
`Operation`/`Reply` types and the generated `schema::lib` wire types; every CLI
input and every daemon reply passes through it (`SchemaCloudInput`,
`SchemaMetaInput`, `SchemaCloudOutput`, `SchemaMetaOutput`, and the
`LegacyObservation`/`LegacyValidation` converters). Report 3 named the *two-tree
drift* abstractly and the `ProviderProjection` micro-tax, but no lane named that
**the bridge between the trees is the single largest artifact in the
codebase**, is entirely hand-written, carries no freshness gate, and its
`Legacy*` naming frames the live path as migration glue. This is the cost report
3's P1 predicts, made concrete: collapsing the two trees would delete the
biggest file in cloud. No lane owned `schema_bridge.rs` directly.

`schema_runtime.rs` corroborates report 1's P2-b in its own doc-comment: "This
engine is still the pure schema/Nexus/SEMA experiment; the live `cloud-daemon`
currently uses the actor-native listener spine with the provider `Store`." The
dead-pilot finding is sound; the source itself admits it.

## Unowned surface 4 — no cloud daemon deployment exists anywhere

The prompt asks: did any lane assert "deployed"/"live" without a built-artifact
witness? `active-repositories.md:91` calls cloud a "Live runtime repo" with a
"live daemon spine." Grepping CriomOS, horizon-rs, and goldragon for
`cloud-daemon`, `cloud.sock`, or `cloud-meta` returns **nothing**. There is no
NixOS module, no systemd unit, no nixosTest, no host that runs the daemon. The
daemon has never been deployed. "Live runtime repo" describes a daemon that
compiles, boots from an rkyv file in a test tempdir, and answers a working
capability query in-process — not one that runs anywhere. No lane stated that
the deployment surface (the systemd/NixOS-module half of "live") is entirely
absent. Report 4's F4 ("no nixosTest") is the nearest neighbour but stops at
the test gate; it doesn't say there is no deploy unit in the consuming OS repos
either.

## Unowned cloud-adjacent change — horizon-rs `072334a` "add cluster domain configuration" (TODAY)

Report 5 correctly placed ad53's missing platform half (`NodeSpecies::CloudNode`,
the CriomOS gate module, the nixos-generators image output) in CriomOS/horizon-rs
and noted cloud CI never touches them. But it did not catch that **horizon-rs
changed today (`072334a`, 2026-06-19) with "add cluster domain configuration"** —
directly relevant to whether a baked CloudNode image can resolve a cluster
domain after boot, which is the next milestone after ad53. CriomOS also moved
today (`649fa8e` "update clavifaber for current nota-next"). Both are
cloud-adjacent changes that got no lane. The image-home milestone's platform
dependencies are actively moving and unaudited.

## Stale lane finding — report 5 F5's `active-repositories.md` claim is itself stale

Report 5 F5 says `active-repositories.md:91` "still calls cloud
'Documentation-only at birth.'" That line has since been **rewritten** — it now
reads "Live runtime repo... DigitalOcean Tier-1 lifecycle is live-proven
(reports 64, 66). Birth bead `primary-kbmi` is closed; live land + hardening is
tracked by `primary-hpkj`. In the kameo-fork camp." So report 5 F5 audited a
prior version of primary's main. The *new* line, however, carries the
unwitnessed "live-proven" claim this report's headline addresses — the staleness
moved, it didn't resolve.

## Cross-lane HEAD inconsistency

The lane digest pins cloud at `7f190c3`, but cloud's HEAD is `3b38cdd` — one
commit ahead ("cloud: harden DigitalOcean live test path"). That commit
rewrote `tests/digitalocean_live.rs` (+224 lines, the entire file as audited),
added `examples/write_config.rs` (+53), and reworked flake.nix (+92, including
the `digitalocean-live-test-compiles --ignored --list` check and the
`apps.digitalocean-live-test` app). So reports 2 and 4, which discuss the live
test and the flake in detail, were reading a version one commit stale from the
artifacts that exist now. Their structural conclusions survive (the live test is
still `#[ignore]`, the flake still ships cloudflare-only by default), but any
line-number citation into those two files is off by this commit. No lane flagged
that it was auditing behind HEAD.

## Severity-ranked gap summary

- **P1** No provider has a reproducible artifact witnessing a live mutation:
  DO live test is `#[ignore]` and its Nix check only `--list`s it; Cloudflare
  (the default-shipped provider) has no live test at all; Hetzner has neither.
  "Live-proven" rests on an unrecorded manual run.
- **P1** The CLI clients (`client.rs` + three bins) — the daemon's first
  client — are an unowned production surface; they sit on the same un-gated
  two-tree straddle report 3 flagged for the daemon, doubling its blast radius.
- **P1** meta-signal-cloud credential custody is a wire-driven `getenv`: the
  `CredentialHandle` (an unvalidated `String`) is used directly as an env-var
  name, gated only by the meta socket's `0o600` mode; no sealing, no documented
  handle↔env-var coupling.
- **P2** `schema_bridge.rs` (107 KB, largest file in the repo) is the
  hand-written, un-gated bridge between the two type trees and was owned by no
  lane; it is the concrete cost of report 3's two-tree P1.
- **P2** No cloud-daemon deployment exists in any consuming repo (no NixOS
  module / systemd unit / nixosTest); "Live runtime repo" has no deploy witness.
- **P2** Reports 1 P1-b and 4 F1 overstate the daemon-lifecycle gap — a
  CI-gated test (`runtime.rs:292`) spawns the real daemon binary and answers a
  working request over its socket; the true gap is narrower (meta socket +
  provider apply over the spawned daemon).
- **P3** Cross-lane contradiction: report 1 P1-a ("no rkyv encoder") is wrong
  and contradicts report 4 F5 (encoder exists).
- **P3** Cloud-adjacent repos moved today with no lane: horizon-rs `072334a`
  (cluster domain configuration — ad53's next milestone) and CriomOS `649fa8e`.
- **P3** Report 5 F5's `active-repositories.md` quote is stale (line rewritten);
  the new line carries the unwitnessed "live-proven" claim instead.
- **P3** Lanes audited cloud `7f190c3`; HEAD is `3b38cdd` — line citations into
  `digitalocean_live.rs`, `write_config.rs`, and `flake.nix` are one commit off.
