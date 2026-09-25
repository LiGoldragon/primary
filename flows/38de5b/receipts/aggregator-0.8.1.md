# Receipt: aggregator 0.8.1 bounds a received frame's nesting before decoding

The aggregator main branch moved from f7db587 (0.8.0) to cc3ec4f (0.8.1). After the push, `git ls-remote origin main` returned cc3ec4f.

- Work clone: scratchpad `agg-0.8.1-38de5b-opus3`. It was held under Orchestrate lock 6499, which has been released.
- This closes the gap named in `aggregator-recursion.md`. Before this change, rkyv validation of a received frame recursed without bound, before the projection's budget ever ran.

## Rule (stated in the commit and in ARCHITECTURE.md)

A received frame's nesting is bounded before the frame is decoded. The limits are the projection's own: depth 32 and 256 nodes.

1. **Validation ceiling.** `wire::ReceivedFrame` validates with rkyv `ArchiveValidator::with_max_depth`.
   - The ceiling is `MAXIMUM_FRAME_NESTING`: 32 plus `FRAME_ENVELOPE_NESTING` (16), so 48 nested pointers.
   - Validation therefore never recurses without bound.
   - A frame past the ceiling is refused as `FrameRefusal::Unvalidated`.
2. **Tree measurement.** Inside the ceiling, every `TextQuery` and `MatchEvidence` tree is measured while still archived.
   - The new trait `text_query::ArchivedTree` spends the existing `ProjectionBudget`. The exact bounds therefore live in one place.
   - A tree past either bound is refused as `FrameRefusal::TreeOutsideBound { request_identifier, fault: TooDeep | TooLarge }`. The refusal comes before `rkyv::deserialize`, so nothing is allocated.
3. **Where it applies.**
   - `SignalFrame::read` now goes through `ReceivedFrame` for every frame that is received:
     - ordinary and meta queries on the daemon;
     - responses in the client.
   - The bound is `Receivable`. It replaces `Signal<T>: Restorable<T>`.
4. **Reply on the ordinary socket.** When a frame is refused as `TreeOutsideBound`, the daemon replies `OperationRejected { SearchTranscriptBlocks, InvalidQuery }` with the request's own identifier. This is the same rejection the in-process projection gives.
   - A frame that fails validation still gets no reply, as before.
5. **Crate rule.** `unsafe_code = "forbid"` still holds. No custom `ArchiveContext` was written; the depth limit comes from rkyv's own validator.

## Tests: `cargo test` 120 passed before (at f7db587), 130 passed after

The new file `tests/received_frame.rs` holds 10 tests. Every leaf in them is a phrase of long, out-of-line words, so each leaf uses the most pointer nesting a leaf can.

| Frame | Case | Result |
|---|---|---|
| `Query` search frame | depth 32 | accepted, and round-trips equal |
| `Query` search frame | depth 33 | `TreeOutsideBound(TooDeep)` |
| `Query` search frame | 256 nodes | accepted |
| `Query` search frame | 257 nodes | `TreeOutsideBound(TooLarge)` |
| `Response` `TranscriptBlocksSearched` evidence frame | depth 32 | accepted |
| `Response` `TranscriptBlocksSearched` evidence frame | depth 33 | `TreeOutsideBound(TooDeep)` |
| `Response` `TranscriptBlocksSearched` evidence frame | 256 nodes | accepted |
| `Response` `TranscriptBlocksSearched` evidence frame | 257 nodes | `TreeOutsideBound(TooLarge)` |
| Query frame 20,000 deep, restored on a 256 KiB stack | | `Unvalidated`, and the stack holds |
| Depth-33 search frame sent through `OrdinarySocketService::handle_stream` over a socket pair | | typed `OperationRejected` with `InvalidQuery`, `SearchTranscriptBlocks` and the request identifier |

**Control (run once, not committed).** An unbounded `rkyv::access` of the same 20,000-deep frame, on the same 256 KiB stack, aborted with a stack overflow. This shows the small-stack test discriminates.

## Checks and version

- `cargo clippy --all-targets` reported 0 warnings. `cargo fmt --check` is clean. The toolchain was cargo 1.97.1, taken from the environment.
- The version went from 0.8.0 to 0.8.1, a patch:
  - no wire change;
  - no public type lost;
  - additions: `wire::{ReceivedFrame, FrameRefusal, BoundedFrame, Receivable, MAXIMUM_FRAME_NESTING, FRAME_ENVELOPE_NESTING}`, `text_query::ArchivedTree`, and `Error::FrameRefused`;
  - one behaviour change: a refused frame is answered, and an unvalidatable frame is refused, before it is decoded.

## Not done

- Nix was not run.
- The 16-pointer envelope allowance is sized by reading the contract's types. It was not derived mechanically.
  - Every existing socket round-trip test still passes under the 48 ceiling.
  - Only a search response has been proven to fit at depth 32 (the tests above). No other frame shape has been proven.

## Sources

- aggregator cc3ec4f: `src/wire.rs`, `src/text_query/archived.rs`, `src/daemon.rs`, `tests/received_frame.rs`
- rkyv 0.8.18 `src/validation/archive/validator.rs` (`with_max_depth`)
- scratchpad test logs `agg-081-before.txt` and `agg-081-after.txt`
