from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from loguru import logger
from sqlalchemy import Engine, create_engine

from sqlmodel import Field, SQLModel
import time

class EnvironmentVariable(SQLModel, table= True):
    temperature: float
    humidity: float
    timestamp: Optional[int] = Field(default_factory= time.time, nullable= False)
    id: Optional[UUID] = Field(default_factory= uuid4, primary_key= True, nullable= False)

    def to_dict(self) -> dict[str, float]:
        return self.__dict__



def init_database() -> Engine:
    SQLALCHEMY_DATABASE_URL = "postgresql://sram-admin:sramsram-admin@sensor-db:5432/db"

    # connection_url = f'postgresql://{params["user"]}:{params["password"]}@{params["host"]}:{params["port"]}/{params["dbname"]}'
    logger.info("[INIT DATABASE] Initializing database...")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    return engine