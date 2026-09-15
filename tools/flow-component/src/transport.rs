use crate::FlowNexusBoundary;
use nexus::Permissive;
use std::{fs, io::{Read, Write}, os::unix::{fs::PermissionsExt, net::{UnixListener, UnixStream}}, path::{Path, PathBuf}};

/// A temporary Nexus-shaped transport. It binds distinct ordinary and meta
/// Unix sockets with the modes supplied by the real `nexus` authority types.
/// Persistence, daemon lifecycle, peer credential checks, and request routing
/// belong to the future Flow Nexus, not this launch prototype.
pub struct TemporaryNexus {
    ordinary: UnixListener,
    meta: UnixListener,
    ordinary_path: PathBuf,
    meta_path: PathBuf,
}

impl TemporaryNexus {
    pub fn bind(directory: &Path) -> Result<Self, String> {
        fs::create_dir_all(directory).map_err(|error| format!("create temporary Nexus directory: {error}"))?;
        let ordinary_path = directory.join("ordinary.sock");
        let meta_path = directory.join("meta.sock");
        let _ = fs::remove_file(&ordinary_path);
        let _ = fs::remove_file(&meta_path);
        let boundary = FlowNexusBoundary::default();
        let ordinary = UnixListener::bind(&ordinary_path).map_err(|error| format!("bind ordinary socket: {error}"))?;
        let meta = UnixListener::bind(&meta_path).map_err(|error| format!("bind meta socket: {error}"))?;
        fs::set_permissions(&ordinary_path, fs::Permissions::from_mode(boundary.ordinary.mode())).map_err(|error| format!("set ordinary socket mode: {error}"))?;
        fs::set_permissions(&meta_path, fs::Permissions::from_mode(boundary.meta.mode())).map_err(|error| format!("set meta socket mode: {error}"))?;
        Ok(Self { ordinary, meta, ordinary_path, meta_path })
    }
    pub fn ordinary_path(&self) -> &Path { &self.ordinary_path }
    pub fn meta_path(&self) -> &Path { &self.meta_path }
    pub fn receive_ordinary(&self) -> Result<Vec<u8>, String> { receive(&self.ordinary) }
    pub fn receive_meta(&self) -> Result<Vec<u8>, String> { receive(&self.meta) }
}

impl Drop for TemporaryNexus {
    fn drop(&mut self) { let _ = fs::remove_file(&self.ordinary_path); let _ = fs::remove_file(&self.meta_path); }
}

pub fn send(path: &Path, frame: &[u8]) -> Result<(), String> {
    let mut stream = UnixStream::connect(path).map_err(|error| format!("connect Signal transport: {error}"))?;
    let length = u32::try_from(frame.len()).map_err(|_| "Signal frame too large")?;
    stream.write_all(&length.to_be_bytes()).and_then(|_| stream.write_all(frame)).map_err(|error| format!("write Signal transport: {error}"))
}

fn receive(listener: &UnixListener) -> Result<Vec<u8>, String> {
    let (mut stream, _) = listener.accept().map_err(|error| format!("accept Signal transport: {error}"))?;
    let mut length = [0_u8; 4];
    stream.read_exact(&mut length).map_err(|error| format!("read Signal length: {error}"))?;
    let length = u32::from_be_bytes(length) as usize;
    if length > 16 * 1024 * 1024 { return Err("Signal frame exceeds 16 MiB".into()); }
    let mut frame = vec![0; length];
    stream.read_exact(&mut frame).map_err(|error| format!("read Signal frame: {error}"))?;
    Ok(frame)
}
