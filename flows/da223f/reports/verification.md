# Independent verification report

Verifier: `/root/verify_codec`, thread `01a071ff-2e96-7ae0-abe2-c6a0f12a6b80`.
Final sources: Protos 0.26 `2d999f173334`; datom-codec 0.21 `41a3c073d5c5`,
pinned exactly to Protos.

Primary-preflight independently reran the final semantic corpus with a 4 GiB
limit, 180-second timeout, one offline Cargo job. It enumerated 3,905 strings
over `a/b/./:/!` of lengths 1–5; 246 DatomWords were admitted. All 738
standalone, one-Variant, and two-Variant cases passed raw Datom equality after
printed Text/reparse and projected Protoform/Situation equality. `a..b`, `.a`,
and `a.` were rejected as Unstable and passed as quoted Text at every depth;
`a:b.c`, `a!b.c`, and Decimal `3.25`, `-42.0`, and `0.5` passed.

F1–F8 and F10 pass in the verifier's external matrix: punctuation Text,
Problem messages, finite Decimal refusal, opaque Meaning, universal bearer and
route matrix, projection equality, iterative deep/budget behavior, and
recoverable Positions exhaustion. F9 passes for supported declarations and
fixed-generator freshness: Route's unsupported borrowed `&str` input is
explicitly omitted, `DatomWord` is imported rather than falsely aliased, and
contracts are regenerated. The generator's old downstream implementation
template remains an evidenced ethos-zero follow-up, not an in-scope crate
failure. Ethos-zero pin `dc54e3323ae00dc3f88f4d65c2785e6800c06b74` was
untouched.

The final remote Nix outcomes witnessed by this flow are green: both exact
heads exited zero with `all checks passed!` under 4 GiB and bounded 900-second
remote-only checks.

Sources: audit `flows/1a6ca4/reports/auditDatomCodecAstra.md`; verifier
artifacts `/tmp/ext-verify-da223f-1653`, `/tmp/ext-verify-da223f-1714/final.rs`,
`/tmp/ext-verify-da223f-contextual-matrix-1724`,
`/tmp/ext-verify-da223f-analogous-1726`; preflight
`/tmp/datom-inverse-probe.YbtxOa` / `target-p026-d021`.
