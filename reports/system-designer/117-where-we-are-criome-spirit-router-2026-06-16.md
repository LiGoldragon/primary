# 117 — Where we are: criome / spirit / router — full picture

*A "where is everything" status with visuals, requested by the psyche. Covers what
is built, what is decided, what is intended, and the current blocker. Consolidates
reports 112–116, the SO audit 225, and the live design discussion. Spirit is down
(`primary-4bw6`), so the three decisions below are queued in `spiritbackup.nota`, not
yet in the intent store.*

## Status at a glance

| Layer | State | Where |
|---|---|---|
| criome real BLS sign/verify | **built, tested** (branch, unmerged) | `criome-auth-pilot`; reports 113/114 |
| criome audit P1 fixes | **open** (7 mine + the registry gap) | SO audit 225; `kr40` |
| criome registry admission / trust root | **decided, not built** | decision A; `kr40` |
| spirit criome-auth pilot (per-op attestation) | **decided, not built** | `5zur`; `w2g3`/`2st7` |
| CriomOS comms architecture | **decided, not built** | report 116; queued in `spiritbackup.nota` |
| router network transport | **intended** | report 116 staged plan |
| intra-host sandbox↔router (tap/L3) | **decided, not built** | decision B |
| mirror per-system + auth ingest | **decided, not built** | decision D; corrects `0yx5` |
| spirit→mirror shipper (e2e leg 1) | **does not exist** | report 116 |
| spirit-daemon | **DOWN** (outage) | `primary-4bw6` |

## The target topology (intended)

```mermaid
flowchart TB
  subgraph NodeA["System A — ONE router per system"]
    direction TB
    subgraph VMa1["microVM sandbox · agent 1 (smart space)"]
      spiritA["spirit<br/>(intent)"]
      msgA["message<br/>(SO_PEERCRED ingress)"]
      criomeA["criome<br/>(auth-only)"]
    end
    subgraph VMa2["microVM sandbox · agent 2"]
      a2["component<br/>agent-spaces"]
    end
    routerA["router<br/>(per-system fabric)"]
    mirrorA["mirror<br/>(object VC)"]
    VMa1 -->|tap/L3| routerA
    VMa2 -->|tap/L3| routerA
    criomeA -.->|sign / verify| routerA
    spiritA -->|ship outbox| mirrorA
  end
  subgraph NodeB["System B"]
    routerB["router"]
    criomeB["criome"]
    mirrorB["mirror"]
    criomeB -.->|verify| routerB
  end
  routerA <==>|"tailnet TCP · encrypted · BLS-attested frames"| routerB
  mirrorA <-->|"tailnet fetch · blake3 objects"| mirrorB
```

criome **signs**, router **transports** (cross-sandbox + cross-network), mirror
**moves bytes**, the tailnet **encrypts**, BLS **authenticates**. One router per
system; one microVM per agent.

## The end-to-end flow (intended)

```mermaid
sequenceDiagram
  participant S as spirit·A
  participant M as mirror·A
  participant RA as router·A
  participant C as criome·A
  participant RB as router·B
  participant CB as criome·B
  participant MB as mirror·B
  S->>S: Record (sema commit + outbox)
  S-->>M: ship outbox suffix (tailnet)  %% leg NOT built yet
  RA->>C: Sign(frame digest)
  C-->>RA: BLS attestation
  RA->>RB: frame + attestation (tailnet, encrypted)
  RB->>CB: VerifyAttestation
  CB-->>RB: Valid (signer chained to cluster root)
  RB->>RB: Persona/mind decides delivery
  RB-->>MB: MirrorObjectNotify (blake3 ref)
  MB->>M: fetch object (ImportSession)
  M-->>MB: object bytes
```

The two legs that do not exist yet: **spirit→mirror ship** (no mirror dep in spirit)
and **real cross-router auth** (criome registry has no admission control; BLS is real
only on the unmerged branch).

## The roadmap (staged)

```mermaid
flowchart LR
  subgraph DONE["done"]
    bls["criome real BLS<br/>sign/verify (branch)"]
  end
  subgraph NOW["now — blocked / in progress"]
    spdown["fix spirit outage<br/>(operator, primary-4bw6)"]
  end
  subgraph CORE["1 · criome security core"]
    p1["merge BLS branch<br/>+ SO P1 fixes"]
    adm["registry admission<br/>+ cluster-root trust"]
  end
  subgraph SHIP["2 · object leg"]
    ship["spirit→mirror shipper<br/>+ authenticated ingest"]
  end
  subgraph NET["3 · router transport"]
    net["lift TcpListener into router<br/>+ signal-router net roots<br/>+ VerifyAttestation + replay window"]
  end
  subgraph INTRA["4 · intra-host"]
    intra["tap/L3 sandbox↔router<br/>+ cross-VM origin proof"]
  end
  subgraph E2E["5 · two-node e2e"]
    e2e["ouranos↔prometheus<br/>spirit→sign→route→fetch"]
  end
  bls --> p1 --> adm --> ship --> net --> intra --> e2e
  spdown -.->|unblocks capture| p1
```

## Decisions captured (queued in spiritbackup.nota until spirit returns)

- **Architecture** (Decision): per-agent microVM sandboxes; one per-system router as
  the cross-sandbox + cross-network fabric; criome auth-only, router transports,
  mirror moves bytes, tailnet encrypts, BLS authenticates; intra-host tap/L3. Realizes
  `i99x`; narrows `l3k4` (harness-ack → local path only); refines `a4i6`; keeps `alom`.
- **Trust root** (Decision): a cluster-root identity signs member keys = criome's
  registry admission gate; peers trust keys chained to the root. The #1 prerequisite.
- **Mirror** (Correction of `0yx5`): per-system mirror with authenticated object
  ingest; router carries the notify, mirror keeps its fetch transport.

## The blocker

spirit-daemon is down on ouranos since 13:06 — a deployed `spirit-migrate-store`
rejects the live store's schema 10 (`primary-4bw6`; same v9/v10 root as `9cop`). Store
data is intact; a rollback of the 13:06 deploy (or a migrate-store fix to no-op on
schema 10) recovers it. Operator is on it. Until then, all intent capture queues in
`spiritbackup.nota` and replays through the guardian on recovery.

## What's mine to do next (once spirit is back / on your steer)

1. Replay `spiritbackup.nota` through spirit (the 3 decisions).
2. The **criome security core**: merge `criome-auth-pilot` + land the SO `225` P1
   fixes + build registry admission control + the cluster-root trust bootstrap
   (decision A). This is the foundation; networking builds on it.
3. Then the object leg (spirit→mirror shipper), the router transport, intra-host, and
   the two-node e2e — in that order.
