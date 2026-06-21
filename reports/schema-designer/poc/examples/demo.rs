//! The CLI view: build the help model client-side, then drive the exact CLI
//! intercept path — recognize the single argument, resolve to the typed tree,
//! render NOTA, never connect to the daemon. Built only with --features
//! nota-text (the "CLI" build).

use schema_help_poc::generated::Input;
use schema_help_poc::render::HelpInvocation;
use schema_help_poc::HelpQuery;

fn main() {
    let model = Input::help_model();

    println!("$ spirit Help");
    for line in model.render(&HelpQuery::all()).expect("bare help renders").lines() {
        println!("  {line}");
    }

    let trace = [
        "(Help Record)",
        "(Help Entry)",
        "(Help Domains)",
        "(Help Description)",
        "(Help Justification)",
        "(Help Testimony)",
        "(Help VerbatimQuote)",
        "(Help OptionalAntecedent)",
        "(Help QuoteText)",
        "(Help RecordAccepted)",
        "(Help Kind)",
        "(Help DomainMatch)",
    ];
    println!();
    for argument in trace {
        // Exactly the CLI path: recognize the single argument, resolve + render,
        // never contact the daemon.
        let invocation = HelpInvocation::recognize(argument).expect("a help invocation");
        let query: HelpQuery = invocation.into();
        let rendered = model.render(&query).expect("known topic renders");
        println!("$ spirit \"{argument}\"  ->  {rendered}");
    }
}
