---
title: 393 — Cloud domain consumer alignment
role: cloud-operator
variant: Synthesis
date: 2026-06-24
topics: [cloud, domain-resolution, test-cluster, intent-alignment]
description: |
  Intent-alignment handoff for the cloud-operator next slice after report
  392: whether to finish the CriomOS-test-cluster domain consumer update
  with pure checks and release the current cloud-operator claim.
---

# 393 — Cloud domain consumer alignment

## Intent Anchors

[Cluster configuration and Horizon should carry the public-domain mapping for ordinary DNS fallback: criome.net is assigned per cluster, with goldragon owning goldragon.criome.net; the exact NOTA shape is open, but the data belongs in cluster config rather than being hardcoded downstream.]

[The Immich-backed agentic media mirror from videographer proposal 6 is a target to build, and is to be one of the first public web-hosting deployments of the CriomOS web-host system. cloud-designer ports and maintains its hosting and infrastructure in tandem with the videographer lane, which owns the media and capture craft.]

[CriomOS provides a website-hosting node service so the psyche can host websites: a user configures a source to be rendered and served from a node, the service supports multiple renderer variants, and the standard default for now is a markdown-based static site in the Jekyll mould. This is the first concrete role doris, the low-trust DigitalOcean cloud node, can fill.]

[Cloud-hosted compute nodes are assigned low cluster trust; doris is a real but minimally-trusted cluster member because it runs on third-party provider hardware outside the operator's physical control.]

## Spirit Gate

The current psyche prompt is a task order plus one-time lane authorization: run `skills/intent-alignment.md` on the forwarded cloud-operator situation prompt, with permission to work in the `cloud-operator` lane. That is task state, not a durable workspace rule, so no new Spirit record was captured.

The forwarded text is agent-written synthesis rather than psyche intent. I gap-checked relevant public Spirit records before aligning. The notable mismatch remains Cloudflare credential wording: public Spirit currently names `cloudflare.com/api-token` as the canonical gopass path for the Cloudflare API token, while report 392 says recent reports and BEADS point at `cloudflare.com/token`. I found no public Spirit record for `cloudflare.com/token`.

## Alignment Result

The first useful slice is already narrow enough to execute if the psyche accepts it: finish the current `CriomOS-test-cluster` domain consumer migration using pure/eval checks, then release the `cloud-operator` claim.

This slice should not include live Cloudflare mutation. Cloudflare has a real credential-path and authorization ambiguity, and live DNS work should wait until the canonical gopass path and token scope are reconciled.

This slice should not decide the full Immich/WebHost hosting model. The shared domain spine needs to support both low-trust static hosting on doris and a trusted-node dynamic application for Immich, but the current test-cluster work only needs to prove that downstream consumers read the projected cluster domain data instead of hardcoding public names.

The missing `CriomOS-test-cluster/ARCHITECTURE.md` is a repo-contract gap. It is adjacent to the current work, but it is not the highest-risk first slice unless the psyche wants the lane to spend the extra scope now.

## Focused Question

Should `cloud-operator` finish the current `CriomOS-test-cluster` domain consumer slice now, using pure/eval checks only, then commit, push, and release the claim?

Recommended answer: yes. The working copy already contains the partial domain-config migration, the claim is blocking later test-cluster work, and pure checks are the right proof surface before any authorized QEMU or live-provider work. The acceptance line should be: projected fixtures still match, structural contracts pass, rejection checks pass, and at least one real downstream consumer is shown to use `cluster.domainConfiguration` rather than a hardcoded `criome.net`.

Alternative one: include a short `ARCHITECTURE.md` in the same landing. That closes the repo-contract gap now, but widens the slice from consumer proof into repo documentation.

Alternative two: pause the test-cluster landing until Cloudflare credential-path intent is resolved. That reduces provider ambiguity before future DNS work, but leaves the current test-cluster claim blocking unrelated follow-on work.

## Handoff If Accepted

Run the slice as cloud-operator against `/git/github.com/LiGoldragon/CriomOS-test-cluster`:

1. Read the repo `INTENT.md` and `AGENTS.md`; note the absent `ARCHITECTURE.md` as a gap, but do not fill it unless the psyche chooses that alternative.
2. Inspect the current `domainConfiguration` projection in generated cluster JSON and the fixture source shape that produced it.
3. Run only pure/eval checks: projection equality, cluster contracts, module contracts, source constraints, and rejection checks.
4. Add or repair the smallest pure witness that proves a downstream consumer reads `cluster.domainConfiguration`.
5. Commit and push the whole working copy in the relevant repo, then release the `cloud-operator` claim.

## Deferred Questions

Cloudflare credential path: reconcile `cloudflare.com/api-token` from Spirit record `nsi2` with the newer `cloudflare.com/token` wording before any live DNS mutation.

Public-domain shape: decide later whether `publicClusterDomains` as a simple vector means full cluster-subdomain coverage, or whether typed coverage metadata is needed before more consumers depend on it.

Immich hosting: derive the public phone URL from the cluster domain, but choose the trusted node and auth exposure model before implementation.

WebHost dynamic mode: decide later whether reverse-proxy-to-upstream is a variant of `HostedSite` or a sibling typed variant.

## Report Hygiene

`reports/cloud-operator/` was at the 12-report soft cap before this file. I reviewed the directory index and kept the existing reports: recent reports 389, 390, 391, and 392 are active context for this alignment; older entries cover distinct live investigations, tombstones, or implementation audits whose substance has not been safely migrated in this slice.
