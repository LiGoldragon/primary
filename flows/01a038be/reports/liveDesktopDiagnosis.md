# Live Codex Desktop and Claude callback diagnosis

## Codex conclusion

The prior Codex Desktop wrapper was neither removed nor shadowed.  The active
profile still supplies `codex-desktop`, and that wrapper defaults to the same
shared llm-agents Codex `0.149.0` executable as the terminal.  The item opens
an application labelled ChatGPT because the maintained frontend package ships
`codex-desktop.desktop` with `Name=ChatGPT`; its observed Desktop version is
therefore consistent with that frontend rather than proof that shell `codex`
invoked an unrelated ChatGPT command.

The exact launcher item clicked was not captured during this read-only probe.
There is also no current profile-visible Codex desktop entry or Noctalia text
override to attribute it to.  Older Codex processes remain live alongside the
current one, so process identity cannot by itself associate a particular
window with an activation generation.

## Claude conclusion

The supported callback scheme declared by the installed package is `claude`.
The live default mapping names `claude-desktop.desktop`, but the corresponding
desktop file is absent from every active XDG application directory and from
their MIME databases.  GNOME's Open With chooser therefore has a default ID it
cannot discover as an application, which directly explains its No Apps
Available fallback after a `claude://` callback.  The Software affordance is a
generic chooser fallback; no Software process or installation action was
observed.

Browser focus remains unproven: Chrome is the configured HTTPS handler and
both Chrome and Claude are running, but no callback event was captured and no
focus-changing action was performed.  The callback's actual scheme is likewise
unobserved to avoid exposing OAuth query material.

## Smallest declarative repair proposal

In the existing medium graphical Agent Intercom block, keep
`claudeDesktopPackage` as the sole package source and add a Home-owned link:

```nix
home.file.".local/share/applications/claude-desktop.desktop".source =
  "${claudeDesktopPackage}/share/applications/claude-desktop.desktop";
xdg.mimeApps.defaultApplications."x-scheme-handler/claude" =
  "claude-desktop.desktop";
```

`modules/home/desktop-database.nix` already refreshes the user desktop MIME
database after link generation, so this reuses the existing mechanism rather
than adding a runtime override.  The proposed focused Nix check should build a
medium graphical profile in a temporary Home, materialize its generated
desktop file, run the existing desktop-database tool, and behaviorally verify
that the `claude` scheme resolves to `claude-desktop.desktop`.  It should also
prove the small/non-graphical profile lacks that handler entry.

This is a proposal only.  No source edit, authentication, URI opening, focus
change, or deployment was made.

## Sources

- [Live desktop diagnosis witness](../witnesses/liveDesktopDiagnosis.md)
- [Desktop deployment witness](../witnesses/codexDesktopDeployment.md)
- [Activation witness](../witnesses/codexHomeActivation.md)
- [Historical desktop packaging report](rememberedDesktopDeployment.md)
- [Recovered user deployment procedure](rememberedUserDeployment.md)
