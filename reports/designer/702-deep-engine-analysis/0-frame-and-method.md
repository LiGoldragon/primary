# 702 — deep engine analysis and review (frame and method)

Orchestrator frame for the deep engine analysis the psyche requested:
*"lets do a deep engine analysis and review."* This is the successor to
report 690 (the full engine audit, ~6 days ago), but **deeper and
different in kind**: 690 asked *"is each change real, and does the stack
cohere?"* — a change-audit. 702 asks the harder questions about the
same engines now that the dust of the strict-positional wave has settled
and two arcs have moved onto `main`:

- **Invariant integrity** — what does each engine actually *guarantee*,
  where is that invariant enforced in code (`file:line`), and where could
  it break? (single-writer soundness, quorum `k > n/2`, one-schema →
  one-semantics across lowering paths, acquire-exactly-`D`.)
- **Soundness vs surface** — does the *production daemon path* do the
  thing, or only a `#[cfg(test)]` harness? (the audit-precision rule.)
- **Design tensions** — where the current shape fights the intent, or
  fights a neighbouring engine, or carries a transitional seam that will
  bite.
- **Risk ranking** — the highest-value thing to fix or decide next,
  per engine and across the stack.

Every claim cites `file:line` and states what the production path *does*,
not what a test *can do*. Findings are adversarially verified before they
enter the synthesis — a skeptic tries to refute each P1/P2 finding against
the code before it is allowed to stand.

## What moved since 690 (the reason this is worth doing now)

| Engine | 690 `main` | 702 `main` | What changed |
|---|---|---|---|
| nota-next | `7105c2b` | `7105c2b` | unchanged on main; codec is the stable floor |
| schema-next | `b3be7d0` | **`da5643c`** | `{| |}` impl-reference syntax **merged to main** (was a branch) |
| schema-rust-next | `bb4dfe2` | **`e116cc4`** | named-frame expansion + a "use Kameo lifecycle fork" commit on the *codegen* layer (investigate) |
| sema-engine | `73eea24` | `73eea24` | unchanged on main |
| criome | `068f9db` | **`454daf8`** | **majority quorum enforced** (`22801af`, 684 Woe 3) + authorized object references published |
| signal-criome | `521a8ed` | **`9194c79`** | authorize typed object references |
| router | `430f1de` | **`fb403c4`** | **authorized-object fanout + head-reference routing landed on main** (was branch `attendance-fanout-139`) |
| signal-standard | `aa672cc` | **`e3ff47b`** | authorized-head object kind + interest matcher |
| spirit | `fb14aaa` | **`aa7e9b0`** | **reject stale mirror restore heads** (verify-after-restore; 700 blocker 2) + propagation schema-chain pin |
| mirror | (unaudited) | `027a991` | routed object notices + schema-chain pin — the chain endpoint nobody audited in 690 |

Plus a live **`criome-gated-propagation-loop`** branch (criome `6c75804`
*retire publish-side authorized-object match* — the `m0p2` retirement;
router `9471219` *expose criome authorized-object projection*). The
single-host loop (report 700) is closing in real time; one lane verifies
exactly how far.

## What "engine" means here (scope)

Same broad reading as 690 — the **schema-derived engine stack** — in
three tiers, plus two **end-to-end pipeline** lanes that 690 lacked
(the deep part):

1. **Codegen engine** — `nota-next` → `schema-next` → `schema-rust-next`
   (authored `.schema` NOTA → typed Rust).
2. **Storage engine** — `sema-engine` over `sema` / `signal-sema`.
3. **Component engines** — `criome` (+`signal-criome`), `router`
   (+`signal-router`/`signal-standard`), `spirit` (+`signal-spirit`),
   `mirror` (+`signal-mirror`), `mentci` (+`signal-mentci`).
4. **Pipeline lanes (cross-cutting, after the per-engine barrier):** the
   **codegen pipeline end-to-end** (does `.schema` → Rust round-trip
   soundly, where are the seams) and the **propagation loop end-to-end**
   (spirit → criome → router → mirror → spirit: is the criome-gated typed
   loop real on `main`, and what does the live branch add).

## Method

Designer parallel-audit protocol run as a Workflow, deeper than 690:

- **Phase 1 — per-engine deep analysis (pipelined with verify).** One
  agent per engine, audits the current `main` HEAD above. Reads the
  repo's `INTENT.md` FIRST, then `ARCHITECTURE.md` / `AGENTS.md`, then the
  real source modules, then recent commits and the governing Spirit
  records + prior designer reports (690/697/698/699/700/701). Produces a
  deep architectural review — invariants, tensions, soundness-vs-surface,
  ranked findings — with at least one mermaid visual, written to its
  numbered file. Builds on 690 rather than redoing it.
- **Phase 1b — adversarial verification (pipelined per engine).** As each
  analysis completes, an independent skeptic tries to **refute** every
  P1/P2 finding against the code. A finding that cannot be grounded in
  `file:line` is downgraded or dropped. Verdicts feed the synthesis.
- **Phase 2 — pipeline lanes + completeness critic (barrier on phase 1).**
  Codegen-pipeline and propagation-loop agents trace the two flows
  end-to-end across the verified per-engine summaries; a completeness
  critic names the engine/change/claim the per-engine lanes missed.
- **Synthesis.** Folds verified findings into the whole-stack narrative,
  the cross-cutting verdicts, and operator/designer-actionable beads — an
  audit that ends without beads is incomplete.

## Lane assignments and report layout

| File | Engine / lane | `main` HEAD |
|---|---|---|
| `1-nota-next.md` | `nota-next` codec | `7105c2b` |
| `2-schema-next.md` | `schema-next` semantics + resolver + impl-reference | `da5643c` |
| `3-schema-rust-next.md` | `schema-rust-next` Rust emission | `e116cc4` |
| `4-sema-engine.md` | `sema-engine` storage planes | `73eea24` |
| `5-criome.md` | `criome` + `signal-criome` agreement engine | `454daf8` / `9194c79` |
| `6-router.md` | `router` + `signal-router` + `signal-standard` | `fb403c4` / `3e4bb07` / `e3ff47b` |
| `7-spirit.md` | `spirit` + `signal-spirit` | `aa7e9b0` / `6884d7a` |
| `8-mirror.md` | `mirror` + `signal-mirror` (the unaudited endpoint) | `027a991` / `d12dda9` |
| `9-mentci.md` | `mentci` + `signal-mentci` + `meta-signal-mentci` | `577d64b` |
| `10-codegen-pipeline.md` | codegen end-to-end (cross-cutting) | — |
| `11-propagation-loop.md` | propagation loop end-to-end (cross-cutting) | — |
| `12-adversarial-verification.md` | the refutation verdicts on P1/P2 findings | — |
| `13-completeness.md` | what the per-engine lanes missed | — |
| `14-synthesis.md` | whole-stack narrative + ranked risks + beads | — |

## Governing intent (the dense neighbourhood)

Codegen: `4np2`/`e6v5` (token-native emission, not string codegen),
`xai7`/`z544` (shape-directed structural codec), `6cfr` (Asschema
removed), `ba6d`+695 (the `{| |}` impl-reference catalog), `3742` (mark
participations at the declaration), `4ups` (`-next` rename pending).
Agreement/propagation: `m0p2` (router-sole operational matcher; criome
observation/audit-only), `d6he`/`nfvm` (criome holds authorized head;
spirit fetches it), `2st7` (criome authenticates submitter), `p3td`
(self-quorum), `ay3y` (attested moment), `gc0n` (closed verdict), `z9d6`
(composable contracts), `9s52` (per-Unix-user criome), `lt44` (two
transport lanes). Storage: `sema`/`sema-engine`-today vs eventual `Sema`.
Each lane cites the records that govern its surface.
