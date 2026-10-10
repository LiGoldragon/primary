---
title: 187 — Psyche context-maintenance situation
role: system-operator
variant: Psyche
date: 2026-06-03
topics: [context-maintenance, psyche-report, open-work, system-operator, prometheus, cloudflare, browser-automation]
description: |
  Psyche-facing context-maintenance pass over the current system-operator
  thread and adjacent recent reports. States what is now addressed, what is
  still open, what matters next, and which stale system-operator report was
  retired.
---

# 187 — Psyche context-maintenance situation

## What this pass did

This is a context-maintenance pass, not a new design proposal. I refreshed the live conversation state, recent Spirit captures, current open beads, and the recent report surface around the topics we have been moving through: Ghostty/editor links, Prometheus local AI, Gemma 4, Playwright Extension browser control, Cloudflare/domain work, Spirit-next handover, privacy/access-gate prep, and report/skill hygiene.

Three recent intent summaries shape how this report is written:

- [Psyche reports should let the psyche follow the line of thought all the way back to the basics: when a report refreshes or audits prior work, it should re-ground the current issues from first principles instead of assuming the reader already has the whole context loaded.]
- [Open-work and psyche reports must explain opaque unresolved items in plain terms, including what the item means and why it matters; listing a label without explanation is not enough.]
- [Intent records cited in prose markdown should quote the literal description summary as bracketed text; the bracketed summary is the load-bearing citation, while record numbers are opaque addresses and should not be the only citation. This applies especially in psyche-facing reports and wherever intent is central.]

Disk-side action: `reports/system-operator/184-left-unaddressed-psyche-report-2026-06-03.md` is now stale. It was the first rough open-list, and its live substance is carried forward by `reports/system-operator/186-psyche-open-work-update-2026-06-03.md`, `reports/system-operator/185-local-ai-toolkit-prefetch-mining-2026-06-03/`, and this report. I retired 184 in this maintenance pass.

## My current situation

I am current on the refreshed workspace intent and important skills: `ESSENCE.md`, `INTENT.md`, `AGENTS.md`, `skills/intent-log.md`, `skills/reporting.md`, `skills/privacy.md`, `skills/secrets.md`, `skills/jj.md`, `skills/system-operator.md`, the Nix/testing skills, role-lanes, and the new `skills/engine-report.md`. The new `skills/intent-log.md` citation section is now present on Primary `main`.

Primary `main` has moved forward since my prior report: designer landed a follow-through batch that includes the bracket-quote intent citation discipline and report-header/front-matter cleanup work. I will not touch the designer-owned skill/report cleanup except where it affects my own reports.

The current system-operator thread is not blocked by Ghostty/editor links anymore. Clean file links, dirty terminal paths with trailing spaces, common `:line[:column]` suffixes, and VSCodium-as-default are all practically addressed. If click-to-line becomes important enough to optimize, the remaining work belongs at the emitter layer, where Pi can emit editor-specific links such as VSCodium file URIs instead of relying on a generic opener to infer location from a dirty terminal string.

## What is now addressed

**Gemma 4.** The earlier “remaining quant variants need testing” item is stale. You reported that the remaining Gemma 4 variants work and you are happy with them. I will treat Gemma 4 on Prometheus + Pi + browser-use as a working runtime path unless a new regression appears.

**Spirit-next production-copy handover.** This is closed. The phrase meant: before a Spirit-next candidate can be trusted near production, the tests must prove it can run against a copy of a production-like `.sema` database, read existing state, write candidate-only state, and leave the original database unchanged. `spirit-next` now has `tests/process_boundary.rs::candidate_daemon_handover_from_production_copy_preserves_original_sema_database`, and the focused test passed. I closed bead `primary-jew3` with that evidence.

**Prometheus prefetch mining.** The subagent mined the completed Prometheus prefetch results in `reports/system-operator/185-local-ai-toolkit-prefetch-mining-2026-06-03/`. The result set is 19 rows, 0 failures. It reports that all inspection was read-only SSH to Prometheus and no downloads/builds/evals happened off Prometheus. The durable rule remains: [Prometheus-local AI model prefetch, hash mining, builds, and evaluations must run on Prometheus or the designated AI node that already holds the model files; agents must not trigger large model downloads or model builds on other computers.]

**Browser live-tab proof.** The older “selected-tab proof remains open” item is stale. We now have two signals: `reports/system-operator/181-playwright-cli-browser-automation-configuration-2026-06-02.md` records extension attach against the main Chrome session, and you reported that another client successfully ran an agent through the Playwright Extension in your real Chrome tab. I did not inspect WhatsApp content; that remains private/supervised account material. The mechanism proof is enough: Playwright Extension selected-tab control works.

**Privacy/access-gate commit panic level.** I read commit `597060b18a73`. It is not a secret-byte leak. It contains no API key, password, token, private key, or decrypted secret value. It is still over-broad branch hygiene because it combines an editor-link report update with counselor/assistant/privacy-access-gate material.

## Still open and important

### 1. Privacy/access-gate public-history decision

What remains is a public-history decision, not an emergency secret incident. The over-broad commit contains privacy mechanism reports and some personal-affairs metadata/status. You clarified that this work is preparatory — getting tools and protocol ready — and that you do not think sensitive content has been said yet in this thread. That matches the Spirit clarification: [Current privacy/access-gate work is preparatory tooling and protocol work; the psyche does not believe sensitive private content has been said yet in this thread.]

The actual question is: do we leave the public privacy-mechanism reports in Primary history as acceptable mechanism/status documentation, or rewrite/split the branch so only the narrow system-operator report update remains on the public line and the privacy/access-gate material is re-landed in a more deliberate shape?

My recommendation: do not treat it as a leak; do a deliberate branch-hygiene pass when convenient. If you want the public line maximally clean, rewrite/split. If you accept public mechanism/status reports about privacy infrastructure, leave it and move on.

### 2. Cloudflare token path and Cloud/domain continuation

The cloud package expects the Cloudflare token at `gopass:cloudflare/api-token`; the wrapper sets `CF_API_TOKEN` from `gopass show -o cloudflare/api-token`. I listed gopass entry names only and did not read secret bytes. I saw `cloudflare.com/token`, but not `cloudflare/api-token`.

So the practical next step is blind secret handling:

- if `cloudflare.com/token` is the correct token, copy it to `cloudflare/api-token` without printing it;
- otherwise insert the new token at `cloudflare/api-token`;
- verify by entry name, exit status, or byte count only — never by displaying the value.

Once that path exists, the cloud/domain work can resume: Cloudflare DNS/redirect read-write, Rulesets/Page-Rules handling, provider runtime hardening, persistence growth, actor split, nonblocking provider actors, and daemon-to-daemon projection handoff.

### 3. Prometheus `llm.json` winners

The prefetch has produced the evidence, but `CriomOS-lib/data/largeAI/llm.json` has not yet been updated from it. The candidates to consider are:

- `qwen3-coder-next-80b-a3b-q5-k-m` — split GGUF files; only add if the router/schema can express split file sets cleanly.
- `gemma-4-e4b-it-ud-q8-k-xl` plus `gemma-4-e4b-it-mmproj-f16` — model plus multimodal projection companion.
- `nemotron-3-nano-omni-30b-a3b-reasoning-ud-q4-k-xl` plus `nemotron-3-nano-omni-30b-a3b-reasoning-mmproj-f16` — model plus multimodal projection companion.

Do not blindly add every GGUF row. Keep these out until runtime homes exist: Parakeet (`.nemo`), Qwen embedding safetensors, Qwen reranker safetensors, and FLUX. The next implementation pass should do the schema-aware `llm.json` edit and validate from Prometheus or the designated AI node only.

### 4. Browser automation packaging and supervision discipline

The Playwright Extension proof moved the issue from “is it possible?” to “how do we make it safe and ergonomic?” The likely next work is a CriomOS-home wrapper or documented command that supplies the NixOS Chrome executable path and the gopass-backed extension token, plus a scout-mode rule: real accounts stay supervised, selected-tab scoped, and private content is not summarized into public reports.

Related open beads still point at browser-use/atlas packaging and browser-use end-to-end smoke work. Those are adjacent but not identical: Playwright Extension controls the real selected tab; browser-use still has its own agent/runtime path and may be better for separate automation profiles.

### 5. Prometheus deployment/network safety

Prometheus remains the resilient-router + large-AI node, and there are still open system-level safety beads around it: console/out-of-band access before risky router deploys, router/wifi projection confirmation, llama-server API token wiring, Gemma multimodal mmproj verification, and the broader “complete Gemma + sops-auth deploy via BootOnce” path.

The important discipline here has not changed: router-impacting Prometheus changes use BootOnce, not Switch, and model artifact work stays on Prometheus.

### 6. Spirit privacy / Spirit-next deployment gap

Recent reports show the privacy axis is implemented in source across the Spirit stack, but not yet live in deployed production Spirit. The current deployed `spirit` wrapper is still v0.3.0-shaped; the newer privacy selector/field work belongs to the spirit-next → production chain. So ordinary Spirit still gets only privacy-safe public/meta intent today; private personal substance still stays out of ordinary Spirit until the live wire supports the privacy field.

The broader Spirit-next deployment chain also has a naming/target gap: reports indicate the side-by-side `spirit-next` slot machinery exists, but the deployed input chain has been pointed at the wrong target in at least one recent audit. That is important because privacy, variant ladder, and schema-derived runtime work only matter operationally once the deployed slot actually points at the intended `spirit-next` source.

### 7. Report/skill hygiene

This is now a live maintenance front. Recent reports drifted into a semicolon-bracket pseudo-NOTA header that was never ratified. The new rule is YAML front matter. The relevant intent summary is: [Reports use standard YAML front matter for metadata, not the semicolon-bracket pseudo-NOTA shape (; role [topics] [description] date role) that recent reports have been emitting. Rationale — YAML front matter plugs into standard markdown UI tooling (previewers, GitHub rendering, Obsidian, editor frontmatter parsers); valid markdown so renderers display reports cleanly; is the conventional metadata-on-markdown standard. The psyche has mentioned this preference before. skills/reporting.md should specify YAML front matter as the canonical report header form.]

Designer has already audited this and landed follow-through. I am following the new YAML shape here. A full report-tree migration is separate work; this pass does not pretend to finish it.

### 8. Schema / triad / Nexus implementation backlog

The design surface moved a lot today. `skills/component-triad.md` now carries the NexusWork/NexusAction/Continue/effects substrate and lifecycle hook direction; `skills/nota-design.md` now carries the enum-payload-vs-struct-product pattern and header-declared inline enum sugar. Those are guidance landings, not full implementation. The open P1/P2 beads around OutputNexus dispatch, schema-diff upgrade traits, observer registration, types-only schema modules, and shared schema-core floor are still the implementation backlog.

The recent engine-report tooling helps here: `tools/engine-situation` and `leta` give agents a better way to prove live runtime paths instead of relying on grep. That is useful, but it is not the same as implementing the outstanding schema/triad pieces.

## What I would do next

If you want the practical system-operator path, I would sequence it like this:

1. **Cloudflare token path** — ask you whether `cloudflare.com/token` should be blind-copied to `cloudflare/api-token`, or whether you want to insert a fresh token there. That unlocks cloud/domain provider work.
2. **Prometheus `llm.json` pass** — add only the three llama-router winners, handling mmproj as companions and split-GGUF carefully, with validation constrained to Prometheus.
3. **Playwright Extension wrapper** — package the already-proven selected-tab control into a repeatable supervised command.
4. **Prometheus safety beads** — console/out-of-band access and BootOnce router safety before risky deploy changes.
5. **Public report hygiene** — continue the YAML/front-matter migration and retire stale system-operator reports topic-by-topic.

The one thing I would not do casually is broad report deletion across lanes. The report tree is over the soft cap, but recent context is actively moving under multiple agents. Retiring reports should happen topic-by-topic with a named successor or permanent landing, not as a cleanup spree.
