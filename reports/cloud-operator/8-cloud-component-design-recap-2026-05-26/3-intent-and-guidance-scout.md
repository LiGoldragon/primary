# Code Context

## Files Retrieved

1. `ESSENCE.md` (lines 1-80) - intent precedence and intent/design readiness rule.
2. `ESSENCE.md` (lines 137-220) - bounded-domain quality priorities, no speed-first design, naming, and clean-break principle.
3. `INTENT.md` (lines 137-184) - deploy-stack and worktree constraints around production vs rewrite work.
4. `INTENT.md` (lines 203-300) - NOTA payload rule, raw component-first rule, schema-driven stack, rkyv-as-sema-and-signal, NEXT/MAIN vocabulary.
5. `skills/component-triad.md` (lines 1-44) - repo triad shape and contract/runtime split.
6. `skills/component-triad.md` (lines 136-165) - vocabulary: component triad, working signal, policy signal, signal tree, policy/working state.
7. `skills/component-triad.md` (lines 173-202) - CLI invariant and daemon signal-frame boundary.
8. `skills/component-triad.md` (lines 204-296) - verb layers, Sema classes, authority tiers, owner-signal naming caveat.
9. `skills/component-triad.md` (lines 298-418) - policy/working state split, bootstrap-once, witness tests, single-argument and Help operations.
10. `skills/component-triad.md` (lines 526-555) - commit-first-success and record-divergence partial-failure semantics.
11. `skills/component-triad.md` (lines 589-634) - runtime triad: Signal / Executor / SEMA.
12. `skills/context-maintenance.md` (lines 1-144) - recap as context-maintenance: inventory, categorize, preserve load-bearing design rationale.
13. `skills/spirit-cli.md` (lines 132-177) - Spirit observe query syntax used for read-only record retrieval.
14. `AGENTS.md` (lines 157-188) - hard overrides for component triad and NOTA single-argument/bracket-string rules.
15. `AGENTS.md` (lines 190-230) - Rust discipline and method-only rule, if cloud design turns into implementation.
16. `skills/system-operator.md` (lines 119-123) - secret-handling warning: secrets stay out of Nix and broad process environments.
17. `reports/cloud-operator/8-cloud-component-design-recap-2026-05-26/0-frame-and-method.md` (lines 1-27) - parent frame and expected scout artifact.

Spirit observe queries used:

- `spirit "(Observe Topics)"`
- Topic records with provenance for `cloud`, `domain-criome`, `domain`, `criome`, `component-triad`, `component-shape`, `signal`, `deploy`, `component`, `cloud-operator`, and `role-lanes`.
- Full-record observe filtered locally for terms: `cloud`, `domain-criome`, `Cloudflare`, `DNS`, `provider`, `Hetzner`, `Google`, `hoster`, `owner-signal`, `meta-signal`, `core-signal`, `signal/executor`, `runtime triad`, `old Rust signal macro`, `schema-engine`.

## Key Code

No source code is needed for this scout. The load-bearing artifacts are guidance snippets and Spirit records.

### Permanent guidance snippets

`skills/component-triad.md` lines 23-44 defines the repo split:

```text
<component>/                      runtime
signal-<component>/               ordinary wire vocabulary
owner-signal-<component>/         owner-only authority/configuration vocabulary
```

The same file lines 173-189 make the CLI thin: one Signal peer, no database, fail closed if the daemon socket is absent. Lines 191-202 make daemon-to-daemon traffic exclusively `signal-frame` frames, with NOTA only at projection edges.

`skills/component-triad.md` lines 253-285 are the authority split: ordinary peer surface plus owner-only policy/configuration surface; both ship together; no static-local-config-first path for privileged mutable configuration.

`skills/component-triad.md` lines 589-634 define the runtime triad: Signal decodes and dispatches; Executor decides acceptability and lowering; SEMA is the single-writer state layer.

`INTENT.md` lines 249-278 says components ship raw CLI + daemon + sema state first, while the durable direction is schema-driven contracts where schema specifies, signal moves, and sema holds.

### Important Spirit records

Cloud identity and first target:

- 281 - cloud owns cloud-provider API management.
- 282 - Cloudflare DNS and redirect rules are the first cloud target.
- 294 - create cloud as the cloud API management triad; first target includes Cloudflare DNS/settings/redirect rules.
- 296 - cloud is the home for provider API machinery: Cloudflare, Google, and hosters such as Hetzner.
- 680 - first production target is Cloudflare DNS management.
- 685 - first cloud daemon target is Cloudflare DNS records and similar Cloudflare-managed resources.

Cloud authority and state model:

- 311 - public `signal-cloud` gets Query/refresh; privileged policy surface gets Mutate; Cloudflare is reflected external state.
- 325 - cloud plan preparation belongs on the owner signal surface.
- 338 - Cloud `Plan` becomes `Mutate`; reply is `Mutated`; state is last-known provider acknowledgment, with pending `Mutate-sent` before ack.
- 339 - Criome state is last-known acknowledgment/quorum; current external providers break that protocol, so cloud keeps last acknowledgment from them until federation/provider support improves.
- 681 - first cloud state may be a lossy provider-backed cache.
- 686 - cloud daemon starts almost-stateless; cache loss is acceptable because Cloudflare is source of truth.
- 687 - first cache is runtime/volatile in-memory; persistent storage is deferred until there is state worth preserving.

Provider support and credentials:

- 283 - provider integrations may be build-time opt-ins.
- 295 - unsupported provider requests should return typed unsupported-capability replies; future self-upgrade is possible when support is cheap.
- 341 - v1 defers build-time provider gating; build all providers by default, Cloudflare first then Hetzner; earlier build-time opt-in remains long-term.
- 342 - capability observation must distinguish built-but-unconfigured providers from providers not built into the daemon.
- 682 - Cloudflare credential starts as an environment token.
- 688 - prefer Cloudflare CLI over direct HTTP API for first integration if easier.
- 689 - API key may use env-var-populated-by-password-manager pattern, but safer auth alternatives should be investigated.

Domain-criome boundary:

- 285 - Criome domain component is named `domain-criome`.
- 286 - `domain-criome` speaks intelligent Signal resolution.
- 297 - create `domain-criome` as name-server/root-registry shape with richer Signal resolution protocol.
- 312 - `domain-criome` is authority for `.criome` domains; each domain is content-addressable and checks current authority by asking its own daemon.
- 321 - `domain-criome` runtime excludes provider APIs and direct CLI store access.
- 340 - a `domain-criome` daemon can resolve non-owned domains via content-addressed, timestamped last-known records; NotAuthoritative delegation is fallback.
- 345 - registered but undelegated domain names need typed `NoRecords` result.
- 346 - keep `domain-criome` contract vocabulary provider-neutral and record-only.
- 352 - domain-criome contracts keep provider vocabulary out.

Component/signal architecture:

- 263 - every component supports Help operations in its NOTA vocabulary.
- 270 - component binaries are `<component>` CLI and `<component>-daemon`; the component name names the role, not a daemon binary.
- 287 - cloud and domain components follow current triad Signal/Sema/Executor architecture.
- 293 - `owner-signal` remains the active policy-signal naming convention until explicit rename lands.
- 298 - future component work should use latest bottom architecture around Signal, Sema, and Signal Executor.
- 359 - signal/sema macro deepens: short header, ordinary+owner namespaces, Help on every enum.
- 365 - CLI help examples using flags/words are wrong; every CLI invocation is one NOTA argument or a path.
- 388 - canonical name is short header; every message carries it; body holds payload.
- 695 - rkyv binary form is the single encoded representation in both sema storage and signal transport; NOTA is the text projection.
- 720 - keep separate ordinary and owner sockets for now; filesystem permissions enforce access.
- 725 - schema may model permissioned/unpermissioned surfaces, but implementation still uses separate owner/ordinary sockets.
- 739 - permission-in-signal variant is possible later; current two-socket filesystem approach stays.
- 768 - newer direction says owner-signal surfaces should become core-signal surfaces; core owns privileged control/library layer.
- 830 - tests should prove CLI NOTA boundary and component-to-component binary rkyv boundary.
- 834 - NOTA is the text interface/spec representation for portable rkyv data shapes used as SEMA or signal.
- 856 - component runtime triad is Signal + Executor + SEMA, distinct from repo packaging triad.
- 858 - schema derives data objects/traits; Rust writes behavior methods on those objects.

Cloud MVP carve-outs and deployment context:

- 679 - cloud component production slice uses old Rust signal macro path.
- 684 - first cloud MVP can skip new schema-engine approach to prioritize production push.
- 356 - lean lojix/horizon stack becomes main deployment after MVP.
- 357 - sandbox testing is precondition for lean-stack cutover.
- 870 - current session/report lane moved to `cloud-operator`.
- 872 - register `cloud-designer` as specialized designer lane scoped to cloud topics.
- 873 - register `cloud-operator` as specialized operator lane scoped to cloud topics.

## Architecture

Cloud is not a general DNS daemon. It is the cloud-provider API management component. Its first concrete job is Cloudflare-managed DNS/redirect/settings, and later provider surface includes Google and hosters such as Hetzner.

`domain-criome` is adjacent but separate. It is the `.criome` content-addressed domain authority and richer Signal-resolution component. Its contracts must stay provider-neutral and record-only, and its runtime excludes provider APIs. Cloudflare DNS/provider vocabulary belongs in cloud, not in `domain-criome`.

The cloud component should be described functionally as a triad:

- runtime repo: `cloud` daemon plus thin `cloud` CLI;
- ordinary signal: `signal-cloud` for peer/public observation/query/refresh;
- privileged policy/control signal: currently named `owner-signal-cloud` in AGENTS and most of `skills/component-triad.md`, but with active newer `core-signal-*` direction in Spirit and a contradictory line in `skills/component-triad.md`.

State model: cloud reflects external provider state. For Criome-native components, state agreement should become last-known acknowledgment/quorum. Current providers do not speak that protocol, so cloud tracks last-known provider acknowledgments and may use lossy/volatile cache for v1. Mutation is an authority operation: issue `Mutate`, enter pending `Mutate-sent`, transition to `Mutated` only on provider acknowledgment.

Runtime model: Signal receives/decodes, Executor validates and lowers, SEMA writes state as the single writer. Even if the first cloud MVP uses old Rust signal macro and little/no persistent state, the recap should frame that as a scoped production carve-out, not the final architecture.

## Current durable constraints

1. Cloud owns provider API management; first target is Cloudflare DNS/redirect/settings.
2. Domain-criome owns `.criome` content-addressed domain authority and must stay provider-neutral.
3. Public/ordinary cloud operations can query/observe/refresh reflected state; mutations and plan preparation require privileged policy/control surface.
4. Cloud state is last-known provider acknowledgment; cache may be lossy and volatile for v1.
5. Provider support must be typed: distinguish unsupported, not-built, built-but-unconfigured, and configured.
6. V1 does not need build-time provider gating; long-term build-selectable providers remain live direction.
7. First Cloudflare auth can start with password-manager-populated environment token, but this is a risk area: keep secrets out of Nix and broad environments, and investigate safer auth.
8. CLI is thin, one Signal peer, no database access. Daemon owns durable state. Daemon external surface is Signal frames only.
9. Every component binary takes exactly one argument: inline NOTA, NOTA file path, or signal-encoded file path. No flags.
10. NOTA strings use bracket forms; component-to-component messaging is binary rkyv.
11. Help/discovery must be through NOTA operations, not `--help`.
12. Schema-driven architecture is the durable direction; cloud MVP old-macro path is an exception for first production push.
13. If implementation follows, Rust behavior belongs as methods on data-bearing/schema-emitted objects, not free functions.

## Superseded or conflicting guidance

- **Policy signal name is unsettled.** `AGENTS.md` and `skills/component-triad.md` lines 140-147/287-294 say `owner-signal-<component>` remains active until explicit rename. But `skills/component-triad.md` line 14 already says `core-signal-<component>`, and Spirit 767/768 say privileged surfaces should become `core-signal-*`. Older Spirit 290/299 preferred `meta-signal` but made it tentative. Recap should preserve the functional invariant as privileged policy/control signal and flag repo naming as unsettled before code/repo creation.
- **Cloud MVP old macro vs schema-driven stack.** Spirit 679/684 authorize old Rust signal macro and skipping schema engine for first production MVP. INTENT and later schema records preserve schema-driven architecture as the durable direction. Treat old macro as time-scoped, not permanent design.
- **Build-time provider opt-ins.** Records 283/295 are low-certainty long-term direction; record 341 defers gating for v1; record 342 still requires capability observation to expose built/unconfigured/not-built states. Do not make provider cfg gating block v1.
- **Credential env token.** Records 682/689 allow environment-token start, but system guidance says secrets stay out of Nix and broad process environments. Recap should call this an initial auth pattern requiring safe scoping and follow-up.
- **Plan vocabulary.** Earlier cloud `Plan` language is superseded by record 338: use `Mutate` / `Mutated` lifecycle for provider-acknowledged state.
- **domain-criome leakage risk.** Any Cloudflare/provider vocabulary in `domain-criome` conflicts with records 321/346/352. Keep provider mechanics in cloud.

## Start Here

Start with Spirit records 281-296, then 311, 338-342, and 679-689. They define cloud identity, Cloudflare first target, authority split, state model, provider support, and MVP carve-outs. Then open `skills/component-triad.md` lines 136-296 and 589-634 to frame the recap in the repo/runtime triad language.

## What the cloud-operator should preserve in the recap

- Cloud is already defined enough to recap: provider API management triad, not a blank design exercise.
- Cloudflare DNS is the first target; Google/Hetzner are named later scope, not v1 blockers.
- The cloud/domain split is load-bearing: provider APIs in cloud, `.criome` authority in `domain-criome`.
- The current state model is “reflected external provider state as last-known acknowledgment,” with lossy/volatile cache acceptable for the first slice.
- Public query/refresh vs privileged mutate/plan is the key signal-tree distinction.
- The old-macro/cloud-MVP shortcut should be labeled as a production-slice exception, while the permanent direction remains schema-driven Signal/Executor/SEMA.
- Policy-signal naming needs explicit caution: `owner-signal-cloud`, `meta-signal-cloud`, and `core-signal-cloud` have conflicting guidance; preserve the uncertainty instead of silently picking a name.

## Supervisor coordination

No supervisor decision was needed for this read-only scout. The only open decision to surface to the parent is the policy-signal naming conflict if the recap turns into implementation or repository creation.
