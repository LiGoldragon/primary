# Flow, the anatomy

```
          ┌──────────────┐
          │ Library      │ 23 types, 9 traits
          │ shared types │ every trait input is
          │ and traits   │ a concrete type
          └──────┬───────┘
      imports    │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
┌─────────┐  ┌───────────┐  ┌──────────┐
│ Signal  │─▶│ Operation │─▶│ Memory   │
│ says    │  │ does      │  │ keeps    │
│ 14      │  │ 15 ops;   │  │ 8        │
│ queries │  │ 9 queries │  │ records; │
│         │◀─│ have none │◀─│ no       │
│         │  │           │  │ versions │
└─────────┘  └───────────┘  └──────────┘
```

Flow's ethos has its types; what it lacks are traits in ethos's own form, operations behind nine of its queries, versions on its records, and the pieces below. Every missing piece is one question; answer by number, one line each.

## Distillation

### Ruling 1 — the one form that governs every trait

Ethos's own line: a concrete type in a capability's input is a trait not yet named. The generator that exists today refuses all fourteen inputs in Flow's traits for that reason.

```
Wakeable.[                 ; wrong: Request is a
   wake!{ [ Request ]      ; type, refused
          [ Result<FlowId Refusal> ] } ]

Wakeable.[                 ; right: the input is
   wake!{ [ Requesting ]   ; a trait the request
          [ Result<FlowId Refusal> ] } ]
```

File: psyche-skills `skills/vision-ethos.md`, «Trait».

Ruling 1: (a) every input becomes a trait the type bears, so Flow's Library gains a one-capability trait per input type, Request bears Requesting, Module bears Composing, and so on; (b) ethos lets a declared type stand as an input, and the vision-ethos line changes to say so; (c) yours.

### Fixed in the next edition without a ruling

| was | becomes | why |
|---|---|---|
| Report and Stop carry a FlowId | the caller is the identified process | no flow declares its id |
| Identifiable and Unidentified declared in Flow's Library | imported from the nexus library | «The caller is witnessed» |
| HarnessKind, Aspect, Verdict, Lock used unimported; Nexus declared in the meta Signal | imported where used; Nexus declared in the Library | the generator refuses them |
| Memory records only imported | declared in Memory | the generator refuses them |
| Hash.Bytes<32> | Hash.String until Bytes exists | the generator refuses it |
| Composable | Assemblable | datom-codec already has a Composable |

### The missing anatomy, as questions

Each question names the skill its answer lands in.

Identity and records

2. Does every Flow type fingerprint itself by the hash of its rkyv archive, or only Hash and FlowId? — vision-nexus
3. Where does a record's former form live for its upgrade: beside it in the same ethos file, or in the file's previous commit? — vision-ethos
4. Does the Flow record keep the harness session id, or only its hash? — vision-flow
5. Is the third root named Memory or Sema? vision-sema says Sema, vision-ethos says Memory. — vision-sema

Reading and observing

6. Is a read of memory, Show, List, Identify, an operation of its own, Observe, or may Signal read Memory directly? — vision-nexus
7. Does a subscription end when its connection closes, or by an Unsubscribe query; and is the subscriber a record? — vision-nexus
8. Which observation does Sent stand for: placed in the harness, submitted, consumed, or entered the flow's context? — vision-messaging
9. Does a request carry its delivery tier, hard abrupt, middle abrupt, soft, or does Flow choose it? — vision-messaging
10. What does a registered poller's record hold? — vision-flow

Launching and a flow's life

11. Does Flow's ethos carry the Capsule now, or once the Capsule is built; and does Launch name the working directory, or does the Capsule? — vision-flow
12. Besides start, tool use, context measure and stop, which hook events does Flow hear: the final reply, the marked transcript block, idle? — vision-flow
13. Is the handover a record Flow stores and hands the successor, or text the flow writes itself? — vision-flow
14. Does a subflow get a metaflow address of its own, and is the request id Flow's, returned by Launch? — vision-flow
15. Is the router of a flow's ending questions a Flow operation, or a Field flow that Flow launches? — vision-flow
16. Does a module's key say where it goes, system prompt or first prompt, or does its subaspect decide? — vision-flow
17. Is the model that judges waking one more Model entry in Flow's configuration? — vision-flow
18. When a lock lapses, what frees it: a timer Flow arms, or the next request? — vision-flow

Configuration and the wire

19. While Flow is unconfigured, does its ordinary socket accept Configure? — vision-nexus
20. Does the Nexus record hold Flow's own socket paths, and are Configure payloads datom files the meta CLI replays at start? — vision-nexus
21. Are the speaking routes Flow enforces configuration, or fixed in code? — vision-flow
22. Does Flow import Message's wire types, or Message Flow's? — vision-nexus
23. Does Flow's Signal take its frame, protocol version and handshake from the shared signal library? — vision-signal
24. Is the step from query to operation a shared trait, Apply, borne by every query? — vision-nexus
25. Are the Signal, Operation and Memory actors declared in ethos now, or after their standards are designed? — vision-nexus

Shared with every Nexus

26. Does the shared nexus library also carry the clock, Instant, and the executable's identity, or only the process? — vision-nexus
27. Do Source and the module registry belong to Flow, or to a shared library every Nexus with modules uses? — vision-nexus
28. Does Flow's ethos reserve the private part now, or wait for the open-source seat? — vision-flow
29. When a topic fails the word check, does Flow refuse with its own variant, or carry protos's refusal? — vision-protos

Where two skills disagree

30. Power: vision-model-roles has Power with four values, Ultra Low among them; the ethos has Effort.[ High Medium Low ]. Which stands? — vision-model-roles
31. Priority: vision-messaging has priority as a head on the datom; the fourth edition says the tiers are gone. Which stands? — vision-messaging
32. Voice: vision-flow says a flow is one run of a voice, aspect and layer; the ethos addresses by aspect, topic and layer with no Voice. Does Voice go? — vision-flow
