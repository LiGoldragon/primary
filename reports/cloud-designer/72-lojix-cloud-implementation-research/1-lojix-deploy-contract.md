# 1 · The lojix deploy contract — the create→observe→DNS→deploy handoff

cloud-designer, Lane A, 2026-06-19. Read-only, source-grounded. Every
load-bearing claim cites `file:line`; NOTA strings are ground-truth
(emitted by the actual `nota_next` encoder over the real generated types,
not hand-written). The live Spirit store was down this session, so intent
is grounded in the manifested `INTENT.md` / `ARCHITECTURE.md` files and the
schema sources.

## TL;DR

- **The deploy verb is `meta-signal-lojix`'s `Deploy`, not "DeploymentSubmission".**
  `DeploymentSubmission` is an internal daemon type (`sema::DeploySubmission`,
  `schema_runtime.rs:2375`). On the wire the owner CLI sends one NOTA
  `(Deploy (System (...)))` where the inner record is `SystemDeployment`
  (`meta-signal-lojix/schema/lib.schema:107-117`). The `Deploy` and `System`
  heads ARE emitted; the `SystemDeployment` struct head is NOT (it lowers
  transparently inside the `System` variant).
- **Exact FullOs BootOnce string** (encoder-verified):
  `(Deploy (System (goldragon prometheus FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriOMOS/main BootOnce None [] None)))`
- **Build-on-target is the production default for any node ≠ the daemon's own host.**
  The daemon realizes the node's closure **in the target's own Nix store over
  `ssh-ng://root@<node>.<cluster>.criome`** (`nix build --eval-store auto
  --store ssh-ng://… <drv>^*`, `schema_runtime.rs:3991-4008`). The closure
  **never transits the daemon host**; the subsequent copy step is a **no-op**
  (`ClosureCopy::from_command` returns `Ok(None)` for `TargetStore`,
  `schema_runtime.rs:3475-3477`).
- **lojix needs ONLY the domain `<node>.<cluster>.criome`. No IP, ever, and
  no per-deploy IP override exists** anywhere in the deploy path
  (`SshTarget::root_at_node` derives the domain from cluster+node alone,
  `schema_runtime.rs:3350-3369`; exhaustive grep found no `ip`/`address`
  field on `Deploy`/`SystemDeployment`).
- **Confirm activation with `Query (ByNode …)`**, not the event log. A live
  `Generation` row exists only after activation committed
  (`record_generation_activated`, `schema_runtime.rs:2440-2496`). The
  `Query (ByEventLog …)` selection does **not** read the event log in this
  daemon — it falls through to the live-set query (`generation_matches` ⇒
  `ByEventLog(_) => true`, `schema_runtime.rs:2736`), and an actual
  `EventLogRead` reply is hard-rejected `MalformedSelector`
  (`schema_runtime.rs:1737-1741`).
- **Report 71's deploy-contact model is WRONG for the build-on-target
  default.** It says lojix "runs its existing `nix copy --to
  ssh-ng://root@<domain>` + remote-activate pipeline"
  (`71/4-lojix-cloud-integration.md:18`). With build-on-target there is **no
  `nix copy`** — the build already put the closure on the node. The handoff
  precondition therefore shifts: the node must be a usable **remote Nix
  store / remote builder over `ssh-ng` at build time**, not merely a copy
  destination at activation time.

## The handoff, end to end

```mermaid
sequenceDiagram
  participant OP as operator (local on daemon host, li)
  participant CLOUD as cloud daemon
  participant CF as Cloudflare (cloud's own op)
  participant LJX as lojix-daemon (owner socket)
  participant NODE as target node (<node>.<cluster>.criome)

  CLOUD->>CLOUD: provision pre-baked CriomOS CloudNode image
  CLOUD-->>OP: Observe Servers -> CloudHost { ipv4_address, host_name }
  OP->>CF: publish A record <node>.<cluster>.criome -> ipv4_address
  Note over OP,LJX: lojix is given ONLY the domain (cluster+node names);<br/>it derives <node>.<cluster>.criome itself
  OP->>LJX: meta-lojix "(Deploy (System (... FullOs ... BootOnce ...)))"
  LJX-->>OP: (Deployed (<deployment-id> (<commit-seq> <state-digest>)))
  LJX->>NODE: nix build --eval-store auto --store ssh-ng://root@<node>.<cluster>.criome <drv>^*
  Note over LJX,NODE: REALIZATION happens in the NODE's store.<br/>Closure never transits the daemon host.
  LJX->>NODE: copy step = NO-OP (closure already on node)
  LJX->>NODE: ssh systemd-run --unit=lojix-boot-once-deploy-<id> ... bootctl set-default OLD + set-oneshot NEW
  OP->>LJX: lojix "(Query (ByNode (<cluster> <node> (Some FullOs))))"
  LJX-->>OP: (Queried ([ (<gen> <dep> <cluster> <node> FullOs BootOnce BootPending <closure>) ] (<seq> <digest>)))
```

## 1 · The exact `meta-lojix` NOTA string (FullOs BootOnce)

### Wire root and nesting

The owner CLI `meta-lojix` parses its one argument into one
`meta_signal_lojix::schema::lib::Input` (`lojix/src/client.rs:164-166`),
whose request root is `[Deploy Pin Unpin Retire Test]`
(`meta-signal-lojix/schema/lib.schema:60`). `Input::Deploy` wraps the
single-field newtype `Deploy(DeployRequest)` (generated
`meta-signal-lojix/src/schema/lib.rs:50, 451`), and `DeployRequest` is the
variant enum `[(System SystemDeployment) (Home HomeDeployment)]`
(`schema/lib.schema:128`).

### `SystemDeployment` positional shape (the schema, declared order)

`meta-signal-lojix/schema/lib.schema:107-117` → generated struct
`meta-signal-lojix/src/schema/lib.rs:192-202`:

| # | field | type | this deploy |
|---|---|---|---|
| 1 | `ClusterName` | `String` | `goldragon` |
| 2 | `NodeName` | `String` | `prometheus` |
| 3 | `DeploymentKind` | `[FullOs OsOnly HomeOnly]` | `FullOs` |
| 4 | `source` | `ProposalSource` (`String`) | the goldragon `datom.nota` path |
| 5 | `flake` | `FlakeReference` (`String`) | `github:LiGoldragon/CriOMOS/main` |
| 6 | `SystemAction` | `[Eval Build Boot Switch Test BootOnce]` | `BootOnce` |
| 7 | `builder` | `(Optional Builder)` | `None` (build-on-target picks the target store) |
| 8 | `substituters` | `(Vec ExtraSubstituter)` | `[]` |
| 9 | `build_attribute` | `(Optional FlakeAttribute)` | `None` (production horizon path) |

### The string (encoder-verified, ground truth)

```
(Deploy (System (goldragon prometheus FullOs /git/github.com/LiGoldragon/goldragon/datom.nota github:LiGoldragon/CriOMOS/main BootOnce None [] None)))
```

Generated by round-tripping the real types through `NotaEncode::to_nota`
this session (a throwaway test, since removed). Notes that matter:

- The `SystemDeployment` head is absent — a single-struct-inside-variant
  lowers its fields positionally directly under `(System …)`. This matches
  the existing `meta-signal-lojix/tests/round_trip.rs:94`
  (`to_nota().starts_with("(Deploy ")`).
- `None` is the bare atom for an absent optional; `[]` is the empty vector.
- Bare atoms throughout (no quotation marks) — `goldragon`, the `/`-bearing
  path, and the `github:…/…` flake ref are all bare-eligible per the NOTA
  rule (single colon, slashes, at-signs stay bare).
- **Invocation:** `meta-lojix "(Deploy (System (…)))"` — one shell
  double-quoted NOTA argument, no flags (`lojix/src/bin/meta-lojix.rs:10-11`;
  `lojix/src/client.rs:125-127`). It exchanges on the owner socket
  (`LOJIX_OWNER_SOCKET`, default `/run/lojix/owner.sock`,
  `client.rs:151`), which is uid/gid-gated, so the call must originate
  **locally on the daemon host** (ARCHITECTURE.md:64-68; report 150 §"How a
  daemon deploy runs").
- **Reply:** `(Deployed (<deployment-identifier> (<commit-seq> <state-digest>)))`
  — `AcceptedDeploy { DeploymentIdentifier DatabaseMarker }`
  (`schema/lib.schema:134`). This is acceptance only; the deploy then runs
  asynchronously through the effect chain.

`OsOnly` is the same shape with field 3 = `OsOnly`; a `Switch` deploy sets
field 6 = `Switch` (and would `switch-to-configuration switch` instead of
the BootOnce transient unit — `schema_runtime.rs:3575-3596`). BootOnce is
the safe default: reboot 1 lands NEW, reboot 2 auto-reverts to the running
generation (`boot_once_script`, `schema_runtime.rs:3616-3635`).

## 2 · Build-on-target mechanics

### When it is chosen

`build_target` (`schema_runtime.rs:975-980`): an explicit `builder` in the
request always wins → `BuildTarget::Remote` (a configured Nix machine).
Otherwise `build_target_for(cluster, node)` decides
(`schema_runtime.rs:714-731`):

- **target node == daemon's own host** (`node_name == daemon_host`,
  `schema_runtime.rs:719`) → **`BuildTarget::Local`** (the host's store
  already holds any model closure; e.g. deploying ouranos from the
  ouranos-hosted daemon). `daemon_host` is a config field
  (`lib.rs:181`, `schema_runtime.rs:68,678`).
- **target node ≠ daemon host** → **`BuildTarget::TargetStore(ssh-ng://root@<node>.<cluster>.criome)`**
  (`schema_runtime.rs:722-723`). This is build-on-target, the production
  default for every node that is not the daemon's own host.

### What the build command does

`NixCommand::build_closure_in_store` (`schema_runtime.rs:3991-4008`):

```
nix build --no-link --print-out-paths \
  --eval-store auto --store ssh-ng://root@<node>.<cluster>.criome \
  <drv-path>^*  [--substituters … per ExtraSubstituter]
```

`--eval-store auto` keeps **evaluation** local and cheap on the daemon host
(it reads the flake and the `.drv`); `--store ssh-ng://…` directs **all
realization** — every output build/substitute, including a
multi-tens-of-gigabyte model NAR — **into the target node's store**
(`schema_runtime.rs:3981-3990`). The `^*` selector resolves the `.drv` to
its realized outputs (`output_installable`, `schema_runtime.rs:4010-4019`).

### Does the closure ever transit the daemon host? — NO (for `TargetStore`)

No. Realization happens in the target store; the daemon host holds only the
evaluation (`.drv` graph), never the realized model-bearing outputs
(ARCHITECTURE.md:18-29; `schema_runtime.rs:2851-2873`; report 150). The
copy step is a **no-op**: `ClosureCopy::from_command` returns `Ok(None)`
for `TargetStore` (`schema_runtime.rs:3475-3477`), and `run_copy_closure`
reports the closure copied without opening any `ssh-ng` transfer
(`schema_runtime.rs:2886-2904`).

Contrast: `BuildTarget::Local` realizes in the daemon host's store, and
`BuildTarget::Remote` offloads to a Nix machine **then copies the result
back into the daemon host's store** (`build_closure_remote` uses
`--builders @/etc/nix/machines`, `schema_runtime.rs:3965-3979`; report
436 §"What Remote Means Today"). Both then run a real `nix copy
--substitute-on-destination --to ssh-ng://root@<node>.<cluster>.criome`
(`ClosureCopy::invocation`, `schema_runtime.rs:3487-3496`). So **only
`TargetStore` keeps the closure off the daemon host**; `Remote` does not.

### When it stays Local

Exactly when the target node IS the daemon's own host
(`schema_runtime.rs:719-720`), or when name validation fails (unreachable
in practice for a submitted deploy, `schema_runtime.rs:724-729`).

### What the TARGET NODE must satisfy for a build-on-target deploy

| Precondition | Why / where |
|---|---|
| Reachable as a **remote Nix store over `ssh-ng` at BUILD time** as `root` | the build realizes there: `--store ssh-ng://root@<node>.<cluster>.criome` (`schema_runtime.rs:3991-4008`). This is the new, stronger requirement vs a pure copy target. |
| `root` **ssh key** trusted, `BatchMode=yes` (non-interactive) | every remote call is `ssh -o BatchMode=yes root@<domain> …` (`remote_invocation`, `schema_runtime.rs:3386-3397`); credentials are the operator's logged-in agent (report 150 §"Credentials"). |
| A working **nix daemon** + the node is a **trusted user / trusted-substituter** so `ssh-ng` store writes and signature checks pass | remote-store realization needs the node's nix-daemon to accept the pushed/built paths. |
| **systemd-boot UEFI NixOS** with `bootctl`, `nixos-generation-N.conf` entries under `/boot/loader/entries`, and a **mutable `/boot`** | activation runs `bootctl status` / `bootctl set-default` / `set-oneshot` and asserts the entry file exists (`boot_once_script`, `schema_runtime.rs:3616-3635, 3674-3689`); lojix has **no install path** (report 71/4 §(a), citing the activation pipeline). |
| `nix-env -p /nix/var/nix/profiles/system --set` + `switch-to-configuration boot` succeed as root | the BootOnce script and simple-switch path (`schema_runtime.rs:3588-3589, 3624-3625`). |
| Configured **substituters/caches** to make realization fast | optional but the point of build-on-target: the node substitutes signed model NARs from the cluster cache into its own store rather than rebuilding (`ExtraSubstituter` threading, `schema_runtime.rs:946-967, 3994-4006`; Spirit `lc28` direction per report 150). |

The node being a real SSH-reachable systemd-boot NixOS is exactly why the
handoff wants a **pre-baked CriomOS `CloudNode` image** (report 71/4 §(a),
Spirit `ad53`) — a bare Ubuntu node satisfies none of the activation
preconditions without a one-time install hop.

## 3 · Does lojix need the IP? — NO. Only the domain.

lojix needs **only the cluster name and node name**; from them it derives
the domain and needs nothing else:

- `SshTarget::root_at_node(cluster, node)` builds
  `root@<criome_domain>` from `CriomeDomainName::for_node(node, cluster)`
  (`schema_runtime.rs:3350-3369`) — `<node>.<cluster>.criome` order,
  asserted by the test `root@node-1.alpha.criome` for cluster `alpha`, node
  `node-1` (`schema_runtime.rs:4410-4412`).
- This single derivation feeds the build store URI (`ssh_uri`,
  `schema_runtime.rs:3378-3380`), the copy target, and the activation ssh
  (`as_ssh_arg`, `schema_runtime.rs:3382-3384`).
- **No per-deploy IP override exists.** The `SystemDeployment` record
  carries no IP/address field (`schema/lib.schema:107-117`), and an
  exhaustive grep across the runtime and both schemas found no `ip` /
  `ipv4` / `address` / endpoint field on the deploy path. The comment at
  `schema_runtime.rs:3337-3339` is explicit: the address is **computed from
  cursor fields already present**, "not threaded as a new
  horizon-projection field." `HostSelection`/`(OnHost h)` is the **test-VM**
  host picker (`schema/lib.schema:79`, `schema_runtime.rs:155-160`), not a
  deploy IP override.

Consequence for the handoff: the operator's only out-of-band step between
cloud and lojix is publishing the DNS A record
`<node>.<cluster>.criome → <ipv4_address>` (cloud's own Cloudflare
operation). lojix resolves the IP through DNS at ssh time; it is never told
the IP directly. **If the A record is wrong or unpropagated, every lojix
ssh/build/activate fails** — DNS is the single load-bearing join.

## 4 · The exact `lojix` Query NOTA to confirm Activated

Confirm via the **live generation set**, which is written only on
activation success:

```
(Query (ByNode (goldragon prometheus (Some FullOs))))
```

Encoder-verified ground truth. `ByNode` is `NodeSelector { cluster_name,
node_name, kind: (Optional DeploymentKind) }`
(`signal-lojix/schema/lib.schema:93`, generated
`signal-lojix/src/schema/lib.rs:292-296`). Drop the kind filter to see any
kind:

```
(Query (ByNode (goldragon prometheus None)))
```

Sent over the ordinary socket: `lojix "(Query (ByNode (…)))"`
(`lojix/src/bin/lojix.rs`; `client.rs:65-93`; default
`/run/lojix/ordinary.sock`). The reply is
`(Queried (GenerationListing …))`:

```
(Queried ([ (<gen-id> <dep-id> goldragon prometheus FullOs BootOnce BootPending <closure-path>) ] (<commit-seq> <state-digest>)))
```

A **non-empty `generations` vector with a row for `(goldragon, prometheus,
FullOs)` is the confirmation that the deploy reached Activated** — the row
is committed by `record_generation_activated` only after the `Activated`
phase (`schema_runtime.rs:2222-2226, 2440-2496`). For a **BootOnce** deploy
the row's `GenerationSlot` is **`BootPending`** (not `Current`) —
`activation_slot(BootOnce) => BootPending`
(`schema_runtime.rs:2930`) — so an empty-or-`BootPending` row is expected;
`Current` would mean a `Switch`.

### Why NOT the event log

It is tempting to read `DeploymentPhase::Activated` from the event log via
`(Query (ByEventLog (<from> <until>)))`. **That does not work in this
daemon:**

- `decide_ordinary_input` routes every non-`ByTestRun` selection —
  including `ByEventLog` — to `QueryGenerations`, NOT `ReadEventLog`
  (`schema_runtime.rs:1517-1528`).
- In `generation_matches`, `Selection::ByEventLog(_) => true`
  (`schema_runtime.rs:2736`), so a `ByEventLog` query returns **all live
  generations across every node**, ignoring the range — useless as a
  per-deploy phase probe.
- The real `read_event_log` path (`schema_runtime.rs:2756-2781`) is only
  reachable through the internal `SemaReadInput::ReadEventLog`
  (`schema_runtime.rs:2659`), which the ordinary `Query` verb never
  constructs; and if an `EventLogRead` reply did surface it is hard-rejected
  `MalformedSelector` (`schema_runtime.rs:1737-1741`).

So the **event-log phase stream is observed by pushed `WatchDeployments`
subscription events** (`DeploymentPhaseEvent`, `schema/lib.schema:142-150`;
ARCHITECTURE.md §6 "Push, never poll"), not by a `Query`. For a one-shot
confirmation the `Query (ByNode …)` live-set read is the correct probe;
for streaming progress use `(WatchDeployments (… <node> …))`.

## 5 · What report-71's design gets WRONG given build-on-target

Report 71 (`71/4-lojix-cloud-integration.md:18`, repeated in the §5
synthesis sequence diagram at `71/5-synthesis.md:162`) states the handoff
as:

> "lojix then runs its existing `nix copy --to ssh-ng://root@<domain>` +
> remote-activate pipeline to switch the node onto the cluster generation."

This describes the **`Local`/`Remote` build path** and is **wrong for the
production build-on-target default** (`builder = None`, target ≠ daemon
host):

1. **There is no `nix copy` step.** For `TargetStore` the copy is a no-op
   (`schema_runtime.rs:3475-3477, 2886-2896`). The closure is put on the
   node **by the build itself**, not pushed after.
2. **The node must be a usable remote Nix store / builder over `ssh-ng` at
   BUILD time, as root**, not merely a `nix copy` destination at activation
   time (`--store ssh-ng://…`, `schema_runtime.rs:3991-4008`). This is a
   strictly stronger precondition: the node's nix-daemon must accept
   remote-store realization, signatures, and the build itself — exactly the
   capability a pure copy target does not need. The handoff design must list
   "node is a working `ssh-ng` Nix store/builder for root" as a
   precondition, not just "SSH-reachable for copy + activate."
3. **The model-pull safety claim only holds for `TargetStore`, never for
   `Remote`.** If a future handoff passes an explicit `builder`, the build
   lowers to `Remote`, which **copies the realized closure back into the
   daemon host's store** before the `nix copy` to the node
   (`schema_runtime.rs:3965-3979`, report 436). For a large-AI node that
   re-introduces the model-pull-onto-daemon-host hazard report 150 exists to
   avoid. The handoff tool must leave `builder = None` for large-AI nodes.

Everything else in report 71's handoff (domain-as-the-only-join, no
inter-daemon wire contract, pre-baked CriomOS image, DNS A record published
by cloud's own Cloudflare op, activation assumes systemd-boot UEFI NixOS)
remains correct. The one correction is: **the deploy is build-on-target,
so the contact is a remote-store `nix build` + a no-op copy + BootOnce
activation — not `nix copy` + activate.**

## Open question

- The build-on-target build authenticates to the node's `ssh-ng` store as
  the **operator's logged-in ssh/GPG agent** (report 150 §"Credentials";
  no first-class daemon credentials yet, bead `primary-srmq`). The handoff
  is therefore **attended** — the operator must hold a live agent that the
  node's `root` `authorized_keys` trusts at build+activate time. Whether
  the pre-baked `CloudNode` image ships that operator key in
  `root`'s `authorized_keys` (so the very first lojix contact works) is the
  one precondition that report 71/4 §(a) flags as "unbuilt today" and that
  this contract depends on.
