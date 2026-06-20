# 77 — CloudNode audit remediation: low trust + substrate model

cloud-designer, 2026-06-20. Resolves the two design decisions the psyche made
after report 76 (the live-deploy confirmation): doris is a real cluster member
at low trust, and the cloud-node role is modeled with typed enums rather than
bool accretion. Both implemented, validated, recorded.

## 1. doris is a real, low-trust member

Per psyche: [doris should have a low trust, since its in the cloud] (Spirit
`5pf6`, Principle Medium). Cloud-hosted nodes run on third-party provider
hardware outside our physical control, so they join as real but minimally-
trusted members.

Mechanism: effective trust is `min(NodeProposal.trust, clusterTrust.nodes[n],
clusterTrust.cluster)`. Following the established balboa convention, doris's
per-node `NodeProposal.trust` is dialed `Max → Min` (the cluster-trust map
stays `Max` like every node). `Min`, not `Zero`: `Zero` on the magnitude
ladder means actively-distrusted/absent — too strong for a node we deploy and
SSH into.

Validated — doris now projects:

```
trust.min=true  trust.max=false   isFullyTrusted=false   isDispatcher=false
behavesAs.cloudNode=true   behavesAs.bareMetal=true   species=CloudNode
```

So doris is a real cluster member but is kept out of the fully-trusted
builder / dispatcher / cache / admin-key roles (all gated on `Max`).
goldragon `53cddfe`.

## 2. Typed enums replace the TypeIs one-hot

Per psyche: selected the typed-enum modeling over keeping the `cloud_node`
bool (Spirit `q4gd`, Principle Medium). The consumer analysis sharpened what
that means, and corrected the self-audit (75) on two points:

| Audit (75) claim | Reality found by consumer analysis |
|---|---|
| Add a typed `Substrate{Metal\|Pod}` enum | The substrate is **already typed** — `MachineSpecies{Metal\|Pod}` on `machine.species`, exposed on the projection. No new enum needed. |
| `cloud_node` is dead state | `cloud_node` is a **live CriomOS gate** — `disks/cloud-node.nix` reads `behavesAs.cloudNode`. Deleting it would break the image gate. |
| (not flagged) | The real dead accretion is the **`TypeIs` one-hot**: 11 bools mirroring `NodeSpecies`, used only internally to derive `BehavesAs`; Nix reads the facets, never `typeIs` (its one CriomOS reference is a commented-out broken line). |

So the refactor deletes the `TypeIs` one-hot and derives `BehavesAs` directly
from the typed `NodeSpecies` + `MachineSpecies`. `BehavesAs` stays — it is the
live cross-repo gating contract, and its role facets (`center`/`router`/`edge`
/…) are **unions over several species** (a `Hybrid` is both edge and router),
not a one-hot, which is the whole reason it exists as a named contract.

Validated — projected JSON drops the `typeIs` key; `behavesAs` (cloudNode,
bareMetal, edge, …) and `machine.species` intact; **64 tests green**.
horizon-rs `750f8cf`.

The accretion vector is closed: adding a node species no longer adds a bool to
a one-hot — facets derive from the typed source enums.

## What "real member" still needs — a decision for the psyche

doris is now a real, low-trust member in the cluster data, but its host key in
the datom is still a **placeholder**. A genuine member needs its real host key,
which only exists once an actual droplet boots and generates
`/etc/ssh/ssh_host_ed25519_key`. That means provisioning a **standing**
(continuously-billed) DigitalOcean droplet — distinct from the always-destroy
test cycles run so far. That is a cost commitment, so it waits on explicit
psyche go-ahead.

## Remaining audit fix-now items (mechanical, queued)

Independent of the two decisions above, still open from report 75:
`until_running` returning a non-running host on timeout (#32); the placeholder
host key gaining a self-identifying marker until the real one lands (#5,
partially mitigated by the datom header note + low trust); a couple of
stale/over-stated comments and the "~55×" report figure caveat (#37, #38).
These are a short mechanical pass.

## Provenance

| Repo | Branch | Commit |
|---|---|---|
| goldragon | `cloud-designer-cloud-node-data` | `53cddfe` (doris low trust) |
| horizon-rs | `cloud-designer-cloud-node-species` | `750f8cf` (TypeIs deletion) |

Spirit: `5pf6` (cloud-node low trust), `q4gd` (typed-enum node model).
