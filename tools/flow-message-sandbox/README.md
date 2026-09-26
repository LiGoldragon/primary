# Flow + Message semi-sandbox

A reusable live test of Flow Nexus 0.16 (`9aa9bf88`) and Message Nexus 0.16
(`f1843dba`) with light real seats: Claude Haiku 4.5 and Codex Luna
(`gpt-5.6-luna`, low effort), on the living's existing logins.

    tools/flow-message-sandbox/flow-message-sandbox run          # everything, then teardown
    tools/flow-message-sandbox/flow-message-sandbox run 1 5 7    # chosen scenarios
    tools/flow-message-sandbox/flow-message-sandbox up           # stand up and keep
    tools/flow-message-sandbox/flow-message-sandbox scenarios <run> 2 3
    tools/flow-message-sandbox/flow-message-sandbox down <run> [--purge]

What a run owns, all named by its run id `fms-xxxxxx`:

- both packages built from their pinned revisions (`nix build`, remote builders);
- a Flow Nexus and a Message Nexus, each in its own capped user scope, with its
  own HOME (store) under `~/.cache/flow-message-sandbox/<run>/` and sockets
  under `/run/user/<uid>/<run>/`; the private Codex app-server for scenario 12
  the same way;
- a Herdr session named after the run, whose panes see only the sandbox
  sockets and pinned binaries;
- five seats bound through `MetaBindExisting`: `haiku`, `luna-a`, `luna-b`
  (recipients) and `sender-a`, `sender-b` (idle Codex seats a sender speaks from).

Credentials are never copied or read: seats run the installed `claude` and
`codex` with the normal user config. Every seat is primed (appended system
prompt, Codex developer instructions) that letters are authorized test
requests; unprimed, a recipient takes a datom letter for a prompt injection.

`~/.cache/flow-message-sandbox/seat/` is the one stable Claude seat cwd and
Flow source root, so Claude's folder-trust question is answered once (the
suite answers it on a first run). One run at a time.

Teardown stops every process by PID and by its run-unique scope unit, stops
the Herdr session and deletes it, removes the socket directory, the stores,
and what the run added under `seat/flows`, then verifies each of those and
that every Herdr session present before is still present. Evidence stays in
`~/.cache/flow-message-sandbox/<run>/{evidence,logs,results.json,results.md}`.

Scenarios: 1 Soft to idle Haiku; 2 Soft to working Luna parks then lands;
3 MiddleAbrupt to working Codex and Claude; 4 HardAbrupt on each; 5 refused
bodies; 6 two senders one pane; 7 Acknowledge to Read; 8 Withdraw; 9 Message
restart with a parked letter; 10 recipient pane closed; 11 Flow Start Claude;
12 Flow Start Codex (known BindingRefused); 13 64 KiB and psyche letters.
