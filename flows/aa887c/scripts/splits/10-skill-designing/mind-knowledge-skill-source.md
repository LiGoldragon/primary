{% raw %}
Target-specific text in a flat source uses `{% if claude %}`, `{% if codex %}`, or `{% if pi %}`, with `{% else %}` and `{% endif %}` alone on their lines; every other character is literal skill content.
{% endraw %}

`user-only: true` — the skill enters only through the user prompt or a
launcher's first turn; the flow cannot load it. It deploys as
`disable-model-invocation: true` in Claude Code, and in Codex as a policy
sidecar beside the skill that withholds it from the skills catalog.
