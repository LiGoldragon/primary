# Typed permaflow effort: design for Astra's ruling (5hnb)

Status: design/evidence only. Updated for Astra iefq relaying Psyche kob2; canonical readiness is still required before implementation. No source edits, builds, publication, configuration, launches, or deployment. This report extends `/tmp/effort-design-2b83e2.Eq1Hi0/design-status.md`; its audit report for gqio remains complete. Decisions below are proposals until approved.

## 1. Shared owner and dependency order

Authored `psyche-belief/vision/flow-nexus-v1.md:40,55` declares Low/Medium/High and places Effort in Member. The task explicitly selects permaflow Option<Effort>, None meaning harness default. Astra's relayed owner proposal is `signal-curriculum-nexus/crates/curriculum/ethos/curriculum.ethos`, crate curriculum, owned by Curriculum Astra/Sol. That checkout is still absent at this report's inspection; no implementation or published revision is verified.

Publish the leaf once, then flow-ethos importing/reexporting it, then signal-flow and meta-signal-flow, then Flow and actual consumers, then owner declarations and Home pins. The leaf must import no Flow contract. Curriculum Role and future Flow Member use that identical Rust type. Flow's existing v0 four-variant curriculum module is outside the v1 replacement graph under Astra tcte/8x4r; preserve it, with no Xhigh coercion or live v0 migration. Curriculum Astra owns old-data readiness.

Canonical crate has default features empty and datom gated; flow-ethos/datom forwards curriculum/datom, then the signal/meta datom features forward through flow-ethos. Test both plain and textual graphs. Current accepted Flow actually enables datom on workspace flow-ethos and meta-signal-flow (`Cargo.toml:16`, nexus manifest:25); plain Nexus compliance is not already proved. Psyche kob2 authorizes removing those existing text edges as its own prerequisite; the concrete boundary plan is in prerequisite-plan.md beside this report. Adding the leaf must introduce no unconditional text dependency.

## 2. Contract and implementation changes

Accepted source: Flow 5d70c7b8a04c5119e978297668b2925b0c5e1186, signal61 4871bb81c1119fe72dc76168a97e1e576411b831, meta77 e72f5552816477e1acfaab6cd7515bc5f807edff; worktrees named in predecessor report. `signal-flow/ethos/signal.ethos:509` currently declares Effort.String; replace its declaration with the canonical import/reexport. Its LaunchProfile:548, NativeLaunchIntent:557 and PromptDeliveryIntent:564 carry Option<Effort>. NativeTargetReceipt:565 needs requested policy separate from native observation. Its enclosing ComposedLaunch, LaunchAttempt, LaunchInspection and Query/Response change transitively. Keep historical rejection variants stable rather than removing InvalidEffort merely because typed inputs make it unreachable; changing unrelated rejection anatomy needlessly enlarges durable migrations.

`meta-signal-flow/ethos/signal.ethos:418`: extend the nine-field ConfigureMetaflow by one Option<Effort> in one fixed, documented position (propose directly after Address). ConfigurationSnapshot and Configure.Permaflow/Metaflows change transitively. Regenerate both contracts, bump wire semvers/digests, and update all clients and fixtures atomically per vocabulary. Old/new greetings must refuse mismatch before archive decoding. No variable-arity compatibility parser.

Flow touch points:
- `src/model.rs` RunsModel and `src/sending.rs:511,590–615`: remove model-selected hardwired effort, read declaration's requested option.
- `src/composition.rs:243,396,831,888`: prompt header, composition validation, FreshFlowContext's current String and its conversion all become option-aware; render None as Harness default, never as an inferred medium.
- `src/launching.rs:475`, generated starter/operation types and all profile/intent constructions follow the same option.
- `src/herdr/launch.rs:2090`: explicit variant becomes lowercase only in native adapter; None omits Claude --effort and Codex -c model_reasoning_effort. Preserve unrelated arguments exactly.
- `src/codex.rs:900,956,970`: omit effort from turn/startup JSON and model_reasoning_effort from config for None. A JSON null is not omission. Explicit variants encode at this contact. Thread id/model/instruction-source checks still run for every option.
- `src/herdr/launch.rs:1188,2725,2885,2929,3060`: option equality in intent/launch matching; native checks and receipt creation must separate requested from observed values.
- `src/restarting.rs:1206–1285,1547`: same-session Restart obtains effort from the original session's durable launch profile, not today's declaration/model rule; current modules/tool handling is a distinct existing policy, not authority to redesign it here. Refresh reads latest declaration. Select the profile by proven flow/native-session binding, not an unproved ordering of launch request ids. Psyche kob2 rules that missing historical intent reopens with requested None and no effort override, without missing-intent refusal. Retain provenance separately (RecoveredIntent versus NoRecordedIntent); that provenance does not change the ruled option. Available original intent is preserved; current declaration is not substituted.

## 3. Requested policy and native evidence

Requested Option is durable intent throughout; observing a native default never writes Some back to it. None proves Flow emitted no effort override. It does not prove the harness chose a particular level, nor exclude user/global harness configuration.

Proposed separate native observation vocabulary: Reported holds foreign NativeEffortText plus the digest of the native source row; Unobserved holds no invented value. NativeEffortText is native evidence, not a second explicit-effort enum; it may faithfully hold a native xhigh/default/other value. Receipt keeps requested Option independently. Thread readback and actual turn observation are distinct evidence; retain their source/stage, and preserve both Claude fields when both are present rather than silently selecting one. Malformed or conflicting reported fields fail verification. Final exact anatomy awaits Astra's ruling, before implementation.

For Some, every native field that reports effort must match the explicit lowercase level; wrong reported effort fails. For None, reported native effort is recorded without imposing a level. Missing/null native fields yield Unobserved, not a claimed matching default. Claude `claude_effort_matches:1503` currently accepts missing/null fields vacuously (including Haiku), and receipt construction:3060 copies intent.effort. The replacement must expose that observation gap. Psyche kob2 allows Some with Unobserved; admit while reporting effort observation as unavailable. Current behavior cannot support a claim of native explicit-effort proof. Keep thread/model/session/turn/hash checks separate from effort evidence.

## 4. Durable family closure and upgrade

For the above minimal shape, exactly these current archive owners embed changed fields:

| Family | Current identity | Why | Proposed next |
|---|---|---|---|
| flow-nexus-meta-metaflow-configuration | v6, `store/metaflow_declaration.rs:20–41` | ConfigureMetaflow | v7 |
| flow-nexus-launch-attempt | v5, `store.rs:1363–1380` | LaunchAttempt includes profile, native intent, prompt intent and receipt/result | v6 |
| flow-nexus-ordered-replacement | v1, `store/ordered_replacement.rs:22–64` | OrderedLaunch embeds LaunchProfile | v2 |

These are proposed next labels, not reserved version numbers. AddressHold stores Option<Metaflow>, not LaunchProfile. StoredMetaflow, launch outcomes, pending reaps/handovers, queue/request records, opened threads, roles and RestartRecord contain no changed effort field under this proposal. Request in the queue is flow-ethos's message request, not signal-flow Query, so changing Start.LaunchProfile does not itself change message archives. If implementation adds an effort snapshot to RestartRecord or changes a nested rejection variant, recompute this closure; do not silently reuse old hashes.

Freeze previous representations, including string Effort and complete old nested LaunchAttempt anatomy. Predecessor declarations lacked any authored effort: proposed migration adds None. Previous launch profiles/intents (including queued OrderedLaunch) had concrete intent: losslessly map low/medium/high to Some; refuse unsupported strings with typed migration evidence, preserving original store. Cross-check legacy profile and intent consistency; preserve old disagreements as failures rather than repair them. Old receipts copied intent; upgrade requested value faithfully but mark native observation Unobserved, retaining native receipt digest. No retrospective claim of observation.

Use a preflight over all three families before committing an upgrade; mixed catalog states must be handled by the one explicit upgrade contract. Add all predecessor descriptors and registration/schema-identity paths, including open/reopen paths at `store.rs:2181,2672,2760,2782,2883,2919,3084,3136,5582,5618`. Older binaries fail closed on the new catalog. Prove atomicity/crash recovery with frozen real old-type fixtures on isolated stores: open launch phases, ambiguous receipt, queued launch, queued Refresh/Restart, active session with no launch history, unrelated queues, open tasks and reminders. Do not run migration against live memory for this brief.

## 5. Published consumer graph

`published-consumers.json` records exact remote main heads and every Cargo.lock under each enumerated active repository, plus energy-nexus/build-base/Home, read during this turn. Canonical checkout HEADs were not used. The scope is those repositories, not an assertion about arbitrary third-party consumers.

Actual present dependents: signal-flow61 -> flow-ethos0.54.3; meta77 -> signal61 + flow-ethos0.54.3; Flow0.54.7 -> signal61/meta77 and older signal60/meta76 test dependencies; energy-nexus cd4c85c0aa -> signal61/flow-ethos0.54.3. All other scanned active implementation/contract locks have no matching Flow packages. Preserve frozen prior-contract and before-request-id fixture crates rather than upgrading away compatibility test inputs. Energy is outside the provided active-project list despite being a real published consumer: Psyche kob2 explicitly authorizes its contract update in this coordinated change. Include energy-nexus and the new Curriculum repositories in the landing report for Psyche knowledge updates.

build-base cd61cac70a must take the new version/revision and deliberate plain/datom sets before dependent lock/Cargo.nix updates. Do not create redundant leaf builds by differing features or revision spellings. Every affected repository regenerates Cargo.nix/crate-hashes with the selected base and runs the remote immutable gate; latest generator/base readiness belongs to their owners.

Home e18aa72876: `modules/home/profiles/min/flow-0540.nix:34` reads owner `complex` input's `metaflows-0533.datom`; fallback `flow-nexus-config*/metaflows.datom` and replay fixtures also need the new arity where they target the new contract. Update the owner definition once and follow its pin in Home. Home flow-0540 input is currently 5d70c7b, but unconfigured-flow inputs still pin d3ab87ee; those are explicit old-version boundaries, not proof all consumers share the new version. CriomOS follows a pushed Home revision only in a separately authorized rollout. No source pin proves runtime activation.

## 6. Acceptance evidence and ordering

1. Apply Psyche kob2 rulings: missing intent -> None with provenance; Some/Unobserved allowed; Energy update included; existing text-edge cleanup a prerequisite. Astra still approves final observation anatomy and prerequisite boundary before those are implemented.
2. Canonical owner publishes leaf/generator prerequisite with verified import resolution and plain/datom anatomy; Flow implementation obtains scoped custody. No implementation until both hold.
3. Prove None/Some.Low/Some.Medium/Some.High datom/rkyv identity across all imports; reject unsupported shared variants. Prove exact ten-field Configure/readback and durable reopen. Preserve all unrelated declarations.
4. Adapter unit fixtures prove absent keys/flags for None and exact explicit values for all levels; native reported mismatch/conflict/malformed/unreported cases; all startup parts; restart same-session versus refresh next-flow; legacy/crash fixtures above. Rehearsal is command evidence only.
5. Publish only after immutable remote gate and independent review arranged by Astra, then dependent sets/pins in dependency order. This brief authorizes no live launch/activation.
6. A separately authorized isolated native test must bind address, native session/thread, model and turn to the exact requested option, command/JSON omission, native observation source and receipt digest. None remains None after reopen even if native reports high. Some verification reports whether actual effort was observed. Final readback distinguishes configured policy, emitted overrides, observed native facts and live identity; it never equates configuration/rehearsal with a native read receipt.

Request 5hnb remains open; Astra iefq directs design refinement and prerequisite preparation, with implementation waiting for canonical publication. Curriculum inventory flows/bb8a0a/role-policy-inventory.md confirms no Xhigh in current authored roles.datom, an explicit old Xhigh test at tests/claude_agent.rs216–227, old renderer/copied-schema boundaries and non-exhaustive host coverage. V1 rejects unsupported source rather than translating it. No automatic declaration/owner/store changes follow from this report.
