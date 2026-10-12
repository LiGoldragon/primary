# Our program and its user unit. Field supplies immutable qualified inputs and installs only this unit.
# Herdr's source, server unit and existing panes are not changed here.
{ pkgs, lib, settings, systemPrompt }:
let
  source = builtins.path {
    path = ./.;
    name = "primary-committer-restarter-source";
    filter = path: type: type == "directory" || builtins.elem (baseNameOf path) [ "restart.mjs" "restart.test.mjs" ];
  };
  program = pkgs.writeShellApplication {
    name = "primary-committer-restarter";
    text = ''exec ${pkgs.nodejs}/bin/node ${source}/restart.mjs "$@"'';
  };
  # Guard immediately before exec, clear inherited hook/native identity, then run the pinned normal wrapper.
  # Field must declare this one literal executable in the supported Codex allowlist, preserving existing entries.
  resume = pkgs.writeShellApplication {
    name = "primary-committer-resume";
    text = ''
      : "''${PRIMARY_COMMITTER_RECOVERY_CONFIG:?missing accounted recovery config}"
      ${program}/bin/primary-committer-restarter --guard "$PRIMARY_COMMITTER_RECOVERY_CONFIG" -- "$@"
      unset PRIMARY_COMMITTER_FLOW_ID CODEX_THREAD_ID
      exec ${lib.escapeShellArg settings.nativeWrapper} "$@"
    '';
  };
  immutableSystem = builtins.path { path = systemPrompt; name = "primary-committer-system.md"; };
  configFile = pkgs.writeText "primary-committer-recovery.json" (builtins.toJSON (settings // {
    systemPrompt = toString immutableSystem;
    resumeExecutable = "${resume}/bin/primary-committer-resume";
    resumeArgs = map (arg:
      if lib.hasPrefix "model_instructions_file=" arg
      then "model_instructions_file=${builtins.toJSON (toString immutableSystem)}"
      else arg
    ) settings.resumeArgs;
  }));
  check = pkgs.runCommand "primary-committer-restarter-tests" { nativeBuildInputs = [ pkgs.nodejs ]; } ''
    node --test ${source}/restart.test.mjs > "$out"
  '';
in {
  inherit program resume configFile check;
  unit = {
    Unit.Description = "Recover the sole Primary committer through Herdr's existing API";
    Service = {
      Type = "simple";
      ExecStart = "${program}/bin/primary-committer-restarter --watch ${configFile}";
      Environment = [ "PRIMARY_COMMITTER_RECOVERY_CONFIG=${configFile}" ];
      WorkingDirectory = settings.primary;
      UMask = "0077";
      # Unknown launch/registration outcomes require exact disposition, not a second automatic client.
      Restart = "no";
      KillMode = "process";
    };
    Install.WantedBy = [ "default.target" ];
  };
}
