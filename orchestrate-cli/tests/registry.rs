use orchestrate_cli::Lane;
use orchestrate_cli::registry::LaneRegistry;

const SAMPLE_REGISTRY: &str = r#"# Role-lane registry — sample.
#
# Comments and blank lines are stripped.

operator
operator-assistant                assistant-of:operator
second-operator-assistant         assistant-of:operator
designer
designer-assistant                assistant-of:designer
second-designer-assistant         assistant-of:designer
system-specialist
system-assistant                  assistant-of:system-specialist
second-system-assistant           assistant-of:system-specialist
poet
poet-assistant                    assistant-of:poet
"#;

#[test]
fn parses_all_lanes_in_order() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let lanes: Vec<Lane> = registry.lanes().collect();
    assert_eq!(
        lanes,
        vec![
            Lane::Operator,
            Lane::OperatorAssistant,
            Lane::SecondOperatorAssistant,
            Lane::Designer,
            Lane::DesignerAssistant,
            Lane::SecondDesignerAssistant,
            Lane::SystemSpecialist,
            Lane::SystemAssistant,
            Lane::SecondSystemAssistant,
            Lane::Poet,
            Lane::PoetAssistant,
        ]
    );
}

#[test]
fn assistant_marker_records_main_role() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let descriptors = registry.descriptors();
    let operator_assistant = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == Lane::OperatorAssistant)
        .expect("operator-assistant descriptor present");
    assert_eq!(operator_assistant.assistant_of, Some(Lane::Operator));
    let operator = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == Lane::Operator)
        .expect("operator descriptor present");
    assert_eq!(operator.assistant_of, None);
}

#[test]
fn unknown_marker_is_rejected() {
    let registry = "operator              unexpected-marker:value\n";
    let err = LaneRegistry::parse(registry).unwrap_err();
    assert!(format!("{err}").contains("unrecognised marker"), "{err}");
}

#[test]
fn unknown_lane_is_rejected() {
    let registry = "operator\nfourth-designer-assistant   assistant-of:designer\n";
    let err = LaneRegistry::parse(registry).unwrap_err();
    assert!(
        format!("{err}").contains("fourth-designer-assistant"),
        "{err}"
    );
}

#[test]
fn empty_registry_is_rejected() {
    let registry = "# only comments\n\n";
    let err = LaneRegistry::parse(registry).unwrap_err();
    assert!(format!("{err}").contains("no entries"), "{err}");
}

#[test]
fn peer_lanes_exclude_self() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let peers: Vec<Lane> = registry.peer_lanes(Lane::Operator).collect();
    assert_eq!(peers.len(), 10);
    assert!(!peers.contains(&Lane::Operator));
}
