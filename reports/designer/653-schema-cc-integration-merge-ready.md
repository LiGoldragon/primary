# 653 — schema-cc → schema-next → spirit: merge-ready integration

The psyche directed: *"get it ready to go on main … put schema-cc with schema, and
integrate it in spirit too, as if you would submit it for merge in main, so fully
tested."* This is the result: schema-cc now generates schema-next's live
parenthesis-reference dispatch, wired in and proven transparent through spirit, to a
merge-ready bar. Design + leans: report `652`. Operator review of the prototype: `384`.
Intent: `vpbx` (schema-cc), `549v` (precedence as data), `v0n6`, `9rjq`.

## What landed

**One unit, on schema-next `next/schema-cc-integration` (off main `f00a467a`), two
reviewable commits:**

1. **Co-locate** (`aa13b4bf`) — schema-next becomes a cargo workspace; **schema-cc is
   a member crate** (`schema-cc/`), per the psyche's "put schema-cc with schema" and
   the "related crates in one repo" rule. The standalone schema-cc repo is superseded
   (see cleanup).
2. **Integrate** (`1a93aad7`) — schema-cc **generates schema-next's real parenthesis
   resolver** from the canonical grammar declared as data
   (`schemas/reference-grammar.nota`); a `build.rs` emits it into a committed,
   freshness-gated `src/reference_resolver_generated.rs` (the schema-rust-next pattern);
   `from_block_with_registry` calls the generated `resolve_parenthesis_reference`; the
   hand-written `from_parenthesis_objects` match is **retired**. The per-built-in
   construction stays in schema-next as five uniform `resolve_*` methods — schema-cc
   owns the *precedence* (data), schema-next owns the per-arm *semantics*.

```
schemas/reference-grammar.nota  (the precedence, as data)
   │  build.rs: schema-cc decode → validate → emit
   ▼
src/reference_resolver_generated.rs  (committed, freshness-gated)
   │  include! + call
   ▼
TypeReference::resolve_parenthesis_reference → resolve_vector/optional/scope_of/map/bytes
                                             → reserved-head guard (from the grammar's built-in set)
                                             → from_macro_or_application (registry → application)
```

## The merge-ready bar — fully tested

**schema-next itself** (verified on my own re-run):
- **171/171 tests green**, `identity.rs` **8/8** — blake3 hash-stability is the
  byte-equivalence witness: the generated dispatch behaves *identically* to the retired
  hand-written match. schema-cc **20/20**. `clippy --workspace -D warnings` clean.
- The freshness gate fails loudly on drift (`SCHEMA_NEXT_UPDATE_RESOLVER=1` to
  regenerate) and the **nix sandboxed build passes** (`.nota` added to the schema
  filter so the grammar vendors).

**spirit + both contracts** (A/B verification, baseline vs schema-cc-patched, all on
`main` — which pin `schema-next=main`, the same base):

| Repo | Build (baseline → patched) | Tests | Generated `src/schema/*.rs` |
|---|---|---|---|
| spirit | green → green (`--no-default-features` + `nota-text`) | green | **byte-identical** (sha256) |
| signal-spirit | green → green | 8/8 | **byte-identical** |
| meta-signal-spirit | green → green | 3/3 | **byte-identical** |

Every patched regen produced **zero artifact drift** — the freshness gate passed
without rewrite (itself a byte-equality proof), sha256 sums matched baseline→patched,
`jj diff --stat src/schema/` empty. The only working-copy change per repo was the
3-line `[patch]` + the Cargo.lock relock. **No schema-cc-attributable divergence; no
regression.** The cargo `[patch]` to the workspace root resolved cleanly (no
nested-workspace conflict). The `primary-opzy` stale-`agent` issue is a
structural-forms-line artifact and did **not** manifest on spirit `main` (clean
baseline).

**Conclusion: the change is byte-transparent to the whole spirit stack — merge-safe.**

## How to merge (operator)

Per the workspace discipline, the code-repo main merge is operator's. The unit is one
schema-next feature branch:
- **schema-next:** merge `next/schema-cc-integration` (the co-locate + integrate
  commits) to main. The consumers need **no change** — they regenerate byte-identical
  artifacts against the new schema-next, so nothing downstream must move in lockstep.
- **Final gate:** `nix flake check` on schema-next (the sandboxed build already passes;
  run the full check before landing).
- This is independent of the positional-syntax epic (the `structural-forms-integration`
  line, report `648`) — different schema-next concern, different base; operator
  sequences both onto main.

## Cleanup + the open roadmap

- **Standalone schema-cc repo superseded.** `/git/github.com/LiGoldragon/schema-cc`
  (and the `repos/schema-cc` symlink) are now redundant — schema-cc lives inside
  schema-next. Remove them after the merge (the co-located copy is the canonical, and
  carries the operator-`384` hardening + the real dispatch emission; the standalone v0
  is fully subsumed).
- **Further datafication** (report `652` roadmap, each a verified slice): the built-in
  head table as the single source for `ReferenceHead::classify`; the shape vocabulary;
  the emission rules; eventually the meta-schema fixpoint (schema-cc's own types as a
  schema). This first slice datafies the built-in dispatch *precedence*; the
  macro/application tail stays schema-next's `from_macro_or_application` for now.
