import enum
from typing import Optional
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class CompanyState(enum.Enum):
    NEW = "new"
    DATA_RETRIEVED = "data_retreived"
    DATA_UNAVAILABLE = "data_unavailable"


class Company(Base):
    __tablename__ = "company"
    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True)
    name: Mapped[str] = mapped_column(String(512))
    nip: Mapped[int] = mapped_column(Integer, unique=True)
    email: Mapped[Optional[str]]
    phone: Mapped[Optional[str]]
    status: Mapped[CompanyState]
    contacted: Mapped[bool] = mapped_column(Boolean)
    
    def __repr__(self) -> str:
        return f"Company(id={self.id!r}, name={self.name!r}, email={self.email!r}, phone={self.phone!r})"


def dict_to_company(dictionary):
    company = Company()
    company.uuid = dictionary["id"]
    company.name = dictionary["nazwa"]
    company.nip = dictionary["wlasciciel"]["nip"]
    company.email = "NONE"
    company.phone = "NONE"
    company.status = CompanyState.NEW
    company.contacted = False
    return company
