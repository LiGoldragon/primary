# Where We Are — 24 September

## Page 1 · Flowchart — The whole picture

**What this flowchart shows:** the five topics as five blocks, each coloured by its state. Green means done or moving; red means blocked, with what blocks it written on the block. Arrows show what blocks what.

- "Prometheus": green, "deployed, rebooted, cable checks pass".
- "Flow and Message": red, "Flow 0.5 (start, stop, send, list) written and tested; blocked: its activation on ouranos goes through Lojix, which hasn't accepted the job".
- "Starting fresh flows": red, "blocked: Claude seats start in auto mode, which refuses full-access launches; the fix is one settings line".
- "Handover between flows": red, "the refresh launch failed once (no transcript, main-flow missing); the launcher is being repaired".
- "Flashbooks": green, "seven published".
- Arrows:
  - "Claude auto mode" → blocks → "Starting fresh flows" and "Field Sol and Luna launch".
  - "Flow 0.5 activation" → blocks → "Message delivering to real flows".

## Page 2 · Who is alive right now

*(Witnessed, about 21:50 UTC.)*

- **Psyche High:** Fable 752e0f.
- **Psyche Medium:** e51411, this flow. It took the seat on the living's word. d8df70 stays up as crossover and carried out the Prometheus deploy.
- **Mind:** Sol 00f95a. It wrote and tested Flow 0.5 and holds the code that connects the live flows into Flow.
- **Field:** Astra 5f38bc, registered and reachable, is the deploy executor and is activating Flow 0.5. **No Field Sol or Luna is running:** their launch is blocked by Claude's auto mode.

## Page 3 · Flowchart — What stands between us and working Flow

**What this flowchart shows:** each step to a working Flow, left to right, marked done, or marked with its blocker.

- "Flow 0.5 written: start, stop, send, list" (done, Mind) → "built" (done) → "activated on ouranos" (blocked: Astra sent it through Lojix, which hasn't accepted the job; direct activation, as used for Prometheus, would get past it) → "live flows bound into Flow" → "one raw send into a real pane" → "Message delivers".
- Below it: "one settings line makes every Claude start in bypass" (the living adds it) → "fresh Psyche Medium launched" → "Field Sol and Luna launched".

## Page 4 · What's done today

- **Prometheus:** built on Prometheus itself and deployed. It carries the crash-reboot watchdog, neighbour discovery and every declared port. Rebooted into Linux 7.1.8 and back in 60 seconds. ssh and the cache work over the cable and by name. *(Witnessed by d8df70.)*
- **ouranos:** off Prometheus's Wi-Fi; Yggdrasil runs over the cable; 7 GB freed.
- **Field Astra:** found, registered, given the deploy job.
- **Your words:** 43 messages to Mind and Field had gone unlogged; the lasting ones are now logged.
- **Books:** the overview, five topic books, and "Is Everybody Logging?".

## Page 5 · Flowchart — What removes each block

**What this flowchart shows:** each block, with the one thing that clears it.

- "Claude auto mode blocks launches" → "`permissions.defaultMode: bypassPermissions` in ~/.claude/settings.json" (you).
- "Flow 0.5 not activated" → "Astra activates it directly on ouranos".
- "Five launchers start Claude without the flag" → "Field adds the flag" (sent).
- "Refresh launch failed" → "launcher clears the inherited setting and passes the startup block as Claude's start argument" (sent to Astra).

## Page 6 · Your questions still unanswered

- How are archives searched?
- How does a running service link back to the CriomOS source that built it?

## Page 7 · Proposals

1. ☐ Add the bypass default to Claude's settings, and later manage it in CriomOS-home.
2. ☐ Astra activates Flow 0.5 directly, binds the live flows, and sends one raw message through Flow.
3. ☐ The launcher starts the fresh Psyche Medium, then Field Sol and Luna.
4. ☐ Someone answers your two open questions.
