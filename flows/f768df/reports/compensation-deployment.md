# Recurring-compensation deployment map

Source: `flows/d4ae97/reports/recurring-insistences.md`.
This is a deployment map, not a new ruling. “Overlay” means an
authored `compensation-*` skill; its body is delivered by the common
standing-load path rather than copied into a role module.

| Report entry | Final authored home | Disposition |
| --- | --- | --- |
| 1, 20 | `compensation-truth.md` | Adopted: sourced-claim and inspect-before-unknown rules. |
| 2, 4, 43 | `compensation-orders.md` | Adopted: execution, standing-order capture, and closing evidence. Revised `tools/main-flow-mode/system-prompt.md` removes forced questions. |
| 3, 17, 19, 37 | `compensation-prose.md` | Adopted: concrete prose, plain recipient message, prose/code boundary, and no-echo rules. |
| 5, 6, 11, 12, 23, 35, 39, 40 | `compensation-launch.md` | Adopted: focused launch, remote readiness, delegation, successor, brief, permission, and lateral contact. The 30%-or-200k trigger applies only to observed values. |
| 7, 16, 34, 44 | `compensation-messenger-clj.md` | Revised: work-owner/live-recipient, verbatim relay, hm-send-only, and receipt-failure rules. It does not invent a Flow lookup wire or treat Transported or Presented as read evidence. |
| 8 | `compensation-default-effort.md` | Revised: cheapest-sufficient and explicit never-extra-high rules; `subagents/book.md` stops naming Opus High. |
| 9, 14, 27 | `compensation-understanding.md` | Adopted: repeated-miss repair, sense-first STT, and case-bounded correction. No unconditional Notion-to-Vision substitution. |
| 10 | `operation-flashbook.md` | Revised: source-complete illustrated coverage. |
| 13, 41, 42 | `compensation-prose.md` | Adopted: current-term and no-new-term checks. `psyche-grasp.md` is revised to say Ethos/datom; `psyche-interraction.md:44` is owner-coordinated to defer layer/model/effort to configured Flow values. |
| 15 | `file-editing.md` | Existing shared-primary rule retained. `compensation-primary-commit.md` is held pending the living’s ruling. |
| 18, 26, 32, 45 | `compensation-design.md` | Adopted: durable-record, vision-boundary, preservation-before-delete, and no-binary-primary rules. |
| 21, 22, 29, 36, 47 | `compensation-book-distillation.md` | Existing first two lines retained byte-for-byte; book source conflict repairs are revised in `trial-presentation-book.md` and `subagents/book.md`. |
| 24, 31, 46 | `compensation-design.md` | Adopted: smallest working shape, live-before-feature, and portable typed-interface rules. No blanket deletion policy. |
| 25 | `nix-workflow.md`; `compensation-default-effort.md` | Revised: remote-builder-only Nix rule; adopted Prometheus rule only for local model hosting and files. |
| 28 | `compensation-design.md` | Adopted: seek a ruling for a concrete conflict or absurd consequence. |
| 30 | `behavior.md:24` | Existing: incomplete work names its blocker, unblocker, and needed decision; `compensation-prose.md` loads that rule rather than duplicating it. |
| 33 | `skill-designing.md` | Existing trial/compensation exception retained; no gold-skill edit. |
| 38 | `compensation-prose.md` | Adopted: refusal once with cause; no alternate-form retry. |

## Contradiction disposition

| Report conflict | Disposition |
| --- | --- |
| 1 | Remove compulsory “questions that need a ruling” from `tools/main-flow-mode/system-prompt.md`. |
| 2 | `compensation-truth.md` makes a source check or an explicit unknown the next act. |
| 3 | `compensation-design.md` requires the smallest sufficient shape first. |
| 4 | `operation-flashbook.md` preserves all source points. |
| 5 | `trial-presentation-book.md` and `subagents/book.md` stop requiring quoted living words. |
| 6 | Held: `compensation-primary-commit.md` remains untouched pending a ruling. |
| 7 | `subagents/book.md` removes the explicit Opus/High chooser and corrects wording that names the book artifact; it preserves the Page storage/API workflow. |
| 8 | `nix-workflow.md` removes local build fallback. |
| 9 | `psyche-grasp.md` changes `Dotos` to `Ethos`; new compensation wording uses Flow. |
| 10 | `compensation-launch.md` supplies the refresh trigger but makes no unsupported runtime claim. |

## Delivery boundary

`roles.datom` now declares one standing selection. `curriculum-deploy`
appends the selected authored bodies to every generated role packet and
generates `tools/standing-skill-selection.mjs`; the Claude, Codex, and
OpenCode launchers import that one selection for their first prompt.
The launchers keep `main-flow` first and retain their harness-specific
and aspect-specific additions. No running flow is claimed to have
reloaded it.

The standing set is exactly `spirit` plus the nine compensation
overlays: `compensation-book-distillation`, `compensation-truth`,
`compensation-orders`, `compensation-prose`,
`compensation-understanding`, `compensation-launch`,
`compensation-design`, `compensation-default-effort`, and
`compensation-messenger-clj`. It is not a claim that every one of the
47 report homes loads universally. `behavior`, `file-editing`,
`operation-flashbook`, `skill-designing`, `nix-workflow`,
`psyche-grasp`, `psyche-interraction`, `trial-presentation-book`, and
`trial-succession` remain situation-triggered at their existing skill
boundaries; their regenerated files merely carry their authored
corrections.

## Frozen publication manifest

This is the complete same-flow source candidate. It includes the
predecessor’s `af6d4ec3` additions, which must be published with the
current corrections; it does not treat them as remote state. SHA-256
lines name the exact frozen source content.

Curriculum (`af6d4ec3` parent `c98fc439`, plus the listed worktree
corrections):

```text
3c29abc4be1d68a7d2f7ac79c99769520c6896fbeac155a3f1cf7d296bc361c5  skills/compensation-default-effort.md
dfd67c4b712b97f3fa647073f7d4cbe745eb003e6720f0fc1078345867d60fbe  skills/compensation-design.md
0e9c51ecf9dd59e15514cb445776c255e0b791946586a64c152c9f1a52375cef  skills/compensation-launch.md
e7714941bc6acba84bbf78ca3ff707cc4681d39c17926027a78cd281a2b9ab0f  skills/compensation-messenger-clj.md
d36455d198d387228aebcaf632f73077716ccf0add68344823bea3213eb95d26  skills/compensation-orders.md
8e3842b4a11dbc0627a6a2f16a8166e565bc7e326a5973c1ff4b7857d8277a57  skills/compensation-prose.md
89d0c20d96bb44298c616649f8092687e436e5f9687d017c6adb23949867cf08  skills/compensation-truth.md
a1c107f05bfc48831062134e576e53f0d67a420e8b47a4cfdf3f10bd0a3df83a  skills/compensation-understanding.md
baabb8605909a03f85effb2688b81b0721e717716e02959525bbfe517208a20c  skills/nix-workflow.md
41d90f27a9ec31f76813742e247881c5060e7ea7b0039c169215e9411b457e20  skills/operation-flashbook.md
340e708c1ba3f3fce62b4273fc3c5e61566253f662e46f06a960f8c62aa77165  skills/psyche-grasp.md
005b14c7d21ff3a66befc18b71e47942666bad1d6859cfbacb457bd8d5de5418  skills/psyche-interraction.md
3f0e11dd56cc171ec5837d4ac2bba4addb5c4fceb724d925702c454c858f995a  skills/spirit.md
74f081762e99bf3b800749982911edf9f5f5bcc5d384a9f49f477292a94610d5  skills/trial-presentation-book.md
33f2badf061c2cd4df3f44bef2c3046087c83384bd439ed7ad22f51ef53c89a1  skills/trial-succession.md
f3c16b751d7f90480032c4f58d9c5a0effd1cc14f1eb2b9180da27e6a7e004f5  skills/compensation-book-distillation.md
62feb46fadf6d696a0e55053ac0b3d50a850ae260cf07f61988c5bae4b801f0d  roles.datom
```

curriculum-deploy (parent `4a3763e3`):

```text
5cf0c9114733036669b45a88e9388a271abf2017a2e960f6563620aeba26bebd  curriculum-deploy.ethos
e6beed47b0d681f854f4d68d18aa9928eb25b061f7a747a71473f07d731bc3a3  src/catalog.rs
b92c075863c53f7df4f25fca0b1e13f1abbdd6d3d92e5775a1cd977805b88313  src/generated.rs
c6fa91f4d997c8c374bfd54e3b9c8f2c6f53e7c0ce2f8f216d64be389e9572c4  src/roles.rs
47744de0f2ef04a216bcaed6d4bc93a9d0ce01152b3dbf3d01591b2378ae77a8  src/runtime.rs
dba057b9049872ca0f1b1f0d7d0be9cb308583c8c8b13bcd7d46e47418e315ed  tests/runtime.rs
11bdfc6cacaa29309fdd6e65b8562141607bbfaec918d193d62630c049e5d6da  tests/sources.rs
```

Primary authored/tool paths (parent `1822e4b7`):

```text
e9db1ec52624ec5fac50d781e70bf4cdb61ec10ee000b48724b47ab91bd29eaf  subagents/book.md
aa9147b43390373bcdcaf7c84793d04c290bbcc6460a591f116834dc13865930  tools/main-flow-mode/system-prompt.md
82c844ba0d33f56b1c97026ee356fbc99867bf721fcd5ef98f3ec187eb556832  tools/claude-main-flow-launch.mjs
d322b309215d915ebc22dd4da648219c17bba42e670b1958f2aa70132817bd04  tools/claude-main-flow-launch.test.mjs
d02b5f279aab43b504055f04e1565cc273f5e038525d7864de681e56f225fc7c  tools/codex-main-flow-launch.mjs
60233df7fea644f39327b4e02e3fed81ef69792463757995eaf8b653e2c63a3f  tools/codex-main-flow-launch.test.mjs
a477ba8a9851e64d8c7f0eaa5ba906dbbe01bdd93952f964898037ce63f844e9  tools/opencode-main-flow-launch.mjs
27cd8712cc09b745b878b655d272d3406702c3d1433db0b41c0050d4f6c52a87  tools/opencode-main-flow-launch.test.mjs
f37cbb803b7ca8edd36d0015e7ea401edb5b77e9a6c15557b48db34475b240d4  tools/standing-skill-selection.mjs
```

Primary generated projections are exactly the `SKILL.md` files for the
16 named Curriculum changes above under each of `.agents/skills`,
`.claude/skills`, and `.opencode/skills`; the generated role packets
are `.claude/agents/{book,read-demanding,read-ordinary,read-trivial,tester,write-demanding,write-ordinary,write-trivial}.md`,
`.codex/agents/{default,explorer,read-demanding,read-ordinary,read-trivial,tester,worker,write-demanding,write-ordinary,write-trivial}.toml`,
and `.pi/agents/{read-demanding,read-ordinary,read-trivial,write-demanding,write-ordinary,write-trivial}.md`.
Their source-to-output equality is the successful
`Check.{ … } → Checked.{ 105 24 }` result; no generated tree was
hand-edited.

Future pins are separate from this source manifest: publish Curriculum
and curriculum-deploy first, then advance Primary’s two flake inputs to
those resulting immutable revisions, regenerate Primary, and rerun the
same check. No future pin is selected by this candidate.
