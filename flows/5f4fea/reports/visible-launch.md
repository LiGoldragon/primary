# Visible Launch Proposal

Status: anatomy proposal only. No sessions, windows, shortcuts, manifest, launcher, or deployment is changed.

## Existing implementation

The existing Codex launcher is `codex-desktop resume <thread-uuid> <directory>`. It opens a Ghostty window backed by the persistent Codex app-server and classed `criomos-codex-desktop`. Claude has no declared equivalent launcher; current attachment uses `claude --bg` and `claude attach <id>` through the Claude daemon control socket. Existing `prompt-relay` addresses backend session IDs, not compositor windows.

No authored per-layer launcher, durable manifest, or window registry was found in the primary workspace.

## Launch-call ruling

The living ruled that loading skills one at a time and then sending the first prompt makes a separate model call for each input and is too expensive. A future launcher therefore needs one model call for the initial launch package. This report keeps two pending implementation alternatives:

- Native batch skill-interface inputs plus the handoff in one initial call.
- A harness-level system-prompt file supplied at launch, with the handoff in that same initial call. Whether this qualifies as a skill-interface input remains an open living question.

These alternatives are both pending; neither is selected, and neither is an implementation claim. The launcher remains an anatomy proposal.

## Proposed inputs

For each layer (`core`, `primary`, `secondary`, `tertiary`, `quaternary`), a durable record would contain:

```text
workspace
generation
Claude session id
Codex thread id
working directory
```

Ephemeral state would contain only owned compositor state:

```text
manifest generation
Claude window id
Codex window id
visibility
```

The backend tuple `(layer, generation, Claude session id, Codex thread id, directory)` remains the identity. Compositor window IDs are handles, not session identity.

## Proposed transitions

`show` reads the durable record, reconciles live compositor windows, launches only missing halves, places the pair on the layer workspace, and applies the half-width preset.

`hide` acts only on registered windows whose owner tuple still matches the layer and generation.

`refresh` publishes a new generation, retains the old owner tuple and window IDs until both old attachments are retired, then records new backend IDs and reconciles the pair. It must not discard old IDs before retirement.

## Layout proposal

The existing anatomy proposes five numbered Niri workspaces, one per layer, with Claude on the left and Codex on the right at the 0.5 column preset. This remains a proposal. Niri already has numbered workspace bindings and a half-width preset; five pair workspaces and the registry do not exist.

## Witnesses and historical identity

The earlier desktop snapshot witnessed Codex thread `01a0a5c3-82a5-79f3-a61a-e365f4fea54f` in window 116 on workspace 1 and a Claude process for session `692df856-1d8d-481f-9988-0840bf566509` in window 82 on workspace 13. The Claude session has since changed to `942914a6-93d5-41ba-95bf-fa98ee557b09`; therefore window 82 and the prior session mapping are historical, not current ownership. Window 116 is likewise a historical snapshot of the earlier Codex attachment. Neither witness proves keyboard focus. No new relaunch is authorized by this report.

The peer claim that core, tertiary, and quaternary Claude sessions are absent is retained as a peer claim, not a fresh launch instruction.

## Acceptance witness criteria

- The manifest identifies one exact backend tuple and generation per layer.
- Each registered window can be tied to its owning layer and generation.
- `show` does not duplicate an existing half.
- `hide` does not touch another layer's window.
- Refresh retires old windows before releasing their owner tuple.
- A fresh compositor query shows both pair windows on the intended workspace.
- Focus is reported separately from presence; a successful launch is not a focus witness.

## Open questions

1. What chord shape shows or hides each layer?
2. Is the primary Claude typing window the owned Claude window, or should a separate attachment be created?

Until those are answered, the launcher and registry remain unbuilt.

## Sources

- `/home/li/primary/flows/eae736/vision/sessionAccess.md`
- `/home/li/primary/flows/eae736/summary.md`
- `/home/li/primary/flows/eae736/log.md`
- `/home/li/primary/flows/692df8/log.md`
- `/home/li/primary/flows/6cc91b/reports/vmAnatomy.md`
- `/home/li/primary/flows/024bc7/tools/codex_wake.py`
- `/home/li/primary/flows/024bc7/tools/claude_inject.py`
