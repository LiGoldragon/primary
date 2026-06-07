# 4 — overview: the corrected, stable verdict

cloud-designer, 2026-06-07. The synthesis after the adversarial verification pass
(`wykwplbt0`). This **supersedes `1-forensic-verdict.md`** (which overclaimed) and
withdraws `34/5-redesign.md`'s opposite overclaim. Grounded in: full
`actor-systems.md` + `component-triad.md`; verbatim Spirit `czw0`/`59dr`/`opvx`/
`ocu7`/`rpr5`/`7ca4`/`h3u7`/`2alg`/`k6w1`/`tj99`/`1483`/`1487`; and a code+history
sweep of all seven daemons.

## The question

The psyche: *"Don't we have a skill that says actors all the way? … Is there a good
reason [the generated stack is sync/no-kameo] or did the agent just misinterpret
something I said and then start hallucinating … we only build actor model systems."*

## The answer in one paragraph

It is **neither a clean "good reason" nor a clean "agent hallucinated."** The sync
generated stack rests on **two genuinely recorded decisions** — a thread-per-
connection concurrency model (`2alg`/`k6w1`/`tj99`) and a dated deferral of the
actor-mailbox/scheduling machinery (`1483`/`1487`=`czw0`) — both written into
`skills/component-triad.md` as "the substrate that lands now." **But** those
decisions sit in **direct, unreconciled contradiction with `skills/actor-systems.md`**,
which says in the present tense "Actors all the way down" and "a daemon … *is* an
actor." The agents followed one of two contradictory skills. The psyche remembers
the other one. **The root cause is that the workspace's own guidance answers this
question both ways, and nobody reconciled the two files.** (And the lojix repo's own
docs still say "Each daemon actor is a Kameo actor" while the code dropped kameo — a
stale-doc manifestation gap on top.)

## The three layers, kept distinct (this is what both my prior verdicts collapsed)

| Layer | Status | Evidence |
|---|---|---|
| **Concurrency *shape*** — bounded thread-per-connection, per-request engine, store as brief shared lock, permit cap | **Recorded intent. Deliberate.** Chosen *against* the serial single-writer model. | `2alg` (Decision, 06-06), `k6w1` (Principle, 06-06), `tj99` (Decision, 06-06); lojix `BoundedWorkers` cites them |
| **Sync engine-trait *substrate*** — `NexusEngine::execute(&mut self) -> NexusAction`, no mailbox, runner drives on the call stack | **Recorded, dated deferral.** Documented as "what lands now," actor promotion deferred "until overload evidence appears in real production load." | Spirit `1483` + `1487`(=`czw0`), written up in `component-triad.md` §"Runtime triad engine traits" |
| **Total absence of kameo / any actor runtime** | **Realization of the deferral — consistent with `1483`/`1487`, but never explicitly chosen, and contradicts `actor-systems.md` + lojix repo docs.** | Code: zero kameo in all 7 Cargo.toml/Cargo.lock; no commit cites intent authorizing "sync instead of kameo" |

My report 34 collapsed all three into "sync is settled, intent wins" (over-read the
deferral as a final decision). My report 35/1 collapsed all three the other way into
"nothing authorizes it, agent hallucinated, I invented the carve-out" (missed `2alg`/
`k6w1` and missed that the carve-out is real in `component-triad.md`). Both were the
same error — reading part of the evidence and over-claiming. The accurate picture is
the table above: shape authorized, substrate deferred-by-record, kameo-absence an
unblessed-but-consistent realization, all colliding with a contradictory skill.

## Did an agent "fuck up"? The honest decomposition

- **The concurrency model:** no. It is recorded intent solving the real
  "nix build must not block other connections" problem.
- **Building the sync engine-trait substrate first:** defensible. There is a real,
  dated, recorded deferral (`1483`/`1487`) that says exactly this is what lands now.
- **Where the genuine failure is:** the workspace shipped **two contradictory
  pieces of guidance** — `actor-systems.md` ("runtime roots ARE actors", present
  tense) vs `component-triad.md`/`1483`/`1487` ("actor machinery deferred, sync
  substrate lands now") — and never reconciled them. That contradiction, plus the
  stale lojix docs still mandating Kameo, is the real bug. It is also why *I* kept
  swinging: I was reading one file at a time.
- **My own failure (twice):** in `34/5` I declared the fork "settled by intent"
  toward sync; in `35/1` I declared it "pure unrecorded drift." Both overclaimed
  from partial evidence. The adversarial pass I ran specifically to check myself is
  what surfaced the correction. Logged plainly here.

## The one engineering fact that should anchor the decision

The deferral's stated trigger is *"if/when overload evidence appears in real
production load."* There is **no production** (per `ESSENCE`/`ax2k`). So the
condition the deferral waits for cannot arrive in the current phase — which means
"defer until production overload" currently functions as "defer indefinitely." That
is worth the psyche knowing: the carve-out was written for a production-pressure
world that the zero-compat, pre-production reality doesn't match.

Separately, the *only* hard engineering reason sync is tempting — lojix's
multi-minute blocking nix build must not starve other connections — is **already
solved within the actor model**: `actor-systems.md` §"Blocking is a design bug"
mandates blocking work live in a dedicated blocking-plane actor (`Command`/
`CommandPool`, `spawn_blocking`+`DelegatedReply`, dedicated OS thread), bounded by
permits — which is exactly `BoundedWorkers` semantics, just hosted in an actor tree.
So actors and the authorized thread-per-connection shape are **not in conflict**;
kameo can realize the `2alg`/`k6w1` model directly.

## The decision the psyche actually faces (genuinely theirs)

This is one fork the guidance currently answers both ways. Reconciling the two
skills is the real deliverable, regardless of direction:

- **Option A — resolve toward actors now** (matches the psyche's stated instinct
  and `actor-systems.md`): promote the generated triad stack to kameo actors;
  realize the `2alg`/`k6w1` bounded-thread-per-connection model as blocking-plane
  worker actors under a supervised runtime root; **retire the `1483`/`1487`
  deferral** (its production-overload trigger doesn't fit a pre-production world);
  update `component-triad.md` to drop the sync-substrate-as-end-state framing. This
  is `34`'s Proposal B (actor-native), which I wrongly discarded.
- **Option B — keep the deferral**: sync engine-trait substrate now, actor
  promotion later; **fix `actor-systems.md`** to carry the explicit today/eventually
  carve-out so it stops reading as "kameo daemons now," and update the stale lojix
  docs. (This is the weaker option given there's no production to generate the
  overload evidence the deferral waits for.)

Either way: **the two skills and the stale lojix docs must be reconciled** — that's
the non-optional follow-up. No Spirit record was captured this turn; the direction
is the psyche's to decide, and that decision is what gets recorded (superseding/
clarifying `1483`/`1487` accordingly).
