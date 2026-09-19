# Unity Web client draft

This directory is a static, dependency-free draft of Unity Web: a phone-first
client surface for observing Mentci flows, reading a selected conversation, and
submitting text through an isolated adapter. It is a review artifact, not an
activated service, a phone application, or evidence that a Mentci endpoint
exists.

## Run locally

Serve this directory with any static file server and open `index.html`. The
default mode uses a restricted binary Signal WebSocket adapter. The Rust/WASM
codec and daemon bridge are not built or activated yet, so its failures remain
visible and never fall back to fixtures. Serve from the parent `flows/0ab019`
root when a compiled codec and the localhost bridge eventually exist; serving
this directory alone cannot resolve the sibling codec module.

Append `?demo=synthetic` to enter the clearly labelled synthetic demo. Demo
responses are generated locally and are never sent to a live endpoint.

The browser test page is `tests/browser.html`. It exercises the production DOM
client against synthetic adapters and reports pass/fail in the page. A headless
Chrome witness can be run from this directory:

```sh
google-chrome --headless --no-sandbox --disable-gpu \
  --allow-file-access-from-files --virtual-time-budget=3000 \
  --dump-dom tests/browser.html
```

## Provisional adapter boundary

`app.js` exposes `createUnityClient`, `createSignalAdapter`, and
`createSyntheticAdapter`. The UI knows only three adapter operations:

- `getRoster()` returns `RosterSnapshot` with `observed_at`, `source_status`,
  and `flows` containing `flow_id`, `name`, `seat`, `state`, optional
  `last_activity_at`, and optional `last_activity_source`.
- `getConversation(flowId)` returns `ConversationSnapshot` with `flow_id`,
  `observed_at`, `source_status`, and entries containing `entry_id`, `sequence`,
  `occurred_at`, `text`, `source_kind`, optional `attributed_actor`, and
  `provenance` (`PsycheViaUnity`, `Machine`, or `Unknown`).
- `send({ request_id, flow_id, text })` returns a receipt with `request_id`,
  `disposition`, optional `reason`, optional `relay_id`, and optional
  `receipt_grade`.

The live adapter targets only same-origin `ws://<current host>/signal` and sends
one codec-produced binary Signal frame per bounded request. The codec exports
only constructors for ObserveRoster, ObserveConversation, and SubmitPsyche plus
their paired decoders; the browser never sends actor or provenance claims.
There is no ad-hoc JSON API or query-string override for a remote endpoint.
This bridge is source-only until generated types, a canonical wire round-trip,
remote compilation, and a localhost runtime witness exist.

There is no polling, tailing, push, notification, speech, provider, Persona,
Slint, or backend implementation here. The roster is observed once on load and
again only when the labelled Refresh button is used. Selecting a flow performs
one conversation fetch for that flow; Refresh performs one fetch for the
selected flow after refreshing the roster. These are bounded requests, never
polling or subscription triggers. A send receipt never creates an optimistic
conversation entry. Whitespace is used only to reject an empty composition;
accepted input is sent unchanged. Browser or transport failure is shown as a
client-unavailable error, never synthesized into a backend `rejected` receipt,
and the per-flow draft is preserved. A selected-conversation failure is shown
as unavailable rather than as an empty conversation.

## Origin and transcript limits preserved

`role=user` and non-Datom text are not proof of human origin. The draft labels
only `PsycheViaUnity` provenance as Living; `Unknown` remains visibly
unverified. `source_kind` is a separate dimension: a final machine response
is displayed as `final-response · Machine`. Unrecognized adapter source kinds
are rendered as unknown while retaining their supplied provenance. Metadata
actor names remain attributed claims.

The current normalization findings intentionally remain outside the browser
client. In particular:

- Codex final text requires `phase=final_answer` plus matching turn completion;
  commentary, tools, meta, duplicated events, and same-turn steering are
  excluded.
- Claude assistant blocks must be grouped by exact session and request,
  ordered by `apiBlockIndex`, and accepted only for a main-line `end_turn`.
  Text in a `tool_use` response is partial, not final.
- Fresh panes without an exact native session identifier cannot be correlated
  safely. Flow aliases must be confirmed against the full marker identity;
  prefix globbing is invalid.
- Multiple Codex rollouts for one native session, several native sessions for
  one logical flow, ambiguous Claude leaves, and unmarked compaction summaries
  remain unresolved. The client expects the adapter to report a partial or
  unavailable source status rather than inventing certainty.

Synthetic fixtures cover Unity-labelled psyche, machine final, and unknown-origin entries,
but deliberately do not claim to resolve those source questions.
