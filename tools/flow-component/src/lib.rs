#![forbid(unsafe_code)]

use datom_codec::{Actualizing, Budget, Potential};
use nexus::{Permissive, SocketAuthority};
use protos::ReaderBudget;
use signal::{ByteViewable, Signalizable};
use std::process::Command;

pub mod transport;

/// The ordinary and meta sockets a real Flow Nexus will bind. This prototype
/// has no sockets or store yet; it makes their authority boundary explicit so
/// a caller cannot mistake launch authority for ordinary attachment traffic.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct FlowNexusBoundary {
    pub ordinary: SocketAuthority,
    pub meta: SocketAuthority,
}

impl Default for FlowNexusBoundary {
    fn default() -> Self {
        Self { ordinary: SocketAuthority::Ordinary, meta: SocketAuthority::Privileged }
    }
}

impl FlowNexusBoundary {
    pub fn ordinary_mode(self) -> u32 { self.ordinary.mode() }
    pub fn meta_mode(self) -> u32 { self.meta.mode() }
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, datom_codec::Composing, datom_codec::Datomizable, Debug, Clone, PartialEq, Eq)]
pub struct UserEnvironment {
    pub home: String,
    pub path: String,
    pub display: Option<String>,
    pub wayland_display: Option<String>,
    pub xdg_current_desktop: Option<String>,
    pub xdg_session_type: Option<String>,
    pub xdg_runtime_dir: Option<String>,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, datom_codec::Composing, datom_codec::Datomizable, Debug, Clone, PartialEq, Eq)]
pub struct Launch {
    pub flow: String,
    pub harness: String,
    pub model: String,
    pub cwd: String,
    pub attach: String,
    pub name: String,
    pub session_id: String,
    pub system_prompt_file: String,
    pub user_prompt_file: String,
    pub environment: UserEnvironment,
}

#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, datom_codec::Composing, datom_codec::Datomizable, Debug, Clone, PartialEq, Eq)]
pub struct Attach {
    pub flow: String,
    pub name: String,
}

#[derive(datom_codec::Composing, datom_codec::Datomizable, Debug, Clone, PartialEq, Eq)]
pub enum FlowCommand {
    Launch(Launch),
    Attach(Attach),
}

/// Ordinary frames are observational/attachment requests. Meta frames carry
/// the privileged launch capability. These are real portable Signal bytes; a
/// bound Flow Nexus listener remains future work.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Debug, Clone, PartialEq, Eq)]
pub enum OrdinarySignal { Observe(Attach), Attach(Attach) }
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Debug, Clone, PartialEq, Eq)]
pub enum MetaSignal { Launch(Launch) }

/// Reserved lifecycle records for the Flow-owned store. They are data only:
/// this prototype neither emits them nor wakes, logs to, or mutates an older
/// flow. A future owner may use Check for health observation and Recycle for
/// the failure-gated handoff described by the lifecycle design.
#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize, Debug, Clone, PartialEq, Eq)]
pub enum FutureLifecycleRecord {
    Check { flow: String },
    Recycle { flow: String, prior_flow: String },
}

pub fn ordinary_signal_bytes(signal: OrdinarySignal) -> Result<Vec<u8>, String> {
    signal.signalize().map(|frame| frame.bytes().to_vec()).map_err(|error| format!("ordinary Signal encoding failed: {error}"))
}
pub fn meta_signal_bytes(signal: MetaSignal) -> Result<Vec<u8>, String> {
    signal.signalize().map(|frame| frame.bytes().to_vec()).map_err(|error| format!("meta Signal encoding failed: {error}"))
}

pub fn budget() -> Budget {
    Budget { remaining: 4096, reader: ReaderBudget { remaining: 4096 }, depth: 0, maximum_depth: 256 }
}

pub fn parse_inline(text: &str) -> Result<FlowCommand, String> {
    Potential::<FlowCommand>::from(text)
        .actualize(&mut budget())
        .map_err(|error| format!("Datom command refused: {error:?}"))
}

fn nonempty(value: &str, name: &str) -> Result<(), String> {
    if value.is_empty() { Err(format!("missing {name}")) } else { Ok(()) }
}

fn uuid(value: &str) -> bool {
    let bytes = value.as_bytes();
    bytes.len() == 36 && [8, 13, 18, 23].into_iter().all(|at| bytes[at] == b'-')
        && bytes.iter().enumerate().all(|(at, byte)| [8, 13, 18, 23].contains(&at) || byte.is_ascii_hexdigit())
}

pub fn launch_argv(launch: &Launch) -> Result<Vec<String>, String> {
    for (value, name) in [(&launch.flow, "flow"), (&launch.harness, "harness"), (&launch.model, "model"), (&launch.cwd, "cwd"), (&launch.attach, "attach"), (&launch.name, "name"), (&launch.system_prompt_file, "system prompt file"), (&launch.user_prompt_file, "user prompt file"), (&launch.environment.home, "HOME"), (&launch.environment.path, "PATH")] { nonempty(value, name)?; }
    if launch.harness != "claude" { return Err("only the Claude harness is implemented".into()); }
    if !["haiku", "sonnet"].contains(&launch.model.as_str()) { return Err("model must be haiku or sonnet for this bounded prototype".into()); }
    if launch.attach != "attach" { return Err("Launch.attach must be attach".into()); }
    if !uuid(&launch.session_id) { return Err("session_id must be an exact UUID".into()); }
    let unit = format!("flow-{}.scope", launch.flow);
    let mut environment = vec![format!("HOME={}", launch.environment.home), format!("PATH={}", launch.environment.path)];
    for (key, value) in [("DISPLAY", &launch.environment.display), ("WAYLAND_DISPLAY", &launch.environment.wayland_display), ("XDG_CURRENT_DESKTOP", &launch.environment.xdg_current_desktop), ("XDG_SESSION_TYPE", &launch.environment.xdg_session_type), ("XDG_RUNTIME_DIR", &launch.environment.xdg_runtime_dir)] {
        if let Some(value) = value { nonempty(value, key)?; environment.push(format!("{key}={value}")); }
    }
    let program = "user_prompt=$(<\"$2\"); exec claude --session-id \"$3\" --name \"$4\" --remote-control \"$4\" --model \"$5\" --effort medium --dangerously-skip-permissions --append-system-prompt-file \"$1\" \"$user_prompt\"";
    Ok([
        vec!["systemd-run".into(), "--user".into(), "--scope".into(), format!("--unit={unit}"), "--collect".into(), "--no-block".into(), "env".into(), "-i".into()],
        environment,
        vec!["ghostty".into(), "--window-inherit-working-directory=false".into(), format!("--working-directory={}", launch.cwd), format!("--title=Claude {}", launch.name), "-e".into(), "bash".into(), "-lc".into(), program.into(), "flow-component".into(), launch.system_prompt_file.clone(), launch.user_prompt_file.clone(), launch.session_id.clone(), launch.name.clone(), launch.model.clone()],
    ].concat())
}

/// This is the one effectful seam. Tests call `launch_argv`; callers must
/// explicitly select `Launch` at the CLI. The child scope owns Ghostty and its
/// Claude descendant, while `env -i` strips Codex variables from both.
pub fn execute(launch: &Launch) -> Result<(), String> {
    let argv = launch_argv(launch)?;
    let status = Command::new(&argv[0]).args(&argv[1..]).status().map_err(|error| format!("systemd-run failed to start: {error}"))?;
    if status.success() { Ok(()) } else { Err(format!("systemd-run exited {status}")) }
}

pub fn attach_plan(attach: &Attach) -> Result<String, String> {
    nonempty(&attach.flow, "flow")?;
    nonempty(&attach.name, "name")?;
    Ok(format!("Attach is a future ordinary-socket operation for flow {} and name {}; no durable registry exists in this prototype", attach.flow, attach.name))
}

#[cfg(test)]
mod tests {
    use super::*;
    use signal::{Restorable, Signal};
    use std::{fs, os::unix::fs::PermissionsExt, thread};
    fn launch() -> Launch { Launch { flow: "throwaway-flow".into(), harness: "claude".into(), model: "haiku".into(), cwd: "/tmp".into(), attach: "attach".into(), name: "throwaway-claude".into(), session_id: "22222222-2222-4222-8222-222222222222".into(), system_prompt_file: "/tmp/system.md".into(), user_prompt_file: "/tmp/user.md".into(), environment: UserEnvironment { home: "/home/li".into(), path: "/run/current-system/sw/bin".into(), display: Some(":99".into()), wayland_display: None, xdg_current_desktop: None, xdg_session_type: None, xdg_runtime_dir: Some("/run/user/1001".into()) } } }
    #[test]
    fn canonical_datom_requires_named_launch() { assert_eq!(parse_inline("Launch.{ throwaway-flow claude haiku /tmp attach throwaway-claude 22222222-2222-4222-8222-222222222222 /tmp/system.md /tmp/user.md { /home/li /run/current-system/sw/bin Some.«:99» None None None Some./run/user/1001 } }").unwrap(), FlowCommand::Launch(launch())); }
    #[test]
    fn launch_plan_scopes_terminal_and_strips_environment() { let argv = launch_argv(&launch()).unwrap(); assert_eq!(&argv[..6], ["systemd-run", "--user", "--scope", "--unit=flow-throwaway-flow.scope", "--collect", "--no-block"]); assert!(argv.windows(2).any(|pair| pair == ["env", "-i"])); assert!(argv.contains(&"ghostty".into())); assert!(argv.contains(&"--working-directory=/tmp".into())); assert!(argv.contains(&"--title=Claude throwaway-claude".into())); assert!(argv.iter().any(|argument| argument.contains("--remote-control"))); assert!(!argv.iter().any(|argument| argument.starts_with("CODEX_"))); }
    #[test]
    fn ordinary_and_meta_are_distinct_actual_nexus_authorities() { let boundary = FlowNexusBoundary::default(); assert_eq!(boundary.ordinary_mode(), 0o660); assert_eq!(boundary.meta_mode(), 0o600); }
    #[test]
    fn bound_binary_signal_transport_keeps_meta_and_ordinary_separate() {
        let directory = std::env::temp_dir().join(format!("flow-component-nexus-{}", std::process::id()));
        let nexus = transport::TemporaryNexus::bind(&directory).unwrap();
        assert_eq!(fs::metadata(nexus.ordinary_path()).unwrap().permissions().mode() & 0o777, 0o660);
        assert_eq!(fs::metadata(nexus.meta_path()).unwrap().permissions().mode() & 0o777, 0o600);
        let expected = MetaSignal::Launch(launch());
        let bytes = meta_signal_bytes(expected.clone()).unwrap();
        let path = nexus.meta_path().to_owned();
        let sender = thread::spawn(move || transport::send(&path, &bytes));
        let received = nexus.receive_meta().unwrap();
        sender.join().unwrap().unwrap();
        assert_eq!(Signal::<MetaSignal>::from(received).restore().unwrap(), expected);
        let attach = Attach { flow: "throwaway-flow".into(), name: "throwaway-claude".into() };
        let bytes = ordinary_signal_bytes(OrdinarySignal::Attach(attach.clone())).unwrap();
        let path = nexus.ordinary_path().to_owned();
        let sender = thread::spawn(move || transport::send(&path, &bytes));
        let received = nexus.receive_ordinary().unwrap();
        sender.join().unwrap().unwrap();
        assert_eq!(Signal::<OrdinarySignal>::from(received).restore().unwrap(), OrdinarySignal::Attach(attach));
        drop(nexus); let _ = fs::remove_dir(directory);
    }
}
