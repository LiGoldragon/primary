---
title: 129 - SO Router Intent Gap Check
role: system-designer
variant: Audit
date: 2026-06-17
topics: [router, intent, criome]
description: |
  Gap-check of the system-operator forwarded Router prompt against
  recent Spirit records, naming what SO logged and what remains only
  partially covered by older intent.
---

# 129 - SO Router Intent Gap Check

## Intent Anchors

[Router owns a standardized routing protocol: a router-typed envelope carries routing and object metadata for a serialized contract-owned rkyv payload, while Router remains payload-blind beyond the envelope, routing, authentication, and delivery policy.] (Spirit `57f9`)

[CriomOS communication architecture. Each agent runs in its own microVM sandbox. One router per system is the communication fabric, carrying cross-sandbox traffic locally and cross-network traffic router-to-router. criome stays auth-only; router transports; mirror version-controls and moves objects; the tailnet provides confidentiality and criome BLS attestations provide per-frame authenticity.] (Spirit `wckt`)

[domain-criome is the authority for .criome domains; each .criome domain is its own authority server, content-addressable. To check the current authority for a domain, ask the domain's own daemon. Last-snapshot per domain serves as cached state. This gives the workspace its own content-addressed DNS.] (Spirit `ty24`)

## Result

SO captured the central routing-protocol intent as Spirit `57f9`. That record says Router owns the standardized protocol envelope: Router sees router-owned routing/object metadata, then carries a serialized rkyv payload whose concrete contract remains owned by the originating component contract. This matches the forwarded prompt's durable center: Router gets a standard contract surface without becoming a shared schema bucket for every component's vocabulary.

I do not see a second new SO capture for the CreomOS hostname/security part of the prompt. The nearest existing records are `wckt` and `ty24`: `wckt` already says CriomOS has one router per system, router-to-router cross-network transport, tailnet confidentiality, and criome BLS per-frame authenticity; `ty24` says domain-criome is the authority for `.criome` domains as content-addressed DNS. Together they cover the broad system shape, but they do not specifically encode the short-term Router invariant discussed earlier: `router.<node>.<cluster>.criome` should lower to the expected Yggdrasil endpoint and Router should fail closed if the configured service endpoint does not match.

The contract-repo point is already covered by older intent: the signal contract repository is the canonical client-facing Signal type surface, with daemon-local Nexus and SEMA planes staying inside the daemon crate until a scale boundary forces extraction. That means SO did not need a new record just to say "the contract repo is the brilliance"; `57f9` applies that established triad pattern to Router's protocol envelope.

## Gap Assessment

No duplicate capture is needed for the core Router protocol. Spirit `57f9` is clean and high-certainty.

The likely gap is narrower: the short-term `.criome` service-name invariant for Router testing and spirit-vcs authenticated mirroring is documented in the Router architecture track, but I do not see it as a Spirit record. That may be correct if it is treated as implementation architecture rather than durable intent. If the psyche wants it to guide future agents independently of the current Router report, it should be captured as a clarification/decision against the existing CriomOS/router/domain-criome records rather than as a broad new principle.

My lean: do not record another broad "CreomOS hostnames are secure" entry. If captured, make it precise and operational:

`router.<node>.<cluster>.criome` is a service-scoped short-term Router name that must resolve or lower to the node's Yggdrasil address plus configured Router port under CriomOS-managed configuration; Router startup checks the resolved endpoint against its generated endpoint map and refuses to use a mismatched target. This gives the short-term live test path a fail-closed endpoint invariant while criome still proves peer/frame authenticity.
