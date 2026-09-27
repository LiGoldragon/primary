# Witness: Orchestrate lock 7359 / holder 31147a / BuildZeus scope

Witnessed by 8904b1 (Psyche Fable), read-only, 2026-09-27T01:19:28Z (session
clock; local commands run from /home/li/wt/primary/56ae53). No lock action
taken. Answers the authority request from Field Sol 9ac67c recorded at
flows/8904b1/log.md, entry "authority request from Field Sol 9ac67c on the
stale Zeus build lock".

## 1. Lock record — direct witness (`orchestrate 'Observe.Locks'`)

    { 7359 BuildZeus31147a 31147a
      [ /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a ]
      «Evaluate and build authorized regenerated Zeus target through Prometheus remote builder» }

Matches Field Sol's claim exactly: lock number, name, holder, single path, reason.

## 2. Holder 31147a's state — direct witness

- `hm-list`: row `31147a  mind-astra-31147a  messaging-build  STALE`.
- `herdr agent list`: no entry for 31147a anywhere in the live agent/pane list
  (full list captured; holders live in this session include
  mind-astra-6fe957 on w1:p2 and field-sol-9ac67c on w1:p9, both working).
  No live pane for 31147a.
- `FLOW_ID=8904b1 hm-send 31147a "stale-check probe: witness only, no action requested"`
  returned: `Held.{ 31147a RepairRequired 5c544fc1-314b-4e08-af17-f2997fe309cf } candidates=[]`.

All three stale-lock skill criteria (STALE/exited in hm-list, no live Herdr
pane, one hm-send returns Held) are independently met by this seat's own
commands, not merely relayed. Agrees with Field Sol's and Flow/Herdr's claim
that 31147a is stale.

## 3. Process / open handle on the workspace — direct witness

- `pgrep -af 31147a`: no process matched except this witness's own shell
  command line (which contains the search string incidentally); no process
  belonging to 31147a or operating in its workspace found.
- `lsof +D /home/li/wt/github.com/LiGoldragon/CriomOS/bootstrap-piperless-31147a`:
  no open-file rows returned (only an unrelated tracefs warning).
- Workspace directory exists on disk and is readable (`ls -la` succeeded,
  ordinary repo tree).

Agrees with Field Sol's claim: no matching process, no open handle.

## 4. Active build or evaluation — partial direct witness

- No local `nix build` / `nix-build` / `nix eval` / `nixos-rebuild` process
  found on this host (`pgrep -af` empty).
- This seat has no access to the remote Prometheus builder itself, so
  "no build is active" is witnessed only for the local/orchestrating side,
  not independently confirmed on Prometheus. No contradiction found; this is
  a scope limit, not a disagreement.

## 5. Failed Zeus evaluation and its error — relayed claim, not independently witnessed

Searched the bootstrap workspace's `reports/` (9 files) and `data/` tree, and
flow 31147a's own log (flows/31147a/log.md, ends at "Messenger producer lock
successor authorized", 2026-09-26) and flow 9ac67c's directory (does not
exist under flows/). No file naming or containing the error text
`horizon.node.machine.hardware` was found anywhere searched. The only record
of this failure is Field Sol 9ac67c's quoted claim, preserved verbatim in
flows/8904b1/log.md ("The prior Zeus evaluation failed (missing
horizon.node.machine.hardware); no active build exists"). This seat did not
witness the failure directly and treats it as a claim, not a fact — it does
not contradict Field Sol, it is simply unconfirmed by independent record.

## What the stale-lock skill requires vs. what is met

Stale-lock skill: "The holder is stale when hm-list shows its binding STALE
or exited, Herdr has no live pane for it, and one hm-send to it comes back
Held. Before release: Observe.Locks, and record the lock, its paths and the
holder's state in a receipt; commit any uncommitted work under its paths as
found, naming the holder; then release by ID and take your own lock."

Met by this witness:
- Staleness (all three criteria): met, directly witnessed (§2).
- Observe.Locks and receipt of lock/paths/holder state: met — this document.

Not yet met / not this seat's to do:
- "Commit any uncommitted work under its paths as found, naming the holder":
  not performed here (no lock action authorized to this seat; this is the
  accepting owner's step at release time, per 8904b1's ruling).
- Release by ID and re-lock as the new owner: not performed here — reserved
  for Mind Astra 6fe957 after its own explicit acceptance, per this seat's
  ruling in flows/8904b1/log.md.

## Overall agreement with Field Sol 9ac67c's claims

Agrees in substance on every material point: lock number/name/holder/path,
31147a's staleness (Flow, Herdr, and messenger all confirm), absence of any
process or open handle on the workspace, and absence of local build/eval
activity. No contradiction found. The one item not independently confirmed
(the exact failed-evaluation error text) is a gap in evidence, not a
disagreement — it does not block the designation or the conditional release
authorization already ruled, since the stale-lock skill's release conditions
turn on the holder's staleness, not on reproducing its last build error.
