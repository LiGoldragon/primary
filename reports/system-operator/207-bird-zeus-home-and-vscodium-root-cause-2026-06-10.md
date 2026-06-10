# Bird Zeus Home and VSCodium Root Cause — 2026-06-10

## Scope

Read-only diagnosis after the failed `bird` Home redeploy on `zeus` and the VSCodium command/open-folder issue.

## Deployment root cause

The `HomeOnly ... Activate` from the operator machine failed before activation because the Home generation contained locally built outputs with no Nix signatures. Both `ouranos` and `zeus` have `require-sigs = true`, and `zeus` trusts the cluster public keys, but unsigned local outputs are still rejected during `nix copy --to ssh-ng://root@zeus...`.

This is not a missing trusted public key on `zeus`. The specific failed outputs existed locally and had an empty signature list. They were absent on `zeus`.

The triggering shape was the request using `builder None`. In `lojix-cli`, `builder None` means `BuildLocation::Dispatcher`; the copy code then performs `nix copy --substitute-on-destination --to <target> <closure>`. The code comment already names the limitation: substituted cache paths arrive signed, but raw daemon-to-daemon transfer of dispatcher-built paths is unsigned and will be rejected by `require-sigs = true`.

There is a second blocker behind that one: this operator machine can SSH to `root@zeus`, but not to `bird@zeus`. `lojix-cli` Home activation runs the profile and activation steps over SSH as the requested Home user. Therefore, even if the signature issue were avoided, the current operator path would likely fail at the user-SSH activation step unless `bird@zeus` authentication is available or the deploy mechanism changes.

The local-on-target activation attempt did not activate anything; it failed before activation. That path is now explicitly avoided in operator behavior.

## VSCodium root cause status

The normal `bird` VSCodium profile still has the Claude, Codex, Pi, and VisualJJ extensions installed, and normal VSCodium processes include active Claude/Codex children. The clean test window fixed the command/open-folder behavior because it used a throwaway profile with extensions disabled. Therefore the missing Claude/Codex UI in that clean window is expected, not evidence that the declared extensions are gone.

The VSCodium issue is narrowed to the normal VSCodium runtime state rather than the base VSCodium binary alone. The clean test changed two variables at once — clean user data and disabled extensions — so the precise root is still one of:

1. stale/corrupt normal VSCodium user-data state;
2. an extension interaction in the normal profile;
3. a normal launcher/runtime difference, such as XWayland versus the native Wayland/Ozone test.

The live normal profile also has a blank VSCodium window beside the real workspace window, matching the user-observed “Open Folder selects then nothing happens” symptom.

## Safe next fixes

For Home deployment, do not repeat `HomeOnly Activate` locally as `bird` on `zeus`. Safer options are:

1. fix `lojix-cli` so remote Home deploys never copy unsigned dispatcher-built outputs to a signature-enforcing target;
2. build the Home closure on the target or a signing/cache-publishing builder through the authorized operator path;
3. fix the Home activation transport so operator-initiated activation does not require unavailable direct `bird@zeus` SSH credentials, or provision the intended credential path explicitly.

For VSCodium, the next discriminator is to test the normal profile with extensions disabled, or a clean profile with extensions enabled, rather than redeploying blindly.
