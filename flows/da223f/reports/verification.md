# Independent verification report

Verifier: `/root/verify_codec`. Thread: `01a071ff-2e96-7ae0-abe2-c6a0f12a6b80`. Final source-ready heads: Protos 0.26 `2d999f173334`; datom-codec 0.21 `41a3c073d5c5`, pinned exactly.

Primary-preflight reran the final semantic probe on these shipped heads with 4 GiB, 180 seconds, one offline Cargo job. It enumerated 3,905 strings over `a/b/./:/!`, lengths 1–5; 246 were admitted. All 738 admitted standalone, one-Variant, and two-Variant cases passed raw Datom equality after printed Text/reparse and projected Protoform/Situation checks. `a..b`, `.a`, and `a.` were rejected as Unstable and passed as quoted Text at every depth; `a:b.c`, `a!b.c`, and Decimal `3.25`, `-42.0`, and `0.5` passed.

| Finding | Independent evidence |
| --- | --- |
| F1 punctuation-bearing Text | Pass: nested punctuation Text in Option/Result and the full admitted separator corpus through two Variant heads. |
| F2 Problem messages | Pass: semicolon-bearing, empty, and closing-curly-quote `Problem::Value(Opaque)` messages roundtrip. |
| F3 finite Decimal | Pass: finite extremes roundtrip; nonfinite values are refused. |
| F4 Meaning opacity | Pass: backslashes, unmatched parentheses, curly quotes, and newlines roundtrip. |
| F5 public bearer matrix | Pass: Text directly `Protosizable`; Protoform via `Potential<Protoform, Protoform>`, `Conceivable<Delineation>`, `Textualizable`; Delineation directly `Protosizable`, `Conceivable<Datom>`; Datom directly `Protosizable`, `Conceivable<Datom>`; external Pair `Datomic`, `Conceivable<Datom>`, `Textualizable`; direct `Datom: Incorporable<Pair>`; routes for Pair, Box, Vec, Option<Box>, and Result<Pair, Text>; generic textualization for i64, Vec, Option, Result. Illegal foreign blanket `Conceivable<Datom>` correctly yields E0210. |
| F6 projection/raw inverse | Pass: all 738 composition cases preserve raw Datom and Protoform/Situation through Text; period chains become Variants and malformed runs become quoted Text. |
| F7 depth and budget | Pass: external depth-20,000 Clone/Eq/Debug/text/drop; retained 100,000 witness; caller budget spent once per library callback, with distinct exhaustion faults. |
| F8 Positions exhaustion | Pass: extra Position reads return recoverable exhaustion/site behavior. |
| F9 declarations/freshness | Pass for supported forms: borrowed `Route::run(&str)` omitted, `DatomWord` imported not aliased, contracts regenerated. Old generator implementation boilerplate is an evidenced ethos-zero follow-up. |
| F10 parser state | Pass: named parser-state path exercised; no custom tuple regression. |

Implementation actor witnessed terminal remote `nix flake check` success on both exact heads under 4 GiB and bounded 900-second remote-only checks: each exited `all checks passed!`.

## Sources

- `flows/1a6ca4/reports/auditDatomCodecAstra.md`.
- `/tmp/ext-verify-da223f-1653`, `/tmp/ext-verify-da223f-1714/final.rs`, `/tmp/ext-verify-da223f-contextual-matrix-1724`, `/tmp/ext-verify-da223f-analogous-1726`.
- Primary-preflight `/tmp/datom-inverse-probe.YbtxOa` / `target-p026-d021`.
- Protos `2d999f173334` v0.26; datom-codec `41a3c073d5c5` v0.21; ethos-zero `dc54e3323ae00dc3f88f4d65c2785e6800c06b74` v4.0.0.
