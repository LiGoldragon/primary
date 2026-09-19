# Model roles

## Opus is two seats, not one model

The older Opus is the wiser seat. The newer Opus is faster and blinder, and
good at getting work done.

## Thinking, design and psyche interaction run on the older Opus or the newest Fable

They do not run on the newer Opus.

## The older seat's work is consideration and qualitative audit

Comparing vision is such an audit. The older seat also does the thinking for
a Fable or older-Opus session flow.

## The older seat is chosen for disposition, not capability

What is wanted is the model most likely to resist the temptation to act and
instead question, doubt, or seek clarification; to understand the unspoken
part of a design; and to reword and represent it back to ask whether that was
the meaning. The purpose is alignment of vision.

## The older seat is Opus 4.6, and its million-token version is Max-only

The default for psyche-medium Claude is Opus 4.6. Opus 4.6 has a
million-token-context version, and the Max subscription is the only
subscription that can use it, so a declaration never assumes the
million-token version is available to every operator.

Callable ids witnessed for the older seat:

    claude-opus-4-6
    claude-opus-4-7

each also in a `[1m]` form. The bare alias resolves to the newest Opus:

    claude --model opus          # takes whatever Opus shipped most recently
    claude --model claude-opus-4-6[1m]   # names the seat

## The lower layer's main flow is the older Opus

On the Codex side it is the latest Sol. At the higher layer it is Astra.

## Delegation ceiling

Each tier has a ceiling on what subflows it may launch. Conservative by
default: prefer the lower tier.

### Codex side (energy tiers)

Luna launches only Luna. Terra launches Terra or Luna, not Sol. Sol is not
launched lightly; it is getting expensive. Astra launches Sol, Terra, and
Luna — try Terra and Luna first. Astra is main-flow only: no flow ever
launches an Astra subflow.

### Claude side (model names)

Haiku is ultra-low power. Sonnet launches Sonnet and Haiku. Opus launches
Sonnet and Haiku, and sometimes Opus, but rarely. Fable launches Opus and
Sonnet often, and Haiku for small jobs. Fable is main-flow only: no flow
ever launches a Fable subflow.

## One declaration sets the model everywhere

The model is declared once, as typed configuration in Flow, mutated only
through the meta wire. Skill variables carry that value by name into every
skill, launcher and brief. Nothing else holds a model name, so a launcher
never writes one by hand and no flow is born on a seat by accident.
