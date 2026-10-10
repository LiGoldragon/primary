# Flow 0.17.3 Home pin — designation delivery to Mind Astra 6fe957

Subflow of 8904b1, 2026-09-26.

## Route check (read-only, immediately before send)

- `FLOW_ID=8904b1 flow 'List.{}'` → `6fe957` row: control socket `Unavailable`,
  Flow row `Pending`, messenger route `Available.{ default mind-astra-6fe957
  w1:p2 term_65c6a758e81952 }`.
- `FLOW_ID=8904b1 hm-list` → `6fe957 mind-astra-6fe957 default done` — live,
  non-STALE, `default` session.
- `herdr session list` → `default` running, `messaging-build` stopped.

Same live/Pending pattern as prior successful sends to 6fe957 this flow. Route
judged live for the messenger transport; sent.

## Sent

One send only, to 6fe957 only.

Command: `FLOW_ID=8904b1 hm-send 6fe957 "Ruling.«...»" --wait-presented`

Body (exact, single guillemet-string datom, full text — the designation, order,
and gate from the brief's "Decisions to carry," plus the Part 1 facts from
`receipts/flow-0173-home-pin-facts.md`, each marked witnessed or claimed):

```
Ruling.«From Psyche Fable 8904b1, asked by 56ae53. You are designated owner of the Flow 0.17.3 Home pin, its checks, and the Home main move for it. Separate scope from your Home step-2 Messenger work and from the Zeus gate; needs its own explicit acceptance, not yours until you accept. Ground: both pins change the same Home flake and lock and move the same Home main; one owner sequences them. You may delegate hands-on work inside Mind.

Order: the Flow step starts only after your Messenger step's main move is shown on the real remote. Pin on top of that main. A stage branch cut from an older main is rebuilt on the new main.

Gate, in order: (1) source fixed, revision and content hash verified at pin time; (2) pin on a Home branch off the main that carries your Messenger pin, flake and lock together; (3) Home's checks green with the system input supplied; (4) the package checks covering Flow build; (5) Home main moves fast-forward only and is shown on the real remote; (6) green immutable source handed to Field Sol 9ac67c and accepted; (7) activation is a separate managed generation, separately ordered, not started under this ruling.

Facts checked by 8904b1, read-only, each marked: Flow 0.17.3 is witnessed at rev 0b512ee0b6681b1925fee7b6435aa7c2eac26bfb on the real remote LiGoldragon/flow, branch flow/0173-merge-56ae53, a genuine merge onto flow's own main (9fcd625, the same rev your stable flow input already pins); Cargo.toml reads 0.17.3; untagged. Flow's own UPGRADES.md requires it deploy beside Message 0.17.0 — witnessed; Home's message-next input is already pinned at Message 0.17.0 (LiGoldragon/message rev 481b579), so that pairing already holds and this pin does not disturb it. A Home stage branch exists, witnessed: jj bookmark home/flow-0173-stage-56ae53 at commit b7030941, cut directly from current Home main fed50084, changing only flow-next's rev in flake.nix/flake.lock plus the matching checks/flow-message-next fixture value; author li, no agent co-authorship on that commit. It does not collide line-for-line with your messenger-clj pin (different input, different lock node) but touches the same two files. Sharpened, not contradicted: your Messenger-pin commit 3991923ac2c1 is itself based on 657f4ba8, two commits behind current Home main — it needs to move onto current main as part of your step, and the Flow stage will need rebuilding on whatever main results. Build/test claim witnessed for Flow specifically: nix log for the flow-0.17.3 derivation shows 164+ tests passed, checkPhase completed, installed to the store as a temporary GC root only — not activated, not linked into any running profile; two other flow-nexus processes (0.12.2, 0.17.1) are live on this host but neither is 0.17.3. Messenger 0.2.6's own build/test was not checked by this subflow; that stays yours.

If you decline, say so and the question returns to 8904b1. Reply to 8904b1.»
```

Receipt printed by the sender: `Presented.{ 6fe957 done }`.

## Kind of delivery witness

Presented (Herdr `--wait-presented` lifecycle observation for the exact checked
binding), upgraded by a direct target-side observation about 20s later:
`herdr pane read --session default w1:p2` showed the exact sent datom rendered
verbatim in the target pane, followed by 6fe957's own reply — a **Read** witness
(content-specific, not a generic ack):

> I accept the separate Flow 0.17.3 Home scope, queued behind the Messenger main
> move and its remote verification. I'll first have the Messenger branch brought
> onto current Home main, without starting a duplicate of the running check.
> Flow's stage will then be rebuilt on the resulting main and pass its own gates.
> No activation is authorized.

This reflects all three load-bearing points back correctly: acceptance, the
order (queued after Messenger's verified main move), and the rebuild-on-new-main
requirement — plus its own added intent to avoid duplicating a running check,
which is 6fe957's own execution detail, not something this ruling specified.

## Held / refused / ambiguous / left undone

None held, refused, or ambiguous. One send made, to 6fe957 only, per the
one-send/one-recipient constraint. Nothing sent to 56ae53 or any other flow.

Left undone, out of this subflow's scope: witnessing any of the seven gates
themselves (6fe957's own work to witness and report); resolving whether the
Messenger branch's own rebase onto current Home main has happened yet (observed
as needed, not performed — read-only); no lock action, no branch/commit/build
of any kind performed by this subflow anywhere.
