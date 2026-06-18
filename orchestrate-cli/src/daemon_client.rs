use std::fs::OpenOptions;
use std::os::unix::net::UnixStream;
use std::os::unix::process::CommandExt;
use std::path::PathBuf;
use std::process::{Command, Stdio};
use std::time::{Duration, Instant};

use nota_next::{NotaDecode, NotaEncode, NotaSource};
use rkyv::{Archive, Deserialize as RkyvDeserialize, Serialize as RkyvSerialize};
use signal_orchestrate::WirePath;

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

#[derive(Archive, RkyvSerialize, RkyvDeserialize, Debug, Clone, PartialEq, Eq)]
struct StartupConfiguration {
    store_path: WirePath,
    ordinary_socket_path: WirePath,
    meta_socket_path: WirePath,
    upgrade_socket_path: WirePath,
    workspace_root: WirePath,
    git_index_root: WirePath,
}

struct DaemonProcess {
    executable: PathBuf,
    configuration: StartupConfiguration,
    configuration_path: PathBuf,
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
        DaemonProcess::new(self)?.spawn()?;
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
        let output = Command::new(self.client_executable())
            .env("PERSONA_ORCHESTRATE_SOCKET", &self.ordinary_socket_path)
            .arg(request.to_nota())
            .output()?;
        if !output.status.success() {
            return Err(Error::ClientFailed {
                status: output.status.to_string(),
                stderr: String::from_utf8_lossy(&output.stderr).trim().to_string(),
            });
        }
        String::from_utf8(output.stdout).map_err(Error::ClientOutputUtf8)
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

    fn startup_configuration_path(&self) -> PathBuf {
        self.workspace_root
            .join("orchestrate")
            .join("orchestrate-daemon.signal")
    }

    fn daemon_executable(&self) -> PathBuf {
        self.component_root
            .join("target")
            .join("release")
            .join("orchestrate-daemon")
    }

    fn client_executable(&self) -> PathBuf {
        self.component_root
            .join("target")
            .join("release")
            .join("orchestrate")
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
                "--features",
                "nota-text",
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

impl StartupConfiguration {
    fn from_client(client: &OrchestrateDaemonClient) -> Result<Self> {
        Ok(Self {
            store_path: WirePath::from_absolute_path(client.store_path.display().to_string())?,
            ordinary_socket_path: WirePath::from_absolute_path(
                client.ordinary_socket_path.display().to_string(),
            )?,
            meta_socket_path: WirePath::from_absolute_path(
                client.meta_socket_path.display().to_string(),
            )?,
            upgrade_socket_path: WirePath::from_absolute_path(
                client.upgrade_socket_path.display().to_string(),
            )?,
            workspace_root: WirePath::from_absolute_path(
                client.workspace_root.display().to_string(),
            )?,
            git_index_root: WirePath::from_absolute_path(
                client.git_index_root.display().to_string(),
            )?,
        })
    }

    fn to_signal_bytes(&self) -> Result<Vec<u8>> {
        rkyv::to_bytes::<rkyv::rancor::Error>(self)
            .map(|bytes| bytes.to_vec())
            .map_err(|_| Error::StartupConfigurationEncode)
    }
}

impl DaemonProcess {
    fn new(client: &OrchestrateDaemonClient) -> Result<Self> {
        Ok(Self {
            executable: client.daemon_executable(),
            configuration: StartupConfiguration::from_client(client)?,
            configuration_path: client.startup_configuration_path(),
            log_path: client.daemon_log_path(),
        })
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
        if let Some(parent) = self.configuration_path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        std::fs::write(&self.configuration_path, self.configuration.to_signal_bytes()?)?;
        let log = OpenOptions::new()
            .create(true)
            .append(true)
            .open(&self.log_path)?;
        let error_log = log.try_clone()?;
        let mut command = Command::new(&self.executable);
        command
            .arg(&self.configuration_path)
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
        Ok(NotaSource::new(self.text.trim()).parse::<Reply>()?)
    }
}
