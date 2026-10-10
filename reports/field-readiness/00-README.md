# Field Readiness Pass — Lane Index (2026-07-02)

Phase 1-2 probe of the persona/criome engine's readiness for a sustained
Fable 5 integration-testing session, especially VM-cluster operation on
prometheus. Four Fable 5 recon workers probed the field in parallel; a
synthesis worker merged their kink ledgers, opened tracker beads for every
non-trivial kink, and recorded the open psyche decisions. Parent audit:
`reports/persona-system-audit/` (read its 00-README for framing).

One-line verdict: READY-WITH-KINKS — VM host, builds, minimal runnable whole,
and tooling all witnessed working, but the whole-engine gate is dead on a
stale fenix pin, wire-vintage skew fails silently, and no continuous-testing
entry point exists. (Single-host concentration on prometheus is accepted by
design, not a kink.)

Read order:

1. `02-kink-ledger.md` — ranked merged kink ledger, bead ids, cheap-fix list,
   open decisions for the psyche, NotBuiltYet appendix pointer. Start here.
2. `10-vm-cluster-probe.md` — prometheus VM infrastructure witnessed GREEN
   end-to-end; declared persistent guest network-dark.
3. `11-build-readiness.md` — every core component builds warm; whole-engine
   gate un-instantiable (fenix FOD); single-host build field.
4. `12-run-and-assembly.md` — minimal runnable whole exchanges real mail
   after rebuild; stale-binary wire skew; 22-entry NotBuiltYet stub surface.
5. `13-tooling-field.md` — jj/nix/spirit/orchestrate/bd/tests all READY;
   known jam points; no continuous-testing entry point.

Tracker: beads under label `field-readiness`. Current state is the
`02-kink-ledger.md` 2026-07-03 CLOSEOUT STATUS DELTA — read it for what is now
true. Headline since the recon: the whole-engine gate's fenix death is fixed
(`primary-j5j2` closed) and the wire skew is resolved at signal-frame 0.3.0; the
gate's sole remaining blocker is the `nota-next`→`nota` crate-rename migration
(`primary-ekvt`, P1), on which `primary-w46v` now depends. `primary-oeng`
retired (single-host concentration accepted). `primary-wgae`/`primary-oftl`/
`primary-ekvt` filed this session.
