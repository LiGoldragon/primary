<!-- to-the-living:start -->
Presentation.{ «CriomOS: the desktop opens nothing on its own» }

# CriomOS: the desktop opens nothing on its own

```
     +------------------------+
     | a flow publishes a     |
     | new artifact           |
     +-----------+------------+
                 | asks
                 v
     +------------------------+
     | main thread with a     |
     | display?               |
     +-----+-------------+----+
           | no          | yes
           v             v
     +----------+ +--------------------+
     | no tab   | | settings.json env  |
     +----------+ | ARTIFACT_AUTO_OPEN |
                  +---+-----------+----+
                      | 0         | unset
                      v           v
                +----------+ +----------+
                | no tab   | | xdg-open |
                +----------+ +----+-----+
                                  | opens
                                  v
                           +--------------+
                           | a new Chrome |
                           | tab          |
                           +--------------+
```

### Proposal 1: CriomOS gets its vision · psyche-context › vision/criomos.md, a new file

+ ---
+ description: CriomOS, its hosts, fixes, hardware, services or desktop, is being designed or judged.
+ dependencies: [compensation-operating-system]
+ ---
+
+ ## CriomOS
+
+ CriomOS is a declarative operating system: nobody edits a file on a host.
+
+ A problem in CriomOS is fixed in CriomOS by a proper fix and a proper deploy.
+ Every hotfix in place is removed and replaced by that fix.
+
+ CriomOS is made more modular; an anatomy of it shows what should be taken out.
+
+ ## Hardware
+
+ CriomOS has a hardware type, so that it supports several kinds of hardware, the Libre M5 Linux smartphone among them; a module may be gated on it.
+ A fix that only some hardware needs is a value in the cluster data, marked by the chip or part that makes it necessary.
+ A library reads the cluster's list of its hardware and answers, by processor, model and variant, which fixes a computer needs.
+
+ ## Harnesses
+
+ The harnesses and their desktop apps are kept stock in at least one version, under their ordinary executable names.
+
+ ## Services
+
+ A new service lives in CriomOS.
+ A service is updated by bringing it up at its latest version.
+
+ ## Desktop
+
+ Nothing opens a tab in the desktop browser on its own.
+
+ ## Sources
+
+ d68c82 criomos
+ 9993b5 criomOsUpgrade
+ b05237 operational-criomosModularHardware

Ruling: land, amend, or reject.

## CriomOS-home › modules/home/profiles/min/codex-remote-control.nix

```nix
{
  config,
  inputs,
  lib,
  pkgs,
  horizon,
  user,
  hexis,
  ...
}:
let
  sizeAtLeast = (import ../../../../lib/horizon-user.nix { inherit lib; }).sizeAtLeast user.size;
  primaryWorkspace = "${config.home.homeDirectory}/primary";
  primaryWorkspacePointer = lib.replaceStrings [ "~" "/" ] [ "~0" "~1" ] primaryWorkspace;
  mediumEnabled = sizeAtLeast "Medium";
  edgeEnabled = ((horizon.node.behavesAs or { }).edge or false);
  desktopEnabled = edgeEnabled && mediumEnabled;
  birdTarget = user.name == "bird" && user.hasPublicKey && user.size == "Max" && config.home.username == "bird" && config.home.homeDirectory == "/home/bird";
  occupied = (config.home.username == "li" && config.home.homeDirectory == "/home/li") || birdTarget;
  codexCliPackage = config.criomos.corePackages.codex;
  # This server has an unregistered client attached.  It is frozen until that
  # client has moved; do not replace its executable with the current package.
  # The literal is the executable in the preserved live-unit receipt.
  occupiedCodex = "/nix/store/wdj0sc69r4n9is1idfb32vcx5739ijkh-codex-0.153.4/bin/codex";
  occupiedNextCodex = "/nix/store/zbznvqk2746igprz4753clizppww5551-codex-next-0.158.0-alpha.9/bin/codex";
  codexStable = pkgs.writeShellApplication {
    name = "codex";
    text = ''
      export CODEX_HOME=${lib.escapeShellArg "${config.home.homeDirectory}/.codex-next"}
      exec ${occupiedNextCodex} --remote ${lib.escapeShellArg "unix://${config.home.homeDirectory}/.codex-next/app-server-control/app-server-control.sock"} "$@"
    '';
  };
  codexRemote = pkgs.callPackage ../../../../owned-agents/codex/remote.nix {
    inherit codexCliPackage;
    endpoint = "unix://${config.home.homeDirectory}/.codex-next/app-server-control/app-server-control.sock";
  };
  claudeCodePackage = config.criomos.corePackages.claude;
  claudePermissionRequestHook = pkgs.callPackage ../../../../owned-agents/claude-code/permission-request-hook.nix { };
  claudeDesktopPackage =pkgs.callPackage ../../../../owned-agents/claude-desktop {
    inherit claudeCodePackage;
  };
  chatgpt = pkgs.callPackage ../../../../owned-agents/chatgpt {
    commandLineArgs = "--ozone-platform=wayland";
  };
in
lib.mkMerge [
  {
    home.packages = [
      claudeCodePackage
      (if occupied then codexStable else codexCliPackage)
    ];

    # Bypass still asks a human for the dangerous-removal check.  The
    # PermissionRequest hook denies it with a rewrite message and logs every
    # request to ~/.local/state/claude/permission-requests.jsonl.  Only this
    # event key is asserted; Herdr's SessionStart hook and other events stay
    # user state.
    home.activation.mergeClaudePermissionDefaults = inputs.hexis.lib.mkManagedConfig {
      inherit lib pkgs hexis;
      file = "$HOME/.claude/settings.json";
      declared = {
        permissions.defaultMode = "bypassPermissions";
        hooks.PermissionRequest = [
          {
            matcher = "Bash";
            hooks = [
              {
                type = "command";
                command = "${claudePermissionRequestHook}/bin/claude-permission-request-hook";
              }
            ];
          }
        ];
      };
      modes = {
        "/permissions/defaultMode" = "always";
        "/hooks/PermissionRequest" = "always";
      };
    };

    home.activation.canonicalizeClaudeWorkspaceTrust =
      lib.hm.dag.entryBefore [ "mergeClaudeWorkspaceTrust" ]
        ''
          claude_config="$HOME/.claude.json"
          workspace=${lib.escapeShellArg primaryWorkspace}
          if [ -f "$claude_config" ]; then
            if ${pkgs.jq}/bin/jq -e --arg workspace "$workspace" '
              (.projects | type) == "object"
              and .projects[$workspace] != null
              and (.projects[$workspace] | type) != "object"
            ' "$claude_config" >/dev/null; then
              temporary_config="$(${pkgs.coreutils}/bin/mktemp "$claude_config.XXXXXX")"
              ${pkgs.jq}/bin/jq --arg workspace "$workspace" \
                '.projects[$workspace] = { hasTrustDialogAccepted: true }' \
                "$claude_config" > "$temporary_config"
              ${pkgs.coreutils}/bin/chmod --reference="$claude_config" "$temporary_config"
              ${pkgs.coreutils}/bin/mv "$temporary_config" "$claude_config"
            fi
          fi
        '';

    home.activation.mergeClaudeWorkspaceTrust = inputs.hexis.lib.mkManagedConfig {
      inherit lib pkgs hexis;
      file = "$HOME/.claude.json";
      declared.projects.${primaryWorkspace}.hasTrustDialogAccepted = true;
      modes."/projects/${primaryWorkspacePointer}/hasTrustDialogAccepted" = "always";
    };
  }
  (lib.mkIf (sizeAtLeast "Min") {
    home.packages = [ codexRemote ];

    systemd.user.services.codex-remote-control = {
      Unit.Description = "Codex Remote Control app-server";
      Service = {
        WorkingDirectory = primaryWorkspace;
        # Keep this definition byte-for-byte compatible with the occupied
        # service.  A later role transition may replace it only after its
        # unregistered client is gone.
        ExecStart = "${if occupied then occupiedCodex else "${codexCliPackage}/bin/codex"} app-server --remote-control --listen unix://";
        UMask = "0077";
        LimitNOFILE = 524288;
        Restart = "always";
        RestartSec = "2s";
      };
      Install.WantedBy = [ "default.target" ];
    };
  })
  (lib.mkIf desktopEnabled {
    home.packages = [
      claudeDesktopPackage
      chatgpt
    ];

    xdg.dataFile."applications/claude-desktop.desktop".source =
      "${claudeDesktopPackage}/share/applications/claude-desktop.desktop";
    xdg.mimeApps.defaultApplications."x-scheme-handler/claude" = "claude-desktop.desktop";
    xdg.dataFile."applications/chatgpt.desktop".source =
      "${chatgpt}/share/applications/chatgpt.desktop";
    xdg.mimeApps.defaultApplications."x-scheme-handler/codex" = "chatgpt.desktop";
  })
]
```

### Proposal 2: every host's Claude opens no tab on publish · CriomOS-home › modules/home/profiles/min/codex-remote-control.nix

```nix
  permissions.defaultMode = "bypassPermissions";
+ # Every host: a publish opens no tab.
+ env.CLAUDE_CODE_ARTIFACT_AUTO_OPEN = "0";
```

Ruling: land, amend, or reject.

## field-context › compensation/book-crystallization.md

```markdown
A book shows current context modules and its crystallization proposals. Every proposal shows a word removed (red) or added (green) in a psyche module, or the code that line lands. A figure draws concepts as nodes linked by edges, with the forks, options and joins its subject has, each label a few words; its ASCII source is no wider than 52 characters. Nothing else is written.

Outside its proposals, a book shows only context modules as they stand, each under its repo › path; it has no prose sections of its own.

A changed figure is shown once, whole, in its new form.

A proposal heading reads `### Proposal N: repository › path`, followed by `, a new file` when the file is new. The heading names the location; no `File:` line appears in the body.

A page is built only by the book builder; a source it refuses goes back to its author.

Below the proposal heading, each removed line starts with "- ", each added line with "+ ", and unchanged lines around them with two spaces. Concise machine results and concrete blockers may be sent outside a book.

Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.

A proposed statement is drawn from the living's records read whole, with their exceptions and later statements on the same subject. A skill line in the author's brief shows where a statement lands, never what it says; the brief marks machine-skill text as the machine's. A count or date claim about the records is made only when the author has witnessed it.

A proposal to destroy or archive a record renders unmistakably apart from a landing: its own colour and a Destroy or Archive mark on the record it removes.

Before publishing, reconcile the relevant current direction and exclude what the living has voided. A new edition carries only what is unruled or changed since the living last read it; what he approved is landed, not shown again.

When the living's comments leave a topic open, a new book follows with the adaptation, or the inquiry, knowledge or compensation review it needs.

A proposed code change shows the value it sets on each host, not only the name it reads it from.

Every question in a book is one specific proposal: the exact lines it lands, in the named file, ruled land, amend or reject; a list of options without their lines is never asked.

Every figure in a published book is the Illustrator's drawing, passed to the builder with --figures; the builder's own drawing is never published.

A book puts vision to the living's ruling; the implementation of landed vision follows without a ruling of its own.

A diagram in a book's source is ASCII, no wider than52 characters; the published book never shows the ASCII, but a figure the Illustrator draws of the same idea by the illustration rules, free of the source's boxes and arrows.

A proposal's heading names the file it lands in, by repository and path.

A book has no technical part; technical references stay out of the book.

A book is published only when every proposal names the file it lands in and carries the lines it adds, and every other section shows a current context module under its location, with no technical part; any other source goes back to its author unpublished.

A book has no technical part; location headings identify the context modules and proposals.
```

### Proposal 3: a browser a book check starts ends with the check · field-context › compensation/book-crystallization.md

  Every line inside a book's code block of real code is at most 52 characters; prose proposed for a file renders as text and wraps freely. A code block spans the full page width, outside nested or indented layout columns; the code inside keeps its own indentation, never wraps inside a token, and scrolls sideways. A short code value inside a choice stays inline. Check every book at phone width before publishing.
+
+ A browser started to check a book exits when the check ends.

Ruling: land, amend, or reject.
<!-- to-the-living:end -->
