# Pi Harness Defaults And Extension Packaging

## Result

`CriomOS-home` now declares Pi as the practical GPT harness path instead
of relying on hand-edited `~/.pi/agent/settings.json`.

Implemented in `/git/github.com/LiGoldragon/CriomOS-home`:

- `modules/home/profiles/min/pi-models.nix`
  - default provider: `openai-codex`
  - default model: `gpt-5.5`
  - default thinking: `xhigh`
  - enabled remote choices include `openai-codex/gpt-5.5` and
    `openai-codex/gpt-5.4-mini`
  - local `criomos-local/*` models remain enabled
  - default theme: `criomos-dark`
  - `doubleEscapeAction = "tree"` so Pi's built-in session tree/rewind
    path is the default escape action
  - packages: `pi-criomos`, `pi-linkup`, `pi-subagents`
- `packages/pi-subagents/default.nix`
  - Nix packages `pi-subagents` `0.25.0`
  - Provides the `subagent` tool, builtin agents, skills, prompt
    workflows, parallel/chain execution, and async/background status
    artifacts.
- `packages/pi-criomos/default.nix`
  - Nix packages `criomos-dark` and `criomos-light` Pi themes.
- `checks/pi-harness-profile/default.nix`
  - Asserts the packaged subagent extension exists.
  - Asserts both themes exist and carry all 51 required Pi color tokens.
  - Asserts the profile still declares GPT-5.5/xhigh, GPT-5.4-mini,
    `criomos-dark`, session-tree rewind, and `pi-subagents`.

The active local home profile on `ouranos` was activated from the local
`CriomOS-home` checkout through `lojix-cli HomeOnly ... Activate`.

## Verification

Passed:

```sh
nix build .#pi-subagents .#pi-criomos --option warn-dirty false -L
nix build .#checks.x86_64-linux.pi-harness-profile --option warn-dirty false -L
nix flake check --option warn-dirty false -L
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Build None None)'
lojix-cli '(HomeOnly goldragon ouranos li "/git/github.com/LiGoldragon/goldragon/datom.nota" "path:/git/github.com/LiGoldragon/CriomOS-home" Activate None None)'
pi --model openai-codex/gpt-5.5:xhigh --no-session --no-context-files --no-tools -p 'Reply exactly: pi-ok'
pi --no-session --no-context-files --no-tools -p 'Reply exactly: default-ok'
```

The live Pi probes returned `pi-ok` and `default-ok`. The second probe
used the declared default settings after activation.

Current active settings witness:

```json
{
  "defaultProvider": "openai-codex",
  "defaultModel": "gpt-5.5",
  "defaultThinkingLevel": "xhigh",
  "theme": "criomos-dark",
  "packages": [
    "packages/pi-criomos",
    "packages/pi-linkup",
    "packages/pi-subagents"
  ]
}
```

`pi list` shows all three packages installed from
`~/.pi/agent/packages/`.

`pi --list-models gpt` shows `openai-codex/gpt-5.5` and
`openai-codex/gpt-5.4-mini`.

A Ghostty window was launched in `/home/li/primary` running `pi` for
interactive testing.

## Remaining Gaps

## Reconciliation With Third-Designer 20

I read
`reports/third-designer/20-pi-as-codex-replacement-design-2026-05-22.md`
after the implementation slice. The implemented v1 follows the
designer's core split:

- v1 is a `CriomOS-home` profile and extension bundle.
- v1 does not create a `persona-pi` triad, signal contract, or daemon.
- Ghostty is the first visible surface.
- Terminal-cell integration is a follow-up.
- Rewind is Pi's built-in session tree/fork surface, not a separate
  extension in this slice.

The implementation deliberately shipped the smallest useful bundle:
`pi-subagents`, `pi-linkup`, and the CriomOS themes. The larger
designer extension wishlist remains unimplemented:

- live system theme switching during an already-running Pi task
- model-status/footer polish
- working indicator/status-line extensions
- destructive-operation guards
- jj-aware checkpointing
- prompt customizer
- context compaction helpers
- `pi-agent-suite`

The biggest unresolved design point is theme switching. I shipped
static `criomos-dark` and `criomos-light` themes and selected
`criomos-dark` as the default, which fixes the immediate night-time
readability problem. It does not prove Pi can switch themes mid-task.
That needs a follow-up against Chroma or another system visual-state
source.

The second unresolved design point is default subagent autonomy.
`pi-subagents` is installed and available. I did not add a policy layer
that disables autonomous subagent use in the prompt. The workspace rule
still says agents only dispatch subagents when psyche explicitly asks.
For the current cluster-operator testing session, psyche explicitly did
ask for subagent capability.

The third unresolved design point is model inventory cleanup. The
designer report says to retire Qwen 3 and Qwen 3.5 and add Gemma and
Magistral. I left all existing `criomos-local` inventory models enabled
because that inventory comes from `criomos-lib` and changing it is a
separate large-AI catalog decision, not a Pi profile decision.

The fourth unresolved design point is Pi login/secrets. The active
subscription login works. I did not move Pi auth into sops or another
declarative secret substrate; doing that would be a separate credential
design and may be undesirable if Pi stores browser-backed subscription
state.

The existing Persona terminal-cell Pi smoke did not reach Pi. It fails
immediately with:

```text
terminal-cell-wait failed: unknown wait argument: --socket
```

That is a stale Persona/terminal-cell script interface, not a Pi auth,
model, theme, or package failure. The likely fix is to update
`persona/scripts/persona-engine-sandbox-terminal-cell-smoke` to the
current `terminal-cell-wait` argument shape. I did not edit `persona`
because another lane currently owns that repo.

There is still no `persona-pi` triad component. Today's change makes
the human-facing Pi harness usable and declarative. A future
`persona-pi` daemon should use Pi's `--mode rpc` surface rather than
driving the interactive terminal UI directly.

`pi-agent-suite` was not packaged in this slice. It is a larger package
with context projection, quota/footer features, advisor/council tools,
and more dependencies. `pi-subagents` is the sharper first package
because it directly covers the Codex-equivalent subagent gap and its
builtin agents inherit the Pi default model, now GPT-5.5/xhigh.

## Operator Notes

The current `jj` change in `CriomOS-home` is:

```text
pmrrqvkn home: package Pi harness defaults and extensions
```

It is not pushed from this lane.
