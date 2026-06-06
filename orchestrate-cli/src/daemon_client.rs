use std::fs::OpenOptions;
use std::os::unix::net::UnixStream;
use std::os::unix::process::CommandExt;
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

use nota_codec::{Decoder, Encoder, NotaDecode, NotaEncode};
use signal_frame::{ClientShape, CommandLineSockets, SingleArgument};

use crate::error::{Error, Result};
use crate::workspace::Workspace;

const READINESS_TIMEOUT: Duration = Duration::from_secs(5);
const READINESS_POLL: Duration = Duration::from_millis(50);

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrchestrateDaemonClient {
    component_root: PathBuf,
    store_path: PathBuf,
    ordinary_socket_path: PathBuf,
    meta_socket_path: PathBuf,
    upgrade_socket_path: PathBuf,
    workspace_root: PathBuf,
    git_index_root: PathBuf,
}

struct DaemonProcess {
    executable: PathBuf,
    configuration_text: String,
    log_path: PathBuf,
}

struct ComponentBuild {
    component_root: PathBuf,
}

struct ReplyText {
    text: String,
}

impl OrchestrateDaemonClient {
    pub fn from_workspace(workspace: &Workspace) -> Self {
        let state = workspace.orchestrate_dir();
        Self {
            component_root: Self::component_root_from_environment(),
            store_path: state.join("orchestrate.redb"),
            ordinary_socket_path: state.join("orchestrate.sock"),
            meta_socket_path: state.join("orchestrate-owner.sock"),
            upgrade_socket_path: state.join("orchestrate-upgrade.sock"),
            workspace_root: workspace.root().to_path_buf(),
            git_index_root: PathBuf::from("/git/github.com/LiGoldragon"),
        }
    }

    pub fn ensure_ready(&self) -> Result<()> {
        if self.can_connect() {
            return Ok(());
        }

        ComponentBuild::new(self.component_root.clone()).build_if_needed()?;
        DaemonProcess::new(self).spawn()?;
        self.wait_for_readiness()
    }

    pub fn submit_working<Request, Reply>(&self, request: &Request) -> Result<Reply>
    where
        Request: NotaEncode,
        Reply: NotaDecode,
    {
        self.ensure_ready()?;
        ReplyText::new(self.submit_text(request)?).decode()
    }

    fn submit_text<Request>(&self, request: &Request) -> Result<String>
    where
        Request: NotaEncode,
    {
        let mut encoder = Encoder::new();
        request.encode(&mut encoder)?;
        let client = ClientShape::<signal_orchestrate::Frame, meta_signal_orchestrate::Frame>::new(
            CommandLineSockets::new(
                Some(self.ordinary_socket_path.clone()),
                Some(self.meta_socket_path.clone()),
                "PERSONA_ORCHESTRATE_SOCKET",
                "PERSONA_ORCHESTRATE_OWNER_SOCKET",
            ),
        );
        let argument = SingleArgument::from_program_and_values(
            "orchestrate".to_string(),
            vec![encoder.into_string()],
        )
        .map_err(signal_frame::CommandLineError::from)?;
        Ok(client.reply_text(argument)?)
    }

    fn wait_for_readiness(&self) -> Result<()> {
        let deadline = Instant::now() + READINESS_TIMEOUT;
        while Instant::now() < deadline {
            if self.can_connect() {
                return Ok(());
            }
            std::thread::sleep(READINESS_POLL);
        }
        Err(Error::DaemonReadinessTimeout {
            socket: self.ordinary_socket_path.clone(),
        })
    }

    fn can_connect(&self) -> bool {
        UnixStream::connect(&self.ordinary_socket_path).is_ok()
    }

    fn configuration_text(&self) -> String {
        format!(
            "([{}] [{}] [{}] [{}] [{}] [{}])",
            self.store_path.display(),
            self.ordinary_socket_path.display(),
            self.meta_socket_path.display(),
            self.upgrade_socket_path.display(),
            self.workspace_root.display(),
            self.git_index_root.display()
        )
    }

    fn daemon_executable(&self) -> PathBuf {
        self.component_root
            .join("target")
            .join("release")
            .join("orchestrate-daemon")
    }

    fn daemon_log_path(&self) -> PathBuf {
        self.workspace_root
            .join("orchestrate")
            .join("orchestrate-daemon.log")
    }

    fn component_root_from_environment() -> PathBuf {
        std::env::var("ORCHESTRATE_COMPONENT_ROOT")
            .map(PathBuf::from)
            .unwrap_or_else(|_| PathBuf::from("/git/github.com/LiGoldragon/orchestrate"))
    }
}

impl ComponentBuild {
    fn new(component_root: PathBuf) -> Self {
        Self { component_root }
    }

    fn build_if_needed(&self) -> Result<()> {
        let daemon = self
            .component_root
            .join("target")
            .join("release")
            .join("orchestrate-daemon");
        let client = self
            .component_root
            .join("target")
            .join("release")
            .join("orchestrate");
        if daemon.is_file() && client.is_file() {
            return Ok(());
        }

        let status = Command::new("cargo")
            .args([
                "build",
                "--release",
                "--locked",
                "--bin",
                "orchestrate",
                "--bin",
                "orchestrate-daemon",
            ])
            .env("CARGO_BUILD_JOBS", "2")
            .current_dir(&self.component_root)
            .status()?;
        if status.success() {
            Ok(())
        } else {
            Err(Error::DaemonBuildFailed {
                status: status.to_string(),
            })
        }
    }
}

impl DaemonProcess {
    fn new(client: &OrchestrateDaemonClient) -> Self {
        Self {
            executable: client.daemon_executable(),
            configuration_text: client.configuration_text(),
            log_path: client.daemon_log_path(),
        }
    }

    fn spawn(&self) -> Result<()> {
        if let Some(parent) = self.executable.parent() {
            std::fs::create_dir_all(parent)?;
        } else {
            return Err(Error::DaemonExecutableHasNoParent {
                path: self.executable.clone(),
            });
        }
        if let Some(parent) = self.log_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        let log = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.log_path)?;
        let error_log = log.try_clone()?;
        let mut command = Command::new(&self.executable);
        command
            .arg(&self.configuration_text)
            .stdin(Stdio::null())
            .stdout(Stdio::from(log))
            .stderr(Stdio::from(error_log));
        command.process_group(0);
        command.spawn()?;
        Ok(())
    }
}

impl ReplyText {
    fn new(text: String) -> Self {
        Self { text }
    }

    fn decode<Reply>(&self) -> Result<Reply>
    where
        Reply: NotaDecode,
    {
        let mut decoder = Decoder::new(self.text.trim());
        Ok(Reply::decode(&mut decoder)?)
    }
}
