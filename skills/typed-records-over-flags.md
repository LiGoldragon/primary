# Skill — typed records over flags

*Any time the system asks a yes/no question of a noun, ask whether the
"yes" carries data. If it does, the question wants to be a typed record,
not a boolean. Booleans that hide data are a recurring drift pattern;
this skill names it.*

---

## What this skill is for

Apply this skill when designing schema for projected state (a `Node`, a
`Cluster`, a `User`), wire records, or projected derivations. The rule
is small but the cumulative effect is large — most of the typed-cluster
migration in this workspace consists of applying it once per concept.

The rule:

> **Boolean-on-a-noun is a code smell when the "yes" branch carries
> data.** Replace `field: bool` with `field: Option<Record>`. The data
> the "yes" carries is the record's payload. Readers migrate from
> `if node.field` to `if let Some(record) = &node.field`.

The same rule generalises to enums: a unit-variant enum whose variants
carry meaning beyond the variant name is asking to become an enum with
data, or a struct of `Option<T>`s.

---

## Why this matters

A boolean field is a question with a hidden answer. `is_nix_cache: bool`
asks "is this node a Nix cache?" but the answer is yes-or-no on a
question that's not yes-or-no. If yes, the consumer needs to know:

- what URL does it serve at?
- what signing key does it use?
- what retention policy governs it?
- what trust level?

In a boolean world, every consumer reinvents that lookup with its own
ad-hoc derivation: "if `is_nix_cache`, the URL is
`format!(\"http://{node.domain}\")`; the signing key is at
`/var/lib/nix-serve/nix-secret-key`; …" The derivation rules diverge,
the magic strings multiply, and the type system stops catching errors.
A node that *should* be a cache but lacks a signing key fails to type-
check nowhere — it deploys and fails at runtime.

When the boolean becomes `binary_cache: Option<BinaryCache>` (and
`BinaryCache` carries `endpoint`, `signing_key`, `retention_policy`),
every property the cache carries is in the type and every consumer
reads it the same way. Adding a property is one struct field; removing
a property breaks every consumer that read it. The type **is** the
contract.

---

## The pattern, concretely

### Before — flag soup

```rust
pub struct Node {
    pub name: NodeName,
    pub is_nix_cache: bool,
    pub is_remote_nix_builder: bool,
    pub is_dispatcher: bool,
    pub nordvpn: bool,
    pub wifi_cert: bool,
    pub behaves_as: BehavesAs {  // grouped, but still flag soup
        pub virtual_machine: bool,
        pub bare_metal: bool,
        // ...
    },
    pub criome_domain_name: CriomeDomainName,  // assumes a TLD
    pub nix_url: Option<String>,                // derived, assumes scheme
    pub nix_pub_key: Option<NixPubKey>,         // separate from is_nix_cache
}
```

Symptoms:

- The `is_*` fields and the supporting fields (`nix_url`,
  `nix_pub_key`) drift apart. A node can be `is_nix_cache: true` with
  `nix_url: None` — illegal but type-checks.
- Every consumer that uses the booleans must also know the magic-
  string derivations.
- Booleans that aren't really independent get bundled into
  `behaves_as`-style records but each remains a yes/no question.

### After — typed records

```rust
pub struct Node {
    pub name: NodeName,
    pub placement: NodePlacement,           // was behaves_as.virtual_machine etc.
    pub capabilities: NodeCapabilities {
        pub build_host: Option<BuildHost>,        // was is_remote_nix_builder
        pub binary_cache: Option<BinaryCache>,    // was is_nix_cache + supporting
        pub container_host: Option<ContainerHost>,// was implicit
        pub public_endpoint: Option<PublicEndpoint>, // was implicit
    },
    pub services: NodeServices {
        pub tailnet: Option<TailnetMembership>,   // was tailnet: bool gated on name
        pub tailnet_controller: Option<TailnetControllerRole>,
    },
    // raw derivations stay where they belong
}

pub struct BinaryCache {
    pub endpoint: BinaryCacheEndpoint,    // scheme, host, port, public_key
    pub signing_key: SecretReference,     // logical name; backend in cluster
    pub retention_policy: CacheRetentionPolicy,
}
```

Each "yes" now names what the yes means. Consumers migrate:

```rust
// Before:
if node.is_nix_cache {
    // ... reconstruct endpoint from node.criome_domain_name, …
}

// After:
if let Some(cache) = &node.capabilities.binary_cache {
    // cache.endpoint, cache.signing_key, cache.retention_policy are right there.
}
```

If the cache record is incomplete, the *proposal* fails validation —
not the deploy.

---

## The three forms

The pattern has three concrete shapes; pick whichever fits.

### Form 1 — `Option<Record>` on a single noun

```rust
pub struct Node {
    pub binary_cache: Option<BinaryCache>,
}
```

Use when a node either is or isn't this thing; if it is, the record
carries the configuration. `is_nix_cache` → `binary_cache:
Option<BinaryCache>`. The capability sub-record is the default home.

### Form 2 — sum enum with data variants

```rust
pub enum WifiAuthentication {
    Wpa3Sae { password: SecretReference },
    EapTls { profile: CertificateProfileId },
    MigrationWindow { primary: Box<Self>, fallback: Box<Self>, until: TimestampNanos },
}
```

Use when the noun is in *one* of several mutually-exclusive states,
each carrying its own data. A boolean `eap_tls: bool` paired with a
boolean `wpa3_sae: bool` is wrong: the values are mutually exclusive,
and each carries different configuration. Sum-with-data names the
exclusion and the per-variant payload.

### Form 3 — typed record replacing a multi-flag struct

```rust
// Before
pub struct BehavesAs {
    pub virtual_machine: bool,
    pub bare_metal: bool,
    pub iso: bool,
    // ...
}

// After
pub enum NodePlacement {
    Metal(MetalPlacement),
    Contained(ContainedPlacement),
    // Iso joins as a variant once it's modelled honestly.
}
```

Use when several booleans are obviously a single closed-set choice
wearing a struct disguise. The `behaves_as.{virtual_machine,
bare_metal, iso}` triplet is one enum with three variants. The triplet
form was equivalent to the enum form except that `(true, true, false)`
was illegal but type-checked. The enum form makes the illegal state
unrepresentable.

---

## What to keep on boolean shape

Not every boolean wants to be a typed record. The rule is:
**booleans whose "yes" branch carries no payload data are fine.**

Examples that stay booleans:

- `online: bool` — yes-or-no with no payload. Either the node is up or
  it isn't.
- `wants_printing: bool` — operator opt-in for the printer bundle.
  Payload is the bundle, which lives in the module that gates on this
  flag.
- `is_fully_trusted: bool` — derived from `trust` magnitude; pure
  yes/no.

The diagnostic: if a `bool` field's value would let you derive the
payload trivially (`if x { default() }`), it can stay. If the payload
requires authored data (endpoints, keys, policies, references), the
boolean is hiding a record.

---

## Migration shape

When converting a flag to a typed record:

1. **Add the typed record alongside the boolean.** Both fields exist
   for a transition cycle.
2. **Derive the typed record from existing inputs in projection.** New
   proposals can author the record directly; old proposals get a
   shimmed default. The boolean continues to derive from the same
   inputs as before.
3. **Migrate consumers** one at a time. Each consumer that read the
   boolean is changed to match on the typed record. The boolean's
   derivation can change to `node.capabilities.binary_cache.is_some()`
   once readers have migrated.
4. **Delete the boolean.** Once no consumer reads it, the field
   retires. The original flag-bundle struct shrinks; eventually it
   disappears.

This is the shape report 04 §1.3 names ("compat-shimmed flags survive
one cycle"). Apply it whenever flag-soup migrates to typed records.

---

## Witnessed examples in the workspace

| Before | After | Repo / context |
|---|---|---|
| `is_nix_cache: bool` | `binary_cache: Option<BinaryCache>` | horizon-rs `capability.rs` (in progress) |
| `is_remote_nix_builder: bool` | `build_host: Option<BuildHost>` | same |
| `machine.species = Pod` (with `super_node`) | `placement: NodePlacement::Contained{...}` | same |
| `tailnet: bool` (gated on node name) | `services.tailnet: Option<TailnetMembership>` | horizon-rs `proposal.rs::NodeServices` |
| `wifi_cert: bool` (separate from cert reference) | `WifiAuthentication::EapTls{profile}` | Wi-Fi PKI migration design |
| `MachineSpecies::Pod` (no payload) | `ContainedPlacement` (substrate, host, …) | dedicated-cloud-host placement design |

The cumulative effect of these migrations is the recurring narrative
arc of this workspace: **typed records replace name overloading and
flag soup.** Every one of the above involved (1) a noun that hides
implicit data, (2) a downstream consumer that re-derived the data
from magic strings, and (3) a type-checking gap that the new record
closed.

---

## Related skills

- `skills/abstractions.md` — verb belongs to noun. The corollary:
  "if the verb's noun has no payload, the verb is a method, not an
  actor." Same diagnostic applied to actor surfaces (see also
  `skills/actor-systems.md` §"Zero-sized actors are not actors").
- `skills/contract-repo.md` — typed records on the wire. The same
  discipline applied to wire-bearing types.
- `skills/architectural-truth-tests.md` — once a typed record exists,
  consumers can fail-loud on illegal combinations the previous flag
  soup admitted.
- `skills/naming.md` — typed records make naming honest; flag soup
  obscures it.

---

## See also

- The week's CriomOS commits ("Use Horizon roles instead of node-name
  gates", "Replace tailnet booleans with NodeServices") are concrete
  applications.
