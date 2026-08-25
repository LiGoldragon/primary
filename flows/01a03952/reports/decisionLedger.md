# Ethos source-placement repair

## Result

The groundless Nexus and Sema Ethos sources and generated modules are gone from both Orchestrate wire repositories. Ethos Monolith now generates a wire consumer from `signal.ethos` alone. The wire contracts and bytes are unchanged, and Orchestrate's live Nexus passes against the two updated wire releases.

## Decisions

1. **[Psyche ruling] Nexus and Sema Ethos are not designed.** No source, schema, scaffold, placeholder, or generated projection for either kind stands in a wire repository. When those interfaces are designed, their Ethos sources live in the Nexus's main repository.

2. **[Implementation] A wire consumer has one generation contract.** Ethos Monolith 0.4.0 replaces `ComponentGeneration` and `GeneratedComponent` with `SignalGeneration` and `GeneratedSignal`. It reads one `signal.ethos` and emits one `signal.rs`; no compatibility path preserves the three-source API.

3. **[Implementation] Every signal source declares its Channel.** `Channel` is unconditionally required. The empty-Interface allowance and generic non-signal projection path that existed to feed the former three-source generator are removed.

4. **[Implementation] Wire repositories own only their wire vocabulary.** `signal-orchestrate` and `meta-signal-orchestrate` delete `ethos/nexus.ethos`, `ethos/sema.ethos`, `src/generated/nexus.rs`, and `src/generated/sema.rs`. Their generated module trees export only `signal`.

5. **[Implementation] Cargo generation remains a freshness gate.** Each wire `build.rs` invokes `SignalGeneration` on `ethos/signal.ethos` into `$OUT_DIR/ethos-generated/signal.rs`, then byte-compares that output with committed `src/generated/signal.rs`. It never writes the source tree.

6. **[Wire] Contract identities and encoded bytes do not change.** Ordinary Orchestrate remains ContractId 1 / WireRevision 4; Meta Orchestrate remains ContractId 2 / WireRevision 3. Fixed pre-change Register, Release, and Configure frames are asserted by the landed tests.

7. **[Version] The generator receives the breaking release; wire consumers receive patches.** Ethos Monolith advances 0.3.0 to 0.4.0 because its public generation API is replaced. With wire shape and bytes unchanged, `signal-orchestrate` advances 0.16.1 to 0.16.2 and `meta-signal-orchestrate` advances 0.10.1 to 0.10.2.

8. **[Integration] The producer lands before its consumers.** Both wire repositories pin the immutable Ethos Monolith 0.4.0 revision `b273030ee68f71184e3c9ae2e24f474d954555ce`.

9. **[Integration] Orchestrate is a proof-only consumer in this repair.** A disposable copy of Orchestrate 0.22.0 at `09c19ce2af53328748a73dd2d7b5c4288bc33d98` changed only `Cargo.toml` and `Cargo.lock` to resolve the two new wire revisions. The authoritative checkout was not changed or pushed.

10. **[Coordination] Failed edit reservation is recorded, not disguised.** The deployed Orchestrate client still speaks the retired interface and the new daemon socket was unavailable. Repository ownership stayed disjoint across subflows; no reservation was claimed.

## Releases

- `ethos-monolith` 0.4.0 — `b273030ee68f`
- `signal-orchestrate` 0.16.2 — `88cc01ec0d78`
- `meta-signal-orchestrate` 0.10.2 — `2b3ec7c4c4a5`

All three revisions are on their repositories' pushed `main` refs.

## Proof

- Ethos Monolith's focused generation/interface/architecture tests passed 15/15. Its current-platform `nix flake check -L --no-write-lock-file` passed all 11 checks on the configured remote builder.
- `cargo build --locked`, full tests, denied-warning Clippy, formatting, flake evaluation, and the remote generated-contract Nix check passed in each wire repository. Each build ran the signal-only source freshness comparison.
- The new fixed-byte tests were seen failing before their fixtures were accepted, then passed for ordinary Register and Release and meta Configure.
- From the disposable Orchestrate copy, `nix build --no-link --no-write-lock-file --max-jobs 0 --option fallback false .#checks.x86_64-linux.live-nexus` exited 0. Nix built the new Git dependencies and `orchestrate-test-0.22.0.drv` on `ssh-ng://nix-ssh@prometheus.goldragon.criome`; local fallback was disabled.
- The disposable copy and tracking pointer were removed. The authoritative Orchestrate checkout remained clean at the supplied base.

## Unresolved

- No Nexus or Sema Ethos document kind has been designed. This repair settles ownership and removes false sources; it does not design either interface.
- The living has not ruled whether a refused or unavailable edit reservation forbids editing. The strict rule in the edit-coordination proposal remains a proposal.
- The ordinary socket has no authoritative `SKILL_VARIABLES.md` value, and the deployed wrapper still targets the retired interface.
- Orchestrate itself still pins the preceding wire revisions because it was explicitly proof-only here. A later consumer release may advance those pins.

## Sources

- `flows/f426777b/vision/ethosSourceFiles.md`
- `flows/012fbf07/vision/threeStacks.md`
- `flows/01a02fd5/vision/interfaces.md`
- `flows/01a03603/reports/decisionLedger.md`
- `flows/01a03952/vision/orchestrateInPath.md`
- `/git/github.com/LiGoldragon/ethos-monolith` at `b273030ee68f71184e3c9ae2e24f474d954555ce`
- `/git/github.com/LiGoldragon/signal-orchestrate` at `88cc01ec0d785f4b279e58968d2f9b0a8139797c`
- `/git/github.com/LiGoldragon/meta-signal-orchestrate` at `2b3ec7c4c4a5111342104ffe2ffb5f8b84800656`
- Disposable Orchestrate 0.22.0 live-Nexus witness from base `09c19ce2af53328748a73dd2d7b5c4288bc33d98`
