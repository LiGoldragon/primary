# OpenCode seat

One OpenCode main-flow seat answered its first prompt on the local open-weight model and sent a message to 28d847 through the messenger, with no permission asked.

## Method

The seat ran from the built, undeployed Home generation of CriomOS-home `d029e60f`: its wrapped `opencode` package (1.18.16, external skill trees off), with that generation's declared `opencode.json` and `tui.json` given through `OPENCODE_CONFIG` and `OPENCODE_TUI_CONFIG`, and the generation's `opencode-local-model` command run as a transient user unit (llama.cpp 10273 Vulkan, Qwen3.6-35B-A3B UD-Q3_K_XL, attention on the integrated GPU, experts on the CPU, loopback port 11435).

It was started by `tools/opencode-main-flow-launch.mjs --model criomos-local/qwen3.6-35b-a3b --aspect Mind --flow-id 28d847`, carrying flow 28d847. The brief asked for three lines (birth skills; aspect, harness and model; next step), then one `hm-send` to 28d847, then the receipt.

The account below is read from `opencode export` of the session and from the Herdr pane record.

## Observed

- Launcher, step by step: pane `w1:p1W`; session `ses_efb87fbf8ffeNiz8sYspte4ulU` reported to that pane by source `herdr:opencode` (Herdr's own OpenCode plugin, loaded from the generation); one accepted prompt whose leading block is main-flow from `.opencode/skills`; agent `main-flow`; model `criomos-local/qwen3.6-35b-a3b`; Herdr agent `mind_qwen_28d847_te4ulu` bound to the session.
- Every assistant message ran under agent `main-flow` on provider `criomos-local`, model `qwen3.6-35b-a3b`.
- Eleven shell commands ran and none asked for a permission. Among them were `flow-id`, then `flow-id codex --flows-root /home/li/primary`, both refused, and directory listings under `flows/28d847`. The brief said to claim no Flow ID, and the main-flow system prompt says not to do bounded work.
- `FLOW_ID=28d847 hm-send 28d847 'OpenCode witness: main-flow seat answered on the local model; this message came through hm-send.'` printed `Transported.{ 28d847 working }`.
- The final answer: "Skills: main-flow, spirit, psyche, psyche-interraction, vocabulary, edit-coordination." / "Aspect: OpenCode witness seat. Harness: OpenCode. Model: qwen3.6-35b-a3b (criomos-local)." / "Next: report this receipt to the living and stop." / "Receipt: `Transported.{ 28d847 working }`". It named the birth skills correctly. It gave its aspect as "OpenCode witness seat", not Mind.
- Time from the first prompt to the final answer: 19:12:16 to 19:43:35. The first model call was a 16,879-token prompt, taking 769 s at about 22 tokens per second. The final turn's context was 22,946 tokens.

## Not established

- That 28d847 read the message: `Transported` is Herdr's acceptance only.
- Behavior after Home deployment: the user's live `~/.config/opencode` was not changed, and its retired plugin entries were still present beneath the overlay.
