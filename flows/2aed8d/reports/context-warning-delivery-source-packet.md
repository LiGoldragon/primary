# Bounded warning-delivery source packet

Parent source-only read; codec worker uninterrupted. Prepared Flow916 sources are unchanged by codec slice at these locations. No architecture or warning-body authorization follows.

## Correlated Stop, measurement, settlement, refresh

1. `reporting.rs:61–86` RecordsReports::report performs Record.Harness first; `after_report:118–165` processes Event::Stopped only after correlated_stop, then calls settle_stopped(flow_id).
2. `waking.rs:1003–1042` CorrelatesNativeEvents::correlated_stop checks registered FlowNode, Claude harness, nonempty stored native session equal to reported session, and matching (or canonicalized matching) transcript path. NativeStop has no event/prompt ID; record_event appends without duplicate identity filtering.
3. `waking.rs:1347` settle_stopped calls settle_rested. `:3044` settle_rested FIRST calls record_context_at_stop. `:2715–2740` that function resolves stored node→Claude transcript→context_tokens, then performs Record.Context. It returns `()` on no node, non-Claude, unreadable context or record failure; failure merely logs, so its call does not yield a successful fresh-measurement receipt.
4. `settle_rested:3044ff` then waits for rest, takes dispatch_gate, resolves awake metaflow/address hold/current node, and `:3091` asks past_threshold. At `:3137ff`, a due maintained seat or waking queue goes to refresh_successor_first (`:2779ff`), otherwise successor_composes then close_at_rest (`:2761–2777`). Close takes the pane lease, performs Operation.Close(node.clone()), then Record.Stopped(flow_id). `settle_stopped:1347–1375` clears refresh-refusal latch/wakes deferred after resulting action.
5. There is currently no context-warning step ordered before close. Old context rows do not prove this Stop produced a fresh measurement; Codex app-server measurement is not a Claude hook receipt.

## Existing lower delivery capability after ordinary Past guard

`delivery.rs:199–236` DeliversMessages::deliver resolves target/body, applies ordinary PastThreshold guard at216–226, then takes `pane_leases.hold(&target.route)` and invokes the private `LeasedDelivery::new(self,&request,&target).run()`.

Exact existing private owner/type:

```rust
// delivery.rs:326–359
struct LeasedDelivery<'run> {
    nexus: &'run RunningNexus,
    request: &'run DeliveryRequest,
    target: &'run DeliveryTarget,
}
// RunsLeasedDelivery supplies:
fn run(&self) -> Result<Delivery, DeliveryRejection>;
```

`DeliveryTarget:72–118` captures stored FlowNode (FlowId/native session), HerdrRoute and HarnessProfile. It refuses stopped/retired/exited flows, held successors and unavailable routes. This is node/route ownership; there is no additional warning-specific fresh native-session/context identity guard. `writable_state:161–188` checks live ready agent, non-Blocked and blank composer. The route carries exact Herdr session/pane/terminal.

`run:461–600` uses this exact target, records a lease step, optionally interrupts for HardAbrupt, then `Herdr.place(route,text,observe)` at539–550. Lower existing `WritesPane::place` is declared `herdr/pane.rs:82`, implemented279; `submit:124` and composer-submission observation are existing separate operations. No distinct native control-notice injection function was found in these bounded paths. Private delivery capability, ordinary policy admission and raw route writer are separate layers; this is not authorization to bypass ordinary Past for arbitrary messages.

## Exact effects and observations

- `Placement::Refused`→DeliveryRejection::NotDelivered.
- `submitted:412–433` observes composer departure, may submit again, and may retract still-held text. `Submitted::TakenBack`→ComposerOccupied.
- `run:560–599`: stuck/unknown placement yields DeliveryGrade::Uncertain; successful transport/submission without observed reaction yields Transported; Presented requires BOTH Herdr agent_prompted reaction for the exact pane/terminal AND text observed leaving composer.
- Presented is a placement/submission/reaction observation, not model consumption or a read receipt. Neither Transported nor Presented establishes the warning was cognitively received before retirement.
- `settle:390–410` returns Ok(Delivery) even if persistence of outcome fails; it logs, and the retained lease resolves Uncertain on reopen. The receipt can therefore be a transport observation without a durable recorded success.
- `close_at_rest:2761–2777` uses the same pane lease around Close, preventing interleaving writes. The existing program does not sequence a warning-delivery result before that close; the lease alone supplies no warning order or guarantee.

## Exact remaining delivery gap

No existing source guarantee places and observes a same-session context warning before close/retirement, nor guarantees reading it. The usable bounded mechanisms are private LeasedDelivery with exact captured target and pane lease, followed by explicit grades, plus current close ordering. A warning-specific capability/identity/order/failure contract requires Primary/Core judgment. No successor delivery, refresh-prevention, blanket Past bypass, cached-row trigger, Codex hook parity or hook-stdout channel is inferred here. Warning bodies remain held; the unchanged reviewed052 implementation proceeds.

## Aggregate bound and lock-order audit, finite executor path only

There is NO current aggregate wall-clock bound. `herdr/pane.rs:239–255` composer read,265–276 press,280–303 place use blocking `Command.output()` with no parent deadline/kill. Herdr observation `herdr.rs:267–280` --timeout10000 is only a CLI observation parameter. `pane_agent:198ff` reads snapshot; `herdr.rs:744–747` snapshot uses another unbounded output(). Pane lease `delivery/lease.rs:49–65` uses Mutex.lock and Condvar.wait without deadline. Durable delivery step/settle `delivery.rs:375–410`→`store/delivery.rs:290–331` performs engine reads/mutations/atomic commits without an explicit wall-clock budget. Component wait values do not bound these operations.

Finite loops: submission12 reads*350ms sleeps (`pane.rs:51–64,99–113`), each read still unbounded. `delivery.rs:412–433` can execute3 such submission passes (initial, after extra submit, after take_back); presses are also unbounded. Interrupt branch has3 attempts and3000ms Herdrwait flag but no subprocess deadline. Proposed Soft warning skips interrupt, not the other waits.

Current ordinary meta lock chain `lib.rs:1334–1347` dispatch_gate→dispatch_meta_from Deliver:571→delivery.rs230 PaneLease→private run→engine calls. Settlement `waking.rs:3064ff` already holds dispatch_gate; close2761 takes PaneLease. Private LeasedDelivery.run acquires neither dispatch_gate nor PaneLease itself. Public serialized dispatch under held gate would recurse on nonrecursive mutex; calling public deliver while already holding the same pane lease would wait on itself. Neither mutex/condvar nor storage waits have an aggregate deadline. Accepted Transport.HerdrPrompt/HerdrCall and Pane submission settings describe future configured components, not an already-enforced whole-attempt cancellation bound. No finite-before-retirement guarantee can be inferred from this current executor.
