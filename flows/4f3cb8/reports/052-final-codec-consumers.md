# 052 final codec consumer supplement

This supplements the frozen56-file packet and the exact recovery appendix; it does not change frozen originals. Core approved direct typed StartRefusal construction and the explicit five-budget store-check adapter. No source bodies are authorized by this document.

## Startup error output: typed construction, no decoder

Pinned flow-ethos `StoreRefusal { path: Path, reason: Reason }` uses String aliases; StartRefusal::Store carries it. Replace main.rs356–370's textual construction and parse round-trip with:

```rust
fn start_store_refusal_datom(path: &str, reason: &str) -> String {
    flow_ethos::StartRefusal::Store(flow_ethos::StoreRefusal {
        path: path.to_owned(),
        reason: reason.to_owned(),
    })
    .datomize(vec![])
    .protosize()
    .compact()
}
```

This remains the existing ConfigurationStartup trait capability; the snippet is its intended method body, not a new free-function owner. No Budget, Potential or decoder is involved. `report_unrecognized_store` main.rs373–377 prints this typed output; remove its now-impossible parse-error branch. Callers at main.rs102–106 and121–125 keep their store refusal meaning and existing exit behavior. This does not turn an admission failure into success or change StoreRefusal wire shape. The output-only chain retains its existing traits.

Tests independently decode the output with explicit FIXTURE budgets and compare exact typed StoreRefusal including quotes, guillemets, braces, newline and Unicode in path/reason. No production decoder budget is required simply to emit an error. Existing duplicate startup-generated refusal declarations are not merged in this pass; use exactly the existing flow_ethos type imported by this output consumer.

## Store-check: explicit adapter, unchanged checking request

Shared owner of BootstrapTextBudget and its five leaves remains flow-ethos, as approved for other adapters. Add this declaration to the existing Flow startup vocabulary, retaining StoreCheckRequest unchanged:

```ethos
Library
[ :flow_ethos:BootstrapTextBudget ]        ; one shared five-limit type
[ StoreCheckInvocation.{                  ; new adapter argument, not persisted data
     BootstrapTextBudget
     StoreCheckRequest } ]
[]                                       ; traits
[]                                       ; associations
```

The actual surrounding startup file retains its existing root/sections and imports; this block shows only the additional declaration/import, not a second competing file.

The Datom, illustrative values only:

```datom
{ { 65536 256 4096 65536 1024 }
  { /home/li/.local/state/flow/flow.sema } }
```

`flow-store-check` takes ONE such argument. Its existing `ReadsStoreCheckRequest` boundary first uses the approved borrowed fixed-prefix scanner to obtain all five limits, budget-decodes the SAME entire StoreCheckInvocation, validates arity/trailing input, then yields `invocation.store_check_request`. Request.check() and result types remain unchanged. No filesystem inspection/open/check effect happens before complete typed decode. Structural nodes/depth, forming depth and composition steps/depth are all explicit; no fallback and no reinterpretation of this utility as an ordinary/meta socket peer. It has no frame setting because no length-prefixed transport is used here.

### Actual producers and package consumers

- `crates/flow-nexus/src/bin/flow-store-check.rs:15–29` replaces its Budget literals and argument help with the new one-argument form; main.rs-equivalent local main32–42 still calls request.check() and prints structural output.
- Existing startup Ethos/generated module adds StoreCheckInvocation; existing StoreCheckRequest{StorePath} and direct Rust test constructors stay unchanged.
- **Actual CLI producers** are `capsule/flow-capsule.clj:1751` and1983–1984. Both invoke packaged flow-store-check with ONE existing StoreCheckRequest datum `{ «store» }`. Core approved preserving that external interface through a Nix-configured wrapper, with no new capsule schema.
- Nix installs the exact compiled raw executable at a fixed package libexec path and emits `bin/flow-store-check` as its configured wrapper. One explicit Nix five-budget declaration supplies the rendered prefix; it is neither a Rust nor Clojure default. The wrapper requires EXACTLY one argument, retains that argument's bytes, and forwards ONE envelope-text argument `{ configured-five-budget request-datum }` to the exact packaged raw path. It never parses/evaluates the request, searches PATH, reads an environment fallback, adds implicit args or executes user content. Shell expansion is quoted; full raw typed decoding validates malformed shape/arity before any check effect.
- Both capsule producers retain their existing one-request argument and package selection, now exercising the actual configured wrapper. No capsule global/environment/config-schema extension is introduced. The direct Cargo-built Rust binary takes StoreCheckInvocation; the packaged wrapper takes StoreCheckRequest. Tests and usage text must name that distinction instead of silently accepting both forms in one parser.
- `flake.nix:310–311,318–319` registers direct store_check tests, not CLI producers. Preserve those registrations; add CLI-envelope fixtures and the two actual capsule producer executions to acceptance.
- `store_check.rs:136–140` directly constructs StoreCheckRequest and tests142+ call check(); these do not gain artificial codec settings. They remain direct typed tests.

### Tests

Missing/zero/negative/overflow/invalid five-limit prefix, wrong arity/trailing data and independent stage exhaustion refuse before request.check() or filesystem effects. A valid envelope projects exactly the old typed StoreCheckRequest and preserves Opens/Absent/Refused outcomes. Both real capsule call sites exercise the wrapper supplying configured values without fallback. Test the ACTUAL rendered wrapper, package/libexec selection and reply parsing, preserving whitespace/comments and request bytes; malformed input, missing/extra argv and shell metacharacters cannot trigger shell execution. No test merely compares illustrative snippets.

## ReaderBudget — approved checked construction and exact projection

Core approved private i64 runtime counters. This supersedes the frozen proposal's public usize-field sketch while preserving its exact two-field order and configured stage meanings. Each stored field is one fact; no duplicated usize/i64 mirrors.

The Rust API delta (trait capabilities, not inherent/free-function machinery):

```rust
pub struct ReaderBudget {
    remaining: i64,
    maximum_depth: i64,
}

pub enum ReaderBudgetField { Remaining, MaximumDepth }
pub enum ReaderBudgetConstructionReason {
    Negative,
    OutsideNativeWidth,
    OutsideIntegerWidth,
}
pub struct ReaderBudgetConstructionError {
    pub field: ReaderBudgetField,
    pub reason: ReaderBudgetConstructionReason,
}

pub trait BuildsReaderBudget: Sized {
    fn from_integer_limits(remaining: i64, maximum_depth: i64)
        -> Result<Self, ReaderBudgetConstructionError>;
    fn from_native_limits(remaining: usize, maximum_depth: usize)
        -> Result<Self, ReaderBudgetConstructionError>;
}
pub trait ReadsReaderBudget {
    fn remaining(&self) -> i64;
    fn maximum_depth(&self) -> i64;
    fn permits_depth(&self, depth: usize) -> bool;
}
```

Integer construction checks both nonnegative values and `usize::try_from` representability before creating the private record. Native construction checks each `i64::try_from`, then delegates to the SAME checked integer constructor. Each error identifies the field and cause; it need not carry an unrepresentable scalar through an incompatible error codec. No `as`, unchecked factory, mutable reference or public counter setter bypasses construction. Zero is VALID runtime exhaustion; initial bootstrap/runtime POLICY validation separately requires positive supplied limits.

Keep the existing Protos `Spendable` trait signature. Its ReaderBudget implementation checks zero and returns its EXISTING exhaustion result; otherwise decrements remaining by exactly one. This mutation is bounded, cannot underflow, and preserves representability. `permits_depth` checks conversion of candidate usize depth to i64; overflow is false, otherwise compares against the retained maximum with the existing inclusive/exclusive depth semantics. Read-only access returns the exact i64 values. No caller can mutate counters directly. The Reader uses the configured maximum, replacing its hidden256.

Datomizable emits the ordered STRUCT `{ remaining maximum_depth }` from the exact i64 accessor results. No narrowing, panic, default or arbitrary-instance precondition. Composing requires exactly TWO positions, decodes both as existing Integer, then invokes the central checked constructor. Construction failure maps to the existing typed composition error vocabulary at the offending position, preserving field/cause; no scalar legacy form is accepted by supplying a default depth. Fixture decoding explicitly tests that old scalar/wrong-arity input refuses.

All current public-field/literal consumers change together. Exact production anchors: Protos core83–103 (record/Spendable),248–254/288–293 (Reader ownership/use/depth),550–583 (removed unbounded conveniences, retained explicit bounded callers); protos.ethos17/kinds.ethos6,18/generatedkinds31/lib8. Datom composition564–581 (old scalar projection),core27/464,datom-codec.ethos9,20; flow client/meta/composer/hook/start/storecheck parser factories use the checked constructor from their explicit five-limit values. Retained structural output `protosize` does not acquire a decoder.

Fixture updates are finite and source-pinned in `reader-budget-changedtype-ledger.md` and raw query under `/home/li/primary/flows/2aed8d/reports/`, including previously missed flow-ethos/tests/waking15 and Protos Spendable fixture caller tests/kinds11–20. Every Budget/ReaderBudget fixture literal switches to explicit checked construction; zero-exhausted fixtures remain valid. Derived Composing signatures are unchanged, so datom-codec-derive0.32.0 remains retained.

Tests: zero remaining construction/spend exhaustion; one node then zero; unchanged maximum after consumption; negative integer inputs; platform maximum shared-representable value; usize>i64::MAX rejection on targets that permit such usize; i64 outside usize rejection on narrower targets; both fields independently checked; depth boundary and unrepresentable candidate; ordered two-field roundtrip with large representable values; no mutable/public construction escape in every affected consumer. Compile/source graph and runtime tests after body clearance establish the implementation, not the proposal alone.

## Final supplemental gate

This document, the approved StopPoll supplement and exact recovery/changed-type consumer appendices are separately hashed additions to the immutable56-file packet. Fresh independent review checks each exact production receiver/producer and all construction/mutation callers against these definitions, rechecks artifact drift and current custody, and reports PASS or precise remaining gaps. No old report is relabeled a fresh check. Core Secondary alone grants one writer after that gate; no source bodies, publish, capsule or Adopt claim follows from this supplement.
