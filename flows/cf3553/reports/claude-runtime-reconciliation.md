# Claude runtime reconciliation

On 2026-09-18, `/home/li/primary` contained stale owned
`tools/claude-native-seat-refresh.py` SHA-256
`5eac09f19434eabf70ac9d014dfdafdad029b3072ec867481ffcc89a5edac759`.
It is preserved under `forensic/` and was replaced only with the published
remote helper set.

Live/runtime hashes after materialization:

- `claude-bootstrap-controller.py`: `abb57966fe33cfe6222c15ff03c11877c06e5593ea11006965e916483497672f`
- `claude-bootstrap-controller.test.py`: `baf1b3879e8fc8024d2dbeb75751ee860ec31696359e9d896d91fcf660b9a2c1`
- `claude-native-seat-refresh.py`: `6e9e784f136a11a487406ec6772f621c4014c0a18c3af457fed096efc611969b`
- `claude-native-seat-refresh.test.py`: `a6e33a531e8e7654eede9da979febda711df87d4800f06e8880401131c8c165f`

Both published test suites passed. The unrelated Field Sol launcher was not changed.
