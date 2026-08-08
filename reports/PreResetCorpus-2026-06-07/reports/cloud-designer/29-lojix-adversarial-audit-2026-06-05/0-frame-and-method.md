# 29 — lojix new-stack adversarial audit — frame & method

cloud-designer lane, 2026-06-05. Psyche directive: "Do a deep audit and
adversarial network analysis of your work after you've refreshed on if there's
anything new that you might have to port, and audit the work you've done in
depth ... fix it if you find flaws. And extend the testing if you can."

Context: the new-stack triad (lojix + signal-lojix + meta-signal-lojix
triad-port) is now pushed to `main` (lojix `5c0ee76f`, signal-lojix
`ffe791e7`, meta-signal-lojix `90818f78`, the last a new repo). M1
(build+evaluate) is green: three real-`nix` smokes pass. This audit stress-tests
that work before building further.

## Canonical location

`/git/github.com/LiGoldragon/{lojix,signal-lojix,meta-signal-lojix}/triad-port`
(the pushed copies). The `~/wt/...` copies are now stale duplicates.

## The five audit dimensions (parallel finders, then verify, then synthesize)

1. **M1-changes correctness** — adversarially audit this session's edits:
   `build_attribute` override, `DeployAction` enum + methods,
   `target_attribute`, the `Eval`/`Build` early-termination, the smoke tests.
   Edge cases, wrong-attribute risks, the drv-vs-attribute build, the reply
   not carrying the store path, Home-deploy correctness.
2. **Wire / network adversarial analysis** — the two-socket daemon
   (`daemon.rs`), `LengthPrefixedCodec`, frame decode/encode, the
   ordinary-vs-owner **authority boundary** (can an ordinary client reach a
   meta Deploy? frame-confusion across sockets? is socket-mode the only
   gate?), malformed/oversized/truncated frames, partial reads, connection
   drops mid-exchange, the `execute()` non-reply fallback.
3. **Engine pipeline correctness** — the `DeployStage` trampoline, the
   `SignalArrived → Command* → Continue` re-entry, continuation budget,
   phase recording, rejection mapping, effect-failure mid-pipeline, the
   in-flight `active_deploy`/`active_operation` state and any
   re-entrancy/interleaving hazard (concurrent deploys; a second request
   arriving mid-deploy).
4. **Engine-port assessment (the refresh)** — schema-rust-next moved 0.1.13 →
   0.1.14+ (`tokenize engine trait emission`, runtime mail tokens; latest
   `7f59b39`); triad-runtime moved past the pinned `28d03c3` (`let
   multi-listener runtimes stop cleanly`, socket-path cleanup; latest
   `973e1d3`); schema-next stream lowering. Assess: does bumping change the
   generated engine-trait surface / break the hand-written `SchemaRuntime`?
   What do the streaming additions enable? Risk/benefit + a recommended
   port plan. This is "anything new to port."
5. **Rust-discipline + abstractions** — method-only/no-free-fn, typed values
   (no String-typification beyond schema aliases), no bool flag-soup,
   schema-emitted-types-are-the-nouns, typed per-crate `Error` enum. Any
   violations introduced or latent.

Then **6 adversarial verification** — a skeptic re-reads the actual files,
tries to REFUTE each claimed flaw, confirms the real ones with file:line
evidence, drops the unsupported ones. Then **7 synthesis** — the prioritized
verified-flaw list (blocks-correctness vs cleanup), the recommended fixes, and
the port decision.

After the workflow: I (main agent) fix the confirmed flaws, extend the tests,
rebuild green, and push to main.

Constraint to finders: read-only, no `cargo`/`jj` (fixes happen after); write
one numbered report file each.
