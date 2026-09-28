# Mind Astra launch, 2026-09-28

Workspace step (authorized by the main flow): in /home/li/primary, `jj git fetch` reported nothing changed; the working copy was empty (tuykplpx 43a0c53d on bc0ce6d4). The only processes with that cwd were the Codex app-server daemons (pids 1936, 1960, 9513). `jj new main` made kstrmyyz af68df32 (empty) on main c3d4c98652c6. jj skipped one update: two symlinks from July, reports/general-code-implementer and reports/SchemaTrainExpansion, which main tracks as directories, stay on disk as symlinks. They do not affect the launch.

Launcher run (once): `node /home/li/primary/tools/codex-main-flow-launch.mjs --model gpt-6-astra --brief /home/li/primary/flows/8904b1/launch/mind-astra-brief.md`

    workspace: /home/li/primary is the default workspace and holds main
    prompt: composed 49984 bytes from main into /tmp/codex-main-flow-launch-EIyBvx/first-prompt.md
    pane: FAILED: expected one Herdr workspace labelled primary, found 0
    exit=1

State left: no tab or pane created; no Codex session started; no first prompt sent; no Flow ID claimed; no title; no registration. Herdr session `default` after the run: workspace w1 labelled `56ae53` (it was labelled `primary` earlier today), panes w1:p8 and w1:pC only.

Rerun, if the main flow authorizes it: the same command plus `--herdr-workspace-label 56ae53`.
