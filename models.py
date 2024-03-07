from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass

class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36))
    name: Mapped[str] = mapped_column(String(30))  # TODO: Max length of the name?
    nip: Mapped[int] = mapped_column(Integer)
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    contacted: Mapped[bool] = mapped_column(Boolean)
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"


def toggle_contacted_state():
    pass

