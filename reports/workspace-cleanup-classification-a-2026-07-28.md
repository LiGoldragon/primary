# C1 workspace cleanup classification A — 2026-07-28

## Scope and safety boundary

Read-only classification of the 18 C1 paths from
`reports/recovery-map-2026-07-28.md`. No fetch, update, snapshot, claim,
conclusion, deletion, prune, commit, push, or beads mutation was performed.

The result is deliberately narrower than a deletion authorization. The recovery
map requires an owner disposition and a successful controlled Orchestrate
lifecycle witness before any conclusion or filesystem teardown. A result of
**likely cleanup-eligible after approval** means that the local evidence meets
the required history-and-material test; it does not waive those gates.

## Method and limits

- Used `jj --ignore-working-copy status`, `log`, `workspace list`, `bookmark
  list`, `diff --summary`, and `evolog`. Thus “clean” below means the recorded
  Jujutsu working-copy commit is clean and empty without asking Jujutsu to
  snapshot the filesystem. A tracked-file physical modification after the
  observation could not be ruled out without a forbidden snapshot.
- Compared each workspace's physical regular files (excluding `.jj` and
  `.git`) to `jj file list -r @`; all 18 had no extra untracked or ignored
  non-metadata files. Searched for `.beads`, `reports`, `agent-outputs`, and
  `.agents`; none existed in these paths.
- `orchestrate '(Observe Worktrees)'` contained none of the 18 C1 physical
  paths. It therefore supplied no active lane owner or lifecycle record.
- “Owner: Li (likely)” is evidence, not assignment: every non-empty parent was
  authored by `li <li@goldragon.criome.net>`. No explicit owner/disposition was
  found in the inspected local metadata.
- Remote state is last locally cached state only. No remote was contacted. A
  cached `main@git` difference is a remote-reconciliation uncertainty, not
  evidence against local ancestry.

## Classification summary

| Class | Count |
| --- | ---: |
| preserve | 0 |
| needs owner decision | 5 |
| likely cleanup-eligible after approval | 13 |
| unknown | 0 |

## Per-workspace evidence

All paths physically exist at the exact location in the first column. Every
current `@` listed below is a clean, empty Jujutsu working-copy commit. “No
extra material” covers untracked/ignored non-metadata files plus the named
report/bead/agent-artifact directories above.

| Physical path / JJ workspace | Canonical repository (default workspace) | Parent (`@-`) and local landing/successor evidence | Likely owner, material, remote uncertainty, retention value | Classification |
| --- | --- | --- | --- | --- |
| `/git/github.com/LiGoldragon/mentci-lib-cargo-migration` / `mentci-lib-cargo-migration` | `/git/github.com/LiGoldragon/mentci-lib` | `upvlwqyl 2ff5fd78`, “migrate to current Mentci contracts”; exactly local `main`. | Li; no extra material; cached `main@git` is one commit behind local main; workspace has no independent retention value once owner approves. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/mentci-lib-mentci-signal-family-migration` / `mentci-lib-mentci-signal-family-migration` | `/git/github.com/LiGoldragon/mentci-lib` | `ykqpvytw c30d50ab`, “remove stale AGENTS bootstrap guidance”; ancestor of local main `upvlwqyl`. Its only direct non-empty parent changed `AGENTS.md`; the named empty child carries no content. | Li; no extra material; cached `main@git` is one commit behind local main; no independent retained material found. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-criome-cargo-source-repair` / `meta-signal-criome-cargo-source-repair` | `/git/github.com/LiGoldragon/meta-signal-criome` | `kkuylnpy b9cda542`, “use main schema-rust source”; exactly local `main`. | Li; no extra material; cached `main@git` is two commits behind; only Cargo source-pin changes, already on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-criome-mentci-contract-migration` / `meta-signal-criome-mentci-contract-migration` | `/git/github.com/LiGoldragon/meta-signal-criome` | `nuuopvrp f569e149`, “migrate Schema 0.3 contract (GPT-5)”; not an ancestor of local main `kkuylnpy`. `evolog` shows its local evolution only, not a main successor. | Li; no extra material, but the committed contract migration itself is unique local evidence; cached `main@git` is two commits behind. | needs owner decision |
| `/git/github.com/LiGoldragon/meta-signal-mentci-cargo-source-repair` / `meta-signal-mentci-cargo-source-repair` | `/git/github.com/LiGoldragon/meta-signal-mentci` | `mvpmkqon 25d1a97f`, “use main schema-rust source”; exactly local `main`. | Li; no extra material; cached `main@git` is two commits behind; only Cargo source-pin changes, already on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-mentci-client-cargo-source-repair` / `meta-signal-mentci-client-cargo-source-repair` | `/git/github.com/LiGoldragon/meta-signal-mentci-client` | `nzwvwrqn f4a2d556`, “use main schema-rust source”; exactly local `main`. | Li; no extra material; cached `main@git` is two commits behind; only Cargo source-pin changes, already on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/meta-signal-mentci-client-mentci-signal-family-migration` / `meta-signal-mentci-client-mentci-signal-family-migration` | `/git/github.com/LiGoldragon/meta-signal-mentci-client` | `uxonpvms 5c492c58`, explicit Schema 0.3 contract migration; not an ancestor of local main `nzwvwrqn`. No local successor proof. | Li; no extra material, but the committed migration changes Cargo, generator, schema, Rust, and witness test surfaces; cached `main@git` is two commits behind. | needs owner decision |
| `/git/github.com/LiGoldragon/meta-signal-mentci-mentci-signal-family-migration` / `meta-signal-mentci-mentci-signal-family-migration` | `/git/github.com/LiGoldragon/meta-signal-mentci` | `nqxwnuns 9c2d5a9d`, explicit Schema 0.3 contract migration; not an ancestor of local main `mvpmkqon`. No local successor proof. | Li; no extra material, but the committed migration changes Cargo, generator, schema, Rust, and witness test surfaces; cached `main@git` is two commits behind. | needs owner decision |
| `/git/github.com/LiGoldragon/signal-criome-cargo-source-repair` / `signal-criome-cargo-source-repair` | `/git/github.com/LiGoldragon/signal-criome` | `uvlmvxml 71681d76`, “use main schema-rust source”; ancestor of current local main `lzynnpvp`. | Li; no extra material; cached `main@git` is five commits behind; only Cargo source-pin changes are retained on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-criome-mentci-contract-migration` / `signal-criome-mentci-contract-migration` | `/git/github.com/LiGoldragon/signal-criome` | `krtkvkxn 7a010ec7`, explicit Schema 0.3 contract migration; not an ancestor of local main `lzynnpvp`. No local successor proof. | Li; no extra material, but the committed migration changes Cargo, generator, schema, Rust, and tests; cached `main@git` is five commits behind. | needs owner decision |
| `/git/github.com/LiGoldragon/signal-mentci-cargo-source-repair` / `signal-mentci-cargo-source-repair` | `/git/github.com/LiGoldragon/signal-mentci` | `nxrsywmo 77540cfb`, “use main contract sources”; exactly local `main`. | Li; no extra material; cached `main@git` is two commits behind; only Cargo source changes, already on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-mentci-mentci-signal-family-migration` / `signal-mentci-mentci-signal-family-migration` | `/git/github.com/LiGoldragon/signal-mentci` | `wtvkonsy d1a3fa26`, explicit Schema 0.3 contract migration; not an ancestor of local main `nxrsywmo`. No local successor proof. | Li; no extra material, but the committed migration changes Cargo, generator, schema, Rust, and tests; cached `main@git` is two commits behind. | needs owner decision |
| `/git/github.com/LiGoldragon/signal-message-cargo-source-repair` / `signal-message-cargo-source-repair` | `/git/github.com/LiGoldragon/signal-message` | `mpnpkunn 95343930`, source repair; ancestor of current local main `rtqrkqxk`. | Li; no extra material; no cached remote `main` target was listed locally; committed repair is retained on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-persona-cargo-source-repair` / `signal-persona-cargo-source-repair` | `/git/github.com/LiGoldragon/signal-persona` | `tvxstnxl 04593c9a`, “converge on canonical TrueSchema generator”; ancestor of current local main `zyxpuswk`. | Li; no extra material; no cached remote `main` target was listed locally; only Cargo source-pin work, retained on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-router-cargo-source-repair` / `signal-router-cargo-source-repair` | `/git/github.com/LiGoldragon/signal-router` | `xoroszqq 56e11a3d`, runtime RegisterActor work; exactly local `main`. | Li; no extra material; no cached remote `main` target was listed locally; the entire substantive parent is on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/signal-terminal-dependency-cascade` / `signal-terminal-dependency-cascade` | `/git/github.com/LiGoldragon/signal-terminal` | `luuvltqu b6f9e481`, “migrate dotted Schema contract”; exactly local `main`. | Li; no extra material; cached `main@git` is one commit behind; substantive dependency cascade is on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/terminal-cell-dependency-cascade` / `terminal-cell-dependency-cascade` | `/git/github.com/LiGoldragon/terminal-cell` | `pyvlvwps dcac484f`, “consume current terminal contract”; ancestor of current local main `ovmzqlwy`. | Li; no extra material; no cached remote `main` target was listed locally; substantive dependency work is retained on main. | likely cleanup-eligible after approval |
| `/git/github.com/LiGoldragon/schema-structural-pipe-retirement` / `schema-structural-pipe-retirement` | `/git/github.com/LiGoldragon/schema` | `tqlwvqvw 6d7afa84`, “retire structural pipe syntax”; ancestor of current local main `vzuwpmqt`. | Li; no extra material; no cached remote `main` target was listed locally; substantial retirement is retained on main. | likely cleanup-eligible after approval |

## Safest three candidates, still not deletion targets

1. `meta-signal-criome-cargo-source-repair`: empty clean child; its two-file
   Cargo source repair (`kkuylnpy b9cda542`) is exactly local `main`; no unique
   filesystem material.
2. `meta-signal-mentci-cargo-source-repair`: the same proof shape—empty clean
   child, two-file Cargo repair `mvpmkqon 25d1a97f` exactly local `main`, no
   unique material.
3. `meta-signal-mentci-client-cargo-source-repair`: empty clean child, two-file
   Cargo repair `nzwvwrqn f4a2d556` exactly local `main`, no unique material.

All three still require Li's disposition, the recovery map's P1–P5 conflict
review, and the authorized O4/C3 lifecycle path. Their cached `main@git`
tracking ref is two commits behind local main, and no fetch was allowed.

## Required next decision

Ask Li to retain, land, or deliberately retire the five non-main Schema 0.3
migration commits. For the remaining 13, an approval may authorize a later,
recoverable Orchestrate conclusion only after the controlled lifecycle witness;
this classification itself authorizes no state change.
