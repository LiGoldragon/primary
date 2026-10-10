# Rust Code Analysis Tools for Agents — 2026-08-16

Provenance: Design session `e4be1c4a`. Field claims come from three
web-research subagents (influencer pass, general tooling pass,
Rust-specific pass) — subagent-returned evidence, not witnessed.
Probe results were witnessed live on this machine, 2026-08-16, on
our own checkouts. Psyche positions are quoted verbatim; everything
unmarked is Designer synthesis.

## Field context (condensed)

Five camps on how agents read code, mid-2026:

1. **Agentic grep** — Claude Code, Codex CLI, most open agents.
   No index; the model drives ripgrep iteratively. Anthropic removed
   embeddings May 2025 ("agentic search outperformed everything. By
   a lot." — Boris Cherny). Windsurf, Cline, Devin, Amp followed.
2. **Grep + trained embeddings** — Cursor only, at scale. Custom
   embedding model trained on agent traces; ~12.5% gain, mostly on
   1000+-file codebases. The only strong published counter-evidence.
3. **Deterministic code graphs** — Sourcegraph/Amp via SCIP.
   "Approximate retrieval… returns plausible-looking results that
   miss cross-cutting impact."
4. **Structural repo maps** — Aider: tree-sitter definitions +
   PageRank selection to a token budget. No embeddings, no LSP.
5. **Language-server inheritance** — JetBrains Junie, Zed ACP,
   Serena; agent consumes the IDE's semantic engine.

Undercurrent: **compiler feedback as the comprehension channel** —
an Apr 2026 paper found precise compiler remarks tripled agent
success ("the bottleneck is the interface, not the agent").
Armin Ronacher argues the complement: design code/languages for
agent-local reasoning instead of recovering comprehension by tooling.

Psyche positions (verbatim, this session):
- "I dont think mcp is very relevant. it forces everything into
  json which is not agent friendly."
- "the standard is still cli's"

Retained from the MCP ecosystem regardless of transport: the
converged capability vocabulary — find symbol, find references,
outline, rename, diagnostics, docs lookup — as a demand signal for
what comprehension queries agents reach for.

## The query catalog and the three engines

Every comprehension question decomposes onto one of three engines:

| Layer | Engine | Sees |
|---|---|---|
| Authored shape | ast-grep (tree-sitter) | source text before macro expansion |
| Declarations | rustdoc JSON (raw or trustfall) | what exists after expansion: types, traits, impls incl. derive/blanket/auto, signatures, bounds |
| Usage | SCIP index (`rust-analyzer scip`) / rust-analyzer | every reference/call site |

| Question | Engine |
|---|---|
| Inherent impls (impl blocks without a trait) | shape |
| Free functions | shape |
| Types carrying a derive | shape (post-expansion a derive is indistinguishable from a hand-written impl) |
| All implementations of a trait | declarations |
| All traits of a type (incl. blanket/auto) | declarations |
| Impls overriding a default method vs inheriting | declarations |
| Types implementing both A and B; signature/bound queries | declarations (trustfall) |
| Who calls X; all uses of type T | usage |
| Trait methods never called | declarations ⋈ usage |
| unsafe blocks, unwrap calls, macro invocations | shape |
| Module structure / internal dependencies | cargo-modules |
| External dependency queries | cargo tree |

Grep is structurally unable to answer the declaration- and
usage-layer questions: blanket impls and derives mean the answer is
not written in the source anywhere.

## Probe results (witnessed 2026-08-16)

Subjects: `protos` (25 .rs files, ~3.9k LoC, zero external deps,
compiles clean) and `spirit` (61 files, ~24.9k LoC — does NOT
currently compile: unresolved import `dotos_text_query` at
`src/store/mod.rs:24`).

### Working today, zero setup

**ast-grep** (on PATH):
- Inherent impls: `ast-grep --pattern 'impl $T { $$$ }' --lang rust`
  — instant; matches ONLY inherent impls; `impl $TRAIT for $T { $$$ }`
  is a disjoint shape. Real answer: `protos/src` has zero inherent
  impls; all found were in the architecture-guards binary and tests.
- Free functions: needs a YAML rule; `protos/src` has zero (guards
  holding), 32 in the guards binary incl. `main`:

```yaml
id: free-functions
language: rust
rule:
  kind: function_item
  not:
    inside:
      stopBy: end
      any:
        - kind: impl_item
        - kind: trait_item
```

- Derive users: `kind: attribute_item` + `regex: "derive.*Debug"` —
  16 types in protos/src, all also Clone/Eq/PartialEq.

**cargo-modules**: `nix run nixpkgs#cargo-modules -- structure --lib
--package protos` (~3s incl. first fetch). Prints the module tree
with visibility, traits first — the closest existing output to the
trait-first comprehension surface. `dependencies` subcommand emits
Graphviz DOT.

**rust-analyzer batch** (on PATH): `rust-analyzer diagnostics .`
5.5s, clean on protos. `rust-analyzer scip .` 2.9s → `index.scip`
704 KiB. Explicit invocation only — consistent with the standing
ruling against rust-analyzer running automatically.

**cargo tree** (built-in): instant. protos: zero external deps.
`cargo tree -i thiserror` on spirit shows 6+ internal crates pulling
it.

**cargo clippy / cargo check `--message-format=json`**: works; one
self-contained JSON object per diagnostic; this surfaced spirit's
broken import. protos is clippy-clean.

### Blocked on this machine

- **rustdoc JSON**: needs nightly rustc; system has stable 1.96,
  no rustup. `cargo rustdoc -- -Z unstable-options --output-format
  json` → "the option `Z` is only accepted on the nightly compiler".
  Unlock: bring nightly in via nix (fenix or oxalica rust-overlay) —
  a nix-workflow decision. docs.rs pre-builds rustdoc JSON for
  published crates, not for our git-sourced ones.
- **cargo-public-api**: hard-requires rustup (shells out to
  `rustup run nightly rustdoc`); unusable on nix-only Rust even with
  a nix nightly present. Querying rustdoc JSON directly avoids it.
- **SCIP reader**: rust-analyzer emits the index but nixpkgs ships
  no reader; the protobuf is inert without a small query tool
  (build one, or obtain Sourcegraph's scip CLI outside nixpkgs).

### Gotchas an agent will trip on

1. `sg` on PATH is setgroups, not ast-grep — invoke `ast-grep`.
2. ast-grep YAML needs exact tree-sitter node kinds (`trait_item`,
   `attribute_item`; `trait` and `meta_item` are invalid) and the
   errors don't suggest correct names.
3. `not: inside:` without `stopBy: end` silently under-matches
   (walks up one level only) — a correctness bug, not an error.
4. cargo-modules requires `--package` inside a workspace.
5. `cargo clippy` silently does nothing when clippy is absent from
   the sysroot — no error, just no lints.
6. rust-analyzer diagnostics interleaves a progress bar on stdout.

## Worked example: query cost without an index

"All traits of `Block`, and every trait's implementors" for protos
was assembled by a subagent grepping — minutes of fan-out reads.
Against rustdoc JSON it is one query on one artifact. Result, for
the record: Block implements `Headed`, `BlockRendering` (private),
`Textualize` plus derives `Clone, Debug, Eq, PartialEq`; protos/src
defines 30 traits of which 24 have exactly one implementor;
`StructuralWalk` alone implements five private single-method
traits. Design implications were taken up with the psyche
separately; this report records the tool evidence only.

## Open forks (unruled)

1. **Default consumption route** for Rust intelligence: batch CLIs
   only / explicitly-invoked session LSP / `ra_ap_*` linked into an
   own component (unstable 0.0.N API).
2. **Toolbelt vs component**: third-party CLIs agents shell to, vs
   an own Signal-speaking comprehension component (the schema-
   explanation vision points at the component as terminal shape;
   the fork is what, if anything, precedes Ethos).
3. **Trait-surface extractor**: nothing ships the trait-and-main-
   types anatomy; a thin extractor over rustdoc JSON could print
   exactly it. Gated on nightly-via-nix.
4. **Nightly toolchain into the nix setup** (unlocks the whole
   declarations layer): yes/no/how.

## Sources

- `reports/RustCodeAnalysisTools-2026-08-16.md`, canonical legacy report
  source migrated by flow 01a02a06.
- Flow `e4be1c4a`, which records the research provenance and live probes
  summarized in this report.
