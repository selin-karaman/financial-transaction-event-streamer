from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.transaction import Transaction


def get_by_id(db: Session, transaction_id: UUID) -> Transaction | None:
    statement = select(Transaction).where(
        Transaction.id == transaction_id
    )
    return db.scalar(statement)


def get_by_idempotency_key(
    db: Session,
    idempotency_key: str,
) -> Transaction | None:
    statement = select(Transaction).where(
        Transaction.idempotency_key == idempotency_key
    )
    return db.scalar(statement)


def create(db: Session, transaction: Transaction) -> Transaction:
    db.add(transaction)
    db.flush()
    return transaction
