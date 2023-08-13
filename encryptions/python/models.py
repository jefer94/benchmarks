from datetime import datetime
from typing import Optional
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

class Token(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[int] = mapped_column(Integer())
    exp: Mapped[datetime] = Column(DateTime())
    token: Mapped[str] = Column(String())
    rand: Mapped[int] = Column(String())

    def __repr__(self) -> str:
        return 