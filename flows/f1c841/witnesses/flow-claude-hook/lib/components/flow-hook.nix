# The Flow harness hook: one Claude Code command hook that reads the event
# Claude Code writes on its stdin and calls the `flow` CLI with one inline
# datom carrying that event's fields. It maps each event to the signal-flow
# operation that names it:
#
#   SessionStart -> ResolveCaller.None (7.0: the Nexus names the flow bound
#                   to the calling process; it carries no event field)
#   Stop         -> QueueTurnEnd.{ SessionId TurnId Some.TranscriptPath }
#                   (7.1: the pre-end wakeup)
#   anything else -> no call: signal-flow 7.x has no operation for it
#
# It never fails the harness: whatever Flow answers, it exits 0, and it
# writes one tab-separated record per event on stderr (event, datom, the
# client's exit code, the client's whole output) for whoever reads it.
{ inputs }:
{
  name = "flow-hook";

  forSystem =
    system:
    let
      pkgs = inputs.nixpkgs.legacyPackages.${system};
      flow = inputs.flow.packages.${system}.default;
    in
    rec {
      package = pkgs.writeShellApplication {
        name = "flow-harness-hook";
        runtimeInputs = [
          pkgs.jq
          flow
        ];
        text = ''
          input="$(cat)"
          field() { jq -r --arg f "$1" '.[$f] // empty' <<< "$input"; }
          # A datom string in guillemets: every glyph is content until the
          # closing guillemet, which is escaped with a backslash.
          quote() { printf '«%s»' "''${1//»/\\»}"; }

          event="$(field hook_event_name)"
          case "$event" in
            SessionStart)
              datom='ResolveCaller.None'
              ;;
            Stop)
              datom="QueueTurnEnd.{ $(quote "$(field session_id)") $(quote "$(field prompt_id)") Some.$(quote "$(field transcript_path)") }"
              ;;
            *)
              printf '%s\t-\t-\tno signal-flow operation\n' "$event" >&2
              exit 0
              ;;
          esac

          set +e
          reply="$(flow "$datom" 2>&1)"
          code=$?
          set -e
          printf '%s\t%s\t%s\t%s\n' "$event" "$datom" "$code" "$reply" >&2
          exit 0
        '';
      };

      command = "${package}/bin/flow-harness-hook";

      # The Claude Code settings that run the hook on three events, every
      # tool for PostToolUse. `prefix` is shell put in front of the command
      # (a scenario's witness tap); `suffix` follows it.
      settings =
        {
          prefix ? "",
          suffix ? "",
        }:
        let
          hook = [
            {
              hooks = [
                {
                  type = "command";
                  command = "${prefix}${command}${suffix}";
                }
              ];
            }
          ];
        in
        builtins.toJSON {
          hooks = {
            SessionStart = hook;
            PostToolUse = map (entry: entry // { matcher = "*"; }) hook;
            Stop = hook;
          };
        };
    };
}
