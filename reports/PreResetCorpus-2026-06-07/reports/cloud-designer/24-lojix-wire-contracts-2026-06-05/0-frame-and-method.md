# lojix triad port — Phase 1: the two wire contracts

Cloud-designer lane. 2026-06-05. **Meta-report directory.** This is the first
implementation phase of the lojix triad port decided in report 23. The psyche
chose to drive the port end-to-end via subagent workflows, phase by phase, with
orchestrator review between phases. Phase 1 authors the foundational wire
contracts everything else builds on.

## Decisions driving this phase (from report 23 + this session)

- **Two-contract split** (`11yimmwp4pueiudhl30`): ordinary `signal-lojix`
  (Query + the Watch subscriptions) and owner-only policy `meta-signal-lojix`
  (Deploy / Pin / Unpin / Retire). Born **meta-signal-lojix**, never
  owner-signal-. `meta-signal-lojix` carried as a path-dep package now, repo at
  cutover.
- **Streaming day-one** (`2tfa`): `signal-lojix` carries `WatchDeployments` +
  `WatchCacheRetention` streaming subscriptions from the start. lojix is the
  first component to prove schema-derived stream emission; if the generator
  can't yet emit streams, that enhancement is on the lojix path — not a reason
  to drop streaming.
- **Local builds permitted** (`783n`): the lean daemon's local-build rejection
  was a hallucinated guard, never psyche intent — drop it. prometheus must
  build its own model-heavy closures locally.
- **Port-first sequencing** (`1cfsmclkytl551wt5hn`): finish the triad port
  before cutover.
- Wire-only contracts, no engine traits; per-plane daemon schemas come in a
  later phase. Plane-schema shape: `29w2hwko8d7mr2jh943`.

## Templates and sources

- Cloud ordinary contract: `/git/github.com/LiGoldragon/signal-cloud/schema/lib.schema`.
- Cloud policy contract: `/git/github.com/LiGoldragon/meta-signal-cloud/schema/lib.schema`.
- Cloud daemon planes (later-phase reference): `/git/github.com/LiGoldragon/cloud/schema/{nexus,sema}.schema`.
- The lojix prototype (domain vocabulary to salvage):
  `/home/li/wt/github.com/LiGoldragon/lojix/schema-deep-iteration-2/schema/lojix.schema`.
- The stale contract spec to re-target: `/git/github.com/LiGoldragon/signal-lojix/ARCHITECTURE.md`.
- The legacy deploy surface the daemon must cover:
  `/git/github.com/LiGoldragon/lojix-cli/src/{request,reply,build}.rs`.

## Method — probe + draft + review

A background workflow drafts into `drafts/` for orchestrator review BEFORE
anything lands on a `next` branch:

- **Probe** — is schema-next/schema-rust-next able to emit streaming
  subscriptions today? Find any `.schema` that declares streams; read the
  emission targets. Determines whether streaming day-one needs a schema-next
  enhancement first.
- **Draft (ordinary)** — `signal-lojix/schema/lib.schema`: Query + the two
  Watch subscriptions + Unwatch, reply variants, event variants, stream
  relations — following the cloud `lib.schema` shape, NOTA-legal.
- **Draft (meta)** — `meta-signal-lojix/schema/lib.schema`: Deploy / Pin /
  Unpin / Retire + typed rejection replies, sharing record types with the
  ordinary contract.
- **Draft (architecture)** — re-targeted `signal-lojix/ARCHITECTURE.md`:
  delete the three-layer section, re-target to schema-derived per-plane +
  two-contract split + streaming day-one, with a Migration-history note.
- **Review** — adversarial check against component-triad rules, NOTA legality,
  the cloud template, and the decisions above.

Drafts land in `drafts/`; the review in `1-review.md`; the orchestrator then
reviews, places the schemas into `next`-branch worktrees, and commits. The
real artifact is the schema files on the contract repos' `next` branches.
