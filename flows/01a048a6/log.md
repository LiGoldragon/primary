# Flow 01a048a6

Remember 01a04881 and present a proposal to fix the CriomOS slop causing the living grief.

Settled by current code read:
- `AgentIntercomGraphical` gates no AgentIntercom implementation. It gates OS graphical prerequisites (AT-SPI, uinput, WLR portal configuration), user uinput membership, and Home desktop applications/handlers plus their platform assertion.
- The AgentIntercom package already exposes alternate wrapped Codex and Claude command names without replacing the ordinary executables.
- Edge already owns the general graphical substrate; remote control already follows its independent `size.min` policy.

Approved realization scope:
- Delete the Graphical and Local AgentIntercom node-service gates rather than renaming the composite.
- Make AgentIntercom alternate wrappers/integration available without a node capability gate.
- Derive generic graphical facilities from Edge; derive desktop apps from Edge plus the cumulative Medium size threshold and local package-platform support.
- Remove obsolete Horizon/schema/data consumers and prove the migration across CriomOS, CriomOS-home, and Goldragon.
- Merge every affected repository on main, then deploy and verify Ouranos and Zeus.
- Refined during realization: AgentIntercom follows the presence of canonical Claude/Codex packages; desktop apps remain Edge plus cumulative Medium, with the unjustified shared x86 gate removed. Bring every affected repository through tested main integration.

Open:
- Deploy and verify Ouranos and Zeus once an authoritative deployment selection exists.

Integrated on main:
- horizon-rs `c70915eb550f729996e0921069b34d7844c9b2e9`
- goldragon `5bc563bf9507b65a8b6ab5cf537ee6413a96a4ca`
- lojix `33b8b6b7e5f893278a27c77130e8542072addda0`
- CriomOS-home `1274c581a51172d4fc53455e0c0cbd761215006b`
- CriomOS `45e83fbc29497208414ca5a08587d28a8e9617f2`

Deployment preflight block:
- No authoritative `manifests/*.dotos` selection supplies the required explicit store/SSH transport, builder, selector, and input mode for Ouranos and Zeus.
- Current Lojix node queries omit those request fields, retained event ranges are empty, `Query.ByDeployment` fails at the frame boundary, and `CheckHostKeyMaterial` is a stub returning empty material.
- No deployment request or runtime mutation was submitted.

Working hypothesis from the living: `AgentIntercomGraphical` may not concern AgentIntercom at all; verify whether it is actually an Edge-node concern under an unrelated name.

Remembered: 01a04881 — depth 2
The flow’s final model response and its carried witnesses were read. The old gate bundled agent-specific GUIs with generic graphical prerequisites, while Edge already expressed general desktop identity; Bird’s absence was the intended projection, not a witnessed activation failure. The prior flow left the correct application projection and the underlying cause of its own slop unresolved.
