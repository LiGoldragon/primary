# Scout — T4-code / Cloud Record Home Verdict

Read-only grounding investigation correcting the orchestrator's under-grounded
claim that "cloud components have no current repo." No record, file, config, or
runtime state was changed.

## Task and scope

Bead `primary-t5vj` covers the code/config (~33) category of archived Spirit
records. Phase 2 routing (`agent-outputs/SpiritArchiveRehoming/RoutingManifest.md`)
deferred a subset to `lojix-cli` (now RETIRED) and a routing scout asserted some
"cloud-component config" records had "no cloud repo present." This map: (1)
enumerates the deferred code/config records with per-record concern, (2) gives
homed-vs-deferred status, (3) reads the cloud records and finds their real home,
(4) recommends a home for every still-deferred record, and reconciles counts.

## Files and commands consulted

- `agent-outputs/SpiritArchiveRehoming/RoutingManifest.md` (Phase-2 record→home assignment).
- `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` (full archived-record text, including descriptions, domains, referents).
- `agent-outputs/SpiritArchiveRehoming/Scout-RoutingAssessment.md` (prior scout; category counts).
- Live repos: `repos/goldragon` (+ `datom.nota`, `README.md`, `AGENTS.md`) and its `cloud-node-data` worktree; `repos/criome`; `repos/CriomOS`; `repos/CriomOS-home`; `repos/horizon-rs`; and `/git/github.com/LiGoldragon/{lojix,signal-lojix,meta-signal-lojix,cloud,signal-cloud,meta-signal-cloud}`.
- `protocols/active-repositories.md` (workspace canon on which repos are live; names `cloud`, `goldragon`, `lojix`, the Replacement Stack, and "two deploy stacks coexist").
- `git worktree list` / `git branch -a` / `git log` in `repos/goldragon`.

## Headline verdict

The orchestrator's claim is **FALSE**. A live cloud/cluster home exists — in
fact three, with cleanly separated responsibilities:

- **`goldragon`** (LIVE, tracked, `/git/github.com/LiGoldragon/goldragon`) — the
  cluster-proposal DATA repo: "Production data for every node, user, and trust
  relation in the LiGoldragon kriom" (`README.md`). Its `cloud-node-data`
  worktree/branch already implements the cloud-node records (declares `doris` as
  a DigitalOcean CloudNode at Min trust, unprovisioned with placeholder host key;
  a commit message literally cites "Spirit zeqq").
- **`cloud`** (LIVE, `/git/github.com/LiGoldragon/cloud`, plus `signal-cloud` /
  `meta-signal-cloud`) — the runtime daemon repo for provider API management
  (DigitalOcean/Hetzner/Cloudflare). This is the home for the cloud-DAEMON
  behavior records. Per `active-repositories.md` it was witnessed end-to-end
  against real droplets.
- **`lojix`** (LIVE, `/git/github.com/LiGoldragon/lojix`, plus `signal-lojix` /
  `meta-signal-lojix`) — the new deploy-stack crate that is the named successor
  to the retired `lojix-cli` ("replaces the implementation surface of today's
  `lojix-cli`", `lojix/AGENTS.md`).

So the manifest's DEFERRED-TO-STRAGGLER parking against `lojix-cli` and a
nonexistent cloud home is stale on two counts: `lojix-cli` was retired but its
successor `lojix` is live, and a cloud/cluster home plainly exists.

## Count reconciliation (observed)

- Manifest DEFERRED-TO-STRAGGLER total = **43**: `lojix-cli` 18 + `CriomOS` 13 +
  `persona` 11 + `schema-cc` 1 (arithmetic verified: 18+13+11+1 = 43).
- Bead `primary-t5vj` "code/config" category ≈ **33** (matches the prior scout's
  code/config = 33).
- Reconciliation: the **31 operations/deploy/config records** = 18 (lojix-cli
  bucket) + 13 (CriomOS bucket) are the genuine "T4-code / code/config" set.
  Add the ~2 cloud/secret records the prior scout also counted as code/config
  (`go41`, plus the WiFi/secret-adjacent ones) and you reach the bead's ~33. The
  `persona` (11) and `schema-cc` (1) buckets are **component-architecture**, NOT
  code/config — they are mis-grouped if folded into the 33. So:
  - **Genuinely code/config + still-deferred: 31** (18 lojix bucket + 13 CriomOS
    bucket), of which **~7 are explicitly "cloud-component" records.**
  - The "~33" in the bead is the four-category code/config tally; the "~18 to
    lojix incl ~7 cloud" in the manifest's lojix bucket is internally consistent
    (see the cloud-tagged subset below).

### The ~7 cloud-component records (the crux subset)

From the manifest's `lojix-cli/cloud` tags + referent inspection, the records
whose referents lead with `cloud` / `cloud-daemon` / a provider are:

`150a`, `16l0`, `7kyx`, `8fe9`, `iprx`, `m3eg`, `mbmy`, `nsi2`, `zeqq`, `5pf6`
— that is **10** cloud-referent records, not 7 (the manifest under-counted; it
tagged only 7 with the literal "/cloud" suffix). All ten concern the cloud
DAEMON or cloud NODE, and all ten have a live home.

## Per-record table — deferred code/config records

Status legend: DEFERRED = still parked in the manifest. Recommended home is a
LIVE repo unless marked drop. All are Privacy Zero per the records; secret-adjacent
ones flagged.

### Cloud bucket (cloud daemon + cloud node) — home is `cloud` or `goldragon`

| id | concerns | status | recommended home |
| --- | --- | --- | --- |
| `150a` | cloud component's next capability: on-demand compute-node provisioning via provider APIs; DigitalOcean lead over Hetzner, billing/keep-warm pool | DEFERRED | `cloud` (runtime/ARCHITECTURE.md) |
| `16l0` | cloudflare feature wraps `flarectl` as runtime dep via makeWrapper so it's on daemon PATH | DEFERRED | `cloud` (flake/packaging) |
| `7kyx` | create cloud as Cloudflare API management triad; Mutate verbs on meta-signal-cloud, Query on signal-cloud | DEFERRED | `cloud` (+ `signal-cloud`/`meta-signal-cloud`) |
| `8fe9` | rename cloud's Plan op to Mutate, reply Mutated; Mutate-sent vs Mutated provider-ack states | DEFERRED | `cloud` |
| `iprx` | cloud credential custody moving toward criome-custodied machine-identity from wire CredentialHandle env var | DEFERRED | `cloud` (secrets-adjacent; criome cross-ref) |
| `m3eg` | cloud daemon almost-stateless, caches last-known Cloudflare state in-memory | DEFERRED | `cloud` |
| `mbmy` | cloud is home for provider API machinery (Cloudflare/Google/Hetzner); plan prep on owner signal | DEFERRED | `cloud` |
| `nsi2` | cloud flake wraps flarectl with gopass shim fetching CF_API_TOKEN from `cloudflare.com/api-token` | DEFERRED | `cloud` (secrets-adjacent) |
| `5pf6` | cloud-hosted nodes get low cluster trust (Min); doris (DO CloudNode) set to Min | DEFERRED | `goldragon` (cluster trust data) — ALREADY in `cloud-node-data` branch |
| `zeqq` | provision-on-role only; doris stays declared low-trust placeholder until given a role | DEFERRED | `goldragon` — ALREADY implemented in `cloud-node-data` branch (commit cites zeqq) |

### Lojix bucket (deploy daemon) — home is the live `lojix` (NOT retired `lojix-cli`)

| id | concerns | status | recommended home |
| --- | --- | --- | --- |
| `2alg` | lojix deploy daemon serves connections concurrently, per-request state, brief Store lock | DEFERRED | `lojix` (ARCHITECTURE.md) |
| `2qhw` [SECRET] | lojix-daemon owns GitHub-authed Nix flake input resolution; secret-fetch+auth-injection lib | DEFERRED | `lojix` (redact; secrets discipline) |
| `75pw` | practical Nix build/test/deploy defaults to safe typed Lojix interface | DEFERRED | `lojix` |
| `h03z` | lojix integrates criome machine-identity for production cutover credentials | DEFERRED | `lojix` (criome cross-ref) |
| `lc28` | lojix substituter resolution (node name→Yggdrasil URL/key) moves into daemon; provisional | DEFERRED | `lojix` |
| `mq5s` | testing and deployment are one lojix function; contained-vs-production typed split | DEFERRED | `lojix` |
| `vfgk` | lojix carries ergonomic public test-authoring interface (cluster tests) | DEFERRED | `lojix` |
| `vudl` | lojix two-contract authority split; Deploy/Pin/Unpin/Retire owner-only in meta-signal-lojix | DEFERRED | `lojix` (+ `meta-signal-lojix`) |

### CriomOS bucket (OS image / node OS) — home is live `CriomOS` / `CriomOS-home`

| id | concerns | status | recommended home |
| --- | --- | --- | --- |
| `0a9p` | model prefetch/build only on Prometheus/AI node, never trigger big downloads elsewhere | DEFERRED | `CriomOS` (or `CriomOS-home`) |
| `1hyg` | LojixOS/CriomOS rename split; cloud-node OS images live in CriomOS as CloudNode profile | DEFERRED | `CriomOS` |
| `6wz8` | synthetic bare-metal firmware-gating stays generic, constrained Nix checks | DEFERRED | `CriomOS` |
| `878r` | CriomOS website-hosting node service; doris first low-trust role (Jekyll-mould static) | DEFERRED | `CriomOS` (role for doris from `goldragon`) |
| `cncj` | CriomOS VM-testing per-node gpu-passthrough VFIO, disabled on Prometheus | DEFERRED | `CriomOS` |
| `kx32` | deploy to large-AI node must preserve hostapd/dnsmasq net; BootOnce path; role-not-host | DEFERRED | `CriomOS` |
| `nz0t` | prometheus API auth via gopass-fed token + mint tool | DEFERRED | `CriomOS` (secrets-adjacent) |
| `osoo` | backup WiFi password stored via sops-nix not plaintext | DEFERRED | `goldragon`/`CriomOS` (secret-adjacent; see note) |
| `p7kn` | install big Gemma multimodal models bf16 on Prometheus; quant variants in llama-server | DEFERRED | `CriomOS` (or `CriomOS-home`) |
| `ufjd` | node NixOS configs build/realize on target node; deploy uses lojix-cli on host | DEFERRED | `CriomOS` |
| `upza` | privileged ops via `ssh root@host` with operator key; sudo not the path | DEFERRED | `CriomOS-home` or workspace `AGENTS.md` (cross-cutting) |
| `wn7q` [SECRET] | Prometheus USB backup admin network; backup SSID/password in sops-nix | DEFERRED | `goldragon` (router data) / `CriomOS` (redact) |
| `wprd` | Ouranos ThinkPad battery-care 75-80% thresholds | DEFERRED | `CriomOS-home` (host config) |

Note on `osoo`/`wn7q`: `goldragon/datom.nota` already carries the router WiFi
references (`routerWifiSaePasswords`, `criome-backup` SSID,
`routerBackupWifiPassword` handles) — so the FACT of these networks is cluster
data in `goldragon`; the secret VALUES live in sops-nix per `CriomOS`. Route the
intent to whichever surface owns the declaration, never paste the secret value.

## Evidence the cloud home is real and already in use (observed facts)

F1. `repos/goldragon/README.md` (verbatim): "Cluster proposal for the
LiGoldragon kriom. Production data for every node, user, and trust relation in
the cluster." `AGENTS.md`: "Data repo only. Owns the cluster proposal — the
source of truth for every node, user, and trust relation in the LiGoldragon
kriom." It is a tracked git/jj repo with `origin` on GitHub.

F2. `repos/goldragon/datom.nota` already encodes the production cluster: nodes
`balboa`, `ouranos`, `prometheus`, `tiger`, `zeus`, `vm-testing` with per-node
trust (`Min`/`Max`), `VmHost`, `NixBuilder`, `NixCache`, `PersonaDevelopment`
roles; Prometheus router WiFi (`routerWifiSaePasswords`) and `criome-backup`
backup WiFi (`routerBackupWifiPassword`); users `bird`, `li`; domain
`goldragon.criome.net`. This is exactly the substrate the cloud/node records
describe.

F3. `git worktree list` shows a live `cloud-node-data` worktree at
`/home/li/wt/github.com/LiGoldragon/goldragon/cloud-node-data` on branch
`cloud-designer-cloud-node-data`. Its commits ADD the cloud-node records'
content:
- `b10df73` "declare doris — a DigitalOcean CloudNode in the cluster data"
- `53cddfe` "doris low trust (Min) — cloud-hosted nodes are minimally trusted"
- `2bfca41` "mark doris unprovisioned — placeholder host key, awaiting a role"
- The `datom.nota` diff adds `doris (CloudNode ... [DigitalOcean Droplet] ...
  digitalocean-nyc3 ...)` with an inline comment "Spirit zeqq." This is records
  `5pf6` and `zeqq` already homed on a branch.

F4. `protocols/active-repositories.md` (workspace canon) lists `cloud`,
`signal-cloud`, `meta-signal-cloud`, `goldragon`, `lojix`, `signal-lojix`,
`meta-signal-lojix` as live repos, describes `cloud` as the witnessed
provider-API daemon, and has a "Two deploy stacks coexist" section confirming
`lojix` is the live successor to `lojix-cli`. The `cloud`, `signal-cloud`,
`meta-signal-cloud` directories exist on disk under `/git/github.com/LiGoldragon/`.

F5. `lojix-cli` is retired: no symlink in `repos/`, and `active-repositories.md`
states "`lojix-cli` is untouched by the arc — stays at the current schema and
retires after CriomOS migrates." The live `lojix` repo's `README.md`/`AGENTS.md`
name it the replacement deploy stack (one crate, two binaries `lojix-daemon` +
`lojix`).

## Interpretations (scout judgment, flagged as such)

- The manifest deferred to `lojix-cli` because at routing time the author treated
  the deploy home as the legacy CLI. The correct durable home for forward-looking
  deploy intent is `lojix` (with its `signal-lojix`/`meta-signal-lojix`
  contracts), not `lojix-cli`. `ufjd` is the one record that legitimately names
  `lojix-cli` (it is a present-tense operational fact: "Deploy uses lojix-cli on
  the host") — route it to `CriomOS` deploy docs and let it note the lojix-cli→
  lojix migration.
- The cloud records split cleanly by subject: cloud-DAEMON behavior → `cloud`;
  cloud-NODE existence/trust/role → `goldragon` (data); OS image for cloud nodes
  → `CriomOS` (per `1hyg`). This three-way split is already the live
  architecture (`1hyg` itself states CriomOS owns the image definition, cloud
  owns snapshot-id selection/provisioning, cluster data owns per-node config).
- Nothing in the genuinely-deferred set needs a "drop" disposition: every record
  maps to a live repo. The only records that would have warranted "drop (config
  for retired lojix-cli)" do not exist — the lojix intent is forward-valid for
  the successor repo.

## Recommended overall disposition

1. **Correct the manifest's premise.** Replace the `lojix-cli` deferral target
   with the live `lojix` repo (+ `signal-lojix`/`meta-signal-lojix` for the
   two-contract records `vudl`, `7kyx`). Replace the "no cloud repo" assumption
   with the live `cloud` repo for daemon records and `goldragon` for node/trust
   data records.
2. **Un-defer the whole code/config set (31 records).** All have live homes:
   - cloud daemon → `cloud/ARCHITECTURE.md` (and contracts): `150a 16l0 7kyx 8fe9 iprx m3eg mbmy nsi2` (8).
   - cloud node/trust → `goldragon` (data; already partly on the `cloud-node-data` branch): `5pf6 zeqq` (2).
   - deploy daemon → `lojix/ARCHITECTURE.md`: `2alg 2qhw 75pw h03z lc28 mq5s vfgk vudl` (8).
   - OS / node OS → `CriomOS` / `CriomOS-home`: `0a9p 1hyg 6wz8 878r cncj kx32 nz0t osoo p7kn ufjd upza wn7q wprd` (13).
3. **Recognize the two cloud-node records are already homed** in the
   `cloud-node-data` branch of `goldragon`; the rehoming task is to land that
   branch and confirm `5pf6`/`zeqq` are covered, not to write them fresh.
4. **Honor secret discipline** on `2qhw`, `wn7q` (SECRET-flagged), and the
   secret-adjacent `nz0t`, `nsi2`, `iprx`, `osoo`: route the intent to the
   config surface that declares the credential, never the value; values stay in
   gopass/sops-nix.
5. **`persona` (11) and `schema-cc` (1) are out of scope** for the code/config
   bead — they are component-architecture and route to their own live repos
   (`persona`, and `schema-cc` is the only bucket with NO obvious live repo;
   confirm whether a `schema-cc` repo exists before treating `vpbx` as a real
   deferral — it was NOT in the cloud/T4-code scope of this investigation).

## Checks run (exact results)

- `repos/goldragon/README.md` / `AGENTS.md` read → "cluster proposal … source of truth for every node, user, and trust relation."
- `git worktree list` in `repos/goldragon` → live `cloud-node-data` worktree present.
- `git log main..cloud-designer-cloud-node-data` → 4 commits declaring/trusting/marking doris; diff adds `doris (CloudNode …)` citing "Spirit zeqq."
- `ls /git/github.com/LiGoldragon/{cloud,signal-cloud,meta-signal-cloud,lojix,signal-lojix,meta-signal-lojix}` → all present on disk.
- `ls repos/ | grep lojix` → no `lojix-cli` symlink (retired); successor `lojix` present in ghq root.
- `protocols/active-repositories.md` → lists `cloud`/`goldragon`/`lojix` as live; "two deploy stacks coexist"; "`lojix-cli` … retires after CriomOS migrates."
- Full record text for all 31 deferred code/config ids extracted from `/tmp/spirit-archive-extract/archived-spirit-records.dump.md` (descriptions, domains, referents) — basis for the per-record concern column.

## Blockers and unknowns

- **`goldragon` is a Jujutsu-only, push-immediately data repo** (`AGENTS.md`:
  "Jujutsu only. Never git CLI. Push immediately after every change."). Landing
  cloud-node intent there must follow that discipline and claim the path.
- **The `cloud-node-data` branch is unmerged** (`2bfca41`, not on `main`). Its
  disposition (merge to `goldragon/main`) is the open action that would close
  `5pf6`/`zeqq`. Not verified here whether a bead already tracks that merge.
- **`schema-cc` repo existence NOT verified** — outside this investigation's
  cloud/T4-code scope; flagged so the next worker checks before treating `vpbx`
  as a live deferral vs a drop.
- Whether `cloud` records should land in `cloud/ARCHITECTURE.md` vs the contract
  repos for the two-contract records (`7kyx`, `vudl`) is a placement nuance for
  the implementer; both target repos are live.
- I did not read `cloud/ARCHITECTURE.md` itself (the repo's existence and role
  are confirmed via `active-repositories.md` and on-disk presence; the exact
  current ARCHITECTURE coverage of these records was not diffed).
