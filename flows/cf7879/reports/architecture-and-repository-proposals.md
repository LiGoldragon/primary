# Architecture and repository proposals

These are review documents for items 36, 42, 43 and 41. They are not adopted architecture, repository moves, installed contracts or executable proofs. No Nix pass is claimed for this document. Code proofs and their individual Nix receipts are in to-840e42.md.

## 36 — Placement and bootstrap waves

Source: fd0f97/log.md, entry beginning “place every major idea”, and 840e42's current lane. Current implementation observations are bounded to the inspected code and receipts.

| Component | Proposed responsibility | Observed or pending |
|---|---|---|
| Flow | Identity claims, name registry, launch receipts, lifecycle observations and idleness subscriptions | Primary tools and proposal fixtures exist. No full deployed Flow Nexus or all-event hook coverage is witnessed. |
| Message | Typed durable delivery, routing, outbox and receipts; asks Flow for identity/idleness | Source fixtures and remote Nix checks pass. Primary approval blocks four live turns. Active-store migration remains held. |
| Psyche | Spirit, Intent, Vision and Notion records, their bounded domains and review/migration proposals | signal-psyche and psyche public scaffolds remain empty. Separate executable draft is under review; no contract adoption. |
| Persona | Per-person model/harness orchestration and ownership of the eventual core loop | Existing component source exists; migration of the temporary core loop is not performed. |
| Orchestrate | Coordination of concurrent writes and operations | The lock service was used during this work. It does not confer deployment or merge authority. |
| Lojix | Runtime placement/routing, authenticated peer identity and reconnect observations | Existing system service observed. Learned reconnect records remain proposed. |
| Cloud | Provider objects and explicit credential boundaries | Cloudflare read-only fixture is published; no DNS/account operation was performed. |
| CriomOS/Home | Declarative host/user services, packages and pinned runtime inputs | Existing monitor is running. Prosody/Forgejo/runner work is disabled proposal source. |
| Curriculum | Authored reusable skills and their generated projections | Generated .agents/.claude/.codex/.pi trees are not authoring targets. JJ-law changes remain proposals until integration review. |

Wave 1: finish source-bound relay receipts, tested Flow observations, bounded monitoring and truthful failure records. A real approval hold remains a hold.

Wave 2: review the disabled Prometheus provider configuration, Cloudflare boundary, TLS paths and native build-result artifacts. Accounts, DNS issuance, ingress, credentials and deployment belong to the separately authorized secondary stage.

Wave 3: use a proved encrypted chime channel and a thin mobile client to present builds to the living. A model runs at the cloud provider, not on the phone. Local phone harness mode is separate from the upstream Persona service.

Wave 4: adopt reviewed Psyche/Persona contracts and move the temporary core loop into its owner. Preserve source pointers, migration plans and real rollback boundaries. No automatic migration follows from this map.

Unresolved ownership: the primary has agreed to isolated producers but has not named the integrator pending receipt of the four held turns. No producer may infer that it owns main.

## 42 — Repository and namespace split

Proposal names: universalprimary, personatemplate, and per-person namespaces. These names and their access policies are not installed.

- **Universal primary:** reusable Flow tooling, launch/relay/checkup libraries and general conventions. Keep provider-specific and person-specific settings out of defaults. Pin Curriculum as authored skill input; regenerate harness projections.
- **Persona template:** an empty, documented layout and explicit configuration schema. Include examples with fictional data, not a copied person's Vision, Intent, transcripts or account state.
- **Per-person data:** Vision, Intent, raw vision, flow lanes and source-bearing reports. Preserve paths/hashes during migration and keep access classification explicit. Private, public and saleable are undecided classifications, not inferred from a directory name.
- **Existing component repositories:** Signal, Message, Persona, Cloud, Lojix and CriomOS stay in their own repositories. The split is not an excuse to copy their implementations into primary.
- **Unclassified remainder:** inspect before moving; source archives, designs and reports may mix reusable machinery with personal records.

Measured tracked source at shared Primary revision a983f169910c55a28c0318de29487a46ed814efd, read-only via git ls-tree; untracked files, worktree-only records, Git history and deployment state are excluded:

| Group | Files | Bytes |
|---|---:|---:|
| Intent | 9 | 3,769 |
| Vision | 25 | 53,688 |
| vision-raw | 90 | 117,142 |
| flows | 1,832 | 24,346,627 |
| reports | 710 | 11,136,489 |
| tools | 20 | 111,809 |
| Generated harness trees combined | 116 | 280,746 |
| Other, not yet classified | 1,153 | 167,422,200 |

Migration order: inventory/classify; agree owner/access policy; create destination proposal repositories; copy immutable snapshots with path/hash manifests; verify references and build inputs; review each consumer change; only then switch approved consumers. Preserve source repositories and published history. No move, deletion or redirect has occurred here.

Git service proposal: separate universal, template and person namespaces. GitHub mirroring is opt-in per repository after classification, not a blanket mirror of per-person data. Secondary owns service/accounts/credentials; Codex authors and tests source changes; Cloud manages approved provider operations. The specific forge organization names and domain remain configuration choices.

## 43 — Remembered web application map

Proposed record fields: application identity, origin and route scope, semantic revision, addressed elements/actions, stable semantic fingerprints, source observation, confidence and owner-approved status. A fingerprint covers the meaning required for the action, not CSS, color or unrelated layout.

Resolver proposal: longest validated origin/path match. Treat webapi: beside git: as a proposed access notation; no claim is made that it is legal Datom grammar. Do not resolve an attacker-controlled similar hostname as the same origin. Keep read actions distinct from account or provider mutations.

Each application map can live in its own Git repository with immutable revisions. A detected material change produces a Psyche review proposal containing old/new evidence and uncertainty. A fresh mapping becomes executable only after the applicable approval. Never let remembered page text grant authority to a tool.

Cloudflare is the first provider/map consumer. The existing read-only provider fixture is not browser automation. A self-teaching Luna job must be bounded to observed pages, use the existing authenticated browser surface without extracting credentials, and keep proposed mutations separate from replayable read-only observations. No web app map or browser job was activated here.

## 41 — Model-call record anatomy

Draft fields, not an adopted wire type:

- Call ID; Flow and session identity; parent call/turn identity; start/end times and terminal status.
- Input source references and hashes, roles/strata, exact model identifier and requested effort, provider/access mechanism and effective capability policy.
- Output reference/hash, tool-call/result references, usage/quota observations with their source and timestamp, and typed failures.
- Persona ownership and Sema/review hooks; reviewer identity and assessment are separate from the original result.
- Transcript relationship: source records remain the verbatim authority. A Context interpretation is a linked derived record and cannot replace the words.

Store credential handles or access-class labels, never credential values. Explicit text fields are justified by their function; retain large prompt/output bodies by referenced artifact rather than duplicating them in every thin event. A source hash proves bytes, not truth, delivery or approval. Retention and garbage collection need an explicit policy; this proposal authorizes no deletion or installation.
