# 3 — stated actor mandate vs. actual code (and the intent backing)

Workflow dimension `explore:stated-mandate`, verified by adversarial thesis-2
(verdict **partial** — core correct; two superlatives trimmed).

## Headline

cloud's `ARCHITECTURE.md` §"Actor Shape" **is** a present-tense actor-per-concern
mandate — but it is **aspirational/stale** text, frozen since birth, contradicted by
the same file and by every line of cloud's actual code. Both runtimes contain zero
kameo / zero tokio / zero `impl Actor`. cloud's code follows
`skills/component-triad.md` (sync engine-trait substrate + the `1483`/`1487`
deferral) and violates `skills/actor-systems.md` (present-tense actor mandate +
"no shared locks"). **No cloud-topic Spirit record blesses sync OR mandates actors
at the concurrency level** — so §"Actor Shape" stands on no intent backing and is an
unblessed contradiction of `actor-systems.md`, while the sync code stands on the
workspace-level (non-cloud-tagged) deferral records.

## 1. §"Actor Shape" verbatim — and yes, it is a present-tense mandate

`ARCHITECTURE.md:30-41`:

> ## Actor Shape
> The first daemon should use one actor per concern:
> - `CloudflareProvider` for Cloudflare HTTP API calls;
> - `PlanStore` for prepared plans and approval state;
> - `PolicyStore` for account, credential-handle, capability, and zone policy;
> - `RateLimitGate` for provider rate-limit and retry state;
> - `RemoteOperationTracker` for asynchronous provider operations.
>
> Provider calls must not block the ordinary listener, owner listener, or plan
> store. Slow provider work belongs behind provider actors with timeouts.

It names five concrete actor nouns, one per concern, plus a non-blocking constraint
that is the exact shape of `actor-systems.md` §"Blocking is a design bug". The
"should use" framing is normative for "the first daemon," not a sketch of one
option. It is the cloud-local realization of "Actors all the way down."

## 2. Implemented? No — aspirational/stale

None of the five named actors and none of the non-blocking constraint exist in
either runtime:
- `cloud/Cargo.toml` has zero `kameo`, zero `tokio`, zero `sema-engine`.
- `grep -rE 'impl Actor|ActorRef' src/` and
  `grep -rE 'CloudflareProvider|PlanStore|PolicyStore|RateLimitGate|RemoteOperationTracker' src/`
  return **nothing** — none of the five types exist (the latter two appear only as
  concern-words inside the doc).

## 3. Internal contradiction inside cloud's own ARCHITECTURE.md

| Aspect | §"Actor Shape" (L30-41) | §"Schema-engine upgrade track" (L91-168) |
|---|---|---|
| Concurrency unit | one actor per concern (5 actors) | sync `SchemaRuntime` impl'ing `NexusEngine`+`SemaEngine` |
| State ownership | per-actor private state | shared `Arc<SchemaStore>` clones (L137-138) |
| Blocking discipline | "must not block … behind provider actors with timeouts" | `run_effect` a synchronous engine-trait method; IO inline on legacy path |
| Substrate | actors (implies kameo) | `schema-rust-next` emitter + `triad-runtime` `MultiListenerDaemon` |

The two sections describe two incompatible runtimes. §"Actor Shape" was **never
deleted or reconciled** when the schema-engine track landed. (Dimension 5 shows the
implementation-slice section even **dropped** its earlier actor language while
leaving the mandate header frozen.)

## 4. Which skill does cloud's code follow?

cloud follows **`skills/component-triad.md`** §"Runtime triad engine traits" — the
sync `SignalEngine`/`NexusEngine`/`SemaEngine` trait composition (Spirit
1326/1327/1330-1336) + the lifecycle-hooks deferral. `component-triad.md:1059-1066`
quotes Spirit `1487`: *"Generated Signal, Nexus, and SEMA engine traits should carry
minimal lifecycle hooks: on_start and on_stop … Full actor mailbox, backpressure,
and runtime-control traits stay deferred."* `:1087-1094` quotes Spirit `1483`:
*"Workspace explicitly defers backpressure handling, runtime control layer, inner
Nexus engine, actor scheduling/prioritization and related deeper-runtime work."*
cloud's `SchemaRuntime` is exactly that sync-trait-impl-on-a-data-bearing-noun.

cloud **violates `skills/actor-systems.md`**:
- L65 "Actors all the way down" — cloud has zero actors.
- L86-94 "the three default actor-shaped planes are Signal, Nexus, and SEMA" —
  cloud realizes these as sync engine traits.
- L290-321 "Blocking is a design bug" — legacy path blocks inline under a global
  mutex; the schema path's `run_effect` is a sync method.
- L354-372 "No shared locks — do not use `Arc<Mutex<T>>` as the ownership model" —
  `daemon.rs:24` is exactly `Arc<Mutex<Store>>`; the schema path uses
  `Arc<SchemaStore>`.
- L556-561 "Runtime roots are actors" — cloud's roots are `Daemon`/
  `MultiListenerDaemon`, neither an actor.

## 5. Cloud-specific Spirit records — none blesses sync, none mandates actors

Queried `spirit "(Observe (Records ((Partial [cloud]) None Any Any
WithProvenance)))"` — 58 cloud-topic records. **None addresses thread-vs-actor or
actor-per-concern at the concurrency level.** The records that govern cloud RUNTIME
SHAPE speak only to STACK choice and contract layout, and point toward the sync
stacks:

- **`12mi`** (Decision High, 2026-05-27): "Cloud component implementation should use
  the existing old NOTA / old signal macro stack … rather than waiting for the new
  schema stack." — picks the sync `signal_channel!` stack.
- **`6k8k`** (Constraint High, 2026-05-25): "Cloud component production slice uses
  old Rust signal macro path."
- **`wdri`** (Decision High, 2026-05-25): "Cloud production push prioritized; first
  MVP can skip new schema-engine approach to ship faster."
- **`ey5p`** (Decision Maximum, 2026-06-04): "The cloud component upgrade should move
  onto the new schema-interface and triad-engine approach, with next carrying the
  breaking design path and main the operator integration path." — moves to the
  (still sync) schema-engine track.
- **`vnnx`** (Decision High, 2026-06-04): "The schema-derived cloud port uses TWO
  schemas … each emitting its own Signal Nexus SEMA engines and sharing record
  types, with the cloud runtime crate importing both and running two listeners …
  two listener actors …" — **the only record using "actors," and it means the two
  LISTENER actors of the two-authority-tier triad shape (the engine-trait listener
  composition), NOT the five provider/plan/policy concern-actors of §"Actor Shape".**
  It mandates the two-contract/two-socket split, not kameo or actor-per-concern.
- **`m3eg`/`g055`/`p83x`** (Principles): "Cloud daemon starts almost-stateless;
  caches last-known-state … cache loss acceptable"; "First cloud cache is
  runtime/volatile (in-memory); persistent storage deferred." — explains the
  in-memory store; no actor implication.

**Verdict:** no cloud record blesses sync at the concurrency level, and none
mandates actors. The cloud corpus is about (a) stack choice
(`12mi`/`6k8k`/`wdri`/`ey5p`), (b) the two-contract split + two listeners (`vnnx`),
(c) Cloudflare-DNS-first scope, (d) credential/gopass/flarectl mechanics. The
thread-vs-actor question is governed only at the WORKSPACE level by the records the
prior forensic established — SHAPE intent `2alg`/`k6w1`/`tj99`, sync-substrate
deferral `1483`/`1487`(=`czw0`), no-compat fence `ax2k` — **none cloud-tagged**. So
§"Actor Shape" has no intent backing.

## Thesis-2 corrections (verified)

- The digest's "written in the first commit ba35849 … only ba35849" provenance is
  **imprecise**: the pickaxe returns TWO birth commits (`ba35849` AND `db5dc5c`,
  both 2026-05-23). Substance (frozen since birth, never reconciled) survives.
- "the workspace's MOST explicit unfulfilled actor mandate" is an **unverified
  superlative** — cloud's is *a* maximally-concrete unfulfilled mandate (five named
  actors + a timeout clause), but report-35 showed the zero-actor property is
  workspace-wide, so "most explicit" was not ranked here. (Completeness MISS-1
  reframes this decisively — see file 7.)
