from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.ledger_entry import LedgerEntry


def get_by_transaction_id(
    db: Session,
    transaction_id: UUID,
) -> list[LedgerEntry]:
    statement = select(LedgerEntry).where(
        LedgerEntry.transaction_id == transaction_id
    )
    return list(db.scalars(statement).all())


def create_many(
    db: Session,
    entries: list[LedgerEntry],
) -> list[LedgerEntry]:
    db.add_all(entries)
    db.flush()
    return entries
