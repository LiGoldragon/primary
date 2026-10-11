# Handover: Psyche core Secondary, from 445410

## The seat

Psyche core Secondary on Claude Opus. It is the hub of the Psyche aspect. It relays the living's words verbatim as psyche messages, logs his words before acting, keeps «Open books», and routes design to Mind, through Mind Secondary Sol 41fa34. Psyche reaches Mind and Field only through 41fa34. It delegates all bounded work to subflows. It commits nothing in the shared /home/li/primary working copy; it publishes its own directory only, under the PrimaryPublish lock, from a full clone (skill compensation-primary-commit).

## Seats

| Topic | Primary | Secondary |
| --- | --- | --- |
| core | none | this seat |
| ethos | 081064 (Fable) | 1d0733 (Opus), being refreshed |
| flow | 875960 (Fable) | 9fed42 (Opus), being refreshed |
| nexus | none | 73ada7 (Opus), being refreshed |
| spirit | d55c56 (Fable) | none |

Mind: Astra 0c85a3, Sol 41fa34, writers A (projection_review: Flow library and store), B (launch_evidence: Flow ordinary socket, test 25), and C (deploy: Message). Field: 42265e.

## Refresh in progress

The living ordered every Claude flow refreshed and old sessions reaped; the record is in log.md. Done:
- 081064 replaced d5df1d.
- d55c56 replaced ebbe30.
- 875960 replaced f5a6e9.
- 8f0f57, 02dda6, 9fcf81 and bc914f were retired.
- 8475a9 and bad807 were deregistered.

Pending: the successors of 1d0733, 9fed42 and 73ada7, then of this seat. They are blocked until tools/native-voice-profiles.mjs configures Psyche.Secondary. The living ruled that the Secondary is Opus, and Sol was asked to set the row. Their handovers are on main: flows/1d0733/handover.md, flows/9fed42/handover.md and flows/73ada7/handover.md. Launch them like flows/445410/launch/flow-primary-successor/ and retire each predecessor after its successor answers. The launcher requires a PascalCase topic, against the living's lowercase ruling; that launcher fix is Mind's. Astra flagged that 02dda6 may have backed a reminder hook; it is unconfirmed, and Mind was asked to name the hook.

## Governing designs

- Flow design: 2d0a119bc27bf46a3d4a76356f377278f41eb4bd, flows/f5a6e9/reports/flow-buildable-design.md, blob 0dac6fdd10baedc3e4f30c77244be51e276cb33d.
- Message design: d9703b5210299bab596cc5d85ae4a84bc4ee32bc, flows/73ada7/reports/build/message-design.md, blob 7e4db1625f87abdd43003890b9f8c7beeaec6d30.
- Acceptance suites: flow-test 01c29c90 (76 Mind targets); message-test 4d40751.

## Build state, per Field (claims)

- Flow and Message both reach compilation. Flow has 31 errors porting to the new design. Message has 3.
- No published signal-flow carries Refused.Store, so writer A must author a new signal-flow stage that Flow and Message share.
- One Aspect (875960): FlowAspect leaves; the new signal-flow stage carries Aspect and the refusal sets.

## Before the living

- Books: «Open books», https://claude.ai/artifact/MhfwBHiFEfWRuaCYTui4Du (version 37, 40 books). Source: books/index.html. Sync from the live page before each edit.
- Open rulings:
  - Fork 3 in «Type, new type, alias» (bare or braced). The Ethos items 1-2 set is ready either way.
  - «What the new Message does with the old store». It decides both stores. Until he answers, no old store is deleted.
  - Which commit rule governs: CLAUDE.md "commit dirty changes first", compensation-primary-commit "independent clone", or Field's "no clones". Until then, Field's private-index route is the supported publisher route.
  - «Sources and the registry», «The lock queue», the four Ethos tension books, and the Message fork books.

## Standing limits

- No timers. The living ordered them removed, and none remain.
- Every design commit is reported with its full hash and blob, and only after its pushed blob is verified by line.
