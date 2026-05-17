//! Plain-text rendering — byte-compatible with the shell helper.
//!
//! Tests and existing agents parse the shell's `print_state` output:
//! `--- <lane>.lock ---\n` headers, `(idle)\n` for empty locks, the
//! verbatim file contents otherwise, then `--- open beads ---` plus
//! the `bd` listing.
//!
//! BEADS output is intentionally not rendered through the `Write`
//! abstraction — `bd` writes its "Showing N issues" footer to stderr,
//! and the shell helper relies on the subprocess' stderr passthrough
//! to surface that footer. The bin layer runs `bd` with inherited
//! stdio so the byte stream matches.

use std::fmt::Write;

use crate::claim::{ClaimOutcome, ClaimOverlapDescription, StatusReport};

pub fn render_lock_state(report: &StatusReport, mut out: impl Write) -> std::fmt::Result {
    for lane_status in &report.lanes {
        writeln!(out, "--- {}.lock ---", lane_status.lane)?;
        if lane_status.lock.is_idle() {
            writeln!(out, "(idle)")?;
        } else {
            let rendered = lane_status.lock.render();
            // render() already terminates each entry with '\n' so the
            // block matches `cat <lock-file>` exactly.
            out.write_str(&rendered)?;
        }
    }
    writeln!(out, "--- open beads ---")?;
    Ok(())
}

pub fn render_claim_conflict(
    overlap: &ClaimOverlapDescription,
    mut out: impl Write,
) -> std::fmt::Result {
    writeln!(
        out,
        "Conflict: {} overlaps {} (held by {})",
        overlap.own_scope, overlap.peer_scope, overlap.peer_lane
    )
}

pub fn render_outcome_claim_conflicts(
    outcome: &ClaimOutcome,
    mut stderr: impl Write,
    mut stdout: impl Write,
) -> std::fmt::Result {
    if let ClaimOutcome::Rejected { overlaps, .. } = outcome {
        for overlap in overlaps {
            render_claim_conflict(overlap, &mut stderr)?;
        }
        writeln!(stdout, "Claim cleared because of overlap.")?;
    }
    Ok(())
}
