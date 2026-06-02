use orchestrate_cli::Lane;
use orchestrate_cli::registry::LaneRegistry;

const SAMPLE_REGISTRY: &str = r#"# Role-lane registry — sample.
#
# Comments and blank lines are stripped.

operator
pi-operator                       parallel-of:operator
second-operator                   parallel-of:operator
cluster-operator
cloud-operator
designer
second-designer                   parallel-of:designer
third-designer                    parallel-of:designer
nota-designer
system-designer
cloud-designer
system-operator
poet
assistant
counselor
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
            lane("pi-operator"),
            lane("second-operator"),
            lane("cluster-operator"),
            lane("cloud-operator"),
            lane("designer"),
            lane("second-designer"),
            lane("third-designer"),
            lane("nota-designer"),
            lane("system-designer"),
            lane("cloud-designer"),
            lane("system-operator"),
            lane("poet"),
            lane("assistant"),
            lane("counselor"),
        ]
    );
}

#[test]
fn lane_markers_record_parallel_main_role() {
    let registry = LaneRegistry::parse(SAMPLE_REGISTRY).expect("registry parse");
    let descriptors = registry.descriptors();
    let second_operator = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == lane("second-operator"))
        .expect("second-operator descriptor present");
    assert_eq!(second_operator.assistant_of, None);
    assert_eq!(second_operator.parallel_of, Some(lane("operator")));
    let assistant = descriptors
        .iter()
        .find(|descriptor| descriptor.lane == lane("assistant"))
        .expect("assistant descriptor present");
    assert_eq!(assistant.assistant_of, None);
    assert_eq!(assistant.parallel_of, None);
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
    assert!(format!("{err}").contains("bad/lane"), "{err}");
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
    assert_eq!(peers.len(), 14);
    assert!(!peers.contains(&operator));
}
