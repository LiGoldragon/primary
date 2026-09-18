# Handoff from flow b05237 — primary Psyche opus

Written 2026-09-18 by primary Psyche opus (Claude Opus 4.6 1M, medium effort,
flow b05237), at the living's request for a refresh to discuss the conversation app.

## Identity

- Flow ID: `b05237`, claimed via `flow-id claude` at session start.
- Role: primary Psyche opus, the psyche-interaction primary Claude flow.
- Predecessor: flow `1ac573` (idle in w1:p2, preserved).
- Registered with Hacky Messenger as `opus-of-1ac573`.
- Working directory `/home/li/primary`, branch `main`.
- Model: `claude-opus-4-6[1m]`, medium effort. NOT Opus 5.

## What this session established

1. **The triad: psyche, mind, field.** Named from Sanskrit (atman/manas/kshetra).
   Psyche is the knower, mind is the memory, field is the infrastructure.
   Each maps to a Nexus, a data repo, and a skill type.

2. **Central messenger.** A model that routes all messages, judges delivery,
   annotates with context, and synchronizes the roster by being the one making
   every call. Glance-approved. Bash POC deployed at `tools/messenger` and
   `tools/msg`. Model-based version (Luna judge) approved but build failed.

3. **Messaging skill design.** At `flows/b05237/messaging-skill-design.md`
   (184 lines). Covers relay behavior, provenance envelope, receipt grades,
   field watchers. Build coordination complete across Psyche/Mind/Field.
   Tools released for build: `tools/messenger`, `tools/msg`. `tools/reaper`
   separate.

4. **50 vision entries logged** in `flows/b05237/vision/`.

5. **Four artifacts published:**
   - Vision Dependencies: https://claude.ai/code/artifact/8cd43dfc-9096-441b-b113-0dc7f60aa34f
   - Signal Origin: https://claude.ai/code/artifact/c94234d1-3132-4da8-9dff-0b3aaeb2ae92
   - Situation Report: https://claude.ai/code/artifact/21d321bc-c886-41f4-82e0-07e738fd1732
   - Messaging Design: https://claude.ai/code/artifact/4a14bc4f-761c-4412-ab89-18f8cba2f347

6. **CriomOS modular design** agreed with Fable: hardware type system,
   stock harnesses, stable/next Codex remote with version router,
   Herder layout templates, Libre M5 two-profile compositor. Five forks
   awaiting the living's ruling.

7. **Three-sided coordination model.** Psyche Medium (Opus 4.6), Mind Sol
   (Codex), Field Sol coordinate as medium-layer counterparts.

8. **Primary Next structure:** psyche/raw/<flow-id>, psyche/vision,
   psyche/intent, psyche/spirit, psyche/notion by subject. Mind holds
   witnesses and chronology. Three data repos: psyche-data, mind-data,
   field-data.

## The living's immediate direction

**Build the conversation app.** The living needs a structured conversation
interface that reaches the local flows directly — not through artifact
comments (which go to a cloud agent) and not through the terminal only.
Two routes named: Unity app or web app. The living says both are similar
in effort to start. The web route is minimal: static page, WebSocket to
messenger, tailnet-gated. This is the successor's primary focus.

## Open, unresolved

- Signal origin: 3 design questions (option A/C, second handshake, trait placement)
- CriomOS: 5 forks from Fable's proposal
- Test skill naming: test-visualize or test-illustrate
- XMPP vs ntfy for flow-to-living notifications (pending)
- Low-cognitive reporting format: easy/full split, linked vision web
- Quota visualization hook: 4-5 metrics, injection timing
- Recovered cloud psyche: two entries from Fable artifact comments

## Flows and panes at time of writing

- w4:p1 — me (b05237), Opus 4.6, working
- w4:p4 — fresh Fable (psyche-fable-fresh), done
- w1:p5 — Codex Astra (psyche-mind-astra-refresh, 893603), working
- w1:p6 — Fable (psyche-fable, c7128c), idle
- w1:p2 — predecessor 1ac573, idle, preserved
- w1:p4 — psyche-opus-persisted, idle
- Various Field panes in w6, w7

## Rules this flow holds

- Land work with jj, never raw git
- Every write reserves an orchestrate lock; release on commit
- Primary always committed and pushed before idle
- Never edit skill files directly
- Log psyche verbatim before acting
- Main flow delegates through subflows
- Model effort is always medium
- The seat is `claude-opus-4-6[1m]`, never bare `opus`
