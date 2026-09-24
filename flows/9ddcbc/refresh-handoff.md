# Refresh handoff — Field Medium 9ddcbc

The living ended this flow for context cost on 2026-09-24. Do not resume implementation here. The incoming main is **Field Sol**, behavioral **Field Medium**, exact **gpt-6-sol medium**, launched only through the corrected deployed Flow Nexus on the next Codex server. Title: `Field Sol <new Flow ID>`. Preserve 9ddcbc until successor startup, identity, route, title, handoff, and target-read receipts; retirement is a separate lifecycle act.

## Current runtime boundary

- Stable Codex and the next Codex server are both active on separate sockets. The next server is Codex 0.158 alpha 9 and has completed GPT-6 Sol/Luna test turns.
- Active Flow Nexus is still old 0.3. It cannot launch the successor coherently. No direct/manual bypass is allowed.
- EB `eb7bae` is the sole deploy executor. First deployment packet must contain one coherent Flow CLI + meta CLI + daemon + patched Herdr + stable/next Codex package graph.
- Field Low `df09b6` owns the first bounded live acceptance after deployment: exactly one disposable GPT-6 Luna medium Start through Flow. Existing mains remain untouched.

## Landed Field work

- Primary `3045fcb`: launcher models/endpoints, Fable/Opus titles, one-block startup composition, transcript receipt, omission repair, refusal gates. Five focused suites passed.
- Curriculum `43c6075`: main-flow and refresh startup contract.
- Mind successor packet `717ee7d`: `flows/9ddcbc/mind-successor-20260924/`; no launch. Mind 6288d1 remains crossover and its lock-5200 worker must report to its successor.
- Psyche Fable `752e0f` and Psyche Opus `e51411` are ready on the old launcher. They refresh through Flow only after Codex migration works.
- Opus 4.6 flow `b80e55` was retired, its pane closed, transcript preserved, and payload sent to e51411. Evidence: `flows/9ddcbc/retirements/b80e55-2026-09-24.md`.
- Field High handoff: `field/9e735b/refresh-handoff.md` on its published Field branch.

## Active source owners

1. **Mind 6288d1 / lock 5200 — Flow adapter only.** Exact model/effort selects stable or next endpoint; existing bindings retain recorded endpoint. Start remains Pending until one-block startup and native receipt match. `MetaConfirmExisting` is not a new-Start gate.
2. **Field worker `herdr_codex_executable` — Home/Herdr boundary.** Upstream Herdr is read-only, so implementation is a CriomOS-home patch/override. Herdr receives an explicit immutable executable. Home exposes a home-setting-only client wrapper: set exact Codex home, exec raw Codex with arguments unchanged, add no `--remote`. Flow owns the single remote flag and must use the same wrapper for native start, proxy, receipt, and refresh. Required Flow environment variables are the stable/next CLIENT, SOCKET, HOME, and MODELS sets; lists are disjoint. New next models include GPT-6 Astra, Sol, Luna; Terra 5.6 stays stable unless later proven otherwise.
3. **Field worker `main_flow_system_mode` — main-only harness instructions.** Main seats need a living-owned replacement system prompt that requires delegation; subagents keep stock prompts. Claude reminder hook is per native session. Codex equivalent must be verified, never invented.

Both workers were told to stop at a coherent checkpoint, commit/push only tested scope, and report directly to Mind 6288d1 and the incoming successor. Their final receipts may arrive after this handoff.

### Home/Herdr boundary receipt

The Home-owned Herdr boundary is tested and pushed on CriomOS-home branch
`field/codex-next-9e735b` at remote revision
`524f3993d90dc8efd5eb49cddfea8e8fa6f652c5` (`4cbdacec` plus
`524f3993`). It patches the pinned Herdr source without an upstream branch.
`herdr agent start` now accepts `--executable` for Codex, requires an exact
absolute executable from the configured immutable allowlist, refuses missing
or unavailable selections, preserves canonical `codex` when omitted, and
records the selected executable in start and managed-agent evidence.

Home exposes immutable stable and next Flow client wrappers. Each wrapper only
exports its exact `CODEX_HOME` and execs its raw Codex package with arguments
unchanged; neither adds `--remote`. Flow owns the single remote flag and calls:

`herdr agent start NAME --kind codex --executable "$FLOW_CODEX_NEXT_CLIENT" -- --remote "unix://$FLOW_CODEX_NEXT_SOCKET" --model MODEL -c model_reasoning_effort=EFFORT`

`flow.nix` supplies the stable/next `CLIENT`, `SOCKET`, `HOME`, and `MODELS`
variables. Stable models are GPT-5.6 Terra/Sol/Luna; next models are GPT-6
Sol/Luna/Astra; the sets are disjoint. The focused Rust selection/refusal test,
Home contract check, and existing Codex-next check passed. No deployment,
restart, or seat launch occurred. EB must integrate this exact Home revision
into the coherent package graph before any Start.

### Main-flow system-mode checkpoint

The `main_flow_system_mode` worker wired the main-only boundary in
`tools/native-batch-refresh.mjs`. The single authored replacement is
`tools/main-flow-system-prompt.md`; Claude mains receive it with
`--system-prompt-file`, and Codex mains receive it with
`model_instructions_file`. Both harnesses receive a `UserPromptSubmit` command
hook backed by `tools/claude-main-flow-reminder.py`, with cadence configured by
manifest `mainFlowReminderEvery` (default 6) and counters keyed by native
session ID. The launcher passes none of these options for a worker/subagent
launch. Missing or empty replacement prompt files fail before launch.

Focused fixtures prove replacement rather than append, main/worker separation,
missing-file refusal, independent per-session cadence, retained Claude startup,
and both harness argument shapes. Local Codex 0.153.4 accepted the exact
`model_instructions_file` plus inline `hooks.UserPromptSubmit` configuration;
its official current hook contract confirms command `UserPromptSubmit` and
developer-context output. No seat was launched, restarted, or deployed.

## Startup rules from the living

- Humans never type launcher commands.
- The launcher composes `main-flow` and other startup-only skill bodies into one startup prompt block. User-only flags remain so models/subagents cannot load those skills themselves.
- A forgotten startup skill may be injected afterward by the launcher as a verified repair; that is not the normal path.
- For Claude, do not rely on slash commands inside a Herdr pasted block. Compose the withheld skill bodies as text at the top.
- Main flows delegate implementation to workers. Main context carries coordination, decisions, receipts, and compact handoffs.

## Next sequence

1. Receive tested Mind Flow adapter and tested Home-patched Herdr revisions.
2. EB builds and activates one coherent package graph; prove installed/source parity and service/socket health.
3. Field Low runs the one disposable Flow Start and verifies selected next wrapper/socket/model, one-block startup, Flow ID, HM/title, native turn, and receipt.
4. Launch the incoming Field Sol successor through Flow using this handoff; preserve 9ddcbc until readiness.
5. Refresh remaining Codex mains one at a time, then Claude mains. No duplicate launches or bulk retirement.
