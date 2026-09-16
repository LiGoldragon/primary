# The model and flow anatomy

The living's order of 2026-09-16: "make the anatomy of all of these models and
the different flows that they can impersonate, and how the system prompt is
changed for that; actually implement that."

This directory holds it as a proposal.

- `modelFlowAnatomy.ethos` — the schema. Model, Harness, Temperament, Layer,
  SubflowKind, Role, Impersonation; Module, Wrap, Composition, Install; the
  Request/Outcome pair the CLI speaks and the Refusal enum it refuses with.
  Every impersonation row carries its Provenance: the vision file and the
  heading the living's words sit under.
- `index.datom` — the data filling that schema: 15 model rows, 18 impersonation
  rows, 111 modules, 16 compositions, 5 install rows.
- `modules/` — the base-context modules, one file each. `modules/sources/**`
  are the frozen lane sources of the launched v6 base, unchanged;
  `modules/header/**` are the nine paragraphs the v6 header already separated;
  `modules/role/**` and `modules/subflow/**` are this proposal's own.
- `compose.py` — the composer. One inline datom value, no flags.
- `seed.py` — how the modules were cut out of the v6 base (`--extract`), and how
  `index.datom` is emitted from the plan it holds (`--index`).
- `compose.test.py` — the tests. Wired as the Nix check `model-flow-anatomy`.

## Using it

```sh
python3 anatomy/compose.py 'Roles'
python3 anatomy/compose.py 'Verify'
python3 anatomy/compose.py 'Compose.{ primary-main claude «/tmp/base.md» }'
# -> Composed.{ Main.Primary Claude 433525 cb93d3d4… «/tmp/base.md» }
```

Then install the composed file at the harness's top stratum:

| harness | how | effect |
| --- | --- | --- |
| Claude | `claude --system-prompt-file <composed>` | replaces the whole system prompt |
| Claude | `--append-system-prompt-file <composed>` | adds to the end of the stock one |
| Codex | `-c model_instructions_file=<composed>` | replaces the base instructions |
| Codex | `developer_instructions` | a developer-role message beside them, never part of them |

The install rows in `index.datom` say the same thing in typed form, with the
stratum each lands in.

## Reproduction

`primary-main` on `claude` reproduces the launched v6 base byte-for-byte:
433525 bytes, sha256 `cb93d3d4e8778ff2206935b6feb7d656fab372d9a7bf5a77e1e5b77c94fed41f`,
the file at `/home/li/.claude/jobs/efa15708/tmp/v6/flows/cf7879/handoff/successors-v6-reviewed/claude-base.md`
that the primary Claude f55ec8 session runs under. The copy committed at
`origin/flow/cf7879 flows/cf7879/handoff/successors-v6-reviewed/claude-base.md`
is an earlier assembly of the same package (421338 bytes, sha256 `f7dcd650…`):
its `sources/efa157/log.md` and `sources/efa157/{,reports/}ordersToCodex-2026-09-16.md`
stop before the afternoon's entries. The launched file is the one seeded here.

## Refusals

The composer refuses, never guesses:

```
Refused.UnknownRole.«quinary-main»
Refused.UnknownHarness.«deepseek»
Refused.NoComposition.{ Sub.Checkup Codex }
Refused.MissingModule.{ «header/quota» «modules/header/quota.md» }
Refused.HashMismatch.{ «header/authority» <recorded> <actual> }
```

## What is not here

- The Codex `model_instructions_file` install path is recorded but has not been
  run live against a Codex session from this proposal.
- The third, open-source seat is chartered and not active: its model has no
  name, so `open-source-unnamed` carries the row and no composition.
- Codex compositions exist for the four main-flow roles only; the subflow kinds
  are witnessed on the Claude side.
- The per-version stock-module inventory of order 11 (the harness repositories'
  block-by-block stock context, and the diff check on a harness upgrade) is a
  separate deliverable; this directory is the replacement half of it.
