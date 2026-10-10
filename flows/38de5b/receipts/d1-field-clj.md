# D1 field-clj path rule — receipt

Task D1 of flows/e51411/reports/audit-flow-messenger-field.md. Ruling: e51411 (exactly the named paths; other dirty paths ignored).

- field-clj main: 212cf38f -> 9026513cf9160cd720a7c65f86db8828318eb87c "Ratify exact-named-paths commit rule". `git ls-remote https://github.com/LiGoldragon/field-clj.git` shows 9026513c. Commit files: README.md, src/field_clj/core.clj, test/field_clj/core_test.clj.
  - README: new "Path rule" section. core.clj: rule in execute-commit docstring; behaviour unchanged (it already enforced the rule).
  - New tests: multi-path commit beside two other dirty paths (never passed to jj); clean named path among dirty ones refuses `:missing-paths` before commit; `@-` missing a named path refuses `:committed-path-scope-mismatch` before bookmark and push.
- Tests (`clojure -M:test`): before 8 tests, 19 assertions, 0 failures; after 11 tests, 30 assertions, 0 failures, 0 errors.
- Curriculum main: 569cb5f7 -> c455e38b98d58a1183b2b3bb5ad8ec4870387adf "State field-clj path rule in file-editing" (skills/file-editing.md only). Remote confirmed. Generated trees not regenerated (pack did not ask).
- Not done: flows/00f95a/launches/field-clj-brief.md step 2 still says "Refuse if any other path is present"; it is 00f95a's launch record, left for its owner. D2 not started.
- Locks 6335 (field-clj clone) and 6339 (Curriculum) released.
