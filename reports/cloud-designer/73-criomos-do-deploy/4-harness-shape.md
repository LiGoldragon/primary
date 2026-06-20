# 4 · The re-usable CriomOS-on-DigitalOcean deploy test harness (2026-06-20)

LANE D. The psyche wants *re-usable test code* that: provisions a
DigitalOcean node **from a pre-made image**, optionally **publishes DNS**,
**deploys CriomOS**, **confirms**, and **always destroys**. This report
decides the harness's home and shape, specifies its parametrization,
always-destroy guarantee, witness output, and opt-in gating, and sketches
the file plus flake-app skeleton.

It builds directly on the proven Tier-1 lifecycle test
(`cloud/tests/digitalocean_live.rs`) and the existing
`digitaloceanLiveTest` flake app (`cloud/flake.nix:102`), and on the
image-home decision in report 65 (CriomOS owns the image *definition*;
cloud selects a snapshot id through the **already-present** `image_name` /
`ServerSpec.image` string — no wire change).

## Decision: option (a) — a new `tests/digitalocean_deploy_live.rs` + a flake `writeShellApplication`

**Recommended: extend the proven Rust-test pattern, not a standalone
shell app.** Concretely a new integration test
`cloud/tests/digitalocean_deploy_live.rs` plus a sibling flake app
`apps.digitalocean-deploy-live-test` that wraps it the same way
`digitaloceanLiveTest` wraps the lifecycle test.

Why (a) over (b) a standalone shell app:

- **Reuse of the exact adapter under test.** The whole point of the cloud
  daemon is that it drives DO via in-process REST
  (`digitalocean::HttpApi`), *not* doctl — doctl is not even installed. A
  Rust test calls `HttpApi::ensure_ssh_key` / `create_server` /
  `get_server` / `delete_server` directly (`src/digitalocean.rs:248-313`),
  so the harness exercises the production code path. A standalone shell
  app would have to re-implement droplet create/poll/destroy against the
  REST API in bash — a second, divergent client of the same endpoints,
  exactly the duplication report 65 §1(c) warns against. doctl is on PATH
  only as an operator debug shim (`flake.nix:65`), never the deploy path.
- **The cleanup drop-guard is the load-bearing safety mechanism.** The
  "ALWAYS destroys" requirement is met most robustly by a Rust `Drop`
  impl (`LiveCleanup`, `digitalocean_live.rs:215-224`): it fires on every
  exit path including `panic!`/failed `assert!`/`?`-early-return, holds
  the typed `HostIdentifier` + fingerprint, and retries. A shell `trap`
  covers signals and `set -e` exits but is easier to defeat (a `trap`
  reset, a subshell, a `kill -9`) and cannot carry typed state. We keep
  the Rust guard as primary and add a shell `trap` in the flake wrapper as
  a belt-and-suspenders *secondary* sweep (see §4).
- **Parametrization is cleaner in Rust + env.** Reading `std::env::var`
  with typed defaults from `digitalocean::DEFAULT_*` consts keeps the
  knobs in one place and lets the test fall back to the cheapest sane
  droplet when unset.
- **Opt-in gating already exists.** `#[ignore]` + a feature gate is the
  established way this repo keeps live tests out of CI spend
  (`digitalocean_live.rs:14,28`; `flake.nix:155` only ever runs the live
  test with `--list`, never executing it). We inherit that for free.

The standalone shell app (b) is rejected: it would either shell out to
doctl (not installed, not the deploy path) or re-roll the REST client in
bash (duplication + no typed cleanup). The flake *wrapper* is still a
`writeShellApplication`, but its body just injects the token and invokes
`cargo test` — it is a launcher, not a second DO client.

## What "deploy CriomOS" and "confirm" mean here (scope honesty)

This must be stated precisely so the harness doesn't over-claim. Two
deploy substrates are possible; the harness supports both via a mode
switch, and the **image** is what carries CriomOS:

1. **Image-as-deploy (primary, recommended default).** The pre-made image
   *is* the CriomOS `CloudNode` snapshot (report 65: built in CriomOS,
   uploaded to DO as a custom image / snapshot, referenced by **numeric
   id**). "Deploy CriomOS" = boot a droplet from that numeric `image_name`
   and **confirm the running system is the CriomOS node** — via SSH
   (`ssh root@<ipv4> nixos-version` / read `/etc/os-release` /
   `criomos`-marker file). No post-boot push step; the OS arrives in the
   image. This is the "up quickly" path the psyche asked for and the one
   report 65 designs the image pipeline around.
   - DO constraint (verified, current): *droplets can only be created in
     the same region as the custom image*; the image can be copied to
     other regions first. So `REGION` must match the image's home region
     (or the image must be multi-region). The harness surfaces a clear
     error if create fails with a region/image mismatch.
2. **Boot-then-activate (secondary mode).** Boot from a stock image
   (`DEFAULT_IMAGE`, `ubuntu-24-04-x64`) and confirm only SSH reachability
   — the existing Tier-1 already proves create→Running→destroy; this mode
   adds the SSH-reachability confirm without claiming a CriomOS push.
   Useful before the CriomOS snapshot exists. A future extension can run
   `nixos-rebuild --target-host` here, but that is **not** wired now and
   the report does not pretend it is.

**Verified vs inferred:**
- *Verified by reading code:* the adapter already routes `image_name` →
  `ServerSpec.image` → DO `image` field unchanged
  (`src/digitalocean.rs:444-455`, `DropletPayload.image`); `ssh_keys` are
  resolved name→fingerprint before the POST (`:274-292`); create/poll/
  destroy/ssh-key-delete all exist and are proven live (report 64: droplet
  `578840636` ran green, IPv4 `157.230.0.136`, destroyed, zero leftovers).
- *Verified by web (current 2026 DO docs):* a custom/snapshot image is
  passed in the **same `image` position as a numeric id**; droplets must
  be created in the image's region; `ssh_keys` accepts fingerprints. Cite
  [DO custom-images: create droplets](https://docs.digitalocean.com/products/custom-images/how-to/create-droplets/).
- *Inferred (NOT yet runnable):* that a *CriomOS* snapshot id exists in
  the DO account today. Report 65 designs the build/upload pipeline but it
  has not been executed; until a snapshot id exists, `CRIOMOS_IMAGE` is
  unset and the harness runs mode 2 (stock image + SSH-reachability
  confirm). The SSH *deploy-confirm* of an actual CriomOS marker is
  therefore **gated on the image existing** — the harness skips the
  CriomOS-marker assertion (printing `criomos-confirm: SKIPPED (no
  CRIOMOS_IMAGE)`) rather than failing, so it is runnable today and
  sharpens automatically once the snapshot lands.

## Parametrization — env vars with defaults

All knobs are environment variables so both the Rust test and the flake
wrapper read the same surface; every one has a default drawn from the
`digitalocean` module consts so an unset run still does something cheap
and safe.

| Env var | Default | Meaning |
|---|---|---|
| `DIGITALOCEAN_ACCESS_TOKEN` | (gopass `digitalocean.com/api-token`) | Required; injected by the flake wrapper, never echoed. |
| `CRIOMOS_IMAGE` | `DEFAULT_IMAGE` (`ubuntu-24-04-x64`) | Numeric snapshot id of the CriomOS image, or a stock slug. Presence flips mode 1 vs mode 2. |
| `DO_REGION` | `DEFAULT_REGION` (`nyc1`) | Must match the custom image's home region in mode 1. |
| `DO_SIZE` | `DEFAULT_SIZE` (`s-1vcpu-512mb-10gb`, ~$4/mo, sub-cent for minutes) | Droplet size slug. |
| `DEPLOY_DNS_DOMAIN` | unset | If set (e.g. `node1.example.com`), publish an A record → droplet IPv4 via the Cloudflare adapter, then delete it on teardown. Unset = skip DNS entirely. |
| `DEPLOY_SSH_CONFIRM` | `1` | When `1`, SSH to the droplet and read the OS marker; `0` confirms only `Running`+IPv4 (matches today's Tier-1). |
| `DEPLOY_POLL_SECONDS` | `5` | Poll interval. |
| `DEPLOY_POLL_ATTEMPTS` | `36` (3 min) | Max polls to `Running`. |
| `DEPLOY_SSH_ATTEMPTS` | `30` | Max SSH-reachability retries (~2.5 min) before confirm fails. |

The token is read in the test via `std::env::var` exactly as the Tier-1
does (`digitalocean_live.rs:30-32`); the flake wrapper sources it from
gopass when unset, mirroring `flake.nix:114-117`, and **never prints it**.

The DNS leg uses the existing Cloudflare adapter
(`src/cloudflare.rs`): `HttpApi::zones` to resolve the zone, `create_record`
to publish the A record, `delete_record` on teardown (trait at
`cloudflare.rs:59-81`). Its token comes from gopass `cloudflare/api-token`
via `CF_API_TOKEN` (the `flarectl` shim path, `flake.nix:46`); the harness
reads `std::env::var("CF_API_TOKEN")` and skips DNS with a printed notice
if the DNS domain is set but the token is absent. DNS requires building
with `--features digitalocean,cloudflare`.

## The always-destroy guarantee

**Primary — Rust `Drop` guard, generalized from `LiveCleanup`.** A
`DeployCleanup` struct holds every created resource as `Option<typed-id>`:
droplet `HostIdentifier`, SSH-key fingerprint, and (optionally) the
Cloudflare `(ZoneIdentifier, RecordIdentifier)`. Each teardown method
`take()`s its field, calls the delete, and re-stores the id on failure so
`Drop` retries. `Drop` runs the same three deletes and logs (never
panics) on error. This fires on success, on `assert!` failure, on `?`
early-return, and on panic-unwind — the same property the Tier-1 relies on
(`digitalocean_live.rs:215-224`). DNS record is deleted **before** the
droplet so a dangling A record never outlives its target.

**Secondary — shell `trap` sweep in the flake wrapper.** After the
`cargo test`, the wrapper runs a best-effort name-prefixed sweep against
`/v2/droplets` (curl with the token, filter droplets whose name starts
with the harness prefix `criome-deploy-test-`, DELETE each) inside a
`trap '...' EXIT`. This catches the pathological case where the test
process is `kill -9`'d before `Drop` runs. It is idempotent and a 404 is
success (the adapter already treats 404-on-delete as success,
`digitalocean.rs:197`). The sweep is the only place the wrapper touches
the REST API directly, and only as a safety net, not the deploy path.

Naming makes the sweep reliable: every resource the test creates is named
`criome-deploy-test-<pid>-<nanos>` (extending the Tier-1's
`criome-live-test-…` convention, `digitalocean_live.rs:147`), so a prefix
match cannot collide with real droplets.

## The witness it prints

A single machine-greppable witness line on success, plus human-readable
progress lines (all to stdout, captured by `--nocapture`). The witness:

```
DEPLOY WITNESS droplet_id=<id> ipv4=<a.b.c.d> region=<r> image=<image_name> dns=<fqdn|none> deploy=<criomos-confirmed|ssh-reachable|running-only> result=OK
```

Progress lines mirror the Tier-1 style:
- `ssh key ready: <name> (<fingerprint>)`
- `droplet created: id=<id> name=<name> status=Initializing`
- `final observed: status=Running ipv4=<ipv4>`
- `dns published: <fqdn> -> <ipv4> (record <id>)` *(only if DNS on)*
- `criomos-confirm: <os-release line>` or `criomos-confirm: SKIPPED (no CRIOMOS_IMAGE)`
- `destroy issued: Ok(())` / `dns delete issued: Ok(())` / `ssh key delete issued: Ok(())`

The `deploy=` field is the honest confirm level: `criomos-confirmed` (mode
1, SSH read a CriomOS marker), `ssh-reachable` (SSH connected but no
CriomOS marker / stock image), or `running-only` (`DEPLOY_SSH_CONFIRM=0`).
The line is the parent agent's / operator's proof and the grep target for
any CI-adjacent assertion.

## Opt-in gating so CI never spends money

Three independent gates, all already established in this repo:

1. **`#[ignore]`** on the test fn with a money-warning reason string
   (`digitalocean_live.rs:28`). `cargo test` never runs it; only
   `-- --ignored` does.
2. **Feature gate** `#![cfg(feature = "digitalocean")]` (plus `cloudflare`
   for the DNS leg) so the file isn't even compiled into the default test
   binary (`digitalocean_live.rs:14`).
3. **Flake check runs `--list` only.** Mirror `flake.nix:155-161`: add a
   `digitalocean-deploy-live-test-compiles` check that runs
   `--test digitalocean_deploy_live -- --ignored --list` — it *compiles
   and lists* the test (catching bit-rot) but never executes it, so
   `nix flake check` stays free. The only way to spend money is to
   explicitly run `nix run .#digitalocean-deploy-live-test` or the
   `cargo test … -- --ignored` line by hand.

## File skeleton — `cloud/tests/digitalocean_deploy_live.rs`

```rust
//! Live CriomOS-on-DigitalOcean deploy harness (re-usable, Tier 1).
//!
//! Provisions a droplet FROM A PRE-MADE IMAGE (CriomOS snapshot numeric id
//! via CRIOMOS_IMAGE, or a stock slug), optionally publishes a Cloudflare A
//! record, confirms the node, and ALWAYS destroys every resource via a Drop
//! guard. `#[ignore]` + feature-gated so CI never spends money.
//!
//! Run:
//!   export DIGITALOCEAN_ACCESS_TOKEN=$(gopass show -o digitalocean.com/api-token)
//!   export CRIOMOS_IMAGE=<snapshot-id>        # optional; default = ubuntu-24-04-x64
//!   export DEPLOY_DNS_DOMAIN=node1.example.com # optional; needs CF_API_TOKEN + cloudflare feature
//!   cargo test --features digitalocean,cloudflare \
//!     --test digitalocean_deploy_live -- --ignored --nocapture
#![cfg(feature = "digitalocean")]

use std::time::Duration;

use cloud::digitalocean::{
    Api, DEFAULT_IMAGE, DEFAULT_REGION, DEFAULT_SIZE, HttpApi, Result as DigitalOceanResult,
    ServerSpec, Token,
};
use signal_cloud::{HostIdentifier, HostStatus};

/// Reads every knob from the environment with module-const defaults. A
/// data-bearing type so its methods are real methods, not free functions.
struct DeployParameters {
    image: String,
    region: String,
    size: String,
    dns_domain: Option<String>,
    ssh_confirm: bool,
    poll: PollBudget,
}

impl DeployParameters {
    fn from_environment() -> Self {
        // std::env::var(...).unwrap_or_else(|_| DEFAULT_*.to_owned()) per row
        // of the parametrization table; dns_domain = var("DEPLOY_DNS_DOMAIN").ok()
        // ssh_confirm = var != "0"; poll budget from DEPLOY_POLL_* / defaults.
        todo!("read CRIOMOS_IMAGE, DO_REGION, DO_SIZE, DEPLOY_DNS_DOMAIN, ...")
    }

    fn is_custom_image(&self) -> bool {
        // numeric id => a pre-made (CriomOS) image; a slug => stock.
        self.image.chars().all(|character| character.is_ascii_digit())
    }
}

struct PollBudget {
    interval: Duration,
    attempts: u32,
}

#[test]
#[ignore = "live: provisions a real DigitalOcean droplet (spends money); needs DIGITALOCEAN_ACCESS_TOKEN + ssh-keygen"]
fn criomos_deploys_on_digitalocean_and_always_destroys() {
    let token = Token::new(
        std::env::var("DIGITALOCEAN_ACCESS_TOKEN").expect("DIGITALOCEAN_ACCESS_TOKEN must be set"),
    );
    let parameters = DeployParameters::from_environment();
    let api = HttpApi::new();
    let key = TemporarySshKey::new("criome-deploy-test"); // prefix-named (see sweep)
    let mut cleanup = DeployCleanup::new(&api, &token);

    let fingerprint = api
        .ensure_ssh_key(&token, key.name(), key.public_key())
        .expect("ensure_ssh_key");
    cleanup.track_ssh_key(fingerprint);
    println!("ssh key ready: {} ({fingerprint})", key.name());

    let spec = ServerSpec {
        name: key.name().to_owned(),
        server_type: parameters.size.clone(),
        image: parameters.image.clone(),       // numeric CriomOS snapshot id, or slug
        ssh_keys: vec![key.name().to_owned()],
        location: Some(parameters.region.clone()),
    };
    let created = api.create_server(&token, &spec).expect("create_server");
    let identifier = created.identifier.clone();
    cleanup.track_droplet(identifier.clone());
    println!("droplet created: id={} status={:?}", identifier.as_str(), created.status);

    // poll to Running (same loop as Tier 1, budget from parameters.poll)
    let host = poll_until_running(&api, &token, &identifier, &parameters.poll)
        .expect("droplet reached Running with an IPv4");
    println!("final observed: status={:?} ipv4={}", host.status, host.ipv4.as_str());

    // optional DNS publish (cloudflare feature); cleanup tracks the record id
    let dns = if let Some(domain) = &parameters.dns_domain {
        Some(cleanup.publish_dns(domain, host.ipv4.as_str())) // skips+prints if no CF token / feature
    } else { None };

    // confirm: SSH read the OS marker when a custom image + ssh_confirm
    let deploy_level = confirm_deploy(&host, key.private_key_path(), &parameters);
    println!("criomos-confirm: {deploy_level}");

    // explicit teardown BEFORE asserts so the witness reflects a clean run;
    // the Drop guard still covers every early-return / panic path.
    let dns_field = dns.as_deref().unwrap_or("none");
    cleanup.tear_down_and_log(); // dns record -> droplet -> ssh key, each logged

    assert!(host.ipv4.as_str().contains('.'), "Running droplet must expose IPv4");
    println!(
        "DEPLOY WITNESS droplet_id={} ipv4={} region={} image={} dns={dns_field} deploy={} result=OK",
        identifier.as_str(), host.ipv4.as_str(), parameters.region, parameters.image, deploy_level,
    );
}

// TemporarySshKey: as in digitalocean_live.rs but the unique_name takes the
// prefix arg ("criome-deploy-test-<pid>-<nanos>") and it also exposes
// private_key_path() for the SSH confirm step.

// DeployCleanup: generalizes LiveCleanup — Option<HostIdentifier> droplet,
// Option<String> ssh fingerprint, Option<(ZoneIdentifier, RecordIdentifier)>
// dns. Methods take()/retry; impl Drop runs dns -> droplet -> ssh key and logs.

// confirm_deploy(): if parameters.ssh_confirm && custom image -> retry ssh
//   `root@ipv4 'cat /etc/os-release'`, return "criomos-confirmed" on a CriomOS
//   marker, "ssh-reachable" otherwise; "running-only" when ssh_confirm is off
//   or "...SKIPPED (no CRIOMOS_IMAGE)" when the image is a stock slug.
```

The free-function placeholders (`poll_until_running`, `confirm_deploy`)
are sketch shorthand; in the landed file they become methods on
data-bearing types per workspace Rust discipline — e.g. a `DropletPoll{
api, token, identifier }` with `.until_running(budget)`, and a
`DeployConfirmation{ host, key_path, parameters }` with `.level()`. The
sketch shows control flow, not final placement.

## Flake-app skeleton — `cloud/flake.nix`

Add next to `digitaloceanLiveTest` (`flake.nix:102`):

```nix
digitaloceanDeployLiveTest = pkgs.writeShellApplication {
  name = "cloud-digitalocean-deploy-live-test";
  runtimeInputs = [ pkgs.gopass pkgs.openssh pkgs.curl pkgs.jq toolchain ];
  text = ''
    if [ ! -f Cargo.toml ]; then
      echo "cloud: run this deploy live test from the cloud repository root" >&2
      exit 2
    fi
    if [ -z "''${DIGITALOCEAN_ACCESS_TOKEN:-}" ]; then
      DIGITALOCEAN_ACCESS_TOKEN=$(gopass show -o digitalocean.com/api-token)
      export DIGITALOCEAN_ACCESS_TOKEN
    fi
    # optional Cloudflare DNS token, only if a DNS domain is requested
    if [ -n "''${DEPLOY_DNS_DOMAIN:-}" ] && [ -z "''${CF_API_TOKEN:-}" ]; then
      CF_API_TOKEN=$(gopass show -o cloudflare/api-token) && export CF_API_TOKEN
    fi

    # secondary safety net: prefix-named sweep on EXIT (covers kill -9 of the
    # test before the Rust Drop guard runs). Idempotent; 404 == already gone.
    sweep() {
      ids=$(curl -fsS -H "Authorization: Bearer $DIGITALOCEAN_ACCESS_TOKEN" \
        "https://api.digitalocean.com/v2/droplets?per_page=200" \
        | jq -r '.droplets[] | select(.name|startswith("criome-deploy-test-")) | .id')
      for id in $ids; do
        curl -fsS -X DELETE -H "Authorization: Bearer $DIGITALOCEAN_ACCESS_TOKEN" \
          "https://api.digitalocean.com/v2/droplets/$id" || true
        echo "sweep: deleted leftover droplet $id" >&2
      done
    }
    trap sweep EXIT

    cargo test --features digitalocean,cloudflare \
      --test digitalocean_deploy_live -- --ignored --nocapture
  '';
};
```

Wire it into outputs alongside the existing app and check:

```nix
apps.digitalocean-deploy-live-test = {
  type = "app";
  program = "${digitaloceanDeployLiveTest}/bin/cloud-digitalocean-deploy-live-test";
};

# in checks: compile + list only, never execute -> nix flake check stays free
digitalocean-deploy-live-test-compiles = craneLib.cargoTest (
  commonArgs // {
    cargoArtifacts = digitaloceanCargoArtifacts;
    cargoTestExtraArgs =
      "--features digitalocean,cloudflare --test digitalocean_deploy_live -- --ignored --list";
  }
);
```

(`digitaloceanCargoArtifacts` already builds with `digitalocean,cloudflare`,
`flake.nix:80`, so the DNS leg compiles in the check with no new artifact
set.)

## How to run (operator / live)

```sh
cd /git/github.com/LiGoldragon/cloud
# mode 2 today (no CriomOS snapshot yet): stock image + ssh-reachable confirm
nix run .#digitalocean-deploy-live-test
# mode 1 once the CriomOS snapshot exists:
CRIOMOS_IMAGE=<numeric-snapshot-id> DO_REGION=<image-region> \
  nix run .#digitalocean-deploy-live-test
# with DNS:
CRIOMOS_IMAGE=<id> DO_REGION=<r> DEPLOY_DNS_DOMAIN=node1.example.com \
  nix run .#digitalocean-deploy-live-test
```

## Open items for the synthesis / operator

- **The CriomOS DO snapshot does not exist yet** (report 65 designs the
  build/upload; LANE A owns landing it). Until then the harness runs mode
  2 and prints `deploy=ssh-reachable`. This is a feature, not a blocker:
  the harness is runnable and useful *today* and sharpens to
  `criomos-confirmed` automatically when `CRIOMOS_IMAGE` is set.
- **Region binding.** In mode 1, `DO_REGION` must equal the image's home
  region (verified DO constraint). The synthesis should record the
  snapshot's region next to its id so callers set both.
- **CriomOS marker for confirm.** The confirm step needs a deterministic
  string to grep in `/etc/os-release` (or a `/etc/criomos-node` marker).
  LANE A/C should name it; the harness reads whatever they choose via a
  `CRIOMOS_MARKER` env (default a sensible `/etc/os-release` NixOS line).
- **Cost.** One `s-1vcpu-512mb-10gb` droplet for a few minutes is a
  fraction of a cent (report 64 measured the Tier-1 at sub-cent). Snapshot
  storage for the image is separate and owned by the image pipeline, not
  this harness.
