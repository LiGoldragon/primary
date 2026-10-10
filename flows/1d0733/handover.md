# Handover — Psyche Ethos Secondary (Opus)

## Role and topic

Psyche aspect, Secondary layer, topic ethos. The secretary of Ethos Primary d5df1d
(Fable): relay to and from it, supply it psyche data, and build and test what it
designs through subflows. Report to Psyche Core Secondary 445410. Mind matters go
through 445410 or Mind Secondary Sol 41fa34, never to Mind Primary (Astra 0c85a3)
directly. Field reaches this seat only through Mind.

## Governing state

Repositories (GitHub main unless named):

- ethos-zero main 07714b0171802787bea1eefe4caa2d826d9c4030 (items 3 and 5 landed; 17.0.0, trait word)
- datom-codec main 4dff16b4f7412febc3b71aac8b49680cd20988cb
- protos main 15b41da8f2579e73ead59bc0c2b97529b8ac32d3
- ethos-test main e21e686b821e12daae08094a60df5e679c8e0b0c — two checks: against 07714b
  (26 pass, 5 expected-failing, 10 differs, 21 no-observable, 19 unruled) and against the
  held set (31 pass, 0 expected-failing)
- psyche-skills main 850fd27228cb7c4a5fb71f7409109d4a437578be; vision/ethos.md blob
  e53e23bf16811c8772a77771a995c45c933ec2ca
- datom-codec branch 445410 776cf4b8913ed7c69be0a597afd261ab819914c9 (445410's Represented)
- ethos-zero branches, non-main, pinning the held set for ethos-test; remove all three when the set lands:
  candidate/held-set-bare a3f6068ecef547fd2a1e884677d8164d3456792c,
  candidate/held-set-datom-codec 3e86f813b2e67e0b56956fbdcb68c1da12e91e88,
  candidate/held-set-protos aa97df7ff0b79172e2d09613674c936bb4c85067
- Primary: this directory published as 23509e1b05ac0e2c3e8da16bbad70ed61e5e4efd

Final candidate patches, all green on Prometheus, none landed, in
`flows/1d0733/reports/` (blob hashes in `reports/handover-hashes.md`). Each
reports `.md` beside it describes the base and how to apply.

- Held set, bare Fork 3 (items 1, 2, 6 on 07714b; lands protos → datom-codec → ethos-zero):
  item12-on-item5-{protos,datom-codec,ethos-zero}.patch + item6-on-set-ethos-zero.patch
- Held set, braced Fork 3: braced-set-{protos,ethos-zero}.patch (datom-codec main unchanged)
- Special representation, Ethos side (association `T.[ Represented.{ Representation.X } ]`,
  pinned by assertion, bodies hand-written, no skeleton; accepted by 445410):
  fork3-<bare|braced>-represented-*.patch, then represented-gaps-<bare|braced>-ethos-zero.patch
  (imported roles from dependency ethos; Expected.Type / Expected.Trait; Problem::Role removed)
- Datom-codec Represented under both answers: representation-fork3-<bare|braced>.patch
- Types Forks 1–2: fork-types-12-{1a,1a+2a,1c,1c+2a}.patch, 1c also fork-types-12-1c-datom-codec.patch
- Invariants 4 (print layout, rule: a form breaks when it holds variants, more than two
  positions, or a broken form; closes after its last element): fork-invariants-4.patch
- Invariants Fork 3 (Mutex): fork-invariants-f3-{a,b}.patch; (a) is import-only
- «Sources and the registry»: fork 1 q8-8a.patch; fork 2 q8-8b-<6d|6e|6f>.patch by his Q6
  letter; fork 3 q8-8c.patch (refuses his own key Topic.core:Name)

## Open items

- Living's rulings, all before him: «Type, new type, alias» (Fork 3 gates the held set),
  «Ethos invariants», «The golden ethos» fourth edition, «The inline import» third edition,
  «Two heads, one name», «No tuple, and FlowId», «Two stale examples», «The alias examples»,
  «Sources and the registry». The day he rules, land the matching patch set through Field.
- Item 7 (refuse source core): held by d5df1d; superseded in meaning by «Sources and the registry».
- protos:String vs String: a vision tension (lines 175 vs 188), held by Mind until he rules
  «Two stale examples».
- Variant named like a declared type carries it: the ruled rule working; Flow (f5a6e9) renames.
- Field 42265e: the book renderer shows a `##` file line as a heading (fixture path given to 445410).

## Standing limits

- Every subflow brief carries: run no git command in /home/li/primary other than read-only
  ones; commit and push nothing there; push no branch to any shared repository; build heavy
  work on Prometheus through Nix, witnessing `hostname`.
- Publish this directory only from an independent full clone under the PrimaryPublish lock
  (compensation-primary-commit), only flows/1d0733 paths, with the COPY's tree file count
  at least main@origin's. Never commit in the shared working copy.
- Land nothing in ethos-zero, datom-codec or protos; Field lands from the patches.
- The living's words travel only as psyche messages (`hm-send --psyche`), never inside a #msg.
- Psyche records: flows/1d0733/vision/ethos.md (five entries), flows/1d0733/notion/ethos.md (one).
