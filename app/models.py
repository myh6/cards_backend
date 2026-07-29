from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    member: Mapped[str] = mapped_column(String(50))
    set_name: Mapped[str] = mapped_column(String(100))
    condition: Mapped[str] = mapped_column(String(20), default="mint")
    acquired_on: Mapped[date | None] = mapped_column(Date, nullable=True)
    owner_id: Mapped[int | None] = mapped_column(
        Integer, index=True, nullable=True
    )

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index= True
    )
    hashed_password: Mapped[str] = mapped_column(String(255))