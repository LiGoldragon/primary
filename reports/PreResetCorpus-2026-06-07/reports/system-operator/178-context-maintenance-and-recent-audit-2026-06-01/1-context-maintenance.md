# Context Maintenance Subreport

System-operator subagent report, 2026-06-01.

## Scope

I reviewed the system-operator report surface, recent Spirit records, and the
recent topics named by the dispatcher:

- DJI Mic keepalive and profile churn
- browser-use / main Chrome session control
- Spirit qualitative depth queries
- Home deployment and the Rust analyzer collision

I used the context-maintenance vocabulary: Forward, Migrate, Keep, Drop.

## Recent Intent Spine

The load-bearing recent intent is:

- Spirit records 1315, 1316, 1317: Spirit topic retrieval should support
  partial/full multi-topic matching and qualitative recency depths, with recent
  intent favored by default and quiet topics reaching farther back.
- Spirit record 1338: the settled production vocabulary is Shallow, Recent,
  Deep, VeryDeep with target counts 5, 15, 30, 100.
- Spirit records 1340 and 1341: positive grep checks are not proof of live
  behavior; proof should compile, execute, round-trip, or exercise the runtime
  path.
- Spirit records 1352, 1353, 1354: operator integration stays on main; designer
  prototype work happens one proof at a time in worktrees rebased on main; after
  implementation/prototype subagent work, run context maintenance and fresh-
  intent audit before deciding immediate fixes.

## Report Disposition

### Spirit qualitative depth

Keep:

- `reports/system-operator/177-spirit-topic-depth-query-implementation-2026-06-01.md`

Reason: this is the current honest production landing report. It records what
was already present, what was newly implemented, what was deployed, and what is
not implemented. It also absorbs the relevant implementation guidance from
`reports/system-designer/56-spirit-verbal-depth-scopes-and-frequency-adaptive-search-2026-06-01.md`.

Migrate already done:

- `skills/spirit-cli.md` now documents the live syntax for `Partial`, `Full`,
  certainty filters, `Shallow`, `Recent`, `Deep`, and `VeryDeep`.

Forward:

- The larger Nexus / weighted scoring / topic-density-statistics idea remains a
  future design topic. It should not be represented as implemented in the
  current production Spirit report.

Immediate cleanup recommendation:

- No code cleanup from this report alone. The feature appears well-behaved:
  signal tests passed, daemon tests passed, production deployment was verified
  with live CLI queries.

### DJI Mic keepalive

Forward:

- `reports/system-operator/175-dji-mic-keepalive-profile-churn-and-deploy-fix-2026-06-01.md`
- `reports/system-operator/176-dji-mic-keepalive-alternative-solutions-research-2026-06-01.md`

Reason: report 175 is the current deployed fix; report 176 is the current
research layer. Together they supersede the older event report but do not yet
settle the whole runtime behavior because the user reported recurring failure
again before it later started working.

Drop candidate after absorption:

- `reports/system-operator/166-dji-mic-profile-churn-fix-2026-05-28.md`

Reason: report 166 described the earlier profile-reassertion approach, including
manual `ConnectProfile` and steady-state profile repair. Report 175 explicitly
reversed the bad `ConnectProfile` pattern and explains the newer model. Keep 166
only until report 175 or a CriomOS-home runbook explicitly says the old
`ConnectProfile` profile-hammering path is retired.

Migrate candidate:

- CriomOS-home should carry a concise permanent note in its repo docs or module
  comments that DJI Mic keepalive must not call BlueZ `ConnectProfile` in the
  steady-state keepalive path. The current Nix check protects that in code, but
  the intent also belongs near the module.

Immediate cleanup recommendation:

- If the problem returns, implement report 176's first concrete follow-up:
  a DJI-specific WirePlumber rule for `session.suspend-timeout-seconds = 0`
  and possibly `node.pause-on-idle = false`, while keeping the current loopback
  unless testing proves it unnecessary.

### Browser-use / main Chrome session

Keep:

- `reports/system-operator/174-browser-use-main-chrome-session-research-2026-05-31.md`

Reason: this is still the current browser automation state. It captures the
important distinction between browser-use profile-copy mode and Playwright
Extension control of the actual main Chrome tab/session.

Forward:

- The next implementation should likely prototype Playwright Extension mode, not
  keep pushing browser-use as if it can attach to the existing default Chrome
  profile through external CDP. Chrome 136 blocks that default-profile CDP path.

Migrate candidate:

- If browser automation becomes a recurring system-operator surface, the
  profile-copy versus extension-control distinction belongs in a browser
  automation skill or CriomOS-home browser tooling docs.

Immediate cleanup recommendation:

- Treat `/tmp/browser-use-user-data-dir-*` directories as sensitive copied
  browser profile data during cleanup. Do not blindly delete from a subagent
  report, but main operator should check whether stale copies exist and remove
  them intentionally.

### Home deployment and Rust analyzer collision

Forward:

- The deployment collision is documented inside
  `reports/system-operator/177-spirit-topic-depth-query-implementation-2026-06-01.md`
  rather than as a standalone report.

Reason: it was a deployment blocker found while shipping Spirit, not a separate
architecture topic. The actual fix landed in CriomOS-home by using the canonical
Rust toolchain's `rust-analyzer` instead of adding a second standalone
`pkgs.rust-analyzer`.

Migrate candidate:

- If this pattern recurs, `skills/nix-discipline.md` or CriomOS-home `skills.md`
  should say that a language-server binary bundled by the canonical language
  toolchain must not also be installed standalone in editor packages.

Immediate cleanup recommendation:

- No immediate cleanup unless a fresh Home profile check shows another duplicate
  package collision. The deployment succeeded after the fix.

### Context-maintenance directories

Drop candidate:

- `reports/system-operator/178-context-maintenance-and-recent-audit-2026-06-01/`

Reason: it is a parallel meta-report directory with only `0-frame-and-method.md`
at the time of this pass. The dispatcher-assigned path for the active current
session is `reports/system-operator/178-context-maintenance-and-recent-work-audit-2026-06-01/`.
Keeping two similarly named `178-*` directories creates report-index ambiguity.
Do not delete from this subagent; main operator should decide after checking
whether another subagent is still writing there.

Keep:

- `reports/system-operator/178-context-maintenance-and-recent-work-audit-2026-06-01/`

Reason: this is the active meta-report directory for the current request. This
file is subreport 1. Subreport 2 is expected to carry the fresh-intent/recent
work audit.

### Older system-operator roots

Keep:

- `reports/system-operator/1-whisrs-durable-first-stt-research-2026-05-17.md`
- `reports/system-operator/2-persona-speech-component-brainstorm-2026-05-17.md`
- `reports/system-operator/139-arca-daemon-content-addressed-store-architecture-2026-05-17.md`
- `reports/system-operator/167-horizon-pure-schema-concept-prototype-2026-05-28.md`
- `reports/system-operator/173-deep-context-maintenance-2026-05-30.md`

Reason: report 173 already kept these as root topic artifacts. Today's work did
not supersede the Whisrs durable-first model, Persona transcription boundary,
Arca architecture, or Horizon schema concept proof. They are old but still
load-bearing until migrated into the relevant repo docs.

Drop candidates already named by report 173:

- `reports/system-operator/169-context-maintenance-2026-05-28/`

Reason: report 173 says it supersedes the 169 maintenance directory. I found no
files under 169 in this pass, so this is likely already empty or inert. Main
operator can remove the empty directory if present.

## Skill And Documentation Recommendations

Immediate:

- Add no new Spirit syntax docs; `skills/spirit-cli.md` is current for the
  deployed query surface.
- Consider a short CriomOS-home doc or module comment for the DJI rule:
  keepalive must not use BlueZ `ConnectProfile` as a steady-state repair path.
- Consider a short Nix/Home discipline note if duplicate toolchain binaries
  recur: editors should reference the canonical language toolchain binary rather
  than installing a second copy.

Deferred:

- Browser automation deserves its own durable skill only after the Playwright
  Extension path is prototyped. Today there is still too much tool-specific
  uncertainty to freeze as a general rule.
- Spirit's Nexus / weighted scoring search belongs in the next Spirit design
  wave, not in production `skills/spirit-cli.md` as though it exists.

## Top Findings

1. The Spirit qualitative-depth work is documented and live enough to Keep; the
   next Spirit search layer is design work, not cleanup of this deployment.
2. The DJI reports need consolidation soon: report 175 and 176 are current;
   report 166 is a Drop candidate once its useful "old path retired" lesson is
   moved into CriomOS-home docs or the module.
3. There are two `178-*` context-maintenance directories. The active one is
   `reports/system-operator/178-context-maintenance-and-recent-work-audit-2026-06-01/`;
   the sibling `reports/system-operator/178-context-maintenance-and-recent-audit-2026-06-01/`
   should be dropped if no other live subagent owns it.
