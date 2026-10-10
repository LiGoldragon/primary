# Unity Web client draft

This directory is a static, dependency-free draft of Unity Web: a phone-first
client surface for observing Mentci flows, reading a selected conversation, and
submitting text through an isolated adapter. The localhost-only POC is running
at `http://127.0.0.1:38081/`; this is not a deployed phone app or activation.

## Run locally

Open `http://127.0.0.1:38081/` on the local machine for the live POC. The
default mode uses a restricted binary Signal WebSocket adapter and the
remote-built Rust/WASM codec. Failures remain visible and never fall back to
fixtures. Serving this directory alone cannot resolve the sibling codec
module or provide the Mentci endpoint.

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
- `getConversation(flowId, cursor?)` returns a bounded `ConversationSnapshot`
  with `flow_id`, `observed_at`, `source_status`, byte coverage, optional older
  cursor, and entries containing `entry_id`, `sequence`,
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
The generated types, canonical wire round-trip, remote host/WASM builds, and
localhost READ witness exist. This remains a bounded POC, not a public route.

There is no polling, tailing, push, notification, speech, provider, or Slint
implementation in this client. The roster is observed once on load and
again only when the labelled Refresh button is used. Selecting a flow performs
one conversation fetch for that flow; Refresh performs one fetch for the
selected flow after refreshing the roster. “Load older” makes one additional
on-demand cursor request; it does not poll. These are bounded requests, never
subscription triggers. A send receipt never creates an optimistic
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

- The bounded Persona normalizer admits Codex assistant text only with
  `phase=final_answer` and typed text blocks; commentary/tools are not finals.
  User-role records remain `Unknown`, even when retained as input.
- The bounded Claude normalizer requires the exact session, main line, and
  `end_turn` for assistant finals. Tool-use text is not a final. More elaborate
  request/block grouping is not claimed by this POC.
- Fresh panes without an exact native session identifier cannot be correlated
  safely. The current POC binds only the full reviewed `effa1b` and `c8d79f`
  identities; other roster seats have no asserted flow ID. Prefix globbing is
  invalid.
- Multiple Codex rollouts for one native session, several native sessions for
  one logical flow, ambiguous Claude leaves, and unmarked compaction summaries
  remain unresolved. The client expects the adapter to report a partial or
  unavailable source status rather than inventing certainty.

Synthetic fixtures cover Unity-labelled psyche, machine final, and unknown-origin entries,
but deliberately do not claim to resolve those source questions.
