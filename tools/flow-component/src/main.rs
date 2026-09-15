use flow_component::{attach_plan, execute, launch_argv, meta_signal_bytes, ordinary_signal_bytes, parse_inline, FlowCommand, MetaSignal, OrdinarySignal};

fn main() {
    let mut args = std::env::args();
    args.next();
    let text = args.next().unwrap_or_else(|| { eprintln!("usage: flow-component 'Launch.{{ flow claude haiku cwd attach name uuid system-prompt user-prompt environment }}'"); std::process::exit(2) });
    if args.next().is_some() { eprintln!("error: exactly one inline Datom command is required"); std::process::exit(2); }
    match parse_inline(&text).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(2) }) {
        FlowCommand::Launch(launch) => {
            let frame = meta_signal_bytes(MetaSignal::Launch(launch.clone())).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(2) });
            eprintln!("meta Signal bytes: {}", frame.len());
            let argv = launch_argv(&launch).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(2) });
            eprintln!("planned argv: {argv:?}");
            execute(&launch).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(1) });
        }
        FlowCommand::Attach(attach) => {
            let frame = ordinary_signal_bytes(OrdinarySignal::Attach(attach.clone())).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(2) });
            println!("ordinary Signal bytes: {}; {}", frame.len(), attach_plan(&attach).unwrap_or_else(|error| { eprintln!("error: {error}"); std::process::exit(2) }));
        }
    }
}
