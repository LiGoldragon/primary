#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("{0} needs a value")]
    MissingArgument(&'static str),

    #[error("missing {0}")]
    RequiredArgument(&'static str),

    #[error("--pane-id must be a number, got {value:?}: {source}")]
    InvalidPaneId {
        value: String,
        source: std::num::ParseIntError,
    },

    #[error("--restore-after-ms must be a number or never, got {value:?}: {source}")]
    InvalidRestoreDelay {
        value: String,
        source: std::num::ParseIntError,
    },

    #[error("unknown argument: {0}")]
    UnknownArgument(String),

    #[error("unknown palette {0}; expected magenta or cyan")]
    UnknownPalette(String),

    #[error("connecting to {socket} failed: {reason}")]
    Connection { socket: String, reason: String },

    #[error("{label} SetPalette RPC failed for pane {pane_id}: {reason}")]
    PaletteApplication {
        label: String,
        pane_id: String,
        reason: String,
    },
}

pub type Result<T> = std::result::Result<T, Error>;
