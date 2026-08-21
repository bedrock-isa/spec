use thiserror::Error;

pub type BusResult<T> = Result<T, BusError>;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum BusFailureCause {
    NoResponder = 0,
    AccessDenied = 1,
    Timeout = 2,
    DataError = 3,
    Other = 4,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RetrySafety {
    RetrySafe,
    EffectMayHaveOccurred,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct AcknowledgedBusFailure {
    pub cause: BusFailureCause,
    pub final_address: u64,
    pub retry_safety: RetrySafety,
}

impl AcknowledgedBusFailure {
    pub const fn new(
        cause: BusFailureCause,
        final_address: u64,
        retry_safety: RetrySafety,
    ) -> Self {
        Self {
            cause,
            final_address,
            retry_safety,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum BusError {
    #[error("address 0x{addr:016x} is out of range")]
    OutOfRange { addr: u64 },
    #[error("address 0x{addr:016x} is unmapped")]
    Unmapped { addr: u64 },
    #[error("address range 0x{start:016x}..0x{end:016x} is invalid")]
    InvalidRange { start: u64, end: u64 },
    #[error("address 0x{addr:016x} is read-only")]
    ReadOnly { addr: u64 },
    #[error("device error at 0x{addr:016x}: {message}")]
    Device { addr: u64, message: String },
    #[error("a bus transaction is already active")]
    TransactionActive,
    #[error("no bus transaction is active")]
    NoTransaction,
}

impl BusError {
    /// Rebases device-local addresses by `base` without wrapping.
    ///
    /// Lifecycle errors do not carry an address and are returned unchanged.
    /// `None` indicates that at least one address overflowed while rebasing.
    pub fn checked_rebase(self, base: u64) -> Option<Self> {
        match self {
            Self::OutOfRange { addr } => {
                base.checked_add(addr).map(|addr| Self::OutOfRange { addr })
            }
            Self::Unmapped { addr } => base.checked_add(addr).map(|addr| Self::Unmapped { addr }),
            Self::InvalidRange { start, end } => Some(Self::InvalidRange {
                start: base.checked_add(start)?,
                end: base.checked_add(end)?,
            }),
            Self::ReadOnly { addr } => base.checked_add(addr).map(|addr| Self::ReadOnly { addr }),
            Self::Device { addr, message } => base
                .checked_add(addr)
                .map(|addr| Self::Device { addr, message }),
            error @ (Self::TransactionActive | Self::NoTransaction) => Some(error),
        }
    }

    /// Rebases a device-local error, reporting an overflowing rebase at the
    /// original bus request address.
    pub fn rebase_or_out_of_range(self, base: u64, request_address: u64) -> Self {
        self.checked_rebase(base).unwrap_or(Self::OutOfRange {
            addr: request_address,
        })
    }
}
