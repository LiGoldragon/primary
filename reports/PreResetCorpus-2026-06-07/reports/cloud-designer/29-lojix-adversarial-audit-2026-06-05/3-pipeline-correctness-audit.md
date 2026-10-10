# 3 — Engine pipeline correctness audit (Dimension 3)

cloud-designer lane sub-agent, 2026-06-05. ADVERSARIAL, READ-ONLY. Lens:
the engine state machine is broken/racy/wrong until proven otherwise. Every
claim cites `file:line` against the pushed copies. Where I cannot confirm
from the file, I say so.

Primary target: `/git/github.com/LiGoldragon/lojix/triad-port/src/schema_runtime.rs`
(the `decide` trampoline, the `DeployStage` machine, the sema writes, the
nix-IO arms). Supporting: `triad-runtime/src/runner.rs` (budget),
`.../src/daemon.rs` (the two-socket loop), `lojix/triad-port/src/lib.rs`
(`StoreState`), `lojix/triad-port/src/schema/nexus.rs` (the generated
`execute` / `NexusRunnerAdapter`).

## Headline verdict

The state machine is **functionally correct on the happy path AND on the
re-entrancy axis** — better than report 26 implied. The two attack vectors
the brief weighted most heavily come back NEGATIVE:

- **(b) Re-entrancy: NO corruption is possible.** `execute` drives the runner
  to a terminal `Reply` while holding `&mut self` exclusively, and the daemon
  loop is single-threaded (poll-accept-handle, one stream at a time). A second
  request cannot enter `decide` mid-pipeline. The single-slot `active_deploy` /
  `active_operation` fields are safe *because of* this serialization — but that
  safety is **undocumented and structurally fragile** (Finding P3).
- **(a) The report-26 name-vs-action mismatch is STILL PRESENT** but it is a
  *naming/legibility* defect, not a wrong-effect-fires bug: I traced every
  stage transition and no action reaches a stage that fires the wrong effect
  on the happy path (Finding P1). The mismatch is real and should be fixed, but
  it is mis-rated if called a correctness break.

The genuinely-broken items this dimension surfaces are different from the
brief's hypotheses: a **double-locked, non-atomic `event_log_position` that is
guaranteed off-by-... nothing-on-happy-path-but-wrong-under-the-stated-model**
(P2), an **`active_operation` leak on the read path that mis-types the NEXT
deploy's rejection** (P4), a **`fail_pipeline` that clears `active_deploy` but
NOT `active_operation`** (P5), and **two sema-write reason mappings that are
provably wrong** (P6). Details below, severity-ordered.

## (a) DeployStage trampoline — every transition traced

The chain is split across two functions. `decide_effect_completion`
(schema_runtime.rs:628-687) handles effect results and fires the *next effect*
directly; `advance_after_phase` (schema_runtime.rs:488-521) handles
phase-write completions and fires the *next effect or final write* keyed on
`pipeline.stage`. The `DeployStage` enum (schema_runtime.rs:77-88) is touched
ONLY in `advance_after_phase` + `set_stage`.

Full happy-path trace for a System **Switch** (the longest pipeline), naming
the firing site and the resulting `NextStep`:

1. `decide_meta_input` Deploy (385-400) → `CommandSemaWrite(RecordDeploySubmitted)`.
2. `record_deploy_submitted` (751-777) sets `active_deploy = Some(stage=Submitted)`; write out `DeploySubmitted`.
3. `begin_deploy_pipeline` (476-486) → `CommandEffect(ResolveFlakeAuth)`. **Stage still Submitted.**
4. effect `FlakeResolved` → `record_phase(Building)` (643-646) → `CommandSemaWrite(RecordPhaseTransition)`. **Stage still Submitted.**
5. phase write done → `advance_after_phase`, `Submitted` arm (501-506): `set_stage(BuildingRecorded)`, fire `NixEval`.
6. effect `ClosureEvaluated` (648-659): `produces_closure()` true → `CommandEffect(NixBuild)`. **Stage BuildingRecorded; not advanced.**
7. effect `ClosureBuilt` (660-672): `activates()` true → `CommandEffect(CopyClosure)`. **Stage still BuildingRecorded.**
8. effect `ClosureCopied` (673-677) → `record_phase(Copying)`. **Stage still BuildingRecorded.**
9. phase write done → `advance_after_phase`, `BuildingRecorded` arm (507-512): `set_stage(CopyingRecorded)`, fire `ActivateGeneration`.
10. effect `GenerationActivated` (678-683) → `record_phase(Activated)`. **Stage still CopyingRecorded.**
11. phase write done → `advance_after_phase`, `CopyingRecorded` arm (513-518): `set_stage(ActivatedRecorded)`, fire `CommandSemaWrite(RecordGenerationActivated)`.
12. that write completes as `GenerationActivated` → `decide_write_completion` (458) → `finish_deploy_pipeline` (529-542) → `ReplyToSignal(Deployed)`.

### Finding P1 — the stage NAMES describe the prior phase, not the next action (report-26 B4 confirmed STILL PRESENT) — LOW/correctness-OK, MEDIUM/legibility

The mismatch report 26 flagged is intact:
- `DeployStage::BuildingRecorded` (schema_runtime.rs:81) fires **ActivateGeneration**, not a build (507-512). Build/Copy effects happen in
  `decide_effect_completion`, invisible to the stage enum.
- `DeployStage::CopyingRecorded` (84) fires the **RecordGenerationActivated write**, not a copy (513-518).

So the enum tracks only 3 of the ~7 real transitions (the eval/build/copy/
activate effect hops live in `decide_effect_completion`), and each variant
name names the phase just *recorded*, while the arm fires an action two steps
downstream. **This is a legibility defect, not a wrong-effect bug**: I confirmed
no action reaches a stage that fires the WRONG effect on the happy path. The
docstring at schema_runtime.rs:72-76 even concedes the chain interleaves
phase-writes and effects, so the names are knowingly approximate.

Why it is still a real flaw to fix: the split-brain sequencing (half in
`advance_after_phase` keyed on `stage`, half in `decide_effect_completion`
keyed on the effect-result variant) means there is **no single place that
expresses the deploy order**. Any future edit that adds a stage (e.g. a
GC-after-activate, or the M3 materialization write) must touch BOTH functions
and keep the implicit interleave consistent, with the enum names actively
misleading the editor. Concrete fix: either (1) lift the full ordered pipeline
into the schema as report 26 recommended (an explicit `DeployStage` covering
FlakeAuth/Eval/Build/Copy/Activate/Record, with `advance` the *sole* driver
and `decide_effect_completion` only validating the expected result for the
current stage), or (2) at minimum rename the variants to name the NEXT action
(`AwaitingEval`, `AwaitingActivate`, `AwaitingActivationRecord`) and add a
doc-comment crosswalk to the effect-driven hops. Option (1) is the durable
fix and removes the dual-driver fragility entirely.

### Finding P1b — Home `Build` / System `Eval` early-termination is CORRECT, but System `Boot/Test/BootOnce` share the Switch path with a WRONG slot recorded — MEDIUM

The early-termination logic the brief flagged as an M1 change is correct where
it terminates: System `Eval` returns after eval without building (650-658,
guarded by `produces_closure()`); System `Build` / Home `Build` return after
build without copy/activate (662-671, guarded by `activates()`). Both verified
against `DeployAction::produces_closure` (105-110) and `activates` (115-128).

But trace a System **Boot** to the activation-record write. `activate_generation_command`
(274-281) passes `self.activation_kind`, set by `system_activation_kind`
(194-203): Boot→`ActivationKind::Boot`. `run_activate_generation` (1153-1166)
maps that through `activation_slot` (1168-1175): Boot→`GenerationSlot::BootPending`.
**But that slot is discarded.** `record_generation_activated` (800-844)
hardcodes `generation_slot: commit.generation_slot` from the `ActivationCommit`,
and `activation_commit` (283-291) hardcodes `GenerationSlot::Current` (288). So
a **Boot deploy records its live generation in slot `Current`**, not
`BootPending` — the activation effect computed the right slot, the live-set
write ignored it. This means a `Boot` (stage the new generation for next reboot,
don't switch now) is indistinguishable in the durable live-set from a `Switch`.
Report 26 C1 noted the live-set never demotes; this is the adjacent bug — the
slot it writes is wrong for 3 of 4 activation kinds. Concrete fix:
`activation_commit` must take the computed slot from the pipeline
(thread the `GenerationSlot` from `run_activate_generation`'s
`ActivatedGeneration.generation_slot` into the `ActivationCommit`, instead of
the literal `Current`), and `record_generation_activated` should also write the
matching `gc_roots` slot. (Note: the `ActivatedGeneration.generation_slot`
field IS produced at 1161 and then dropped — confirming the wiring gap.)

## (b) Re-entrancy — NO corruption; serialization is real but undocumented

### Finding P3 — single-slot `active_deploy`/`active_operation` are safe ONLY because of an undocumented single-thread + run-to-completion invariant — MEDIUM (latent)

I attacked this hard and could not produce corruption. The reasons, traced:

1. `execute` (nexus.rs:1260-1273) builds a `Runner`, then calls
   `runner.drive(&mut runner_adapter, first_work)` which loops until
   `NextStep::Reply` (runner.rs:156-185, returns only on the `Reply` arm).
   Every intermediate step (`SemaWrite`/`SemaRead`/`RunEffect`/`Continue`)
   loops back into `decide_next_step` on the SAME `&mut Engine`. So one
   `execute` call runs the ENTIRE deploy pipeline to its terminal `Deployed`
   reply before returning. There is no yield point.
2. The daemon loop is single-threaded. `BoundMultiListenerDaemon::serve_streams`
   (triad-runtime/src/daemon.rs:392-397) → `serve_next_stream` (382-390) →
   `try_serve_next_stream` (368-380) accepts ONE stream, calls
   `self.runtime.handle_stream(...)` **synchronously** (372), and only then
   returns to poll the next. `handle_stream` (lojix daemon.rs:178-188) →
   `handle_ordinary`/`handle_owner` → `self.execute(...)` (daemon.rs:103,115).
   No thread spawn anywhere in either file. So request N's `execute` fully
   completes — including any in-flight deploy — before request N+1 is accepted.

Therefore a Query or a second Deploy arriving "while a deploy is mid-flight" is
**impossible**: there is no mid-flight observable state between requests,
because a deploy is atomic within one `execute`. The single-slot fields are
re-initialised (`active_deploy = Some(...)` at 764, taken at 531) cleanly per
deploy. **No interleaving, no corruption — confirmed.**

Why this is still a flaw to record: the safety is **entirely implicit**.
Nothing in `SchemaRuntime`, the daemon, or the runtime documents "this engine
MUST be driven single-threaded and run-to-completion; the single-slot
`active_deploy` field will corrupt if two `execute` calls ever interleave."
The moment anyone (a) spawns a thread per stream for concurrency, (b) makes any
effect arm yield/await, or (c) adds a real async sema-engine, the single-slot
model silently breaks: a second Deploy's `record_deploy_submitted` would
overwrite `active_deploy` (764) and the first deploy's continuations would
operate on the second's cursor. The `nix` effect arms BLOCK on
`Command::output()` (schema_runtime.rs:1295) for the entire build — could be
minutes — so the single-thread serialization also means **the daemon cannot
service ANY request, not even a Query, while a deploy builds**. That is a
liveness problem the brief's re-entrancy question implicitly assumes away.
Concrete fix: (1) document the invariant on `SchemaRuntime` and on
`MultiListenerRuntime::handle_stream` ("the engine is single-writer; one
request runs to completion before the next is accepted; `active_deploy` relies
on this"); (2) carry to the synthesizer as an open design question — the
blocking-build-stalls-all-requests behavior needs either a worker model or an
async effect plane before production, and whichever lands MUST replace the
single-slot fields with a keyed in-flight map.

## (c) Continuation budget (32) — cannot be exhausted by a real pipeline; exhaustion reply is mis-typed for ordinary callers

The budget is spent once per non-Reply step (runner.rs:159-182:
`SemaWrite`/`SemaRead`/`RunEffect`/`Continue` each call `spend_next_step`;
the `Reply` arm at 158 does NOT). `decide` itself is free —
`decide_next_step` (nexus.rs:1297-1300) does not spend; only the resulting
action's execution does.

The Switch trace above spends exactly **10** steps (steps 1-11 in the trace
minus the terminal reply): RecordDeploySubmitted, ResolveFlakeAuth,
RecordPhaseTransition(Building), NixEval, NixBuild, CopyClosure,
RecordPhaseTransition(Copying), ActivateGeneration,
RecordPhaseTransition(Activated), RecordGenerationActivated. Eval spends 4,
Build spends ~6. All well under 32. There is **no loop** in the pipeline (each
stage advances monotonically; `decide` never emits `NextStep::Continue` —
confirmed: no `NexusAction::Continue` is constructed anywhere in
schema_runtime.rs), so a pathological caller cannot inflate the step count from
a single request. **(c) comes back NEGATIVE — not exhaustible by any current
path.**

### Finding P7 — `budget_exhausted_reply` ALWAYS replies a META `DeployRejected`, even for an ordinary-socket request — MEDIUM (latent, but a real wrong-reply)

`budget_exhausted_reply` (schema_runtime.rs:1358-1365) unconditionally returns
`SignalOutput::MetaOutput(meta::Output::DeployRejected(...))`. If budget
exhaustion ever fired on an ORDINARY-socket request (a Query that somehow
looped), `handle_ordinary` → `ordinary_reply` (daemon.rs:145-152) would hit
the `MetaOutput(_) => Err(Error::UnexpectedFrame)` arm and the request would
error out instead of returning a typed ordinary rejection. Today no ordinary
path loops, so this is latent — but it is a structural wrong-reply: the
exhaustion handler doesn't know which socket the request came from
(`_exhausted` is ignored, and there's no origin-role in scope). Concrete fix:
the exhaustion reply must be origin-aware (route on the `OriginRoute` /
listener role the request carried), or — simpler — never reachable, which
argues for an assertion/trace that exhaustion-on-a-deploy is a bug worth
logging rather than a normal `DeployRejected(DeploymentInFlight)`. Note also
the reason it chooses, `DeploymentInFlight`, is semantically wrong for
budget exhaustion (the deploy isn't in-flight-elsewhere; the engine gave up) —
see P6.

## (d) Effect-failure mid-pipeline — `fail_pipeline` clears `active_deploy` but LEAKS `active_operation`

### Finding P5 — `fail_pipeline` does not clear `active_operation`; a failed deploy poisons the NEXT operation's rejection typing — HIGH

`fail_pipeline` (schema_runtime.rs:714-727) sets `self.active_deploy = None`
(715) and replies `DeployRejected`. **It never touches `self.active_operation`**,
which was set to `Some(MetaOperation::Deploy)` in `decide_meta_input` (388) and
is normally cleared by `finish_deploy_pipeline` (530) or
`reject_active_or_meta` (549, via `.take()`). After a mid-pipeline effect
failure, `active_operation` stays `Some(Deploy)` forever.

Now the consequence, traced. Suppose deploy A fails at the Build effect →
`fail_pipeline` replies `DeployRejected`, leaves `active_operation =
Some(Deploy)`. Request B is a **Pin**. `decide_meta_input` Pin arm (401-404)
overwrites `active_operation = Some(Pin)` — so B itself is fine. **But** suppose
B is instead a Pin whose SEMA write is rejected: `reject_active_or_meta` (549)
`.take()`s `active_operation` → `Some(Pin)`, replies `PinRejected`. Correct.
The leak is benign ONLY because every meta operation re-sets
`active_operation` on entry (388/402/406/410). So the leak is **masked on the
meta path** by the unconditional re-set.

Where it is NOT masked: a deploy whose `begin_deploy_pipeline` finds
`active_deploy == None` (476-479) — which happens precisely after a prior
`fail_pipeline` cleared `active_deploy` but the runner somehow re-entered (it
can't today, per P3, but this is the latent coupling). More concretely and
reachably: `advance_after_phase`'s `None` arm (492-498) and `record_phase`'s
`None` arm (705-709) both reply `DeployRejected(DeploymentInFlight)` when
`active_deploy` is unexpectedly `None`. If a prior `fail_pipeline` left state
half-cleared and a stray effect/write completion arrived, these arms fire — but
again, P3's serialization prevents the stray completion. **Net: the leak is
currently latent, not active, because of the same single-thread invariant.**
But it is a clear correctness bug-in-waiting and trivially fixable. Concrete
fix: `fail_pipeline` must `self.active_operation = None;` alongside the
`active_deploy = None;` at line 715 — symmetric with `finish_deploy_pipeline`
(530-531). This is the cleanest single-line correctness fix in the file.

### Finding P5b — `fail_pipeline` reads the failure stage but the next deploy does start clean (confirmed) — OK

I verified the brief's sub-question "does the next deploy start clean?": YES,
on the `active_deploy` axis. `fail_pipeline` nulls `active_deploy` (715); the
next Deploy's `record_deploy_submitted` (764) writes a fresh
`Some(DeployPipeline{stage: Submitted, closure_path: None, ...})`. No stale
closure path or stage carries over. The ONLY leak is `active_operation` (P5).

## (e) sema writes + rejection mapping — two provably-wrong reason maps

### Finding P6 — `deploy_reason` and `retire_reason` fallthroughs map to WRONG/ambiguous reasons; `pin_reason` fallthrough is also wrong — MEDIUM

`reject_active_or_meta` (544-570) maps a sema `RejectionReason` to a typed meta
rejection reason via four helpers. Auditing each against the contracts:

- `deploy_reason` (601-610): the `_ =>` fallthrough maps **everything else** to
  `DeployRejectionReason::DeploymentInFlight` (608). But the catch-all swallows
  `PlanNotApproved` (the reason `record_deploy_submitted:775` and every
  poisoned-lock path emit) into "DeploymentInFlight" — so a **poisoned store
  lock during a deploy submit is reported to the owner as 'deployment already
  in flight'**, a actively misleading diagnosis. Concrete fix: add an explicit
  arm for the lock/internal reasons (a distinct `DeployRejectionReason` for
  internal failure, or at least not `DeploymentInFlight`).

- `retire_reason` (589-599): the `_ =>` fallthrough maps to
  `RetireRejectionReason::GenerationUnknown` (597). So a retire that fails for
  any reason not in the 4 explicit arms reports "generation unknown" even when
  the generation exists. Less severe (retire's real rejections are covered by
  the explicit arms), but the fallthrough is a wrong-reason default. Lower
  priority than the deploy one.

- `pin_reason` (572-579): `_ =>` maps to `PinRejectionReason::PinSlotExhausted`
  (577). But `PinSlotExhausted` is a reason **never produced by the sema layer**
  (report 26 C4 confirmed no pin-slot cap exists). So an *unexpected* sema
  reason on the pin path is reported as a pin-slot-exhaustion that the system
  cannot actually cause — a phantom reason. The poisoned-lock path
  (`pin_generation:880`) emits `GenerationUnknown` which IS explicitly mapped
  (574), so the lock case is fine; the fallthrough is the concern. Fix: default
  to `GenerationUnknown` (the safest "we couldn't apply it") rather than a
  never-otherwise-produced reason.

These three are correctness-of-diagnosis bugs, not crashes — but the brief
asked specifically for "wrong-reason" mapping and these are it.

### Finding P6b — `record_generation_activated` reads `active_deploy` AFTER the pipeline may be the wrong source of truth — LOW

`record_generation_activated` (800-844) re-reads `self.active_deploy` (807) to
recover `deployment_identifier`/`deployment_kind`/`activation_kind`, with
`.unwrap_or(0)` / `.unwrap_or(FullOs)` / `.unwrap_or(Switch)` defaults
(809-817). On the happy path `active_deploy` is still `Some` (it is taken only
in `finish_deploy_pipeline` at 531, which runs AFTER this write completes), so
the defaults never fire. Confirmed safe today. But it is a second read of
pipeline state from a different method than the one that owns it
(`activation_commit` at 283 already carried `generation_slot` and
`closure_path` — yet `deployment_kind`/`activation_kind` are NOT on the
`ActivationCommit`, forcing this back-channel read). This is the same
"`ActivationCommit` doesn't carry everything the write needs" gap that produced
P1b's wrong-slot bug. Fix: widen `sema::ActivationCommit` to carry
`deployment_identifier`, `deployment_kind`, `activation_kind`, AND the computed
`generation_slot`, so `record_generation_activated` is a pure function of its
input and the back-channel `active_deploy` read disappears.

## (f) event-log position — double-locked, non-atomic, and wrong under the stated model

### Finding P2 — `event_log_position` is computed under TWO separate locks and stamped TWICE with potentially different values; and `next_event_log_position` is read-only `Vec::len` with no reservation — MEDIUM (HIGH if the model ever becomes concurrent)

`next_event_log_position` (lib.rs:149-151) is `self.event_log.0.len() as u64` —
a pure read, no increment, no reservation. It is read in TWO places for the
SAME phase event:

1. `record_phase` (schema_runtime.rs:700-703): locks the store, reads
   `next_event_log_position()`, **drops the lock**, and stamps the
   `DeploymentPhaseEvent.event_log_position` with that value (the value that
   travels in the wire event).
2. `record_phase_transition` (779-798): locks the store AGAIN, reads
   `next_event_log_position()` AGAIN (786), pushes the `EventLogEntry` with
   THAT value (788), and the `PhaseReceipt.event_log_position` (792) carries
   the second read.

Between the two locks the engine does nothing else (single-thread), so the two
`len()` reads return the same value TODAY. But this is structurally a
**check-then-act across a dropped lock**: the position is read, the lock is
released, and the write re-reads. The `DeploymentPhaseEvent` that goes out on
the wire (stamped in step 1) and the `EventLogEntry`/`PhaseReceipt` stored in
step 2 are stamped from independent reads. Under the stated future model
(concurrent sema engine, redb, or per-stream threads — lib.rs:10-12 names
"sema-engine / redb persistence is a noted follow-on"), two concurrent
phase-records would both read the same `len()`, both push, and **two entries
would share one `event_log_position`** — a duplicate-key / lost-ordering bug.
`next_event_log_position` does not reserve; `Vec::push` does the actual append
without consuming a reserved slot.

Also note the off-by-context subtlety: positions are **0-based** (`len()` of an
empty vec is 0, so the first event is position 0), while `read_event_log`
(1049-1074) filters `position >= range.until` (1060) — a half-open `[from,
until)` range. That is internally consistent (0-based, half-open). I found **no
off-by-one** in the happy path. The defect is the non-atomic double-read, not
an index error. Concrete fix: make position assignment a single
locked reserve-and-return — `record_phase` should NOT pre-stamp from a
separate lock; instead `record_phase_transition` should allocate the position
under its lock and the outgoing `DeploymentPhaseEvent` should be built from
THAT allocation (return the position from the write and thread it into the
reply event), or add a `next_event_log_position(&mut self) -> u64` that
atomically reserves (e.g. backed by a counter like the other `next_*_sequence`
methods at lib.rs:134-156, which DO increment — the event-log one is the odd
one out that only reads).

### Finding P2b — `next_event_log_position` is the ONLY `next_*` that doesn't increment a counter — inconsistency that signals the bug — LOW (corroborating)

`next_commit_sequence` (lib.rs:134), `next_deployment_identifier` (139),
`next_generation_identifier` (144), `next_subscription_token` (153) all
`+= 1; return`. `next_event_log_position` (149) alone derives from `Vec::len()`
without a counter. This asymmetry is the smell that surfaces P2: the event-log
position should be a reserved monotonic counter like its siblings, not a
derived length, so that reservation is atomic and decoupled from the Vec's
actual push. (Today `len()` happens to equal the counter because nothing
deletes from the log — but the moment anything compacts/truncates the event
log, `len()`-derived positions COLLIDE with prior positions. The counter form
is collision-proof.)

## (Cross-cut) Finding P4 — the READ path leaks `active_operation`, mis-typing a LATER deploy/pin/etc. rejection — MEDIUM

Trace: a `Query` arrives. `decide_ordinary_input` (347-360) routes to
`CommandSemaRead`. **It never touches `active_operation`.** Suppose
`active_operation` is `Some(Pin)` left over from a prior pin whose write was
rejected — except `reject_active_or_meta` `.take()`s it (549), so a rejected
pin clears it. The leak window is: a meta operation that sets
`active_operation` (388/402/406/410) but then takes a path that NEVER reaches
`reject_active_or_meta` OR a `*Pinned/*Unpinned/*Retired/finish` clear. The
clearest such path is **the deploy effect-failure path (P5)**: `fail_pipeline`
leaves `active_operation = Some(Deploy)`. Now a Query arrives (read path,
doesn't touch it), returns fine. Then a Pin arrives → re-sets to `Some(Pin)`,
fine. So on the meta path the stale value is always overwritten before use.

The genuinely-reachable hazard: `reject_active_or_meta` (544-570) is the
ONLY consumer of `active_operation`, and it `.unwrap_or(MetaOperation::Deploy)`
(549). If a sema WRITE rejection arrives when `active_operation` is `None`
(e.g. a `RecordPhaseTransition` or `RecordGenerationActivated` write that gets
rejected mid-deploy — `record_phase_transition:796` and
`record_generation_activated:842` both emit `WriteRejected` on a poisoned
lock), `decide_write_completion` (472) routes to `reject_active_or_meta`. At
that point in a deploy `active_operation` is still `Some(Deploy)` (set at 388,
not yet cleared) — so it correctly maps to `DeployRejected`. Good. **But** the
`.unwrap_or(Deploy)` default means: if ANY write rejection ever arrives with
`active_operation == None`, it is silently reported as a **DeployRejected** even
if the originating request was a Pin/Unpin/Retire. Combined with P5's leak,
the failure modes compound. Concrete fix: pair the P5 fix (clear
`active_operation` in `fail_pipeline`) with making the `None` case explicit —
`reject_active_or_meta` should not silently assume `Deploy`; an unexpected
`None` is an internal-invariant violation worth a distinct reply/trace, not a
defaulted `DeployRejected`.

## Tight summary for the verifier/synthesizer

Ordered by severity. Every finding cites the file above.

1. **P5 (HIGH, 1-line fix): `fail_pipeline` (schema_runtime.rs:714-727) clears
   `active_deploy` but NOT `active_operation`.** A mid-pipeline effect failure
   leaks `active_operation = Some(Deploy)`. Currently masked by every meta op
   re-setting it on entry + the single-thread invariant, but a real correctness
   bug. **Fix: add `self.active_operation = None;` at line 715**, symmetric with
   `finish_deploy_pipeline:530`.

2. **P1b (MEDIUM, wrong durable state): Boot/Test/BootOnce record slot
   `Current`.** `run_activate_generation` (1153-1166) computes the right
   `GenerationSlot` (1161) then drops it; `activation_commit` (283-291)
   hardcodes `GenerationSlot::Current` (288). A `Boot` deploy is
   indistinguishable from `Switch` in the live-set. **Fix: thread the computed
   slot from the activate effect into `ActivationCommit`; have
   `record_generation_activated` write it (and the matching gc_root slot).**

3. **P2 (MEDIUM, HIGH-if-concurrent): `event_log_position` double-locked,
   non-atomic, derived from `Vec::len()` with no reservation.** `record_phase`
   (700-703) and `record_phase_transition` (786) read the position under TWO
   separate locks and stamp it twice; `next_event_log_position` (lib.rs:149) is
   the only `next_*` that doesn't increment a counter. Safe under today's
   single-thread happy path, collides the instant the log compacts or the model
   goes concurrent. **Fix: a single locked reserve-and-return (a monotonic
   counter like the sibling `next_*_sequence` methods), allocate the position
   once in the write and thread it into the outgoing event/receipt.**

4. **P6 (MEDIUM, wrong diagnosis): two/three rejection-reason fallthroughs are
   wrong.** `deploy_reason` (601-610) maps a poisoned-lock `PlanNotApproved`
   to `DeploymentInFlight` (608) — reports a lock error as "already deploying."
   `pin_reason` (577) defaults to `PinSlotExhausted`, a reason the system never
   actually produces. `retire_reason` (597) defaults to `GenerationUnknown`
   even for existing generations. **Fix: give each fallthrough an honest
   internal-error reason instead of a misleading domain reason.**

5. **P3 (MEDIUM, latent + liveness): single-slot `active_deploy`/`active_operation`
   are safe ONLY because `execute` runs to completion single-threaded
   (nexus.rs:1260-1273 + triad-runtime daemon.rs:368-397 — no thread spawn).**
   The invariant is real (so NO re-entrancy corruption today — the brief's (b)
   is NEGATIVE) but **undocumented and fragile**, and the blocking `nix` effect
   (schema_runtime.rs:1295) means the daemon services NO request, not even a
   Query, while a build runs. **Fix: document the single-writer/run-to-completion
   invariant on `SchemaRuntime` + `handle_stream`; carry the
   blocking-build-stalls-everything liveness issue to the synthesizer as an
   open design question (worker model / async effect plane MUST replace the
   single-slot fields with a keyed in-flight map before any concurrency).**

6. **P4 (MEDIUM): `reject_active_or_meta` (549) `.unwrap_or(Deploy)` silently
   types any `active_operation == None` write-rejection as `DeployRejected`,
   even for a Pin/Unpin/Retire origin.** Compounds with P5. **Fix: treat the
   `None` case as an internal-invariant violation, not a defaulted Deploy.**

7. **P1 (LOW correctness / MEDIUM legibility): the report-26 DeployStage
   name-vs-action mismatch is STILL PRESENT** (`BuildingRecorded` fires
   ActivateGeneration at 507-512; `CopyingRecorded` fires the activation-record
   WRITE at 513-518). I confirmed **no wrong effect fires on the happy path** —
   it is a legibility/maintainability defect from the dual-driver split
   (sequencing half in `advance_after_phase` keyed on stage, half in
   `decide_effect_completion` keyed on result). **Fix: lift the full ordered
   pipeline into one driver (report 26's recommendation), or at minimum rename
   variants to name the NEXT action.**

8. **P7 (MEDIUM latent): `budget_exhausted_reply` (1358-1365) always replies a
   META `DeployRejected`**, which `ordinary_reply` (daemon.rs:150) would turn
   into `UnexpectedFrame` for an ordinary caller; its reason
   `DeploymentInFlight` is also semantically wrong for exhaustion. Not reachable
   today (no path loops; budget caps at 32, happy Switch spends 10 — **(c) is
   NEGATIVE**). **Fix: make the exhaustion reply origin-aware, or assert/trace
   exhaustion-on-deploy as a bug.**

9. **P6b/P2b (LOW, corroborating): `record_generation_activated` back-channels
   `active_deploy` (807) for fields `ActivationCommit` should carry; the
   event-log position is the lone non-counter `next_*`.** Both point at the
   same fix family (widen the sema input records so writes are pure functions
   of their input).

### Brief-question scorecard

- (a) wrong-effect-fires: **NEGATIVE on the happy path** (no action fires the
  wrong effect); the report-26 name mismatch is a real but mis-rated legibility
  defect (P1). One genuine wrong-state write found adjacent: Boot/Test slot
  (P1b).
- (b) re-entrancy/corruption: **NEGATIVE** — `execute` runs to completion,
  daemon is single-threaded; single-slot fields are safe but the invariant is
  undocumented and carries a liveness cost (P3).
- (c) budget exhaustion: **NEGATIVE** — uninflatable; happy Switch spends 10/32;
  exhaustion reply is mis-typed if ever reached (P7).
- (d) fail mid-pipeline: **POSITIVE** — `active_deploy` cleared cleanly, next
  deploy starts clean, BUT `active_operation` leaks (P5, the headline fix).
- (e) sema writes / rejection mapping: **POSITIVE** — three wrong-reason
  fallthroughs (P6), plus the Boot slot write (P1b).
- (f) event-log position: **POSITIVE** — non-atomic double-read, no off-by-one
  on the happy path but collision-prone under the stated future model (P2).
