---
title: 2 — Bird Zeus home profile redeploy
role: system-maintainer
variant: Handover
date: 2026-06-11
topics: [home-profile, zeus, deployment]
description: |
  Operational handover for Bird's Zeus Home Manager profile redeploy:
  reachability, activation path, conflict resolution, and remaining service issue.
---

# 2 — Bird Zeus home profile redeploy

## Intent Anchors

[For Crayon OS host maintenance, the maintainer has root SSH access on all cluster hosts but cannot SSH as Bird on Zeus; Bird's Zeus home-profile redeploy must use an existing root or maintainer-user path rather than direct Bird SSH.]

## Outcome

Bird's Home Manager profile on Zeus is redeployed to the current `CriomOS-home/main` profile. The profile now points at `home-manager-11-link`, and the user systemd manager reports no failed units in the final broad check.

The direct `bird@zeus` SSH path still fails, matching the access constraint. The successful path is root SSH to Zeus plus commands executed as Bird with Bird's live user-session environment.

## What blocked the normal path

The old lojix `HomeOnly` activation path expects remote user SSH for `Profile` and `Activate`. That cannot work for Bird on Zeus because Bird SSH is unavailable.

An earlier Zeus build-only run existed, but it stopped before activation. The build log also showed Prometheus cache timeouts at that time, so the earlier failure likely combined host reachability/cache instability with the missing user-SSH activation path.

## What changed during activation

Activation first failed at `installPackages` because Bird had a mutable `nix profile install` entry for `cameractrls`, while the current Home profile now declaratively owns `cameractrls`. I removed only the conflicting mutable `cameractrls` profile entry and reran activation. Unrelated mutable user profile entries remained.

The second activation completed successfully. It linked the generation, rebuilt bat caches, merged user settings, reloaded user systemd units, started the current Home-managed services, and applied the UI-priority oneshot.

## Remaining observation

`whisrs.service` restarted during activation and its journal showed failures to retrieve `openai/api-key` from Bird's password store. That is not a deploy-blocking profile issue, but it is a runtime service issue for dictation. The final broad `systemctl --user --failed` check did not list failed units, but spot checks showed `whisrs.service` could cycle through auto-restart states. Treat Whisrs as needing a follow-up secret/runtime check before calling dictation healthy.

## Durable lesson

Root-mediated Home activation is a valid maintenance path when target-user SSH is absent: build on the target or otherwise realize the closure on the target, set the user's Home Manager profile as that user, and run the activation package as that user with the live `XDG_RUNTIME_DIR` and D-Bus address.
