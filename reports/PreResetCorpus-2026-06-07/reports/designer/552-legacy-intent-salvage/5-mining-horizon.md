# 552 — Legacy intent salvage — mining horizon.nota

## Scope

Scanned `intent/horizon.nota` — 29 records (text-only extraction at
`/tmp/intent-text/horizon.txt`). The file is the Horizon / lojix
lean-rewrite design thread: cluster-data shape, the species/services
fold into `roles`, boolean-to-variant migrations, and the
Yggdrasil-addressed network substrate. Most of it is already preserved
in the live guidance layer (`skills/typed-records-over-flags.md`,
horizon-rs `INTENT.md`) or in Spirit (`a2t4`, `qkvx`, `9p8v`, the
horizon charter records). Four core ideas surfaced as genuinely at
risk; everything else is preserved or too specific.

## Salvage candidates

### 1. Cluster data embeds no routing/addressing — Yggdrasil-style per-node identity bootstraps it

**Kind:** Principle

**Proposed topics:** `[cluster-data horizon yggdrasil addressing networking identity routing]`

**Proposed description:** Cluster data does NOT embed routing
details, peer endpoints, or transport ports. The cluster relies on
Yggdrasil-style unique per-node IP addresses derived from each node's
public key; routing tables bootstrap dynamically from those
identities, so peers find each other through the routing substrate
rather than through authored configuration. This is a workspace-wide
substrate assumption that informs every component contract: addressing
is not a cluster-data concern. The same key-derives-address pattern is
the approved (deferred) direction for other mesh memberships such as
Wireguard internal IPs, with the caveat that key-derived addressing is
protocol-native for Yggdrasil but a workspace convention elsewhere.

**Supporting verbatim:** "we have things like unique IP addresses with
the Yggdrasil routing system, and then these can be used to bootstrap a
routing table dynamically. So there's no need to embed all of this
stuff in the cluster configuration." (record 4, Maximum); "I'd rather
derive some kind of IP address from the wire guard public key, kind of
like how Yggdrasil does it." (record 18/20).

**Preservation evidence:** Queried Spirit
`[horizon cluster-data]`, `[yggdrasil addressing networking network]`,
`[addressing identity routing networking criome-domain]`, and
`[identity universal-identity hash networking]` — no record states the
Yggdrasil-derived-addressing-means-no-routing-in-cluster-data
principle. The only Yggdrasil hits are `actor-systems.md`'s
`YggdrasilKey` actor lifecycle (binary supervision, unrelated). Grepped
`yggdrasil` across all INTENT/ESSENCE/skills — only the actor example.
horizon-rs INTENT's proposal-boundary three-test covers
"non-derivable" generically but never names the addressing substrate.

**At-risk rationale:** This is the foundational network-substrate
assumption that JUSTIFIES the minimal cluster-data shape — it is the
"why" behind dropping routing/endpoint/port fields. The minimal-data
principle is preserved (`a2t4`, horizon-rs INTENT) but its load-bearing
justification — the routing substrate that makes it safe — exists
nowhere in the durable layer and would be lost on deletion.

### 2. A future network daemon discovers interfaces and assigns roles dynamically; interface names in cluster data are an acknowledged temporary hack

**Kind:** Clarification

**Proposed topics:** `[networking cluster-data horizon network-daemon future-direction interface-discovery]`

**Proposed description:** The destination network model is a dedicated
network daemon that discovers connectivity at runtime and assigns
interface roles dynamically — it figures out where the node's internet
connection comes from (a Wi-Fi access point one day, a LAN interface
the next) and distributes that connection across other interfaces.
Until that daemon exists, network interface names in cluster data are
an explicit short-term hack carried only so deploy can wire the system.
Treat the interface-name fields as transitional: do not deepen them,
do not grow further interface/topology fields, and do not build
dependent abstractions assuming their permanence.

**Supporting verbatim:** "currently it's a hack, right, it's a short
term hack, but we have things like network interface names in the
cluster data… right now we don't have that daemon" (record 5,
Maximum); "we're going to have to develop our own network daemon,
eventually… intelligent enough to try and get an internet connection
from something, whatever it is… and distributes that connection to its
LAN interfaces" (record 6).

**Preservation evidence:** Spirit queries
`[yggdrasil addressing networking network]` and
`[addressing identity routing networking criome-domain]` return router
backup-network and VM-testing records only — nothing on a future
network daemon or interface-discovery. Grepped
`network daemon|discover.*interface|interface.*role` across all
INTENT/ESSENCE/skills — empty. The concept is fully absent from the
durable layer.

**At-risk rationale:** This both names a real future-direction
destination AND marks a current field-set as deliberately temporary.
Losing it means a future agent could mistake the interface-name fields
for permanent schema and build abstractions on a surface the psyche has
flagged for removal. Conservative certainty kept at the record's own
level — it is a destination-naming clarification, not a committed build.

### 3. Additive feature vectors cannot express un-selection, so node KIND is a categorical label distinct from the capability vector

**Kind:** Principle

**Proposed topics:** `[cluster-data horizon roles variants categorical typed-records schema]`

**Proposed description:** When modelling node identity, separate the
categorical KIND ("what kind of cluster member this is") from the
additive CAPABILITY vector ("what specific things this node does"). A
feature/capability vector is additive — it adds capabilities and has no
natural way to express un-selection of a default — so KIND cannot be a
pre-selected-defaults model overridable by features; it must be an
explicit categorical choice with no implicit defaults. Cluster intent
is fully explicit. Some kind-roles are mutually exclusive (exactly one
per node, validated at projection with a typed error). A different
trust ceiling (e.g. a cloud-hosted node whose hardware cannot be
physically inspected) is a KIND difference, not a capability. The
general lesson generalises beyond nodes: the additive-vs-categorical
distinction is a schema-design axis — additive vectors for things you
turn on, categorical labels for the one-of-N essence that has no
"off".

**Supporting verbatim:** "the feature vector doesn't let you turn
stuff off. So if you have a center node… center node has services x, y,
z enabled and configured, and then you can't turn those off."
(record 23, Maximum, "Categorical model approved"); "cloud hosting
automatically implies a certain amount of trust. It's not the same as
self-hosting in my house, on my own hardware." (record 25).

**Preservation evidence:** Spirit
`[roles router node-service node-feature species]` and
`[boolean variant variants feature-flags typed-records]` return the
typed-cluster-data records (`qkvx`, `4wyw`, role/router deployment
records) but NONE state the additive-cannot-unselect reasoning or the
categorical-kind-vs-additive-capability axis.
`typed-records-over-flags.md` covers boolean→variant and
mutually-exclusive-sum (Form 2) but never the additive-vector
un-selection limitation that forces KIND to be categorical. Grepped
`categorical|additive feature|turn.*off|un-?select` across
INTENT/ESSENCE/skills — only intent-supersession "negation" hits,
unrelated. Genuinely absent.

**At-risk rationale:** This is the reusable schema-design reasoning
behind the species/services design — durable far beyond the specific
`roles` enum. The concrete merge (one `Vec<Role>` field, the variant
list, field order) is too specific and is already settled in horizon-rs
code/INTENT; but the GENERAL principle (additive vectors can't unselect
⇒ essence is categorical) is a transferable design rule that would be
lost.

### 4. Beauty budget goes to the durable layer, not the throwaway substrate — unavoidable ugliness lives in the layer being replaced

**Kind:** Principle

**Proposed topics:** `[horizon nix lowering aesthetic-gate cleanliness layering]`

**Proposed description:** When a reduction/projection layer (Horizon)
lowers intent into a substrate the consumer holds (Nix), and that
substrate is itself slated for eventual replacement, spend the beauty
budget on the durable layer and let unavoidable operational ugliness —
constants, derived names, glue — live in the throwaway substrate.
Prefer a beautiful Horizon over beautiful Nix code: Horizon is meant to
be elegant and small, Nix is the bootstrap substrate that will be
replaced, so optimising the substrate's beauty at the durable layer's
expense is the wrong trade. The general rule: the layer with the longer
life gets the cleanliness investment; the layer being retired absorbs
the dirt.

**Supporting verbatim:** "I would way rather make the horizon code more
beautiful and keep some of this dirty stuff like port numbers into the
Nixcode… That can stay in Nix." (record 9, Maximum); "it's not that
hard to put these constants in the Nixcode, that way we keep the
horizon more simple." (record 8).

**Preservation evidence:** Spirit `[horizon cluster-data]` and
`[criomos criomos-home nix lowering]` — `a2t4` covers WHAT-not-HOW and
input/output type reuse (the minimal-Horizon principle) and qkvx covers
typed-end-to-end, but neither states the beauty-budget tradeoff (which
layer absorbs ugliness). horizon-rs INTENT's three-test routes
non-authored values out of the proposal but does not say the
destination is chosen by which layer is throwaway. The
which-layer-gets-the-beauty framing is absent.

**At-risk rationale:** This is a sharp, reusable design tradeoff — a
decision rule for WHERE unavoidable ugliness goes when two layers have
different lifespans. It is adjacent to but distinct from the preserved
"constants stay in the consumer" rule; the distinct contribution is the
LIFESPAN-driven rationale (beauty to the durable layer). Lower priority
than candidates 1–3 — it is the most likely to be judged already-implied
by the minimal-Horizon principle, flagged here for the psyche to decide.

## Already preserved / dropped

Scanned all 29 records; 25 judged preserved or too-specific.

- **Booleans de-emphasized → vectors of named / data-carrying variants
  (records 1, 2, 12, 13).** Preserved: `skills/typed-records-over-flags.md`
  is the canonical home (boolean→typed-record, sum-with-data variants,
  the `online: bool` drop reasoning), and horizon-rs INTENT states
  "service roles are self-describing variants, not positional booleans."
  Spirit `qkvx` enforces typed-end-to-end NodeService. The general
  principle is solidly preserved; only the cluster-data-readability
  emphasis is weaker, not lost.
- **Minimal cluster data / constants stay in Nix / no type duplication
  input↔output (records 3, 7, 8, 10).** Preserved: Spirit `a2t4`
  (Horizon expresses WHAT not HOW; type-count minimal, reuse input type
  at output) and horizon-rs INTENT's proposal-boundary three-test
  (variability / authority / non-derivable). The eventual-minimal
  destination (node type + disk config) is the same direction at a
  specific snapshot — too specific.
- **Rewrite charter / lojix gets the triad, Horizon stays a projection
  hack (implicit context throughout).** Preserved: Spirit `tvbn`,
  `fe2j`, `9p8v`, `avvh`, `nhwv`, `munq`, `j9ba`.
- **Derived-predicate location, field order, NodePlacement rename
  Contained→Pod, wireguard key placement, fold-4-bools, drop online,
  builder-config collapse, IPv4-LAN-to-Nix-constants, merge into one
  `roles` field, three subsidiary role confirmations (records 11, 14,
  15, 16, 17, 19, 22, 24, 26, 27, 28, 29).** Dropped as too specific —
  these are concrete schema/field decisions already settled in
  horizon-rs code and INTENT; the specifics change and the general
  ideas behind them (typed-records, categorical-kind) are captured by
  the candidates above or by `typed-records-over-flags.md`.
- **Wireguard-IP-from-key brainstorm (records 18, 20).** The general
  key-derives-address pattern is folded into candidate 1 as supporting
  evidence; the Wireguard-specific deferred implementation is too
  specific to salvage on its own.

With the four candidates captured (psyche's choice), `horizon.nota` is
safe to delete: its durable core is either already in the guidance
layer / Spirit or surfaced above.
