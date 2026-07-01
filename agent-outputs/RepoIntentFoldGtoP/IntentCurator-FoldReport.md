# Intent Curator — INTENT.md Fold Report (G–P slice)

## Task and scope

Per-repo doctrine coverage gap: fold each missed repo's `INTENT.md` into
`ARCHITECTURE.md §0.5`, then remove `INTENT.md`. Slice covers repos whose
names begin G–P (case-insensitive). Source: `agent-outputs/RepoManifestDiscovery/Scout-MissedRepos.md`.
Repos live under `/git/github.com/LiGoldragon/<name>`.

Excluded per brief: `CriomOS-test-cluster`, `signal-standard`, `AnaSeahawk-website`,
`persona-pi`, `WebPublish`.

One-off task: integrate archived Spirit record `y1v5` into `horizon-rs/ARCHITECTURE.md`.

## Method

1. Read INTENT.md + ARCHITECTURE.md for each repo.
2. Synthesized `## 0.5 · Direction` section from psyche-stated direction in INTENT.md.
   — Contract repos: authority-split rationale, key psyche decisions (Spirit citations), non-ownership.
   — Daemon/library repos: mission, production goals, cited decisions.
3. Inserted §0.5 before the first numbered section of each ARCHITECTURE.md.
4. Deleted INTENT.md.
5. Committed and pushed each repo via jj.

For horizon-rs: added VM tech spec from y1v5 record (real display/GPU/DRM-capable VM,
chroma first target, Nix-native + CI-automatable + interactively viewable, systemd sandboxes
on Prometheus) into the existing "VM hosting is cluster-data-generated" section.
No secret values touched (y1v5 is priv=Zero, no redaction needed).

## Results per repo

| Repo | §0.5 folded | INTENT.md removed | Pushed | Notes |
|---|---|---|---|---|
| lojix | yes | yes | yes | §0.5 captures mission + cutover bar; §7 retained for detailed direction bullets |
| mentci | yes | yes | yes | §0.5 captures approval-organ purpose + daemon rationale + prompt-to-work direction |
| meta-signal-agent | yes | yes | yes | §0.5 captures authority split + provider model decision (Spirit f8k7, iucr) |
| meta-signal-cloud | yes | yes | yes | §0.5 captures mutation/read split + PreparePlan rationale |
| meta-signal-domain-criome | yes | yes | yes | §0.5 captures registry authority + provider separation |
| meta-signal-lojix | yes | yes | yes | §0.5 captures owner-only isolation + Spirit ssk2/vudl |
| meta-signal-mentci | yes | yes | yes | §0.5 captures single-Configure purpose + binary startup constraint |
| meta-signal-mentci-client | yes | yes | yes | §0.5 captures policy/authority rationale + RemoteControlMode relocation |
| meta-signal-mind | yes | yes | yes | §0.5 captures PersonaSpirit-owns-PersonaMind + deliberate small surface |
| meta-signal-mirror | yes | yes | yes | §0.5 captures meta-vs-working split + deferred enforcement/attestation |
| meta-signal-orchestrate | yes | yes | yes | §0.5 captures code-enforced authority split + partial-failure semantics |
| meta-signal-persona | yes | yes | yes | §0.5 captures meta-policy side + infrastructure-minted identity |
| meta-signal-repository-ledger | yes | yes | yes | §0.5 captures three-layer model rationale |
| meta-signal-router | yes | yes | yes | §0.5 captures orchestrate-as-caller authority graph |
| meta-signal-spirit | yes | yes | yes | §0.5 captures owner-only operations + Sema-as-daemon-projection constraint |
| meta-signal-terminal | yes | yes | yes | §0.5 captures privilege rationale + meta chain |
| meta-signal-version-handover | yes | yes | yes | §0.5 captures Persona-consumes + AttemptHandover-as-normal-path |
| mirror | yes | yes | yes | §0.5 captures Spirit 0yx5/rj9y/29pb/x0ja decisions + deferred enforcement |
| nota-config | yes | yes | yes | §0.5 captures one-argument workspace rule + library-only boundary |

## One-off: y1v5 / horizon-rs

| Item | Result |
|---|---|
| Record | y1v5, Decision, cert=Medium, imp=Minimum, priv=Zero |
| Description | VM-based testing node feature using real display/GPU/DRM-capable VM; chroma first target; Nix-native + CI-automatable + interactively viewable; systemd sandboxes on Prometheus |
| Integrated into | `horizon-rs/ARCHITECTURE.md` §"VM hosting is cluster-data-generated" |
| Redaction needed | No (priv=Zero, no secret-adjacent material) |
| Pushed | yes |

## Skipped / excluded (per brief)

- `persona-pi` (P) — explicitly excluded
- `CriomOS-test-cluster` — excluded AND no ARCHITECTURE.md target
- `signal-standard` — excluded AND no ARCHITECTURE.md target
- `AnaSeahawk-website`, `WebPublish` — excluded

## Anomalies

None. All 19 repos had both INTENT.md and ARCHITECTURE.md present, all jj repos had
clean working copies on top of main, all commits and pushes succeeded.
