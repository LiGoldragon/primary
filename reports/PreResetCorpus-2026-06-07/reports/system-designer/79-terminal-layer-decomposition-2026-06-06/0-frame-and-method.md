# 79.0 — Frame & method: who owns the terminal control/session surface?

Role: system-designer. Date: 2026-06-06. Variant: Psyche. Session unit: this directory.
Ultracode session.

## How we got here

Reports 77/78 mis-framed the terminal layer; two psyche corrections fixed it:

1. terminal-cell lacking triad deps is a **timing artifact** — the triad engine didn't
   exist when terminal-cell was written — not evidence it's inherently non-triad.
2. terminal-cell is an **abduco-style per-application attached wrapper process**
   (one child + one PTY + transcript, persisting only for viewer detach/reattach), and
   **instance management belongs to `orchestrate`**, not a dedicated daemon. Confirmed:
   process-per-application, the abduco model. Captured as Spirit `bcca`.

That settles the *cell*. It opens the real question the psyche then raised:

> *"I don't see why it needs a daemon … and we have the orchestrate component to do the
> instance management. Or maybe it's 'harness' (renamed from persona-harness) or
> 'terminal' (renamed from persona-terminal — but after the rename I think 'terminal' is
> too ambiguous — but I don't know if we even want that component)."*

## The question this report answers

If terminal-cell is just an abduco wrapper process and orchestrate manages its instances,
then **who owns the terminal control / session surface** — session naming + registry,
viewer-adapter launch policy, input-gate + injection policy, prompt-pattern lifecycle, the
`signal-terminal` control plane, durable session metadata? Three candidates the psyche
floated, all uncertain:

- **(A)** a dedicated session-owner component (currently `terminal`, but the name is now
  ambiguous post the persona-terminal → terminal rename);
- **(B)** fold the surface into **harness** (renamed from persona-harness);
- **(C)** no dedicated component — dissolve into orchestrate + harness + the cell.

A load-bearing complication: a terminal-cell can wrap **any** program (shell, editor,
build), not only an AI harness — so folding everything into `harness` may orphan
non-harness terminals.

## Method (workflow `terminal-layer-decomposition`)

Two phases. **Read** (4 parallel): orchestrate's instance-management scope (can it
spawn/track/retire wrapper processes?); harness's scope (is a harness ≈ an AI program in a
cell? could it own the surface? what about non-harness terminals?); terminal's current
responsibilities (mapped generic-vs-harness-specific, plus the naming problem); and the
recorded intent + relationships (the persona-* renames, the agent abstraction `w4jp`/`gdbf`,
`tq18`/`mazv`). **Decompose** (1 architect): map each responsibility to its best owner;
lay out options A/B/C + hybrids with tradeoffs; recommend; propose names; specify exactly
how orchestrate manages cell instances.

## Output

`1-the-decomposition.md` — the responsibility map, the options, the recommendation, the
naming proposal, the cell-management mechanism, and the residual decisions for the psyche.
Raw per-agent detail in workflow transcript `w2qcp5qxh` / `wf_25cdf9cc-8ce`.

## Discipline

Read-only on `/git`. The firm intent (`bcca`) was captured before this research; the
ownership question is explicitly carried OPEN (the psyche is unsure) and is resolved by
proposal here, captured to Spirit only after the psyche chooses.
