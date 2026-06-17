# 57 · Hetzner compute provider — Phase 1 built + verified (2026-06-17)

Phase 1 of the on-demand cloud-node directive (Spirit `150a`) is implemented
and green across the cloud triad. This records what shipped, the independent
verification, the review fixes, the integration state, and what remains.

Design + spec: reports 56 (`56-cloud-onramp-hetzner-design.md`,
`56-hetzner-phase1-impl-spec.md`). This is the build record.

## What shipped — a bare cloud node, up/observe/down on demand

A Hetzner compute provider added to the shipped `cloud` daemon, mirroring the
proven Cloudflare-in-the-`Store` pattern. Built on a shared `hetzner-compute`
branch across three worktrees:

- **signal-cloud** (`1466d949`, pushed): the read-only compute wire vocabulary
  — `CloudHost`, `CloudHostListing`, `HostQuery`, `HostStatus`
  [Initializing Running Stopped Deleting Unknown], and a `Servers` arm on the
  `Observation` / `ObservationResult` roots. Green, 7 tests, fmt+clippy clean.
- **meta-signal-cloud** (`db013c92`, pushed): the owner-only mutation
  vocabulary — `DesiredHostState`, a dedicated `HostPlan` (not a union into the
  DNS `Plan`), `HostIntent` [Create Destroy], and a `PrepareHostPlan` op that
  reuses the existing `ApprovePlan` / `ApplyPlan` (a host plan flows through
  them keyed by `PlanIdentifier`). Green, 12 tests, fmt+clippy clean.
- **cloud** (`14bec6d5`, committed, **unpushed**): `src/hetzner.rs` — a
  `reqwest`-free blocking-`ureq` adapter (`trait Api` + `HttpApi` +
  `ProviderClient` + `EnvironmentCredentialSource`) speaking the Hetzner Cloud
  v1 REST API; the `Store` host handlers (observe → `Servers`; prepare →
  `HostPlan`; apply → synchronous create/destroy mirroring
  `apply_cloudflare_plan`); the `schema_bridge` Legacy↔Schema arms; the
  `hetzner` cargo feature; the `flake.nix` gopass shim. Green on
  `--features hetzner`, `default`, and `cloudflare hetzner`; fmt+clippy clean
  (`-D warnings`); 8 hetzner tests pass including a full
  `PrepareHostPlan → ApprovePlan → ApplyPlan` create round-trip through a mock.

`Provider::Hetzner` and the `(Hetzner, CloudHosts)` capability already existed
across the schemas + the matrix, so the directive landed on pre-scaffolded
ground — no new provider identity, just the missing record/adapter/handler/feature.

## Independent verification + review fixes

The build agents reported green; I rebuilt and re-tested independently
(`cargo build --features hetzner`, `cargo test`) — confirmed. The adapter is
discipline-clean: typed `Error` via thiserror, `HostMapping` / `HetznerStatus`
are data-bearing projection types (no free functions, no ZST holders), newtypes
throughout, serde only at the REST edge, direction-encoded names.

Adversarial review of the apply path caught two correctness gaps the green
build masked, both now fixed (`14bec6d5`):

1. **No SSH key on create (usability).** The create call passed an empty key
   list, so a provisioned node would be unreachable — defeating the whole
   point. Fixed: `ssh_key_name` from the `HostPlan` is threaded into Hetzner's
   `ssh_keys` create field (which accepts key *names*), so the node is born
   with the durable key attached and SSH-able on boot. The key must be
   pre-registered once as a Hetzner project resource — matching "the durable
   root key lives in the CriomOS flake / `datom.nota`."
2. **Destroy targeted the wrong path (bug).** Destroy built the Hetzner
   identifier from the node *name*, but `DELETE /v1/servers/{id}` needs the
   numeric server id. Fixed with `destroy_host_by_name`: resolve name→id via
   `list_servers`, then delete by id (a name with no live server is
   already-gone → success). Two tests added.

## Integration state — designer-built, operator-integrates

Per the designer/operator split, the contracts are pushed as the
`hetzner-compute` feature branch and the cloud branch is built green but
**unpushed**, pending the operator's main integration. Two integration notes:

- **The `links = "signal-cloud"` collision.** `meta-signal-cloud@hetzner-compute`
  still references `signal-cloud` via `branch=main`, while cloud needs
  signal-cloud's `hetzner-compute` branch; cargo forbids two `signal-cloud`
  sources. The build resolves it with a temporary `[patch]` pointing cloud's
  signal-cloud dep at the local worktree. **Clean integration must:** land
  signal-cloud + meta-signal-cloud on main, have meta-signal-cloud repin its
  own signal-cloud dep, then replace cloud's `[patch]` with branch/rev pins.
- The cloud branch tip is `14bec6d5`; the contract tips are `1466d949` /
  `db013c92`.

## The live run is psyche-gated

The build + the hermetic (mock-`Api`) tests need nothing external. The first
*real* spinup needs three things only the psyche/ops can provide:

1. A **Hetzner Cloud account** + an **API token** at gopass `hetzner/api-token`
   (the flake shim injects it as `HCLOUD_TOKEN`; the registered credential
   handle is the string `HCLOUD_TOKEN`). Never echoed.
2. The **durable CriomOS root SSH key registered once** as a Hetzner project
   resource, named to match the `ssh_key_name` used in the host plan.
3. A choice of **server_type** (default lean: CAX11 ARM ~€3.79/mo) and
   **image** for the create call.

## Remaining (Phase 2 — needs the psyche's forks from report 56 §7)

- **Install-hop ownership + nixos-anywhere orchestration** — turn the bare VM
  into a deployed CriomOS node. This is where the **deferred-effect/actor seam**
  becomes mandatory (the multi-minute install would freeze the single-mailbox
  daemon if run inline; Phase 1's fast REST calls don't). Built deliberately as
  its own effort.
- **The chicken-and-egg / spec-identity split** — the provisioning ledger
  joined in horizon `fill_viewpoint`.
- **A Destroy path on the wire** — `PrepareHostPlan` currently always builds
  `intent=Create`; reaching `Destroy` needs a contract affordance (the apply
  side already handles it correctly).
- **Default arch (ARM vs x86)** and the **contract-bump** for clean integration.
