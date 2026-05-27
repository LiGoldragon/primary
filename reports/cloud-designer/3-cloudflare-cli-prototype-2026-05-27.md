# 3 · Cloudflare CLI prototype — branched-worktree mockup

Designer mockup-on-worktree per intent 502–504 + 515. Probes
psyche intents 914–919 (old NOTA stack, working tool via CLI,
DNS get/set as first action, redirects as stretch, Cloudflare CLI
as the first adapter to investigate, cloud-designer prototype
directive). Pairs with cloud-operator's parallel working-tool
effort; the two probe the same surface from designer/implementer
angles.

## Worktree + branch

| | |
|---|---|
| **Worktree path** | `/home/li/wt/github.com/LiGoldragon/cloud/designer-cloudflare-cli-prototype-2026-05-27/` |
| **jj bookmark** | `designer-cloudflare-cli-prototype-2026-05-27` |
| **Branch base** | `main` at `f09a7dd` (the existing read-path landing) |
| **Pushed to** | `origin/designer-cloudflare-cli-prototype-2026-05-27` |
| **PR URL** | https://github.com/LiGoldragon/cloud/pull/new/designer-cloudflare-cli-prototype-2026-05-27 |

## What the prototype adds

A single new module — `src/cloudflare_cli.rs`, 540 lines including
tests — wired into `lib.rs` under the existing `cloudflare` Cargo
feature, plus `serde_json` added to that feature. The module
ships:

- `FlarectlApi` struct that implements the existing
  `cloudflare::Api` trait (`zones`, `records` read paths) by
  shelling out to `flarectl --json` and parsing stdout. Drop-in
  parallel to `HttpApi` — anything that takes `Arc<dyn Api>`
  works with either.
- Inherent mutation methods on `FlarectlApi`:
  `create_record`, `create_or_update_record`, `delete_record`.
  These are not on the `Api` trait (kept stable) but live where
  callers find them.
- Typed newtypes carrying the flarectl-side vocabulary:
  - `FlarectlBinary(String)` — overridable binary path with a
    `default()` of `"flarectl"`.
  - `FlarectlDnsMutation` (enum `Create | CreateOrUpdate`) —
    closed selector for the mutation subcommand, no string
    typification.
  - `FlarectlRecordIdentifier(String)` — flarectl-issued DNS
    record ID, used for `delete_record`.
  - `FlarectlRecordKindName(&'static str)` — the cloudflare wire
    spelling (`A`, `AAAA`, `CNAME`, …) with `from_signal_kind`,
    `parse`, and `to_signal_kind` methods for round-tripping
    against `signal_cloud::RecordKind`.
- `CommandRunner` trait + `ProcessRunner` production impl. Tests
  swap in a `CapturingRunner` that records the (binary, argv)
  tuple passed in, so the test surface verifies the spawned
  command-line without ever touching a real process.
- 10 unit tests covering: zone-list argv shape, client-side zone
  filtering, dns-list keyed by zone name, dns-create argv shape,
  proxy flag conditional emission, create-or-update subcommand
  selection, delete argv shape, record-kind round-trip, default
  binary, binary override propagation.

Full test suite passes (21 tests — 10 new + 11 pre-existing
integration). `cargo check --all-targets` is clean.

## Surveyed flarectl surface

Inspected via `nix run nixpkgs#flarectl -- <subcommand> --help`
(version `dev` per the binary's self-report). Live API calls
deliberately not attempted; the prototype proves the spawn shape
and the JSON-parse shape via mocks, leaving live verification to
cloud-operator with a real Cloudflare account.

| Action | Command | Status |
|---|---|---|
| List zones | `flarectl --json zone list` | Supported. No name filter at CLI; client filters in adapter. |
| List DNS records | `flarectl --json dns list --zone <name>` | Supported. Zone identified by **NAME**, not by Cloudflare zone ID. |
| Create DNS record | `flarectl --json dns create --zone --name --type --content [--proxy] [--ttl] [--priority]` | Supported. |
| Upsert DNS record | `flarectl --json dns create-or-update ...` | Supported. |
| Update DNS record | `flarectl --json dns update --zone --id --name --type --content` | Supported (prototype routes upsert through `create-or-update` instead). |
| Delete DNS record | `flarectl --json dns delete --zone <name> --id <record-id>` | Supported. |
| List redirects | `flarectl --json pagerules list` | Supported. |
| **Mutate redirects** | — | **Not supported.** flarectl's `pagerules` subcommand has `list` only — no create/update/delete. |

Auth: `CF_API_TOKEN` environment variable (also `CF_API_KEY`
legacy form). The adapter injects `CF_API_TOKEN` from the
`signal_cloud` credential handle when spawning.

Account: `--account-id` global flag or `CF_ACCOUNT_ID` env var.
Not currently wired in the prototype — single-account flow only.
If cloud-operator's first production case is single-account,
nothing to do; if multi-account, add the flag wiring.

## Findings — CLI vs HTTP API for the first integration

**Flarectl works cleanly for DNS get/set.** All six surveyed
DNS subcommands have the right shape, return parseable JSON,
and accept a token via the standard env var. Auth model maps
directly to the existing `CredentialHandle` → env-var pattern
(intent 682), so the credential-source plumbing in
`cloudflare.rs` doesn't move.

**Flarectl is unfit for the redirects stretch goal.**
`pagerules list` is read-only — there is no
`pagerules create/update/delete` in the flarectl tree. Two
exit paths:

1. **Use direct Cloudflare API for redirects** (Page Rules at
   `/zones/{id}/pagerules`, or the newer Rulesets at
   `/zones/{id}/rulesets/.../http_request_dynamic_redirect`),
   reuse the existing `HttpApi` for that leg only.
2. **Use a different CLI for redirects.** `wrangler`
   (Cloudflare's Workers CLI) handles some of this surface but
   redirects via Workers Rules is a different abstraction
   (Custom Domains, redirect rules in dashboard, etc.).
   Adds another binary dep + a second auth path.

The first path is operationally lighter: keep flarectl for
DNS, fall through to `HttpApi` for redirects. The cloud
component already has `HttpApi`; nothing new to deploy beyond
flarectl itself.

**Zone identifier semantics differ between the two adapters.**
The existing `HttpApi::records(token, zone: &ZoneIdentifier)`
passes the Cloudflare-internal zone ID (a hex string from
`/zones`). flarectl's `dns list --zone` takes the zone *name*
(`example.com`). The prototype handles this by interpreting the
`ZoneIdentifier` newtype's inner string as the zone NAME when
the FlarectlApi adapter is in play.

If the cloud component wires both adapters at runtime, this is
a hazard — the contract uses one `ZoneIdentifier` type but the
two adapters mean different things by it. Two clean fixes:

- **Always resolve to zone-name at the adapter boundary** so
  `ZoneIdentifier` carries the name. Cheap if HttpApi can be
  taught to look up by name first; `cloudflare-go` exposes
  this.
- **Have FlarectlApi do an internal name→ID lookup** via
  `flarectl --json zone list` to keep the contract's semantic
  stable. Costs one extra spawn per request unless cached.

**Spawn-per-request is the obvious cost.** Each call to
`zones` or `records` spawns a flarectl process. Acceptable for
the first production slice (a handful of records, occasional
plan apply) but flagged as the long-run cost. Direct HTTP API
keeps a single process and amortises the credential
verification.

## What still needs design / a contract update

- **`signal_cloud::ApiRecord` lacks a `RecordIdentifier` field.**
  The flarectl `dns list --json` output includes an `ID` per
  record (captured locally as `FlarectlRecordIdentifier` and
  marked `#[allow(dead_code)]` in the prototype's
  `FlarectlRecord` struct). Without that identifier propagating
  to `ApiRecord`, the `apply_plan` deletion path
  (`record_names_to_delete`) can only delete *by name* — which
  means an extra `list → match → delete by id` round-trip per
  deletion. Adding `identifier: RecordIdentifier` to
  `ApiRecord` and threading it through the Cloudflare adapters
  closes this gap.
- **`Plan` model assumes name-keyed deletion** (`record_names_to_delete`).
  Cloudflare DNS does not enforce uniqueness on
  (zone, name, type) — multiple records can share a name and
  type — so the deletion-by-name semantic loses information.
  Either narrow the contract (delete by full key including
  value or by identifier), or accept the lossy semantic and
  document it.
- **Proxy mode isn't part of `Plan.records_to_create`.** The
  contract's `DomainNameSystemRecord` carries `proxy_mode`
  (Direct vs ProviderProxy), but the prototype currently
  doesn't connect that to the plan's record-create path — the
  cloud-operator implementation should make sure the proxy
  flag flows from Plan through to `flarectl --proxy`.
- **Multi-account support** via `CF_ACCOUNT_ID` is not wired.
  Single-account is fine for the first production target;
  multi-account needs `account_id: Option<&str>` plumbing
  through `FlarectlApi`.

## Recommendations for cloud-operator's working tool

- **Reuse the `Api` trait abstraction.** Both `HttpApi` and
  `FlarectlApi` implement it; the daemon can switch between
  them via the `ProviderClient::new(api, credentials)`
  constructor without touching the Store layer.
- **Adopt the `CommandRunner` trait** for any shell-out path —
  it makes the production daemon testable without forking
  processes in CI.
- **Default to flarectl for DNS, HttpApi for redirects.** Hybrid
  adapter; both already exist; no new dependencies beyond
  packaging flarectl in the cloud daemon's nix closure.
- **Add flarectl to the cloud component's flake.** `nixpkgs#flarectl`
  is available; add it as a runtime dep so `cloud-daemon`
  doesn't rely on whatever happens to be on PATH.
- **Live-test the JSON field-name guesses.** The prototype
  assumes flarectl emits `ID`, `Name`, `Type`, `Content`,
  `Proxied` (PascalCase, matching cloudflare-go's struct field
  tags). This is a strong guess but unverified against a live
  account. cloud-operator's first integration call should
  capture an actual JSON response and confirm the field names
  before relying on the parse.

## Intent records this prototype anchors against

| # | Kind | Magnitude | Substance |
|---|---|---|---|
| 502–504 | Decision | n/a | Mockup-on-worktree method for designer-side probes. |
| 515 | Decision | n/a | Designer lanes work on feature branches under `~/wt`. |
| 914 | Decision | Maximum | Cloud component uses the old NOTA / old signal_channel stack. |
| 915 | Decision | Maximum | Working cloud tool invoked through the cloud CLI. |
| 916 | Decision | Maximum | DNS get/set is the first useful action. |
| 917 | Decision | Medium | Redirects desired if Cloudflare surface supports cleanly. |
| 918 | Clarification | High | Investigate the Cloudflare CLI as the first adapter; preserve direct-API fallback. |
| 919 | Decision | High | cloud-designer's branched-worktree prototype directive (the trigger for this report). |
