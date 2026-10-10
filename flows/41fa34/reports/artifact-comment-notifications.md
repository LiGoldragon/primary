# Artifact comment notifications

## Bounded finding

Anthropic documents two different meanings of Claude being enabled.

Organization or product activation controls whether Artifacts and Claude Docs are available. Owners enable Artifacts in Organization settings; Claude Docs is on by default for Pro, Max, and Team, and off by default for Enterprise until an owner enables it. See [Artifacts admin guide](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans) and [Get started with Claude Docs](https://support.claude.com/en/articles/16923645-get-started-with-claude-docs).

Comment-level invocation is separate. The Docs guide says a collaborator can select text, leave a comment, mention `@Claude`, and have Claude reply in the thread and make the edit. That documents a Claude action requested from the comment; it does not document a notification to another session or a wake of an idle session. See [Get started with Claude Docs](https://support.claude.com/en/articles/16923645-get-started-with-claude-docs).

Anthropic's sharing guide says invited users with Commenter or Can edit access can comment but do not receive email notifications about comments. That statement is about those invited recipients. It does not establish that the artifact owner or publisher never receives another kind of notification. See [Share artifacts](https://support.claude.com/en/articles/9547008-share-artifacts).

Within the official Anthropic/Claude documentation searched, I found no public artifact-comment webhook, artifact-comment API, watch subscription, documented delivery to the artifact owner’s Claude session, documented delivery to another Claude session, or documented automatic wake of an idle Claude.ai session. This is a public-documentation result, not proof that private or future product mechanisms do not exist.

Anthropic's webhook product is a separate product boundary: the documented webhook catalog is for Claude Managed Agents lifecycle and session events, including session idle and run-started events. It contains no Claude.ai Artifact, Docs, Design, or comment event. See [Webhook API reference](https://platform.claude.com/docs/en/api/beta/webhooks), [Subscribe to Managed Agents webhooks](https://platform.claude.com/docs/en/managed-agents/webhooks), and [Session event stream](https://platform.claude.com/docs/en/managed-agents/events-and-streaming).

The Artifacts admin guide also says Compliance API activity inside a doc, including edits and comments, is not currently recorded. See [Artifacts admin guide](https://support.claude.com/en/articles/16994751-artifacts-admin-guide-for-team-and-enterprise-plans).

## Retained account evidence

The retained account record at `flows/7b4d4c/log.md:67`–`75` reports a historical publisher-only watch: comment wake-ups armed only for an artifact the session itself published; a main flow watch started in a turn without a living message armed nothing; republishing from the main session produced a status of “connected, auto-replies armed.” This is historical account evidence, not a current product guarantee or proof of a general idle-session wake contract.

Generated tool schemas are not live product evidence and do not establish an available artifact-comment route.

## Current harness correction

Opus 5578cc relayed a newer harness witness and contract on 2026-10-03. The main session watched subflow-published books; a bare watch list of eight artifacts armed by a publisher. The harness Artifact Comments contract says that a comment using `@Claude` or “Send to Claude” on a watched artifact wakes the main-loop session holding that watch, while a plain comment does not notify it. Only the main loop holds the watch. Publishing by a subflow can therefore arm the parent main loop.

This supersedes the earlier historical inference that wake-ups arm only for an artifact published by the same session, while preserving that earlier account record and its provenance. The current harness contract is not a witness that a real Claude.ai `@Claude` comment actually wakes an idle session; that real-product idle-wake behavior remains unwitnessed.

The attributable evidence should therefore be kept in three columns: the witnessed watched-artifact list and publisher arming; the harness contract for `@Claude`/“Send to Claude” versus plain comments and main-loop ownership; and the still-unverified real Claude.ai idle-wake behavior. The current route remains `comment source → explicitly named continuous Voice/main loop holding the watch → Flow/messenger event`, with no default short-lived Book owner.

## Minimal route proposal

Do not poll, scrape, access private transports, add credentials, or implement a new adapter from this report. If and when an ordinary comment source is witnessed, the event route should be:

`comment event source → explicitly named continuous Voice → Flow/messenger event`

The continuous Voice must own the durable watch and delivery responsibility. A short-lived Book or artifact publisher is not the default owner merely because it created the page. A Book may be an explicitly selected target, but only after its publisher lifetime and idle-wake behavior are witnessed.

Before adopting the route, witness all of these in the actual account/product path: an ordinary comment (including the distinction from an explicit `@Claude` request) reaches the intended source; an idle target is actually woken; and ownership survives the publisher/session lifetime expected by the Voice. Until those witnesses exist, the report supports only an evidence gap and a future event boundary, not implementation or activation.
