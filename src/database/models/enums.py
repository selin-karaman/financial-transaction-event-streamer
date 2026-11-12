from enum import Enum


class AccountStatus(str, Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"
    CLOSED = "closed"


class TransactionType(str, Enum):
    TRANSFER = "transfer"


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class LedgerEntryType(str, Enum):
    DEBIT = "debit"
    CREDIT = "credit"


class OutboxStatus(str, Enum):
    PENDING = "pending"
    PUBLISHED = "published"
