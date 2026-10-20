# Clojure demonstration v2 evidence manifest

This manifest retains the attributed Babashka execution evidence beside the
separate, unexecuted JVM v2 handoff. The execution is attributed to Mind
Prototyping flow `d68c82`; this flow only reviewed the cited receipt and hashed
the retained snapshots. It did not rerun the command.

## Frozen Babashka snapshots

The retained source is `src/translation_example.clj` and its SHA256 is
`2bd0e91c1b49349a8683695df9c819e58cac93650a2733fc8daeaaeaa1d8ab53`.
The retained config is `bb.edn` and its SHA256 is
`3726c4b9775abf87d612ad1fc03c6d7780d5ffff4283d83c563c79842b8d83c9`.
The config contains Malli `0.18.0` and the `src` path.

The source receipt is the retained copy
`15-clojure-translation.refs.md`, copied from
`flows/d68c82/books/references/15-clojure-translation.refs.md`, lines 40–57
(the corrected rerun receipt).

That receipt reports Babashka `v1.13.219`, command
`bb src/translation_example.clj`, exit status `0`, and printed results:
`true`, `false`, `true`, `true`, `false`. It attributes the five cases to
Reply accepted Ada age 36, wrong age string, nested absent Option, nested
present-absent Option, and inequality.

The receipt records the corrected source after removing the duplicate print and
adding the wrong-age `println`. The receipt is the execution witness; the
retained source and config are hash-matched snapshots reviewed here.

## JVM handoff separation

The unexecuted JVM artifact is
`../clojure-demonstration-v2.md`, SHA256
`10e3069d00c2d97a60cc9d8531a85ba0259fbc1528ee13facad8ae474d42a0f8`.
The unchanged original is
`../clojure-demonstration-v1.md`, SHA256
`3a122f9e1f87f5e04ffbb665a7350f04fdeea80ebdc7def5dac46eb4e4cec1bb`.
The Babashka execution does not witness either JVM artifact.

## Provenance boundary

The receipt supplies the runtime version, command, exit status, output, and
source/config identities. This flow's observation is a receipt and hash
review, not an independent rerun or a claim that the JVM handoff executed.
