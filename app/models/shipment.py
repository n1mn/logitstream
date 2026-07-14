from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )

    shipment_id: Mapped[str] = mapped_column(
        String(50),
        unique=True, 
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
    )

    origin: Mapped[str] = mapped_column(
        String(100),
    )

    destination: Mapped[str] = mapped_column(
        String(100),
    )