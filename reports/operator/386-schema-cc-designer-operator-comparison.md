# Schema-CC Designer / Operator Comparison

## Verdict

Designer's `schema-next` branch `next/schema-cc-integration` is the better immediate main-merge candidate for the schema-cc slice.

My `structural-forms-integration` work is useful, but it is a wider integration line: it bundles schema-cc with positional schema syntax, TypeReference structural-form work, downstream lock propagation, Spirit Nix vendor patch fixes, and the agent triad positional migration. That proves the larger structural-forms stack can build, but it is not the cleanest branch to merge for "schema-cc generates schema-next dispatch" alone.

## Actual Branch State

Designer branch:

- `schema-next` `next/schema-cc-integration` at `1a93aad7`.
- Based on `schema-next` main `f00a467a`.
- Two reviewable commits: co-locate schema-cc, then generate the parenthesis-reference dispatch.
- Diff from main is narrow: `schema-cc/`, `build.rs`, `schemas/reference-grammar.nota`, `src/reference_resolver_generated.rs`, and the TypeReference dispatch hook.

Operator branch:

- `schema-next` `structural-forms-integration` at `23299642`.
- Includes schema-cc plus the positional/structural-forms cascade.
- Diff from main touches roughly 66 files: schema syntax, fixtures, source codec, declarative lowering, TypeReference, schema-cc, and tests.
- Downstream stack was propagated through `schema-rust-next`, `signal-spirit`, `meta-signal-spirit`, `spirit`, and the agent triad because Spirit's Nix gate vendors those repos.

## Implementation Difference

Designer's branch uses a committed generated resolver:

- `build.rs` decodes `schemas/reference-grammar.nota`.
- It emits `src/reference_resolver_generated.rs`.
- The build checks the committed file for byte freshness.
- Regeneration is explicit with `SCHEMA_NEXT_UPDATE_RESOLVER=1 cargo build`.
- Reviewers can read the generated dispatch directly.

My branch emits to `OUT_DIR`:

- `build.rs` decodes the same grammar and writes `OUT_DIR/reference_resolver.rs`.
- `src/schema.rs` includes the generated module through `concat!(env!("OUT_DIR"), ...)`.
- This compiles and tests, but it makes the generated compiler code less visible and lacks the freshness-gated committed artifact pattern already used by `schema-rust-next`.

For a compiler-compiler slice, Designer's committed-generated-file pattern is better: data source, generated artifact, and freshness witness are all inspectable.

## Consumer Claim Difference

Designer's claim is narrow: schema-cc is byte-transparent to consumers on current main. They tested `spirit`, `signal-spirit`, and `meta-signal-spirit` by patching schema-next and proving generated `src/schema/*.rs` artifacts stayed byte-identical.

My claim is broader: the full structural-forms integration branch and its downstream lock stack passed Cargo and Nix, including Spirit's full `nix flake check --max-jobs 0`. That is real evidence, but it proves a different thing: the combined structural-forms stack is coherent. It does not make my schema-next branch the best schema-cc-only main merge.

## What To Do

Use Designer's branch for the schema-cc main landing:

1. Operator merges `schema-next` `next/schema-cc-integration` to `schema-next` main.
2. Run `schema-next` full gate, especially `nix flake check`.
3. Optionally rerun the byte-transparent consumer witness against `signal-spirit`, `meta-signal-spirit`, and `spirit` main.
4. Do not propagate consumer lock changes for this slice unless the final gate proves they are necessary.

Then reconcile the structural-forms line:

- Rebase or port `structural-forms-integration` on top of schema-next main after the schema-cc branch lands.
- Drop the duplicate `OUT_DIR` resolver strategy in favor of Designer's committed freshness-gated resolver.
- Keep the downstream fixes from my work where they still apply: Spirit's Nix vendor patcher branch assumptions and the agent triad positional/schema-toolchain migrations are valuable for the larger structural-forms stack, not for the schema-cc-only landing.

## Correction To My Prior Framing

My report `385` is accurate as a record of what I implemented and tested, but its "ready for main-merge review" framing is too broad if read as "this is the schema-cc-only main candidate." It is merge-ready evidence for the larger structural-forms branch family. For the narrower schema-cc dispatch datafication, Designer's `next/schema-cc-integration` is cleaner, more reviewable, and closer to the actual main merge path.
