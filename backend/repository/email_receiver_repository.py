

from typing import Iterable

from sqlalchemy import Engine
from sqlmodel import Session, select

from repository.models import EmailReceiver


class EmailReceiverRepository:
    def __init__(self, sql_engine: Engine) -> None:
        self.engine = sql_engine
        
    def save(self, email_receiver: EmailReceiver) -> None:
        with Session(self.engine) as session:
            session.add(email_receiver)
            session.commit()
            
    def find_all(self) -> Iterable[EmailReceiver]:
        with Session(self.engine) as session:
            statement = select(EmailReceiver)
            results = session.exec(statement)
            return results.all()
            
            