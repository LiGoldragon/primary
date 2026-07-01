# Lojix nonlegacy holistic audit

## Review
- Correct: `lojix-run` is deleted from the approved CriomOS-home live package/check surfaces. `/git/github.com/LiGoldragon/CriomOS-home/packages/lojix-run` and `/git/github.com/LiGoldragon/CriomOS-home/checks/lojix-run` are absent, and live scoped `rg` found no `lojix-run` matches in CriomOS-home outside excluded archives/reports.
- Correct: the three core repos in the implementation report are clean for the named legacy vocabulary outside locks/targets: `signal-lojix`, `meta-signal-lojix`, and `lojix` had no live matches for `lojix-run`, `FullOs`, `OsOnly`, `HomeOnly`, `Deployed`, `AcceptedDeploy`, `DeploymentKind`, `HomeMode`, `SystemAction`, or `lojix-cli` when excluding `target`, `Cargo.lock`, and lock files.
- Correct: the new core schema surfaces use the accepted names: `meta-signal-lojix/schema/lib.schema:65` uses `DeployAccepted DeployHandle`; `meta-signal-lojix/schema/lib.schema:90` defines `SourceRevisionPolicy [RequireImmutable ResolveAndRecord]`; `meta-signal-lojix/schema/lib.schema:103-126` makes policy a required deploy field.
- Correct: no hidden local-jj exactification, niri/pi side effect, or replacement `lojix-run` wrapper was found in the core Lojix runtime. `lojix/src/schema_runtime.rs` routes `ByEventLog` to `ReadEventLog` at lines 1599-1600, maps it to `DeploymentEventsQueried` at lines 1843-1847, rejects mutable refs under `RequireImmutable` at lines 1809-1826, and replaces the pipeline flake with the resolved ref for `ResolveAndRecord` at lines 2364-2369. CriomOS-home docs make Niri reload explicit operator procedure, not deploy tooling, at `/git/github.com/LiGoldragon/CriomOS-home/skills.md:224-231`.
- Correct: deferred repo rename is captured. `bd show primary-4wvl` reports `primary-4wvl · Rename CriomOS-home to CriomOS-user [P2 · OPEN]`, and `/home/li/primary/criomos-user-rename-bead.md:3-5` records the same bead and open status.
- Blocker: public live deploy test surface still uses the removed legacy contract. `/git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:38`, `:455-476`, `:501-533`, and `:546-549` still submit `(Deploy (System (... FullOs ... Boot ...)))`, assert `Deployed`, mention `AcceptedDeploy`, and assert `FullOs Boot Current`. This is a real live test generator, not an archive/lock/generated-only occurrence.
- Blocker: current operator/docs examples use the new heads but omit required `SourceRevisionPolicy`, so they no longer match the schema. The schema requires `source_revision_policy` before `builder` in `meta-signal-lojix/schema/lib.schema:103-124`, but examples omit it in `/git/github.com/LiGoldragon/CriomOS/README.md:26-28`, `/git/github.com/LiGoldragon/CriomOS/docs/GUIDELINES.md:270-271`, `/git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md:24-36`, `/home/li/primary/.agents/skills/operating-system-operations/SKILL.md:29-41`, and `/home/li/primary/.claude/skills/operating-system-operations/SKILL.md:29-41`.
- Blocker: broad public live search still finds `lojix-cli` as current deploy-stack/deploy-path guidance outside archival reports: `/git/github.com/LiGoldragon/CriomOS/devshell.nix:20`, `/git/github.com/LiGoldragon/CriomOS/AGENTS.md:9`, `/git/github.com/LiGoldragon/forge/README.md:7-12`, `/git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md:3-5`, `/git/github.com/LiGoldragon/signal-forge/src/lib.rs:19-20`, `/git/github.com/LiGoldragon/criome/ARCHITECTURE.md:459-501`, and `/git/github.com/LiGoldragon/persona/ARCHITECTURE.md:96-98,1464-1465`. Some are docs rather than runtime code, but they are live current files, not archives/locks.
- Note: `/git/github.com/LiGoldragon/signal-criome/tests/round_trip.rs:110-112` still uses authorization scope `deploy:zeus:FullOs`. This is not an obvious Lojix runtime contract file, but it is a live public test containing a removed artifact name.
- Note: archival/generated-only occurrences remain in places such as `CriomOS/reports/**` and `skills/skills/archive/**`; those were excluded from blocker classification. The generated `.agents`/`.claude` operating-system skill files are not archival; they are live generated surfaces and share the missing-policy blocker above.
- Note: `/home/li/primary/plan.md` was requested but does not exist. I read `/home/li/primary/progress.md`, the redesign plan, and both implementation output reports instead.

Pass/fail: FAIL. Core Lojix schema/runtime and `lojix-run` deletion are mostly clean, but closeout is blocked by live public legacy deploy test/docs and malformed current examples.

Closeout recommendation: do not commit/push/deploy as complete. Fix the live `CriomOS-test-cluster` deploy test to the `Host CompleteHost`/`DeployAccepted DeployHandle`/new action/policy shape, update all current deploy examples to include `RequireImmutable` or `ResolveAndRecord`, remove or rewrite live `lojix-cli` guidance, then rerun the broad public grep and targeted cargo/nix validation.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Concrete findings include blockers at /git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:472, /git/github.com/LiGoldragon/CriomOS/README.md:26-28, /git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md:24-36, and live lojix-cli references such as /git/github.com/LiGoldragon/CriomOS/devshell.nix:20."
    }
  ],
  "changedFiles": [
    "/home/li/primary/lojix-nonlegacy-holistic-audit.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "read /home/li/primary/progress.md, implementation reports, and redesign plan",
      "result": "passed",
      "summary": "plan.md was absent; progress and available implementation/redesign reports were read."
    },
    {
      "command": "rg legacy vocabulary in approved repos excluding target/locks/reports/archive",
      "result": "failed",
      "summary": "Core repos were clean; public live search still found CriomOS-test-cluster legacy deploy test terms and live lojix-cli docs."
    },
    {
      "command": "test -e checks/packages lojix-run paths and rg lojix-run in CriomOS-home live files",
      "result": "passed",
      "summary": "lojix-run package/check directories are absent and no live CriomOS-home lojix-run matches were found."
    },
    {
      "command": "jj status --no-pager in signal-lojix, meta-signal-lojix, lojix, CriomOS-home, CriomOS, skills, and primary",
      "result": "passed",
      "summary": "Read-only status inspection; no commit/push/stage performed."
    },
    {
      "command": "bd show primary-4wvl",
      "result": "passed",
      "summary": "Bead primary-4wvl is open and titled Rename CriomOS-home to CriomOS-user."
    }
  ],
  "validationOutput": [
    "Core signal-lojix/meta-signal-lojix/lojix grep: no old vocabulary matches outside excluded locks/targets.",
    "Broad public live grep: remaining real live matches include CriomOS-test-cluster legacy deploy test, live lojix-cli docs/devshell references, and signal-criome test scope deploy:zeus:FullOs.",
    "Docs/examples mismatch: schema requires SourceRevisionPolicy; current meta-lojix examples omit it."
  ],
  "residualRisks": [
    "Real Nix/network/daemon tests were not run in this read-only audit.",
    "Broad public docs outside the approved implementation slice still teach or reference lojix-cli; some may be stale docs rather than runnable code but are not archival paths."
  ],
  "noStagedFiles": true,
  "diffSummary": "Audit report only; no code edits, commits, pushes, deploys, or private-repos inspection.",
  "reviewFindings": [
    "blocker: /git/github.com/LiGoldragon/CriomOS-test-cluster/lib/mkDeployTest.nix:472 - live deploy test still submits legacy System/FullOs and asserts Deployed/AcceptedDeploy-era output/state.",
    "blocker: /git/github.com/LiGoldragon/CriomOS/README.md:26-28 and /git/github.com/LiGoldragon/skills/modules/operating-system-operations/full.md:24-36 - current examples omit required SourceRevisionPolicy field.",
    "blocker: live public docs/devshell still reference lojix-cli, e.g. /git/github.com/LiGoldragon/CriomOS/devshell.nix:20 and /git/github.com/LiGoldragon/horizon-rs/ARCHITECTURE.md:3-5.",
    "note: no live lojix-run package/check remains in CriomOS-home.",
    "note: deferred CriomOS-home to CriomOS-user rename is tracked by bead primary-4wvl."
  ],
  "manualNotes": "Read-only audit; private-repos was not inspected. Completion should remain blocked until live public legacy references and malformed examples are fixed."
}
```
