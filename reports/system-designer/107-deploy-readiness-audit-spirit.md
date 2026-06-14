# 107 — Deploy-readiness audit: spirit `structural-forms-integration`

*Narrow, deploy-shaped audit requested by the operator before shipping the
integration branch to the live Spirit store. Answers the operator's six
questions with primary evidence (branch diffs, version constants, the live
store on disk). Verdict: **the candidate is sound to deploy in shape** — ship
`structural-forms-integration` (mirror correctly excluded), `im1l` does not
block, sequence before the domain coarsening, bump to 0.13.0. The remaining
gates are the system-operator's staging-copy migration proof + the ignored
Nix/deploy tests — no further design work is required.*

## The candidate, established

`structural-forms-integration` is a **matched branch family** across all four
repos: `spirit`, `sema-engine`, `signal-spirit`, `meta-signal-spirit` all on a
branch of that name (verified in the candidate `Cargo.toml`). It is the engine
VC-hardening tower + store decomposition + the **structural-forms (TypeReference
structural-macro) schema relocation**, with the mirror shipper **removed**.

Candidate composition (spirit `structural-forms-integration`, `main@origin..@`):
`d586ba3f` engine repoint → `c3a21070` migration cleanup (sd7n + **im1l** + h3ll)
→ `35264227` diagnostics (12r5) → `68931ec4` v7+v8-only migration scope
→ `37bafef6` VersionReport store axes + meta MirrorTarget (0.13.0) → `a7b7d958`
gated mirror shipper → `339b08f9` guardian-journal architecture note → `8eeeda88`
store god-impl decomposition → `d2cf86fd` **integrate structural forms** (the new
top commit).

Pins: `sema-engine` = branch `structural-forms-integration` (v0.6.2 @ `1afcd01`),
`sema-engine-previous` = 0.2.3 @ `ebee6e44`, `signal-spirit` + `meta-signal-spirit`
= branch `structural-forms-integration`.

## Q1 — Is `structural-forms-integration` the deploy candidate (not just substrate)?

**Yes.** It is pushed (`structural-forms-integration@origin`), it carries a
coherent, self-consistent family across all four repos on one branch name, and it
integrates the whole non-mirror tower plus the structural-forms relocation. It is
shaped as a deploy candidate, not a scratch substrate. One caveat that makes it
*not identical* to the reviewed 0.13.x tower: the top commit `d2cf86fd` is a
**material restructuring** — it deletes spirit's in-repo generated wire plane
(`src/schema/signal.rs` 5456 lines, `meta_signal.rs` 773, the `signal.schema` /
`meta-signal.schema` sources) and moves spirit to **consume** the contract from
`signal-spirit` / `meta-signal-spirit` (architecture intent `u7tj`: wire contracts
live in the signal crate). That relocation is the **newest and least-separately-
reviewed** part of the candidate; it is the one area the test pass should target
specifically (see Q3).

## Q2 — Anything from the old 0.13.x tower missing and truly required?

**Only the mirror shipper + MirrorTarget — and their absence is correct, not a
gap.** The top commit deletes `src/shipper.rs` (127 lines); the candidate has no
`mirror` dependency, no `mirror-shipper` feature (`default = []`), and **zero
`mirror`/`MirrorTarget` references in `src`** (the only `mirror` hits are the
English word in two doc comments). Mirror durability is **blocked by `primary-x3l7`**
(the unauthenticated `0.0.0.0:7474` ingress) and must not go live until that is
fixed — so shipping the non-mirror integration now is the *right* shape, not a
shortfall.

Everything else from the tower **is present**: engine hardening
(candidate `sema-engine` carries `rebuild_from_log`, `LayoutOpenPlan`/
`validated_storage_layout`, `CHAIN_HEAD` — the full single-writer + O(1)
head-digest + commit-log/outbox decomposition chain), store god-impl
decomposition (`8eeeda88`), the migration fixes (`im1l`/`sd7n`/`h3ll`/`12r5`),
VersionReport store axes (`dmy4`, `37bafef6`). Nothing required is missing.

## Q3 — Store migration risk; does `primary-im1l` block?

**`im1l` does not block — twice over.** (a) It is **fixed in the candidate**
(`c3a21070`): the v7 referent registry is now read via
`PreviousTableReference<SpiritStoreV7Referent>` — "a v7 record whose entry carries
a referent resolves against this table during the migration," replacing the
`Option<…V8Referent>` shape that dropped them. (b) The live store is **already
spirit-schema v9**, so the v7/v8 → v9 record fold path is **never reached** on this
store.

**The actual migration this deploy performs is an engine layout self-heal, not a
record fold.** Evidence: the deployed spirit (`f4635c3c`) pins **sema-engine 0.4.0**;
the candidate pins **0.6.2 with `STORAGE_LAYOUT = 5`**. On first open the candidate's
`validated_storage_layout` sees the older layout and takes the rebuild-from-log
path (`primary-lmf3`: refold derived slots from the versioned log + re-stamp 5) —
the self-heal designed for exactly this. The spirit `SPIRIT_SCHEMA_VERSION` is 9 on
both sides, so no spirit-record migration runs.

**The one genuine risk to prove on a staging copy** (system-operator): confirm the
live store carries a **versioned log**, so the candidate takes `rebuild_from_log`
(refold) and **not** the no-log previous-engine path. The deployed 0.4.0 opened
with `VersioningPolicy`, so a log should exist — but this is the load-bearing
assumption and must be verified against the real store before deploy, along with
record count (1248), referent survival, query surface, and daemon restart.

## Q4 — Does MirrorTarget / mirror shipper stay out?

**Confirmed out.** `shipper.rs` deleted, no mirror dependency, no `mirror-shipper`
feature, no `MirrorTarget` reference in `src`. If a `MirrorTarget` field survives
in the relocated `meta-signal-spirit` contract it is **inert** — there is no shipper
to consume it, so even a set target ships nothing. Safe. (Worth a one-line confirm
during integration that the meta contract either drops the field or leaves it
clearly inert.)

## Q5 — Sequencing with the domain coarsening (report 106 / `primary-fwe3`)

**This deploy first; domain coarsening second.** Both touch the store, but they are
disjoint migrations: this one is an **engine layout** rebuild (no record rewrite);
the coarsening is a **record domain-vector** rewrite. They must not interleave.
Order: land + deploy `structural-forms-integration`, prove it live, **then** rebase
`fwe3` onto the deployed state and run the domain migration as its own staged step.
Note the dependency: `fwe3` targets `signal-spirit`'s `domain.schema`, and this
deploy moves spirit to `signal-spirit#structural-forms-integration` — so the
coarsening branches **from the post-deploy `signal-spirit`**, not old main. Either
sequence the two migrations or bundle both `From`-chain steps in one pass; do not
run two uncoordinated store migrations (Spirit `qr5o`; report 106).

## Q6 — Versioning: stay 0.12.1 or bump?

**Bump to 0.13.0 as part of the deploy.** The candidate `Cargo.toml` currently reads
`0.12.1` (the top commit reset it), but the deployed daemon is *also* `0.12.1` — so
shipping this materially different artifact under the same version would make
`spirit Version` report `0.12.1` for two different binaries, defeating the very
VersionReport observability `dmy4` just added. The removed mirror shipper does not
argue for a lower number; the component version names the *artifact identity*, and
this artifact differs from the live one (engine layout 5, relocated wire plane,
migration fixes). Set `0.13.0` before/at deploy and update `skills/spirit-cli.md`'s
stated deployed version. The store-schema axis (9) + layout (5) further distinguish
it, but the component version must still move.

## Verdict and go / no-go

**Designer sign-off on shape: GO.** Ship `structural-forms-integration`. The shape
is correct (mirror out, gated behind x3l7), nothing required is missing, `im1l` is
non-blocking, the migration is the designed layout self-heal, and sequencing vs the
coarsening is clear.

**Conditions the system-operator owns before flipping it live:**
1. **Staging-copy migration proof** (the load-bearing gate): copy the live
   `~/.local/state/spirit/` store, open with the candidate, confirm — versioned-log
   present so `rebuild_from_log` runs (not the no-log path); record count 1248
   preserved; **referents survive**; `Observe`/`Count` return the expected set;
   daemon restarts and self-resumes.
2. **Run the ignored Nix/deploy integration tests** the build/test pass skipped.
3. **Bump to 0.13.0** + update the version stated in `skills/spirit-cli.md`.
4. **Confirm** the relocated wire contract (signal/meta-signal now from
   signal-spirit/meta-signal-spirit) is shape-unchanged so the CLI and any
   consumer still interoperate — the newest, least-reviewed change.

No design blocker remains; these are deploy-operations gates, not design questions.
After they pass, deploy, then proceed to the domain coarsening migration (`fwe3`).
