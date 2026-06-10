# 9 — completeness critique: what the eight dimensions missed

cloud-designer, 2026-06-10. A final critic re-read the full evidence and the
synthesis, then drilled the source for what the dimension fan-out failed to
examine. The verdict ("not production-ready") survives — nothing here rescues
it — but three findings materially reshape the *gate ranking*, and one corrects
an over-rating that pre-empts a decision the psyche explicitly reserved.

## A — GC-retention / eviction safety: an entire dimension nobody examined

The dimensions treated GC-roots only as a *state-durability* question ("the Vec
is in-memory"). None asked whether the retention machinery — the daemon's
charter per INTENT.md — actually *works*. It does not:

- **`Retire` reclaims nothing.** `retire_generation` (`schema_runtime.rs:1070-1103`)
  only does `state.gc_roots.0.remove(index)` — an in-memory `Vec` pop — then
  replies `Retired`. It never deletes a `/nix/var/nix/gcroots` symlink (none is
  ever written) and never triggers store GC on any node. Retiring a generation
  is pure bookkeeping with zero disk effect.
- **The GC effect is dead code.** `EffectCommand::PathInfoGc` /
  `run_path_info_gc` / `NixCommand::collect_garbage` (`ssh <node> "nix-store
  --gc"`, `schema_runtime.rs:1351-1360,1831-1836`) has a dispatch arm and a body
  but is **never constructed** — every `CommandEffect` emission site
  (`:605/625/631/774/790/802`) was grepped; `PathInfoGc` is absent. The daemon
  can never collect garbage on a node.
- **If it were wired, it would be rootless-unsafe.** `collect_garbage` is bare
  `nix-store --gc` with no `--max-freed` / keep-roots guard. On a node whose
  live/pinned generations live only in the daemon's volatile memory with **no
  on-disk gcroot symlink**, that would be free to delete the running system
  closure. A latent footgun the whole retention story rests on.

## B — Deployment-input field divergence: a real OsOnly parity defect mislabeled "covered"

The deploy-parity dimension marked deployment-input materialization COVERED
without diffing the *emitted fields*. They differ, and the difference changes
the built closure:

- lojix-cli's `DeploymentShape` (`lojix-cli/src/build.rs:57-91`) emits **only**
  `includeHome`.
- The new daemon's `DeploymentInput` (`schema_runtime.rs:1612-1638`) emits
  `includeHome` **and** `includeAllFirmware`.
- CriomOS reads both (`flake.nix:81-85`,
  `modules/nixos/metal/default.nix:36`: `includeAllFirmware = deployment.includeAllFirmware or includeHome`);
  the firmware-policy check (`checks/metal-firmware-policy/default.nix:80-83`)
  pins the intended matrix.

Consequence: for an **OsOnly** deploy, lojix-cli emits `includeHome=false` →
firmware falls back to `false`; the new daemon emits
`includeHome=false, includeAllFirmware=true` → `enableAllFirmware=true`. **The
two tools build different metal closures for the same OsOnly deploy** — a real
behavioral divergence in the one capability (build) the daemon claims, and
"parity" here isn't even well-defined until this is reconciled.

## C — The in-memory-state gate is over-rated *for the strict lojix-cli parity bar*

The single most consequential correction. The synthesis lists in-memory state as
a co-equal **blocker** alongside activation. But `lojix-cli` **keeps no state
whatsoever** — it is a stateless one-shot CLI with exactly 4 request variants
(`lojix-cli/src/request.rs:51-55`); grep for gcroot/retire/pin/event-log/live-set
in its source returns zero. The entire live-set / GC-roots / event-log /
pin-unpin-retire machinery is **net-new daemon charter, not parity scope.**

So "state lost on restart" blocks the daemon's *expanded ambition* (durably
owning the cluster-wide live set, per INTENT.md), **not** functional parity with
lojix-cli. For the minimal "build + activate one node on demand" bar, restart-
amnesia is as irrelevant as it is for lojix-cli today. INTENT.md sequences
durable backing as "the next storage cutover," deliberately *after* parity — and
the psyche's own open question 2 ("is the first cutover allowed to run on
in-memory state?") is exactly this decision. Flatly ranking durable state as a
co-equal blocker **pre-empts the answer the psyche reserved.** It is a blocker
for the *full charter*, conditional for the *first cutover*.

## D — Thinly-verified / slightly-overstated claims to hold honestly

- The **474µs concurrency figure** is one `#[ignore]` run nobody re-ran. The
  non-blocking property is proven *by construction* (the `!Send` guard cannot
  cross the `+Send` future bound — trustworthy); don't cite the microsecond
  number as a guarantee.
- The **secrets-eval break is narrower than "router/LLM nodes."** Precisely: the
  router throw (`router/default.nix:28,36`) fires only when
  `wpa3SaePassword` is set; the LLM `sopsFile` read (`llm.nix:163`) only when the
  LLM module is active. Genuine blocker for *those* nodes, not unconditional.

## E — Angles still uncovered (lower confidence, worth a look before any go)

- **Partial-failure compensation.** Ordering is *safe* against stale state
  (live-set written only after `GenerationActivated`; `fail_pipeline`
  `:862-866` clears in-flight slots) — no bug today. But there is **no
  compensation for copy-succeeds/activate-fails** (closure on target, no
  live-set record, no cleanup). Moot while activate is rejected; live the instant
  it lands.
- **`state_digest = commit_sequence` is a fake** (`schema_runtime.rs:425,432`) —
  the wire `DatabaseMarker` carries no real integrity hash, so a client can't
  detect divergence for compare-and-swap against the marker.

## Bottom line of the critique

The "not production-ready" verdict is correct and well-supported. But fold in:
(1) GC-retention/eviction is an unbuilt, latently-unsafe dimension nobody scored;
(2) the OsOnly firmware-field divergence is a concrete build-correctness defect,
not "covered" parity; (3) durable state blocks the *charter*, not minimal
parity — keep it distinct so the psyche's reserved decision stays open. Files to
drill before any go: `schema_runtime.rs:1070-1103` (retire),
`:1351-1360`/`:1831-1836` (dead GC), `:1612-1638` (deployment fields) vs
`lojix-cli/src/build.rs:85-91` and `CriomOS/checks/metal-firmware-policy/`.
