# Frame — schema-deep iteration 2 (Nexus mail keeper + sema-engine)

*Meta-report orchestrator's frame. Psyche directive 2026-05-27 (Spirit records 971 Decision Maximum + 972 Principle Maximum + 973 Principle Maximum + 974 Constraint Maximum, with 980 as redundant follow-on capture from this lane): mine intent and recent reports and prototypes for working solutions; implement a fully-working prototype that uses all designed components fully; audit it against component-fullness; let the audit drive component development. The lojix/criomos/horizon rewrite is the explicit target per 974. This iteration extends the `/35` schema-deep pilot to wire in the components `/35` left in-mem or bypassed.*

## Psyche intent — the prototype-iteration discipline

Five Spirit records bear directly on this work:

- **971** (Decision Maximum) — mine recent intent + reports + prototypes for working solutions, then implement a fully-working prototype rather than another design-only pass.
- **972** (Principle Maximum) — the prototype must be audited against whether it uses all designed components fully: **NOTA structure, schema macro lowering, assembled schema, Rust emission, generated signal, Nexus mail keeper, SEMA state handling, and Spirit runtime behavior**. This is the 8-component fullness criterion.
- **973** (Principle Maximum) — audit findings feed implementation directly; each critique identifies missing designed components and the next pass develops those components further instead of accepting a partial mock.
- **974** (Constraint Maximum) — prototype audits for the CriomOS/Lojix/Horizon rewrite must require the prototype to use the designed components fully; when a designed component is too incomplete to use, the prototype work should DEVELOP THAT COMPONENT FURTHER rather than bypass it.
- **980** (Principle Maximum, captured by this lane) — redundant follow-on capture of the same methodology principle in different framing. Should have queried Spirit first per AGENTS.md "EXCEPTION + REFINEMENT" gap-check; left standing as alternate framing, not deleted per intent-maintenance (psyche-only supersession).

## What the mining surfaced

The mining pass (designer/389-395, operator/210-218, spirit records 894-980) surfaced:

- **`/392-vision-schema-driven-stack-canonical`** is THE workspace vision. Schema is the source of truth for every data type; everything else implements traits on schema-emitted nouns. The runtime triad is **Signal / Nexus / SEMA** (per record 964; Executor renamed to Nexus). Three schema types correspond to three runtime planes, all schema-driven.
- **`/35-schema-deep-new-logics`** (this lane's prior iteration, shipped earlier today) is the working precedent at the lojix-component scale: 28 schema-emitted typed nouns in one `schema/lojix.schema`, 9-actor Kameo topology, 10/10 tests green on commit `rnwxqrlzmrmm` pushed to `origin/schema-deep`. But it used the legacy "Executor" terminology, an in-memory Store, no real sema-engine backing, no Nexus-as-mail-keeper, no Communicate trait, no DatabaseMarker.
- **Workspace direction has refined** under `/35`: records 963-970 named the SIGNAL PROTOCOL, defined Nexus as the mail keeper ("when Nexus has the mail, the mail is in the BEING-PROCESSED state"), specified message lifecycle hooks (method-on-message-sent), and made Nexus the runtime mail keeper between Signal ingress and SEMA state handling.
- **Substrate state**: nota-next + schema-next + schema-rust-next are landed and moving forward; spirit-next is the working pilot for the schema-derived runtime triad at spirit-component scale. The signal-frame schema-derived rewrite is **not yet started** (per `/390`). The Nexus mail keeper component does not exist as a primitive in any repo. sema-engine exists as a separate crate but is not consumed by `/35`'s in-mem Store.

## What this iteration extends

`/35` is the baseline. This iteration extends the same pilot on the same branch with the next-most-load-bearing missing components from the 8-component fullness criterion:

1. **Rename Executor → Nexus** throughout `/35` (per record 964). Naming alignment.
2. **Reshape `OperationDispatcher` into the Nexus mail keeper** per records 966-970. When Nexus holds a message, it's in BEING-PROCESSED state. Add lifecycle hooks (sent / queued / processing / replied) per records 960-963. Each `Input` becomes mail that Nexus tracks; reply path returns through Nexus with a DatabaseMarker.
3. **Replace in-memory `Store` actor with sema-engine** (records 948-949). Real single-writer durable state. Schema-emitted `SemaCommand` / `SemaResponse` still carry the in-process protocol; sema-engine carries the rkyv-on-redb persistence.
4. **Add `Communicate` trait** (record 935). Abstract wire interface used by CLI and daemon. Concrete impl is Unix socket (per current `/35`). The trait lives in signal-frame or schema-rust-next; the schema-emitted Input/Output types implement it.
5. **Add `DatabaseMarker` reply payload** (record 935): hash (Blake3 of SEMA state at this transaction) + counter (monotonic). Declare in `schema/lojix.schema` as a payload field in every reply enum variant.
6. **Develop missing substrate where it blocks the prototype** per record 974. If signal-frame's schema-derived rewrite is too incomplete, start it. If sema-engine lacks the surface needed, extend it. If a Nexus-mail-keeper primitive needs to live in a shared crate (proposed name in `/390`: `persona-mail`), the subagent picks the right home and surfaces the decision.
7. **Update per-repo INTENT.md/ARCHITECTURE.md** per record 944's continuous-manifestation discipline as relevant.
8. **All `/35` tests still pass + new tests** for Nexus mail mechanism + sema-engine integration + Communicate trait + DatabaseMarker.

The full per-component mapping with rationale lives in `1-prototype-target-and-component-mapping.md`.

## Method

Three threads:

1. **Mine** — done this turn (the §"What the mining surfaced" section above).
2. **Dispatch subagent in background** — non-blocking per hard override; subagent extends `/35` on the same `schema-deep` branch with the iteration above. Subagent inherits this system-designer lane per record 920 (no `-assistant` lane created; subagent reports land in `reports/system-designer/`). Brief in §"Subagent dispatch brief" below.
3. **Audit + synthesise on return** — the audit applies the 8-component fullness criterion (record 972); each gap derives a component-development task for iteration 3 per record 973. The audit + synthesis lands as `N-overview.md`.

## What lives where in this directory

- `0-frame-and-method.md` — this file. Orchestrator's frame, mining summary, method, dispatch brief.
- `1-prototype-target-and-component-mapping.md` — per-component mapping of `/35` state against `/392`'s 8-component fullness criterion + the specific extensions this iteration targets.
- `2-...md` — slot reserved for the subagent's implementation report.
- `N-overview.md` — slot reserved for orchestrator's audit + component-development queue for iteration 3.

## Subagent dispatch brief

*Verbatim. This is what the subagent reads as its complete instruction set.*

### You are a designer subagent

You are a designer-class subagent dispatched by the system-designer lane (per record 920 you INHERIT this lane and lock; do NOT create a `-assistant` lane; subagent reports land in `reports/system-designer/`). Your task is iteration 2 of the schema-deep lojix-horizon pilot: extend the `/35` pilot to use more of the workspace's designed components fully, and develop those components further where they're too incomplete to use. Take this seriously — per psyche records 971-974, partial mocks are the failure mode this exercise is trying to eliminate.

### Required reading, in this order

1. `/home/li/primary/AGENTS.md` — workspace compact contract. Note the new rust-skill hard override (intent 884) mandates reading skills/rust-discipline.md before authoring Rust. Note record 944 mandates per-repo INTENT.md + ARCHITECTURE.md manifestation as part of work.
2. `/home/li/primary/skills/rust-discipline.md` + linked sub-skills (`skills/rust/methods.md`, `skills/rust/errors.md`, `skills/rust/storage-and-wire.md`, `skills/rust/parsers.md`, `skills/rust/crate-layout.md`).
3. `/home/li/primary/skills/abstractions.md` (verb belongs to noun) + `skills/actor-systems.md` (deep actor topology + Nexus-as-mail-keeper shape) + `skills/component-triad.md` §"Runtime triad" (Signal/Nexus/SEMA per record 964) + `skills/kameo.md`.
4. `/home/li/primary/skills/feature-development.md` (worktree pattern) + `skills/jj.md` (headless jj — every description-taking command passes `-m` inline).
5. `/home/li/primary/skills/repo-intent.md` + `skills/architecture-editor.md` for the per-repo continuous-manifestation discipline (record 944).
6. `/home/li/primary/reports/system-designer/35-schema-deep-new-logics/2-schema-deep-lojix-next-pilot.md` — your baseline. Your iteration extends this code.
7. `/home/li/primary/reports/system-designer/35-schema-deep-new-logics/3-overview.md` — orchestrator's synthesis of the baseline; names what's NOT delivered.
8. `/home/li/primary/reports/designer/392-vision-schema-driven-stack-canonical-2026-05-27.md` — THE workspace vision. The 8-component fullness criterion comes from §"Where the work actually lives" + records 963-965 + 972.
9. `/home/li/primary/reports/designer/390-wire-runtime-canonical-direction.md` — Communicate trait + signal-frame schema-derived rewrite + mail state manager + DatabaseMarker design.
10. `/home/li/primary/reports/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/1-prototype-target-and-component-mapping.md` — this directory's per-component target mapping.
11. Repos: `/git/github.com/LiGoldragon/{sema-engine,signal-frame,nexus,schema-next,schema-rust-next,nota-next,spirit-next}` — read their `INTENT.md`, `ARCHITECTURE.md`, current state. Note: the `nexus` repo PREDATES the Nexus-runtime-plane terminology — it is the "typed semantic text vocabulary written in NOTA syntax" per `protocols/active-repositories.md`. Do NOT put Nexus-mail-keeper code into the existing `nexus` repo without checking; the right home is likely inside lojix-next (in-process plane) OR a new `persona-mail` crate (substrate plane) per `/390` §"Mail state manager". You decide.

### Worktree

Continue on the existing `/35` worktree + branch:

```sh
cd ~/wt/github.com/LiGoldragon/lojix/schema-deep
# you are extending; do not delete /35's commits
```

If you need to extend other repos (signal-frame, sema-engine, nota-next, schema-next, schema-rust-next), create per-repo worktree branches under `~/wt/github.com/LiGoldragon/<repo>/schema-deep-iteration-2/` per `skills/feature-development.md` §"Multi-repo arc coordination". Same branch name across repos when the arc spans multiple.

Claim before editing:

```sh
tools/orchestrate claim system-designer '[draft:schema-deep-iteration-2-nexus-sema-2026-05-27]' ~/wt/github.com/LiGoldragon/lojix/schema-deep -- 'iteration 2: nexus mail keeper + sema-engine + Communicate + DatabaseMarker'
```

(System-designer claim per inheritance from dispatcher per record 920.)

### What to build — the deliverable (per `1-prototype-target-and-component-mapping.md`)

Extending `/35` schema-deep pilot on branch `schema-deep`:

1. **Rename Executor → Nexus** throughout the codebase (per record 964). Module names, type names, doc comments, test names. `Engine::handle` becomes `Nexus::handle` or `Engine` becomes the runtime-root and `Nexus` is the mail-keeper actor. ARCHITECTURE.md updated.
2. **Build the Nexus mail keeper** per records 966-970. Concrete shape:
   - `NexusMailKeeper` actor (or whatever name fits the noun) owns the message lifecycle.
   - Each incoming `Input` becomes a `MailEntry` with typed lifecycle state: `Sent` → `Queued` → `Processing` → `Replied` (or `Failed`).
   - Hookable events per records 960-963: actors can attach to `MessageSent`, `MessageQueued`, `MessageProcessing`, `MessageReplied`. Hooks fire synchronously inside the actor handler (push, not poll, per `skills/push-not-pull.md`).
   - The `MailEntry` carries a unique correlation ID + the schema-emitted `Input` payload.
   - When SEMA processing completes, NexusMailKeeper marks the entry `Replied` and returns the `Output` via the original reply channel.
3. **Wire sema-engine for real durable SEMA**. Replace `/35`'s `Store` actor's in-memory `Vec<...>` with sema-engine's redb-backed `Database`. The schema-emitted `SemaCommand` lowers to sema-engine operation calls; the schema-emitted `SemaResponse` is constructed from sema-engine results. The Store actor's State becomes the sema-engine handle + the connection pool / kernel surface.
4. **Add `Communicate` trait** in `signal-frame` (or wherever the abstract wire interface naturally lives — your call, document the decision):
   ```rust
   pub trait Communicate {
       type Input;
       type Output;
       type TransportError;
       async fn send_request(&mut self, input: Self::Input) -> Result<Self::Output, Self::TransportError>;
   }
   ```
   Concrete impl: `UnixSocketCommunicate` carrying `tokio::net::UnixStream` and using the schema-emitted Input/Output encode/decode methods.
5. **Add `DatabaseMarker` to `schema/lojix.schema`** as a namespace record:
   ```
   DatabaseMarker [TransactionCounter StateHash]
   TransactionCounter [Integer]
   StateHash [Text]  ; Blake3 hash of SEMA state at this transaction, hex-encoded for now
   ```
   Add as a field on every Output reply variant. NexusMailKeeper populates it from sema-engine's transaction state.
6. **Per record 974, develop substrate further if blocked**:
   - If sema-engine's surface doesn't expose what NexusMailKeeper needs (e.g. transaction-counter, state-hash hook), extend sema-engine on its own feature branch `schema-deep-iteration-2` and import the extension in lojix-next.
   - If signal-frame's schema-derived rewrite is too incomplete to host `Communicate`, decide: start the schema-derived rewrite on signal-frame's `schema-deep-iteration-2` branch, OR put `Communicate` in schema-rust-next and migrate later. Document your decision.
   - If Nexus-mail-keeper primitive should be a shared crate (`persona-mail` per `/390` §"Mail state manager"), create the crate; if it should stay inside lojix-next for this iteration, document that and surface the cross-component promotion as iteration-3 work.
7. **Per record 944, update per-repo INTENT.md + ARCHITECTURE.md** in every repo you edit. Each repo's INTENT carries the psyche intent it serves; ARCHITECTURE carries the structural shape. Continuous manifestation, not deferred pass.

### Tests — the deliverable's witness

All `/35` tests still pass + new ones:

11. `lojix_next_nexus_is_mail_keeper` — assert NexusMailKeeper holds a `MailEntry` while SEMA is processing; assert lifecycle transitions Sent → Queued → Processing → Replied.
12. `lojix_next_message_lifecycle_hooks_fire` — attach a test hook to `MessageSent`; send an Input; assert hook fired with the right correlation ID.
13. `lojix_next_sema_engine_durable_across_restart` — write a `RecordPlan` SemaCommand; stop the daemon; restart; verify the GenerationRecord is still in the sema-engine redb. Spawn-and-drive test.
14. `lojix_next_communicate_trait_round_trip` — `UnixSocketCommunicate` does a full Input → Output round trip via the trait.
15. `lojix_next_database_marker_in_every_reply` — every Output variant carries a DatabaseMarker; the marker's transaction-counter monotonically increases across operations.
16. `lojix_next_database_marker_state_hash_changes_on_write` — write operations change the StateHash; read operations leave it stable.

`nix flake check` must pass with all 16 tests + the architectural-truth checks (`no_free_functions`, `no_zst_actors`, `actor-mailboxes-schema-emitted`, etc.).

### Hard rules (every keystroke — restated from `/35` brief)

- **No free functions** outside `fn main()` / `#[cfg(test)]`. Methods on non-ZST data-bearing types or trait impls only.
- **Schema-emitted types are the nouns.** Hand-write methods on emitted types. No parallel mirrors.
- **Single argument rule** for binaries.
- **No ZST actors.** Every Kameo actor's State carries data.
- **No string typification.** Domain values are typed newtypes.
- **Typed `Error` enum per crate** via thiserror; no anyhow/eyre at boundaries.
- **NOTA strings come EXCLUSIVELY from bracket forms.** Never emit `"`.
- **Headless jj.** Every description-taking `jj` command passes `-m` inline. NEVER let jj open `$EDITOR`.
- **Designer lanes do not push to main.** Per-repo feature branches under `~/wt/`.
- **Sub-sub-agent dispatches** (if any) MUST be `run_in_background: true`.

### Reporting back

When you finish (or hit a hard blocker), write your implementation report at:

```
/home/li/primary/reports/system-designer/37-prototype-schema-deep-iteration-2-nexus-mail-sema-engine-2026-05-27/2-<descriptive-name>.md
```

Include:
- Per-file structure + line counts (extend `/35/2`'s table).
- Per-test pass/fail with output excerpts for failures.
- For each of the 8 components in `/392`'s fullness criterion, score 0-1 on how-fully-used WITH evidence (file path + line number anchoring the use).
- Component-development work you did in substrate repos (sema-engine, signal-frame, etc.) — what you extended, why.
- Architectural decisions the brief didn't pin (Nexus-mail-keeper home, Communicate trait location, etc.).
- Any new Spirit Clarifications you captured (record YOUR clarifications back to psyche; do NOT re-capture 971-974 + 980).
- What's STILL bypassed or partial — feeds iteration 3's pickup queue.

If you can't make progress on a particular sub-deliverable, REPORT THE BLOCKER. Don't ship half-implementations as if they work — that's exactly what 974 is trying to fix.

### Don't do these things

- Don't push to `main` of any repo. Designer lanes don't push to main.
- Don't delete `/35`'s commits on the `schema-deep` branch.
- Don't put Nexus-mail-keeper code into the existing `nexus` repo without checking — name collision (existing `nexus` is "typed semantic text vocabulary," not the runtime plane).
- Don't capture redundant Spirit records (971-974 + 980 already cover the methodology).
- Don't modify workspace-level guidance files (`AGENTS.md`, `ESSENCE.md`, workspace `INTENT.md`); per-repo INTENT.md and ARCHITECTURE.md are fair game per record 944.
- Don't `cat`/`head`/`tail`/`sed`/`awk` when Read/Edit fit.
- Don't search `/nix/store`.

### Closing

This is iteration 2 of a working precedent (`/35` shipped earlier today). The pilot proves the schema-derived stack works at lojix-component scale; your iteration extends it to use more of the workspace's designed components fully, per the 8-component fullness criterion (record 972). When a component is too incomplete to use, develop it further (record 974) — don't bypass.

Take the depth seriously. Begin by reading the brief at `0-frame-and-method.md` + `1-prototype-target-and-component-mapping.md`.

## Risks + open questions for orchestrator-level decision

- **Nexus-mail-keeper home** — inside lojix-next (in-process plane) vs new `persona-mail` crate (substrate plane). Subagent will decide and surface; the right answer depends on whether it's reusable across other components (likely yes, but not blocking this iteration).
- **Communicate trait home** — `signal-frame` vs `schema-rust-next` vs new abstract crate. `/390` §"Open questions" item 1 names the tradeoff; subagent makes a working choice.
- **sema-engine API gaps** — if sema-engine doesn't expose transaction-counter or state-hash hooks needed for DatabaseMarker, subagent extends sema-engine. That extension is operator-owned crate; designer-class extension on a feature branch is fine per double-implementation-strategy.
- **signal-frame schema-derived rewrite** — full rewrite is `/390`'s deferred substantial work. Subagent may NOT need to do the full rewrite to land Communicate trait + iteration-2 goals; document the boundary.
- **Settings hook caveat from `/35`** — still applies if the psyche hasn't opened `/hooks` since `/35` shipped; the AGENTS.md hard override fires for all harnesses regardless.
- **Naming collision** between existing `nexus` repo and runtime-plane Nexus — surfaced for psyche awareness; doesn't block this iteration but needs resolution at some point (rename existing nexus? prefix new component as `persona-nexus`? subagent surfaces in `2-...md`).
