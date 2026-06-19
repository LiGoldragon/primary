# 70 · Tier-2 daemon spine — PROVEN live (and the working socket protocol)

The audit (report 68) named as its #1 risk that no provider had a built
artifact witness of a live mutation *through the daemon spine* — the
register→prepare→approve→apply→observe path crossed the socket only for
capability reads and rejected registrations; no `apply` ever provisioned a
node over the socket (finding P1-b). That gap is now closed with a live
witness, and this report records the witness plus the exact socket protocol
(which was schema-inferred and undocumented — reverse-engineered from the
parser's arity errors).

## The witness

Driven entirely through the real Unix sockets of a booted `cloud-daemon`
(DO+Cloudflare build, kameo fork, synchronous `Store`), against live
DigitalOcean:

```
RegisterAccount        -> (AccountRegistered (DigitalOcean criome-test))
PrepareHostPlan        -> (HostPlanPrepared (criome-spine-test-DigitalOcean-host-plan
                                             DigitalOcean criome-spine-test
                                             s-1vcpu-512mb-10gb ubuntu-24-04-x64 criome-test Create))
ApprovePlan            -> (PlanApproved (...-host-plan))
ApplyPlan   [CREATE]   -> (PlanApplied (...-host-plan))      # droplet 578873541 created
ObserveServers         -> (Observed (Servers ([(DigitalOcean criome-test 578873541
                              criome-spine-test s-1vcpu-512mb-10gb ubuntu-24-04-x64 [] Initializing)])))
PrepareHostDestruction -> (HostPlanPrepared (...-host-destruction-plan ... Destroy))
ApprovePlan            -> (PlanApproved (...-host-destruction-plan))
ApplyPlan   [DESTROY]  -> (PlanApplied (...-host-destruction-plan))
final sweep            -> droplets: []     # gone, no leak
```

A real node (droplet `578873541`) was created, **observed by the daemon**,
and destroyed — every leg over the socket, no in-process shortcut. The
capability report confirms the build: `(DigitalOcean CloudHosts Compiled)`.

One honest note: the post-destroy `ObserveServers` still listed the host as
`Initializing` (DigitalOcean's delete is eventually-consistent; the droplet
was mid-deletion). The independent API sweep moments later showed
`droplets: []`, so the destroy succeeded — the stale read is DO's API
consistency window, not a daemon defect. Worth a follow-up: `ObserveServers`
right after a destroy can report a node that is already being torn down.

## The working socket protocol (reusable)

Boot:
```sh
# 1. encode the rkyv daemon config (modes default 0o600)
cargo run --example write_config --features digitalocean,cloudflare -- out.rkyv ord.sock meta.sock
# 2. boot the daemon (needs the credential env var the handle names); binds both sockets in ~1s
DIGITALOCEAN_ACCESS_TOKEN=... cloud-daemon out.rkyv &
# 3. clients target the sockets by env
export CLOUD_SOCKET_PATH=ord.sock CLOUD_META_SOCKET_PATH=meta.sock
```

Operations — `cloud <nota>` (ordinary socket) and `meta-cloud <nota>` (meta socket):

| Operation | NOTA |
|---|---|
| Capabilities | `cloud "(Observe (Capabilities (None None)))"` |
| Observe hosts | `cloud "(Observe (Servers (DigitalOcean None)))"` |
| Register account | `meta-cloud "(RegisterAccount (DigitalOcean <account> DIGITALOCEAN_ACCESS_TOKEN))"` |
| Prepare create | `meta-cloud "(PrepareHostPlan ((DigitalOcean <host> <server_type> <image> <ssh_key_name>)))"` |
| Approve | `meta-cloud "(ApprovePlan (<plan-id>))"` |
| Apply | `meta-cloud "(ApplyPlan (<plan-id>))"` |
| Prepare destroy | `meta-cloud "(PrepareHostDestruction (DigitalOcean <host>))"` |

Plan ids are **derived, deterministic strings**, not opaque UUIDs:
`<host>-<provider>-host-plan` (create) and
`<host>-<provider>-host-destruction-plan` (destroy) — so a caller can
construct them without round-tripping the prepare reply.

### The NOTA nesting rule (the part that bites)

Every operation decodes as `(VariantHead Payload)` — exactly **2 root
objects**. The payload shape depends on the payload *type*:

- **Inline-struct payload → flat record.** `Registration {provider,
  account, handle}` and `HostDestruction {provider, host_name}` are inline
  structs, so the payload is the flat record: `(DigitalOcean criome-test
  HANDLE)`.
- **Newtype/alias payload → one extra nesting.** `HostPlanPreparation` is
  an alias newtype over `DesiredHostState`, so it holds *one* object (the
  inner record): `((DigitalOcean host type image key))` — double parens.
  This is the single non-obvious shape; the parser error
  ("HostPlanPreparation to hold 1 root object, found 5") is the tell.
- **Scalar payload → bare atom.** A `PlanIdentifier`/`ProviderAccount` is a
  bare atom; `Optional` is `None` or `(Some x)`.
- **The hand-written contract tree can rename variants vs the schema.**
  The CLI parses the hand-written `signal_cloud::Operation`, whose
  `Observation` variant for hosts is **`Servers`**, not the schema's
  `ObserveServers` (the bridge maps one to the other). This is the audit's
  two-tree-drift finding (`68-3-P1-1`) biting in practice — until the
  schema cutover lands, drive the **hand-written** names.

## What this changes for the cloud audit

`68`'s headline was "adapter-proven, spine-unproven." The spine is now
proven for DigitalOcean create/observe/destroy. The remaining `68` risks
stand (the single-`EngineActor` blocking shape, the two-tree drift, the
Hetzner-unshipped gap, the `ad53` CloudNode platform half) — proving the
spine works does not make the daemon's architecture sound, it makes it
*usable for testing today*, which was the psyche's ask ("I want to be able
to use cloud to test things"). The blocking-actor risk (P2-a) is now the
top structural item: this lifecycle held one socket for the full duration
of each blocking provider call.
