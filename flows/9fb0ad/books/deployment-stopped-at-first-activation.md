Presentation.{ «The deployment stopped at the first activation» }

Your word this morning: "Everything can get deployed: all of this messenger, apparently, the new flow, the new orchestrate. I want all this deployed, made as the regular version in [CriomOS] in our home." -- psyche, STT, 2026-10-03, to Psyche Fable f1c841.

## 1. Where it stopped

f1c841 built the regular-slot Home generation (orchestrate 0.37, flow 0.23, message 0.19 as the regular units); the build succeeded at 06:53 and the commit is pushed as a branch. This seat then ran the first of the three planned activations. It failed before touching any Nexus, in a Home step that has nothing to do with the deployment: the messenger guard. The profile was restored to the generation you have been running since Sep 30; every Nexus runs its old version; the messenger works for every seat. The orchestrate Nexus was stopped and restarted once, on the same binary and store, unreachable for about eight seconds. Nothing was merged. A copy of the orchestrate store was taken before the attempt.

## 2. Why: the messenger guard refuses every activation now

Your home configuration carries a step that refuses to replace `~/.local/bin/messenger-clj` and the `hm-*` links unless they point into one specific, pinned set of files from an earlier generation. Since the Sep 30 activation they point into that generation's own files, so the guard refuses every activation — the three new generations and the rollback target alike. Rollback worked only by moving the profile pointer by hand. f1c841's tests ran the Nexus binaries directly and never an activation, so they could not catch it.

What the guard protects — in its commit's own words — is being read now; a fix is being prepared on a branch, built, activated nowhere, so that one number from you suffices.

## 3. The fix proposed

The guard admits a link that points into the generation being replaced (Home Manager names it to the activation) or into the current profile's files, and still refuses a link pointing anywhere else. After it, the three generations are rebuilt on the fixed commit and the activation runs again from step 1, in the order the night's reports give, with the same rollback. The `claude` wrapper's bypass (point 2.5 of «The night, for your word») stays untouched.

## 4. Your choices

1. Fix the guard as proposed, rebuild, activate all three, land CriomOS-home main.
2. Fix the guard, rebuild, and activate only orchestrate 0.37 first; Flow and Message after you see it run.
3. Remove the guard altogether.
4. Stop here; leave the Home as it is.

Also: 5. delete the orphan generation 1040 the failed activation left; 6. keep it.

Name the numbers.
