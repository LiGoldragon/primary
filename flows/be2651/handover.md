# Handover: Lojix onto its Ethos (bead primary-kc4e), from Mind curriculum Opus be2651

The living wants implementation done by Codex (Psyche core Opus ktzu). This file hands the Lojix line over whole. Nothing is half-written: every commit below is pushed, and the builder's copy matches the last commit.

## Where it stands

All work is on the branch `ethos28-be2651` of each repository. Nothing is merged to main, released or deployed. The live Lojix is still 0.10.6 on ouranos and zeus.

| repository | branch head | notes |
|---|---|---|
| lojix | **ab92ed6** (0.11.0) | the steps below, one commit each |
| signal-lojix | 17c23e2 (0.12.0) | wire break: positional pairing, split Query, `Refused.StoreFailure`; ethos-zero 29 |
| meta-signal-lojix | 7fe43b8 (0.13.0) | ethos-zero 29 |
| horizon-rs (horizon-lib 0.18.0) | 182f530 | ethos-zero **28** on purpose (Fable: stays on 28 until the Memory upgrade form; see "Held"); Ondyfaind respelled Undefined (Fable 6grp) |
| ethos-zero | main f23eacf (29.0.0) | landed |
| datom-codec | eb79226 (0.32.3) | the contracts and lojix pin it |

Lojix commits in order, each gated green on prometheus unless said:
316422f (dead types out), 4b2c50f and 26caf36 (contracts repinned, ingress on 29), bde7b0e (106 twins out), 7f218c1 (memory.ethos; deploy-job upgrade; quarantine retired), 70ff5fe and 23f88f2 (rulings; Answering through the generated dispatch, adapters.rs gone), 9ab9eeb (operation.ethos), af38505 and 5c2cff8 (emission.ethos, 29 emissions; shutdown fix), 10241fb (stages as attempts; systemd enums), 38a57f1 (6llk: retained self-switch unit, terminal from its result), 73dfcf3 (6llk: LoaderInfo capability read, clears skipped where unsupported), 2d4330e (materialization writes and the profile read as emissions), a83218c (bead primary-bg32: user activation with explicit XDG_RUNTIME_DIR), 8701216 (6llk remote half: Current recorded, Failed with the clear's evidence), f50602c (legacy startup archive retired; offline tools' tests in the gate; its gate failed same-host-test-activation, fixed by af392ec), af392ec, **ab92ed6** (lojix-bootstrap on its Ethos: generated ingress with no twin, journal records in ethos/bootstrap_journal.ethos, emissions in ethos/bootstrap_emission.ethos).

The gate logs for the last four commits show no failed attribute: /tmp/claude-1001/-home-li-primary/be26511c-e6c3-597a-9e57-a86a1ac3a1e0/scratchpad/se11/gate-*.log. **Re-gate ab92ed6 before you build on it.** Its log ends without the summary line, and the worker was stopped while it was rewriting the bootstrap tests.

The reports, in order, are in /home/li/primary/flows/be2651/reports/:
- lojix-survey.md and lojix-questions.md;
- lojix-steps-1-4.md, -5.md, -6-7.md, -r-8.md, -9-10.md, -a-b.md and -b2-c-d.md.

Each report gives the proofs, and the A/B harness and the live-store copy procedure: copy as root, check the sha256, never touch the running service, and discard a copy that holds an in-flight deploy.

## What remains, in order

1. **Finish step 11, the offline tools.** These are already done: write-configuration and migrate-configuration are retired, reset-store takes no input, and bootstrap is on its Ethos. Left to do:
   - confirm the bootstrap tests;
   - check whether a bootstrap journal is live. `handover-evidence/journals-ouranos-decoded.txt` lists the journals on ouranos, all terminal; zeus is not checked;
   - fix the two `nexus_configuration` tools tests, which have failed at every base since 316422f, or say why not.
2. **Hand-written types left.** Re-check `handover-evidence/hand-types.txt`, the list as it stood at the stop. Each entry should be a runtime holder (actor, socket, store handle, error), not data. Any data type there goes into an Ethos.
3. **Rerun the ethos-in-runtime audit for Lojix.** The audit is `/home/li/primary/flows/00e2a8/audits/ethos-in-runtime.txt`, and the definition of yes is in bead primary-kc4e. It needs yes.
4. **Release.**
   1. Merge the branches to main in dependency order: datom-codec if needed, horizon-rs, signal-lojix, meta-signal-lojix, lojix. Keep the pinned branch commits reachable.
   2. Bump CriomOS's lojix lock. CriomOS must change in the same change:
      - `lojix.nix:45` and `:267`;
      - `checks/lojix-nexus-service`;
      - the reset service and its check, since `lojix-reset-store` now takes no argument;
      - `harness-update.nix:106`, which matches `Watching.*`; the output is now `DeploymentsWatched`;
      - `docs/GUIDELINES.md:277`.
   3. The live CriomOS main was 00f90ad at the last note.
   4. Deploy through Lojix on ouranos, then zeus. Before each switch, take a copy of the lojix store: after 0.11.0 opens it, 0.10.6 refuses it, so that copy is the rollback.
   5. Ask for the ouranos slot first. Mind flowNexus Opus and Field core Sol both use it, and Field core Sol asked (0jtc) to be told before any ouranos transition.
5. **Done.** Send Done to Psyche core Opus for its Orders k5zh and yjj2, and Done on beads primary-6llk and primary-bg32, when Lojix is live.

## Held, not in this release

- **horizon-lib's one-variant enums.** These are MotherBoard, DomainProvider, SiteRenderer and PersonaCapability, and also CompositionCommand. Fable ruled them reshaped away, but only with the Memory upgrade form, since the reshape changes stored bytes. Until then horizon-lib stays on ethos-zero 28 and is not touched.
- **HOME and USER into configuration.** This is bead primary-rq3j, right after the release.
- **The deployment watch stream** stays hand-written until a serving library exists (Fable C).

## Rulings in force

The rulings in force are in lojix-questions.md, with Fable's later answers recorded in the reports:
- A: emit runs on a blocking thread;
- B: horizon-lib's type is stored wrapped and pinned;
- C: the watch stream stays as it is;
- 1uvt: `Refused.StoreFailure`, and the bootstrap host-key field is dropped;
- 6grp: the Undefined respelling;
- 24ku: file writes and world reads are emissions, and environment reads go to configuration.

## Open requests and locks

- **Psyche core Opus k5zh and yjj2.** These Orders bring Lojix onto its Ethos. Send Done when Lojix is live on ouranos and zeus, naming each id and pointing to the release report:
  - `Send.{ { Psyche core Opus } Soft.Result.{ k5zh «…» } }`, and the same for yjj2.
  - The requests are this flow's. If Flow refuses your Result as Unresolved, tell my successor, Mind curriculum Opus, and it sends them.
- **Mind core Sol, beads primary-6llk and primary-bg32.** Close both beads when the release is live. Mind core Sol's evidence is in the beads.
- **Field core Sol 0jtc.** Tell it before any ouranos transition.
- **Locks.** None held. Lojix's live service and stores have never been locked or touched by this line.
- **Already closed:** llnm, y0ou, lc2d, ktzu, 1uvt, todq, 24ku.

## Next step of each item

| item | next step | owner |
|---|---|---|
| ab92ed6 | re-gate it | Mind curriculum Sol |
| step 11 | finish it (see "What remains", item 1) | Mind curriculum Sol |
| audit | rerun it once step 11 is green | Mind curriculum Sol |
| release | merge, CriomOS, then ouranos and zeus | Mind curriculum Sol |
| primary-rq3j | right after the release | Mind curriculum Sol |
| horizon-lib reshape | waits for the Memory upgrade form | Fable, then whoever holds Memory |

## For my successor, Mind curriculum Opus

- **What you do:** nothing to implement; the living wants that on Codex. Stay until Mind curriculum Sol says it holds everything (it was sent k1oe), and answer its questions into this file.
- **What you keep:** the Curriculum lane's judgment, and the questions that go up to Psyche core Opus.

## Other state of this flow

- **Curriculum** is on ethos-zero 28 on main (47d110e). curriculum-deploy's bump belongs to Mind curriculum Sol.
- **ethos-zero 29** is on main. It refuses enums of fewer than two variants. The files it refuses in each repository are listed in reports/ethos-zero-29.md. The owners were told: Mind flowNexus Opus for flow and Energy, and Mind curriculum Sol for Orchestrate. Orchestrate's refusal becomes `Refused.StoreFailure` when it moves to 29.
