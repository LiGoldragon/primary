<!-- to-the-living:start -->
Presentation.{ «Nobody edits files» }

# Nobody edits files

```
 ┌──────────────────────────────┐
 │  DECLARATION                 │
 │  (the only thing changed)    │
 └──────────────┬───────────────┘
                │ rebuild, redeploy
                ▼
 ┌──────────────────────────────┐
 │  RUNNING HOST                │
 │  no file edited here         │
 │  no state set by hand        │
 └──────────────────────────────┘

 a local fix ──╳──▶ a change of architecture
```

No psyche skill says the system is declarative; only a machine skill does, and it says to change the system «by editing its declarative source». Your records: flows/d68c82/vision/criomos.md, 2026-10-11; flows/b666e7/vision/declarative-features.md, 2026-09-30 (declarative features, nothing tuned on any host by hand); flows/caf622/vision/stateful-installation.md, 2026-09-29 (nothing installed statefully). An older record of 2026-08-17 (flows/01a01046/vision/noctalia.md) had a stateful override; the three later records displace it.

## Distillation

### Proposal 1: in vision-deployment

File: `psyche-skills/skills/vision-deployment.md`. Added, as a new section before «## A proof of concept deploys on the flow's own host»:

## The system is declarative

The operating system is declarative. What a host runs is its declaration, rebuilt and redeployed; nothing is installed, tuned or set on a host by hand, and no file on a running host is edited.

Added to «## Sources»: d68c82 criomos; b666e7 declarative-features; caf622 stateful-installation.

Ruling 1: does the section land?

Ruling 2: «nobody edits files anymore, ever». The section above reads it as: no one edits a running host's files; the declaration is still edited by hand. The wider reading is that declarations too are generated, never hand-edited, as the generated skill trees already are. Which did you mean: 1, the running host only; 2, the wider one? If 2, the last clause becomes «and no file is edited by hand: a change is made to the source it is generated from».

### Proposal 2: in spirit

Record: the same 2026-10-11 words, «Why are you taking it upon yourself to decide that we're changing all the architecture and how things are done?»

File: `psyche-skills/skills/spirit.md`. Added, as a new line after «Start with the smallest shape that works. Add machinery only where the requested behavior needs it.»:

A blocker met on the way is not a reason to change the architecture or how things are done; a flow that cannot proceed inside them says so.

Ruling 3: this is a conduct correction read as spirit. Does it land there, as worded, or is it vision for a narrower skill?
<!-- to-the-living:end -->
