# Designer 652 schema-cc Review

## Findings

### P1: The generator does not yet honor `ReferenceGrammar` as the ordered precedence source

The report's core claim is that `ReferenceGrammar` makes reference dispatch
precedence declared data. The code only does that for the relative order of
`Builtin` arms. The marker forms are discarded and reintroduced as a hard-coded
tail.

Evidence:

- `src/grammar.rs:10` says the list order is dispatch precedence, and
  `src/grammar.rs:20` says the grammar body decodes an ordered stream of forms.
- `src/generate.rs:46` filters the grammar down to built-ins only:
  `filter_map(BuiltinFormEmit::from_form)`. `DeclaredMacro` and `Application`
  positions are ignored.
- `src/generate.rs:94` emits every built-in arm, then `src/generate.rs:95` emits
  one reserved-head guard, then `src/generate.rs:96` always emits
  `DeclaredMacro`, and `src/generate.rs:99` always emits `Application`.
- `src/validate.rs:49` only checks `Application` ordering if an `Application`
  marker is present. `tests/validate.rs:65` explicitly says a grammar without a
  catch-all still validates.

Impact: a validated grammar can be generated into a resolver with behavior not
present in the grammar. For example, `(ReferenceGrammar (Builtin Vector 1)
DeclaredMacro)` validates, but the generated resolver still returns
`Resolution::Application` for all non-built-in, non-macro heads. A grammar that
places `DeclaredMacro` before a built-in also validates, but generation still
moves every built-in before the registry hook.

That reintroduces the hidden precedence this repo exists to remove. The
prototype proves "declared built-in order generates built-in arms"; it does not
yet prove "reference precedence is generated from data."

Recommended fix: choose one of two strict shapes before rewiring `schema-next`.
If the canonical precedence is fixed as built-ins, then declared macro, then
application, make validation enforce that exact grammar shape: all built-ins
first, exactly one `DeclaredMacro`, exactly one `Application`, application last.
If the grammar is meant to be a truly ordered value, generate every
`ReferenceForm` in order and only emit `DeclaredMacro` / `Application` arms when
those forms appear.

### P2: The emitted resolver shape cannot yet be the real schema-next integration surface

The emitted module declares `pub struct ReferenceResolver;` at
`src/generate.rs:79`, then puts the registry hook on a private associated
function at `src/generate.rs:104`. That is acceptable as a token prototype, but
it is not the eventual integration shape: a declared-macro check needs registry
state or a context receiver, and the workspace Rust discipline rejects ZST
method holders when runtime behavior lives behind them.

Designer does mark this as a v0 stub in report 652, lines 189-192. The review
point is narrower: do not treat the current emitted resolver as the code shape
to wire into `schema-next`. The next slice should generate a data-bearing
resolver/context adapter, or generate methods onto schema-next's existing
context type, so the registry lookup has an owned place to live.

### P3: New canonical repo hygiene is incomplete

`schema-cc` has `INTENT.md` and `ARCHITECTURE.md`, which is the important part,
but it does not yet have the standard repo agent surfaces:

- no `AGENTS.md`
- no `CLAUDE.md` shim
- no `skills.md`

That is not a blocker for the prototype, but it should be fixed before treating
the repo as a normal shared code surface. The workspace contract expects agents
entering a repo to read `INTENT.md`, then `AGENTS.md`, `skills.md`, and
`ARCHITECTURE.md`.

## Verified

- `/git/github.com/LiGoldragon/schema-cc` is on local bookmark `next/schema-cc`
  at change `79ad0fc3` with the ReferenceGrammar prototype.
- `cargo test` passes: 15 tests.
- `cargo clippy --all-targets -- -D warnings` passes.
- No remote is configured for the repo. This matches Designer's handoff: remote
  creation was deliberately left to the psyche/operator.

## Verdict

The direction is good and worth keeping: a NOTA-decoded grammar generating Rust
is the right compiler-compiler brick. But the headline claim is too strong.
Right now the data drives only the built-in arm order; the real precedence tail
is still hard-coded Rust. Fix that before schema-next consumes the generated
resolver.
