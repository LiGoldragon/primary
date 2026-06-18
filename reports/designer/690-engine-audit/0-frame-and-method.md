# 690 — full engine audit (frame and method)

Orchestrator frame for the parallel engine-audit session the psyche
requested: *"do a full context maintenance, after rereading skills and
spirit. and start a full engine audit with visuals explaining all the
new changes in the last few days."*

## The problem

The schema-derived stack moved hard over the last week. A single
grammar change in the codegen engine (strict positional structural
field roles) rippled into a **port-to-strict-schema-contracts wave**
across every consumer; criome grew a whole authorized-object-pulse /
policy-contract / attested-moment machinery; router landed networked
router-to-router forwarding; spirit gained a negative-guideline guardian
reason and public text search; and an entire new component — mentci —
plus the signal-standard shared library were born. No one document
explains the whole motion. This audit produces it: per-engine, what
changed, is it real, does it cohere with intent, and what gap remains —
each with a visual.

## What "engine" means here (scope decision)

Read broadly and deliberately: **engine = the schema-derived engine
stack that changed in the last ~6 days**, in three tiers.

1. **Codegen engine** — the pipeline that turns `.schema` NOTA into
   typed Rust: `nota-next` (structural-macro-node codec) →
   `schema-next` (schema semantics + resolver) → `schema-rust-next`
   (Rust emission via `quote!`).
2. **Storage engine** — `sema-engine` (the full database engine over
   `sema` + `signal-sema`).
3. **Component engines built on the stack that saw major change** —
   `criome` (+ `signal-criome`), `router`, `spirit` (+ `signal-spirit`),
   and the new `mentci` component (+ `signal-mentci`,
   `meta-signal-mentci`, `signal-standard`).

This is the honest reading of *"all the new changes in the last few
days."* If the psyche meant a narrower "engine" (e.g. only the schema
codegen engine, or only criome's internal policy engine), say so and the
audit re-scopes; the broad reading is the more useful default and the
session proceeds on it.

## Method

Designer parallel-audit protocol (`skills/designer.md` §"Parallel
manifestation + audit pattern"), run as a Workflow:

- **Phase 1 — per-engine audit (parallel).** One subagent per engine /
  engine-cluster. Each reads the repo's `INTENT.md` / `ARCHITECTURE.md`,
  the recent commits listed below, the current code, and the governing
  Spirit records + designer reports; verifies every claimed change is
  **real** (commit + code + test/build evidence, cited `file:line`),
  **coherent** with design intent, and flags **drift / gaps**. Each
  writes its numbered report with at least one mermaid visual and
  returns a structured summary.
- **Phase 2 — cross-cutting critics (parallel, barrier on phase 1).**
  A **coherence** critic checks the engines fit together (the
  strict-positional port is consistent across consumers; schema-cc
  resolver integration is reflected everywhere; the criome pulse
  contract matches router's delivery; signal-standard is consumed not
  re-declared). A **completeness** critic asks what engine or change was
  missed. Both read every phase-1 summary.
- **Synthesis (orchestrator).** The designer folds both critics into the
  cross-cutting and synthesis files and names operator-actionable beads
  for any gap — an audit that ends without beads is incomplete
  (`skills/designer.md` §"Audits feed into bead filing").

**Audit precision rule** (`skills/designer.md`): claims state what the
production path **does**, not what the code **can do** in a test.
Round-trip-in-test ≠ artifact discipline. Every claim cites `file:line`.

## Lane assignments and report layout

| File | Engine | Tier | HEAD audited |
|---|---|---|---|
| `1-schema-next.md` | `schema-next` | codegen | `b3be7d0` |
| `2-schema-rust-next.md` | `schema-rust-next` | codegen | `bb4dfe2` |
| `3-nota-next.md` | `nota-next` | codegen | `7105c2b` |
| `4-sema-engine.md` | `sema-engine` | storage | `73eea24` |
| `5-criome.md` | `criome` + `signal-criome` | component | `068f9db` / `521a8ed` |
| `6-router.md` | `router` | component | `430f1de` |
| `7-spirit.md` | `spirit` + `signal-spirit` | component | `fb14aaa` / `ee5a98e` |
| `8-mentci.md` | `mentci` + `signal-mentci` + `meta-signal-mentci` + `signal-standard` | component | `5ddd3b4` |
| `9-cross-cutting.md` | coherence + completeness | — | (orchestrator, from critics) |
| `10-synthesis.md` | whole-stack narrative + beads | — | (orchestrator) |

## Commit inventory (the audit target — last 6 days)

**schema-next** (codegen, schema semantics + resolver): structural field
roles grammar (`af3705c` reject retired struct field pair syntax,
`95f1ee7` reject redundant explicit field roles, `1de72dd` support
explicit structural field roles); nested namespace POC (`61aa1bf`);
schema-cc resolver integration (`caa7797`), generate parenthesis-ref
dispatch from schema-cc + retire hand match (`1a93aad`), co-locate
schema-cc (`aa13b4b`); generics/traits/component-codegen constraints
doc (`e721626`); applied frame roots from pipe generic decls (`f130937`);
shared rust-build toolchain (`7318654`, `b3be7d0`).

**schema-rust-next** (Rust emission): standard newtype impls for wire
contracts (`cad9ec2`), schema-implied newtype trait impls (`f265aad`);
expand applied frame roots into concrete enums (`71838fa`); dependency
contracts declare streams (`9ffa588`); terminal domain scopes
(`a526405`), optional-enum terminal decoders (`660d350`, `e6d1394`).

**nota-next** (codec): pipe delimiter construct constraints (`7426a6a`);
structural macro shapes integration (`00d0050`); PascalHeadBody shape
(`db0f10a`), HeadedAtom shape (`3e18e37`).

**sema-engine** (storage): decompose Engine god-impl by data-ownership —
CommitLog + Outbox planes (`f074b98`, `1afcd01`); RecordKey closed sum +
drop dead MaterializeIdentifierParse (`65a6126`); single-writer lock +
O(1) chain-head digest (`22b9de1`); domain keys vs identifiers
(`909eaa0`); portable checkpoint bytes (`da959d6`); range-read versioned
log suffixes (`e5e38e8`).

**criome** (auth/agreement engine): port to strict signal-criome
contract (`068f9db`); interest-bearing authorized object tokens
(`4250cbb`); classified authorized object pulse POC (`b9bc29f`);
contract-programmed time pulses doc (`255660a`); publish authorized
object update references (`0cf326c`); persist policy contracts + stamp
quorum signatures (`3c05122`); evaluate schema-emitted policy contracts
(`03d2b32`); bind policy evaluation to attested moments (`92a703b`);
explicit psyche escalation outcome (`9719703`); Crayome→Criome language
naming fix (`a04154`/`865f8b3` POC).
**signal-criome**: port to strict schema contracts (`ca3624c`); bind
authorized object interest into stream token (`e33ea04`);
subscriber-filtered object pulse POC (`4ea7319`); authorized object
update pulse (`caad934`); stamp quorum signature surfaces (`9d8ea38`);
attested-moment policy evidence (`8459fb4`); policy contract wire
surface (`947f271`); snapshot/wrapped-field accessors (`521a8ed`,
`a04e595`).

**router**: port persona integration to current contract (`430f1de`);
port to strict schema contracts (`dc9a3bb`); deliver routed objects to
component sockets (`629ca92`); accept routed contract objects over
forward ingress (`37f9387`); networked router-to-router forwarding —
milestone 2 (`075ca73`); port nexus frame to schema generics (`4faee08`).

**spirit**: reject negative-guideline intent captures (`6092b80`); port
to strict schema contracts (`fb14aaa`); 0.14.0 inline stashed
observations (`4a1b0a8`); public text search shorthand (`e386d90`);
mirror shipper integration (`5779432`, `08fffdf`); OFFLINE full-chain
e2e harness (`4121bf9`); resolve clarification records into target edits
(`2ed1c76`); public intent render client (`1cd4b35`).
**signal-spirit**: port schema to strict positional syntax (`e971059`);
negative-guideline guardian reason (`e5f432b`); public text search root
(`6967958`); generated standard newtype impls (`876c272`);
ResolveClarification contract operation (`717a3fe`).

**mentci component (new)**: `mentci` daemon runtime + thin client
(`5ddd3b4`), daemon-local schemas bootstrap (`ac37ee5`); `signal-mentci`
programmable UI contract (`97730d5`) + observation-token-with-snapshot
(`d0fea7b`); `meta-signal-mentci` daemon configuration contract
(`270cd90`); `signal-standard` shared cross-component standards
(`3f9d75e`) + typed standard socket vocabulary (`aa672cc`).

## Governing intent (refreshed this session)

The criome/mentci design is governed by a dense Spirit neighborhood —
`m0p2` (router-sole operational matcher; criome keeps no delivery
registry), `l2ha` (object-update fan-out owned by router + subscribers),
`lt44` (two transport lanes: router general + direct criome peer),
`ay3y` (crystallized-past attested-moment, a-priori window), `gc0n`
(closed verdict; criome only authorizes submitted objects; EscalateTo
Psyche dead-letter until UI), `9s52` (per-Unix-user criome), `q1le`
(encrypted multi-key store), `nfvm` (mirror = cross-machine self; criome
holds authorized head), `7x5z`/`1rqy` (mentci = state-bearing
programmable-UI daemon; spelling), `eaf7` (signal-standard socket type),
`2st7` (criome authenticates the submitter), `z9d6` (content-addressed
composable authorization contracts). Each engine audit cites the records
that govern its surface.
