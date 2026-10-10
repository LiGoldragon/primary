# primary-psyche-medium v1 — the medium-effort psyche flow of the primary layer

Assembled by flow b49251 (the high-effort Fable flow) on 2026-09-16, on the
living's working instruction of that evening: "You should get a medium-effort
flow going in primary… Let's start uploading all of your work into that Opus
psyche. I'm going to talk to him, and he's going to talk to you about the whole
of everything."

Unlaunched packet. Nothing here has been started.

    python3 assemble.py                                    # index.datom + claude-base.md
    python3 claude-launch.py --cwd <independent-jj-clone>  # dry run, the default
    python3 claude-launch.py --cwd <independent-jj-clone> --launch

## The flow

| | |
| --- | --- |
| name, remote control | `primary-psyche-medium` |
| model | `claude-opus-4-7[1m]` (the old Opus) |
| effort | `medium` |
| base | `claude-base.md`, installed with `--system-prompt-file` (replaces the whole system prompt) |
| first prompt | `first-prompt.md`, the first user turn |

## How the base is built

The composer is the one from `origin/proposal/f55ec8-model-flow-anatomy`
(`anatomy/compose.py`), vendored here unchanged together with `datom_read.py`
and `index_read.py`. `index_read.py` carries one additive extension by this
flow: `Role` gains a third kind, `Psyche.Effort` over `Low | Medium | High`,
so the role name `psyche-medium` can be spoken, for the three effort levels the
living named (`sources/b49251/vision/psycheFlows.md`, "Three levels of psyche
flows, low, medium and high effort"). The extension was regression-checked
against the proposal: with it in place, `compose.py 'Compose.{ primary-main
claude … }'` still reproduces the launched v6 base at 433,525 bytes,
sha256 `cb93d3d4e8778ff2206935b6feb7d656fab372d9a7bf5a77e1e5b77c94fed41f`, and
`compose.test.py` is green.

`assemble.py` writes `index.datom` from the frozen bodies under `modules/` —
hashes computed from disk, never transcribed — and then calls `compose.py` with
`Compose.{ «psyche-medium» «claude» «claude-base.md» }`. The modules are not
fetched at assembly time; `modules/` is the frozen snapshot.

Order of the composed base, which is the order the living asked for:

1. the Authority line, alone, first;
2. `modules/header/identity.md` — who this flow is, its role in the living's
   own words, and the cluster around it (b49251 session b492510d, address
   primary-claude-successor-f55ec8 [5e4984]; Codex pair d9961c thread 01a0aacb,
   cf7879 primary until a recorded handoff; secondary 57a7aa / 348e7b; core
   e43002);
3. `modules/header/harness-rules.md` — EnterWorktree before edits, the
   classifier's refusals and the orders-file route, worktree isolation's refusal
   of complex substitution, one send per subflow, the per-harness model stacks,
   refresh at thirty percent, no reset credit on its own word;
4. thirteen complete skill bodies, byte-exact from
   `/home/li/wt/github.com/LiGoldragon/Curriculum/efa157-branches/skills/`
   (behavior, claude-harness, correction, edit-coordination, main-flow, nexus,
   prompt-crafting, psyche-interraction, psyche, spirit, subflow, testing,
   vocabulary), each wrapped with its Curriculum location;
5. Spirit;
6. all six Intent files from primary `main`;
7. all twelve top-level Vision files from primary `main`;
8. `## Frozen current context`, then the frozen lane sources:
   - `sources/b49251/` — this lane whole from `origin/flow/b49251` at 67720498:
     log.md, branches.md, the nine vision files, the three reports (the idea
     book, the idea-book index, readiness) and the one brief;
   - `sources/f55ec8/` — its ten vision files, and handoffToSuccessor.md,
     the five ideaBook-*.md, distillationProposal.md, messagingBrief.md;
   - `sources/efa157/` — its twenty-seven vision files and
     ordersToCodex-2026-09-16.md.

103 modules compose into the base: 4 header, 13 skills, 86 sources.

## What is not verified here

- The packet has not been launched, and the `--effort` value has not been
  witnessed taking effect in a running session; the launcher only records that
  the flag exists on this CLI.
- The dry run's daemon-record figure is a bounded model with a 64 KiB reserve,
  not a measured record. The actual record must be read after a dispatch.
- Complete skill bodies in the base are packaged inputs, not a skill-loader
  receipt, and child inheritance of a replaced base remains unproved.
- `modules/sources/spirit/spirit.md` is carried forward from the v7 packet
  (`flows/f55ec8/handoff/successors-v7/sources/spirit/spirit.md`), which is the
  Spirit the launched v6 and v7 bases carry. It is not a file on primary `main`,
  and its upstream authoring source was not re-derived here.
