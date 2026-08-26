## 01a03e02 — `log.md` embedded Code runtime observability

The earlier flow could not observe Claude Desktop's managed Code runtime through the supported package interface. A later Desktop local-thread failure exposed a concrete selected runtime in its error: `~/.config/Claude/claude-code/2.1.237/claude`. This makes that one downloaded runtime and version observable at failure time; it does not establish a supported external-runtime override or parity with the separately pinned terminal CLI.

The versioned executable also corrects the scope of the earlier statements that the Home change added no stateful installer: the authored Home configuration added none, but the deployed Desktop application later materialized executable software in user state. Under the recorded ruling in `vision/installingSoftwareStatefully.md`, local-thread support therefore has a design violation beyond its immediate NixOS loader failure.
