# Handover — Psyche Primary Ethos topic, flow d5df1d

## Role and topic

Psyche Primary, Ethos topic, Fable, title `Psyche.{ Fable d5df1d }`. Secretary and peer: Psyche Ethos Secondary 1d0733 (Opus; runs every build and test on Prometheus through Nix). Reports to Psyche Core Secondary 445410. Psyche Flow Primary f5a6e9 (secretary 9fed42). Mind Astra 0c85a3 builds ethos-zero; Field 42265e is sole publisher of ethos-zero and repairs Primary.

Owns: the ethos vision against its implementation; the Ethos Zero design decisions the books imply; the golden ethos, types, invariants, inline-import and registry books; the Ethos side of 445410's special representation.

## Governing state

Primary origin main `d9703b5210299bab596cc5d85ae4a84bc4ee32bc`; this flow's records are whole there under `flows/d5df1d/` (every book source, report, `vision/ethos.md`, `notion/ethos.md`, `log.md`; blobs listed in the log's last hash record). Publish from an independent full clone under the Orchestrate `PrimaryPublish` lock; never commit in the shared working copy.

Vision: psyche-skills `vision/ethos.md`, origin main `850fd27228cb7c4a5fb71f7409109d4a437578be`, blob `e53e23bf16811c8772a77771a995c45c933ec2ca`. Changes only on the living's ruling, landed under an Orchestrate lock, then pushed.

Ethos Zero main `07714b0171802787bea1eefe4caa2d826d9c4030` (package 17.0.0): the trait word (item 5) and the inline import `Topic.custom:Name` with the refusal of `Topic:custom:Name` (item 3, `b2fa8b0e6bd273f0b590444d19e72083a3c865e9`) are landed. Baseline before this flow: `c2653dd82adbdb1f1f2f654405c6620e0d06fd58`.

datom-codec main `4dff16b4f7412febc3b71aac8b49680cd20988cb`; 445410's Represented branch `776cf4b8913ed7c69be0a597afd261ab819914c9`. protos main `15b41da8f2579e73ead59bc0c2b97529b8ac32d3`.

ethos-test main `e21e686b821e12daae08094a60df5e679c8e0b0c`: the acceptance suite of `vision/ethos.md`; main check 26 pass, 5 expected-failing; second check against the held set 31 pass, 0 expected-failing. Statement map `STATEMENTS.md`; judgement in `reports/ethos-test-judgement.md`.

Candidates, all green on Prometheus, none pushed, patches under `flows/1d0733/reports/` (each rebuilds its tree on clean 07714b):

- The set, items 1, 2, 6 on the landed 5: `item12-on-item5-{protos,datom-codec,ethos-zero}.patch` then `item6-on-set-ethos-zero.patch`; landing order protos, datom-codec, ethos-zero. Bare (newtype prints as its inner value) and braced trees both complete: `fork3-complete.md`. Gate: the living's types Fork 3.
- Every option of the held forks: `fork-types-12-{1a+2a,1a,1c+2a,1c}.patch` (+ `1c-datom-codec`), `fork-invariants-4.patch`, `fork-invariants-f3-{a,b}.patch`; spec `reports/fork-options-spec.md`.
- Special representation, Ethos side: form in `reports/special-representation-form.md`; `fork3-{bare,braced}-represented-*.patch`, gaps closed in `represented-gaps-{bare,braced}-ethos-zero.patch`.
- Registry forks: `q8-8a.patch`, `q8-8c.patch`, `q8-8b-{6d,6e,6f}.patch`; spec `reports/inline-import-questions-spec.md`.

Solution index: `reports/ethos-solution.md` (items 1–8 with status).

## Open items and who holds them

The living, nine books, each one number:
«Type, new type, alias» 95uNfgPXqPMQ9cDgWNiHd5 (Fork 3 gates the set); «Ethos invariants» 7Sz4yj7ZcGoEy2T8y35Vzk; «The golden ethos» fourth edition 9y9ZqnNDbM6HSRXp1MNydH; «The inline import, third edition» 488DdxYfWUghW6EcBeXg6y (D1, the vision statement for `Topic.custom:Name`); «Two heads, one name» DMEAiqM1GCoCnjhfSGKLQZ; «Two stale examples» DJtpvWov6qxE7LvhcLzxnY; «The alias examples» NZ8GTdxDEnvkEU54kVdLTM; «No tuple, and FlowId» U664wc6k8XWbQvUopmdCLQ; «Sources and the registry» RX6W2WyacPbRaubsz5qgbp. Commented and closed: inline import first (CCFHiycbDtGJFY93SF25UC) and second (UKSnYtjk7CscFHEvsXY1tA) editions, golden ethos third.

On a ruling: land the vision line (lock, push psyche-skills); tell 1d0733 which candidate lands (Field publishes); promote the ethos-test target; new edition for any commented book, never a change to it.

The living: whether «Astra's five candidates» (d4ae97, 3AXTdcjQjzqka5kFHCoLZw) becomes a topic flow; the design given is five single-proposal books, each with a vision line and a figure, Clojure-under-Nix to Field as a message.

445410: the special-representation book; routing of the `protos:String` case (a tension between vision lines 175 and 188, in «Two stale examples»), not a Mind defect until ruled.

1d0733: all patches above; the Represented tests live in the candidate; Problem::Role removed in both trees.

Mind (0c85a3 through Sol): item 7 (`core` refusal) held — it would refuse the living's own key `Topic.core:Name`; it is fork 3 of the registry book.

Held for the next types edition after his ruling: nothing beyond the four tension books.

## Standing limits

- His words travel only as psyche messages; never quoted or paraphrased in a #msg or a book; a message resting on them is two sends.
- One proposal at a time; a proposal accepted whole; a commented book never changes; a new flow's first response presents its context, never READY.
- Every subflow brief carries: "Commit and push nothing in Primary; build heavy work on Prometheus through Nix." Primary publish only from an independent full clone under `PrimaryPublish`, changing only this flow's paths, tree never smaller than main's, one try, no polling; the lock holder is asked for a release line.
- ethos-test: a target only for an observable of ethos-zero; expected-failing only for what is ruled and unlanded; nothing unruled becomes a target.
- Vision changes only on his ruling; the code the books imply is built before his comments as candidates that land nothing.
- Name `psyche-skills/vision/ethos.md` in distillations (the ruled path).
- A flow directory is written only by its flow; evidence from others is a claim until witnessed.
