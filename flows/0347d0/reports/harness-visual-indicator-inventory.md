# Harness visual indicator inventory

This Field Terra lane implements the living's harness-display direction recorded
in `flows/753e69/vision/harnessVisualIndicatorsAndRemoteControl.md`. The bounded
collector is `tools/field-census/harness-visual-indicators.mjs`; its focused
tests are beside it. It reads one exact Herdr pane's visible viewport, pane
metadata, and foreground process. It emits structured observations without
emitting raw terminal content.

## Evidence contract

| Grade | Source | Permitted conclusion |
| --- | --- | --- |
| `machine` | Herdr pane/process metadata | Harness kind and exact binding fields exposed by Herdr. |
| `text-pane` | Visible TUI footer or visible error | Displayed model, effort, context percentage, `/rc` feature indicator, or explicit failed authentication. |
| `model-visual` | Optional caller-supplied review of a full-screen image | Remote Control indicator visible when the structured review is complete and medium/high confidence. |
| `unknown` | Missing, ambiguous, partial, or rejected evidence | No positive or negative claim. |

The Claude `/rc` footer glyph establishes only that Remote Control is displayed
as enabled. It does not establish an authenticated account, a reachable URL,
or attachment by an external client. Those fields remain separate and unknown
unless independently observed. The collector does not treat command history
such as `❯ /rc` or prose mentioning `/remote-control` as a footer indicator.
Absence of an accepted indicator remains unknown rather than disabled.

The optional visual observation is fail closed. It must declare a full-screen
observation, the exact `remote-control-indicator` fact, a reviewing model,
medium/high confidence, and an enabled boolean. Only a positive enabled result
is promoted; partial, malformed, low-confidence, error, and negative inputs
remain unknown. The input is bounded to 64 KiB. Screenshots stay outside the
JSON result, and callers must exclude or redact OAuth URLs, pairing codes,
tokens, secrets, and private prompts before model review.

## Current harness inventory

| Harness | Installed evidence | Visible indicators currently understood | Gap |
| --- | --- | --- | --- |
| Codex CLI 0.153.4 | Existing Field runtime audit | `gpt-*` model, effort and lifecycle/context footer text; process argv identifies Codex | No accepted TUI Remote Control glyph has been documented. App-server `--remote-control` is process configuration, not external reachability. |
| Claude Code 2.1.263 | Existing Field runtime audit | Named model/effort, context percentage, login errors, and `/rc` footer glyph | A screenshot capture primitive and authenticated remote URL/client receipt remain absent. |
| Other harnesses | No installed executable witnessed in the Terra inventory | None | Preserve as unknown until installed and observed. |

## Usage

```sh
node tools/field-census/harness-visual-indicators.mjs \
  --session messaging-build --pane wD:p7
```

An optional visual reviewer writes a small JSON observation and passes it with
`--visual-observation FILE`. This script does not call a model or capture a
screenshot itself because the current Herdr surface exposes pane text and ANSI,
but no image capture command. A future image adapter should capture the entire
pane, redact sensitive regions before inference, retain an evidence locator,
and produce the bounded observation schema consumed here.
