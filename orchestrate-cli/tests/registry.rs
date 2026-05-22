use orchestrate_cli::Lane;
use orchestrate_cli::registry::LaneRegistry;

const SAMPLE_REGISTRY: &str = r#"# Role-lane registry — sample.
#
# Comments and blank lines are stripped.

operator
second-operator                   parallel-of:operator
operator-assistant                assistant-of:operator
second-operator-assistant         assistant-of:operator
designer
second-designer                   parallel-of:designer
third-designer                    parallel-of:designer
designer-assistant                assistant-of:designer
system-specialist
system-assistant                  assistant-of:system-specialist
second-system-assistant           assistant-of:system-specialist
poet
poet-assistant                    assistant-of:poet
"#;

fn lane(token: &str) -> Lane {
    Lane::from_token(token).expect("valid lane")
}

#[test]
fn parses_all_lanes_in_order() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let lanes: Vec<Lane> = registry.lanes().collect();
    assert_eq!(
        lanes,
        vec![
            lane("operator"),
            lane("second-operator"),
            lane("operator-assistant"),
            lane("second-operator-assistant"),
            lane("designer"),
            lane("second-designer"),
            lane("third-designer"),
            lane("designer-assistant"),
            lane("system-specialist"),
            lane("system-assistant"),
            lane("second-system-assistant"),
            lane("poet"),
            lane("poet-assistant"),
        ]
    );
}

#[test]
fn assistant_marker_records_main_role() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let descriptors = registry.descriptors();
    let operator_assistant = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == lane("operator-assistant"))
        .expect("operator-assistant descriptor present");
    assert_eq!(operator_assistant.assistant_of, Some(lane("operator")));
    assert_eq!(operator_assistant.parallel_of, None);
    let second_operator = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == lane("second-operator"))
        .expect("second-operator descriptor present");
    assert_eq!(second_operator.assistant_of, None);
    assert_eq!(second_operator.parallel_of, Some(lane("operator")));
    let operator = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == lane("operator"))
        .expect("operator descriptor present");
    assert_eq!(operator.assistant_of, None);
    assert_eq!(operator.parallel_of, None);
}

#[test]
fn unknown_marker_is_rejected() {
    let registry = "operator              unexpected-marker:value\n";
    let err = LaneRegistry::parse(registry).unwrap_err();
    assert!(format!("{err}").contains("unrecognised marker"), "{err}");
}

#[test]
fn invalid_lane_token_is_rejected() {
    let registry = "operator\nbad/lane   assistant-of:designer\n";
    let err = LaneRegistry::parse(registry).unwrap_err();
    assert!(
        format!("{err}").contains("bad/lane"),
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
    let operator = lane("operator");
    let peers: Vec<Lane> = registry.peer_lanes(&operator).collect();
    assert_eq!(peers.len(), 12);
    assert!(!peers.contains(&operator));
}
