# 365 — Engagement with operator/203: schema-next interface implementation

*Operator's `/203` documents the concrete double-implementation baseline landing across all three new repos. This is the first IMPLEMENTATION-status report after the vision-arc; engagement is concrete + assessment-shaped rather than critique-shaped. Several `/361 §12` aspirational items become empirically demonstrated; new emergent questions surface.*

## §1 Frame — what /203 reports

Three operator-owned repositories landed with substantive code on main:

| Repo | Commit | What it carries |
|---|---|---|
| `nota-next` | `0f21138d` | Structural reader: Document + Block + Atom + AtomClassification + SourceSpan + position tracking |
| `schema-next` | `2558aaf5` | Schema engine + Asschema (Vec-canonical) + position-aware SchemaMacro trait + MVP lowering |
| `schema-rust-next` | `a290b7c7` | RustEmitter producing newtypes/structs/enums + root-surface enums + short-header constants |

The chain works end-to-end on an MVP fixture: NOTA source → nota-next Document → schema-next SchemaEngine + position-aware macros → ordered Asschema → schema-rust-next Rust source → compiled fixture. Operator names it explicitly: *"This is not full schema self-hosting yet, but it proves the intended interface chain is real."*

## §2 What's now empirically demonstrated (was aspirational in /361)

`/361 §12` table updates from this landing:

| Element | Before /203 | After /203 |
|---|---|---|
| Header derivation from Asschema | 🔵 ASPIRATIONAL | ⚪ PARTIAL — surface-index + variant-index encoding lands; deeper 64-bit namespace plan still pending |
| Composer emits Rust over Asschema (no signal_channel!) | 🔵 ASPIRATIONAL | ✅ DEMONSTRATED — `schema-rust-next/src/lib.rs` emits + `nix flake check`'s `no-old-signal-macro` enforces |
| Nix-enforced grep-prohibitions | (named in /199 design; not in /361 status table) | ✅ DEMONSTRATED — four constraints implemented as derivations |
| First emit-from-schema fixture (Spirit-shape) | 🔵 ASPIRATIONAL | ✅ DEMONSTRATED — Input/Output enum + short-header constants emitted + compiled |

The most-impactful resolution: **the chain operator promised in /199's Phase 4-5 is real**. Source → emitted fixture → compiled-and-used. Three-way verification (string-compare + compile + use) per /195's methodology landing across repos.

## §3 What I notice in the interfaces

### §3.1 The Nix-enforced grep-prohibitions — concrete enforcement

From `schema-next/flake.nix`:

```nix
no-btree-canonical = pkgs.runCommand "schema-next-no-btree-canonical" { } ''
  if grep -R "BTreeMap" ${src}/src ${src}/tests; then
    echo "BTreeMap must not be canonical assembled-schema storage" >&2
    exit 1
  fi
  touch $out
'';
no-authored-features = pkgs.runCommand "schema-next-no-authored-features" { } ''
  if grep -R "EffectTable\|FanOutTargets\|StorageDescriptor\|Features" ${src}; then
    echo "retracted authored schema features are forbidden" >&2
    exit 1
  fi
  touch $out
'';
```

From `schema-rust-next/flake.nix`:

```nix
no-old-signal-macro = pkgs.runCommand "schema-rust-next-no-old-signal-macro" { } ''
  if grep -R "signal_channel!" ${src}; then
    echo "schema-rust-next must not use the old signal_channel macro" >&2
    exit 1
  fi
  touch $out
'';
no-rust-macro-surface = pkgs.runCommand "schema-rust-next-no-rust-macro-surface" { } ''
  if grep -R "macro_rules!\|proc_macro" ${src}/src; then
    echo "Rust emission must stay separate from Rust macros in src/" >&2
    exit 1
  fi
  touch $out
'';
```

This is the **discipline-as-derivation** pattern from /199 §"Required Nix and constraint tests" landing concretely. The retracted-drift cluster (records 730-732) is now structurally impossible to reintroduce — a contributor can't sneak `EffectTable` back into `schema-next` without `nix flake check` failing.

**The `no-rust-macro-surface` check is the load-bearing piece** of the user's "emission separate from rust macros" intent (record 819): `schema-rust-next/src/` can EMIT Rust source code as data but cannot DEFINE Rust macros. Emission and macros are different layers; the check enforces it.

### §3.2 The short-header encoding — Layer 4 lands concretely

From schema-rust-next's emitted fixture:

```rust
pub mod short_header {
    pub const INPUT_RECORD: u64 = 0x0000000000000000;
    pub const INPUT_OBSERVE: u64 = 0x0001000000000000;
    pub const OUTPUT_RECORD_ACCEPTED: u64 = 0x0100000000000000;
    pub const OUTPUT_RECORDS_OBSERVED: u64 = 0x0101000000000000;
}
```

The /199 Layer 4 / /361 §7 header-derivation is no longer aspirational. The encoding reads:
- Top byte (`0x00` / `0x01`) = surface namespace (Input / Output)
- Second byte (`0x00` / `0x01`) = variant order within the surface
- Lower bytes (0) = reserved for nested variant paths

This is a **wider slot allocation** than record 763 strictly required (8-bit root enum / 256 variants). Operator went 16-bit per slot for headroom. Per record 764's seven-data-carrying-root-variants ceiling, plenty of room remains for compile-time enforcement.

### §3.3 The MVP schema shape matches the root-struct model

From /203:

```nota
{}
[
  (Input (Record Entry) (Observe Query))
  (Output (RecordAccepted RecordIdentifier) (RecordsObserved RecordSet))
]
{
  Topic [Text]
  Entry [Topics Kind Description Magnitude]
  Kind (Decision Principle Correction Clarification Constraint)
}
```

Read against /361 §5's three-section root struct:
- Field 1: `{}` — empty imports/exports namespace ✓
- Field 2: `[ (Input ...) (Output ...) ]` — input/output struct with TWO enum sub-fields ✓
- Field 3: `{ Topic ... Entry ... Kind ... }` — namespace map ✓

Operator's interpretation realizes /361 §5 faithfully. The "input/output struct" from the design becomes a literal struct (the `[]` field) containing two enum-declared sub-fields (Input + Output). The carry-uncertainty Q1 (record 806 imports-first ordering) is reflected — imports first, even when empty.

### §3.4 Two-level test methodology applied per /195/355

From /203 schema-rust-next tests:
- "emit Rust source from a schema and compare exactly to a checked-in fixture"
- "compile and use the checked-in fixture as Rust code"

Two-layer verification. Not the three-layer (string-compare + compile + behavioral-run-against-real-NOTA) full version from /195/355 §6, but the structural enforcement is intact. The third layer would land when wire reader/writer emission gets added (/203's "next implementation slice").

## §4 What I'd flag

### §4.1 The `no-btree-canonical` check is stricter than the discipline

The discipline (record 805 + /199 §"Asschema properties"): *"BTreeMap must not be canonical assembled-schema storage."*

The check: `grep -R "BTreeMap" ${src}/src ${src}/tests` — fails on ANY `BTreeMap` mention.

Legitimate use case: a `count_by_kind` method returning `BTreeMap<&'static str, usize>` as a DERIVED-index lookup (the designer parallel uses exactly this at `design-nota-from-schema/crates/emit/src/lib.rs:482`). Such a use is not canonical storage; it's a method return.

Operator's check would flag the legitimate derived-index use as a violation. Two options:
- **(a) Accept the stricter cut**: BTreeMap is banned everywhere; if you need a sorted map for a derived method, build it ad-hoc or use a wrapper. Simple rule, easy to enforce.
- **(b) Relax the check**: grep for usage in struct/field declarations only (canonical storage shape), allow methods to return BTreeMap for derived indexes.

(a) is defensible (BTreeMap-as-smell could justify the wider ban). (b) is more principled (matches the underlying discipline exactly). Worth psyche input on which cut to pin. Not blocking; just an enforcement-vs-discipline alignment question.

### §4.2 The `no-authored-features` check is broader than retraction

The check greps for `EffectTable | FanOutTargets | StorageDescriptor | Features` anywhere in `${src}`. That's the full retracted-drift cluster from records 730-732. Strict enforcement is right.

BUT — the word "Features" alone (case-sensitive grep) would flag legitimate-mention contexts like documentation that REFERENCES the retraction (e.g., a comment saying *"we removed the Features section per /350"*). That would be a false positive.

Looking at the check more carefully: it's `grep -R "...|Features"` — case-sensitive. So lowercase "features" (as in a comment about "the features section") wouldn't trip. Capital-F "Features" would. Plausible enough but worth being explicit: the grep is structural-token-shape, not concept-mention.

Carry as a small observation; not a bug.

### §4.3 schema-rust-next consumes schema-next by git dependency on main

From /203 §"Known limits": *"schema-rust-next consumes schema-next by Git dependency on main; as the stack matures, forge/content-addressed generated crates may replace that dependency pattern."*

This is the inter-repo Cargo coupling I noted in `/364 §3.5`. Operator acknowledges + names the future path (forge content-addressing per record 822). For the current MVP it's fine. **Carry-forward signal**: when designer parallel's `nota-emitted` lands, it will be ANOTHER consumer of operator's `nota-next` (via the design repo's Cargo). Eventually four-repo coupling. The forge content-addressing direction would dissolve that.

### §4.4 The MVP schema's empty imports + missing namespace section

The MVP `spirit-min.schema` has `{}` for imports (empty map) and a populated namespace map. Both sections present, even when one is empty. Per /361 §5 / record 805's optionality framing: *"Optionality applies to which sub-fields appear inside the input/output struct, not to which sections exist."*

So the schema-shape is: section presence is structural; section content is optional. Operator's MVP is structurally consistent with the design.

Open question carrying forward: at the wire encoding level, do empty sections cost bytes (a zero-length list marker in the encoded form) or are they free? /364 §3 didn't raise this; /203 doesn't address; designer parallel might surface it.

## §5 What's still aspirational

Per operator's own §"Known limits" + /361 §12:

- Third-party macro registration (Q15 still open)
- rkyv impls on emitted types (named in /199 Layer 5; not yet emitted)
- NOTA reader/writer impls on emitted types (next slice)
- Version-projection traits for upgrade/downgrade (Layer 6 — entire layer queued)
- Full signal client/server code generation
- The deeper 64-bit header namespace plan (current is simple 16-bit-per-slot)
- Designer parallel's `nota-emitted` feasibility (separate verdict from `a4793f8b`)

These are the next slices. The chain WORKS for the MVP; the next layer expands it.

## §6 Convergence with designer parallel still in flight

Operator's track and the designer parallel (`a4793f8b`, design-nota-from-schema) converge on:

- Block API with span + delimiter predicates + qualifies_as discipline
- Vec-canonical Asschema-shape
- Position-aware macro `lower(object, position, ctx)` signature
- Structured Error enums with named variants
- Three-section root struct (`{}` + `[]` + `{}`)
- Compiled-fixture test methodology

They diverge on:

- Operator's recursion floor is `nota-next` (hand-authored structural reader)
- Designer parallel's recursion floor is `crates/kernel` (explicit markers; smaller; goal is to emit MORE from `nota.schema`)
- Operator emits to a sibling crate (`schema-rust-next`)
- Designer parallel emits to itself (`crates/nota-emitted`)

The convergence is STRUCTURAL (both arrive at the same data shapes); the divergence is on the EMISSION TARGET (which is the recursion-floor experiment). Verdict pending designer parallel's completion.

## §7 What this means for /361's status table

`/361 §12` empirical-vs-aspirational table needs these updates after /203:

| Element | New status | Evidence |
|---|---|---|
| Composer emits Rust over Asschema | ✅ DEMONSTRATED | `schema-rust-next/src/lib.rs` + `nix flake check` green |
| Header derivation | ⚪ PARTIAL | Simple 16-bit-per-slot encoding lands; deeper plan pending |
| Nix-enforced grep-prohibitions | ✅ DEMONSTRATED | Four checks across schema-next + schema-rust-next |
| End-to-end NOTA → Rust emission chain | ✅ DEMONSTRATED | MVP fixture compiled + used |

I won't amend /361 until the designer parallel verdict lands — both updates can ship together as the synthesis-after-comparison artifact.

## §8 References

- `/203` — operator's schema-next interface implementation (subject of this engagement)
- `/199` — six-layer architecture (/203 lands Layer 1 + 2 + 5 partially)
- `/361` — latest vision (the empirical-vs-aspirational table this report updates)
- `/362` — critique of /200 (the macro position correction /203 has structurally absorbed)
- `/364` — mid-flight code inspection (the BTreeMap-import observation that /203's check would also flag)
- Spirit records 730-732 (retracted-drift cluster /203 Nix-enforces against), 763-764 (root-enum + 7-data-carrying-variant ceiling), 805-807 (root-struct + macro interface), 819-822 (repo strategy /203 implements)
- Operator commits: `nota-next@0f21138d`, `schema-next@2558aaf5`, `schema-rust-next@a290b7c7`
