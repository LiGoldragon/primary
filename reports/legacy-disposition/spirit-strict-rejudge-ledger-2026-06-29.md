# Spirit Strict Re-Judge — Keep Ledger (2026-06-29)

Judgment-and-proposal only. READ-ONLY on Spirit (Observe/Count only). Nothing
removed, edited, or rehomed — this ledger is for the psyche to adjudicate the
keep-set before anything moves.

Supersedes the classifications in `spirit-cleanup-plan-2026-06-26.md` (that plan
kept 575 under the OLD loose bar). Re-judged from scratch under the strict bar in
`HANDOVER-2026-06-29-spirit-matter-enforcement.md`.

## Scope and method

- Corpus: Spirit active set = 650 records (certainty >= VeryLow). All Privacy
  Zero (public). Confirmed live via `Count` -> `(RecordsCounted 650)`.
- Dumped the full active set via `Observe` (8-field Query, certainty floor
  AtLeastCertainty VeryLow), parsed all 650 into id + domain + kind + description
  + certainty + importance + referents (0 parse failures).
- Strict bar applied to every record, DEFAULT = MATTER. A record STAYS only if
  ALL of: directive · durable · universal · psyche-authored · single-claim · not
  matter. MATTER if ANY of: too specific/technical · transient/one-off ·
  single-component or architectural · restated skill / Spirit-usage /
  agent-training material · agent-authored · multiple clauses fused. Asymmetry:
  keeping matter OUT outweighs letting intent IN; when in doubt, MATTER.
- Bulk classification fanned out across 10 parallel workers, each applying the
  identical bar to a 65-record batch. Every keep/borderline return was then
  vetted personally against the full description, and the independent
  non-Technology-domain sweep (94 records) plus a governance-signal grep were
  cross-checked so no universal directive was buried in the Technology bulk.
- Coverage verified: all 650 ids classified exactly once (0 missing, 0 extra).

Observed fact vs interpretation: the id/domain/kind/description/magnitudes are
observed from the live store. KEEP/BORDERLINE/MATTER and home tags are
interpretation under the strict bar. Verbatim psyche testimony is NOT in the
Observe projection (only the clarified description), so a few borderline split
calls should be confirmed against testimony at execution time.

## KEEP-CANDIDATES (11) — plausibly clear the strict bar; psyche confirms

Universal, single-claim, psyche-authored direction about the work or the world,
not tied to one component/tool/repo and not a skill/Spirit-usage restatement.

- `jlo7` | State everything positively; lead with the desired practice, the why outweighs the what-not | universal rule across all guidelines, names, and communication; one claim.
- `ty3g` | An agent is a machine; every failure is a guidance gap — fix the guidance, never blame the agent | universal stance on agents and failure; load-bearing, single claim.
- `w312` | Deterministic-from-input work (routing, dispatch, lookup, classification) is mechanism for code/schema, never agent judgment | universal division-of-labor rule; the why behind the whole schema-derivation thrust.
- `9g07` | Most correct wins, not shortest or smallest | universal quality maxim for any implementation choice; one rule.
- `izsf` | A psyche design decision applies to the WHOLE design unless explicitly scoped | universal rule on how to absorb any direction; not component-bound.
- `j8g6` | Scope work by what it requires, not by time estimates | universal planning maxim; directive, single-claim.
- `sfy0` | Ask fewer questions at a time, with enough context to answer directly | clean single-claim universal communication directive.
- `obo5` | When the psyche loses the thread, stop and re-ground top-down; their understanding is a precondition for proceeding | universal psyche-facing leadership principle, single claim. (Worker tagged skill; elevated on vetting.)
- `jys2` | Design at the post-agent capability frontier — target the best end-shape, not a historically-practical compromise | universal design stance; psyche philosophy. (design-telos cluster — see note.)
- `sj2c` | The build target is the best possible design — the terminal best, not good-enough | universal design telos. (design-telos cluster.)
- `cam8` | Design analysis targets the ideal pattern and contrasts it with current so the gap is visible | universal design method. (design-telos cluster.)

Note — design-telos cluster: `jys2`, `sj2c`, `cam8` (and borderline `zn2l`) are
near-restatements of one "aim at the ideal/best design" value. Each individually
clears the bar; the psyche may wish to MERGE them into one or two strong records
rather than keep all.

## BORDERLINE (18) — genuine edges for the psyche to rule

Most carry a keep-worthy universal kernel welded to matter; the handover's
bundled-record rule (shed the matter clause, reintroduce a clean directive)
applies. Tension noted per record.

- `qjrf` | Ask the psyche when a design surface is incomplete; don't fabricate intent | the blessed ask-don't-fabricate maxim, but welded to capture-gate definition ("intent layer holds intent not info") = Spirit-usage matter. Split (precedent: handover qjrf disposition).
- `q9n2` | Match effort to the request and stay within the asked scope | strong universal scope-discipline core, but fused with effort-sizing + MVP-proposal clauses (bundled).
- `48y4` | When work is authorized, execute fully autonomously; reserve asking for genuine forks | strong autonomy maxim, but a subagent-dispatch (agent-training) clause is welded in.
- `ki6i` | Proceed on reversible defaults; block only on hard-to-reverse decisions | universal judgment maxim, but agent-conduct overlapping intent-clarification/keep-working; near-duplicate of `48y4` (merge).
- `hv5f` | Follow where the logic wants to go (desire paths) rather than the existing shape | strong universal design maxim, fused with a second convergence-signal claim.
- `lrfa` | Value lean design; break freely in development, not production | genuine ethos, but welds break-in-dev to a lean-means-no-duplication clause that overlaps beauty/abstractions skills.
- `j81n` | Actions are taken, not announced | clean near-universal maxim, but framed as agent-chat/workflow-state discipline (agent-training).
- `t5qr` | Judge the design of what you touch while debugging/rewriting; surface flaws rather than silently working around | universal-leaning work principle, but code-quality discipline kin to beauty/code-review skills.
- `zn2l` | The endpoint is the final self-improving software engine | genuine non-technical psyche telos, but descriptive vision (workspace ESSENCE material) more than an applied rule.
- `o7zt` | Lead with a plain-language description; the opaque identifier is a trailing reference; name the concrete noun first | strong durable communication directive (kin `jlo7`), but partly bundled with reporting-convention detail (line-number suffixes, identifier placement). (Worker tagged skill.)
- `nu76` | A major first-digit version bump requires explicit psyche authorization | clean single-claim psyche governance gate, but the versioning skill restates the mechanism. (Worker tagged skill.)
- `op4b` | New GitHub repos only on explicit psyche authority | a genuine psyche governance gate, but welded to a feature-branch-default clause that belongs in the feature-development skill. Split. (Worker tagged skill.)
- `k09z` | Act on private personal-affairs material only when the owning psyche requests it; ask when in doubt | universal privacy-authority kernel, but bundled with instruction-file-placement mechanics. (Worker tagged skill.)
- `qoku` | Routing intent through a third-party hosted inference API is not a privacy violation | universal privacy-scope clarification (the rule guards publication to world-readable surfaces), but reads as a one-off clarification. (Worker tagged skill.)
- `h0bj` | Personal substance is private; infrastructure/general-knowledge intent is public | universal privacy classification kernel, but bundled with Spirit privacy-magnitude mechanics. (Worker tagged spirit-manual.)
- `gni3` | Agent-authored content is not a psyche-authorized design surface; retracting agent-drift restores reality | universal authority/provenance principle, but overlaps the intent-core doctrine (arguably Spirit-usage). (Worker tagged spirit-manual.)
- `c5nq` | Build event surfaces, not polling — producers push, consumers subscribe, escalate to add an event surface | universal system-design principle, but restated by the push-not-pull skill. (Worker tagged skill.)
- `hu84` | Cross-audit — one model audits another's output before it is trusted | genuine universal quality principle, but bundled with subagent-by-default orchestration mechanics. (Worker tagged skill.)

## MATTER (621) — must leave; grouped by proposed home

Home tags are a reasonable first placement, not a final routing. The bulk is
architecture/component matter. Per-record home precision was intentionally not
chased.

### architecture-doc (384) — component/engine/schema/NOTA/rkyv/sema/nexus/signal/wire/storage internals and single-component or architectural decisions

```
06l6 07pn 081i 0dsr 0dys 0yx5 150a 1aam 1hyg 1sa2 1vj5 20id 26e7 29pb 2alg 2cuo
2dzp 2f04 2foy 2i75 2qhw 2qia 2rb7 2uhh 2v9u 31nz 32wj 34hu 3742 3chp 3d5z 3don
3fm6 3got 3itj 3naf 3nla 3qjw 3sq4 42rh 44dp 4d8f 4fao 4frx 4itr 4np2 4oev 4wt3
506w 54g9 57f9 58bv 5cyn 5d5o 5fck 5fdr 5jac 5mxn 5myr 5p9s 5pf6 5zgi 61lk 62r4
6cfr 6grf 6jdv 6oun 6th4 6wwf 70gd 7118 75pw 77i8 7c71 7d4x 7kyx 7l7l 7let 7rrs
7sx6 7tqc 7x5z 7y8w 7yth 80bl 878r 87ts 88eq 8p0r 8pux 8rew 8u1o 8y24 94sj 96mi
9npk 9pil 9uje 9v7h 9xwr 9yxh a2t4 a4i6 a5tg a9sq ahop alom ay3y b05y b0s4 b1vi
b9ao ba6d beaj bexd bhs5 bkcd bkzd brgo burk bw9v bwid bybe c6j4 c8b3 c8lc c9fv
cbtg cd76 cgd8 cok7 cqxg crlc cyik czw0 d3r2 d5v6 d6if dcqz ddlv dfl5 dqmc duis
dun9 dx10 e8iu edqu ef6i en7k eo25 er9w ermr esn1 ezcy f8ds f8k7 f8m3 f8tb fcsg
fhe8 flqt fo38 fosp fry8 fuls fvtf g2xr g31j gb3d gdbf ghw7 gjr1 go9u gopu gvgu
h03z h053 h6fh h9xd hc0t hckx hetk hl1z hqg7 hrte i1b5 i1jw i4ak i6ih i8wt i9xk
ic4o iir4 iprx irmw isia iwbt iypq izib jaz4 jl3k js6b jwm9 k5y3 k6w1 kfqa khbv
kzk5 l0w8 l1ip l3ca l6zw l8ox laim lc28 lf7y lilh lk22 lt44 lvy9 lw73 lxo3 m3eg
m3ms m5jl m76h m91k mbmy mcuk mimk mn3k mq5s mqlb mu0o mz16 mzfj n5ch nc9k neib
ng1x nm97 ns7t ntsg o2xk o8x5 oe6s of73 ok16 ooxy oqwb ospz own9 oxgh ozbz p43g
p675 p6fx p6k5 p8sq pb1g pbgy pdbn plum pmg5 potn ppp4 ppuk psc6 pul9 pviw py4h
q13r q33b q4gd q4l0 q73w qbx7 qe84 qkrg qkvx qmsh qv4q qw1j r0le r2jx rfg9 rj9y
rmqo rmv8 rnrg rpog rq3p rxcp s5dz s8lq sanf sarw sd7x sjcy so0p sqnx sqrk sqx6
ssk2 str0 t0tu t4gd t5wx tace tbff tdfp tdvr thi1 tmji tpvu tw15 twlp u7fj u7tj
udgu udjq ugig ujb2 umsv ur16 uuh7 uujd ux9i uzxp v0n6 vdiu vfgk vfjw voa8 vpbx
vqbt vr32 vudl w1ss w54p w6y1 wgii wl2a wqdi wrjl wv2a wvgh wvpg wx5c x0ja x2yz
x92t xai7 xbc2 xbu8 xe6q xen8 xhwa xiqa xk7f xlrk xnnb xprx xqkv y1v5 y3ag ychx
ycmd ycwf ydpa ymq8 yngr yp29 ypb5 yr2w yzwg z6qu z9d6 z9kv zdie zg84 zjmc zrrv
```

### skill (98) — work-discipline already owned by a skill (jj, feature branches, testing, naming, reporting, nota-design, orchestration, beauty, etc.)

```
1kfk 1sx5 20hv 26m5 29s6 30cu 3do3 3ey7 3pw2 4ivz 4lkn 4ry9 56kv 57hq 6u6o 6utp
6x2k 6xzu 7gcs 7nbu 9o9g aipc amb5 b2jg bcm1 biij bn07 bsrv cb0j cjrl d0fi d0mp
dctk di1r e3ou ecbv eg3a eh5a el7z g7yd g9oc h2oa hg78 ii8v j028 j4r1 jkkq jldt
jq8w js3u k2o1 k4i3 ka4l krez ktub kxzh kype l50b mi6m mz3p n097 n1x8 nifs o5rz
p29p papc pjib pm1b pn0n q9iz qmbf qr9g r2x2 rg2i ri4n tbg6 tdsu tenr ty8z tyoz
us1v utaa uxnu vcin vqtd w2mf w85v wc4n wfzz wx57 x3m9 ykdi ypg9 yy76 zbfq zeuy
zze6
```

(Includes `r2x2` commit-entire-working-copy and `hp9n`-adjacent jj rules already
in the jj skill + AGENTS.md; `ykdi` code-elegance -> beauty/abstractions/naming;
`56kv` designer-lean -> orchestration role discipline.)

### spirit-manual (76) — Spirit/guardian/certainty/capture mechanics and Spirit-usage / agent-training material

```
0fmg 0s5u 0xqp 1rcj 29ed 2gj4 2o5j 2st7 2vp2 3jkx 3pfh 3v3r 3w61 5g5h 5tar 5trg
69fa 6kfz 7mvx 80zj 853n 8jtz 8l2a 8rpu 9c6f 9huv a3l4 arb2 bwxn ca65 cws0 dfii
ek8w f5jr fiw4 g78b g8ln h7sz hgvg hvfe icpa j6r4 jn3m k12x kasm kfon kg2z mlq0
nob8 nr7h oj3i opbj otel qr5o qy15 rh29 rvnf s0wd sn1g t4uq tf2o tfpd tw81 uara
urnt vjye x1rz xblw xf25 xpen y212 ywua z3ka zjho zjop ztX
```

### code (33) — config/operational facts: paths, tokens, node names, wiring, deploy commands, hardware/network setup

```
0a9p 11m7 16l0 1924 242o 51u8 6wz8 8fe9 b0v3 bc6f bdse bev5 cncj cx7y go41 hp9n
jtos kx32 nsi2 nz0t osoo p7kn qxye rc8v ud6l ufjd upza vgon wn7q wp91 wprd zeqq
zgwf
```

(`hp9n` repos-untracked is already manifested in AGENTS.md hard boundaries; the
TO-ARCH config facts from the 2026-06-26 plan — go41 nz0t 16l0 upza bdse nsi2
osoo qxye — recur here. Most code/config homes are UNTRACKED repos; landing them
needs the psyche's hold/edit-untracked/transitional-in-tree call.)

### vocabulary-doc (12) — definitional "what term X means"

```
1i1b 4vde 8koe beue bnxx cx2m d2ql fwme kmhb ngk0 qerc tnam
```

### repo-intent (11) — direction tied to one specific repo

```
8dib aa7l bsg1 ctkv edgt m9yz p4sm tvbn uh8l umgr wa4j
```

### junk-remove (7) — obsolete / test placeholder / pure duplicate

```
zNEW9 zt1 zt2 zt3 zt4 ztA ztB
```

`zNEW9` ("insert-only proof"), `ztA`/`ztB` ("trivial a"/"trivial b") are test
placeholders — safe hard-remove. `zt1`–`zt4` (plus `rvnf` and `ztX`, here in
spirit-manual) are six copies of one capture-gate discipline — migrate once,
remove the rest.

## Summary

Total judged: 650 active records (cert >= VeryLow, all Privacy Zero). Under the
strict bar the surviving intent core is small: 11 KEEP-CANDIDATES and 18
BORDERLINE (most of the borderlines are bundled records carrying a keep-worthy
universal kernel that should be split out and re-recorded clean), leaving 621
MATTER — roughly 95% of the corpus. Matter home distribution: architecture-doc
384, skill 98, spirit-manual 76, code/config 33, vocabulary-doc 12, repo-intent
11, junk-remove 7. The keep core concentrates in universal work/communication/
design maxims (state positively; agent-failure-is-a-guidance-gap; deterministic
work is mechanism; most-correct-wins; ask fewer questions; re-ground the psyche;
design to the ideal), with a design-telos trio (`jys2`/`sj2c`/`cam8`) the psyche
may want to merge. The 18 borderlines are the split-or-keep decisions: governance
gates (`nu76`, `op4b`), privacy kernels (`k09z`, `qoku`, `h0bj`), the
ask-don't-fabricate maxim (`qjrf`), the push-not-pull principle (`c5nq`), and a
set of autonomy/design-process maxims fused with agent-conduct.

## Follow-up requirements

- These rulings are provisional until the psyche confirms the keep-set. Nothing
  is removed or rehomed here.
- At execution, confirm the bundled-record splits (`qjrf`, `op4b`, `q9n2`,
  `k09z`, `h0bj`, `hu84`, `lrfa`, `48y4`, `hv5f`) against verbatim testimony, not
  the clarified description, before extracting the clean directive.
- Resolve the design-telos overlap (`jys2`/`sj2c`/`cam8`/`zn2l`) and the
  near-duplicate autonomy maxims (`48y4`/`ki6i`) by merge decision.
- Removal path is archive-first (the deployed 0.18.1 meta-socket
  `CollectRemovalCandidates`); rehoming the matter into manuals/architecture/
  skills is a separate follow-on pass, several homes being untracked repos.
