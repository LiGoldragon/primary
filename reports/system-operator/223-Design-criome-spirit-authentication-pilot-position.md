---
title: 223 - Criome Spirit authentication pilot position
role: system-operator
variant: Design
date: 2026-06-16
topics: [criome, spirit, authentication, authorization]
description: |
  System-operator position after the psyche forwarded the Criome/Spirit
  authentication prompt to system-designer and asked this lane to join the
  conversation.
---

# 223 - Criome Spirit authentication pilot position

## Spirit Gate

I treated the prompt as forwarded to system-designer plus an explicit invitation
for system-operator to join. I queried the current Spirit authentication and
authorization neighborhood before recording anything.

Existing records already covered the general rule: components can escalate
authorization to Criome, Criome public keys are the authentication anchor, and
version-control history uses blake3 plus criome BLS for signatures. They did not
cover the narrower pilot choice. I recorded gap-fill Spirit record `w2g3`:

> Spirit should be an early pilot consumer of Criome-backed operation
> authorization: Spirit operations that require authentication ask Criome to
> authorize an exact content-addressed request or log-message digest, with the
> concrete envelope design still open.

I did not record the separate "move away from intent files into Spirit" thought.
It is important, but the prompt says "I think" and it conflicts with the active
workspace contract that still requires per-repo `INTENT.md` as first read. That
needs an explicit psyche decision before agents rewrite the guidance stack.

## Current Ground

`criome` already has the right boundary in its repo intent and architecture:
Criome verifies signatures and authorization grants for exact bytes; Persona and
component daemons decide what those bytes mean. The authorization model is
digest-first: a request is permitted only when signatures over the canonical
request digest satisfy Criome policy for that exact request.

Spirit already has the right consumer shape: a working Signal socket, a
meta-signal owner socket, a guardian admission path, and a SEMA store whose log
is becoming the authoritative source of truth. It also already has an
owner-only import path that bypasses the guardian, which makes authentication
more urgent rather than optional.

The clean integration is therefore not "Criome replaces the guardian." It is:
Criome authenticates and authorizes the principal over exact operation bytes;
Spirit's guardian judges whether the authenticated operation is acceptable
intent or policy state; SEMA records the operation and its provenance.

## Operator Shape

The first design target should be an authorization envelope that Spirit can
attach to an accepted operation and eventually to a SEMA log entry. That
envelope should bind at least:

- the component and contract namespace (`spirit`, working or meta);
- the operation root and schema/contract hash;
- the canonical operation payload digest;
- the target store identity, branch or head precondition when available;
- the requesting principal identity;
- nonce, expiry, and replay domain;
- Criome policy identity and collected signature proof.

The digest should be over canonical binary/rkyv bytes, not human NOTA text.
NOTA remains the CLI edge; the daemon path authorizes the same bytes it will
decode and execute.

The order should be explicit:

1. Signal admission validates framing and derives the canonical operation
   digest.
2. Spirit asks Criome to authorize that digest for the relevant operation class.
3. If Criome denies or is unavailable for a required class, the operation fails
   before semantic mutation.
4. If Criome grants, Spirit includes the principal and grant in guardian context.
5. The guardian admits, rejects, or transforms according to Spirit semantics.
6. The final write logs the operation, guardian verdict, and authorization
   envelope together.

For ordinary local reads, this can start permissive or socket-authenticated. For
writes, owner-only meta operations, imports, migrations, and future remote
version-control ingest, fail-closed is the safer target.

## Design Tension To Keep Visible

The implementation must keep three authorities separate:

- filesystem/socket authority answers "can this local process reach this tier";
- Criome answers "is this principal authorized for this exact digest";
- Spirit guardian answers "does this operation satisfy Spirit's semantic intent
  discipline."

Collapsing them makes the system harder to audit. A guardian rejection is not an
authentication failure. A Criome denial is not a semantic contradiction. A
socket peer-credential mismatch is not a bad signature. Those should produce
different typed rejections.

The SEMA version-control work then gets a natural signature target: signed heads
and checkpoints are aggregate attestations, while operation authorization grants
are per-operation provenance. They should compose, not compete.

## Open Decisions

The intent-file migration needs a direct psyche call. The likely end-state may
be "Spirit is the only raw intent substrate; `INTENT.md` becomes a generated or
architecture-adjacent summary," but that is not the current contract. Until the
contract changes, agents must keep reading repo `INTENT.md` first.

The exact authorization vocabulary belongs in `signal-criome` /
`meta-signal-criome`, not in Spirit. Spirit should consume a reusable Criome
authorization request and grant shape. If Spirit needs a component-specific
purpose value, that purpose should still be typed, not a free string.

The fallback mode before Criome is fully production-ready must be named. Either
Spirit keeps today's socket/guardian path for local development with a visible
"unauthenticated-local" provenance class, or persistent writes fail closed once
the pilot lands. Silent fallback would undermine the pilot.

## Immediate Recommendation

System-designer should draw the concept with Criome as the reusable
authentication/authorization substrate and Spirit as the first demanding client.
Operator implementation should wait until the current Spirit schema/SEMA stack
is stable enough to add the new gate once, at Signal admission or Nexus intake,
rather than thread ad-hoc auth checks through individual operations.
