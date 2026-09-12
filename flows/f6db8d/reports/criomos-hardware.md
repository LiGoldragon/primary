# Hardware classification in CriomOS, and the metal fixtures

Subflow thread `f6db8d14-1dfe-472d-914e-9c441f852834` of flow f6db8d,
2026-09-12. Brief: implement `reports/design-decisions.md` item 5 — recompute
what `modules/nixos/metal/default.nix:37` and its neighbours need from the live
Horizon fields, in CriomOS itself, with no host-name heuristics and no defaults
that silently disable ThinkPad battery/thermal/lid behaviour; give the four
metal check fixtures the real producer's shape, generated from the pinned
`horizon-compose` where possible; make the whole `checks` output evaluate; then
drive the complete-system `BuildOnly` of `reports/lojix-criomos.md` §3 as far as
it goes. The coordinator added, mid-task, that branch `f6db8d-remote-only-builds`
lands on main first. Nothing was deployed: no activation, no switch, no
`lojix-meta` request, no running service touched.

**witnessed** — this thread ran the command or opened the file and the text
below is what came back. **relayed** — a named report or file says so; not
re-verified here. **this thread's inference** — reasoning, not a ruling.

## 0. What to read first

1. **CriomOS main moved twice.** `b84b99ba` → `79cc994a` (remote-only builds)
   → `8fcfbfec` (hardware classification). Both pushed and verified against the
   real remote URL (§5).
2. **The `modelIsThinkpad` stop is gone**, and the complete-system `BuildOnly`
   is past it (§4). The next stop is named in §4.3 and it is not in the
   hardware group.
3. **Two upstream defects were corrected on the way, not just relocated**
   (§1.3): `chipIsIntel` was derived from the architecture and so claimed Intel
   microcode and Intel GPU drivers for every AMD machine we own; and
   `ThinkPadE15Gen2Intel` and `ThinkPadX250` were never in the retired
   `KnownModel` table, so tiger has been running as a non-ThinkPad.
4. **`fixtures/horizon-node.nix` is producer output**, not a transcription
   (§2), and this run proved it against what `lojix` itself materializes.
5. **Two pieces of the item could not be landed**: registering the new check in
   `flake.nix` and dropping `typeIs.largeAiRouter` from
   `checks/lojix-ownership`. Both paths are inside Orchestrate lock 1227, still
   held by a sibling f6db8d subflow at the time of writing. §6.
