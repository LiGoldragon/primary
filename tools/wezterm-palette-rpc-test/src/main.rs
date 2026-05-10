use std::path::PathBuf;
use std::time::{Duration, Instant};

use codec::SetPalette;
use config::UnixDomain;
use error::{Error, Result};
use mux::connui::ConnectionUI;
use mux::pane::PaneId;
use wezterm_client::client::Client;
use wezterm_term::color::{ColorPalette, RgbColor, SrgbaTuple};

mod error;

struct ProbeSettings {
    socket: PathBuf,
    pane_id: PaneId,
    restore_after: Option<Duration>,
    palette: ProbePalette,
}

impl ProbeSettings {
    fn from_args() -> Result<Self> {
        let mut socket = None;
        let mut pane_id = None;
        let mut restore_after = Some(Duration::from_millis(1200));
        let mut palette = ProbePalette::Magenta;

        let mut args = std::env::args().skip(1);
        while let Some(arg) = args.next() {
            match arg.as_str() {
                "--socket" => {
                    let value = args.next().ok_or(Error::MissingArgument("--socket"))?;
                    socket = Some(PathBuf::from(value));
                }
                "--pane-id" => {
                    let value = args.next().ok_or(Error::MissingArgument("--pane-id"))?;
                    pane_id = Some(
                        value
                            .parse()
                            .map_err(|source| Error::InvalidPaneId { value, source })?,
                    );
                }
                "--palette" => {
                    let value = args.next().ok_or(Error::MissingArgument("--palette"))?;
                    palette = ProbePalette::from_name(&value)?;
                }
                "--restore-after-ms" => {
                    let value = args
                        .next()
                        .ok_or(Error::MissingArgument("--restore-after-ms"))?;
                    restore_after = if value == "never" {
                        None
                    } else {
                        Some(Duration::from_millis(value.parse().map_err(|source| {
                            Error::InvalidRestoreDelay { value, source }
                        })?))
                    };
                }
                "--help" | "-h" => {
                    Self::print_usage();
                    std::process::exit(0);
                }
                _ => return Err(Error::UnknownArgument(arg)),
            }
        }

        Ok(Self {
            socket: socket.ok_or(Error::RequiredArgument("--socket"))?,
            pane_id: pane_id.ok_or(Error::RequiredArgument("--pane-id"))?,
            restore_after,
            palette,
        })
    }

    fn print_usage() {
        eprintln!(
            "usage: wezterm-palette-rpc-test --socket PATH --pane-id N \
             [--palette magenta|cyan] [--restore-after-ms N|never]\n\
             \n\
             This uses WezTerm's internal SetPalette RPC. It does not send OSC \
             and does not write to /dev/pts. Run only against a disposable test pane."
        );
    }

    async fn run(self) -> Result<()> {
        let mut ui = ConnectionUI::new_headless();
        let domain = UnixDomain {
            name: "chroma-palette-rpc-test".to_string(),
            socket_path: Some(self.socket.clone()),
            no_serve_automatically: true,
            ..Default::default()
        };
        let client =
            Client::new_unix_domain(None, &domain, true, &mut ui, true).map_err(|source| {
                Error::Connection {
                    socket: self.socket.display().to_string(),
                    reason: source.to_string(),
                }
            })?;

        let probe_palette = self.palette.color_palette();
        let accepted = PaletteApplication {
            client: &client,
            pane_id: self.pane_id,
            palette: probe_palette,
            label: PaletteApplicationLabel::Probe,
        }
        .apply()
        .await?;
        println!("probe accepted in {} ms", accepted.as_millis());

        if let Some(delay) = self.restore_after {
            smol::Timer::after(delay).await;
            let accepted = PaletteApplication {
                client: &client,
                pane_id: self.pane_id,
                palette: ColorPalette::default(),
                label: PaletteApplicationLabel::DefaultRestore,
            }
            .apply()
            .await?;
            println!("default restore accepted in {} ms", accepted.as_millis());
        }

        Ok(())
    }
}

struct PaletteApplication<'client> {
    client: &'client Client,
    pane_id: PaneId,
    palette: ColorPalette,
    label: PaletteApplicationLabel,
}

impl<'client> PaletteApplication<'client> {
    async fn apply(self) -> Result<Duration> {
        let started = Instant::now();
        self.client
            .set_configured_palette_for_pane(SetPalette {
                pane_id: self.pane_id,
                palette: self.palette,
            })
            .await
            .map_err(|source| Error::PaletteApplication {
                label: self.label.as_str().to_string(),
                pane_id: self.pane_id.to_string(),
                reason: source.to_string(),
            })?;
        Ok(started.elapsed())
    }
}

enum PaletteApplicationLabel {
    Probe,
    DefaultRestore,
}

impl PaletteApplicationLabel {
    fn as_str(&self) -> &'static str {
        match self {
            Self::Probe => "probe",
            Self::DefaultRestore => "default-restore",
        }
    }
}

enum ProbePalette {
    Magenta,
    Cyan,
}

impl ProbePalette {
    fn from_name(name: &str) -> Result<Self> {
        match name {
            "magenta" => Ok(Self::Magenta),
            "cyan" => Ok(Self::Cyan),
            _ => Err(Error::UnknownPalette(name.to_string())),
        }
    }

    fn color_palette(&self) -> ColorPalette {
        self.sample().to_color_palette()
    }

    fn sample(&self) -> PaletteSample {
        match self {
            Self::Magenta => PaletteSample {
                background: Rgb8 {
                    red: 0x22,
                    green: 0x10,
                    blue: 0x28,
                },
                foreground: Rgb8 {
                    red: 0xff,
                    green: 0xd7,
                    blue: 0xff,
                },
                accent: Rgb8 {
                    red: 0xff,
                    green: 0x66,
                    blue: 0xcc,
                },
            },
            Self::Cyan => PaletteSample {
                background: Rgb8 {
                    red: 0x06,
                    green: 0x20,
                    blue: 0x24,
                },
                foreground: Rgb8 {
                    red: 0xd8,
                    green: 0xff,
                    blue: 0xff,
                },
                accent: Rgb8 {
                    red: 0x00,
                    green: 0xcc,
                    blue: 0xcc,
                },
            },
        }
    }
}

struct PaletteSample {
    background: Rgb8,
    foreground: Rgb8,
    accent: Rgb8,
}

impl PaletteSample {
    fn to_color_palette(&self) -> ColorPalette {
        let mut palette = ColorPalette::default();
        let background = self.background.to_srgba_tuple();
        let foreground = self.foreground.to_srgba_tuple();
        let accent = self.accent.to_srgba_tuple();

        palette.background = background;
        palette.foreground = foreground;
        palette.cursor_bg = accent;
        palette.cursor_fg = background;
        palette.cursor_border = accent;
        palette.selection_bg = accent;
        palette.selection_fg = background;
        palette.colors.0[0] = background;
        palette.colors.0[7] = foreground;
        palette.colors.0[8] = Rgb8 {
            red: 0x66,
            green: 0x66,
            blue: 0x66,
        }
        .to_srgba_tuple();
        palette.colors.0[15] = foreground;
        palette
    }
}

#[derive(Clone, Copy)]
struct Rgb8 {
    red: u8,
    green: u8,
    blue: u8,
}

impl Rgb8 {
    fn to_srgba_tuple(self) -> SrgbaTuple {
        RgbColor::new_8bpc(self.red, self.green, self.blue).into()
    }
}

fn main() -> Result<()> {
    let settings = ProbeSettings::from_args().inspect_err(|_| ProbeSettings::print_usage())?;
    smol::block_on(settings.run())
}
