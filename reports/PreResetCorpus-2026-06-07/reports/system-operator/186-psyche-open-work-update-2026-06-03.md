# Psyche open-work update — 2026-06-03

## Privacy/access-gate commit audit

I read commit `597060b18a73` (`system-operator: record VSCodium editor default`) instead of leaving it as a vague risk.

Result: it is not an API-key or secret-byte leak. It does not contain Cloudflare tokens, passwords, private keys, or decrypted secret values. It is over-broad because it combines the system-operator editor-link report update with counselor/assistant/privacy-access-gate material.

The privacy material is mostly mechanism: new counselor role registration, private-repo routing, ordinary-Spirit privacy gate, private-report interim substrate, and audit prose. There is some personal-affairs metadata/status in the counselor reports, but not credential material. The right next action is not panic; it is branch hygiene and a psyche decision about whether those public privacy-mechanism reports are acceptable as public Primary history or should be rewritten more narrowly.

## Local AI toolkit mining

I launched a background subagent to mine the Prometheus prefetch results with the hard constraint restated explicitly: no model downloads, no model prefetches, no model builds, and no Nix evaluation that can touch model artifacts on any non-Prometheus machine. The child was told to use only Prometheus for any model-side inspection and to stop if Prometheus access fails.

Subagent run: `0fe9442e-b4d0-4878-b164-71cb78cffb17`. Expected output path: `reports/system-operator/185-local-ai-toolkit-prefetch-mining-2026-06-03/1-subagent-prefetch-mining.md`.

I also captured the durable constraint in Spirit record `1525`: Prometheus-local AI model prefetch, hash mining, builds, and evaluations must run on Prometheus or a designated AI node that already holds the model files; agents must not trigger large model downloads or model builds on other computers.

## Gemma 4 quantized variants

The prior open-work list is now stale here. The psyche reports that the remaining quantized variants have been tested and work. I will treat the Gemma 4 runtime path as good unless a later runtime regression appears.

## Browser live-tab automation and WhatsApp

The older open item said the Playwright Extension selected-tab proof was not done. Current evidence says that is stale too: `reports/system-operator/181-playwright-cli-browser-automation-configuration-2026-06-02.md` already records that extension attach succeeded against the main Chrome session using the gopass-backed extension token and NixOS Chrome executable path, and the psyche now reports that another client successfully ran an agent through the Playwright Extension in a real Chrome tab.

I did not inspect WhatsApp message content in this pass. That is private account material; I can only inspect it under explicit supervised direction for that surface. For the workspace report, the important mechanism update is: live main-profile selected-tab control through the Playwright Extension is proven, so the remaining work is packaging/wrapper ergonomics and supervision discipline, not proving the concept from zero.

## Cloudflare API token path

The cloud package currently expects the token at gopass path `cloudflare/api-token`. In `/git/github.com/LiGoldragon/cloud/flake.nix`, the wrapped `flarectl` sets `CF_API_TOKEN` from `gopass show -o cloudflare/api-token`.

I listed gopass entry names only and did not read any secret values. Existing relevant entries include `cloudflare.com/token`, but I did not see `cloudflare/api-token` in the name listing. So the simplest alignment is either:

1. copy the existing entry name to the expected path without displaying it, if `cloudflare.com/token` is the right token; or
2. insert a new Cloudflare API token at `cloudflare/api-token`.

No secret bytes should be printed in either path. Verification should be by entry name, command exit status, or byte count only.

## Spirit-next production-copy handover test

The prior open-work line was under-explained. It means: before `spirit-next` replaces or becomes a production Spirit candidate, the test suite must prove that a candidate daemon can run against a copy of a production-like `.sema` database, read old records from the copy, write new candidate-only records, and leave the original source database unchanged. This prevents a bad candidate from corrupting the real Spirit database during handover.

That item is no longer open. `spirit-next` now has `tests/process_boundary.rs::candidate_daemon_handover_from_production_copy_preserves_original_sema_database`, repo `INTENT.md` and `ARCHITECTURE.md` document the handover rule, and the focused test passed on 2026-06-03:

`nix develop -c cargo test --features nota-text --test process_boundary candidate_daemon_handover_from_production_copy_preserves_original_sema_database -- --nocapture`

I closed bead `primary-jew3` with that evidence.

## Editor jump-to-line emitter

The opener fix now handles the common dirty terminal cases: trailing spaces and `:line[:column]` suffixes on Primary-relative paths. The remaining distinction is reliability. An opener sees only a clicked string after Ghostty sends it to `xdg-open`; it often cannot know the terminal program's original working directory or whether `:12` is a line number versus part of a filename.

An emitter-side fix means Pi would emit a richer hyperlink in the first place, such as a VSCodium-specific `vscodium://file/<absolute-path>:<line>:<column>` URI when a tool result knows the file and line. That is more reliable for jump-to-line, but it bakes in editor-specific behavior. My recommendation: keep the current generic opener fix as the baseline; add emitter-level VSCodium links only if click-to-line from Pi output is a frequent workflow need.
