# F1 — Flow contract branches merged to main

Subflow of 38de5b, 2026-09-25. Clones in the subflow scratchpad; Orchestrate
lock 6342 on both clone paths, released. No prior lock on either repo's paths.

## signal-flow

- Before: origin/main 968ae3b (1.1.0).
- `flow/system-prompt-bundle-00f95a` tip ab70332 had main as ancestor; merged by
  fast-forward (no merge commit, no history rewritten).
- ab70332 failed its own test with `--features datom`:
  `every_ordinary_request_has_a_concrete_datom` — Start fixture lacked the new
  `SystemPromptBundleFile` field (Arity expected 13, found 12). Fixed the fixture
  only: commit 0d4ed64 "Carry system-prompt bundle file in Start datom fixture".
- After: origin/main 0d4ed64, version 2.2.0.
- `cargo test --features datom`: 5 passed, 0 failed (contract.rs), lib 0.
- `git branch -r --contains ab70332`: origin/main, origin/flow/system-prompt-bundle-00f95a.

## meta-signal-flow

- Before: origin/main aa61040 (1.1.0).
- Branch tip a34bc65 fast-forwarded onto main; pins signal-flow ab70332.
- After: origin/main a34bc65, version 4.1.0.
- `cargo test --features datom`: 3 passed, 0 failed (contract.rs), lib 0.
- `git branch -r --contains a34bc65`: origin/main, origin/flow/system-prompt-bundle-00f95a.

## Ethos regeneration

Freshness is enforced by build.rs (asserts `ethos/signal.ethos` generates exactly
`src/generated/signal.rs`); build passed in both, so no regeneration was needed.

## Versioning rule applied

"Update the version surface changed by public behavior, wire, storage, package,
or deployment changes." The fast-forward adds no change of its own; each branch
commit carries its own bump, so main reaches 2.2.0 and 4.1.0. The fixture fix is
test-only and takes no bump.

Open: ab70332 changed the wire (a required field added to LaunchProfile) without
a bump over 7ba21d0 (also 2.2.0); a34bc65 repinned that change keeping 4.1.0 over
85a5d40. Two wire shapes share each version label. No post-hoc bump was made,
since Flow 0.7.0 pins ab70332 exactly and a later bump would not be what it pins.

Plain `cargo test` (no features) fails to compile the contract tests in both
repos (datom_codec/protos are optional); tests need `--features datom`.

Flow repo Cargo.toml pins untouched.
