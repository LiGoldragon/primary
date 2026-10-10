# 0 — frame and method

cloud-designer, 2026-06-07. Meta-report directory for a focused explore/research
audit of the **cloud** repo on the actor-model divergence. This zooms the
workspace-wide forensic (`reports/cloud-designer/35-actor-divergence-forensics/`)
down onto cloud-designer's home repo, where the divergence is at its sharpest.

## The question

The psyche, continuing the actor-divergence thread: *"let's go back to cloud — do
an explore/research audit on the subject."* The subject = how the actor-model
divergence (sync stack, zero kameo, vs. "we only build actor model systems")
manifests **specifically in the cloud repo**, and what that implies.

## Why cloud is the sharpest instance

cloud's own `ARCHITECTURE.md` carries the **most explicit actor-per-concern
mandate in the workspace** — a whole §"Actor Shape" naming `CloudflareProvider`,
`PlanStore`, `PolicyStore`, `RateLimitGate`, `RemoteOperationTracker` as one actor
per concern, plus the hard rule *"Provider calls must not block the ordinary
listener … behind provider actors with timeouts."* Yet (established inline before
the audit):

- cloud's `Cargo.toml` has **zero kameo / zero tokio** (it pulls `triad-runtime` +
  `schema-rust-next`).
- cloud runs **two** synchronous runtimes: a **legacy production runtime**
  (`src/daemon.rs`, `thread::spawn`-per-listener over a single global
  `Arc<Mutex<Store>>`) that `cloud-daemon` actually runs and that does the live
  Cloudflare IO; and a **schema-engine triad path** (emitted `src/schema/daemon.rs`
  + `src/schema_runtime.rs` + `src/schema_daemon.rs`) that is build-verified and
  socket-tested but not yet wired to live Cloudflare IO — cutover pending.

So cloud is a repo whose own architecture doc mandates actors-per-concern with an
explicit no-blocking-the-listener rule, while shipping a sync, mutex-serialized,
actorless runtime that makes blocking Cloudflare calls. That is the divergence in
its most concentrated form.

## Method

Hybrid: inline scouting (repo layout, the three daemon files, the global-mutex
threading shape, Cargo deps) to scope the work-list, then a background research
workflow (`wwudq57zz`, ultracode) fanning out six parallel explorer dimensions,
then an adversarial verification pass.

Six explorer dimensions (each reads the actual source, cites file:line):

1. **legacy-production-runtime** — `cloud-daemon` → `daemon.rs` → `Store` → provider
   client. Threading, locking spans, the live Cloudflare IO path.
2. **schema-triad-runtime** — emitted `schema/daemon.rs`, `schema_runtime.rs`,
   `schema_daemon.rs`, `schema_store.rs`, `build.rs`, `schema/*.schema`. The sync
   engine-trait spine, store sharing, where IO would plug in.
3. **stated-actor-mandate** — cloud's `ARCHITECTURE.md` §Actor Shape vs its own
   schema-engine track; `INTENT.md`/`AGENTS.md`; `actor-systems.md` vs
   `component-triad.md`; cloud-topic Spirit records.
4. **provider-blocking-hazard** — does a slow/hung Cloudflare call block the
   listener / serialize connections / hold the Store mutex, violating cloud's own
   no-block rule? The concrete actor-model payoff for cloud.
5. **two-runtime-cutover-history** — git/jj timeline; was an actor cloud ever
   built and removed, or always aspirational; the cutover plan; deferred items.
6. **triad-substrate-inheritance** — is cloud's sync-ness *inherited* from
   `triad-runtime` + the emitter (so cloud can't be actor-native alone), or could
   cloud host kameo provider actors behind the triad listener? Ties to report 35.

Verification: four adversarial skeptics, each tasked to **refute** a load-bearing
thesis (total actorlessness; the Actor-Shape-never-built claim; the blocking-hazard
violation; the substrate-inheritance claim), re-reading the source rather than
trusting the digest — plus a completeness critic. The deliberate self-refutation
pass exists because the report-34/report-35 swings showed this investigator
over-claims from partial evidence.

## Outputs

Numbered dimension reports land here as `1`..`6`; the verification/completeness
findings fold into the synthesis. The orchestrator's synthesis is the
highest-numbered file (`7-overview.md`).
