# 5 · Synthesis — self-audit verdict + fix list, lojix↔cloud integration, questions

cloud-designer synthesis lane, session 71. Consolidates the three
self-audit lanes (`1-audit-report-68.md`, `2-audit-69-70.md`,
`3-audit-captures-docs.md`) and the lojix-integration design lane
(`4-lojix-cloud-integration.md`). Every fix below was re-verified against
source at cloud `HEAD 3b38cdd`, meta-signal-cloud `54d62be`, signal-cloud
`4e846bc`, nota-next codec, and the `cloud-designer-intent-refresh` branch
INTENT.md before listing. Read-only lane — fixes are described for the
main agent to apply, not applied here.

> **Correction (session 72).** The lojix deploy leg in the sequence diagram
> below shows `nix copy --to ssh-ng://`; lojix is now **build-on-target**
> (`nix build --eval-store auto --store ssh-ng://… <drv>^*`, realize in the
> node's store, copy is a no-op — report 150). The implementation-ready,
> corrected handoff supersedes this one:
> `reports/cloud-designer/72-lojix-cloud-implementation-research/6-synthesis.md`.

## Self-audit verdict

The session's work holds up. Across the four threads the audit lanes tried
to refute — the cloud engine audit (68), the token/Cloudflare report (69),
the Tier-2 spine report (70), and the durable captures (Spirit
`hcp8`/`iprx`, INTENT.md, active-repositories) — **no factual error,
invented handle, or ungrounded structural claim survived that isn't
already corrected on the branch.** What remains is a short tail of genuine
blemishes: one cross-layer conflation in INTENT.md, one doc/flake-vs-INTENT
internal inconsistency, one over-reaching Spirit cross-reference, and two
wording imprecisions in report 70. None changes a verdict; all are worth
fixing for grounding hygiene.

Specifically, lane by lane:

- **Report 68 (engine audit) — stands, two findings now stale-favorable.**
  Every still-checkable structural claim (single-`EngineActor` blocking
  shape, dead sema pilot, wire two-tree drift, Hetzner-unshipped,
  DNS-only default daemon) reproduces verbatim at `3b38cdd` and none is
  overstated. Two findings move to PARTIALLY CLOSED after report 70's live
  run: **P1-b** ("no apply crosses the daemon socket") is closed on the
  *behavioral* axis — report 70 drove create/observe/destroy over the real
  ordinary+meta sockets against live DigitalOcean (droplet 578873541), and
  the production apply path is real and shipped
  (`cloud/src/lib.rs:1637-1677` `apply_digitalocean_host_plan`, dispatch
  `:1569-1570`, `flake.nix:125-129`). **Risk #1** ("no built-artifact
  witness of a live mutation") is likewise closed on behavior. But the
  *artifact* axis still stands for both: the one committed spawned-daemon
  test (`tests/runtime.rs:292`) connects the ordinary socket and answers a
  capability read only — it drives no `ApplyPlan`; the DO live test
  (`tests/digitalocean_live.rs:29`) is `#[ignore]` and drives
  `digitalocean::HttpApi` directly, never the socket; the only Nix check
  (`flake.nix:155-161`) runs `--ignored --list` and executes nothing.
  Honest post-70 state: **DigitalOcean spine witnessed live once
  (manual); no re-runnable artifact.** No fix to report 68 — it graded
  correctly at its time and the staleness is favorable.

- **Reports 69 + 70 — substantially accurate, two wording blemishes in 70.**
  Report 69's flake-line-46 wrong-gopass-path bug is exact, its CF
  mutation surface and 15 record kinds confirmed, its threat model sound.
  Report 70's socket protocol matches the parser (host `Observation`
  variant is `Servers` not `ObserveServers`, the newtype double-nesting
  rule holds, the credential env var and dual-socket bind are real). The
  only issues are wording-level (an "alias newtype" mislabel for a named
  struct, a paraphrased parser-error quote) plus the live-run facts
  (droplet id, ~1s bind) that have no checked-in witness artifact — flagged
  *unwitnessed*, not *wrong*, because nothing in source contradicts them.

- **Captures — clean, two INTENT.md corrections + one Spirit blemish.**
  Both new Spirit records are well-formed and correctly scoped; `g7zd` is
  cleanly retired (returns record-not-found) with its DO-lead intent fully
  migrated into `hcp8` and no duplicate Hetzner-lead record left behind.
  The remaining items are the INTENT.md Cloudflare-handle conflation, the
  flake/README-vs-INTENT gopass inconsistency, and the `iprx` sops-nix
  cross-reference.

### Fix list

These are the genuine corrections, prioritized. P1 = factual error a
reader would act on wrongly; P2 = grounding/consistency defect; P3 =
wording precision. **There is no P1 in this session** — the work was
accurate.

| What | Where | Severity | Action |
|---|---|---|---|
| INTENT.md presents `CF_API_TOKEN` as the Cloudflare credential handle the daemon reads, in parallel with the DO/Hetzner daemon-read handles. The daemon-read handle is `CLOUDFLARE_DNS_TOKEN` (`tests/runtime.rs:470,513,561`); `CF_API_TOKEN` is the env var the `flarectl` subprocess reads downstream (`cloudflare_cli.rs:18` const, `:50` `.env(...)`). Cloudflare alone shells out (`cloudflare.rs:53` resolves the handle, then hands the value to `flarectl`), so its handle and its downstream var are two different names. | `~/wt/github.com/LiGoldragon/cloud/intent-refresh/INTENT.md:36` (cloud-designer-intent-refresh branch) | P2 | Reword the Cloudflare clause to name the daemon-read handle (`CLOUDFLARE_DNS_TOKEN`) as the parallel to DO/Hetzner, and note `CF_API_TOKEN` separately as the var `flarectl` reads downstream — e.g. "Cloudflare from `CLOUDFLARE_DNS_TOKEN` (the daemon-read handle; the resolved token is passed to the bundled `flarectl` as `CF_API_TOKEN`)". |
| INTENT.md:37 already reads `gopass cloudflare.com/token` (the report-69 recommendation was applied), but `flake.nix:46` and `README:15` still read `cloudflare/api-token`. Internal inconsistency within the same repo/session: INTENT documents a path the shipped flake does not use. (DO already took the `.com` correction — `flake.nix:71` reads `digitalocean.com/api-token`.) | `cloud/flake.nix:46` (two occurrences in the wrapper line) and `cloud/README:15`; consumer of the report-69 rec | P2 | Move the flake and README Cloudflare gopass path to `cloudflare.com/token` to match INTENT.md and the DO `.com` shape — OR, if the secret-store entry is genuinely named `cloudflare/api-token`, revert INTENT.md:37 back to `cloudflare/api-token` and retract report-69:128-131. The real gopass key name is a secret-store fact not inspectable here; pick the direction once and align all three (INTENT, flake, README). Belongs on the cloud operator/doc branch. |
| Spirit `iprx` body attributes a "criome-custodied AND sops-nix machine-identity pattern" to `h03z`. `(Lookup h03z)` is purely about lojix custodying its operational credentials / unattended machine identity through **criome** (vs borrowing the operator's GPG/SSH session); h03z does not mention sops-nix. The criome-custody half is grounded; the sops-nix attribution is not. | Spirit record `iprx` (cross-reference clause) | P3 | Edit `iprx` (via `Clarify`/`ChangeRecord`) to drop "sops-nix" from the "pattern of h03z" phrase, leaving the criome-custody attribution. Keep the directional intent intact. |
| Report 70 labels `HostPlanPreparation` "an alias newtype over `DesiredHostState`". It is a **named single-field struct** (`meta-signal-cloud/src/lib.rs:216-218`, field `desired_host_state: DesiredHostState`) — not a Rust newtype or type alias. The structural consequence the report draws (one inner record → one extra nesting → double parens) is correct; only the label is imprecise. | `reports/cloud-designer/70-tier2-daemon-spine-proven.md:83` | P3 | Replace "alias newtype over `DesiredHostState`" with "a single-field struct wrapping `DesiredHostState`". Leave the nesting consequence unchanged. |
| Report 70 quotes the parser error as "HostPlanPreparation to hold 1 root object, found 5". The codec source emits "to hold {expected} root **objects**, found {found}" (`nota-next/src/codec.rs:65`), plural and prefixed "expected". Substance identical; quote is paraphrased. | `reports/cloud-designer/70-tier2-daemon-spine-proven.md:86` | P3 | Either mark it as a paraphrase ("the parser complains it expected one root object but found several") or quote the codec verbatim. Minor. |

If those five are applied, the session's durable surface (INTENT.md, the
two reports, `iprx`) is fully grounded. The unwitnessed live-run facts and
the missing socket-apply artifact are **not** fixes to the reports — they
are correctly stated as "witnessed manually, no re-runnable artifact," and
closing them is *new work* (build a committed socket-apply test), which I
carry into the questions below.

## lojix↔cloud deployment integration

### Verdict

**Pre-baked CriomOS `CloudNode` snapshot, then activate — not bare-node.**
cloud and lojix are two operator-driven daemons that **never call each
other**; they are joined by the operator (or a thin handoff tool) through
exactly two shared facts: a **node domain/IP** and a **CriomOS closure**.
There is **no wire contract between the daemons and none is needed** — the
coupling is the domain name `<node>.<cluster>.criome` plus the ssh-key
identity, both external orchestration, and **zero new wire field** is
required (`image_name`, `ipv4_address`, and `DomainNameSystemRecord`
already carry everything). This is the right shape and it preserves each
daemon as a single-responsibility Signal endpoint.

The pre-baked decision (Spirit `ad53`) is forced by lojix's mechanism:
lojix has **no install path** — it assumes the target is already a
systemd-boot UEFI NixOS with `bootctl` and a mutable `/boot`
(`lojix schema_runtime.rs:2390-2515`, report 46-1 §3). Only a pre-baked
CriomOS image satisfies that on first boot; a bare stock-Ubuntu node would
force a one-time `nixos-anywhere` install hop before lojix's copy/activate
pipeline means anything. cloud already plumbs the snapshot id through the
existing `HostPlan.image_name` field into `ServerSpec.image`
(`cloud/src/lib.rs:1661` DO, `:1578-1612` Hetzner) — so the split is clean:
**CriomOS owns the image bytes, cloud selects the snapshot id, lojix
activates generations.**

### The handoff contract (create → observe → DNS → deploy)

The seam has four steps, each an existing NOTA op on an existing socket,
and **the create→observe seam is the load-bearing one**: `ApplyPlan
[Create]` returns only `PlanApplied { plan-id }` (`cloud/src/lib.rs:1672`)
— **the IP is not returned by create.** The node's IP/identity surface
*later* via `Observe Servers → CloudHost { host_identifier, ipv4_address,
host_status }` (`signal-cloud/src/lib.rs:283-292`; report 70 witness). So
the orchestrator must **poll Observe until `host_status` leaves
`Initializing` and an `ipv4_address` is present** before it can publish DNS
or hand off to lojix. Host-create and DNS-create are **disjoint
operations** — the `apply_*_host_plan` path issues no DNS call
(`cloud/src/lib.rs:1547-1677`); the orchestrator issues the A-record
(`RecordKind::AddressV4 → "A"`, `cloudflare_cli.rs:324`) as a second meta op
after observing the IP, using cloud's *own* Cloudflare capability.

```mermaid
sequenceDiagram
    actor Op as Operator / handoff tool
    participant CriomOS as CriomOS<br/>(image bytes)
    participant Cloud as cloud daemon<br/>(compute + DNS)
    participant Prov as Provider<br/>(DigitalOcean / Hetzner)
    participant Node as New node<br/>(CloudNode snapshot)
    participant Lojix as lojix daemon<br/>(generation activator)

    Note over CriomOS,Prov: ONE-TIME per provider — mint the CloudNode snapshot (ad53, UNBUILT)
    CriomOS->>Prov: build CloudNode image -> upload (DO) / bootstrap-snapshot (Hetzner) -> numeric image id

    Note over Op,Node: PER NODE — create -> observe -> DNS -> deploy
    Op->>Cloud: PrepareHostPlan (provider, host, type, IMAGE=snapshot-id, ssh_key_name)
    Op->>Cloud: ApprovePlan / ApplyPlan [Create]
    Cloud->>Prov: create_host(ServerSpec{ image=snapshot, ssh_keys=[plan.ssh_key_name] })
    Prov->>Node: boot CloudNode snapshot; cloud-init injects ssh key
    Cloud-->>Op: PlanApplied(plan-id)  %% NO ip returned — load-bearing seam

    loop poll until host_status != Initializing AND ipv4_address present
        Op->>Cloud: Observe Servers
        Cloud-->>Op: CloudHost{ host_identifier, ipv4_address, host_status }
    end

    Op->>Cloud: apply DNS plan: A  <node>.<cluster>.criome -> ipv4  (cloud's own Cloudflare cap)
    Cloud->>Prov: Cloudflare create A record

    Note over Lojix,Node: lojix's existing pipeline — the domain is the ONLY coupling
    Op->>Lojix: Deploy (cluster, node, FullOs, BootOnce)
    Lojix->>Node: nix build --eval-store auto --store ssh-ng://root@<node>.<cluster>.criome <drv>^*  (build-on-target; copy is a no-op, sops inside the realized closure)
    Lojix->>Node: ssh root@<domain> switch-to-configuration boot  (node decrypts sops at activation — cjrl)
    Lojix-->>Op: AcceptedDeploy(generation-id)
```

### The secret / identity path

**Secrets never touch cloud.** Cluster/node secrets ride **inside the
lojix-copied CriomOS closure** as sops-encrypted files and decrypt on the
node at `switch-to-configuration` time (Spirit `cjrl`); cloud only ever
sees an IP and a domain. This is live-gated — report 40-2 shows a router
node hard-fails eval without `sopsFiles`, while secret-free
zeus/tiger/ouranos deploy with the empty stub. The **first CloudNode
cutover targets a secret-free minimal profile** so sops materialization is
off the critical path.

Three identities, three custodians, no overlap:

| Identity | Used for | Custodian (today → end-state) | State |
|---|---|---|---|
| cloud provider API token | create/destroy nodes | gopass handle → env var behind `0o600` owner socket (`iprx`) → criome-custodied | built |
| node ssh / deploy key | lojix reaches the node | operator ssh identity (report 46-1 §6) → criome-custodied (`h03z`) | built (operator), intended (criome) |
| node host / age key | decrypts sops at activation | the node's own machine identity (`cjrl`) → criome-custodied (`h03z`) | per-node; sops path live, criome integration unbuilt |

The ssh key cloud injects at create (`ServerSpec.ssh_keys =
[plan.ssh_key_name]`, `cloud/src/lib.rs:1658-1664`) **must be the public
key of lojix's ssh/nix-copy identity** — that is the whole authentication
join. Under `h03z`/`iprx` the migration end-state is a custody upgrade to
the *same* sequence (operator session → criome machine principal), not a
reshape.

### What's built vs unbuilt

**Built and proven live:** cloud create→observe→destroy over the daemon
socket spine against live DigitalOcean (report 70); cloud's Cloudflare DNS
A-record capability; ssh-key injection by provider-registered name; lojix's
full copy + UEFI `BootOnce` activation pipeline (validated against a local
VM, report 46-3); the sops-nix-at-activation gate with the secret-free
escape proven (report 40-2).

**Unbuilt / open:**
- The CriomOS `CloudNode` species + gate module + provider-format build
  attribute — the snapshot itself (`ad53` is a captured Decision, not an
  artifact; report 65 §1).
- The first-snapshot mint per provider: DigitalOcean has a true custom-image
  upload API (no throwaway server); Hetzner has **no** upload API, so its
  first snapshot must be cut from a bootstrapped running server (report
  65 §3).
- **The create→observe→DNS→deploy orchestration glue** — nothing sequences
  the four legs today; report 70 ran the cloud legs by hand and never
  crossed into lojix. This is the first thing to build.
- criome-custodied deploy/machine identity (`h03z`/`iprx` end-state).
- A SEMA-persisted provisioning ledger binding (cluster, node) ↔ (provider,
  host_identifier, ipv4) — that mapping lives only in the orchestrator's
  head today (cloud INTENT.md names SEMA persistence as future).

### Recommendation

Build **a thin, operator-authorized handoff tool** that runs the
create→observe→DNS→deploy sequence, each step an existing NOTA op on an
existing socket — **not** a daemon-to-daemon wire. cloud stays the
compute/DNS control plane; lojix stays the generation activator; CriomOS
owns the image; the operator authorizes the run. The tool needs zero new
wire field on either contract. The create→observe poll loop is the one
piece of real glue and should be the tool's first responsibility.

## Questions for the psyche

These are genuine forks the design cannot resolve without intent.

1. **Handoff: a tool now, or hand-issued NOTA for the first cutover?** The
   orchestration glue is unbuilt and is the first thing to build. The
   recommendation is a thin operator-authorized handoff *tool* (not a
   daemon-to-daemon wire). Do you want that tool built now, or continue
   hand-issuing the NOTA legs (as report 70 did for the cloud side) for the
   first end-to-end run?

2. **First end-to-end proof path, given the `CloudNode` snapshot is
   unbuilt.** `ad53` is a captured Decision, not an artifact. Until the
   snapshot exists, a live cloud+lojix test must either (a) boot stock
   `ubuntu-24-04-x64` and add a one-time `nixos-anywhere` install hop, or
   (b) reuse the proven Prometheus-hosted local VM path (report 46) that
   sidesteps cloud. Which path for the first proof?

3. **Which provider leads the `CloudNode` image work?** The first-snapshot
   mint diverges: DigitalOcean has a real custom-image upload API; Hetzner
   has none, so its first snapshot must be cut from a bootstrapped running
   server. `hcp8` makes DigitalOcean the lead compute provider — does the
   image work follow that (DO first), or do both providers get the snapshot
   in lockstep?

4. **Does the handoff need a durable provisioning ledger now?** cloud has
   no SEMA-persisted (cluster, node) ↔ (provider, host_identifier, ipv4)
   binding; it lives only in the orchestrator's head. For the first cutover,
   is per-run orchestrator state acceptable, or should the durable ledger
   land before the first live handoff?

5. **Which ssh identity do we register for the first live run?** The key
   cloud injects at create (`cloud/src/lib.rs:1658-1664`) must equal the
   public key lojix's ssh/nix-copy inherit. Today that is the operator's
   session identity (report 46-1 §6); under `h03z` it becomes
   criome-custodied. Which identity do we register for the first live run —
   operator session now, or stand up the criome-custodied deploy identity
   first?

6. **Cloudflare gopass path — confirm the secret-store key name** (resolves
   fix #2). INTENT.md now says `cloudflare.com/token`; the flake and README
   still say `cloudflare/api-token`. The true entry name is a secret-store
   fact not inspectable from code. Which is the real key — so we align
   INTENT, flake, and README to it and either keep or retract report-69's
   `.com` recommendation?
