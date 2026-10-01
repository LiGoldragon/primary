# Mind Sol route-repair judgment

Observed 2026-09-26T18:59:45-06:00 from the live local Herdr server and the
installed Messenger CLI. Scope was only the requested possible repair of flow
`6fe957`; no process, pane, session, title, network, service, or unrelated
Messenger record was changed.

## Exact native identity and current binding

`herdr agent get mind-astra-6fe957` returned exactly:

* Herdr session: `default`
* agent name: `mind-astra-6fe957`
* pane: `w1:p2`
* terminal: `term_65c6a758e81952`
* native Codex session: `01a0dfdc-a500-7271-8f54-e446fe9578dd`
* lifecycle: `done`; `interactive_ready: true`

`hm-heartbeat-state` independently records flow `6fe957` as the same complete
bound tuple, with native thread `01a0dfdc-a500-7271-8f54-e446fe9578dd`.
`hm-list` reads it back as `6fe957 mind-astra-6fe957 default done`.

The claimed `default/w1:p1` is not that identity: live Herdr reports a separate
working Codex process there, terminal `term_65c6a3b37c3011`, with no recorded
native session or agent name. It cannot safely be substituted for the Mind
Astra route.

## Repair decision

No Messenger mutation was made. The installed `hm-repair` contract requires a
specific outstanding `RepairRequired` pending ID and one exact, live candidate
identity; it prompts the held envelope as part of the operation. The current
binding already matches the only exact recorded Mind Astra identity, and no
pending repair attempt was supplied or established. More decisively, its native
endpoint is currently `done`, so it is not a supported candidate for a new
delivery repair. `hm-rebind` is also inapplicable: it requires a distinct new
live agent name while preserving the exact native thread, and no such identity
exists.

## Receipts and limits

* Submitted: none.
* Transported: none.
* Presented: none.
* Read: none.
* Binding before and after: unchanged, `default/w1:p2/term_65c6a758e81952`,
  `mind-astra-6fe957`, native `01a0dfdc-a500-7271-8f54-e446fe9578dd`.

This is a no-op judgment, not a claim that the `done` Mind Astra endpoint can
receive a future message. A future repair would require a concrete held pending
attempt plus one live Herdr candidate whose full identity and native session
match; a new or different main native seat would require its own authorized
binding path.

## Recovered version from unlanded commit 6df7ee9e74ad (2026-09-28 16:31 UTC)

#\1 Mind Sol `56ae53` route-repair judgment

Observed 2026-09-26T19:00:00-06:00 from the live default Herdr server, the
installed Messenger CLI, and Flow. This corrects an earlier scope error: the
authorized target is Mind Sol `56ae53`, not flow `6fe957`.

`hm-heartbeat-state` and `hm-list` show `56ae53` bound stale to
`messaging-build/wM:pJ/term_65c6462fe47809b`, agent
`mind-sol-of-00f95a-56ae53`, Codex native thread
`01a0de4c-554d-7343-bbc5-e4256ae5366f`. Exact pane and agent reads against
that session return `server_not_running`; it was not started or attached.

The claimed current pane is proven to host the same native thread: passive
`herdr pane process-info --pane w1:p1` reports a working Codex `resume` command
with final argument `01a0de4c-554d-7343-bbc5-e4256ae5366f`. Its live identity
is `default/w1:p1/term_65c6a3b37c3011`. Herdr exposes no agent name or
`agent_session` for that pane.

Flow is independently stale too. `flow 'ResolveRecipient.56ae53'` resolves the
same native thread but reports both Codex endpoint and Herdr route
`Unavailable`; `flow 'List.{}'` retains the old `messaging-build/wM:pJ` route
as `Available` metadata. No Flow mutation was authorized or made.

No Messenger repair was made. Installed `hm-repair` requires a specific pending
`RepairRequired` ID, the held envelope, and one exact live candidate with
session, pane, terminal, nonempty Herdr name, harness, and official native
session. No pending attempt/envelope was supplied, and `w1:p1` lacks the Herdr
name and session required to be that candidate. `hm-rebind` also requires a
live old binding and distinct live agent name. `hm-register` would create a new
registration rather than surgically repair the stale record and is outside this
authority.

Binding before and after is unchanged. Submitted, transported, presented, and
read receipts are all none. The repair is blocked by missing supported
Messenger-candidate and pending-repair prerequisites, despite exact proof of
the native thread at `w1:p1`. No prompt, restart, stop, title change, Flow
rebind, or Messenger rebind occurred.
