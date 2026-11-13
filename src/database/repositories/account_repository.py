from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database.models.account import Account


def get_by_id(db: Session, account_id: UUID) -> Account | None:
    statement = select(Account).where(Account.id == account_id)
    return db.scalar(statement)


def get_by_id_for_update(
    db: Session,
    account_id: UUID,
) -> Account | None:
    statement = (
        select(Account)
        .where(Account.id == account_id)
        .with_for_update()
    )
    return db.scalar(statement)


def get_by_account_number(
    db: Session,
    account_number: str,
) -> Account | None:
    statement = select(Account).where(
        Account.account_number == account_number
    )
    return db.scalar(statement)


def create(db: Session, account: Account) -> Account:
    db.add(account)
    db.flush()
    return account
