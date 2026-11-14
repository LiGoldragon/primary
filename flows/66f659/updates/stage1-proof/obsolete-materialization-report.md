# Obsolete stage-one materialization 542

Deployment 542 was admitted before Opus superseded Home `f64f24d805eed9e5a9d001384524c4b5ba1df480` and consumer `163a9be4854363183bcab4ff4ca2f86cd60c787e`. It was therefore allowed to finish only as an obsolete, non-activating proof.

- Watcher 70 was acknowledged before submission.
- Lojix admitted deployment 542 at marker 12982.
- The watcher observed Submitted, Building and `Completed Some.Succeeded` at marker 12997.
- One post-terminal `Query.ByDeployment` confirmed `UserEnvironment.Realize`, `ProfileOnly`, `RequireImmutable`, revision `163a9be4854363183bcab4ff4ca2f86cd60c787e`, Completed/Succeeded.
- The watcher was stopped at terminal.

The Home Manager profile, user profile, system profile, runtime system, and Lojix service PID/invocation were identical before and after. No activation, SetProfile, source main change, profile/boot/network/service action, further build check, or artifact handoff was performed. This proof is obsolete and grants no gate toward either main or any deployment.

Evidence is retained in `raw/watch.log`, `raw/admission.txt`, `raw/record.txt`, `pre-state.txt`, `post-state.txt`, `request.datom`, and `request.sha256`.
