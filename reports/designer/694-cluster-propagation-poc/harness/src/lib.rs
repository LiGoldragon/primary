//! Cluster-propagation PoC harness (report 694).
//!
//! One process, three logical "machines" (A producer, B/C acquirers). The
//! cluster is the *logic* of admission + type-fan + acquire, not three kernels;
//! physical multi-host is system-operator's downstream leg.
//!
//! The boundary is drawn at TRANSPORT, never at LOGIC. REAL on the falsifiable
//! line: criome's `is_valid_majority` k>n/2 guard, the distinct-signer tally,
//! real `blst` BLS sign/verify, the attested-moment window, the `ermr`
//! admission gate, content-addressed `database_marker` interchangeability, the
//! router type matcher `matches_interest`, and acquire+import. CUT to
//! in-process: cross-host sockets, cross-criome peer signature solicitation,
//! BLS aggregation, production cluster-root ceremony.
//!
//! The three legs live in `criome_quorum`, `spirit_propagation`,
//! `router_fanout`; the propagation glue (`From<criome ref> for
//! signal_standard ref`) lives in `glue`. The falsifiable end-to-end test is
//! `tests/end_to_end.rs`.

pub mod criome_quorum;
pub mod glue;
pub mod router_fanout;
pub mod spirit_propagation;

/// The three logical machines of the principal's self-quorum (`p3td`): each
/// principal runs more than one node, so a threshold of *your own* nodes is
/// what authorizes the new head.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Machine {
    A,
    B,
    C,
}

impl Machine {
    /// The principal-name a machine signs under as a cluster member.
    pub fn principal_name(self) -> &'static str {
        match self {
            Machine::A => "machine-a",
            Machine::B => "machine-b",
            Machine::C => "machine-c",
        }
    }
}
