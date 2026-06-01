# Synthesis and immediate actions

## Subagent run outcome

Two async subagent runs were attempted.

- Run `76b8209f-090b-4444-86dc-a0fac018aa28` (context-builder + reviewer) was interrupted and abandoned. The reviewer failed because the harness injected missing `plan.md` / `progress.md` reads; the context-builder produced no useful report before interruption.
- Run `6327a9d1-7147-4ee9-80ad-f290b5e704ef` (delegate + delegate) also had lifecycle trouble, but it produced useful reports before the run paused/failed. Those outputs were recovered and copied into this canonical directory:
  - `1-context-maintenance.md`
  - `2-recent-audit.md`

The duplicate sibling directory `reports/system-operator/178-context-maintenance-and-recent-work-audit-2026-06-01/` was removed after its useful reports were copied here.

## Immediate actions taken

1. **Consolidated the meta-report directory.** The canonical report session is now `reports/system-operator/178-context-maintenance-and-recent-audit-2026-06-01/` with frame, context-maintenance, audit, and synthesis files.

2. **Cleaned sensitive browser-use profile copies.** Removed 18 stale `/tmp/browser-use-user-data-dir-*` directories after verifying no remaining process was using those paths. These directories are treated as sensitive because browser-use copied Chrome profile data into them during the main-profile-copy tests.

3. **Migrated the DJI keepalive boundary and retired the old report.**
   The useful lesson from `reports/system-operator/166-dji-mic-profile-churn-fix-2026-05-28.md`
   landed in CriomOS-home, then report 166 was deleted. The permanent
   rule now lives in `/git/github.com/LiGoldragon/CriomOS-home/skills.md`
   and beside the keepalive module in
   `/git/github.com/LiGoldragon/CriomOS-home/modules/home/profiles/min/dictation.nix`:
   after PipeWire exposes the Bluetooth card, repair DJI profile churn through
   PipeWire profile reassertion, not BlueZ profile-specific connection calls.
   CriomOS-home commit `092214bd` (`home: document DJI keepalive profile repair
   boundary`) was pushed. `nix fmt -- --check modules/home/profiles/min/dictation.nix
   skills.md` and `nix build .#checks.x86_64-linux.dji-keepalive --no-link
   --print-build-logs` passed.

4. **Tracked the Spirit-next production-copy acceptance gate.** Created bead
   `primary-jew3` (Spirit-next production-copy handover acceptance test). The
   bead carries record 1325's acceptance shape: exercise a candidate runtime
   against a copied production-like SEMA database, prove existing records remain
   readable, write only to the copy, and leave the original unchanged.

5. **Left unrelated dirty files untouched.** `jj status` shows many modified/added files under designer, system-designer, operator, and shared skills surfaces. They are outside this system-operator browser/context-maintenance thread and were not edited here.

## Findings accepted for immediate decision

### Browser automation

`reports/system-operator/174-browser-use-main-chrome-session-research-2026-05-31.md` is the current browser automation report and should stay. Its important current conclusion is narrow: browser-use can copy main Chrome profile data into a temporary controlled profile, but the visible headed test was unreliable because the foreground page remained `about:blank` while browser-use operated another target. For supervised real-account work, the next promising path is the installed Playwright Extension (`mmlmfjhmonkocbjadbfplnigmagldckm`) via Playwright MCP/CLI extension mode.

No wrapper/package should be landed immediately from this state. The next Playwright Extension step is new prototype/design work: prove visible selected-tab control first, then decide whether packaging belongs in CriomOS-home on main.

### Spirit qualitative-depth audit

The subagent audit found the recent Spirit qualitative-depth work implemented, deployed, and live. The one substantial deferred acceptance gap is a production-copy handover test before the next Spirit production-candidate cutover. That is not part of this browser-use cleanup and should be tracked by the Spirit/operator thread, not fixed in this system-operator pass.

That follow-up is now bead `primary-jew3`.

### DJI Mic reports

The current deployed DJI Mic fix/report pair is report 175 plus report 176.
Report 166 is now retired because the durable lesson landed near the
CriomOS-home module and in the repo skill: steady-state keepalive must not use
BlueZ profile-specific connection calls as a profile-hammering repair path.
No live runtime behavior changed in this pass; the CriomOS-home change is
documentation plus a module-side guard comment.

## Deferred work

- Prototype Playwright Extension control of the existing main Chrome tab under supervision. Because this is new design/prototype work, follow the fresh intent: use a designer/system-designer worktree rebased on main, one proof at a time.
- After the Playwright Extension proof, decide whether a durable operator-main package/wrapper belongs in CriomOS-home.
- Add Spirit production-copy handover acceptance testing before the next Spirit production-candidate cutover: tracked as bead `primary-jew3`.
- Migrate the browser-use profile-copy versus extension-control distinction into a durable browser automation skill or CriomOS-home doc only after the Playwright Extension path is proven.
