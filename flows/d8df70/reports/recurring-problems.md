# Recurring problems that need particular attention

Started 2026-09-24 on the living's word: "Why don't we start making a log of the things that are recurring and not getting solved, which need particular attention." Each entry: what recurs, how often, what has been tried, where it stands, and who owns it. Newest state at the bottom of each entry.

## 1. Prometheus drops off the network until rebooted

- Recurs: yes. The living: "It works and then doesn't work and I have to reboot it." Last seen: reachable ~14:00 UTC 09-24 (uptime then ~20h), dark by ~19:30 UTC. Powered on, link light lit, no traffic; ouranos gets no ARP reply from 10.44.0.148.
- Effect: no remote builder and no cache; every build stalls on Prometheus first, because ouranos still lists it as its builder and first substituter.
- Tried: firewall diagnosis (NDP drop and inert port-80 declaration found; fixes written, not deployed). The cause of the drop itself was never found.
- Now: root-cause research running (lead hypothesis: the uplink DHCP lease expires and is not renewed; unconfirmed). Owner: Field, once a Field seat is reachable.

## 2. Flow and Message run, but no flow can use them

- Recurs: blocked since the deploy. Flow and Message daemons are live on clean stores, but Flow knows no flows, so nothing resolves or delivers.
- Now: waiting on Mind Sol 6288d1's bind command (a flow container plus its typed flows through the meta socket) and a Field seat to run it. Owner: Mind builds, Field runs.

## 3. Field seats become unreachable

- Recurs: Field panes deleted or missing (9ddcbc gone, eb7bae pane missing); others sit in a second Herdr session (default) with no messenger binding. The living: there is one Herdr session.
- Now: order out to consolidate into messaging-build; no Field seat reachable to carry it. Owner: Psyche High (coordination), Field.

## 4. Main flows do the work themselves instead of delegating

- Recurs: in every main flow, this one included. Cause, found in this seat: the stock system prompt tells the model to act directly and not to use subagents; the main-flow skill sits below it.
- Now: design sent: replace the main flow's system prompt at launch (Claude --system-prompt-file; Codex launch-only model_instructions_file), plus a periodic reminder hook. Live test of main-only scope running. Owner: Psyche High drafts, Field wires.

## 5. Seats launched badly

- Recurs: one skill per turn; wrong model (opus-5 for opus-5-5; Astra at extra-high under a Sol title); a first prompt too large for the argument limit; the old seat exited before its successor was ready.
- Owner: Field (launcher).
