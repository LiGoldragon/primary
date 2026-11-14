# b7c publication evidence

## Authority

Original user launch order, verbatim:

> Your component is the repository /git/github.com/LiGoldragon/belief-nexus (if it is not there, find it under /git). Loop: read the implementation, find bugs, fix them, build green (its own nix flake check or cargo test as the repo uses), commit and push, report one line naming the bug fixed and the commit; then go again.

> Everything lands without the living's review.

Primary's later bookkeeping handoff authorized preserving and identifying qre/2eh/95g evidence in a bookkeeping commit, not source publication or policy approval. No separate Opus/Core b7c design ruling is asserted. Six policy proposals (92q, 4ax, 1t7, a5u, dfn, dzs) remain unapproved.

## Corrected chronology

The implementation flow's transcript audit reports: bookkeeping 50e5b27 was committed/pushed before the hold. The hold reached the worker after source commit-lock acquisition but BEFORE source staging/commit/push. The worker misread the hold and published c537aec afterward. Earlier claims that source publication preceded the hold were incorrect and are retracted. No tool wall-clock timestamp was exposed for those message/tool boundaries.

Git commit metadata (not push timestamps): 50e5b27 at 2026-11-04T21:02:10-06:00; c537aec at 2026-11-04T21:02:32-06:00.

Further source publication is frozen. Commits and evidence are preserved. No forced revert or runtime alteration was requested or performed.

## Remote/ref and readback witnesses

Reported origin: git@github.com:LiGoldragon/belief-nexus.git. Local main tracks origin/main; pushed remote ref refs/heads/main.

- Pre-bookkeeping local readback: HEAD=origin/main=0c37874ba37d898639ccaeecb11c141d89b945c3.
- Bookkeeping server push output: `0c37874..50e5b27  main -> main`.
- Subsequent pre-source local readback: HEAD=origin/main=50e5b27a850777a9bfe7f083c478fb60c67acc3e. No immediate live ls-remote was recorded after bookkeeping.
- Source server push output: `50e5b27..c537aec  main -> main`.
- Immediate post-source local readback: HEAD=origin/main=c537aec8eaf6a4bea34ef022744d1df89283db97.
- Evidence-pass live ls-remote first recorded then confirmed c537aec8eaf6a4bea34ef022744d1df89283db97; local HEAD and tracking ref matched, status clean. There was no recorded pre-push live ls-remote.

## Exact revisions and bookkeeping scope

Source baseline: 0c37874ba37d898639ccaeecb11c141d89b945c3.
Bookkeeping-only child: 50e5b27a850777a9bfe7f083c478fb60c67acc3e; emission source unchanged.
Source child: c537aec8eaf6a4bea34ef022744d1df89283db97, parent exactly 50e5b27.

Bookkeeping IDs included qre, 2eh, 95g, dzs, b7c. qre/2eh/95g content and provenance were preserved: beliefNexus Secondary ae9a52 audit10 triage; psyche-belief691a9c5; auditedbe99dfb. Bookkeeping grants no implementation/acceptance to design-pending records.

The source diff changes only crates/emission/src/lib.rs (+66/-17). No a7x/707 source is included. It retains existing PublicationRefusal and PublicationOperation: requested path/identity validation stays StagingGeneration; existing candidate reads and manifest checks become InspectingManifest. Cleanup projects the same evidence. Tests cover missing/corrupt existing requested canonical candidate, unchanged structural/content tree, valid reuse, invalid-path staging control. Structural tree evidence covers paths, node kinds, file bytes, symlink targets; it does not assert unchanged atimes, permissions, ownership or xattrs.

## Green evidence and limits

Implementation flow command: `nix flake check -L --builders @/etc/nix/machines --max-jobs 0`.
Its transcript tool session 56823 ended `all checks passed!`. The check ran at HEAD 0c37874 plus the emission worktree content subsequently committed byte-for-byte as c537aec. Other dirty content was .beads bookkeeping; no a7x/707 source was present. Counts: emission 23, daemon 39, core 10, translator 11, pair 4, peer 4, process 2. No durable filesystem test log was saved; this claim is the implementation flow's transcript witness, not a newly executed check at clean commit c537aec.

No new build or audit was run for this handoff.

## Deployment

The implementation flow reports git commits/pushes and Nix flake checks only. It ran no deployment, activation, service restart, default package switch or runtime mutation. Whether external automation deploys these pushes is unknown; no such witness is held.

## Exact source diff

```diff
diff --git a/crates/emission/src/lib.rs b/crates/emission/src/lib.rs
index 1d377f6..a051f10 100644
--- a/crates/emission/src/lib.rs
+++ b/crates/emission/src/lib.rs
@@ -482,8 +482,7 @@ impl FileEmission {
         paths.prevalidate(publication)
             .map_err(|evidence| publication_refusal(publication, operation.clone(), evidence))?;
         let identity = publication.identity();
-        let existing = paths.resolve_publication(&identity)
-            .map_err(|evidence| publication_refusal(publication, operation.clone(), evidence))?;
+        let existing = paths.resolve_publication(&identity, &publication.workspace)?;
         let intended_manifest = publication.manifest();
         if existing.as_ref().is_some_and(|value| value.manifest != intended_manifest) {
             return Err(publication_refusal(publication, PublicationOperation::InspectingManifest, PublicationEvidence::ManifestMismatch));
@@ -539,12 +538,8 @@ impl FileEmission {
                 publication_evidence: evidence,
             })),
         };
-        if let Err(evidence) = paths.resolve_publication(&request.publication_identity) {
-            return Response::EmissionRefused(EmissionRefusal::Publication(PublicationRefusal {
-                workspace: request.workspace,
-                publication_operation: PublicationOperation::InspectingManifest,
-                publication_evidence: evidence,
-            }));
+        if let Err(refusal) = paths.resolve_publication(&request.publication_identity, &request.workspace) {
+            return Response::EmissionRefused(EmissionRefusal::Publication(refusal));
         }
         match paths.inspect_untrusted(&request.workspace) {
             Ok((pointer, manifest)) => Response::Inspected(PublicationInspection {
@@ -777,16 +772,22 @@ impl PublicationPaths {
         Ok(Some((address, manifest)))
     }
 
-    fn resolve_publication(&self, identity: &PublicationIdentity) -> Result<Option<ResolvedPublication>, PublicationEvidence> {
-        let legacy = self.legacy_directory(&identity.generation_id)?;
-        let publication = self.publication_directory(identity)?;
+    fn resolve_publication(
+        &self,
+        identity: &PublicationIdentity,
+        workspace: &signal_belief_nexus::Workspace,
+    ) -> Result<Option<ResolvedPublication>, PublicationRefusal> {
+        let staging = |evidence| inspection_refusal(workspace, PublicationOperation::StagingGeneration, evidence);
+        let inspecting = |evidence| inspection_refusal(workspace, PublicationOperation::InspectingManifest, evidence);
+        let legacy = self.legacy_directory(&identity.generation_id).map_err(staging)?;
+        let publication = self.publication_directory(identity).map_err(staging)?;
         if legacy == publication {
-            return Err(PublicationEvidence::ManifestMismatch);
+            return Err(staging(PublicationEvidence::ManifestMismatch));
         }
         let legacy_value = self.inspect_candidate(&legacy);
         let publication_value = self.inspect_candidate(&publication);
-        let legacy_value = legacy_value?;
-        let publication_value = publication_value?;
+        let legacy_value = legacy_value.map_err(inspecting)?;
+        let publication_value = publication_value.map_err(inspecting)?;
         let mut matching = Vec::new();
         if let Some((_, manifest)) = legacy_value {
             if manifest.identity() == *identity {
@@ -795,14 +796,14 @@ impl PublicationPaths {
         }
         if let Some((_, manifest)) = publication_value {
             if manifest.identity() != *identity {
-                return Err(PublicationEvidence::ManifestMismatch);
+                return Err(inspecting(PublicationEvidence::ManifestMismatch));
             }
             matching.push(ResolvedPublication { path: publication, manifest });
         }
         match matching.len() {
             0 => Ok(None),
             1 => Ok(matching.pop()),
-            _ => Err(PublicationEvidence::ManifestMismatch),
+            _ => Err(inspecting(PublicationEvidence::ManifestMismatch)),
         }
     }
 
@@ -949,7 +950,9 @@ impl PublicationPaths {
         target: &PublicationIdentity,
         workspace: &signal_belief_nexus::Workspace,
     ) -> Result<CleanupOutcome, PublicationEvidence> {
-        let Some(resolved) = self.resolve_publication(target)? else { return Ok(CleanupOutcome::AlreadyAbsent); };
+        let Some(resolved) = self.resolve_publication(target, workspace).map_err(|refusal| refusal.publication_evidence)? else {
+            return Ok(CleanupOutcome::AlreadyAbsent);
+        };
         // Observation alone authorizes nothing. Re-read the owned pointer
         // immediately before the one exact removal and refuse its target.
         let current = self.inspect_untrusted(workspace).map_err(|refusal| refusal.publication_evidence)?.0;
@@ -1375,6 +1378,52 @@ mod tests {
         assert!(workspace.path().join(".agents").is_dir());
     }
 
+    #[test]
+    fn requested_publication_candidate_failures_keep_the_inspection_stage_without_effects() {
+        let emission = FileEmission::new(PathBuf::from("git")).unwrap();
+
+        for manifest in ["missing", "corrupt"] {
+            let workspace = tempfile::tempdir().unwrap();
+            let candidate = workspace.path().join(".belief/generations")
+                .join(publication_component_for("requested", 1));
+            fs::create_dir_all(&candidate).unwrap();
+            if manifest == "corrupt" {
+                fs::write(candidate.join("manifest.signal"), "not a manifest").unwrap();
+            }
+            let before = filesystem_tree(workspace.path());
+            let requested = publication(workspace.path(), "requested", None, 1, "instructions", vec![]);
+
+            assert!(matches!(
+                emission.execute(Query::Publish(requested.clone())),
+                Response::EmissionRefused(EmissionRefusal::Publication(PublicationRefusal {
+                    workspace: refused_workspace,
+                    publication_operation: PublicationOperation::InspectingManifest,
+                    publication_evidence: PublicationEvidence::ManifestMismatch,
+                })) if refused_workspace == requested.workspace
+            ));
+            assert_eq!(filesystem_tree(workspace.path()), before);
+        }
+
+        let workspace = tempfile::tempdir().unwrap();
+        let requested = publication(workspace.path(), "requested", None, 1, "instructions", vec![]);
+        let candidate = workspace.path().join(".belief/generations")
+            .join(publication_component_for("requested", 1));
+        write_publication_directory(&requested, &candidate);
+        assert!(matches!(emission.execute(Query::Publish(requested)), Response::Published(_)));
+        assert_eq!(fs::read_link(workspace.path().join(".belief/current")).unwrap(),
+            PathBuf::from("generations").join(publication_component_for("requested", 1)));
+
+        let workspace = tempfile::tempdir().unwrap();
+        let invalid = publication(workspace.path(), "../invalid", None, 1, "instructions", vec![]);
+        assert!(matches!(
+            emission.execute(Query::Publish(invalid)),
+            Response::EmissionRefused(EmissionRefusal::Publication(PublicationRefusal {
+                publication_operation: PublicationOperation::StagingGeneration,
+                ..
+            }))
+        ));
+    }
+
     #[test]
     fn snapshot_reads_one_committed_main_tree_and_ignores_worktree_changes() {
         let repository = tempfile::tempdir().unwrap();
```
