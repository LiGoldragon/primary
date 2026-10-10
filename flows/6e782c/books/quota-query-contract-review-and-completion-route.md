# Quota query: contract review and completion route

From Mind Astra d66c26, 2026-10-03.

### 1. Finish the native request path

Secondary Opus reports working collectors and successful tests, but the CLI and daemon still use an older contract that cannot carry the new query.

The completion route is to migrate Harness and its affected callers to the current contract together, removing the temporary second contract dependency.

### 2. Use the existing daemon

Install the existing Harness daemon as a user service. Keep one CLI call as its typed client, with private user sockets and a matching client/daemon build.

The query needs no interactive model session, stored accounting history, or polling timer.

### 3. Preserve what the sources actually say

Equal reset times do not establish equal quota windows. Credits, extra allowance, spend controls, and source failures must remain visible.

Hundredths of a percent are acceptable when labeled. Unknown context capacity stays unknown, and a name containing a flow ID is not a verified session binding.

### 4. Completion instructions are ready but held

The review and completion plan are published. Acceptance still requires the installed CLI request, independent tests, and a bounded live result through the daemon.

Messenger held the completed instructions because Secondary Opus **28d847** is marked blocked. Nothing was typed. Please resume that seat or name another active Opus main flow to receive them.
