---
title: 392 — Cloud-operator situation insights and questions
role: cloud-operator
variant: Synthesis
date: 2026-06-23
topics: [cloud, domain-resolution, criomos, web-host, test-cluster]
description: |
  Situation synthesis after loading the cloud-operator lane, active claims,
  relevant Spirit intent, recent cloud-designer handoffs, BEADS, and the
  current CriomOS-test-cluster working copy.
---

# 392 — Cloud-operator situation insights and questions

## Intent Anchors

[Cluster configuration and Horizon should carry the public-domain mapping for ordinary DNS fallback: criome.net is assigned per cluster, with goldragon owning goldragon.criome.net; the exact NOTA shape is open, but the data belongs in cluster config rather than being hardcoded downstream.]

[Mobile Android clients on the Criome WiFi access point should get near-native name resolution for cluster services; improve the AP-to-Android resolving path before falling back to ordinary public DNS names.]

[The Immich-backed agentic media mirror from videographer proposal 6 is a target to build, and is to be one of the first public web-hosting deployments of the CriomOS web-host system. cloud-designer ports and maintains its hosting and infrastructure in tandem with the videographer lane, which owns the media and capture craft. It extends the web-host direction 878r toward hosting a dynamic application, and builds on the phone-media-mirror constraint vgon (Immich as the uploader, no Syncthing on the phone).]

[CriomOS provides a website-hosting node service so the psyche can host websites: a user configures a source to be rendered and served from a node, the service supports multiple renderer variants, and the standard default for now is a markdown-based static site in the Jekyll mould. The psyche requires the implementation be the most reliable and secure way to do it. This is the first concrete role doris, the low-trust DigitalOcean cloud node, can fill.]

## Situation

Cloud-operator is currently a qualified operator lane, not a separate discipline. The lane writes under `reports/cloud-operator/`, claims as `cloud-operator`, and inherits the operator rule: implement settled designs, surface design gaps in reports, and keep deployment/live-provider actions behind explicit authorization.

The active orchestration claim is `cloud-operator` on `/git/github.com/LiGoldragon/CriomOS-test-cluster` for `pan-cluster domain configuration consumer update`. A separate `cloud-maintainer` claim exists on `/git/github.com/LiGoldragon/cloud` for the DigitalOcean gopass credential-path fix. Those are adjacent but not the same work: this lane is carrying the cluster-fixture consumer path; cloud-maintainer is carrying provider-session maintenance.

The checked-out `CriomOS-test-cluster` working copy already contains a partial domain-configuration migration:

- `clusters/fieldlab.nota`, `clusters/fieldlab-pod-missing-super-node.nota`, and `clusters/fieldlab-two-controllers.nota` now end with `(criome [fieldlab.criome.net])`.
- All committed Horizon fixture JSON files now expose `cluster.domainConfiguration.internalSuffix = "criome"` and `publicClusterDomains = ["fieldlab.criome.net"]`.
- User-facing generated identity in the fixtures now uses `aria@fieldlab.criome.net` and `@aria:fieldlab.criome.net`.
- `flake.lock` is repinned to newer `horizon-rs`, `CriomOS`, `CriomOS-home`, and related component revisions.
- `AGENTS.md` and `INTENT.md` gained the rule that QEMU-backed VM checks run only on authorized VM-testing hosts.

`CriomOS-test-cluster` has an `INTENT.md` and `AGENTS.md`, but no `ARCHITECTURE.md` or `skills.md`. The missing `ARCHITECTURE.md` is a workspace-contract gap. It is not blocking the current read, because the repo intent is unusually explicit, but it should be filled when this lane next edits shared repo docs.

## Insights

The pan-cluster domain work is a shared spine, not a DNS-only cleanup. The same cluster-authored value now wants to feed AP-local Android resolution, public TLS names, web-host site domains, Immich reverse-proxy names, user identity fields, and eventually Cloudflare DNS publication. Treating it as one Horizon projection surface is the right pressure relief; hardcoding it separately in CriomOS, web-host, Immich, and cloud would multiply drift.

The current implementation shape appears to be in the narrow consumer phase. `horizon-rs` already emits `domainConfiguration` into projected cluster JSON, and the test-cluster fixture has been regenerated around it. The next useful cloud-operator step is not inventing the schema; it is proving downstream consumers read the projection: static checks for user identity, DNS rendering, and service-domain aliases.

`CriomOS-test-cluster` is becoming the place that catches accidental production leakage and projection regressions at the same time. That is healthy, but it increases the cost of holding the lane claim. BEAD `primary-exzf` (the de-branch criome cluster test work) explicitly says this claim is a near-term gate. If the domain-config consumer update is nearly done, finish and release; if not, split or narrow the claim so the criome-cluster-test work can proceed.

Cloudflare is capability-built but authorization-gated. Spirit still contains an older Cloudflare credential-path record naming `cloudflare.com/api-token`; cloud-designer report 69 and the BEADS notes say the live token path is `cloudflare.com/token`, and that the existing token lacks usable zone/DNS scope. This is either an intent/documentation drift or a real credential-path ambiguity. It should be resolved before any live DNS test.

DigitalOcean is no longer speculative in the cloud lane. The adapter live mutation and the daemon-spine live create/observe/destroy cycle have both been proven, and the CloudNode image was live-confirmed. The unresolved cloud risks have shifted from "can it mutate a provider" to "can the component do it with the right architecture, bounded blocking, coherent generated wire, and a durable CloudNode/lojix handoff."

WebHost changed the cloud priority stack. Doris has a concrete role for low-trust static hosting, while Immich explicitly does not belong on low-trust doris because it holds private media. That means one public-domain system needs to serve two trust models: low-trust static edge on doris and trusted dynamic app behind auth on an always-on node.

The VM-testing rules are getting crisper. `CriomOS-test-cluster` now separates structural/eval checks from QEMU-backed VM checks, and cloud-designer report 81 identified the missing `nixos-test` builder feature as the practical gate for VM checks. This should prevent accidental local QEMU runs and keeps cloud-operator work testable through pure checks first.

The LojixOS extraction is still rightly deferred. Report 390 frames it as a consequence after two or three concrete hardcoded-brand/domain seams are moved into config. The current domain-configuration migration is one such seam; it should land cleanly before starting a repo split.

## Questions

Should the current `CriomOS-test-cluster` domain-configuration slice finish as a pure/eval-only landing first? The working copy already has projected fixtures and doc changes. A sensible close would run the structural checks that do not require QEMU, fix any consumer regressions, commit/push main, and release the cloud-operator claim so `primary-exzf` can proceed.

Do you want the `CriomOS-test-cluster` missing `ARCHITECTURE.md` filled as part of this same lane, or kept separate? The repo intent already states the architecture clearly enough to synthesize a short file: fixture cluster, projection equality, static checks, VM checks, production-fact firewall. The trade-off is scope: doing it now closes a workspace-contract gap, but it adds doc churn to a code/data migration.

Which Cloudflare credential path is canonical for the daemon wrapper today: `cloudflare.com/token` or `cloudflare.com/api-token`? Reports and BEADS say `cloudflare.com/token`; one older Spirit record says `cloudflare.com/api-token`. The answer decides whether this is only stale intent/docs, or whether the live wrapper needs another credential-path correction.

For public cluster domains, is a vector of public roots enough for now, or should the projection carry coverage/type metadata? The current fixture shape is `publicClusterDomains: ["fieldlab.criome.net"]`; earlier report 390 sketched `(criome [(goldragon.criome.net ClusterSubdomain)])`. If every configured public domain means full cluster-subdomain coverage for now, the simple vector is beautiful. If partial coverage is already needed, the schema should say so before more consumers depend on the vector.

For Immich, should cloud-operator assume the public phone URL pattern is `immich.<cluster-public-domain>` while the app itself runs on a trusted node? That keeps the domain derivation consistent with WebHost, but the hosting decision still needs the trusted node name and exposure model.

Should `WebHost` dynamic reverse-proxy mode reuse `HostedSite`, or become a sibling typed variant? The static model is already `HostedSite { domain, source, renderer }`; Immich wants a domain plus upstream application target, not a source renderer. If the same noun stretches, it may become too broad. A closed enum such as rendered-static versus reverse-proxy-to-upstream may be the cleaner design surface.

## Recommended Next Slice

Finish the current `CriomOS-test-cluster` domain consumer update before taking new cloud work:

1. Inspect the updated `horizon-rs` projected shape and confirm the current `publicClusterDomains` vector is the intended schema.
2. Run pure checks only: `projections-match-fieldlab`, `cluster-contracts`, `full-module-contracts`, `source-constraints`, and rejection checks.
3. Add or adjust a pure check that proves at least one real downstream consumer uses `cluster.domainConfiguration` rather than hardcoded `criome.net`.
4. Decide whether to include a short `ARCHITECTURE.md` in the same landing.
5. Commit/push the whole working copy, then release the `cloud-operator` claim.

That closes the immediate lane responsibility and unblocks the next test-cluster sequence.
