# 72 · Lane B — cloud socket contract (exact NOTA + Cloudflare credential resolution)

## TL;DR

- Every cloud leg is `cloud <nota>` (ordinary socket, `CLOUD_SOCKET_PATH`)
  for reads or `meta-cloud <nota>` (meta socket, `CLOUD_META_SOCKET_PATH`)
  for mutations. The exact, copy-pasteable NOTA for each leg is in the
  table below, matching report 70's proven encoding (2 root objects per
  operation; single-field-struct payloads double-nest; bare atoms, no
  quote marks).
- **The create→observe seam is asynchronous on purpose.** `ApplyPlan`
  for a host returns only `(PlanApplied (<plan-id>))` — no IP, no status.
  Readiness is observed separately: poll `cloud "(Observe (Servers ...))"`
  until the `CloudHost`'s `status` field leaves `Initializing` for
  `Running` AND its `ipv4` field stops being the empty atom `[]` and
  carries a real address. The `HostStatus` variants are
  `Initializing | Running | Stopped | Deleting | Unknown`
  (`signal-cloud/src/lib.rs:215-221`).
- **`image_name` plumbs end-to-end to the provider `ServerSpec.image`,
  confirmed by line.** NOTA `DesiredHostState.image_name` →
  `HostPlan.image_name` → `ServerSpec.image`
  (`cloud/src/lib.rs:1282`, then `:1602` Hetzner / `:1661` DigitalOcean).
  A snapshot id is a plain atom in the `image` slot.
- **The Cloudflare credential question, RESOLVED — and the prompt's
  premise is wrong in a load-bearing way.** There is *no*
  `CLOUDFLARE_DNS_TOKEN` constant anywhere in `cloud`. The daemon DOES
  call `EnvironmentCredentialSource` on the live flarectl path, but it
  reads **the env-var name the operator registered as the credential
  handle in `RegisterAccount`** — not a hardcoded name. `CF_API_TOKEN`
  is a *separate*, downstream variable: the daemon injects the resolved
  token *value* into a child-process `CF_API_TOKEN` env for `flarectl`
  (`cloud/src/cloudflare_cli.rs:50`). So two env vars exist on the path,
  and the flake gap is real but **not** a missing `CLOUDFLARE_DNS_TOKEN`.
  Severity and precise fix below.

Report 70 (`reports/cloud-designer/70-tier2-daemon-spine-proven.md`) is
the proven witness this builds on; this report extends it to the DNS
A-record leg and resolves the credential trace.

## The legs (copy-pasteable NOTA)

Boot context (from report 70 §"working socket protocol"):

```sh
cargo run --example write_config --features digitalocean,cloudflare -- out.rkyv ord.sock meta.sock
DIGITALOCEAN_ACCESS_TOKEN=... CF_API_TOKEN_VALUE_IN_HANDLE_ENV=... cloud-daemon out.rkyv &
export CLOUD_SOCKET_PATH=ord.sock CLOUD_META_SOCKET_PATH=meta.sock
```

| # | Leg | Socket | NOTA |
|---|---|---|---|
| 1 | Register host account | meta (`CLOUD_META_SOCKET_PATH`) | `meta-cloud "(RegisterAccount (DigitalOcean criome-test DIGITALOCEAN_ACCESS_TOKEN))"` |
| 2 | Prepare create plan | meta | `meta-cloud "(PrepareHostPlan ((DigitalOcean node.cluster.criome s-1vcpu-512mb-10gb 178342618 criome-test)))"` |
| 3 | Approve plan | meta | `meta-cloud "(ApprovePlan (node.cluster.criome-DigitalOcean-host-plan))"` |
| 4 | Apply plan [Create] | meta | `meta-cloud "(ApplyPlan (node.cluster.criome-DigitalOcean-host-plan))"` |
| 5 | Observe servers (poll) | ordinary (`CLOUD_SOCKET_PATH`) | `cloud "(Observe (Servers (DigitalOcean None)))"` |
| 6 | Register DNS account | meta | `meta-cloud "(RegisterAccount (Cloudflare criome-dns CF_DNS_TOKEN_ENV))"` |
| 7 | Prepare DNS A-record plan | meta | `meta-cloud "(PreparePlan ((Cloudflare criome [(node.cluster.criome AddressV4 [203.0.113.10] Direct)] [])))"` |
| 8 | Approve DNS plan | meta | `meta-cloud "(ApprovePlan (<dns-plan-id>))"` |
| 9 | Apply DNS plan | meta | `meta-cloud "(ApplyPlan (<dns-plan-id>))"` |
| 10 | Observe records (verify) | ordinary | `cloud "(Observe (Records (Cloudflare criome)))"` |

Field notes for each leg follow.

### Leg 1 — RegisterAccount (host)

`Registration` is an inline 3-field struct (`provider account credential`,
`meta-signal-cloud/src/lib.rs:45-49`), so the payload is a flat record,
not double-nested. The third atom is the **credential handle = the name
of the env var the daemon will `getenv` for this account's token**
(`digitalocean.rs:79` documents `DIGITALOCEAN_ACCESS_TOKEN` as the
expected handle). Reply: `(AccountRegistered (DigitalOcean criome-test))`.

### Leg 2 — PrepareHostPlan (the double-nest one)

`PrepareHostPlan` carries `HostPlanPreparation`, a **single-field struct**
wrapping `DesiredHostState` (`meta-signal-cloud/src/lib.rs:216-218`), so
the payload double-nests: `(PrepareHostPlan (( ...desired-host-state... )))`.
`DesiredHostState` is the inline 5-field record
`(provider host_name server_type image_name ssh_key_name)`
(`:205-211`). The fourth field, `image_name`, is **where the snapshot id
goes** (`178342618` above is illustrative). This matches report 70's
verbatim parser tell: *"expected HostPlanPreparation to hold 1 root
objects, found 5."* Reply: `(HostPlanPrepared (<plan> ... Create))`.

### Legs 3-4 — ApprovePlan / ApplyPlan

`Approval` and `Application` are both single-field structs over
`PlanIdentifier` (a `String` scalar), so the payload is a **bare atom in
single parens**: `(ApprovePlan (<plan-id>))`. The plan id is a derived,
deterministic string — `<host_name>-<Provider:?>-host-plan`
(`cloud/src/lib.rs:1274-1278`); `Provider` formats `{:?}` so it is
PascalCase: `node.cluster.criome-DigitalOcean-host-plan`. A caller can
construct it without reading the prepare reply.

### Leg 5 — Observe Servers (create→observe seam)

Ordinary socket. `Observation::Servers(HostQuery)` where `HostQuery` is
`(provider account-option)` (`signal-cloud/src/lib.rs:275-278`); account
is `None` or `(Some criome-test)`. The hand-written tree's variant is
**`Servers`**, not the schema's `ObserveServers` — report 70 §"NOTA
nesting rule" / audit finding `68-3-P1-1`. Reply per host is an 8-field
`CloudHost` record (`signal-cloud/src/lib.rs:283-292`):
`(provider account identifier name server_type image ipv4 status)`.

### Legs 6-10 — DNS A-record path

The DNS path is the **same Prepare/Approve/Apply triad**, but over
`PreparePlan` (records/redirects), not `PrepareHostPlan`. `PreparePlan`
carries `PlanPreparation`, a single-field struct over `DesiredState`
(`meta-signal-cloud/src/lib.rs:108-110`), so it double-nests exactly
like `PrepareHostPlan`: `(PreparePlan (( ...desired-state... )))`.
`DesiredState` is re-exported `signal_cloud::DesiredState`
(`meta-signal-cloud/src/lib.rs:13-14`), the inline 4-field record
`(provider zone records redirects)` (`signal-cloud/src/lib.rs:354-359`).
`records` is a vector of the **hand-written** 4-field
`DomainNameSystemRecord` `(name kind value proxy_mode)`
(`signal-cloud/src/lib.rs:304-309`). The A-record kind atom is
**`AddressV4`** (hand-written `RecordKind`, `:130-131`) — NOT the
schema's `Address`; the flarectl adapter maps `AddressV4 → "A"`
(`cloud/src/cloudflare_cli.rs` / `cloud/src/lib.rs:324`). `proxy_mode`
is `Direct` or `ProviderProxy` (`signal-cloud/src/lib.rs:161-164`).

The value `[203.0.113.10]` is bracketed only as an example of an IP that
is in fact bare-eligible — `.` is not a structural delimiter, so a bare
`203.0.113.10` is also legal at that `RecordValue(String)` position
(`signal-cloud/src/schema/lib.rs:54`). The empty redirects vector is `[]`.

The DNS plan id derivation was not located in the host-plan path (host
ids derive at `cloud/src/lib.rs:1274`; the record-plan id derivation for
`PreparePlan` was not read this session — see open questions). Drive
legs 8-9 from the `(PlanPrepared (<plan> ...))` reply's identifier field
rather than constructing the id blind.

## The create→observe seam (confirmed)

**ApplyPlan[Create] returns only `PlanApplied{plan}` — no IP.** Both
provider arms return `MetaReply::PlanApplied(PlanApplied { plan:
plan.identifier })` on success (`cloud/src/lib.rs:1613-1615` Hetzner,
`:1672-1674` DigitalOcean). `PlanApplied` is the single-field struct
`{ plan PlanIdentifier }` (`meta-signal-cloud/schema/lib.schema:39`). No
address, no host record is in the apply reply. Report 70's witness
confirms live: `ApplyPlan [CREATE] -> (PlanApplied (...-host-plan))`.

**Readiness lives in the separately-observed `CloudHost`.** Two fields
signal it (`signal-cloud/src/lib.rs:290-291`):

- `status: HostStatus` — variants `Initializing | Running | Stopped |
  Deleting | Unknown` (`signal-cloud/src/lib.rs:215-221`). Fresh node
  reads `Initializing`; ready is `Running`.
- `ipv4: IpAddress` — `IpAddress(String)`
  (`signal-cloud/src/schema/lib.rs:99`). Report 70's witness showed the
  empty value rendering as the bare empty-string atom `[]` in the
  observed record (`... ubuntu-24-04-x64 [] Initializing`). So the poll
  predicate is: `status == Running` AND `ipv4 != []`.

Caveat carried from report 70: right after a *destroy*, `Servers` can
still list a node as `Initializing` during the provider's
eventual-consistency window; that is a provider read lag, not a daemon
defect.

## image_name end-to-end (confirmed by line)

| Hop | Site | Line |
|---|---|---|
| NOTA in | `DesiredHostState.image_name` (field 4 of leg 2) | `meta-signal-cloud/src/lib.rs:209` |
| Prepare copies it | destructured then placed into `HostPlan.image_name` | `cloud/src/lib.rs:1255`, `1282` |
| Wire plan field | `HostPlan { ... image_name ImageName ... }` | `meta-signal-cloud/schema/lib.schema:80` |
| Apply → adapter (Hetzner) | `image: plan.image_name.as_str().to_owned()` into `hetzner::ServerSpec` | `cloud/src/lib.rs:1602` |
| Apply → adapter (DigitalOcean) | `image: plan.image_name.as_str().to_owned()` into `digitalocean::ServerSpec` | `cloud/src/lib.rs:1661` |

A snapshot id flows verbatim as the `image_name` atom into the provider
`ServerSpec.image`. No transformation, no validation in the daemon —
whatever string you pass is handed to the provider's create call.

## Cloudflare credential resolution — RESOLVED

### The trace

Production DNS apply: `apply_cloudflare_plan` →
`self.cloudflare.apply_plan(&binding.credential, &zone, &plan)`
(`cloud/src/lib.rs:1511`). Inside `ProviderClient::apply_plan`, the very
first line is `let token = self.credentials.token(credential)?`
(`cloud/src/cloudflare.rs:366`). For a `production()` client,
`self.credentials` is `EnvironmentCredentialSource`
(`cloud/src/cloudflare.rs:290-295`), whose `token` impl is
`std::env::var(handle.as_str())` (`cloud/src/cloudflare.rs:51-56`) — it
reads **the env var named by the credential handle the operator passed
to `RegisterAccount`**, not any fixed name. That resolved token value is
then handed to `FlarectlApi`, and `ProcessRunner::run` spawns `flarectl`
with `.env(TOKEN_ENVIRONMENT_VARIABLE, token.as_str())` where
`TOKEN_ENVIRONMENT_VARIABLE = "CF_API_TOKEN"`
(`cloud/src/cloudflare_cli.rs:18, 50`).

### The answers

- **Does the daemon call `EnvironmentCredentialSource` on the live
  flarectl path?** Yes. `production()` wires `FlarectlApi` +
  `EnvironmentCredentialSource` together (`cloudflare.rs:290-295`), and
  `apply_plan`/`records`/`zones` all call `self.credentials.token(...)`
  before any flarectl shell-out (`cloudflare.rs:350, 366`). It is **not**
  vestigial and **not** REST-only — `production()` (the flarectl path)
  and `production_http()` (the REST path) share the *same*
  `EnvironmentCredentialSource`; the only difference is the `Api` impl.
- **Is the only live token `CF_API_TOKEN`?** No. There are **two**
  variables on the live flarectl path: (1) the **credential-handle env
  var** the daemon itself reads via `EnvironmentCredentialSource`
  (operator-chosen name, supplied in `RegisterAccount`); and (2)
  **`CF_API_TOKEN`**, which the daemon *sets on the flarectl child
  process* to carry that resolved value. They can be the same string if
  the operator registers the handle `CF_API_TOKEN`, but they are distinct
  mechanisms.
- **Is there a `CLOUDFLARE_DNS_TOKEN`?** No — the constant does not
  exist anywhere in `cloud` (grep over `src/`, `examples/`, `flake.nix`
  returns nothing). The prompt's "does the daemon call
  `EnvironmentCredentialSource::resolve(CLOUDFLARE_DNS_TOKEN)`" rests on
  a name that isn't in the tree. The real handle name is whatever
  `RegisterAccount` carried; the host providers document their expected
  handles as constants (`HCLOUD_TOKEN`, `DIGITALOCEAN_ACCESS_TOKEN`,
  `hetzner.rs:66`, `digitalocean.rs:79`) but Cloudflare has **no
  daemon-side handle constant** — the wrapper's `CF_API_TOKEN` is the
  flarectl-subprocess name, not a daemon-read handle.

### The flake situation, severity, and fix

The flake wires Cloudflare's token at the **flarectl wrapper** layer, not
on the daemon. `cloudflareCli` is a gopass-wrapped `flarectl` that, on
every invocation, sets `CF_API_TOKEN=$(gopass show -o cloudflare/api-token)`
(`flake.nix:40-47`). The `cloud-daemon` wrapper
(`flake.nix:95-99`) injects `HCLOUD_TOKEN` and `DIGITALOCEAN_ACCESS_TOKEN`
into the daemon's own env (those providers read REST in-process, so the
daemon needs them) but does **not** inject any Cloudflare variable — by
design, because the daemon doesn't read Cloudflare's token; flarectl
does, and flarectl self-fetches via its own wrapper.

**Severity: low, conditional on the registered handle.** This is only a
gap if the operator registers a Cloudflare account whose credential
handle names an env var that must be present in the *daemon's* process
for `EnvironmentCredentialSource::token` to succeed
(`cloudflare.rs:53`). Two cases:

1. Operator registers handle `CF_API_TOKEN` and exports `CF_API_TOKEN` in
   the daemon's env → `EnvironmentCredentialSource` resolves it, and that
   value is re-injected to flarectl. But then flarectl's *own* wrapper
   *also* overwrites `CF_API_TOKEN` from gopass on spawn (`flake.nix:46`),
   so the daemon-injected value is shadowed. Works, but redundant and
   confusing — two sources race and gopass wins.
2. Operator registers any other handle (e.g. the Cloudflare account is
   meant to be credential-free at the daemon because flarectl
   self-fetches) → `EnvironmentCredentialSource::token` will *fail* with
   `CredentialUnavailable` unless that exact env var is set in the daemon
   process, because the daemon resolves the handle *before* it ever
   reaches flarectl. The verify step at register time
   (`cloud/src/lib.rs:1400`, `verify_credential` →
   `credentials.token(...)`) fails the same way at `RegisterAccount`.

**Precise fix (two coherent options; pick one — no backward-compat
constraint):**

- **Option A (handle-as-passthrough, smallest):** register the
  Cloudflare account with the handle `CF_API_TOKEN`, and add one line to
  the `cloud-daemon` wrapper mirroring the other two providers:
  `--run 'export CF_API_TOKEN=''${CF_API_TOKEN:-$(gopass show -o cloudflare/api-token 2>/dev/null)}'`
  inserted at `flake.nix:99`. Then both the daemon's
  `EnvironmentCredentialSource` *and* flarectl resolve the same gopass
  secret, and the daemon-side resolution no longer fails at register.
  Drop the per-wrapper gopass fetch in `cloudflareCli` (`flake.nix:46`)
  to avoid the double-fetch shadow, or leave it as a harmless fallback.
- **Option B (skip daemon-side resolution for flarectl):** give the
  flarectl Cloudflare path a no-op credential source so the daemon does
  not `getenv` at all (flarectl owns the secret end-to-end via its
  wrapper). This means `production()` should NOT pair `FlarectlApi` with
  `EnvironmentCredentialSource`; it should pair it with a source that
  returns an empty/sentinel token, since the token the daemon resolves is
  thrown away anyway when flarectl's wrapper re-fetches. This is the
  cleaner model (single source of truth = gopass via flarectl) but is a
  code change in `cloudflare.rs`, not just flake.

Recommendation: **Option A** for the immediate Lojix bring-up (one flake
line, zero code), with Option B logged as the principled follow-up since
the current `production()` pairing makes the daemon resolve a token it
then discards.

## Two-tree drift reminder (carry from report 70 / audit 68-3-P1-1)

The CLI parses the **hand-written** `signal_cloud::Operation` /
`meta_signal_cloud::Operation` trees, not the `.schema` files. Where they
diverge, drive the hand-written names:

| Concept | Hand-written (drive this) | Schema `.schema` (do NOT drive) |
|---|---|---|
| Observe hosts variant | `Servers` | `ObserveServers` |
| A-record kind atom | `AddressV4` | `Address` |
| `DomainNameSystemRecord` arity | 4 fields incl. `proxy_mode` | 3 fields, no proxy_mode |
| record value field | `RecordValue` | `RecordContent` |

Until the schema cutover lands, the NOTA in the legs table above uses the
hand-written shapes and is the one that parses.
