from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Analytics(Base):
    __tablename__ = "analytics"

    metric: Mapped[str] = mapped_column(
        String(50),
        primary_key=True,
    )

    value: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )