# Graphical role history

Method: code read repository history and current Horizon/CriomOS sources through the delegated `graphical_role_history` subflow on 2026-08-25.

The remembered role is `NodeSpecies::Edge`. The effective graphical predicate was and remains `behavesAs.edge`, derived from the union `Edge | Hybrid | EdgeTesting`; it was never a standalone `Graphical` species.

Horizon revision `0b386260655e` (2026-04-23) introduced `NodeSpecies`, duplicate one-hot `TypeIs`, derived `BehavesAs`, and `has_video_output`. `BehavesAs::derive` set `edge` from the three edge-like species, and proposal projection made `has_video_output` follow it. CriomOS revision `febf8560e5ea` (2026-04-24) placed the Edge desktop module behind `behavesAs.edge`.

Revision `750f8cf6eae3` (2026-06-20) removed duplicate `TypeIs`, but deliberately retained `BehavesAs` as the cross-repository gate. Current Horizon still derives `behavesAs.edge` from the same species union and retains `has_video_output` as an alias.

Agent Intercom roles have a separate history:

```text
2026-07-20  AgentIntercomGateway + AgentIntercomPeer
              remote topology/transport roles
                    |
2026-07-23  AgentIntercomLocal + AgentIntercomGraphical
              local runtime + additive GUI integration
                    |
2026-07-29  both become explicit opt-in capabilities;
            Graphical requires Local and no longer follows species
```

Thus current sources hold two independent meanings of graphical:

```text
Node species ──► behavesAs.edge
                 general OS/Home desktop policy and video-output alias

Node services ─► AgentIntercomLocal ─► local agent runtime and CLIs
                    └─ + Graphical ─► Codex-specific GUI prerequisites/package
```

Gateway/Peer remote endpoint, credential, pairing, and listener semantics were rejected rather than carried forward. General Edge desktop gating was preserved. Agent Intercom graphical behavior moved to explicit per-node service capability.
