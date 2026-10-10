# Morning checkpoint — 2026-09-16, from primary Claude efa157

Short, as asked. Everything below is on proposal branches; nothing was merged to main, deployed, restarted, or reset. Each row says what was put together and why, what it looks like, and what its tests prove. Codex's own table is in its morning review; the audit verdicts are this lane's.

## What was built overnight

| For | What it looks like | Reliability, tests |
|---|---|---|
| Your words reaching every cluster member (item 50) | One-call relay: head and tail words, transcript lookup, typed ClusterMessage with a Luna-written Context beside your verbatim text; fanout to Codex, Claude (prompt-relay) and the message Nexus | Delivered: your four held turns landed in this session today, each hash-verified. Witnessed: ordinary Claude turns parsed, loop guard holds, one signal source, real-socket process test in Nix. Codex's claim only: the Claude and Nexus legs (landed 11:00Z, process tests 3/3). Open: live route registration, delivery to a busy Claude. |
| A monitor that cannot stall itself (item 49) | Deterministic runner under a kernel lock, no model child, bounds in the runner; a pinned Home unit; a separate wake adapter | Witnessed in source. Codex: 12 remote tests, Home closure check green. The installed monitor on ouranos is still the old runner (recovered from a garbage-collection deletion at 06:22Z, green since 07:22Z), wake and repair off; activation is the secondary's. |
| Your chime channel (items 47, 48) | Prometheus module: Prosody plus Forgejo, self-signed TLS with atomic seven-day renewal, SOPS secret declarations, a `Notify.{ jid «body» }` parser through datom-codec, an offline OMEMO 2 roundtrip | Witnessed: the enabled configuration now evaluates; TLS renewal and the Notify head run are real and match their receipts. Not a chime yet: no account, no bot, no open firewall port, Actions enabled with no runner, reload and secret decryption unproved at runtime. |
| Cloudflare first (item 47) | A scoped DNS plan for the messaging domain, read-only, on the existing provider client | Codex: four local tests, one remote. No record applied, no certificate issued. |
| The phone app (item 46) | A Slint proof on mentci-lib behind a feature flag; a bounded offline reply state | Witnessed: the four state tests are real but never open a window; no Android target of any kind; disjoint from the crate's real models. Codex: the graphical binary now compiles remotely as an isolated fixture crate. |
| Launch records and hook events (items 31, 45) | Typed launch, hook and error fixtures; a Flow-owned idleness API | Codex: focused remote checks. Nothing installed. |
| The identifier, Psyche, MCP, architecture, language and reconnect items (32, 34, 40, 36, 42, 43, 51, 39) | Documents and bounded source proofs on proposal branches | As documents, not executable proofs; see Codex's report. |

## What you can try now

- Speak to this session: your words now reach Codex by the relay, and Codex's answers come back to my lane. That is the one live loop.
- Read the two audits with the sharpest findings: `flows/efa157/reports/item48Audit.md` and `clusterRelayAudit2.md`, plus `slintClientAudit.md`, all on origin flow/efa157. Codex's full account is `flows/cf7879/reports/to-840e42.md` on origin flow/cf7879, its short table `morning-review-2026-09-16.md`.

## What waits on your word

1. The Jujutsu law wording (the version-control skill and the entry-file Committing section), printed whole in my reply at 08:23Z. Codex's inventory says 45 authored skills, residual Beads clauses in three.
2. The integrator. Codex proposes itself after exact-main authorization; I proposed the primary Claude with the secondary deploying. Nothing moves main until you name one.
3. The two settings lines, unchanged: crossSessionInbound accept, and a permission rule for tools/prompt-relay. The secondary still receives nothing from the primaries except through its own approval window; three messages expired there overnight.
4. The contact channel: XMPP now versus waiting for the app. The chime pieces exist but no account or bot.
5. A script space per flow lane with a doc per script, per your fourth turn; my predecessor's ten uncommitted send scripts wait on it.
6. Quota: Codex Pro fell from 58 percent last night to 28 percent at 09:52Z and 23 percent at 12:22Z; the burn slowed to about two points an hour after I asked Codex to stop new implementation at 09:10Z, corrections and receipts still costing. Reset 19 September 15:05Z; three reset credits unused. Your call whether to spend one.

## Open forks carried

Tailnet: Tailscale versus Yggdrasil; ouranos and prometheus are not logged in to Tailscale, Yggdrasil carries the hosts today. "Unity" in your channel words, unrecognized. Context beside the words in the relay (implemented beside). The nine decisions from the 15th, none blocking.

## Provenance

Lane: origin flow/efa157, `flows/efa157/log.md` for the whole night in order. Witnessed means a subflow of this flow ran or read it; Codex's claims are marked as such.
