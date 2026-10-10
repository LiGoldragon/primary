# G1 messenger-clj: fallback sends reach the exact live pane

Task G1 of flows/38de5b/reports/audit-messenger.md, done by an Opus subflow of 38de5b on 2026-09-25, with the M1 launch-receipt fix Mind 00f95a asked for in its M1 review.

- Repository: github.com/LiGoldragon/messenger-clj
- Branch: `m1-sender-aspect-model-38de5b`, on top of M1 f592ede
- G1 revision: c72fc9df13b12cb1cf26c827c9f37f223f5fcf38 "Deliver fallback sends to the exact live pane"
- M1 fix revision: 5171131d465c0ee80806cb485bcb81300ff6766c "Require the launcher receipt to name the registering Flow"
- `git ls-remote` shows the branch at 5171131; main is still d4f2d08. Nothing was merged.
- Tests before, on f592ede: 44 tests, 0 failures, 0 errors, with 327 to 334 assertions across runs. The brief expected 329. The assertion count varies because the fake orchestrate in `concurrent-sends-wait-for-one-path-lock-with-unique-operation-names` runs one `is` for each Lock retry.
- Tests after, on 5171131: 52 tests, 0 failures, 0 errors, with 388 to 394 assertions. The command is the README's `bb --config bb.edn -e` run over the four test namespaces.
- The new G1 tests fail on f592ede with 16 failures, so they cover the gap.
- Untouched: `dist/`, `flake.nix`, `check.nix`, `nix/`, and the pane envelope.

## G1 change (src/messenger_clj/core.clj)

- `fallback-binding` normalizes every fallback route to the RouteBinding keys: session, name, pane_id, terminal_id, agent, and state "Fallback". This covers the stored-name, `--pane`, and Flow-title paths. The native thread is the stored one when the Flow has one and is absent otherwise. The zero-UUID placeholder is gone.
- Native-thread check: a fallback route with no stored native thread skips only the process check. A stored native thread is still checked, and a mismatch is Held ProcessMismatch. The exact Herdr identity check stays (name, pane, terminal and agent, before and after the prompt), and so does Herdr's `interactive_ready`.
- Held instead of a dump: a validation failure before the prompt, in fallback resolution or the Submitting record, is Held with a pending record and the new reason `InvalidBinding`. The printed line is only `Held.{ FLOW InvalidBinding attempt-… }`, with no Malli explain and no body. `held!` leaves out a binding that the closed schema refuses rather than raising a second failure.
- Grading: fallback is graded only Fallback-Presented, never Read. An unobserved presentation is Uncertain and is not retried.
- Presented observation, found while doing G1: `presented!` required a `:presented true` field. That field does not occur anywhere in Herdr 0.8.2's API schema (`herdr api schema --json`). A waited `agent.prompt` answers `agent_prompted` with the pane's AgentInfo. So under the old check, every live `--wait-presented` send and every fallback send could only end Uncertain. The check now requires `agent_prompted` for the exact pane, on a call that asked to wait.
- Wait states: the wait now names every state, `--until working|idle|done|blocked --timeout 10000`. Previously a plain `--wait --timeout 5000` waited for a settled state that a working agent does not reach in 5 s. This probably explains the audit's f5a74e Unknown. It is inferred from the schema and the Herdr help text; a live Herdr reply was not observed, as the next section explains.
- The test fakes (`test/fake-herdr` and the core tests) now return Herdr's real reply shape.

## M1 fix

`hm-register --launch-receipt` now refuses a `canonicalFlowId` that is missing, blank, whitespace or not a string, and one that names another Flow. Only a receipt naming the registering Flow gives the role. Test: `launch-receipt-must-name-the-registering-flow`.

## Disposable-pane evidence

- Pane: a new unfocused tab `wD:tH`, labeled `g1-disposable-G1MARK5b70be51`, whose root pane was `wD:pT` with terminal `term_65c550a4d612386`, in Herdr session messaging-build. It ran a bash receiver script that reports a Herdr lifecycle (`pane report-agent`, label g1shell) and appends each typed line to an observation file. The agent was renamed `g1-disposable-g1mark5b70be51`.
- Marker: `G1MARK5b70be51`
- The sends used the branch's own `bin/hm-send` against a temporary registry (`HM_REGISTRY` in the scratchpad) with FLOW_ID=38de5b. The sender route was the main pane wD:pR's identity, read and not touched.
- Send 1, at 21:06:12Z, with the intermediate build: `Uncertain.{ g1probe attempt-5e65bbe7-529 }`. Herdr refused `agent prompt` with `agent_not_ready: agent wD:pT is not an active named agent`. Nothing was typed: the observation file never appeared and the pane screen was unchanged. There was no retry. The fallback did pass resolution, normalization, the identity check and the Submitting record, and its ledger binding was pane wD:pT with state Fallback.
- Send 2, at 21:10:12Z, with the final c72fc9d code: `Held.{ g1probe NotReady attempt-f332a26e-3f0 }`, one pending record, nothing typed.
- Observation: no typed prompt was observed. Herdr 0.8.2 has no `interactive_ready` for a lifecycle-reported shell agent and refuses `agent prompt` to any pane that is not a detected agent, meaning one of the `agent start --kind` harnesses. So the brief's one typed prompt in a harmless shell pane cannot be done through HM's transport. It needs either a disposable detected agent (a real harness) or a ruling.
- Cleanup: `herdr tab close wD:tH` returned ok, and `pane get wD:pT` now returns pane_not_found. No live flow pane was touched.
