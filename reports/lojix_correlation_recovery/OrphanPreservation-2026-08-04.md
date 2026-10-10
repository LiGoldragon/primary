# Lojix orphan preservation — 2026-08-04

This records nonsecret fingerprints before clean-main correlation work. These
recovery commits are local-only: they were neither merged nor pushed.

| Repository | Pre-recovery change fingerprint | Changed paths | Recovery commit | Recovery bookmark | Clean fetched main |
| --- | --- | ---: | --- | --- | --- |
| `meta-signal-lojix` | `9951abf7bce2d66cdc55040fad2eaecf10a961680d34acb1d9d398892eadafa8` | 3 | `f81433a3` | `recovery/meta-signal-lojix-orphan-20260804` | `b7f5968b` |
| `signal-lojix` | `d8e21af413f4a3c8f94a76c1ce668f0c54c2e28e50f41e23da23353351390b05` | 7 | `40ef16a5` | `recovery/signal-lojix-orphan-20260804` | `41f796fe` |
| `lojix` | `a2ac23dab63335250e79c459532c7575be90578ca936a2cadff096cf794fed0a` | 20 | `1d0a61b1` | `recovery/lojix-orphan-20260804` | `15e25e0a` |

The stale `meta-signal-lojix` and `signal-lojix` workspaces were first updated
with `jj workspace update-stale`; their former diffs became divergent parent
commits, then received the explicit recovery descriptions and bookmarks above.
Each active workspace was then moved to fetched `main` and verified clean.
