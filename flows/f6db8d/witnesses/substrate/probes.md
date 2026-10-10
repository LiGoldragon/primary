# Probe transcripts — substrate audit (flow f6db8d)

Method: scratch clones of protos b543678, datom-codec f2cc068, ethos-zero 4695ee0 under this directory; probe crates probe/, probe2/, probe3/, probe4/ built against the clones with a cargo [patch] pinning protos to the local clone so both crates share one protos. Run 2026-09-11. The clones were removed afterwards; see Reproducing below.

## Reproducing

The three scratch clones were removed after the run (they are exact copies of
the pinned upstream revisions and duplicate them for nothing). To reproduce,
from this directory:

```sh
git clone /git/github.com/LiGoldragon/protos      protos
git clone /git/github.com/LiGoldragon/datom-codec datom-codec
git clone /git/github.com/LiGoldragon/ethos-zero  ethos-zero
git -C protos      checkout b543678cfc8609529cea7174eb4af8a64daa54ad
git -C datom-codec checkout f2cc06858d38a4028c928d33323a6d682e7c222f
git -C ethos-zero  checkout 4695ee0c1f5d00dcf5cceba08f5fa00412b92184
for p in probe probe2 probe3 probe4; do cargo run -q --manifest-path $p/Cargo.toml; done
```

`probe3` is run with `--release`, and has a second binary,
`probe3/src/bin/roundtrip.rs` (`cargo run --release --bin roundtrip`), which is
the random-text fixpoint probe cited at section 2.1 of the report: 48 557
accepted texts, zero print/reparse instabilities, and
`Canonicalizable::canonicalize` agreeing exactly with a fresh parse of the
canonical text in every case. Each probe crate's `Cargo.toml` carries

```toml
[patch."https://github.com/LiGoldragon/protos"]
protos = { path = "../protos" }
```

so the probe, datom-codec and protos all share one protos; without it cargo
builds two copies of protos and the trait impls do not line up.

## probe/ — parser, ascent and derive edge cases
```
=== P1: guillemet writer does not escape backslash
  content "a b\\" -> text "«a b\\»" -> reparse ERR Error { extent: Extent { start: 0, end: 8 }, problem: Unclosed('«') }
  content "a\\»b" -> text "«a\\\\»b»" -> reparse ERR Error { extent: Extent { start: 7, end: 7 }, problem: Multiple }
  content "x\\" -> text "«x\\»" -> reparse ERR Error { extent: Extent { start: 0, end: 6 }, problem: Unclosed('«') }
  (parentheses, for contrast)
  content "a b\\" -> text "(a b\\\\)" -> reparse Opaque { extent: Extent { start: 0, end: 7 }, boundary: Parentheses, content: "a b\\" }
  content "a\\)b" -> text "(a\\\\\\)b)" -> reparse Opaque { extent: Extent { start: 0, end: 8 }, boundary: Parentheses, content: "a\\)b" }
  content "x\\" -> text "(x\\\\)" -> reparse Opaque { extent: Extent { start: 0, end: 5 }, boundary: Parentheses, content: "x\\" }
=== P2: String round-trip through the full ascent/descent
  "a b\\" -> "«a b\\»" -> ERR Error { layer: Protos, path: [], kind: Structural(Error { extent: Extent { start: 0, end: 8 }, problem: Unclosed('«') }) }  *** FAILED ***
  "a\\»b" -> "«a\\\\»b»" -> ERR Error { layer: Protos, path: [], kind: Structural(Error { extent: Extent { start: 7, end: 7 }, problem: Multiple }) }  *** FAILED ***
  "plain" -> "plain" -> "plain" SAME
  "a.b" -> "a.b" -> "a.b" SAME
  "a:b" -> "a:b" -> "a:b" SAME
  "no such file: { } is content" -> "«no such file: { } is content»" -> "no such file: { } is content" SAME
=== P3: MissingHead reachability
  ".foo": parse OK -> Bare { extent: Extent { start: 0, end: 4 }, text: ".foo" }
      reprint ".foo"
  "..": parse OK -> Bare { extent: Extent { start: 0, end: 2 }, text: ".." }
      reprint ".."
  "a..b": parse OK -> Bare { extent: Extent { start: 0, end: 4 }, text: "a..b" }
      reprint "a..b"
  ".{ }": parse ERR Error { extent: Extent { start: 1, end: 1 }, problem: Multiple }
  ".": parse OK -> Bare { extent: Extent { start: 0, end: 1 }, text: "." }
      reprint "."
  "a.": parse OK -> Bare { extent: Extent { start: 0, end: 2 }, text: "a." }
      reprint "a."
  "a. b": parse ERR Error { extent: Extent { start: 3, end: 3 }, problem: Multiple }
=== P4: angle constraints without a following separator
  "Vector<Integer>": parse ERR Error { extent: Extent { start: 6, end: 6 }, problem: Multiple }
  "[ Scores.Vector<Integer> ]": parse OK -> Enclosed { extent: Extent { start: 0, end: 26 }, enclosure: Bracketed, children: [Headed { extent: Extent { start: 2, end: 15 }, head: Symbol("Scores"), constraints: None, separator: Period, body: Bare { extent: Extent { start: 9, end: 15 }, text: "Vector" } }, Enclosed { extent: Extent { start: 15, end: 24 }, enclosure: Angled, children: [Bare { extent: Extent { start: 16, end: 23 }, text: "Integer" }] }] }
      reprint "[ Scores.Vector <Integer> ]"
  "Foo<Bar>.{ x }": parse OK -> Headed { extent: Extent { start: 0, end: 14 }, head: Symbol("Foo"), constraints: Some(Enclosed { extent: Extent { start: 3, end: 8 }, enclosure: Angled, children: [Bare { extent: Extent { start: 4, end: 7 }, text: "Bar" }] }), separator: Period, body: Enclosed { extent: Extent { start: 9, end: 14 }, enclosure: Braced, children: [Bare { extent: Extent { start: 11, end: 12 }, text: "x" }] } }
      reprint "Foo<Bar>.{ x }"
=== P5: decimal recognised by structure, not position
  "3.14" protos Headed { extent: Extent { start: 0, end: 4 }, head: Symbol("3"), constraints: None, separator: Period, body: Bare { extent: Extent { start: 2, end: 4 }, text: "14" } }
        datom  Ok(Datom { path: [], form: Bare("3.14") })
  "-0.5" protos Headed { extent: Extent { start: 0, end: 4 }, head: Symbol("-0"), constraints: None, separator: Period, body: Bare { extent: Extent { start: 3, end: 4 }, text: "5" } }
        datom  Ok(Datom { path: [], form: Bare("-0.5") })
  "3.14.15" protos Headed { extent: Extent { start: 0, end: 7 }, head: Symbol("3"), constraints: None, separator: Period, body: Headed { extent: Extent { start: 2, end: 7 }, head: Symbol("14"), constraints: None, separator: Period, body: Bare { extent: Extent { start: 5, end: 7 }, text: "15" } } }
        datom  Ok(Datom { path: [], form: Variant(Symbol("3"), Datom { path: [1], form: Bare("14.15") }) })
  "1.x" protos Headed { extent: Extent { start: 0, end: 3 }, head: Symbol("1"), constraints: None, separator: Period, body: Bare { extent: Extent { start: 2, end: 3 }, text: "x" } }
        datom  Ok(Datom { path: [], form: Variant(Symbol("1"), Datom { path: [1], form: Bare("x") }) })
=== P6: f64 ascent panics on non-finite (catch_unwind)

thread 'main' (212542) panicked at /home/li/primary/flows/f6db8d/witnesses/substrate/datom-codec/src/composition.rs:302:9:
Datom decimals are finite
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
  NAN.datomize -> PANIC

thread 'main' (212542) panicked at /home/li/primary/flows/f6db8d/witnesses/substrate/datom-codec/src/composition.rs:199:9:
internal error: entered unreachable code: strings compose from a scalar form
  String::from_positions -> PANIC
=== P7: Meaning accepted in a String position (lossy)
  "(a (b) c)" as String -> "a (b) c" -> retextualized "«a (b) c»"
=== P8: datomize path labels vs tree position
  Extent datom: Datom {
    path: [],
    form: Variant(
        Symbol(
            "Extent",
        ),
        Datom {
            path: [],
            form: Struct(
                [
                    Datom {
                        path: [
                            0,
                        ],
                        form: Bare(
                            "3",
                        ),
                    },
                    Datom {
                        path: [
                            1,
                        ],
                        form: Bare(
                            "7",
                        ),
                    },
                ],
            ),
        },
    ),
}
  text: Extent.{ 3 7 }
```

## probe2/ — derive, budget, depth
```
=== Q1: derive round-trips
  Flag::On: "On" -> SAME
  Odd::Unit: "Unit" -> SAME
  Odd::Empty(): "Empty" -> *** ERR Error { layer: Composition, path: [], kind: Variant { expected: "Odd", found: "Empty" } }
  Odd::Named{}: "Named" -> *** ERR Error { layer: Composition, path: [], kind: Variant { expected: "Odd", found: "Named" } }
  Odd::One: "One.7" -> SAME
  Odd::Two: "Two.{ 7 x }" -> SAME
  Pair<i64>: "{ 1 [ 2 3 ] }" -> SAME
  Nest: "{ { 1 [ 2 ] } Off Some.{ { 3 [] } On None } }" -> SAME
=== Q2: composition budget bypass on derived bare variants
  10000 bare variants, budget.remaining = 5 -> Ok(10000)
  budget left after: 4
  10000 integers,      budget.remaining = 5 -> Err(Budget)
=== Q3: protos reader depth / budget
  300 nested braces -> Err(Depth)
  255 nested braces -> Ok("OK")
  5000 wide (default 4096 budget) -> Err(Budget)
=== Q4: composition depth stack safety
  5000 Some. heads, maximum_depth 1e6 -> Ok(Err("Structural(Error { extent: Extent { start: 1280, end: 1280 }, problem: Depth })"))
=== Q5: non-canonical but accepted texts
  "{a b}" -> canonical "{ a b }"
  "{  a   b  }" -> canonical "{ a b }"
  "[]" -> canonical "[]"
  "{ }" -> canonical "{}"
  "«»" -> canonical "«»"
  "()" -> canonical "()"
=== Q6: Option None spelling
  "None" -> Ok(None)
  "Some.42" -> Ok(Some(42))
=== Q7: integer canonicality
  "0" -> Ok(0)
  "-0" -> Err(Value { expected: "Integer", value: "-0" })
  "007" -> Err(Value { expected: "Integer", value: "007" })
  "+4" -> Ok(4)
  "9223372036854775808" -> Err(Value { expected: "Integer", value: "9223372036854775808" })
```

## probe3/ — structurally built opaque leaves, 600000 trials
```
built opaque leaves: 600000 trials
  guillemets   round-trip failures: 27657
    "\\" -> "«\\»"
    "\\" -> "«\\»"
    "x«{\\" -> "«x«{\\»"
    " {{\\" -> "« {{\\»"
    " \\" -> "« \\»"
    "{(\\" -> "«{(\\»"
    "\\»x" -> "«\\\\»x»"
    "}\\" -> "«}\\»"
    "»(\\" -> "«\\»(\\»"
    "\\»x)" -> "«\\\\»x)»"
  parentheses  round-trip failures: 0
```

## Test suites of the three released repositories
```
--- protos
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 18 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.06s
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
--- datom-codec
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 31 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.23s
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
--- ethos-zero
test result: ok. 17 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 3 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s
test result: ok. 8 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
test result: ok. 2 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 7.92s
test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

## probe4/ — generic, recursive and shadowing derives; datomize path labels
```
=== R1 generic / recursive / shadowing derives
  Either::Left: Left.1  -> SAME
  Either::Right: Right.x  -> SAME
  Either::Neither: Neither  -> SAME
  Tree: Node.{ Leaf.1 Node.{ Leaf.2 Leaf.3 } }  -> SAME
  Named: { Some.[ Left.1 Right.y Neither ] Ok.Leaf.9 }  -> SAME
  Shadow::Some: Some.1  -> SAME
  Shadow::None: None  -> SAME
  Shadow::Ok: Ok.2  -> SAME
=== R2 nested variant payload path labels vs tree position
  Tree::Node derived: 0 mismatches
  protos::Extent hand-written: 3 mismatches
    MISMATCH labelled [] actual [1] form Struct([Datom { path: [0], form: Bare("3") }, Datom { path: [1], form: Bare("7") }])
    MISMATCH labelled [0] actual [1, 0] form Bare("3")
    MISMATCH labelled [1] actual [1, 1] form Bare("7")
  datom_codec::Error hand-written: 1 mismatches
    MISMATCH labelled [] actual [1] form Struct([Datom { path: [1, 0], form: Bare("Datom") }, Datom { path: [1, 1], form: Vector([Datom { path: [1, 1, 0], form: Bare("1") }]) }, Datom { path: [1, 2], form: Bare("Budget") }])
  Error text: Error.{ Datom [ 1 ] Budget }
```
