# Main-flow refresh witness

The final authored diff replaces only the former Flow-refresh paragraph in
`skills/main-flow.md`. It includes the corrected spelling: a newer flow holds
its `Flow`; a successor takes its predecessor's `Flow`; the other `Flows` are
untouched; and orchestrate books which flows hold which `Flows`.

Before the capitalization-only correction, the fresh native behavioral test
ran with this receipt:

`timeout 180s codex exec --ephemeral -m gpt-5.6-luna -s read-only -C /home/li/primary -o /tmp/main-flow-refresh-fresh-test.txt '$main-flow …'`

It received `/home/li/primary/.agents/skills/main-flow/SKILL.md` in a
read-only sandbox and returned these data-only decisions: builder at 80% did
not restart; main flow at 60% restarted; dramatic change at 15% restarted;
ordinary shift at 15% did not restart; a newer flow holding the current Flow
redirected the living. It performed no flow mutation. This witness predates
only the capitalization correction, so the behavioral decisions were not
rerun.

After the correction, native generation returned `Generated.{ 44 21 }` and
`nix run .#check-skills -- 'Check.{ «/tmp/curriculum-main-flow-refresh» «/home/li/primary» }'`
returned `Checked.{ 44 21 }`.
