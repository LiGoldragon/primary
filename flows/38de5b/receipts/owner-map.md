# Owner map witness — 2026-09-25, observed from 38de5b (read-only)

## `hm-list` raw output (relevant rows only, full output captured in this session)

```
FLOW	AGENT	SESSION	STATE
-	psyche-haiku-of-b80e55	messaging-build	idle
d8df70	psyche-opus-5	messaging-build	done
752e0f	psyche-fable-of-836818	messaging-build	done
e51411	psyche-opus-of-d8df70-r2	messaging-build	done
-	psyche-opus-b87854	messaging-build	idle
-	psyche-fable-refresh-5f38bc	messaging-build	working
00f95a	mind-sol-00f95a	messaging-build	working
26c50c	mind-astra-26c50c	messaging-build	done
5f38bc	field-astra-5f38bc	messaging-build	done
b7da5d	field-sol-b7da5d	messaging-build	done
e71dab	field-luna-e71dab	messaging-build	done
-	codex-2d0e71a77a40543c10ac8ac1	messaging-build	idle
cf3553	field-astra-of-33ba2b	messaging-build	STALE
... (remainder STALE, older flow ids not in the bundle list)
```

Note: no row anywhere in the full listing carries FLOW column `38de5b`. This
seat's own pane appears under AGENT `psyche-fable-refresh-5f38bc`, FLOW `-`
(unregistered), STATE `working`.

## `herdr agent list` raw (relevant fields, JSON trimmed to name/title/status)

- psyche-opus-5 — "Psyche Medium d8df70" — done
- psyche-fable-of-836818 — "Psyche Fable 752e0f" — done
- psyche-opus-of-d8df70-r2 — "Psyche Opus e51411" — done
- psyche-fable-refresh-5f38bc — "Psyche Fable 38de5b" — working — agent_session
  value `38de5bbb-be48-4bae-883e-2d622fb79c9e` (matches this session's own id)
- mind-sol-00f95a — "Mind Sol 00f95a | primary" — working
- field-astra-5f38bc — "Field Astra 5f38bc | primary" — done
- field-sol-b7da5d — "Field Sol b7da5d | primary" — done
- field-luna-e71dab — "Field Luna e71dab | primary" — done

d8df70 appears as pane title "Psyche Medium d8df70" (agent name
psyche-opus-5), not as a separate live crossover pane; no second d8df70 pane
was found.

## Table (observed = O, inferred = I)

| Bundle name | Flow ID | Alive | Registered (FLOW col) | Notes |
|---|---|---|---|---|
| Psyche Fable | 752e0f | yes (O, state=done, pane present) | yes (O) | |
| Psyche Opus | e51411 | yes (O, state=done, pane present) | yes (O) | |
| Mind Sol | 00f95a | yes (O, state=working) | yes (O) | |
| Field Astra | 5f38bc | yes (O, state=done, pane present) | yes (O) | |
| Field Sol | b7da5d | yes (O, state=done) | yes (O) | |
| Field Luna | e71dab | yes (O, state=done) | yes (O) | |
| d8df70 (crossover) | d8df70 | yes (O, pane title "Psyche Medium d8df70", state=done) | yes (O) | bundle called it crossover-finishing; title now reads as Medium, not clearly separate crossover pane (I) |
| This seat | 38de5b | yes (O, own session, state=working) | no (O — FLOW col is `-`) | title shows "Psyche Fable 38de5b" but registry has not bound Flow ID 38de5b yet |

"Alive" here means: present in `herdr agent list` with a live pane/state
(done/working/idle), as opposed to STALE/absent in `hm-list`. This is Herdr's
own state label (O), not a stronger claim about process liveness underneath.

## Differences from the bundle's list

- All six named Flows (752e0f, e51411, 00f95a, 5f38bc, b7da5d, e71dab) match
  the bundle: present, alive, registered. (O)
- d8df70: present and alive, but not distinctly visible as a separate
  "crossover" pane — its title/agent name reads as the Medium line
  (psyche-opus-5 / "Psyche Medium d8df70"), consistent with the bundle's
  note that Medium succession was assigned to e51411 while d8df70 remained
  crossover; no second, separately-titled d8df70 pane was found (I).
- 38de5b (this seat): alive and present in `herdr agent list` with title
  "Psyche Fable 38de5b", but **not yet registered** — `hm-list` shows FLOW
  `-` for this pane, not `38de5b`. So its registration has not landed. (O)

## Skip-permissions default

- `flows/e51411/reports/claude-skip-permissions-audit.md` (dated
  2026-09-24): audit found no launch path sets
  `--dangerously-skip-permissions` or `defaultMode` by default (except the
  disabled/obsolete paths and `agent-intercom cci`); recommends Option 1
  (Nix-managed `permissions.defaultMode: "bypassPermissions"` in
  CriomOS-home), **not yet applied** at audit time. (O, from file)
- `flows/5f38bc/log.md`: no line mentions skip-permissions at all (grep
  returned nothing). (O)
- `flows/752e0f/refresh-bundle.md` "State of the world": explicitly lists
  this as still "Blocked" — "the fix is a settings default in CriomOS-home
  plus the skip flag in five launch paths ... Field's to land." (O)
- Conclusion: **not landed** (O, corroborated by two independent file
  sources, no contradicting evidence found).
