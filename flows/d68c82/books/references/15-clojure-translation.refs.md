# References: The shared Clojure translation pattern

Source: flows/d68c82/books/15-clojure-translation.md

- flows/df159a/vision/clojure.md:3-9
- flows/d68c82/vision/ethos.md (2026-10-14 entries)
- flows/55a2b4/books/15-flow-nexus-whole.md:384-422 («The Flow Nexus, whole», P3)
- flows/55a2b4/books/14-short-term-prototypes-clojure.md («Short-term prototypes: Clojure now?»)
- Origin: Mind Prototyping Secondary, flow e4b7d7

## Edition 2

- Example run: bb with metosin/malli 0.18.0 loaded from bb.edn; all five expected results held (true, false, true, true, false); no fix to the example. Scratch: /tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/clj-example/. The code is reformatted for width only (readers uses #(...)); the reformatted form was not rerun separately.
- Host: field-clj a2c278 dirty; deps.edn Clojure 1.12.6 and Malli 0.18.0; JVM test aliases; no bb runner; executor unassigned.
- Untested: the forward/inverse value adapter needed to test recovery; Option/Result beyond the nested Option case; struct positions and vectors in code.
- Test plan: fixture checks Person, Accepted, Refused, Pending, vectors, None, Some(None); rejects missing or extra fields, wrong scalars, unknown tags, malformed payloads.

## Edition 2 rerun receipt

- Date: Wed Oct 14 06:10:13 PM UTC 2026
- bb version: babashka v1.13.219
- File digests (sha256sum):
```
3726c4b9775abf87d612ad1fc03c6d7780d5ffff4283d83c563c79842b8d83c9  bb.edn
39e167387aee0097ce2a097d65bcf095b0f32fade0e8fb02264bb2dd4db4825b  src/translation_example.clj
```
- Working directory: /tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/clj-example/
- Command: `bb src/translation_example.clj` (exit status 0)
- Full output, as printed:
```
true
true
true
false
true
```
- The five printed results map to source lines: 1 = line 35 (Reply on accepted Ada 36): true; 2 = line 52 (NestedOption on absent): true; 3 = line 54 (NestedOption on present-absent): true; 4 = line 56 (= absent present-absent): false; 5 = line 58 (NestedOption on present-absent): true. Line 37 evaluates without printing, so it is not counted.
- Scope: this rerun covers the reformatted file as it stands on disk. The earlier record reran only cases 1 and 2 after reformatting; this run covers all five printed checks.

## Rerun receipt, corrected

- Date: Wed Oct 14 06:10:35 PM UTC 2026
- bb version: babashka v1.13.219
- File digest (sha256sum):
```
2bd0e91c1b49349a8683695df9c819e58cac93650a2733fc8daeaaeaa1d8ab53  src/translation_example.clj
```
- Working directory: /tmp/claude-1001/-home-li-primary/d68c8272-6db0-47dd-9c8e-538d95ff12a6/scratchpad/clj-example/
- Command: `bb src/translation_example.clj` (exit status 0)
- Output, as printed:
```
true
false
true
true
false
```
- Mapping of printed lines to the five cases:
  1. line 35, Reply accepted (Ada, 36): true
  2. line 37, Reply with :age "36": false
  3. line 52, NestedOption absent: true
  4. line 54, NestedOption present-absent: true
  5. line 56, equality (absent = present-absent): false
- Changes from the prior run: line 37 now wraps its validate call in println; the duplicate NestedOption present-absent print at former line 58 is removed.
