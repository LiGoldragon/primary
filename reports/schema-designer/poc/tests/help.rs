//! Golden acceptance tests for the help renderer. Required-features: nota-text.
//!
//! These exact strings are the non-negotiable acceptance gates — they reproduce
//! the navigation trace from `reports/schema-designer/1-…` with real spirit
//! types. They run in a CWD with no schema directory at all, catching any latent
//! on-disk / import dependency by construction.

#![cfg(feature = "nota-text")]

use schema_help_poc::generated::Input;
use schema_help_poc::render::HelpInvocation;
use schema_help_poc::{HelpQuery, Name};

fn render_topic(topic: &str) -> String {
    Input::help_model()
        .render(&HelpQuery::topic(Name::from(topic)))
        .expect("known topic renders")
}

#[test]
fn record_struct_payload_inlines_one_level() {
    assert_eq!(render_topic("Record"), "(Record { Entry Justification })");
}

#[test]
fn record_accepted_newtype_payload_shows_by_name() {
    assert_eq!(render_topic("RecordAccepted"), "(RecordAccepted RecordIdentifier)");
}

#[test]
fn entry_struct_fields_are_newtype_names() {
    assert_eq!(
        render_topic("Entry"),
        "(Entry { Domains Kind Description Certainty Importance Privacy Referents })"
    );
}

#[test]
fn justification_struct_inlines_one_level() {
    assert_eq!(render_topic("Justification"), "(Justification { Testimony Reasoning })");
}

#[test]
fn vec_element_stays_a_named_reference() {
    // The settled answer: a Vec element is a reference, not inline-expanded.
    assert_eq!(render_topic("Domains"), "(Domains (Vec Domain))");
    assert_eq!(render_topic("Testimony"), "(Testimony (Vec VerbatimQuote))");
}

#[test]
fn optional_element_stays_a_named_reference() {
    assert_eq!(render_topic("OptionalAntecedent"), "(OptionalAntecedent (Optional Antecedent))");
}

#[test]
fn newtype_bottoms_out_at_scalar_leaf() {
    // The scalar surfaces only at the newtype boundary, one Help step down.
    assert_eq!(render_topic("Description"), "(Description String)");
    assert_eq!(render_topic("RecordIdentifier"), "(RecordIdentifier String)");
    assert_eq!(render_topic("QuoteText"), "(QuoteText String)");
}

#[test]
fn struct_with_newtype_field_navigates_one_level() {
    assert_eq!(render_topic("VerbatimQuote"), "(VerbatimQuote { QuoteText OptionalAntecedent })");
}

#[test]
fn enum_declaration_inlines_variants_one_level() {
    assert_eq!(
        render_topic("Kind"),
        "(Kind [Decision Principle Correction Clarification Constraint])"
    );
    assert_eq!(
        render_topic("DomainMatch"),
        "(DomainMatch [Any (Partial DomainScopes) (Full DomainScopes)])"
    );
}

#[test]
fn imported_or_undeclared_payload_stays_bare_leaf() {
    // State -> Statement and Observe -> Query: Statement/Query are not declared
    // here (imported / undeclared), so they stay bare leaf names.
    assert_eq!(render_topic("State"), "(State Statement)");
    assert_eq!(render_topic("Observe"), "(Observe Query)");
}

#[test]
fn unit_root_renders_bare() {
    assert_eq!(render_topic("Version"), "(Version)");
}

#[test]
fn bare_help_is_the_one_level_signature_index() {
    let listing = Input::help_model()
        .render(&HelpQuery::all())
        .expect("bare help always renders");
    let expected = [
        "(State Statement)",
        "(Record { Entry Justification })",
        "(Observe Query)",
        "(Version)",
        "(Marker)",
        "(RecordAccepted RecordIdentifier)",
        "(Proposed RecordIdentifier)",
    ]
    .join("\n");
    assert_eq!(listing, expected);
}

#[test]
fn unknown_topic_is_typed_error() {
    let result = Input::help_model().render(&HelpQuery::topic(Name::from("Nonexistent")));
    assert!(result.is_err());
}

#[test]
fn cli_recognizer_distinguishes_all_and_topic() {
    match HelpInvocation::recognize("Help").expect("bare Help") {
        HelpInvocation::All => {}
        HelpInvocation::Topic(_) => panic!("bare Help must be All"),
    }
    match HelpInvocation::recognize("(Help Record)").expect("topic Help") {
        HelpInvocation::Topic(name) => assert_eq!(name.as_str(), "Record"),
        HelpInvocation::All => panic!("(Help Record) must be Topic"),
    }
    assert!(HelpInvocation::recognize("(State foo)").is_err());
}

#[test]
fn cli_recognizer_drives_render_end_to_end() {
    let invocation = HelpInvocation::recognize("(Help RecordAccepted)").expect("topic Help");
    let query: HelpQuery = invocation.into();
    let rendered = Input::help_model().render(&query).expect("renders");
    assert_eq!(rendered, "(RecordAccepted RecordIdentifier)");
}
