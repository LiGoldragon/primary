# Nexus semantic-text vocabulary

> A genuinely healthy two-repo cluster: nexus is a real 3-actor kameo translator daemon and nexus-cli is a clean 87-LOC byte-shuttle, both with zero true free functions and zero hand-assembled NOTA. The one shared liability is dead schema cruft — both carry a stale `.concept.schema` (Parse/Render/Evaluate v0.1) that no code implements or references and that predates the entire terse-form grammar — plus nexus pinning nota-next 8 commits behind HEAD (but safely below the d8862b6 encoding bump).

## Cluster: Nexus semantic-text vocabulary

**Verdict.** A healthy two-repo cluster. `nexus` is a real 3-actor kameo translator daemon; `nexus-cli` is a clean 87-LOC byte-shuttle. Both pass the two hard scans cleanly: zero true module-level free functions (only `fn main`) and zero hand-assembled NOTA (`nexus` uses the real nota-next codec; `nexus-cli` touches no NOTA at all). The one liability they share is dead schema cruft, and `nexus` carries a modestly stale nota-next pin.

| Repo | Prod LOC | Test LOC | Gen LOC | Role | Daemon shape | Intent fit | Dep status | Schema | FreeFn | FakeNota |
|---|---|---|---|---|---|---|---|---|---|---|
| nexus | 912 | 290 | 0 | Vocabulary + NOTA<->Signal translator daemon | real-kameo-daemon (3 actors) | mixed | signal/signal-derive at HEAD; nota-next 8 behind (no d8862b6) | stale `.concept.schema`, 0 terse-form | 0 | 0 |
| nexus-cli | 87 | 0 | 0 | Thin stateless text shuttle (binary `nexus`) | thin-CLI | aligned | N/A — no git deps (thiserror only) | stale `.concept.schema`, 0 terse-form | 0 | 0 |

LOC verified: `nexus` has no inline `#[cfg(test)]` modules in `src/` (all 290 test lines live in `tests/`), so prod = 912 (src + src/bin), matching the baseline exactly. `nexus-cli` is 87 prod / 0 test, confirmed.

### nexus — real daemon, stale schema, compatibility-era parser

The supervision tree is real and matches the lib doc: `Daemon` (root, `src/daemon.rs`) spawns `Listener` (`src/listener.rs`, UDS accept loop, re-arms via an `AcceptConnection` self-tell) which spawns one `Connection` per client (`src/connection.rs`, reads to EOF, parses, forwards, renders, stops). `CriomeLink` (`src/criome_link.rs`) is a plain post-handshake signal client struct (4-byte length prefix + rkyv `Frame`), not an actor — so the actor count is **3**. Two extra debug bins (`src/bin/parse.rs`, `src/bin/render.rs`) expose the parser/renderer without the daemon.

The parser is honest about its state: `src/parser.rs:1-15` describes itself as a pre-renovation compatibility adapter that only accepts `Assert -> Node/Edge/Graph` while signal moves to the multi-root contract. It consumes the **real** nota-next codec — `Document::parse`, `NotaBlock::expect_delimited`, `NotaDecode::from_nota_block` — no hand-rolled paren parsing.

The schema is dead cruft. `schema/nexus.concept.schema` is the OLD single `.concept.schema` form, frozen at `(Version 0 1)(Status Concept)`, declaring `Parse`/`Render`/`Evaluate` roots and `Expression`/`Text`/`Identifier` types. No code implements that vocabulary (the parser dispatches `Assert`->`Node`/`Edge`/`Graph`), and `rg` finds zero references to the file in `src`, `Cargo.toml`, `flake.nix`, or any `include_str!`. Zero terse-form adoption (no 52ro self-tag, no yp29 `Bytes` leaf, no qz6j, no lm84) — moot, since the file is not the live source of truth for anything. The recommendation is deletion or a rewrite to the real six-root + Node/Edge/Graph vocabulary.

Dependencies: `signal` (`c4fbbfa`) and `signal-derive` (`5d6c80c`) are both at HEAD. `nota-next` is pinned `f0e435a`, **8 commits behind** HEAD `d8862b6`, and sits *below* `ae5c25c` — i.e. on a pre-numeric-codec / pre-bare-safe-string nota-next. It does **not** pin `d8862b6`, so there is **no encoding-bump exposure**. `flake.lock` pins no foundation crates (only toolchain/nixpkgs); the build is crane-driven from `Cargo.lock`, so there is no Cargo.lock-vs-flake.lock disagreement to report. The crate does not depend on schema-next/schema-rust-next/sema at all.

### nexus-cli — clean reference client

`src/client.rs` is a single `Client` struct over a std `UnixStream`; `Client::shuttle` (a real method on a data-bearing type) connects, writes, half-closes for EOF, reads the reply. `fn main` (`src/main.rs`) reads args/stdin and calls it. No actors, no async, no NOTA construction or parsing — by design (its INTENT says the CLI shuttles bytes; parsing is the daemon's job). Only foundation-free dependency is `thiserror`, so it cannot go stale and has no `d8862b6` exposure.

It shares the dead-schema problem: `schema/nexus-cli.concept.schema` declares a `Parse`/`Render` vocabulary with `Input`/`Expression`/`Text` — which directly contradicts the crate's own INTENT (it does *not* parse). Frozen at `(Version 0 1)(Status Concept)`, referenced nowhere. A byte-shuttle has no NOTA vocabulary to declare; the file should be deleted. The diagnostics-rendering substrate its INTENT promises (surface `(Diagnostic ...)` replies and machine-applicable suggestions for an LLM front-end) is also unimplemented — today it prints raw reply bytes.

### Free-function findings

No true module-level free functions in either repo — the only column-0 `fn`s are `fn main` (allowed). One soft architectural finding in `nexus`:

- `nexus` `src/renderer.rs:82-208` — `Renderer` carries ~15 associated methods (`render_node`:155, `render_edge`:159, `render_graph`:168, `render_diagnostic`:90, `render_ok`:82, `render_into`:59, `render_outcome`:75, `render_records`:99, the three `render_*_bindings`, the three `render_*_binding`, `local_error_code`:196) that take no `&self` and never read `self.output`. They are pure `signal-type -> String` transforms. This is **not** a hard free-fn violation (Renderer is a real data-bearing type owning `output: String`), but the conversion logic for `Node`/`Edge`/`Graph`/`Diagnostic` would more honestly live as `NotaEncode`/`From` impls on the signal types rather than bucketed statically on the renderer, and the head tags are passed as bare string literals that can drift from the schema. Severity: low; deliberate per the renderer's own doc comment that signal Reply types are wire-only.

### Fake-NOTA findings

None in either repo. `nexus` emits via nota-next's own `Delimiter::Parenthesis.wrap([...])` assembler (a legitimate nota-next API at `nota-next/src/parser.rs:289`) and delegates every field value through `.to_nota()`; there is no `format!("(")`, `push_str("(")`, or `write!(...,"(")` hand-assembly, and parsing goes through `Document::parse`/`NotaBlock`. `nexus-cli` performs no NOTA construction or parsing at all. The only stylistic note (already captured above as a low free-fn finding) is that record head tags in the renderer are bare string literals rather than a derived codec — a drift risk, not cheating.
