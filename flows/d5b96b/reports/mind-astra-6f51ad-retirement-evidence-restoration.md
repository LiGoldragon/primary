# Mind Astra 6f51ad retirement evidence restoration

The Messenger retirement marker for Flow `6f51ad` references `/home/li/primary/flows/d5b96b/reports/mind-astra-6f51ad-messenger-retirement.md` with SHA-256 `9e195a185a8e82d22a42d480acbc0c065e7e5c6a948b17be45e8f60660a0b895`.

The file was missing from the current checkout. It was restored byte-for-byte from immutable commit `694d3716f8b9fd2111e2355c851cc204da89921b`, where it was authored as part of `Record Mind Astra successor launch and route closure`. The resulting on-disk SHA-256 matches the marker exactly.

The retirement itself was executed by Field `d5b96b` through `rotation_finish`, using witnessed command `hm-retire 6f51ad --session default --pane-id w1:pG --terminal-id term_65c8d7ace74b012 --name mind_astra_6f51ad --agent codex --native-thread 01a0e8d3-aace-7712-aae2-3ce6f51adad5 --evidence /home/li/primary/flows/d5b96b/reports/mind-astra-6f51ad-messenger-retirement.md --evidence-sha256 9e195a185a8e82d22a42d480acbc0c065e7e5c6a948b17be45e8f60660a0b895`.

Read-only `hm-heartbeat-state` resolves this marker as `state: retired`, with its recorded predecessor session, pane, terminal, Codex harness kind, native thread, evidence path, and evidence hash.

The marker's `retired_by` field is empty. No supported metadata-repair interface for that field was witnessed in this scope, so it was not rewritten. The factual execution provenance above does not alter the marker.

## Sources

Immutable commit `694d3716f8b9fd2111e2355c851cc204da89921b`; live read-only `hm-heartbeat-state` result on 2026-09-30.
