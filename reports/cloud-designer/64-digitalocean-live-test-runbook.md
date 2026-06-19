# 64 · DigitalOcean live-test runbook (2026-06-19)

Concrete, copy-pasteable runbook for the first real DigitalOcean
lifecycle test of the `cloud` component. Synthesised from four
investigations (build verification, daemon startup, gopass shim, live
commands) and spot-checked against the canonical checkout at
`/git/github.com/LiGoldragon/cloud` (HEAD `0768326`, "use Kameo lifecycle
fork", working tree clean).

Two paths are offered, run them in this order:

- **Tier 1 — adapter-level live test** (section 2): drives
  `digitalocean::HttpApi` directly from a `#[ignore]` integration test.
  Fastest real signal, no daemon, no rkyv config, no sockets, no NOTA.
  Run this first.
- **Tier 2 — full daemon chain** (section 3): boots `cloud-daemon`,
  registers the account over the meta socket, drives the lifecycle over
  the ordinary socket with the thin CLIs. Exercises the whole production
  shape. Run this once Tier 1 is green.

The single hard blocker is a paid DigitalOcean token (section 5). Two
in-repo gaps make Tier 2 a couple-of-line patch away from one-command;
Tier 1 has no such gap.

## 1 · Readiness

### Build status — GREEN

A fresh depth-full clone of `main` builds green against the committed
`Cargo.lock` with `--locked`, with no `schema-rust-next`
`RetiredStructFieldSyntax` panic (the `--locked` flag is what
structurally prevents that landmine — no resolver drift can slip in).

| Check | Result |
|---|---|
| `cargo build --locked --features digitalocean` | Finished, no warnings/errors (~1m15s cold) |
| `cargo build --locked --features digitalocean,cloudflare` | Finished (incremental; CF + DO share `serde`/`serde_json`/`ureq`) |
| `cargo test --locked --features digitalocean --test digitalocean` | 9 passed, 0 failed |
| `Cargo.lock` drift after builds + tests | None (`git status --short Cargo.lock` empty) |

The 9 hermetic DigitalOcean tests are offline/mocked (one explicitly
checks `missing_credential`); they prove the pinned lock + provider code
compile and the Store/provider plumbing works, but they do **not** touch
the real DigitalOcean API. That is exactly what Tiers 1 and 2 add.

Binaries land under `target/debug/` (or `target/release/` for a release
build): `cloud-daemon` (the live DO daemon, entrypoint
`src/bin/cloud-daemon.rs` -> `CloudDaemonCommand::from_environment().run()`),
`cloud` (ordinary thin CLI), `meta-cloud` (meta thin CLI).

Recommended live build: `--features digitalocean,cloudflare` (DO compute
+ Cloudflare DNS, which ships under the `cloudflare` feature).
`digitalocean` alone also builds and passes tests if DNS is not needed.

### gopass shim status — COMPLETE (one path correction)

The gopass-to-env credential shim is **complete and correct end-to-end**
— there is no gap to close. `flake.nix` injects `DIGITALOCEAN_ACCESS_TOKEN`
in two places: the `doctl` debug-CLI wrapper (`flake.nix:71`) and,
load-bearingly, the `cloud-daemon` wrapper (`flake.nix:91`) that the
in-process REST adapter actually runs inside. The four-way name chain
agrees:

- wrapper sets `DIGITALOCEAN_ACCESS_TOKEN` (flake.nix:71, :91),
- `RegisterAccount` carries handle `DIGITALOCEAN_ACCESS_TOKEN` (tests/digitalocean.rs:123 etc.),
- adapter reads `std::env::var(handle.as_str())` (src/digitalocean.rs:84),
- documented const `TOKEN_ENVIRONMENT_VARIABLE = "DIGITALOCEAN_ACCESS_TOKEN"` (src/digitalocean.rs:79).

**Correction to the investigation input:** the gopass secret path is
`digitalocean.com/api-token`, **not** `digitalocean/api-token`. Verified
directly in `flake.nix:71` and `:91`. Use `gopass show -o
digitalocean.com/api-token` everywhere below. (Cloudflare and Hetzner do
use the bare `cloudflare/api-token` / `hetzner/api-token` form; DO is the
odd one with the `.com`.)

Two behavioural notes, neither a blocker:

- The daemon wrapper uses a `${VAR:-$(gopass ... 2>/dev/null)}` fallback
  that **silently swallows** a gopass failure (empty token, no `exit
  78`), unlike the loud `doctl`/`hcloud`/`flarectl` CLI wrappers. If
  gopass is unavailable at daemon start, the token is empty and the
  failure surfaces later as `Error::CredentialUnavailable` from the
  adapter, not at wrap time. Watch for this when debugging.
- Correctness rests on the registered handle string equalling the env
  var name; the const at `digitalocean.rs:79` is convention, not
  referenced by the read path. The integration tests assert the match,
  so `nix flake check` would catch a divergence.

### Daemon-startup mechanism — REAL, with a small encoder gap

There is no flag-driven or NOTA-driven daemon start: `cloud-daemon` takes
**exactly one rkyv file** as its single argument (workspace contract —
daemons accept binary startup only and reject inline NOTA / `.nota`
paths, asserted in tests/runtime.rs:274-289). The rkyv message is a
`DaemonConfiguration` carrying **only socket paths/modes, no token**
(src/lib.rs:149-155):

- `ordinary_socket_path`, `ordinary_socket_mode`,
- `meta_socket_path`, `meta_socket_mode`.

The canonical real boot is proven in-repo at tests/runtime.rs:291-323:
write the rkyv config via `CloudDaemonConfigurationFile::write_configuration`
(src/daemon_command.rs:83-90), then
`Command::new(cloud-daemon).arg(config.rkyv).spawn()`.

**The gap:** the rkyv writer is **library-only**, reachable today only
from `#[cfg(test)]` code. There is no `examples/` dir (confirmed:
`examples/` does not exist) and no standalone encoder binary or nix app
to emit a `DaemonConfiguration.rkyv` on the command line. So Tier 2 is
**not one command today** — you must add a tiny adapter (section 3.1) or
generate the rkyv from the existing test harness. This is the single real
gap between today's repo and a one-command live DO boot.

The DO provider is **feature-gated off by default** (default =
`["cloudflare"]`, Cargo.toml:27; `Store::new()` builds the DO provider
only under `#[cfg(feature = "digitalocean")]`, src/lib.rs:564-577). The
flake's `packages.default` passes **no feature override**, so `nix run
.#daemon` / `nix build` yield a daemon **without** the DO provider (DO
capabilities answer `NotBuilt` / `ProviderNotConfigured`). A live DO run
**requires** a `cargo ... --features digitalocean` build; the gopass
wrapper is only applied by the nix package `postInstall`, so under
`cargo run` you inject the token yourself (section 3).

## 2 · Tier 1 — adapter-level live test (run this first)

Fastest real signal. Drives `digitalocean::HttpApi` straight from an
`#[ignore]` integration test — no daemon, no rkyv, no sockets, no NOTA,
no account registration. If this is green, the adapter, token, and DO
account are all real and working.

### 2.1 Create the test file

Create `cloud/tests/digitalocean_live.rs`. The shape below mirrors the
typed values used in the hermetic tests and the `Api` trait
(src/digitalocean.rs:118-124); `ensure_ssh_key` must run before
`create_server`, which drops unknown SSH-key names (src/digitalocean.rs:268-286).
`delete_server` treats a 404 as already-gone (:196). `active` maps to
`HostStatus::Running` (:553). Defaults `DEFAULT_SIZE` / `DEFAULT_REGION`
/ `DEFAULT_IMAGE` live at :28-32.

```rust
#![cfg(feature = "digitalocean")]

use cloud::digitalocean::{
    Api, HttpApi, ServerSpec, Token,
    DEFAULT_SIZE, DEFAULT_REGION, DEFAULT_IMAGE,
};
use signal_cloud::HostStatus;

#[test]
#[ignore = "live: spends real DigitalOcean money; needs DIGITALOCEAN_ACCESS_TOKEN + DO_TEST_PUBLIC_KEY"]
fn digitalocean_full_lifecycle_runs_against_the_real_api() {
    let token = Token::new(
        std::env::var("DIGITALOCEAN_ACCESS_TOKEN")
            .expect("DIGITALOCEAN_ACCESS_TOKEN must be set"),
    );
    // ensure_ssh_key needs the PUBLIC KEY TEXT (ssh-ed25519 AAAA...), not a path.
    let public_key = std::env::var("DO_TEST_PUBLIC_KEY")
        .expect("DO_TEST_PUBLIC_KEY must hold the public key text");

    let api = HttpApi::new();

    // Register the SSH key by name; create_server references it by NAME only.
    let _fingerprint = api
        .ensure_ssh_key(&token, "criome-test", &public_key)
        .expect("ensure_ssh_key");

    let spec = ServerSpec {
        name: "criome-live-test".to_string(),
        server_type: DEFAULT_SIZE.to_string(),
        image: DEFAULT_IMAGE.to_string(),
        ssh_keys: vec!["criome-test".to_string()],
        location: Some(DEFAULT_REGION.to_string()),
    };

    let created = api.create_server(&token, &spec).expect("create_server");
    let identifier = created.identifier;

    // Poll until Running with a non-empty IPv4 (~36 tries x 5s = 3 min cap).
    let mut running = None;
    for _ in 0..36 {
        let host = api.get_server(&token, &identifier).expect("get_server");
        if host.status == HostStatus::Running {
            assert!(
                !host.ipv4.is_empty(),
                "Running droplet must expose an IPv4"
            );
            running = Some(host);
            break;
        }
        std::thread::sleep(std::time::Duration::from_secs(5));
    }
    let running = running.expect("droplet reached Running within 3 minutes");
    println!("LIVE droplet up: id={identifier} ipv4={}", running.ipv4);

    // Always destroy — this is the meter-stopping call.
    api.delete_server(&token, &identifier).expect("delete_server");
    println!("LIVE droplet destroyed: id={identifier}");
}
```

Guessed / scaffold values to confirm against your account before
running: the SSH key name `criome-test`, the droplet name
`criome-live-test`, and the exact field set of `ServerSpec` (taken from
the typed test values; verify the struct field names/order in
`src/digitalocean.rs` if the file does not compile). `DO_TEST_PUBLIC_KEY`
must hold the **public key text**, not a path.

### 2.2 Run it

```sh
cd /git/github.com/LiGoldragon/cloud
export DIGITALOCEAN_ACCESS_TOKEN=$(gopass show -o digitalocean.com/api-token)
export DO_TEST_PUBLIC_KEY=$(cat ~/.ssh/criome_test.pub)
cargo test --features digitalocean --test digitalocean_live -- --ignored --nocapture
```

Never echo `DIGITALOCEAN_ACCESS_TOKEN`; it is exported into the test
process env only. The `--nocapture` prints the live droplet id + IPv4 so
you can cross-check the DigitalOcean dashboard.

If the test aborts between create and delete (panic, ctrl-c), the droplet
is still billing — destroy it manually (section 4).

## 3 · Tier 2 — full daemon chain

Exercises the production shape: `cloud-daemon` over Unix sockets, account
registration over the meta socket, lifecycle over the ordinary socket via
the thin CLIs. The thin CLIs each parse exactly one NOTA `Operation`
string (src/client.rs:121-145, 154-159) and are pointed at the daemon by
`CLOUD_SOCKET_PATH` (ordinary, default `/run/cloud/cloud.sock`) and
`CLOUD_META_SOCKET_PATH` (meta, default `/run/cloud/cloud-meta.sock`),
src/client.rs:18-46.

### 3.1 Close the encoder gap first (one small adapter)

Because no built code path emits the rkyv `DaemonConfiguration` on the
command line, add a ~10-line example before Tier 2 can boot. Create
`cloud/examples/write_config.rs`:

```rust
// Emits a DaemonConfiguration rkyv file for cloud-daemon's single argument.
// Usage: write_config <out.rkyv> <ordinary.sock> <meta.sock>
fn main() {
    let mut args = std::env::args().skip(1);
    let out = args.next().expect("out.rkyv path");
    let ordinary = args.next().expect("ordinary socket path");
    let meta = args.next().expect("meta socket path");

    let configuration = cloud::DaemonConfiguration::new(
        ordinary.into(),
        cloud::SocketMode::default(),
        meta.into(),
        cloud::SocketMode::default(),
    );
    cloud::CloudDaemonConfigurationFile::write_configuration(&out, &configuration)
        .expect("write rkyv configuration");
}
```

Confirm the real constructor/field shape of `DaemonConfiguration`
(src/lib.rs:149-155) and the `write_configuration` signature
(src/daemon_command.rs:83-90) — the call above is the documented shape
but was not compiled. If you prefer not to add a file, generate the rkyv
by running the existing
`daemon_process_starts_from_binary_configuration` test and reusing the
`cloud-daemon.rkyv` it writes (tests/runtime.rs:263-265).

### 3.2 Boot the daemon

```sh
cd /git/github.com/LiGoldragon/cloud

# Writable socket dir for this run.
export CLOUD_RUN=$(mktemp -d)/cloud
mkdir -p "$CLOUD_RUN"

# Generate the rkyv startup message (requires the examples/write_config.rs above).
cargo run --features digitalocean --example write_config -- \
  "$CLOUD_RUN/cloud-daemon.rkyv" "$CLOUD_RUN/cloud.sock" "$CLOUD_RUN/cloud-meta.sock"

# Start the daemon with the DO token in ITS process env (the daemon makes the REST
# calls). cargo run does NOT apply the flake's gopass wrapper, so inject it here.
DIGITALOCEAN_ACCESS_TOKEN=$(gopass show -o digitalocean.com/api-token) \
  cargo run --features digitalocean --bin cloud-daemon -- "$CLOUD_RUN/cloud-daemon.rkyv"
```

Leave that running. In a second shell, point the thin CLIs at it:

```sh
cd /git/github.com/LiGoldragon/cloud
export CLOUD_SOCKET_PATH="$CLOUD_RUN/cloud.sock"
export CLOUD_META_SOCKET_PATH="$CLOUD_RUN/cloud-meta.sock"
```

(If you prefer a single release build of all three binaries:
`cargo build --release --features digitalocean,cloudflare --bin cloud-daemon --bin cloud --bin meta-cloud`,
then invoke `target/release/<bin>` instead of `cargo run`.)

### 3.3 The ordered lifecycle commands

All NOTA below follows workspace bare-atom rules: provider atoms,
account, host name, and the credential-handle env-var name are bare (no
quotation marks). `None` is the bare atom `None`; `Some x` is `(Some x)`.
Records are positional (type first, then fields in declared order).

Plan IDs are minted by the daemon. `CREATE_PLAN_ID` and
`DESTROY_PLAN_ID` below are placeholders — substitute the real
`PlanIdentifier` returned as the first inner atom of each
`HostPlanPrepared` reply (HostPlan id is the first field,
meta-signal-cloud/src/lib.rs:231-239).

Step 1 — register the DigitalOcean account over the **meta** socket. The
credential handle must equal the daemon's token env-var **name**
(`DIGITALOCEAN_ACCESS_TOKEN`), not the literal token. `Registration` is
`(provider account credential)`, meta-signal-cloud/src/lib.rs:45-49.

```sh
meta-cloud "(RegisterAccount (DigitalOcean primary DIGITALOCEAN_ACCESS_TOKEN))"
```

Step 2 — prepare a create plan over the **meta** socket. The inner record
is `DesiredHostState` with 5 fields (provider, host-name, size, image,
ssh-key-name), wrapped by `HostPlanPreparation` -> the double parens
(meta-signal-cloud/src/lib.rs:205-218). Capture `CREATE_PLAN_ID` from the
reply.

```sh
meta-cloud "(PrepareHostPlan ((DigitalOcean edge-test s-1vcpu-512mb-10gb ubuntu-24-04-x64 criome-test)))"
```

Step 3 — approve, then step 4 — apply (both meta socket; Approval and
Application each carry the plan, meta-signal-cloud/src/lib.rs:252-261):

```sh
meta-cloud "(ApprovePlan (CREATE_PLAN_ID))"
meta-cloud "(ApplyPlan (CREATE_PLAN_ID))"
```

Step 5 — observe over the **ordinary** socket; poll until `edge-test` is
`Running` with an IPv4. `HostQuery` is `(provider account)` with account
`Option` (signal-cloud:275-278); `Servers` is the variant wrapping it
(signal-cloud:398).

```sh
cloud "(Observe (Servers (DigitalOcean None)))"
```

Step 6 — confirm SSH reachability (replace `<IPv4>` with the observed
address):

```sh
ssh -i ~/.ssh/criome_test root@<IPv4>
```

Step 7 — prepare a destruction plan over the **meta** socket.
`HostDestruction` is `(provider host_name)`,
meta-signal-cloud/src/lib.rs:223-226. Capture `DESTROY_PLAN_ID`.

```sh
meta-cloud "(PrepareHostDestruction (DigitalOcean edge-test))"
```

Step 8 — approve, step 9 — apply (meta socket; this is the
meter-stopping call):

```sh
meta-cloud "(ApprovePlan (DESTROY_PLAN_ID))"
meta-cloud "(ApplyPlan (DESTROY_PLAN_ID))"
```

Step 10 — observe again over the **ordinary** socket; confirm `edge-test`
is **absent**:

```sh
cloud "(Observe (Servers (DigitalOcean None)))"
```

Guessed / unverified NOTA values, confirm before relying on the literal
strings:

- **Field order and provider-variant casing** of every operation above
  were inferred from the typed values in tests/digitalocean.rs:217-228
  and the meta-signal-cloud / signal-cloud schema line cites; they were
  **not round-tripped through the `meta-cloud` / `cloud` NOTA parser**.
  Verify each record's field order against the
  `Operation` / `Registration` / `DesiredHostState` / `HostDestruction`
  schema before the run.
- `edge-test` (host name) and `primary` (account) are chosen labels.
- The droplet size `s-1vcpu-512mb-10gb`, image `ubuntu-24-04-x64`, and
  SSH-key name `criome-test` are example values — confirm against your DO
  account.

## 4 · Cost + teardown

DigitalOcean droplets bill **per second** from creation to destruction.
The smallest droplet (`s-1vcpu-512mb-10gb`, the spec above) is on the
order of a few dollars per month, which is a small **fraction of a cent**
for a lifecycle test that lives a few minutes. The `DELETE` call
(Tier 1 `delete_server`; Tier 2 `(ApplyPlan (DESTROY_PLAN_ID))`) **stops
the meter** — there is no separate stop/power-off needed for billing.

Both tiers make **real, mutating** calls: `(Apply ...)` /
`create_server` really create droplets, `delete_server` really destroys
them, and a live `(Observe (Servers ...))` makes a real `/v2/droplets`
GET (src/digitalocean.rs is synchronous in-process `ureq`). The driver
also forces IPv6 + monitoring true on create (src/digitalocean.rs:437-448).
Use a throwaway DO account/project; prefer `Observe` before any mutating
op.

Confirm nothing is left running after the test, in order of trust:

1. **Observe via the daemon** (Tier 2): `cloud "(Observe (Servers
   (DigitalOcean None)))"` — `edge-test` / `criome-live-test` must be
   absent.
2. **doctl** (the gopass-wrapped debug CLI, on PATH from the flake):
   `doctl compute droplet list` — confirm no test droplet remains. The
   wrapper sources the token from `gopass show -o
   digitalocean.com/api-token` and fails loudly (`exit 78`) if it can't.
3. **DigitalOcean dashboard** — final visual confirmation; also check the
   `criome-test` SSH key if you want a clean account.

If a tier aborts mid-lifecycle (panic, ctrl-c, daemon crash between
create and destroy): the droplet keeps billing. Recover it by id/name
with `doctl compute droplet delete <id>` or by re-running the Tier 2
destroy steps (7-9) against the live `edge-test`.

## 5 · Open gaps / what still blocks

### Hard blocker — paid DigitalOcean token (psyche)

The live test needs a real `DIGITALOCEAN_ACCESS_TOKEN` in
`gopass digitalocean.com/api-token`. This is **pending payment** on the
DigitalOcean account. Until the token is live and the account can create
droplets, neither tier can run. Everything else below is in our hands.

### Gap — no command-line rkyv config encoder (Tier 2 only)

The rkyv `DaemonConfiguration` writer
(`CloudDaemonConfigurationFile::write_configuration`,
src/daemon_command.rs:83-90) is library-only, reachable today only from
`#[cfg(test)]`. There is no `examples/` dir and no encoder binary/nix
app. **Concrete fix:** add `examples/write_config.rs` (section 3.1, ~10
lines: 3 args -> `DaemonConfiguration` -> `write_configuration`) or
generate the rkyv from the existing
`daemon_process_starts_from_binary_configuration` test
(tests/runtime.rs:263-265). Tier 1 is unaffected — it has no daemon and
no rkyv.

### Gap — flake has no `--features digitalocean` daemon variant (Tier 2 / deploy)

`packages.default` builds with default features (`["cloudflare"]`) and
passes no feature override (flake.nix:82-94), so `nix run .#daemon` /
`nix build` give a daemon **without** the DO provider (DO capabilities
report `NotBuilt`). The live test therefore runs via `cargo run
--features digitalocean`, not `nix run`. **Concrete fix** (for a
nix-native live boot later): add a DO-enabled package variant
(`buildFeatures = [ "digitalocean" "cloudflare" ]` / `cargoExtraArgs`
override in `commonArgs`); the gopass token wrapper for `cloud-daemon` is
already present (flake.nix:91), so a feature-enabled `nix run` would boot
a DO-capable daemon with the token wiring done.

### Note — gopass path corrected, not a gap

The DO secret lives at `digitalocean.com/api-token` (not
`digitalocean/api-token`). Verified in flake.nix:71, :91. Use the `.com`
form everywhere. The shim itself is complete (section 1) — no fix needed,
just use the right path.

### Note — guessed NOTA values (Tier 2 only)

Every Tier 2 NOTA string's field order and provider-variant casing was
inferred from typed test values and schema line cites, **not** round-trip
through the parsers. Verify each record against the
meta-signal-cloud / signal-cloud `Operation` schemas before the live run.
Tier 1 uses typed Rust values directly and carries no NOTA-spelling risk.

### Note — daemon wrapper swallows gopass failure (debugging)

The `cloud-daemon` gopass fallback (flake.nix:91) is
`${VAR:-$(gopass ... 2>/dev/null)}`, which silently yields an empty token
on gopass failure (surfacing later as `Error::CredentialUnavailable`),
unlike the loud CLI wrappers. Not a blocker; relevant only when debugging
a "token unavailable" symptom under the nix package.
