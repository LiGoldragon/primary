use typed_call_trial::{
    Admission, Answer, BeliefLine, Committable, Decodable, Emittable, ModelCall, Outcome,
    Processor, Promptable, Question, Snapshot,
};

trait Fixture {
    fn admission() -> Self;
    fn queue() -> Self;
}
impl Fixture for Question {
    fn admission() -> Self {
        Self::Admission {
            case: "synthetic".into(),
            submitted: "one proposed line".into(),
            snapshot: Snapshot {
                revision: "r1".into(),
                module: "vision:example:0".into(),
                lines: vec![BeliefLine {
                    identifier: "a".into(),
                    text: "held line".into(),
                }],
                modules: vec!["vision:elsewhere:0".into()],
            },
        }
    }
    fn queue() -> Self {
        Self::Queue {
            case: "synthetic".into(),
            message: "result ready".into(),
            recipient_state: "asleep".into(),
            pending_work: vec![],
        }
    }
}

#[test]
fn admission_decodes() {
    assert!(matches!(
        Question::admission()
            .decode(r#"{"kind":"Admission","judgment":{"kind":"Admitted","wording":"line"}}"#),
        Outcome::Answered { .. }
    ));
}
#[test]
fn repeats_decodes_with_valid_reference() {
    assert!(matches!(
        Question::admission().decode(
            r#"{"kind":"Admission","judgment":{"kind":"Repeats","line":"a","wording":null}}"#
        ),
        Outcome::Answered { .. }
    ));
}
#[test]
fn collides_decodes_with_valid_reference() {
    assert!(matches!(Question::admission().decode(r#"{"kind":"Admission","judgment":{"kind":"Collides","line":"a","wording":"new wording"}}"#), Outcome::Answered { .. }));
}
#[test]
fn elsewhere_decodes_with_valid_module() {
    assert!(matches!(Question::admission().decode(r#"{"kind":"Admission","judgment":{"kind":"Elsewhere","module":"vision:elsewhere:0","wording":null}}"#), Outcome::Answered { .. }));
}
#[test]
fn unknown_references_refuse() {
    assert!(matches!(
        Question::admission().decode(
            r#"{"kind":"Admission","judgment":{"kind":"Repeats","line":"invented","wording":null}}"#
        ),
        Outcome::Malformed { .. }
    ));
}
#[test]
fn unknown_modules_refuse() {
    assert!(matches!(Question::admission().decode(r#"{"kind":"Admission","judgment":{"kind":"Elsewhere","module":"unknown","wording":null}}"#), Outcome::Malformed { .. }));
}
#[test]
fn empty_wording_refuses() {
    assert!(matches!(
        Question::admission()
            .decode(r#"{"kind":"Admission","judgment":{"kind":"Admitted","wording":" "}}"#),
        Outcome::Malformed { .. }
    ));
}
#[test]
fn refusal_is_its_own_outcome() {
    assert_eq!(
        Question::queue().decode(r#"{"kind":"Refused","reason":"insufficient state"}"#),
        Outcome::ModelRefused {
            reason: "insufficient state".into()
        }
    );
}
#[test]
fn queue_decodes() {
    assert!(matches!(
        Question::queue().decode(
            r#"{"kind":"Queue","judgment":{"kind":"KeepQueued","reason":"recipient is awake"}}"#
        ),
        Outcome::Answered { .. }
    ));
}
#[test]
fn wrong_task_refuses() {
    assert!(matches!(
        Question::admission()
            .decode(r#"{"kind":"Queue","judgment":{"kind":"StartFresh","reason":"important"}}"#),
        Outcome::Malformed { .. }
    ));
}
#[test]
fn malformed_fences_extra_keys_duplicates_and_trailing_values_refuse() {
    for text in [
        "not json",
        "```json\n{}\n```",
        r#"{"kind":"Refused","reason":"r","extra":1}"#,
        r#"{"kind":"Refused","reason":"a","reason":"b"}"#,
        r#"{"kind":"Refused","reason":"r"} {}"#,
    ] {
        assert!(
            matches!(
                Question::admission().decode(text),
                Outcome::Malformed { .. }
            ),
            "{text}"
        );
    }
}
#[test]
fn stale_snapshot_does_not_change() {
    let Question::Admission { mut snapshot, .. } = Question::admission() else {
        unreachable!()
    };
    let answer = Outcome::Answered {
        answer: Answer::Admission {
            judgment: Admission::Admitted {
                wording: "new".into(),
            },
        },
    };
    assert_eq!(snapshot.commit("old", answer), Outcome::StaleSnapshot);
    assert_eq!(snapshot.lines.len(), 1);
}
#[test]
fn only_admitted_changes_disposable_snapshot() {
    let Question::Admission { mut snapshot, .. } = Question::admission() else {
        unreachable!()
    };
    let answer = Outcome::Answered {
        answer: Answer::Admission {
            judgment: Admission::Admitted {
                wording: "new".into(),
            },
        },
    };
    snapshot.commit("r1", answer);
    assert_eq!(snapshot.lines.len(), 2);
    assert_eq!(snapshot.revision, "r1+");
    snapshot.commit(
        "r1+",
        Outcome::Malformed {
            reason: "bad".into(),
        },
    );
    assert_eq!(snapshot.lines.len(), 2);
}
#[test]
fn duplicate_identifiers_refuse_before_prompt() {
    let mut question = Question::admission();
    if let Question::Admission { snapshot, .. } = &mut question {
        snapshot.lines.push(snapshot.lines[0].clone());
    }
    assert!(question.prompt().is_err());
}
#[test]
fn missing_prompt_never_executes_processor() {
    let call = ModelCall {
        model: "fixture-model".into(),
        question: Question::admission(),
        prompt_file: "/nonexistent/typed-call-fixture".into(),
    };
    let processor = Processor {
        executable: "/nonexistent/processor".into(),
        arguments: vec![],
    };
    assert!(
        matches!(call.emit(&processor).outcome, Outcome::ProviderFailed { reason } if reason.contains("prompt file differs"))
    );
}
