# proposal · flow-anatomy

*Flow 48cff7 · 2026-09-16 · pending living review*
*Kind: new skill*
*Source records: flows/48cff7/vision/flowAnatomy.md*

---

## description

Understanding, reading, or shaping a flow's custom harness system prompt.

## body

A flow's harness system prompt has a shared layer and a role block.

The shared layer carries the harness base, the project instructions (`CLAUDE.md`, `NON_MANAGEMENT_AGENTS.md`, `SKILL_VARIABLES.md`), the skills index, and the environment.

The role block, appended by the launch package, carries the role name, the effort tier, the stack, the layer, the authority scope, the peer sessions, the ad hoc skill body inline, and the Curriculum skills the role always loads.

The role block is what varies between flow types. Everything above it is identical.

When a role stabilises, promote its ad hoc skill body to a Curriculum skill and reference it by name in the launch package.
