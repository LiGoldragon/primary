use std::path::Path;

use orchestrate_cli::scope::RawScope;
use orchestrate_cli::{Lane, NormalizedScope};
use signal_persona_orchestrate::{OrchestrateRequest, RoleName, ScopeReference};

fn scope(raw: &str) -> NormalizedScope {
    NormalizedScope::from_raw(&RawScope::new(raw), Path::new("/home/li")).unwrap()
}

#[test]
fn claim_decodes_to_role_claim_with_typed_scope_and_reason() {
    let scopes = vec![scope("/home/li/primary/skills/foo.md")];
    let request =
        orchestrate_cli::request::claim_request(Lane::Operator, &scopes, "syncing claim docs")
            .expect("claim request");
    match request {
        OrchestrateRequest::RoleClaim(record) => {
            assert_eq!(record.role, RoleName::Operator);
            assert_eq!(record.scopes.len(), 1);
            match &record.scopes[0] {
                ScopeReference::Path(path) => {
                    assert_eq!(path.as_str(), "/home/li/primary/skills/foo.md");
                }
                other => panic!("expected ScopeReference::Path, got {other:?}"),
            }
            assert_eq!(record.reason.as_str(), "syncing claim docs");
        }
        other => panic!("expected OrchestrateRequest::RoleClaim, got {other:?}"),
    }
}

#[test]
fn claim_with_task_scope_projects_to_task_reference() {
    let scopes = vec![scope("[primary-68cb]")];
    let request = orchestrate_cli::request::claim_request(Lane::Operator, &scopes, "rust port")
        .expect("claim request");
    match request {
        OrchestrateRequest::RoleClaim(record) => match &record.scopes[0] {
            ScopeReference::Task(task) => {
                assert_eq!(task.as_str(), "primary-68cb");
            }
            other => panic!("expected ScopeReference::Task, got {other:?}"),
        },
        other => panic!("expected RoleClaim, got {other:?}"),
    }
}

#[test]
fn release_decodes_to_role_release_with_role_name() {
    let request = orchestrate_cli::request::release_request(Lane::Operator);
    match request {
        OrchestrateRequest::RoleRelease(record) => assert_eq!(record.role, RoleName::Operator),
        other => panic!("expected RoleRelease, got {other:?}"),
    }
}

#[test]
fn observation_decodes_to_role_observation() {
    let request = orchestrate_cli::request::observation_request();
    assert!(matches!(request, OrchestrateRequest::RoleObservation(_)));
}

#[test]
fn second_assistant_lanes_project_to_matching_role_name() {
    assert_eq!(
        Lane::SecondOperatorAssistant.role_name(),
        RoleName::SecondOperatorAssistant
    );
    assert_eq!(
        Lane::SecondDesignerAssistant.role_name(),
        RoleName::SecondDesignerAssistant
    );
    assert_eq!(
        Lane::SecondSystemAssistant.role_name(),
        RoleName::SecondSystemAssistant
    );
}

#[test]
fn empty_reason_is_rejected_at_request_layer() {
    let scopes = vec![scope("/home/li/primary/skills/foo.md")];
    let result = orchestrate_cli::request::claim_request(Lane::Operator, &scopes, "");
    assert!(result.is_err(), "{result:?}");
}
