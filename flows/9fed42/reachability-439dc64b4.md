# Reachability, flow socket, 439dc64b4

Source: flows/f5a6e9/reports/flow-buildable-design.md at 439dc64b4 (blob 66bd01a8; read; line numbers are that file's). 439dc64b4 is an ancestor of origin/main.

## Identify.Process
| Return | Condition | Lines |
|---|---|---|
| Identified.Address | ancestor walk reaches a Flow record's Process, pid and start time match | 313, 774-778 |
| Refused.Unidentified.Process | in no metaflow | 383-384, 777-778 |
| Refused.Store | store failure; Identify named | 794-797 |
| Refused.NotMessage | does not apply: any local peer may ask | 379-382 |

## Lock.{ Sender Recipient }
| Return | Condition | Lines |
|---|---|---|
| Locked.Lock | granted, carries resolved Address and Up | 311, 679-682 |
| Refused.Locked | refresh under way | 331, 687-688 |
| Refused.Held.Lock | held lock | 332, 688-689 |
| Refused.Unknown.Address | Sender or Up target names no metaflow; also Recipient naming none | 343-345, 694-696, 698-699 |
| Granted (Asleep Recipient) | an Asleep recipient is granted | 700 |
| Refused.Ended.Address | Sender's metaflow Ended; also Recipient Ended | 367-370, 697-698, 700-701 |
| Refused.NoneAbove | Up above Primary | 376, 693-694 |
| Refused.Asleep | Sender's metaflow Asleep | 696-697 |
| Refused.OffRoute | off vision-aspects routes | 371-375, 719-720 |
| Refused.NotMessage | peer not bound Message binary; dead bound process on re-check also, binding dropped | 377-382, 726-731, 770-772 |
| Refused.NoLayer | Asleep recipient, no Model for its layer | 356-360, 702-709 |
| Refused.Unknown.Key | Asleep recipient, a module the wake would compose forgotten since; empty module set valid | 350-355, 704-710 |
| Refused.Store | store failure | 794-797 |

## Deliver.{ Lock Request }
| Return | Condition | Lines |
|---|---|---|
| Delivered | awake, can take it now | 314, 627-628, 683-684 |
| Queued | asleep + result/notice; awake and busy; never when the wake's configuration changed | 316-317, 631-636, 645-649, 711-714 |
| Woken.FlowId | asleep + order/question/psyche(s) | 318-320, 630-632 |
| Refused.Lapsed | granted lock ran out | 339, 718-719 |
| Refused.Unknown.Lock | never granted or consumed | 346-347, 719 |
| Refused.Ended.Address | Deliver named in the variant gloss (recipient Ended); no sentence says when | 367-370 |
| Refused.NoLayer / Unknown.Key | Asleep recipient, configuration changed between Lock and Deliver: same refusal, never Queued | 356-360, 350-355, 711-714 |
| Refused.NotMessage | peer not Message binary; dead bound process on re-check | 377-382, 726-731, 770-772 |
| Refused.Store | store failure | 794-797 |

## Requested items
| Item | Status | Lines |
|---|---|---|
| Awake.FlowId | unreachable (Launch only) | 334-336, 628-630 |
| Unknown.FlowId | unreachable (Report, Stop, Observe.Agent) | 348-349, 401-402 |
| Unknown.Key | reachable at Lock and Deliver for an Asleep recipient, only for a module the wake would compose that was forgotten since; unregistered topic (empty set) is valid, no refusal; also Launch, Forget | 350-355, 704-710, 533, 555 |
| NoLayer | reachable at Lock and Deliver for an Asleep recipient with no Model for its layer; also Launch | 356-360, 702-709, 532-533 |
| NotConfigured | unreachable (Launch; not needed for Lock, Deliver, Release, Identify) | 361-362, 530-536 |
| Taken.Address | unreachable (Bind) | 387-388, 742-743 |

## Other unreachable
HashMismatch (Launch at compose, 363-366, 536-540). Per query: OffRoute never at Deliver (719-720); Lapsed and Unknown.Lock never at Identify or Lock.

## Left open
1. Deliver: refusals beyond Lapsed, Unknown.Lock, NotMessage, NoLayer, Unknown.Key, Store unnamed; Ended.Address gloss lists Deliver (367-368) but no sentence says when. Held.Lock stated for lock requests (688-689), not at Deliver.
2. Asleep wake path at Lock for a Recipient: stated (700, 702-710). Closed: Recipient naming none, Asleep, Ended (698-701); NotMessage for Identify (380); dead bound process (770-772); config change after lock (711-714).
