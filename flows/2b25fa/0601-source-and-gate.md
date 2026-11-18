# Flow 0.60.1: hnc2 source and gate request

## Immutable source
- Repository/worktree: `/git/worktrees/flow-reminder-7b5174`, branch `reminder-link-7b5174`.
- Published commit: `cda44973b69ba36d0765cfd64be80c19abef4098`; parent `ec4eb9356e9441aec58bee94810d7e67014cbf0b`; worktree clean after push.
- Reservation 417 remains held for the same permaflow; successor 2b25fa adoption explicitly confirmed by Opus epvq and Core zg23. Packet reservation 422.

## Anatomy and source review
- `crates/flow-nexus/ethos/send_tool.ethos`: internal SendKind adds Done.RequestId. Generated `src/generated/send_tool.rs` changes by exactly that variant; no public wire, Memory, Cargo or flake change.
- `src/send_tool.rs`: tool declaration and parser admit Result and Done with request. BecomesRequest/BecomesMessage now produce public SendableRequest/SendableMessage. The actual handler calls the existing `resolve_sendable_message` before answer_route, including the kept-answer branch. The resolver supplies the original logical id, validates open/delivered binding and distinguishes Result for Order/Question from Done for Task. The old empty logical-id construction is gone.
- `src/store/logical_delivery.rs`: ordinary Done admission uses the binding instead of requiring a reminder. The existing atomic closure commit retracts the reminder only when present, as the tool path already does. This preserves Done after Silence and keeps closure/reminder removal atomic.
- Inherited lock-order review: ordinary admission explicitly drops `_handover_guard` and `_guard` before withdrawing reminder Notices; tool admission drops `_guard` before doing so. Silence calls close_reminder to completion, then withdraws Notices under the dispatch gate; close_reminder retains no store write gate across that return. No additional lock-order change was needed. This is static review, not concurrency execution proof.
- `crates/flow/src/hook.rs`: replaces the complex fixture tuple with named ProcessRow fields; no lint allowance or production behavior change.

## Fixtures and evidence boundaries
- `tests/unit/queue_operations.rs`: actual JSON/parser/handler Result-to-Task refusal and ordinary parity for addressed, Unbound, Flow and Unknown origins; correct tool Done closes those Tasks and removes schedules. Silence then Done runs both ordinary and tool paths for those origins, verifies Open then Answered, no schedule, replay stability, and second-answer refusal. A separate handler fixture covers undelivered/unknown/closed requests, Done-to-Order refusal, and the routed Result original logical identity.
- `tests/unit/send_tool.rs`: declaration conditional now names Result and Done; parser fixtures cover Done with id, missing id and wrong id type.
- These fixtures are UNRUN. Baseline regression expectations are source-derived, not observed failing tests: ec4eb935 incorrectly accepts tool Result/Task, parses Done as malformed, and refuses ordinary addressed Done after Silence. No baseline compilation or candidate test pass is claimed.
- Formatting and `git diff --check` passed. No build, cargo test, clippy or Nix gate has run in this flow.
- Generation used existing `/nix/store/i3q64y2k95qkkgxa4khyxa6lzk6s24pb-rust_ethos-zero-29.0.0-bin/bin/ethos-zero`. Its derivation source `/nix/store/pf0hfh43ihyfdll14v3sf4l6m67ggcja-ethos-zero-29.0.0/src` compares byte-for-byte equal to cached git source f23eacf338a90ce4a6dea011554724fa6488fcc9 src. Generated output contains exactly the new variant; nothing generated was edited by hand.

## Requested gate and resource-control decision
One whole per-crate Nix gate, no separate cargo compilation, against the published immutable commit above. The gate evaluates and builds remotely and downloads no result. Candidate command, NOT STARTED and NOT a complete resource harness:

```sh
nix run github:Mic92/nix-fast-build -- --remote prometheus \
  --no-nom --no-download --eval-workers 1 \
  --flake 'github:LiGoldragon/flow?rev=cda44973b69ba36d0765cfd64be80c19abef4098#checks.x86_64-linux'
```

Core zg23 reports no verified daemon-contained capped harness. A client-unit MemoryMax does not contain Nix-daemon builds. Therefore this packet requests either an accepted exact daemon-contained resource envelope or an explicit Psyche exception before Core grants the slot. The required floor is 24 GiB; available memory, safe limit, aggregate overlapping build allocation and mechanism are not verified here. The command above alone supplies no such guarantee. No heavy job may start on its authority.

On grant, send exact revision, invocation, enforced scope/limits and process/log locations directly to Core and Field at start. Wait for terminal exit as an event. Send terminal status, process-ended and scratch-cleanup receipts directly to both. Freeze source throughout. Green checks are required before main landing/Field handoff; Field owns switches. Source is ready for review, not gated or released.

## Following work
Opus epvq orders the named meta overrides after 0.60.1: inspect `flows/1e2133/proposals/overrides-2.md` and build the missing ones, preserving existing CloseRequest. Earlier 5f30 queues the Living Reading-field contract release; epvq supplies the newer next-work order. Neither lane has been edited here. Do not reopen historical carried requests without current direction.
