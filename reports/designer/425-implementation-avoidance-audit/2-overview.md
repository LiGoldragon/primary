# 425 — Implementation-avoidance audit: overview (verified, post-slice)

*Synthesis after verifying the operator's response to [[1-findings]]. The
verdict stands and is reinforced: **honest bootstrap, no avoidance** — and three
of the four gaps the audit named are now CLOSED.*

## Verified state (re-checked against the live code)

The operator read 1-findings and landed/confirmed the fixes; re-checking
confirms the claims (not just asserts them):

- **`.witness.txt` — DELETED.** No `*.witness.txt` remain in schema-next or
  schema-rust-next. Record 1112 satisfied. (The audit found six present; gone now.)
- **Shared codec — DONE.** `nota-next/src/codec.rs` exists (commit `c589490`
  "add shared value codec"); schema-rust-next emits through it (`90b9130` "use
  shared nota codec emission", `415482c` "encode … with shared codec"). The
  per-file-reader workaround is replaced — mandatory step 2
  ([[424-schema-nota-extension-full-correctness-design-intent]] §3) is met.
- **`Path` scalar — ADDED.** `TypeReference::Path` is a reserved scalar
  (`asschema.rs:188/208/214`), wired through emission (`Path =
  std::string::String`); local-stack validation in flight at this writing.

So scalar floor is now `String`/`Integer`/`Boolean`/`Path` (record 1152
complete), and the "one shared codec" core (records 1184 step 2, 1109) is real.

## Sole remaining gap

- **Roots model (record 1155) — STILL ABSENT.** `Asschema` is still `input` +
  `output` + `namespace` (`asschema.rs:63-65`); no `roots` / `RootDeclaration`.
  This is the one mandatory step (424 §3, step 5) not built, and it is
  load-bearing for the full-constraints / actor-system target (record 1184): the
  signal/nexus/sema engines run on the roots set, not a fixed input/output pair.
  The operator has not flagged it — it should be the next slice (bead
  `primary-8vzk` step 4).

## Verdict

Honest bootstrap, reinforced. The operator is closing gaps genuinely and fast —
the audit found no disguised incompleteness, and three of four named gaps closed
within the pass. Finish the roots model and the stack converges on
[[424-schema-nota-extension-full-correctness-design-intent]].
