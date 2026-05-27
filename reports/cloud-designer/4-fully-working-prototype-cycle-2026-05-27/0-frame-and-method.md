# 0 · Frame and method — cloud fully-working prototype cycle

Session-spawning prompt (psyche, 2026-05-27): *"mine intent and
recent reports and prototypes for working solutions and implement
a fully-working prototype - then audit it with a critique that
it must use all designed components fully, therefore developping
them further each time"*.

Captured as spirit record 979 (Principle, High): the cycle is
**mine → implement → audit → grow underlying components**. Each
iteration grows the prototype's completeness AND the components
the prototype needs to use fully — component development is
co-developed through prototype use, not as separate work.

## The cycle, made explicit

1. **Mine** Spirit records + reports + existing code for what's
   already been designed, decided, or built that the prototype
   should honor or reuse.
2. **Synthesize** the minimum surface a "fully-working"
   prototype must exercise — typed as a completeness checklist.
3. **Implement** that surface on the existing
   `designer-cloudflare-cli-prototype-2026-05-27` worktree.
4. **Audit** the implementation against the full designed
   surface: per component, is it used? used fully? what's the
   gap?
5. **Grow** the underlying components to close audit gaps that
   point upstream (e.g. missing `RecordIdentifier` in
   `signal-cloud`).
6. (Future) Re-audit; repeat from step 3 until the prototype
   exercises 100% of designed surfaces — at which point the
   designed surface itself is what needs growing next.

This pass executes 1→5 once. Step 6 is by design out of scope
for a single session.

## Subagent fanout — three parallel mining scouts

Per designer protocol exception (intent 539 + designer
authorization 2026-05-21), parallel subagent dispatch is the
default for designer work. Three scouts, each writing into this
meta-report directory:

- **Scout 1 — Spirit substance for full implementation.** Reads
  every cloud-relevant Spirit record (cloud topic + related
  topics like deploy, persona, component-shape that touch cloud)
  and extracts: (a) hard constraints the prototype must satisfy;
  (b) settled design decisions the prototype must implement; (c)
  open questions to leave at typed-rejection boundaries; (d)
  *anti-patterns* the prototype must avoid. Output:
  `1-spirit-substance-for-full-implementation.md`.

- **Scout 2 — Report mining for working solutions.** Sweeps the
  13 settled-design reports identified in
  `reports/cloud-designer/2-cloud-component-design-recap-2026-05-27/`
  (system-operator/156-160, second-designer/196,
  third-designer/22, 23, 25 subdirectories) and extracts the
  concrete shapes the prototype must adopt — actor topology,
  operation routing, dispatcher patterns, state-machine
  semantics, identity primitives, etc. Output:
  `2-reports-working-solutions.md`.

- **Scout 3 — Code survey for what's already built.** Maps the
  existing surface in `/git/github.com/LiGoldragon/cloud/` and
  the worktree at
  `/home/li/wt/github.com/LiGoldragon/cloud/designer-cloudflare-cli-prototype-2026-05-27/`,
  plus `signal-cloud` and `owner-signal-cloud` contracts. Catalogs
  every operation variant, reply variant, handler stub, and
  identifies which paths are already wired vs. stubbed vs.
  missing. Output: `3-code-survey.md`.

## Synthesis + implementation + audit + growth

After the three scouts return, the orchestrator (this agent)
performs steps 2→5:

- `4-completeness-checklist.md` — synthesizes mining into a
  per-operation, per-reply, per-component checklist for "fully
  working".
- `5-implementation.md` — what was changed on the worktree, with
  commit references and test coverage.
- `6-audit.md` — critique of the implementation against the
  full designed surface; gap list with each gap classified as
  (prototype-fix) or (component-growth).
- `7-component-growth.md` — changes made to underlying components
  (e.g. signal-cloud) in this pass to close audit gaps.
- `8-overview.md` — synthesis the psyche reads, with next-cycle
  pointers.

## Out of scope this pass

- Live Cloudflare auth + real-world DNS mutation. The
  CapturingRunner mock pattern stays the verification surface
  for this cycle; live integration is a separate cycle.
- Schema-engine cutover — psyche 914 holds the cloud component
  on the old NOTA stack for this push.
- Redirect-rules mutation — flarectl can't, and the prototype
  reflects that finding via typed `RequestUnsupported` replies.
- Other providers (Google Cloud, Hetzner) — Cloudflare-first
  per psyche 282/685.
