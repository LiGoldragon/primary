# 69 · Provider tokens — capabilities, Cloudflare DNS status, and the full-caps question

Answers the psyche's session questions: can cloud modify Cloudflare DNS and
can we test it; do we have a CF token; what DigitalOcean capabilities are
useful for agents; and is a full-capability token a real problem given that
agents can already mint any token through the browser. All findings probed
live against the real provider APIs (read-only).

## 1 · Cloudflare DNS — built in code, blocked by the token

**The capability exists.** `cloud/src/cloudflare.rs` is *not* read-only: the
`Api` trait carries `create_record`, `update_record`, `delete_record`, and
`ProviderClient::apply_plan` (`cloudflare.rs:360-378`) does a real
delete-then-upsert reconciliation against a live zone, covering 15 record
kinds (A, AAAA, CNAME, TXT, MX, NS, SRV, CAA, …). So "modify domain name
settings" is a built path, not a gap — it simply has no live witness yet.

**The stored token is the blocker, two ways:**

- **Wrong gopass path.** The token lives at gopass `cloudflare.com/token`
  (the domain form, like `digitalocean.com/api-token`), but
  `cloud/flake.nix:46` reads `cloudflare/api-token`, which **does not
  exist** (probed: 0 bytes). This is the exact bug class the DO `.com` fix
  just corrected (`7f190c3`) — the CF wrapper points at an empty path, so
  the `flarectl`/daemon CF path gets no token.
- **The token is under-scoped.** The token at `cloudflare.com/token` is
  valid and `active` (40-char scoped API token), and it can read
  `/accounts` (sees `Anna.bird@protonmail.com's Account`,
  `deb8b8…2718c`) — but `GET /zones` returns **zero zones** and
  `GET /user/tokens/{id}` is refused (`9109 Unauthorized`). So the token
  lacks `Zone:Read` (and therefore cannot enumerate or edit DNS), **or**
  that account has no domains added to Cloudflare. Either way the current
  token cannot drive a DNS change.

**To test it live** (the same create-then-destroy shape as the DO droplet
test — a throwaway `TXT cloud-livetest` record created and immediately
deleted, zero routing impact) we need a CF token with **`Zone.Zone:Read` +
`Zone.DNS:Edit`** on the target zone. Open question for the psyche below.

## 2 · The DigitalOcean token's real scope surface (probed live)

The current DO token (`digitalocean.com/api-token`, scoped `dop_v1_` PAT) —
probed by hitting each resource's read endpoint:

| Scope | Status | For cloud's job? |
|---|---|---|
| `droplet` | **200 (have)** + write proven (live test) | core compute |
| `ssh_key` (`account/keys`) | **200 (have)** | core |
| `image` | **200 (have)** | **ad53 CloudNode images** |
| `snapshot` | **200 (have)** | **ad53 snapshots** |
| `vpc` | **200 (have)** | private networking |
| `project` | **200 (have)** | org/grouping |
| `account` | 403 (lacks) | capability report (`/v2/account`) |
| `domain` | 403 (lacks) | **DO-managed DNS** (alt/complement to Cloudflare) |
| `reserved_ip` | 403 (lacks) | stable IPs for nodes |
| `firewall` | 403 (lacks) | node security groups |
| `volume` | 403 (lacks) | persistent block storage |
| `load_balancer` | 403 (lacks) | multi-node fronting |
| `monitoring` | 403 (lacks) | alerts/metrics |
| `database`, `kubernetes`, `cdn` | 403 (lacks) | not cloud's job today |

So "only a few capabilities" is fairer than it looked — it already has the
six that matter for provisioning + the `ad53` image work. The useful
**additions** for an agent-driven provisioning daemon, in priority order:

1. **`account` (read)** — closes the one capability-report gap (the daemon
   asks `/v2/account`; today that 403s).
2. **`reserved_ip`** — stable addresses so a re-provisioned node keeps its IP.
3. **`firewall`** — lock down test nodes (SSH-only ingress).
4. **`domain`** — lets DO manage DNS for the nodes directly, an alternative
   to the Cloudflare path.
5. **`volume`, `monitoring`, `load_balancer`** — as those features land.

Not needed unless a specific use appears: `database`, `kubernetes`, `cdn`,
Spaces (object storage; Spaces uses separate keys anyway).

## 3 · Is a full-caps token a real problem? — yes, but not where you'd think

The instinct "agents can mint any token via the browser, so why scope the
stored one" conflates **two different threat surfaces**:

**(a) Agent capability surface — scoping buys nothing here.** If an agent
has browser access to the DO/CF dashboard, it can already mint a
full-scope token at will. The *stored* token's scope does not contain a
trusted-or-compromised agent — the agent isn't bounded by it. From this
angle your instinct is correct: scope is not an agent-containment boundary.
Constraining *agents* belongs at the authorization layer (criome / the
auth component — this is exactly what [[cloud-credential-system-creds]]
Spirit `iprx` and `h03z` point at), not at the token's scope.

**(b) Token-leak blast radius — scoping is the whole game here.** The
stored token is a secret *at rest* (gopass) that flows into the daemon's
process environment, argv-adjacent surfaces, logs, and crash state. If
*that* token leaks — a stray log line, a crash dump, a misconfigured
process env read by another process, a compromised host — a full-caps
token is a catastrophe: delete every droplet, spin up expensive
GPU/managed-DB resources, read Spaces object storage, touch billing. A
job-scoped token caps the damage to "someone can churn test droplets."
This risk is entirely independent of the browser path.

**The synthesis (and the recommendation):**
- **Scope the *stored daemon* token to the daemon's job + an expiry.** Both
  DO and CF support token expiry; a leaked job-scoped token that also
  expires self-limits in both blast-radius and time. This aligns with the
  workspace's standing secret intent — `ravc` ([secret paths are scoped to
  the resource they serve]), `cjrl` ([secrets land in the most secure place
  available]).
- **Keep browser-mint for ad-hoc, broad, *short-lived* tokens** — mint per
  task and discard, rather than storing a permanent god-token that is a
  standing leak prize.
- **Net:** a full-caps *stored* token is a real marginal risk (the leak
  surface), a full-caps *interactive browser* mint is a trust decision you
  already made. Use a job-scoped + expiring token for the daemon; reach for
  the browser when you genuinely need a one-off broad action.

For cloud specifically: a DO token with `droplet, ssh_key, image, snapshot,
reserved_ip, firewall, vpc, project, monitoring, account:read` (+ `domain`
if DO does your DNS) covers everything cloud does and the `ad53` image work,
without billing/Spaces/k8s. That is "most of them" — deliberately, not all.

## 4 · Open question + next moves

- **Cloudflare:** does `Anna.bird@protonmail.com's Account` actually hold
  the domains you want cloud to manage (so we mint a `Zone:Read + DNS:Edit`
  token for it), or are those domains elsewhere / not yet on Cloudflare?
  Once a DNS-edit token exists at `cloudflare.com/token`, the live
  create-then-delete DNS round-trip is a 1-minute test.
- **Flake fix:** `cloud/flake.nix:46` should read `cloudflare.com/token`,
  not `cloudflare/api-token` — same fix shape as the DO `.com` correction.
  Belongs on the cloud doc/operator branch.
- **Still queued from "proceed with all your next moves":** Tier-2 live
  daemon spine (the DO `register→prepare→approve→apply→observe→destroy`
  over the sockets), and the `cloud/INTENT.md`/`ARCHITECTURE.md` refresh
  (DO-lead `hcp8`, `ad53`, the single-`EngineActor` reality). Tracked on
  bead `primary-x8by`.
