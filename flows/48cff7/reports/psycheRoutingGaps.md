# Psyche Routing Gaps

*Vision distillation proposal — pending living review*
*Flow 48cff7 · Primary MEDIUM · Opus 4.7 [1m] · 2026-09-16*
*Companion: `psycheRoutingMap.md`*

What the intended routing rests on that we have not yet built — badged on the same map so the missing pieces show against the whole.

## Figure — brief for a subflow to draw

Same base diagram as `psycheRoutingMap.md` — the 3×3 grid of stacks × effort tiers, the LIVING band, the arrows, the two bottom annotations. Redraw it in a subdued neutral (the diagram is the ground, not the message) and overlay a small amber circle carrying a gap number at each affected element. Each numbered dot maps directly to a numbered gap below.

Recommended placements:

- G01 — on the LIVING → LOW trunk (logged-psyche event has no defined source).
- G02 — one dot on each Claude LOW and Codex LOW box (LOW never launched).
- G03 — on the OPEN row (third stack unbuilt).
- G04 — on the LOW → MEDIUM arrow (packet format undefined).
- G05 — on the MEDIUM → HIGH arrow (escalation informal).
- G06 — on the MEDIUM ↔ MEDIUM mirror arrows (no router above the flows).
- G07 — on the LAYERS annotation (walk-up has no addressing spec).
- G08 — on the NON-PSYCHE INPUT annotation (funnel not enforced).

Gaps 9–14 are not visible on the diagram; keep them in the numbered list below.

The subflow can render this as its own image or by re-using the base map with an overlay layer.

## Proposed distilled Vision — psycheRoutingGaps

Each item is a gap the routing map depends on. Accept as a Vision statement to keep the gap named until it is closed.

- **G01 — Logged-psyche event has no defined source.** The transcript marker that says "the psyche just spoke" is not yet specified, so nothing wakes LOW. *(anchor: trunk from LIVING)*
- **G02 — No LOW psyche flow is launched in any stack.** The packager tier exists only on paper; MEDIUM is receiving raw living speech today. *(anchor: LOW column, Claude & Codex)*
- **G03 — The open stack does not exist.** Two of three peers are missing from every layer; the third-seat charter is still inactive. *(anchor: OPEN row)*
- **G04 — The self-contained packet has no format.** What LOW hands to MEDIUM — its envelope, its verbatim body, its context window — is unspecified. *(anchor: LOW → MEDIUM arrow)*
- **G05 — Escalation from MEDIUM to HIGH is informal.** No protocol says what triggers it, who authorizes it, or what carries across. *(anchor: MEDIUM → HIGH arrow)*
- **G06 — No router or mirror layer sits above the flows.** Same-effort mirroring across stacks is described as a rule, but each flow currently has to relay itself (this flow used `codex queue` by hand). *(anchor: mirror arrows)*
- **G07 — Layer walk-up has no addressing spec.** "Ascend until a psyche is found" has no name for layers, no lookup, no falls-back-to-core mechanism. *(anchor: LAYERS annotation)*
- **G08 — The non-psyche funnel has no enforcement path.** Non-psyche flows can still receive living input directly; nothing routes them through their layer's psyche. *(anchor: NON-PSYCHE INPUT annotation)*
- **G09 — The presentation flow is unbuilt.** First gatherer subflow, the image-making subflows it delegates to, and the stitching step all live only as description.
- **G10 — "What HIGH has said lately" has no owner.** The report the gatherer is meant to produce has no cadence, no landing place, and no consumer today.
- **G11 — No verbatim-psyche index exists.** Raw records are scattered across `flows/*/vision/`; the gatherer would have to sweep every flow to find them.
- **G12 — The trigger message does not encode routing.** The launch context for a psyche flow names its layer, role, effort, and stack only implicitly; the mirror and walk-up rules are not baked in.
- **G13 — The inline-report + CLI hand-off has no marker skill.** The intended flow — the main flow prints its report in its reply, then invokes a CLI that scans the transcript just above to find that report by explicit begin/end markers — is unspecified. A separator between report and the flow's own comment to the living is also owed, so the two are extractable independently.
- **G14 — No final-response hook produces a light visual report.** For at least the higher-effort psyche flows, the end of a turn should also emit a small distilled artifact — not yet configured anywhere.
